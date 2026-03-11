#!/usr/bin/env bash
# bmad-subagent-trace.sh — SubagentStart/SubagentStop hook
# Trace les transitions entre sub-agents pour le debug SOG.
# Les traces sont écrites dans _bmad-output/BMAD_TRACE.md

set -euo pipefail

input=$(cat)

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TRACE_FILE="$PROJECT_ROOT/_bmad-output/BMAD_TRACE.md"

# Extraire les infos de l'événement
event_name=$(echo "$input" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('hookEventName', data.get('event', 'unknown')))
except: print('unknown')
" 2>/dev/null || echo "unknown")

agent_name=$(echo "$input" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('agentName', data.get('agent', 'unknown')))
except: print('unknown')
" 2>/dev/null || echo "unknown")

timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Créer le fichier trace s'il n'existe pas
if [[ ! -f "$TRACE_FILE" ]]; then
  mkdir -p "$(dirname "$TRACE_FILE")"
  echo "# BMAD SOG Trace Log" > "$TRACE_FILE"
  echo "" >> "$TRACE_FILE"
fi

# Ajouter la trace
echo "- \`$timestamp\` **$event_name** → \`$agent_name\`" >> "$TRACE_FILE"

echo "{}"
