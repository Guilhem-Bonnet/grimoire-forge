#!/usr/bin/env bash
# bmad-inject-context.sh — SessionStart hook
# Injecte le contexte BMAD au démarrage de chaque session agent.
# Lit _bmad/core/config.yaml et _bmad/_memory/shared-context.md,
# puis émet un systemMessage pour pré-charger le contexte.

set -euo pipefail

# Lire le JSON d'entrée depuis stdin
INPUT=$(cat)

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CONFIG_FILE="$PROJECT_ROOT/_bmad/core/config.yaml"
SHARED_CTX="$PROJECT_ROOT/_bmad/_memory/shared-context.md"

CONTEXT_PARTS=""

if [[ -f "$CONFIG_FILE" ]]; then
  # Extraire les variables clés du config
  USER_NAME=$(grep -E '^user_name:' "$CONFIG_FILE" | sed 's/^user_name: *//' | tr -d '"')
  LANG=$(grep -E '^communication_language:' "$CONFIG_FILE" | sed 's/^communication_language: *//' | tr -d '"')
  CONTEXT_PARTS="BMAD Context loaded — user: ${USER_NAME}, lang: ${LANG}."
fi

if [[ -f "$SHARED_CTX" ]]; then
  # Résumé du shared context (première ligne non-vide)
  SUMMARY=$(grep -m1 -v '^\s*$' "$SHARED_CTX" | head -c 200)
  CONTEXT_PARTS="${CONTEXT_PARTS} Shared context: ${SUMMARY}"
fi

# Émettre le systemMessage pour enrichir le contexte de la session
if [[ -n "$CONTEXT_PARTS" ]]; then
  cat <<EOF
{
  "systemMessage": "${CONTEXT_PARTS}"
}
EOF
else
  echo '{"continue": true}'
fi
