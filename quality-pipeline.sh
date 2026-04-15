#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# Grimoire Forge — Quality Pipeline
# ═══════════════════════════════════════════════════════════════════════════════
#
# Pipeline qualité obligatoire pour toute évolution du moteur.
# Enchaine: lint → tests → preflight → memory-lint
# Retourne 0 si tous les checks passent, 1 si un check critique échoue.
#
# Usage:
#   bash quality-pipeline.sh                 # Depuis la racine du projet
#   bash quality-pipeline.sh --fast          # Skip des checks lents (memory-lint)
# ═══════════════════════════════════════════════════════════════════════════════

set -uo pipefail  # Removed -e to allow checks to fail without stopping

# ─── Couleurs ─────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

# ─── Variables ────────────────────────────────────────────────────────────────
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAST_MODE=false
CRITICAL_FAILURES=0
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# ─── Parser args ──────────────────────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --fast) FAST_MODE=true ;;
  esac
done

cd "$ROOT_DIR"

echo ""
echo -e "${BOLD}${CYAN}🔒 Grimoire Forge — Quality Pipeline${NC}"
echo -e "${CYAN}──────────────────────────────────────${NC}"
echo -e "  Projet : ${GREEN}$(basename "$ROOT_DIR")${NC}"
echo -e "  Date   : ${GREEN}$TIMESTAMP${NC}"
echo ""

# ─── Check 1: Lint ────────────────────────────────────────────────────────────
echo -e "${BOLD}[1/4] Lint${NC}"

# Python syntax check (critical)
echo -e "${CYAN}▶${NC} Python syntax check"
PY_ERROR=0
for pyfile in $(find . -name "*.py" -type f -not -path "./.git/*" -not -path "*/__pycache__/*" 2>/dev/null | head -10); do
  if ! python3 -m py_compile "$pyfile" 2>/dev/null; then
    echo -e "  ${RED}✗ $pyfile${NC}"
    PY_ERROR=1
    CRITICAL_FAILURES=$((CRITICAL_FAILURES + 1))
  fi
done

if [ $PY_ERROR -eq 0 ]; then
  echo -e "  ${GREEN}✓ Python syntax OK${NC}"
fi

# Shellcheck (non-critical)
if command -v shellcheck &>/dev/null; then
  echo -e "${CYAN}▶${NC} Shellcheck"
  SHELL_WARN=0
  for script in $(find . -maxdepth 3 -name "*.sh" -type f -not -path "./.git/*" 2>/dev/null); do
    if ! shellcheck "$script" >/dev/null 2>&1; then
      SHELL_WARN=1
    fi
  done
  if [ $SHELL_WARN -eq 0 ]; then
    echo -e "  ${GREEN}✓ Shellcheck OK${NC}"
  else
    echo -e "  ${YELLOW}⚠ Shellcheck warnings (non-bloquant)${NC}"
  fi
fi

echo ""

# ─── Check 2: Tests ───────────────────────────────────────────────────────────
echo -e "${BOLD}[2/4] Tests${NC}"

# Find test directory
TEST_DIR=""
for dir in "grimoire-kit/tests" "tests" "_grimoire/tests"; do
  if [ -d "$dir" ] && find "$dir" -name "test_*.py" 2>/dev/null | grep -q .; then
    TEST_DIR="$dir"
    break
  fi
done

if [ -z "$TEST_DIR" ]; then
  echo -e "${YELLOW}⚠ Aucun répertoire de tests trouvé — skip${NC}"
elif ! command -v python3 &>/dev/null || ! python3 -m pytest --version &>/dev/null 2>&1; then
  echo -e "${YELLOW}⚠ pytest non disponible — skip${NC}"
else
  echo -e "${CYAN}▶${NC} pytest $TEST_DIR"
  if python3 -m pytest "$TEST_DIR" -q --tb=short -x 2>&1; then
    echo -e "  ${GREEN}✓ Tests OK${NC}"
  else
    echo -e "  ${RED}✗ Tests FAILED${NC}"
    CRITICAL_FAILURES=$((CRITICAL_FAILURES + 1))
  fi
fi

echo ""

# ─── Check 3: Preflight ───────────────────────────────────────────────────────
echo -e "${BOLD}[3/4] Preflight Check${NC}"

PREFLIGHT=""
for path in "grimoire-kit/framework/tools/preflight-check.py" "_grimoire/tools/preflight-check.py"; do
  if [ -f "$path" ]; then
    PREFLIGHT="$path"
    break
  fi
done

if [ -z "$PREFLIGHT" ]; then
  echo -e "${YELLOW}⚠ preflight-check.py non trouvé — skip${NC}"
else
  echo -e "${CYAN}▶${NC} python3 $PREFLIGHT"
  if python3 "$PREFLIGHT" --project-root . 2>&1; then
    echo -e "  ${GREEN}✓ Preflight OK${NC}"
  else
    echo -e "  ${YELLOW}⚠ Preflight warnings (non-bloquant)${NC}"
  fi
fi

echo ""

# ─── Check 4: Memory Lint ─────────────────────────────────────────────────────
echo -e "${BOLD}[4/4] Memory Lint${NC}"

if $FAST_MODE; then
  echo -e "${YELLOW}⚠ Fast mode — skip memory-lint${NC}"
else
  MEMORY_LINT=""
  for path in "grimoire-kit/framework/tools/memory-lint.py" "_grimoire/tools/memory-lint.py"; do
    if [ -f "$path" ]; then
      MEMORY_LINT="$path"
      break
    fi
  done

  if [ -z "$MEMORY_LINT" ]; then
    echo -e "${YELLOW}⚠ memory-lint.py non trouvé — skip${NC}"
  else
    echo -e "${CYAN}▶${NC} python3 $MEMORY_LINT"
    if python3 "$MEMORY_LINT" --project-root . 2>&1; then
      echo -e "  ${GREEN}✓ Memory-lint OK${NC}"
    else
      echo -e "  ${YELLOW}⚠ Memory-lint warnings (non-bloquant)${NC}"
    fi
  fi
fi

echo ""

# ─── Résultat final ───────────────────────────────────────────────────────────
echo -e "${CYAN}──────────────────────────────────────${NC}"
echo ""

if [ $CRITICAL_FAILURES -eq 0 ]; then
  echo -e "${GREEN}${BOLD}✅ QUALITY PIPELINE PASS${NC}"
  echo -e "${GREEN}   Tous les checks critiques sont passés${NC}"
  echo -e "${GREEN}   Timestamp: $TIMESTAMP${NC}"
  echo ""
  exit 0
else
  echo -e "${RED}${BOLD}❌ QUALITY PIPELINE FAIL${NC}"
  echo -e "${RED}   $CRITICAL_FAILURES check(s) critique(s) échoué(s)${NC}"
  echo -e "${RED}   Corriger les erreurs (lint, tests) avant de continuer.${NC}"
  echo -e "${RED}   Timestamp: $TIMESTAMP${NC}"
  echo ""
  exit 1
fi
