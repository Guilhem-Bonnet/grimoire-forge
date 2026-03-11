#!/usr/bin/env bash
# bmad-cleanup-dynamic-artifacts.sh
# Nettoie les artefacts dynamiques (_dyn-*) dont la date d'expiration est dépassée.
# Couvre : agents, workflows (prompts), skills, instructions.
# Peut être exécuté manuellement ou via cron/task.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TODAY=$(date '+%Y-%m-%d')

cleaned=0
kept=0

# Fonction générique de nettoyage
cleanup_expired() {
  local pattern="$1"
  local label="$2"

  for file in $pattern; do
    [[ -f "$file" ]] || continue

    # Extraire la date d'expiration du frontmatter (format: expires: YYYY-MM-DD)
    expires=$(grep "^expires:" "$file" | sed 's/^expires: *//' | tr -d "'" | tr -d '"' | head -1)

    if [[ -z "$expires" ]]; then
      kept=$((kept + 1))
      continue
    fi

    if [[ "$TODAY" > "$expires" || "$TODAY" == "$expires" ]]; then
      name=$(basename "$file")
      echo "EXPIRED [$label]: $name (expires: $expires) → supprimé"
      rm "$file"
      cleaned=$((cleaned + 1))
    else
      kept=$((kept + 1))
    fi
  done
}

# 1. Agents dynamiques
cleanup_expired "$PROJECT_ROOT/.github/agents/_dyn-*.agent.md" "agent"

# 2. Workflows dynamiques (prompts)
cleanup_expired "$PROJECT_ROOT/.github/prompts/_dyn-*.prompt.md" "workflow"

# 3. Skills dynamiques (dossiers _dyn-*/SKILL.md)
for skill_dir in "$PROJECT_ROOT/.github/skills"/_dyn-*/; do
  [[ -d "$skill_dir" ]] || continue
  skill_file="$skill_dir/SKILL.md"
  [[ -f "$skill_file" ]] || continue

  expires=$(grep "^expires:" "$skill_file" | sed 's/^expires: *//' | tr -d "'" | tr -d '"' | head -1)

  if [[ -z "$expires" ]]; then
    kept=$((kept + 1))
    continue
  fi

  if [[ "$TODAY" > "$expires" || "$TODAY" == "$expires" ]]; then
    name=$(basename "$skill_dir")
    echo "EXPIRED [skill]: $name (expires: $expires) → supprimé"
    rm -r "$skill_dir"
    cleaned=$((cleaned + 1))
  else
    kept=$((kept + 1))
  fi
done

# 4. Instructions dynamiques
cleanup_expired "$PROJECT_ROOT/.github/instructions/_dyn-*.instructions.md" "instruction"

echo ""
echo "Résultat: $cleaned artefact(s) nettoyé(s), $kept artefact(s) conservé(s)"
