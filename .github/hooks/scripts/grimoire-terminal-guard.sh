#!/usr/bin/env bash
# grimoire-terminal-guard.sh — PreToolUse hook
# Valide les commandes shell générées par les LLM avant exécution :
# quotes non équilibrées, commandes trop longues, patterns crashants.
# Mode: shadow → warn-only, jamais bloquant.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
policy_script="$project_root/grimoire-kit/framework/tools/terminal-guard-policy.py"
policy_python="$project_root/grimoire-kit/.venv/bin/python"
input=$(cat)

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -z "$policy_python" || ! -f "$policy_script" ]]; then
  echo "{}"
  exit 0
fi

if ! output=$(printf '%s' "$input" | "$policy_python" "$policy_script" 2>/dev/null); then
  echo "{}"
  exit 0
fi

emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  phase="info"
  if [[ "$output" == *'"decision"'*'"block"'* ]]; then
    phase="block"
  elif [[ "$output" == *'"message"'* ]]; then
    phase="correct"
  fi
  "$emit_event_script" \
    --scope tool --phase "$phase" \
    --source-hook "grimoire-terminal-guard.sh" \
    --payload-json '{"hook":"terminal-guard"}' 2>/dev/null || true
fi

printf '%s\n' "$output"
