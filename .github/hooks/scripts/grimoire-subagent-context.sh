#!/usr/bin/env bash
# grimoire-subagent-context.sh — SubagentStart hook
# Injecte une capsule de contexte courte aux sub-agents a partir de l'etat de
# session le plus recent.

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

if ! output=$(printf '%s' "$input" | "$policy_python" "$policy_script" subagent-context --project-root "$project_root" --prompt-state-file "$prompt_state_file" 2>/dev/null); then
  echo "{}"
  exit 0
fi

# V1 ledger: scope=subagent, phase=info (injection de contexte).
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  "$emit_event_script" --scope subagent --phase info --source-hook "grimoire-subagent-context.sh" --payload-json '{"hook":"subagent-context"}' 2>/dev/null || true
fi

printf '%s\n' "$output"