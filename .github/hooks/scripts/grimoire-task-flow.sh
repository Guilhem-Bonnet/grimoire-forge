#!/usr/bin/env bash
# grimoire-task-flow.sh -- Task-level hook wrapper for VS Code tasks.
# Records start/success/failure events for agentic tasks and keeps a
# small latest-state snapshot for downstream tooling.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
FLOW_DIR="$PROJECT_ROOT/_grimoire-runtime-output/task-flow"
EVENTS_FILE="$FLOW_DIR/events.jsonl"
LATEST_FILE="$FLOW_DIR/latest.json"
TASK_STATE_DIR="$FLOW_DIR/tasks"

json_escape() {
  local value="$1"
  value=${value//\\/\\\\}
  value=${value//\"/\\\"}
  value=${value//$'\n'/\\n}
  value=${value//$'\r'/\\r}
  printf '%s' "$value"
}

sanitize_name() {
  local value="$1"
  value=${value//[^[:alnum:]]/_}
  printf '%s' "$value"
}

join_command() {
  local part
  local escaped
  local joined=""

  for part in "$@"; do
    printf -v escaped '%q' "$part"
    joined+="${joined:+ }$escaped"
  done

  printf '%s' "$joined"
}

timestamp_utc() {
  date -u '+%Y-%m-%dT%H:%M:%SZ'
}

usage() {
  cat <<'EOF'
Usage:
  grimoire-task-flow.sh --task <label> --flow <name> [--kind <kind>] -- <command> [args...]
EOF
}

write_state_file() {
  local target="$1"
  local task_label="$2"
  local flow_name="$3"
  local kind_name="$4"
  local status_name="$5"
  local event_name="$6"
  local exit_code="$7"
  local duration_seconds="$8"
  local started_at="$9"
  local finished_at="${10}"
  local command_line="${11}"
  local cwd="${12}"
  local tmp_file

  tmp_file="$(mktemp "$FLOW_DIR/.state.XXXXXX")"
  {
    printf '{'
    printf '"task":"%s",' "$(json_escape "$task_label")"
    printf '"flow":"%s",' "$(json_escape "$flow_name")"
    printf '"kind":"%s",' "$(json_escape "$kind_name")"
    printf '"status":"%s",' "$(json_escape "$status_name")"
    printf '"event":"%s",' "$(json_escape "$event_name")"
    printf '"exitCode":%s,' "$exit_code"
    printf '"durationSeconds":%s,' "$duration_seconds"
    printf '"startedAt":"%s",' "$(json_escape "$started_at")"
    printf '"finishedAt":"%s",' "$(json_escape "$finished_at")"
    printf '"cwd":"%s",' "$(json_escape "$cwd")"
    printf '"command":"%s"' "$(json_escape "$command_line")"
    printf '}'
    printf '\n'
  } > "$tmp_file"
  mv "$tmp_file" "$target"
}

append_event() {
  local event_name="$1"
  local task_label="$2"
  local flow_name="$3"
  local kind_name="$4"
  local status_name="$5"
  local exit_code="$6"
  local duration_seconds="$7"
  local started_at="$8"
  local finished_at="$9"
  local command_line="${10}"
  local cwd="${11}"
  local timestamp

  timestamp="$(timestamp_utc)"
  printf '{"timestamp":"%s","event":"%s","task":"%s","flow":"%s","kind":"%s","status":"%s","exitCode":%s,"durationSeconds":%s,"startedAt":"%s","finishedAt":"%s","cwd":"%s","command":"%s"}\n' \
    "$(json_escape "$timestamp")" \
    "$(json_escape "$event_name")" \
    "$(json_escape "$task_label")" \
    "$(json_escape "$flow_name")" \
    "$(json_escape "$kind_name")" \
    "$(json_escape "$status_name")" \
    "$exit_code" \
    "$duration_seconds" \
    "$(json_escape "$started_at")" \
    "$(json_escape "$finished_at")" \
    "$(json_escape "$cwd")" \
    "$(json_escape "$command_line")" \
    >> "$EVENTS_FILE"
}

task_label=""
flow_name=""
kind_name="task"
declare -a command=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task)
      task_label="${2:-}"
      shift 2
      ;;
    --flow)
      flow_name="${2:-}"
      shift 2
      ;;
    --kind)
      kind_name="${2:-}"
      shift 2
      ;;
    --)
      shift
      command=("$@")
      break
      ;;
    *)
      usage >&2
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$task_label" || -z "$flow_name" || ${#command[@]} -eq 0 ]]; then
  usage >&2
  exit 2
fi

mkdir -p "$TASK_STATE_DIR"

task_slug="$(sanitize_name "$task_label")"
task_state_file="$TASK_STATE_DIR/$task_slug.json"
command_line="$(join_command "${command[@]}")"
cwd="$(pwd)"
started_at="$(timestamp_utc)"
start_epoch="$(date +%s)"

echo "[grimoire-task-flow] start task=$task_label flow=$flow_name kind=$kind_name"

# V1 ledger: scope=task, phase=start.  PROJECT_ROOT est defini plus haut dans le script.
emit_event_script="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  "$emit_event_script" --scope task --phase start --source-hook "grimoire-task-flow.sh" \
    --payload-json "$(printf '{"label":"%s","flow":"%s","kind":"%s"}' "$task_label" "$flow_name" "$kind_name")" \
    2>/dev/null || true
fi

append_event \
  "task-start" \
  "$task_label" \
  "$flow_name" \
  "$kind_name" \
  "running" \
  0 \
  0 \
  "$started_at" \
  "$started_at" \
  "$command_line" \
  "$cwd"

write_state_file \
  "$task_state_file" \
  "$task_label" \
  "$flow_name" \
  "$kind_name" \
  "running" \
  "task-start" \
  0 \
  0 \
  "$started_at" \
  "$started_at" \
  "$command_line" \
  "$cwd"

write_state_file \
  "$LATEST_FILE" \
  "$task_label" \
  "$flow_name" \
  "$kind_name" \
  "running" \
  "task-start" \
  0 \
  0 \
  "$started_at" \
  "$started_at" \
  "$command_line" \
  "$cwd"

set +e
"${command[@]}"
command_status=$?
set -e

finish_epoch="$(date +%s)"
duration_seconds=$((finish_epoch - start_epoch))
finished_at="$(timestamp_utc)"

if [[ "$command_status" -eq 0 ]]; then
  status_name="success"
else
  status_name="failed"
fi

append_event \
  "task-finish" \
  "$task_label" \
  "$flow_name" \
  "$kind_name" \
  "$status_name" \
  "$command_status" \
  "$duration_seconds" \
  "$started_at" \
  "$finished_at" \
  "$command_line" \
  "$cwd"

write_state_file \
  "$task_state_file" \
  "$task_label" \
  "$flow_name" \
  "$kind_name" \
  "$status_name" \
  "task-finish" \
  "$command_status" \
  "$duration_seconds" \
  "$started_at" \
  "$finished_at" \
  "$command_line" \
  "$cwd"

write_state_file \
  "$LATEST_FILE" \
  "$task_label" \
  "$flow_name" \
  "$kind_name" \
  "$status_name" \
  "task-finish" \
  "$command_status" \
  "$duration_seconds" \
  "$started_at" \
  "$finished_at" \
  "$command_line" \
  "$cwd"

echo "[grimoire-task-flow] end task=$task_label status=$status_name duration=${duration_seconds}s exit=$command_status"

# V1 ledger: scope=task, phase=end.  phase=block si status_name=failed.
if [[ -x "$emit_event_script" ]]; then
  task_end_phase="end"
  if [[ "$status_name" == "failed" ]]; then
    task_end_phase="block"
  fi
  "$emit_event_script" --scope task --phase "$task_end_phase" --source-hook "grimoire-task-flow.sh" \
    --payload-json "$(printf '{"label":"%s","flow":"%s","kind":"%s","status":"%s","exit":%d,"duration_s":%d}' "$task_label" "$flow_name" "$kind_name" "$status_name" "$command_status" "$duration_seconds")" \
    2>/dev/null || true
fi

exit "$command_status"