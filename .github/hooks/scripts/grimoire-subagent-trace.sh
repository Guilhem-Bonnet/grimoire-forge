#!/usr/bin/env bash
# grimoire-subagent-trace.sh — SubagentStart/SubagentStop hook
# Trace les transitions entre sub-agents pour le debug SOG.
# Parse le JSON des hooks VS Code avec les champs documentés (hookEventName,
# hook_event_name, agent_type, agent_id) tout en gardant des fallbacks.
# Le hook auto-repare le journal runtime, reconstruit le sidecar JSONL,
# permet un audit lecture seule ou strict, et archive les contenus legacy
# ou les payloads non parsables au lieu d'ajouter des evenements `unknown`
# dans la trace principale.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TRACE_FILE="$PROJECT_ROOT/_grimoire-runtime-output/GRIMOIRE_TRACE.md"
TRACE_JSONL_FILE="$PROJECT_ROOT/_grimoire-runtime-output/GRIMOIRE_TRACE.jsonl"
TRACE_LEGACY_FILE="$PROJECT_ROOT/_grimoire-runtime-output/GRIMOIRE_TRACE.legacy.txt"
HOOK_STATE_DIR="$PROJECT_ROOT/_grimoire-runtime-output/hook-runtime"
SUBAGENT_STOP_DIR="$HOOK_STATE_DIR/subagent-stop"
PROMPT_STATE_FILE="$HOOK_STATE_DIR/user-prompt-latest.json"
SUBAGENT_STOP_LATEST_FILE="$SUBAGENT_STOP_DIR/latest.json"
SUBAGENT_STOP_EVENTS_FILE="$SUBAGENT_STOP_DIR/events.jsonl"
SUBAGENT_STOP_COUNTER_FILE="$SUBAGENT_STOP_DIR/repetition-counters.json"
POLICY_SCRIPT="$PROJECT_ROOT/grimoire-kit/framework/tools/guardrail-policy.py"
POLICY_PYTHON="$PROJECT_ROOT/grimoire-kit/.venv/bin/python"
RUNTIME_ENTRY_BASH_REGEX='^- `([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})` \*\*([^*]+)\*\* → `([^`]+)`$'

json_escape() {
  local value="$1"
  value=${value//\\/\\\\}
  value=${value//\"/\\\"}
  value=${value//$'\n'/\\n}
  value=${value//$'\r'/\\r}
  printf '%s' "$value"
}

write_runtime_header() {
  local target="$1"
  {
    echo "# Grimoire Runtime Trace"
    echo ""
    echo "Journal runtime genere par les hooks \`SubagentStart\` et \`SubagentStop\`."
    echo ""
    echo "- Audit lecture seule: \`grimoire: trace-audit\` (alias \`bmad: trace-audit\`)"
    echo "- Audit strict CI/preflight: \`grimoire: trace-audit-strict\` (alias \`bmad: trace-audit-strict\`)"
    echo "- Reparation manuelle: \`grimoire: trace-repair\` (alias \`bmad: trace-repair\`)"
    echo "- Archive legacy si migration: \`GRIMOIRE_TRACE.legacy.txt\`"
    echo "- Sidecar machine-readable: \`GRIMOIRE_TRACE.jsonl\`"
    echo "- Format: \`YYYY-MM-DD HH:MM:SS\` **Event** → \`Agent\`"
    echo ""
  } > "$target"
}

initialize_runtime_trace() {
  mkdir -p "$(dirname "$TRACE_FILE")"
  write_runtime_header "$TRACE_FILE"
}

ensure_legacy_file() {
  mkdir -p "$(dirname "$TRACE_LEGACY_FILE")"
  if [[ ! -f "$TRACE_LEGACY_FILE" ]]; then
    {
      echo "Grimoire runtime trace — archive legacy et payloads rejetes"
      echo ""
    } > "$TRACE_LEGACY_FILE"
  fi
}

append_legacy_snapshot() {
  local reason="$1"
  local content_file="$2"

  if [[ ! -s "$content_file" ]]; then
    return
  fi

  ensure_legacy_file
  {
    printf '=== %s | %s ===\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$reason"
    cat "$content_file"
    printf '\n'
  } >> "$TRACE_LEGACY_FILE"
}

archive_rejected_payload() {
  local reason="$1"
  local payload="$2"
  local payload_file

  if [[ -z "${payload//[[:space:]]/}" ]]; then
    return
  fi

  payload_file=$(mktemp)
  printf '%s\n' "$payload" > "$payload_file"
  append_legacy_snapshot "$reason" "$payload_file"
  rm -f "$payload_file"
}

extract_prelude_and_body() {
  local prelude_file="$1"
  local body_file="$2"

  : > "$prelude_file"
  : > "$body_file"

  if [[ ! -f "$TRACE_FILE" ]]; then
    return
  fi

  awk -v prelude="$prelude_file" -v body="$body_file" '
    /^- `/ { in_body = 1 }
    {
      if (in_body) {
        print >> body
      } else {
        print >> prelude
      }
    }
  ' "$TRACE_FILE"
}

rebuild_jsonl_sidecar() {
  local runtime_entries_file="$1"
  local line
  local timestamp
  local event_name
  local agent_name

  mkdir -p "$(dirname "$TRACE_JSONL_FILE")"
  : > "$TRACE_JSONL_FILE"

  while IFS= read -r line; do
    if [[ "$line" =~ $RUNTIME_ENTRY_BASH_REGEX ]]; then
      timestamp="${BASH_REMATCH[1]}"
      event_name="${BASH_REMATCH[2]}"
      agent_name="${BASH_REMATCH[3]}"
      printf '{"timestamp":"%s","event":"%s","agent":"%s","source":"vscode-hook"}\n' \
        "$(json_escape "$timestamp")" \
        "$(json_escape "$event_name")" \
        "$(json_escape "$agent_name")" \
        >> "$TRACE_JSONL_FILE"
    fi
  done < "$runtime_entries_file"
}

audit_trace_artifacts() {
  local fail_on_warning="${1:-false}"
  local tmp_dir=""
  local header_file=""
  local prelude_file=""
  local body_file=""
  local trace_exists=false
  local jsonl_exists=false
  local legacy_exists=false
  local header_drift=false
  local runtime_entries=0
  local jsonl_entries=0
  local unknown_runtime_entries=0
  local legacy_snapshots=0
  local repair_snapshots=0
  local unparsed_payload_snapshots=0
  local status="healthy"
  local first_issue=1
  local issue
  local -a issues=()

  if [[ -f "$TRACE_FILE" ]]; then
    trace_exists=true
    runtime_entries=$(awk '
      /^- `[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}` \*\*[^*]+\*\* → `[^`]+`$/ {
        count++
      }
      END {
        print count + 0
      }
    ' "$TRACE_FILE")
    unknown_runtime_entries=$(grep -E -c '\*\*unknown\*\* → `unknown`$' "$TRACE_FILE" || true)

    tmp_dir=$(mktemp -d)
    header_file="$tmp_dir/header.md"
    prelude_file="$tmp_dir/prelude.txt"
    body_file="$tmp_dir/body.txt"
    write_runtime_header "$header_file"
    extract_prelude_and_body "$prelude_file" "$body_file"

    if ! cmp -s "$prelude_file" "$header_file"; then
      header_drift=true
      issues+=("header-drift")
    fi

    rm -rf "$tmp_dir"
  else
    issues+=("trace-missing")
  fi

  if [[ -f "$TRACE_JSONL_FILE" ]]; then
    jsonl_exists=true
    jsonl_entries=$(wc -l < "$TRACE_JSONL_FILE")
    jsonl_entries=${jsonl_entries//[[:space:]]/}
  else
    issues+=("jsonl-missing")
  fi

  if [[ -f "$TRACE_LEGACY_FILE" ]]; then
    legacy_exists=true
    legacy_snapshots=$(grep -E -c '^=== ' "$TRACE_LEGACY_FILE" || true)
    repair_snapshots=$(grep -E -c '\| trace-repair ===$' "$TRACE_LEGACY_FILE" || true)
    unparsed_payload_snapshots=$(grep -E -c '\| unparsed-hook-payload ===$' "$TRACE_LEGACY_FILE" || true)
  fi

  if [[ "$unknown_runtime_entries" -gt 0 ]]; then
    issues+=("unknown-runtime-entries")
  fi

  if [[ "$trace_exists" == true && "$jsonl_exists" == true && "$runtime_entries" -ne "$jsonl_entries" ]]; then
    issues+=("jsonl-runtime-mismatch")
  fi

  if [[ "${#issues[@]}" -gt 0 ]]; then
    status="warning"
  fi

  printf '{'
  printf '"status":"%s",' "$(json_escape "$status")"
  printf '"traceExists":%s,' "$trace_exists"
  printf '"jsonlExists":%s,' "$jsonl_exists"
  printf '"legacyExists":%s,' "$legacy_exists"
  printf '"headerDrift":%s,' "$header_drift"
  printf '"runtimeEntries":%s,' "$runtime_entries"
  printf '"jsonlEntries":%s,' "$jsonl_entries"
  printf '"unknownRuntimeEntries":%s,' "$unknown_runtime_entries"
  printf '"legacySnapshots":%s,' "$legacy_snapshots"
  printf '"repairSnapshots":%s,' "$repair_snapshots"
  printf '"unparsedPayloadSnapshots":%s,' "$unparsed_payload_snapshots"
  printf '"issues":['

  for issue in "${issues[@]}"; do
    if [[ "$first_issue" -eq 0 ]]; then
      printf ','
    fi
    printf '"%s"' "$(json_escape "$issue")"
    first_issue=0
  done

  printf ']}'
  printf '\n'

  if [[ "$fail_on_warning" == "true" && "$status" != "healthy" ]]; then
    return 1
  fi
}

normalize_trace_artifacts() {
  local tmp_dir
  local header_file
  local prelude_file
  local body_file
  local runtime_entries_file
  local legacy_file
  local needs_repair=0

  tmp_dir=$(mktemp -d)
  header_file="$tmp_dir/header.md"
  prelude_file="$tmp_dir/prelude.txt"
  body_file="$tmp_dir/body.txt"
  runtime_entries_file="$tmp_dir/runtime.txt"
  legacy_file="$tmp_dir/legacy.txt"

  : > "$runtime_entries_file"
  : > "$legacy_file"
  write_runtime_header "$header_file"

  if [[ -f "$TRACE_FILE" ]]; then
    extract_prelude_and_body "$prelude_file" "$body_file"

    if ! cmp -s "$prelude_file" "$header_file"; then
      if [[ -s "$prelude_file" ]]; then
        cat "$prelude_file" >> "$legacy_file"
      fi
      needs_repair=1
    fi

    awk -v runtime="$runtime_entries_file" -v legacy="$legacy_file" '
      /^- `[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}` \*\*[^*]+\*\* → `[^`]+`$/ {
        if ($0 ~ /\*\*unknown\*\* → `unknown`$/) {
          print >> legacy
        } else {
          print >> runtime
        }
        next
      }

      NF > 0 {
        print >> legacy
      }
    ' "$body_file"

    if [[ -s "$legacy_file" ]]; then
      needs_repair=1
    fi
  else
    needs_repair=1
  fi

  if [[ "$needs_repair" -eq 1 ]]; then
    append_legacy_snapshot "trace-repair" "$legacy_file"
    mkdir -p "$(dirname "$TRACE_FILE")"
    cat "$header_file" > "$TRACE_FILE"
    if [[ -s "$runtime_entries_file" ]]; then
      cat "$runtime_entries_file" >> "$TRACE_FILE"
    fi
  fi

  if [[ "$needs_repair" -eq 1 || ! -f "$TRACE_JSONL_FILE" ]]; then
    rebuild_jsonl_sidecar "$runtime_entries_file"
  fi

  rm -rf "$tmp_dir"
}

if [[ "${1:-}" == "--audit-only" ]]; then
  audit_trace_artifacts false
  exit 0
fi

if [[ "${1:-}" == "--audit-strict" ]]; then
  audit_trace_artifacts true
  exit 0
fi

if [[ "${1:-}" == "--repair-only" ]]; then
  normalize_trace_artifacts
  echo "{}"
  exit 0
fi

input=$(cat)

if [[ ! -x "$POLICY_PYTHON" ]]; then
  POLICY_PYTHON="$(command -v python3 || true)"
fi

# Extraire event et agent via regex bash (pas de spawn python)
event_name="unknown"
agent_name="unknown"

if [[ "$input" =~ \"hookEventName\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  event_name="${BASH_REMATCH[1]}"
elif [[ "$input" =~ \"hook_event_name\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  event_name="${BASH_REMATCH[1]}"
fi

if [[ "$input" =~ \"agent_type\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  agent_name="${BASH_REMATCH[1]}"
elif [[ "$input" =~ \"agentName\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  agent_name="${BASH_REMATCH[1]}"
elif [[ "$input" =~ \"agent_id\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  agent_name="${BASH_REMATCH[1]}"
fi

normalize_trace_artifacts

if [[ -z "${input//[[:space:]]/}" ]]; then
  echo "{}"
  exit 0
fi

if [[ "$event_name" == "unknown" || "$agent_name" == "unknown" ]]; then
  archive_rejected_payload "unparsed-hook-payload" "$input"
  echo "{}"
  exit 0
fi

timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Creer le fichier trace s'il n'existe pas
if [[ ! -f "$TRACE_FILE" ]]; then
  initialize_runtime_trace
fi

# Ajouter la trace
echo "- \`$timestamp\` **$event_name** → \`$agent_name\`" >> "$TRACE_FILE"

mkdir -p "$(dirname "$TRACE_JSONL_FILE")"
printf '{"timestamp":"%s","event":"%s","agent":"%s","source":"vscode-hook"}\n' \
  "$(json_escape "$timestamp")" \
  "$(json_escape "$event_name")" \
  "$(json_escape "$agent_name")" \
  >> "$TRACE_JSONL_FILE"

# V1 ledger : emit GrimoireEvent scope=subagent.  phase = start/end selon event.
# Fail-open : toute erreur d'emission est silencieuse.
emit_event_script="$PROJECT_ROOT/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  if [[ "$event_name" == "SubagentStop" ]]; then
    subagent_phase="end"
  else
    subagent_phase="start"
  fi
  agent_json=$(printf '{"id":"%s","role":"subagent"}' "$(json_escape "$agent_name")")
  "$emit_event_script" \
    --scope subagent \
    --phase "$subagent_phase" \
    --source-hook "grimoire-subagent-trace.sh" \
    --agent-json "$agent_json" \
    --payload-json "$(printf '{"event_name":"%s"}' "$(json_escape "$event_name")")" \
    2>/dev/null || true
fi

if [[ "$event_name" != "SubagentStop" ]]; then
  echo "{}"
  exit 0
fi

mkdir -p "$SUBAGENT_STOP_DIR"

if [[ -z "$POLICY_PYTHON" || ! -f "$POLICY_SCRIPT" ]]; then
  echo "{}"
  exit 0
fi

if ! output=$(printf '%s' "$input" | "$POLICY_PYTHON" "$POLICY_SCRIPT" subagent-stop --project-root "$PROJECT_ROOT" --prompt-state-file "$PROMPT_STATE_FILE" --latest-file "$SUBAGENT_STOP_LATEST_FILE" --events-file "$SUBAGENT_STOP_EVENTS_FILE" --counter-file "$SUBAGENT_STOP_COUNTER_FILE" 2>/dev/null); then
  echo "{}"
  exit 0
fi

printf '%s\n' "$output"
