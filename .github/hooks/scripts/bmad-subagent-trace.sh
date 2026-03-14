#!/usr/bin/env bash
# bmad-subagent-trace.sh — SubagentStart/SubagentStop hook
# Trace les transitions entre sub-agents pour le debug SOG.
# Optimisé : regex bash au lieu de python pour le parsing JSON.

set -euo pipefail

input=$(cat)

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TRACE_FILE="$PROJECT_ROOT/_bmad-output/BMAD_TRACE.md"

# Extraire event et agent via regex bash (pas de spawn python)
event_name="unknown"
agent_name="unknown"

if [[ "$input" =~ \"hook_event_name\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  event_name="${BASH_REMATCH[1]}"
elif [[ "$input" =~ \"hookEventName\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  event_name="${BASH_REMATCH[1]}"
fi

if [[ "$input" =~ \"agent_type\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  agent_name="${BASH_REMATCH[1]}"
elif [[ "$input" =~ \"agentName\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
  agent_name="${BASH_REMATCH[1]}"
fi

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
