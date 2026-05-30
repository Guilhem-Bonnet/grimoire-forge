#!/usr/bin/env bash
# grimoire-hook-gateway.sh — stable wrapper around hook scripts.
# Route chaque hook via un registre de promotion pour eviter qu'un hook
# recemment modifie bloque tout le runtime avant validation explicite.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
python_bin="$project_root/grimoire-kit/.venv/bin/python"

if [[ ! -x "$python_bin" ]]; then
  python_bin="$(command -v python3 || true)"
fi

if [[ -z "$python_bin" ]]; then
  echo '{"continue": true, "systemMessage": "Hook gateway indisponible: python3 introuvable."}'
  exit 1
fi

exec "$python_bin" "$project_root/grimoire-kit/framework/tools/hook-safety-gate.py" --project-root "$project_root" invoke "$@"