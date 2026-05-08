#!/usr/bin/env bash
# grimoire-hooks-smoke.sh
# Verifie les manifests hooks, la syntaxe shell des scripts et les drapeaux
# workspace necessaires a l'activation des hooks Grimoire.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
hook_dir="$project_root/.github/hooks"
script_dir="$hook_dir/scripts"
settings_file="$project_root/.vscode/settings.json"
gate_python="$project_root/grimoire-kit/.venv/bin/python"

if [[ ! -x "$gate_python" ]]; then
    gate_python="$(command -v python3 || true)"
fi

echo "[hooks-smoke] validate hook manifests"
python3 - "$hook_dir" <<'PY'
import json
import os
import shlex
import sys
from pathlib import Path

hook_dir = Path(sys.argv[1]).resolve()
project_root = hook_dir.parents[1]
errors: list[str] = []

for manifest in sorted(hook_dir.glob("*.json")):
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{manifest.relative_to(project_root)}: JSON invalide ({exc.msg} a la ligne {exc.lineno})")
        continue

    hooks = payload.get("hooks")
    if not isinstance(hooks, dict) or not hooks:
        errors.append(f"{manifest.relative_to(project_root)}: objet hooks manquant ou vide")
        continue

    for event_name, commands in hooks.items():
        if not isinstance(commands, list) or not commands:
            errors.append(f"{manifest.relative_to(project_root)}: liste vide pour {event_name}")
            continue
        for index, command_entry in enumerate(commands, start=1):
            if not isinstance(command_entry, dict):
                errors.append(f"{manifest.relative_to(project_root)}: entree {event_name}[{index}] invalide")
                continue
            command = str(command_entry.get("command") or "").strip()
            if not command:
                errors.append(f"{manifest.relative_to(project_root)}: commande manquante pour {event_name}[{index}]")
                continue
            token = shlex.split(command)[0]
            if token.startswith("."):
                target = (project_root / token).resolve()
                if not target.exists():
                    errors.append(f"{manifest.relative_to(project_root)}: cible inexistante {target.relative_to(project_root)}")
                elif target.suffix == ".sh" and not os.access(target, os.X_OK):
                    errors.append(f"{manifest.relative_to(project_root)}: script non executable {target.relative_to(project_root)}")

if errors:
    for entry in errors:
        print(entry)
    raise SystemExit(1)
PY

echo "[hooks-smoke] validate hook shell syntax"
for script in "$script_dir"/*.sh; do
  bash -n "$script"
done

echo "[hooks-smoke] inspect hook promotion registry"
"$gate_python" "$project_root/grimoire-kit/framework/tools/hook-safety-gate.py" --project-root "$project_root" status

echo "[hooks-smoke] validate workspace settings flags"
grep -q '"chat.useCustomizationsInParentRepositories": true' "$settings_file"
grep -q '"chat.useCustomAgentHooks": true' "$settings_file"

echo "[hooks-smoke] ok"