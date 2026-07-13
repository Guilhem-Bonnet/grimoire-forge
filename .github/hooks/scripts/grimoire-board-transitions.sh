#!/usr/bin/env bash
# grimoire-board-transitions.sh — PostToolUse hook (chantier C1)
# Journalise en append-only les transitions de statut du kanban gouverne
# (_grimoire/standard/task-board.yaml) dans _grimoire-runtime/_memory/.
# Le journal est ecrit par ce hook, jamais par l'agent : c'est la propriete
# qui rend la preuve opposable. Fail-open integral.

set -euo pipefail

input=$(cat)
project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
logger_script="$project_root/scripts/board-transitions-log.py"
logger_python="$project_root/grimoire-kit/.venv/bin/python"

if [[ ! -x "$logger_python" ]]; then
  logger_python="$(command -v python3 || true)"
fi

if [[ -z "$logger_python" || ! -f "$logger_script" ]]; then
  echo "{}"
  exit 0
fi

# Filtre rapide : ne paye le cout Python que si le payload touche le board.
if [[ "$input" != *"task-board.yaml"* ]]; then
  echo "{}"
  exit 0
fi

printf '%s' "$input" | "$logger_python" "$logger_script" --project-root "$project_root" record --stdin-json 2>/dev/null || true

# V1 ledger : trace l'evenement, fail-open.
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  "$emit_event_script" \
    --scope tool \
    --phase info \
    --source-hook "grimoire-board-transitions.sh" \
    --payload-json '{"hook":"board-transitions"}' 2>/dev/null || true
fi

echo "{}"
