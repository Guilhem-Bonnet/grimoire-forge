#!/usr/bin/env bash
set -euo pipefail

standard_command="${1:-}"
if [[ -z "$standard_command" ]]; then
  echo "usage: scripts/run-standard.sh <standard-subcommand> [args...]" >&2
  exit 2
fi
shift

supports_standard() {
  "$1" standard --help >/dev/null 2>&1
}

run_if_supported() {
  local candidate="$1"
  shift
  if [[ -x "$candidate" ]] && supports_standard "$candidate"; then
    exec "$candidate" standard "$standard_command" "$@"
  fi
}

if [[ -n "${GRIMOIRE_CLI:-}" ]]; then
  run_if_supported "$GRIMOIRE_CLI" "$@"
fi

run_if_supported "grimoire-kit/.venv/bin/grimoire" "$@"
run_if_supported "../Grimoire-kit-agentic-standard-bridge/.venv/bin/grimoire" "$@"

if command -v grimoire >/dev/null 2>&1; then
  run_if_supported "$(command -v grimoire)" "$@"
fi

echo "No grimoire CLI with the 'standard' command was found. Install grimoire-kit or set GRIMOIRE_CLI." >&2
exit 127
