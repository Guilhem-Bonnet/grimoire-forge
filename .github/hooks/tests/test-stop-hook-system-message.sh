#!/usr/bin/env bash
# test-stop-hook-system-message.sh
#
# Verifie que grimoire-master-stop-hook.sh relaie systemMessage des qu'il
# est present dans la sortie de guardrail-policy.py stop-closure, meme
# quand ce payload ne porte NI decision=block NI additionalContext.
#
# Ecart couvert : relecture Copilot PR #32 (grimoire-master-stop-hook.sh:90)
# — guardrail-policy.py peut renvoyer un payload Stop ne contenant QUE
# systemMessage (enforcement du budget de tokens, ecart B2). Avant
# correction, ce cas tombait dans le bloc par defaut et le message etait
# perdu : ce test ECHOUE sur le code d'origine et PASSE une fois le
# relayage corrige.
#
# Usage: bash .github/hooks/tests/test-stop-hook-system-message.sh

set -uo pipefail

repo_root="$(cd "$(dirname "$0")/../../.." && pwd)"
scripts_dir="$repo_root/.github/hooks/scripts"

failures=0

fail() {
  echo "FAIL: $1" >&2
  failures=$((failures + 1))
}

pass() {
  echo "PASS: $1"
}

fixture_dir="$(mktemp -d)"
trap 'rm -rf "$fixture_dir"' EXIT

mkdir -p "$fixture_dir/.github/hooks/scripts" "$fixture_dir/.github/hooks/lib"
cp "$scripts_dir/grimoire-master-stop-hook.sh" "$fixture_dir/.github/hooks/scripts/"
chmod +x "$fixture_dir/.github/hooks/scripts/grimoire-master-stop-hook.sh"

# Politique fictive : ne renvoie qu'un systemMessage, sans
# hookSpecificOutput.decision ni additionalContext — reproduit le payload
# que guardrail-policy.py emet quand seul l'enforcement du budget de
# tokens est declenche.
cat > "$fixture_dir/.github/hooks/lib/guardrail-policy.py" <<'PY'
import sys
print('{"systemMessage": "Budget de tokens: 91% (critical) — resume recommande."}')
PY

output="$(printf '{}' | "$fixture_dir/.github/hooks/scripts/grimoire-master-stop-hook.sh" 2>/dev/null)"

if [[ -z "$output" ]]; then
  fail "sortie vide (attendu: JSON portant systemMessage)"
elif ! printf '%s' "$output" | python3 -c '
import json, sys
data = json.loads(sys.stdin.read())
message = data.get("systemMessage", "")
assert message, "systemMessage absent ou vide"
assert "Budget de tokens" in message, f"contenu inattendu: {message!r}"
' 2>/dev/null; then
  fail "systemMessage absent de la sortie du hook Stop — sortie: ${output}"
else
  pass "grimoire-master-stop-hook.sh relaie systemMessage seul (sans decision=block ni additionalContext)"
fi

if [[ "$failures" -gt 0 ]]; then
  echo "test-stop-hook-system-message: ${failures} assertion(s) en echec" >&2
  exit 1
fi

echo "test-stop-hook-system-message: ok (1/1 assertion)"
