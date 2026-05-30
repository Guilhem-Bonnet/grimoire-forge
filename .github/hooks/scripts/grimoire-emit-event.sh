#!/usr/bin/env bash
# grimoire-emit-event.sh — helper universel pour émettre un GrimoireEvent.
#
# Contrat (voir grimoire-kit/src/grimoire/tools/events.py, SCHEMA_VERSION=1.0) :
#   - scope ∈ {session, prompt, tool, subagent, compact, stop, task, anomaly}
#   - phase ∈ {start, end, block, correct, info}
#   - source_hook  : nom du script émetteur (ex: grimoire-post-edit.sh)
#   - payload-json : objet JSON (défaut '{}')
#   - agent-json   : optionnel, objet JSON {id,role,parent}
#   - correlation-id : optionnel
#
# Mode d'emploi dans un script de hook :
#   emit_grimoire_event() {
#     "$PROJECT_ROOT/.github/hooks/scripts/grimoire-emit-event.sh" \
#       --scope tool --phase start \
#       --source-hook "$(basename "$0")" \
#       --payload-json '{"file":"foo.py"}'
#   }
#
# Fail-open : toute erreur de validation est silencieuse, l'event est logué
# dans events-errors.jsonl et le hook continue sans blocage.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PYTHON_BIN="$PROJECT_ROOT/grimoire-kit/.venv/bin/python"
LEDGER="$PROJECT_ROOT/_grimoire-runtime/_memory/activity.jsonl"
ERROR_LOG="$PROJECT_ROOT/_grimoire-runtime-output/hook-runtime/events-errors.jsonl"

if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python3 || true)"
fi

if [[ -z "$PYTHON_BIN" ]]; then
  # Sans Python, on ne peut ni valider ni écrire : fail-open silencieux.
  exit 0
fi

# Forward all args to events CLI.  stdout = JSONL ready to append.
set +e
output="$("$PYTHON_BIN" -m grimoire.tools.events emit "$@" 2>/dev/null)"
rc=$?
set -e

if [[ $rc -ne 0 || -z "$output" ]]; then
  mkdir -p "$(dirname "$ERROR_LOG")"
  ts="$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")"
  printf '{"ts":"%s","reason":"emit-rejected","args":%s}\n' \
    "$ts" "$(printf '%s' "$*" | "$PYTHON_BIN" -c 'import sys,json;print(json.dumps(sys.stdin.read()))')" \
    >> "$ERROR_LOG"
  exit 0
fi

# Append via the canonical writer (one-line semantic).  Single writer guarantee
# is respected: all scripts funnel through this same script.
mkdir -p "$(dirname "$LEDGER")"
printf '%s\n' "$output" >> "$LEDGER"
exit 0
