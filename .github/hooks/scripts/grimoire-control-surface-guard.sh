#!/usr/bin/env bash
# grimoire-control-surface-guard.sh — PreToolUse hook
# Applique des garde-fous sur les surfaces de controle agentiques et les
# patterns de commande destructifs.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
prompt_state_file="$project_root/_grimoire-runtime-output/hook-runtime/user-prompt-latest.json"
policy_script="$project_root/grimoire-kit/framework/tools/guardrail-policy.py"
policy_python="$project_root/grimoire-kit/.venv/bin/python"
input=$(cat)

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -z "$policy_python" || ! -f "$policy_script" ]]; then
  echo "{}"
  exit 0
fi

if ! output=$(printf '%s' "$input" | "$policy_python" "$policy_script" control-surface --prompt-state-file "$prompt_state_file" 2>/dev/null); then
  echo "{}"
  exit 0
fi

# V1 ledger: scope=tool, phase=block si garde applique, info sinon.
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  phase="info"
  if [[ "$output" == *'"decision"'*'"block"'* || "$output" == *'"permissionDecision"'*'"deny"'* ]]; then
    phase="block"
  fi
  "$emit_event_script" --scope tool --phase "$phase" --source-hook "grimoire-control-surface-guard.sh" --payload-json '{"hook":"control-surface-guard"}' 2>/dev/null || true
fi

printf '%s\n' "$output"