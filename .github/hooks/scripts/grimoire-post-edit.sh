#!/usr/bin/env bash
# grimoire-post-edit.sh — PostToolUse hook
# Valide rapidement les fichiers modifies sur des checks deterministes et locaux.

set -euo pipefail

input=$(cat)
project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
prompt_state_file="$project_root/_grimoire-runtime-output/hook-runtime/user-prompt-latest.json"
policy_script="$project_root/grimoire-kit/framework/tools/guardrail-policy.py"
policy_python="$project_root/grimoire-kit/.venv/bin/python"

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -z "$policy_python" || ! -f "$policy_script" ]]; then
  echo "{}"
  exit 0
fi

if ! output=$(printf '%s' "$input" | "$policy_python" "$policy_script" post-edit --project-root "$project_root" --python-executable "$policy_python" --prompt-state-file "$prompt_state_file" 2>/dev/null); then
  echo "{}"
  exit 0
fi

# V1 ledger : emet un GrimoireEvent scope=tool.  Fail-open : toute erreur
# d'emission est silencieuse et n'affecte pas la sortie du hook.
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  phase="info"
  if [[ "$output" == *'"modified"'*'true'* || "$output" == *'"blocked"'*'true'* ]]; then
    phase="correct"
  fi
  "$emit_event_script" \
    --scope tool \
    --phase "$phase" \
    --source-hook "grimoire-post-edit.sh" \
    --payload-json '{"hook":"post-edit"}' 2>/dev/null || true
fi

printf '%s\n' "$output"
