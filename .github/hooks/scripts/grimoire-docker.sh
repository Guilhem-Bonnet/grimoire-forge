#!/usr/bin/env bash
# grimoire-docker.sh - Docker wrapper for shells that have not reloaded groups.

set -uo pipefail

err_file="$(mktemp)"
trap 'rm -f "$err_file"' EXIT

if docker "$@" 2>"$err_file"; then
  exit 0
fi

status=$?
if grep -qi "permission denied" "$err_file" && command -v sg >/dev/null 2>&1 && getent group docker >/dev/null 2>&1; then
  exec sg docker -c "$(printf '%q ' docker "$@")"
fi

cat "$err_file" >&2
exit "$status"
