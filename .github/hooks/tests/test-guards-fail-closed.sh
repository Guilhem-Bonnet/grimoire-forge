#!/usr/bin/env bash
# test-guards-fail-closed.sh
#
# Verifie que grimoire-control-surface-guard.sh et grimoire-memory-guard.sh
# echouent fermes (permissionDecision=ask, avec une raison) au lieu
# d'autoriser en silence ("{}") quand :
#   1. le script de politique (guardrail-policy.py) est absent
#   2. l'appel a la politique echoue (exit code != 0)
#   3. la politique renvoie une sortie invalide (JSON malforme)
#   4. la politique renvoie une sortie vide
#
# Ecart couvert : B1 (audit-ecarts-reference-agentique-20260908.md, action
# A1 du plan-execution-ecarts-20260908.md). Ce test ECHOUE sur le code
# d'origine (`echo "{}"; exit 0` dans les trois cas) et PASSE une fois le
# fail-closed applique. Verifie manuellement avant correction: en pointant
# ce test sur les scripts d'origine (git show origin/main:...), les quatre
# assertions "control-surface-guard" et "memory-guard" echouent — la
# sortie observee est "{}" au lieu de permissionDecision=ask.
#
# Usage: bash .github/hooks/tests/test-guards-fail-closed.sh

set -uo pipefail

repo_root="$(cd "$(dirname "$0")/../../.." && pwd)"
scripts_dir="$repo_root/.github/hooks/scripts"

failures=0

# Fichier d'erreur temporaire et reentrant (au lieu d'un chemin fixe sous
# /tmp) : deux executions concurrentes de ce test ne doivent pas se
# marcher dessus.
err_file="$(mktemp)"
trap 'rm -f "$err_file"' EXIT

fail() {
  echo "FAIL: $1" >&2
  failures=$((failures + 1))
}

pass() {
  echo "PASS: $1"
}

# Construit un projet jetable qui reproduit l'arborescence attendue par les
# scripts testes (project_root = .github/hooks/scripts/../../..), avec une
# politique fictive selon le mode d'echec simule.
make_fixture_project() {
  local mode="$1"
  local dir
  dir="$(mktemp -d)"
  mkdir -p "$dir/.github/hooks/scripts" "$dir/.github/hooks/lib"
  cp "$scripts_dir/grimoire-control-surface-guard.sh" "$dir/.github/hooks/scripts/"
  cp "$scripts_dir/grimoire-memory-guard.sh" "$dir/.github/hooks/scripts/"
  chmod +x "$dir/.github/hooks/scripts/"*.sh

  case "$mode" in
    missing-script)
      : # pas de guardrail-policy.py -> le guard doit fail-closed
      ;;
    failing-call)
      cat > "$dir/.github/hooks/lib/guardrail-policy.py" <<'PY'
import sys
sys.exit(1)
PY
      ;;
    invalid-json)
      cat > "$dir/.github/hooks/lib/guardrail-policy.py" <<'PY'
print("not-json{{")
PY
      ;;
    empty-json)
      cat > "$dir/.github/hooks/lib/guardrail-policy.py" <<'PY'
print("", end="")
PY
      ;;
    *)
      echo "mode inconnu: $mode" >&2
      exit 2
      ;;
  esac
  printf '%s' "$dir"
}

# Verifie que le script renvoie hookSpecificOutput.permissionDecision=ask
# avec une permissionDecisionReason non vide, jamais "{}".
assert_ask_decision() {
  local script_path="$1"
  local mode="$2"
  local output
  output="$(printf '{"tool_name":"Bash","tool_input":{"command":"echo hi"}}' | "$script_path" 2>/dev/null)"

  if [[ -z "$output" ]]; then
    fail "$(basename "$script_path") ($mode): sortie vide (attendu: JSON avec permissionDecision=ask)"
    return 1
  fi

  if [[ "$output" == "{}" ]]; then
    fail "$(basename "$script_path") ($mode): autorisation silencieuse \"{}\" au lieu d'un ask trace"
    return 1
  fi

  if ! printf '%s' "$output" | python3 -c '
import json, sys
try:
    data = json.loads(sys.stdin.read())
except Exception as exc:
    print(f"json invalide: {exc}", file=sys.stderr)
    sys.exit(1)
spec = data.get("hookSpecificOutput", {})
decision = spec.get("permissionDecision")
if decision != "ask":
    print(f"permissionDecision inattendu: {decision}", file=sys.stderr)
    sys.exit(1)
if not spec.get("permissionDecisionReason"):
    print("permissionDecisionReason manquante ou vide", file=sys.stderr)
    sys.exit(1)
' 2>"$err_file"; then
    fail "$(basename "$script_path") ($mode): $(cat "$err_file") — sortie: ${output}"
    return 1
  fi

  pass "$(basename "$script_path") ($mode) -> ask avec raison"
}

for mode in missing-script failing-call invalid-json empty-json; do
  tmp_root="$(make_fixture_project "$mode")"
  assert_ask_decision "$tmp_root/.github/hooks/scripts/grimoire-control-surface-guard.sh" "$mode"
  assert_ask_decision "$tmp_root/.github/hooks/scripts/grimoire-memory-guard.sh" "$mode"
  rm -rf "$tmp_root"
done

if [[ "$failures" -gt 0 ]]; then
  echo "test-guards-fail-closed: ${failures} assertion(s) en echec" >&2
  exit 1
fi

echo "test-guards-fail-closed: ok (8/8 assertions)"
