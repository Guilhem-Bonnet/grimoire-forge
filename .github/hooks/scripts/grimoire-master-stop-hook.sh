#!/usr/bin/env bash
# grimoire-master-stop-hook.sh — Stop hook scoped to grimoire-master.
# Objectif: empêcher une clôture sèche du tour et demander une prochaine
# demande dans la même conversation, une seule fois par tentative d'arrêt.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
hook_state_dir="$project_root/_grimoire-runtime-output/hook-runtime"
stop_dir="$hook_state_dir/stop"
prompt_state_file="$hook_state_dir/user-prompt-latest.json"
task_latest_file="$project_root/_grimoire-runtime-output/task-flow/latest.json"
subagent_latest_file="$hook_state_dir/subagent-stop/latest.json"
latest_file="$stop_dir/latest.json"
policy_script="$project_root/.github/hooks/lib/guardrail-policy.py"
policy_python="$project_root/.venv/bin/python"
input=$(cat)

# V1 ledger: scope=stop, phase=info (une emission par invocation, quelle que
# soit la decision finale).  Fail-open.
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  "$emit_event_script" --scope stop --phase info --source-hook "grimoire-master-stop-hook.sh" --payload-json '{"hook":"master-stop"}' 2>/dev/null || true
fi

stop_hook_active="false"
stop_additional_context=""
stop_decision=""
stop_reason=""
stop_system_message=""

mkdir -p "$stop_dir"

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -n "$policy_python" && -f "$policy_script" ]]; then
  stop_closure_output=$(printf '%s' "$input" | "$policy_python" "$policy_script" stop-closure \
    --project-root "$project_root" \
    --prompt-state-file "$prompt_state_file" \
    --task-latest-file "$task_latest_file" \
    --subagent-latest-file "$subagent_latest_file" \
    --latest-file "$latest_file" \
    2>/dev/null || true)

  if [[ -n "$stop_closure_output" && "$stop_closure_output" != "{}" ]]; then
    stop_additional_context=$(printf '%s' "$stop_closure_output" | "$policy_python" -c 'import json,sys; payload=json.load(sys.stdin); print(payload.get("hookSpecificOutput", {}).get("additionalContext", ""))' 2>/dev/null || true)
    stop_decision=$(printf '%s' "$stop_closure_output" | "$policy_python" -c 'import json,sys; payload=json.load(sys.stdin); print(payload.get("hookSpecificOutput", {}).get("decision", ""))' 2>/dev/null || true)
    stop_reason=$(printf '%s' "$stop_closure_output" | "$policy_python" -c 'import json,sys; payload=json.load(sys.stdin); print(payload.get("hookSpecificOutput", {}).get("reason", ""))' 2>/dev/null || true)
    # systemMessage porte le signal d'enforcement du budget de tokens
    # (enforcementRecommended, ecart B2) : aucun hote ne lit additionalContext
    # sur un evenement Stop, donc ce champ doit etre transmis a part.
    stop_system_message=$(printf '%s' "$stop_closure_output" | "$policy_python" -c 'import json,sys; payload=json.load(sys.stdin); print(payload.get("systemMessage", ""))' 2>/dev/null || true)
  fi
fi

if [[ "$input" =~ \"stop_hook_active\"[[:space:]]*:[[:space:]]*(true|false) ]]; then
  stop_hook_active="${BASH_REMATCH[1]}"
elif [[ "$input" =~ \"stopHookActive\"[[:space:]]*:[[:space:]]*(true|false) ]]; then
  stop_hook_active="${BASH_REMATCH[1]}"
fi

if [[ "$stop_hook_active" == "true" ]]; then
  echo '{"continue": true}'
  exit 0
fi

if [[ "$stop_decision" == "block" && -n "$stop_reason" ]]; then
  "$policy_python" -c "
import json, sys
reason = sys.argv[1]
additional_context = sys.argv[2]
system_message = sys.argv[3]
specific = {'hookEventName': 'Stop', 'decision': 'block', 'reason': reason}
if additional_context:
    specific['additionalContext'] = additional_context
payload = {'hookSpecificOutput': specific}
if system_message:
    payload['systemMessage'] = system_message
print(json.dumps(payload))
" "$stop_reason" "$stop_additional_context" "$stop_system_message"
  exit 0
fi

# systemMessage doit etre relaye des qu'il est present, meme sans
# additionalContext : guardrail-policy.py peut renvoyer un payload Stop ne
# portant que l'enforcement du budget de tokens (systemMessage seul).
if [[ -n "$stop_additional_context" || -n "$stop_system_message" ]]; then
  "$policy_python" -c "
import json, sys
additional_context = sys.argv[1]
system_message = sys.argv[2]
specific = {
    'hookEventName': 'Stop',
    'decision': 'block',
    'reason': \"Avant de conclure, demande a l'utilisateur sa prochaine demande en une phrase concise et attends sa reponse dans cette conversation. N'affiche pas le menu si cette nouvelle demande est deja actionable.\",
}
if additional_context:
    specific['additionalContext'] = additional_context
payload = {'hookSpecificOutput': specific}
if system_message:
    payload['systemMessage'] = system_message
print(json.dumps(payload))
" "$stop_additional_context" "$stop_system_message"
  exit 0
fi

cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "decision": "block",
    "reason": "Avant de conclure, demande à l'utilisateur sa prochaine demande en une phrase concise et attends sa réponse dans cette conversation. N'affiche pas le menu si cette nouvelle demande est déjà actionable."
  }
}
EOF