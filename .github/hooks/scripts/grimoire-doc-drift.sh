#!/usr/bin/env bash
# grimoire-doc-drift.sh — PostToolUse hook (Phase 3).
# Detecte si le fichier modifie est declare comme source d'une doc miroir.
#  - drift `blocking` -> permissionDecision: deny (l'edit est refuse)
#  - drift `enforcing`/`info` -> additionalContext (non-bloquant, juste informatif)
#
# stdin  : JSON VS Code Copilot PostToolUse
# stdout : `{}` | `{"additionalContext": "..."}` | `{"permissionDecision":"deny","reason":"..."}`
# exit 0 toujours (fail-open si le detecteur casse — jamais de blocage fantome)

set -euo pipefail

input=$(cat)
project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
kit_root="$project_root/grimoire-kit"
detector="$kit_root/framework/tools/doc-drift-detector.py"
python_bin="$kit_root/.venv/bin/python"

if [[ ! -x "$python_bin" ]]; then
  python_bin="$(command -v python3 || true)"
fi

if [[ -z "$python_bin" || ! -f "$detector" ]]; then
  echo "{}"
  exit 0
fi

export GRIMOIRE_PROJECT_ROOT="$project_root"
export GRIMOIRE_HOOK_INPUT="$input"

file_path=$("$python_bin" - <<'PY' 2>/dev/null
import json, os, sys
try:
    payload = json.loads(os.environ.get("GRIMOIRE_HOOK_INPUT") or "{}")
except Exception:
    sys.exit(0)
ti = payload.get("tool_input") or payload.get("toolInput") or {}
if not isinstance(ti, dict):
    sys.exit(0)
raw = ti.get("filePath") or ti.get("file_path") or ""
if not raw:
    sys.exit(0)
pr = os.environ.get("GRIMOIRE_PROJECT_ROOT", "")
if pr and raw.startswith(pr):
    raw = raw[len(pr):].lstrip("/")
if raw.startswith("grimoire-kit/"):
    raw = raw[len("grimoire-kit/"):]
print(raw)
PY
) || file_path=""

if [[ -z "$file_path" ]]; then
  echo "{}"
  exit 0
fi

drift_json=$(cd "$kit_root" && "$python_bin" "$detector" --project-root . --files "$file_path" --json 2>/dev/null) || true
if [[ -z "$drift_json" ]]; then
  echo "{}"
  exit 0
fi

export GRIMOIRE_DRIFT_JSON="$drift_json"

result=$("$python_bin" - <<'PY' 2>/dev/null
import json, os, sys
try:
    data = json.loads(os.environ.get("GRIMOIRE_DRIFT_JSON") or "{}")
except Exception:
    print("{}")
    sys.exit(0)
drifts = data.get("drifts") or []
if not drifts:
    print("{}")
    sys.exit(0)

by_sev = {"blocking": [], "enforcing": [], "info": []}
for d in drifts:
    by_sev.setdefault(d.get("severity", "info"), []).append(d)

# Phase 3 : un drift blocking => deny. Sinon => additionalContext.
if by_sev["blocking"]:
    lines = ["DOC-DRIFT BLOQUANT — la doc miroir critique doit etre mise a jour AVANT cette edition :"]
    for d in by_sev["blocking"]:
        lines.append(f"  [BLOCKING] {d['source']}  ->  {d['mirror']}")
    lines.append("")
    lines.append("Cette regle est declaree blocking dans doc-manifest.yaml car le source porte des contrats critiques (ex: ADR-001).")
    lines.append("Action : mettre a jour la doc miroir, puis retenter l'edition.")
    lines.append("Check  : cd grimoire-kit && .venv/bin/python framework/tools/doc-drift-detector.py --project-root . --since HEAD")
    print(json.dumps({
        "permissionDecision": "deny",
        "reason": "\n".join(lines),
    }))
    sys.exit(0)

lines = ["DOC-DRIFT detecte — la doc miroir n'a pas ete mise a jour :"]
for sev in ("enforcing", "info"):
    for d in by_sev.get(sev, []):
        tag = {"enforcing": "[ENFORCE]", "info": "[INFO]"}[sev]
        lines.append(f"  {tag} {d['source']}  ->  {d['mirror']}")
lines.append("")
lines.append("Action : mettre a jour la doc miroir avant cloture.")
lines.append("Check  : cd grimoire-kit && .venv/bin/python framework/tools/doc-drift-detector.py --project-root . --since HEAD")
print(json.dumps({"additionalContext": "\n".join(lines)}))
PY
) || result="{}"

printf '%s\n' "$result"
