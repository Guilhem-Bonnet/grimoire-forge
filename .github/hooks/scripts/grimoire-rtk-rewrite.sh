#!/usr/bin/env bash
# grimoire-rtk-rewrite.sh — PreToolUse hook
# Route les appels d'outil shell via RTK (Rust Token Killer) pour compresser
# les sorties verboses (git, pytest, ruff, build...) avant qu'elles n'atteignent
# l'agent. Cote Copilot, RTK reecrit la commande de maniere transparente.
# Mode courant : `enforced` (voir hook-safety-registry.json) — la reecriture est
# appliquee. Repli non bloquant : `hook-safety-gate.py set-mode shadow
# grimoire-rtk-rewrite` (en shadow/canary le gateway observe sans reecrire).

set -euo pipefail

input=$(cat)

rtk_bin="$(command -v rtk || true)"
if [[ -z "$rtk_bin" ]]; then
  rtk_bin="${CARGO_HOME:-$HOME/.cargo}/bin/rtk"
fi

if [[ ! -x "$rtk_bin" ]]; then
  # RTK absent : passthrough no-op (JSON valide pour le gateway).
  echo "{}"
  exit 0
fi

if ! output=$(printf '%s' "$input" | "$rtk_bin" hook copilot 2>/dev/null); then
  echo "{}"
  exit 0
fi

if [[ -z "$output" ]]; then
  echo "{}"
  exit 0
fi

printf '%s' "$output"
