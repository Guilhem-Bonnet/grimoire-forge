#!/usr/bin/env bash
# grimoire-pre-compact.sh — PreCompact hook
# Capture une capsule de contexte avant compaction et l'injecte pour la phase
# de summarization quand le host supporte additionalContext.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
hook_state_dir="$project_root/_grimoire-runtime-output/hook-runtime"
precompact_dir="$hook_state_dir/precompact"
prompt_state_file="$hook_state_dir/user-prompt-latest.json"
task_latest_file="$project_root/_grimoire-runtime-output/task-flow/latest.json"
trace_file="$project_root/_grimoire-runtime-output/GRIMOIRE_TRACE.jsonl"
subagent_latest_file="$hook_state_dir/subagent-stop/latest.json"
latest_file="$precompact_dir/latest.json"
events_file="$precompact_dir/events.jsonl"
policy_script="$project_root/.github/hooks/lib/guardrail-policy.py"
policy_python="$project_root/.venv/bin/python"
input=$(cat)

mkdir -p "$precompact_dir"

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -z "$policy_python" || ! -f "$policy_script" ]]; then
  echo "{}"
  exit 0
fi

if ! output=$(printf '%s' "$input" | "$policy_python" "$policy_script" pre-compact --project-root "$project_root" --prompt-state-file "$prompt_state_file" --task-latest-file "$task_latest_file" --trace-file "$trace_file" --subagent-latest-file "$subagent_latest_file" --latest-file "$latest_file" --events-file "$events_file" 2>/dev/null); then
  echo "{}"
  exit 0
fi

# V1 ledger: scope=compact, phase=info (capsule de contexte avant summarization).
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  "$emit_event_script" --scope compact --phase info --source-hook "grimoire-pre-compact.sh" --payload-json '{"hook":"pre-compact"}' 2>/dev/null || true
fi

printf '%s\n' "$output"