#!/usr/bin/env bash
# grimoire-memory-guard.sh — PreToolUse hook
# Protege les fichiers memoire Grimoire contre les ecritures accidentelles.
#
# Fail-closed (ecart B1, audit-ecarts-reference-agentique-20260908.md) : si
# python ou le script de politique manquent, si l'appel a la politique
# echoue, ou si sa sortie n'est pas un JSON exploitable, la decision
# renvoyee au host est "ask" — jamais une autorisation silencieuse "{}".
# Modele de reference cote produit : src/grimoire/hosts/decisions.py,
# _failed_decision() (renvoie ASK sur PreToolUse plutot qu'ALLOW).

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
policy_script="$project_root/.github/hooks/lib/guardrail-policy.py"
policy_python="$project_root/.venv/bin/python"
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
input=$(cat)

# VALID_PHASES (grimoire_tools/events.py) = start|end|block|correct|info :
# il n'existe pas de phase "ask". Un fail-closed est trace en "block" car
# la politique n'a pas pu juger l'appel — ce n'est pas un simple "info".
emit_trace() {
  local phase="$1"
  if [[ -x "$emit_event_script" ]]; then
    "$emit_event_script" --scope tool --phase "$phase" --source-hook "grimoire-memory-guard.sh" --payload-json '{"hook":"memory-guard"}' 2>/dev/null || true
  fi
}

fail_closed() {
  local reason="$1"
  emit_trace "block"
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"%s"}}\n' "$reason"
  exit 0
}

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -z "$policy_python" || ! -f "$policy_script" ]]; then
  fail_closed "Grimoire memory-guard indisponible (python ou script de politique introuvable) : appel non juge, decision renvoyee a l'utilisateur."
fi

if ! output=$(printf '%s' "$input" | "$policy_python" "$policy_script" memory-guard 2>/dev/null); then
  fail_closed "Grimoire memory-guard a echoue a l'execution de la politique : appel non juge, decision renvoyee a l'utilisateur."
fi

if [[ -z "$output" ]] || ! printf '%s' "$output" | "$policy_python" -c 'import json, sys
json.loads(sys.stdin.read())' >/dev/null 2>&1; then
  fail_closed "Grimoire memory-guard a renvoye une sortie vide ou un JSON invalide : appel non juge, decision renvoyee a l'utilisateur."
fi

# V1 ledger: scope=tool, phase=block si policy a bloque, sinon info.
phase="info"
if [[ "$output" == *'"decision"'*'"block"'* || "$output" == *'"permissionDecision"'*'"deny"'* ]]; then
  phase="block"
fi
emit_trace "$phase"

printf '%s\n' "$output"
