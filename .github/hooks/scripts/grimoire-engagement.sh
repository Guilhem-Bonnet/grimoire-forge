#!/usr/bin/env bash
# grimoire-engagement.sh — UserPromptSubmit hook (chantier C4)
# Journalise les signaux d'engagement des workflows (slash command, mention)
# dans _grimoire-runtime/_memory/engagement.jsonl. Metrique d'entree du bras
# « active » de la campagne d'evals. Fail-open integral, aucune sortie active.

set -euo pipefail

input=$(cat)
project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
logger_script="$project_root/scripts/engagement-log.py"
logger_python="$project_root/grimoire-kit/.venv/bin/python"

if [[ ! -x "$logger_python" ]]; then
  logger_python="$(command -v python3 || true)"
fi

if [[ -n "$logger_python" && -f "$logger_script" ]]; then
  printf '%s' "$input" | "$logger_python" "$logger_script" --project-root "$project_root" record 2>/dev/null || true
fi

echo "{}"
