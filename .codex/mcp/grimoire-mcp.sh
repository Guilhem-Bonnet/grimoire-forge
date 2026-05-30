#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "${ROOT_DIR}/grimoire-kit"
export PYTHONPATH="${ROOT_DIR}/grimoire-kit/src${PYTHONPATH:+:${PYTHONPATH}}"
export GRIMOIRE_QDRANT_URL="${GRIMOIRE_QDRANT_URL:-http://localhost:6333}"

exec "${ROOT_DIR}/grimoire-kit/.venv/bin/python" -m grimoire.mcp.server "$@"
