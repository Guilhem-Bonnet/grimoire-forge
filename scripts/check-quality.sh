#!/usr/bin/env bash
# Pipeline qualité obligatoire (issue #1).
#
# Enchaîne, en une seule commande, les checks critiques avant toute évolution
# du moteur Grimoire Forge :
#   1. Lint         — ShellCheck + bash -n (scripts du dépôt) et Ruff (moteur)
#   2. Tests        — suite unitaire du moteur grimoire-kit
#   3. Préflight    — `framework/tools/preflight-check.py` sur le moteur
#   4. Memory-lint  — `framework/tools/memory-lint.py` sur le moteur
#   5. Gouvernance  — `standard verify` (profil governed)
#
# Un check critique en échec rend la commande bloquante (exit code != 0).
# Les checks dont l'outillage est absent sont ignorés avec une note explicite,
# en miroir du comportement de la CI (`.github/workflows/ci.yml`), afin que la
# commande reste exécutable sur un checkout sans moteur embarqué.
#
# Variables :
#   GRIMOIRE_KIT_DIR    Checkout du moteur (défaut : grimoire-kit)
#   GRIMOIRE_CLI        CLI grimoire explicite pour la gouvernance
#   QUALITY_SKIP_TESTS  =1 pour sauter la suite de tests (itération rapide)
#
# Usage :
#   bash scripts/check-quality.sh
#   npm run quality
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR" || exit 1

KIT_DIR="${GRIMOIRE_KIT_DIR:-grimoire-kit}"

if [[ -t 1 ]]; then
  C_RESET=$'\033[0m'; C_BOLD=$'\033[1m'
  C_GREEN=$'\033[32m'; C_YELLOW=$'\033[33m'; C_RED=$'\033[31m'
else
  C_RESET=""; C_BOLD=""; C_GREEN=""; C_YELLOW=""; C_RED=""
fi

PASSED=(); SKIPPED=(); FAILED=()

section() { printf '\n%s== %s ==%s\n' "$C_BOLD" "$1" "$C_RESET"; }
pass()    { PASSED+=("$1"); printf '  %s✓%s %s\n' "$C_GREEN" "$C_RESET" "$1"; }
skip()    { SKIPPED+=("$1"); printf '  %s∼%s %s (ignoré : %s)\n' "$C_YELLOW" "$C_RESET" "$1" "$2"; }
fail()    { FAILED+=("$1"); printf '  %s✗%s %s\n' "$C_RED" "$C_RESET" "$1"; }

# Détecte un moteur grimoire-kit embarqué utilisable (checkout + venv Python).
KIT_PY="$KIT_DIR/.venv/bin/python"
kit_present() { [[ -d "$KIT_DIR" && -x "$KIT_PY" ]]; }

# Scripts shell versionnés du dépôt (hors moteur embarqué, qui a sa propre CI).
repo_scripts() { find scripts -maxdepth 1 -type f -name '*.sh' 2>/dev/null | sort; }

# Découvre un CLI grimoire supportant une sous-commande donnée.
discover_cli() {
  local subcommand="$1" candidate
  for candidate in \
    "${GRIMOIRE_CLI:-}" \
    "$KIT_DIR/.venv/bin/grimoire" \
    "../Grimoire-kit-agentic-standard-bridge/.venv/bin/grimoire" \
    "$(command -v grimoire 2>/dev/null || true)"; do
    [[ -n "$candidate" && -x "$candidate" ]] || continue
    if "$candidate" "$subcommand" --help >/dev/null 2>&1; then
      printf '%s' "$candidate"; return 0
    fi
  done
  return 1
}

# 1. Lint
section "1/6 Lint"
# 1a. ShellCheck sur les scripts du dépôt
if command -v shellcheck >/dev/null 2>&1; then
  mapfile -t _scripts < <(repo_scripts)
  if [[ ${#_scripts[@]} -eq 0 ]]; then
    skip "ShellCheck" "aucun script dans scripts/"
  elif shellcheck -S warning "${_scripts[@]}"; then
    pass "ShellCheck (${#_scripts[@]} script(s))"
  else
    fail "ShellCheck"
  fi
else
  skip "ShellCheck" "binaire shellcheck absent"
fi
# 1b. Syntaxe bash (toujours disponible)
_syntax_ok=1; _syntax_n=0
while IFS= read -r _s; do
  [[ -n "$_s" ]] || continue
  _syntax_n=$((_syntax_n + 1))
  bash -n "$_s" || { _syntax_ok=0; printf '    erreur de syntaxe : %s\n' "$_s"; }
done < <(repo_scripts)
if [[ $_syntax_n -eq 0 ]]; then
  skip "Syntaxe bash" "aucun script dans scripts/"
elif [[ $_syntax_ok -eq 1 ]]; then
  pass "Syntaxe bash ($_syntax_n script(s))"
else
  fail "Syntaxe bash"
fi
# 1c. Ruff sur le moteur
if kit_present && [[ -x "$KIT_DIR/.venv/bin/ruff" ]]; then
  if (cd "$KIT_DIR" && .venv/bin/ruff check framework/tools/ tests/ --quiet); then
    pass "Ruff (moteur framework/tools + tests)"
  else
    fail "Ruff"
  fi
else
  skip "Ruff" "moteur grimoire-kit/.venv absent"
fi

# 2. Tests
section "2/6 Tests — moteur grimoire-kit"
if [[ "${QUALITY_SKIP_TESTS:-0}" == "1" ]]; then
  skip "Tests" "QUALITY_SKIP_TESTS=1"
elif kit_present && [[ -d "$KIT_DIR/tests/unit" ]]; then
  if (cd "$KIT_DIR" && .venv/bin/python -m pytest tests/unit -q --tb=short); then
    pass "pytest tests/unit"
  else
    fail "pytest tests/unit"
  fi
else
  skip "Tests" "moteur grimoire-kit absent (couvert par la CI Kit)"
fi

# 3. Préflight
section "3/6 Préflight — preflight-check.py"
if kit_present && [[ -f "$KIT_DIR/framework/tools/preflight-check.py" ]]; then
  if (cd "$KIT_DIR" && .venv/bin/python framework/tools/preflight-check.py --project-root . --quiet); then
    pass "preflight-check (moteur)"
  else
    fail "preflight-check"
  fi
else
  skip "Préflight" "moteur grimoire-kit absent"
fi

# 4. Memory-lint
section "4/6 Memory-lint — memory-lint.py"
if kit_present && [[ -f "$KIT_DIR/framework/tools/memory-lint.py" ]]; then
  if (cd "$KIT_DIR" && .venv/bin/python framework/tools/memory-lint.py --project-root .); then
    pass "memory-lint (moteur)"
  else
    fail "memory-lint"
  fi
else
  skip "Memory-lint" "moteur grimoire-kit absent"
fi

# 5. Gouvernance — standard verify
section "5/6 Gouvernance — standard verify"
if cli=$(discover_cli standard); then
  if bash scripts/run-standard.sh verify; then
    pass "standard verify ($cli)"
  else
    fail "standard verify"
  fi
else
  skip "Gouvernance" "aucun CLI grimoire avec la commande 'standard'"
fi

# 6. Preuve — chaine de preuve des workflows (chantiers C1-C3)
section "6/6 Preuve — transitions kanban, evidence, steps"
if kit_present; then
  if "$KIT_PY" scripts/board-transitions-log.py --project-root . check; then
    pass "board-transitions check"
  else
    fail "board-transitions check"
  fi
  if "$KIT_PY" scripts/evidence-reconcile.py --project-root .; then
    pass "evidence-reconcile"
  else
    fail "evidence-reconcile"
  fi
  if "$KIT_PY" scripts/workflow-step-check.py --project-root .; then
    pass "workflow-step-check"
  else
    fail "workflow-step-check"
  fi
else
  skip "Preuve" "moteur grimoire-kit absent (loader YAML requis)"
fi

# Synthèse
section "Synthèse qualité"
printf '  %s%d réussi(s)%s · %s%d ignoré(s)%s · %s%d échec(s)%s\n' \
  "$C_GREEN" "${#PASSED[@]}" "$C_RESET" \
  "$C_YELLOW" "${#SKIPPED[@]}" "$C_RESET" \
  "$C_RED" "${#FAILED[@]}" "$C_RESET"

if [[ ${#FAILED[@]} -gt 0 ]]; then
  printf '\n%sPipeline qualité : ÉCHEC%s — %s\n' "$C_RED" "$C_RESET" "${FAILED[*]}"
  exit 1
fi
printf '\n%sPipeline qualité : OK%s\n' "$C_GREEN" "$C_RESET"
exit 0
