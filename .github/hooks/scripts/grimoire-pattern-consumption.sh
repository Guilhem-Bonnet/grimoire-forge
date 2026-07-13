#!/usr/bin/env bash
# grimoire-pattern-consumption.sh — SessionStart hook (via gateway, mode shadow).
# Garde-fou « fonctionnel = consommé » (lot 4 durcissement agentique) :
# joue le contrôle statique rapide de grimoire-pattern-consumption-check.py.
# Fail-open : toute erreur interne émet {} et sort en 0.

set -euo pipefail
trap 'echo "{}"; exit 0' ERR

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
check_script="$project_root/.github/hooks/scripts/grimoire-pattern-consumption-check.py"

# Consommer stdin (contrat hook JSON) sans l'utiliser.
cat >/dev/null || true

python_bin="$project_root/grimoire-kit/.venv/bin/python"
if [[ ! -x "$python_bin" ]]; then
  python_bin="$(command -v python3 || true)"
fi

if [[ -z "$python_bin" || ! -f "$check_script" ]]; then
  echo "{}"
  exit 0
fi

if "$python_bin" "$check_script" --project-root "$project_root" --static-only >/dev/null 2>&1; then
  echo "{}"
  exit 0
fi

# Violations statiques : message non bloquant (le hook reste fail-open).
printf '{"continue": true, "systemMessage": "Pattern-consumption check: sigles de protocoles non gouvernes detectes dans les instructions. Lancer la task \\"grimoire: pattern-consumption-check\\" pour le detail."}\n'
