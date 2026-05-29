#!/usr/bin/env bash
# grimoire-memory-gate.sh — PostToolUse hook for Memory OS projection drift.
# Runs a soft, no-sync verification only when memory/code/task surfaces changed.

set -euo pipefail

cat >/dev/null || true

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
kit_dir="$project_root/grimoire-kit"
python_bin="$kit_dir/.venv/bin/python"

if [[ "${GRIMOIRE_MEMORY_GATE_HOOK:-auto}" == "off" ]]; then
  echo "{}"
  exit 0
fi

if [[ ! -f "$kit_dir/project-context.yaml" ]]; then
  echo "{}"
  exit 0
fi

if [[ ! -x "$python_bin" ]]; then
  python_bin="$(command -v python3 || true)"
fi

if [[ -z "$python_bin" ]]; then
  echo "{}"
  exit 0
fi

changed_files="$(
  {
    git -C "$project_root" diff --name-only HEAD -- 2>/dev/null || true
    git -C "$project_root" ls-files --others --exclude-standard 2>/dev/null || true
  } | sort -u
)"

if [[ "${GRIMOIRE_MEMORY_GATE_HOOK:-auto}" == "auto" ]]; then
  if [[ -z "$changed_files" ]]; then
    echo "{}"
    exit 0
  fi
  if ! printf '%s\n' "$changed_files" | grep -E '^(grimoire-kit/src/grimoire/(memory|codegraph|missions|evidence)/|grimoire-kit/tests/(unit/)?(memory|unit/test_codegraph|unit/test_missions|unit/test_evidence)|grimoire-kit/project-context.yaml|grimoire-kit/_grimoire/_memory/migration/|_grimoire-runtime-output/(ledger|evidence)/|docker-compose\.memory-target\.yml)' >/dev/null; then
    echo "{}"
    exit 0
  fi
fi

cd "$kit_dir"

gate_output="$(
  "$python_bin" -m grimoire -o json memory gate --soft --skip-migration --no-sync --skip-vectors 2>&1 || true
)"

if printf '%s' "$gate_output" | "$python_bin" -c 'import json,sys; data=json.load(sys.stdin); raise SystemExit(0 if data.get("ok") else 1)' 2>/dev/null; then
  echo "{}"
  exit 0
fi

summary="$(printf '%s' "$gate_output" | tr '\n' ' ' | cut -c 1-360)"
"$python_bin" -c 'import json,sys; print(json.dumps({"continue": True, "systemMessage": "Memory OS gate shadow: " + sys.argv[1]}))' "$summary"
