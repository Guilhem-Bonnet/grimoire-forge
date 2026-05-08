#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_SCRIPT="$SCRIPT_DIR/grimoire-kit/grimoire.sh"

if [[ ! -f "$KIT_SCRIPT" ]]; then
  echo "Erreur: script introuvable: $KIT_SCRIPT" >&2
  exit 1
fi

exec bash "$KIT_SCRIPT" "$@"
