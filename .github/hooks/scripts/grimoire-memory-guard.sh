#!/usr/bin/env bash
# grimoire-memory-guard.sh — PreToolUse hook
# Protege les fichiers memoire Grimoire contre les ecritures accidentelles.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
policy_script="$project_root/.github/hooks/lib/guardrail-policy.py"
policy_python="$project_root/.venv/bin/python"
input=$(cat)

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -z "$policy_python" || ! -f "$policy_script" ]]; then
  echo "{}"
  exit 0
fi

if ! output=$(printf '%s' "$input" | "$policy_python" "$policy_script" memory-guard 2>/dev/null); then
  echo "{}"
  exit 0
fi

# V1 ledger: scope=tool, phase=block si policy a bloque, sinon info.
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  phase="info"
  if [[ "$output" == *'"decision"'*'"block"'* || "$output" == *'"permissionDecision"'*'"deny"'* ]]; then
    phase="block"
  fi
  "$emit_event_script" --scope tool --phase "$phase" --source-hook "grimoire-memory-guard.sh" --payload-json '{"hook":"memory-guard"}' 2>/dev/null || true
fi

printf '%s\n' "$output"
