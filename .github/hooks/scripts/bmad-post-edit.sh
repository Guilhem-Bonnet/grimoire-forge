#!/usr/bin/env bash
# bmad-post-edit.sh — PostToolUse hook
# Après une édition de fichier Python, vérifie le lint automatiquement.

set -euo pipefail

input=$(cat)

tool_name=$(echo "$input" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('toolName', ''))
except: pass
" 2>/dev/null || echo "")

file_path=$(echo "$input" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    params = data.get('toolInput', {})
    for key in ('filePath', 'path', 'file'):
        if key in params:
            print(params[key])
            break
except: pass
" 2>/dev/null || echo "")

# Seulement pour les outils d'édition
case "$tool_name" in
  replace_string_in_file|multi_replace_string_in_file|create_file)
    ;;
  *)
    echo "{}"
    exit 0
    ;;
esac

# --- Python lint ---
if [[ "$file_path" == *.py ]]; then
  PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
  if command -v python3 &>/dev/null && [[ -f "$file_path" ]]; then
    lint_output=$(python3 -m ruff check "$file_path" --no-fix -q 2>&1 | head -5 || true)
    if [[ -n "$lint_output" ]]; then
      lint_output=$(echo "$lint_output" | sed 's/"/\\"/g' | tr '\n' ' ')
      echo "{\"systemMessage\": \"[BMAD Lint] Problèmes détectés dans $file_path: $lint_output\"}"
      exit 0
    fi
  fi
fi

# --- UDF Frontmatter validation (Point 6 — Party Review) ---
# Valide le YAML frontmatter des artefacts UDF après création/édition
if [[ "$file_path" == *.agent.md || "$file_path" == *.prompt.md || "$file_path" == *.instructions.md || "$file_path" == */SKILL.md ]]; then
  if command -v python3 &>/dev/null && [[ -f "$file_path" ]]; then
    fm_error=$(python3 -c "
import sys
try:
    with open(sys.argv[1]) as f:
        content = f.read()
    if not content.startswith('---'):
        print('Pas de frontmatter YAML détecté (doit commencer par ---)')
        sys.exit(0)
    end = content.find('---', 3)
    if end == -1:
        print('Frontmatter non fermé (--- de fermeture manquant)')
        sys.exit(0)
    import yaml
    fm = yaml.safe_load(content[3:end])
    if not isinstance(fm, dict):
        print('Frontmatter invalide: doit être un mapping YAML')
        sys.exit(0)
    if not fm.get('description'):
        print('Champ description manquant dans le frontmatter')
        sys.exit(0)
except yaml.YAMLError as e:
    print(f'Erreur YAML dans le frontmatter: {e}')
except Exception:
    pass
" "$file_path" 2>/dev/null || true)
    if [[ -n "$fm_error" ]]; then
      fm_error=$(echo "$fm_error" | sed 's/"/\\"/g' | tr '\n' ' ')
      echo "{\"systemMessage\": \"[BMAD UDF] Frontmatter invalide dans $file_path: $fm_error\"}"
      exit 0
    fi
  fi
fi

echo "{}"
