#!/usr/bin/env bash
# bmad-memory-guard.sh — PreToolUse hook
# Protège les fichiers mémoire BMAD contre les écritures accidentelles.
# Optimisé : fast-path pure bash, python uniquement si nécessaire.

set -euo pipefail

INPUT=$(cat)

# Fast-path : si le JSON ne contient pas _bmad/_memory, on skip immédiatement
# Ça évite de spawner python pour 95% des tool calls
if [[ "$INPUT" != *"_bmad/_memory/"* ]]; then
  echo '{"continue": true}'
  exit 0
fi

# Seuls les outils d'écriture sont concernés
if [[ "$INPUT" != *"create_file"* && "$INPUT" != *"replace_string_in_file"* && "$INPUT" != *"multi_replace_string_in_file"* ]]; then
  echo '{"continue": true}'
  exit 0
fi

# Si on arrive ici, c'est un write sur _bmad/_memory → demander confirmation
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Modification d'un fichier mémoire BMAD (_bmad/_memory/). Confirmer ?"
  }
}
EOF
