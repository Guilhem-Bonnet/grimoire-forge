#!/usr/bin/env bash#!/usr/bin/env bash






















































fi  echo "{}"else  }'    }      "permissionDecisionReason": "Ce fichier est dans _bmad/_memory/ (mémoire BMAD protégée). Confirmer la modification."      "permissionDecision": "ask",      "hookEventName": "PreToolUse",    "hookSpecificOutput": {  echo '{if echo "$file_path" | grep -q '_bmad/_memory/'; then# Vérifier si le chemin touche la mémoire BMADesac    ;;    exit 0    echo "{}"  *)    ;;  create_file|replace_string_in_file|multi_replace_string_in_file|edit_notebook_file)case "$tool_name" in# Ne vérifier que les outils d'écriture" 2>/dev/null || echo "")except: pass            break            print(params[key])        if key in params:    for key in ('filePath', 'path', 'file'):    # Chercher un chemin de fichier dans les paramètres courants    params = data.get('toolInput', {})    data = json.load(sys.stdin)try:import sys, jsonfile_path=$(echo "$input" | python3 -c "" 2>/dev/null || echo "")except: pass    print(data.get('toolName', ''))    data = json.load(sys.stdin)try:import sys, jsontool_name=$(echo "$input" | python3 -c "# Extraire le nom de l'outil et le chemin du fichierinput=$(cat)# Lire le JSON d'entrée depuis stdinset -euo pipefail# Demande confirmation avant toute modification dans _bmad/_memory/.# Protège les fichiers mémoire BMAD contre les écritures accidentelles.# bmad-memory-guard.sh — PreToolUse hook# bmad-memory-guard.sh — PreToolUse hook
# Protège les fichiers mémoire BMAD contre les écritures accidentelles.
# Demande confirmation (ask) avant toute modification dans _bmad/_memory/.

set -euo pipefail

INPUT=$(cat)

# Extraire le nom de l'outil et le chemin du fichier depuis le JSON d'entrée
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('toolName',''))" 2>/dev/null || echo "")
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); i=d.get('input',{}); print(i.get('filePath', i.get('path','')))" 2>/dev/null || echo "")

# Ne vérifier que les outils d'écriture (edit, create, replace)
WRITE_TOOLS="create_file replace_string_in_file multi_replace_string_in_file"

IS_WRITE=false
for wt in $WRITE_TOOLS; do
  if [[ "$TOOL_NAME" == "$wt" ]]; then
    IS_WRITE=true
    break
  fi
done

if [[ "$IS_WRITE" == "true" && "$FILE_PATH" == *"_bmad/_memory/"* ]]; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Modification d'un fichier mémoire BMAD (_bmad/_memory/). Confirmer ?"
  }
}
EOF
else
  echo '{"continue": true}'
fi
