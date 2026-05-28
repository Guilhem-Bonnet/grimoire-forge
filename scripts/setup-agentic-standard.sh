#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KIT_DIR="${ROOT_DIR}/grimoire-kit"
PROJECT_ROOT="${PROJECT_ROOT:-${ROOT_DIR}}"
PROFILE="${PROFILE:-orchestrated}"
TASK_ID="${TASK_ID:-bootstrap}"

usage() {
  cat <<'USAGE'
Usage: scripts/setup-agentic-standard.sh [--project-root PATH] [--profile ID] [--task-id ID] [--provider ID] [--providers LIST] [--provider-policy POLICY] [--force] [--dry-run] [--verify-only] [--audit-only] [--detect-providers] [--markdown]

Environment overrides:
  PROJECT_ROOT   Target project root (default: repository root)
  PROFILE        starter | controlled | orchestrated | governed | production (default: orchestrated)
  TASK_ID        Evidence task id (default: bootstrap)
USAGE
}

FORCE=()
DRY_RUN=()
PROVIDER_ARGS=()
VERIFY_ONLY=false
AUDIT_ONLY=false
DETECT_PROVIDERS=false
MARKDOWN=()

require_value() {
  local option="$1"
  if [[ $# -lt 2 || -z "${2:-}" || "${2:-}" == --* ]]; then
    echo "Missing value for ${option}" >&2
    usage >&2
    exit 2
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-root)
      require_value "$@"
      PROJECT_ROOT="$2"
      shift 2
      ;;
    --profile)
      require_value "$@"
      PROFILE="$2"
      shift 2
      ;;
    --task-id)
      require_value "$@"
      TASK_ID="$2"
      shift 2
      ;;
    --provider)
      require_value "$@"
      PROVIDER_ARGS+=(--provider "$2")
      shift 2
      ;;
    --providers)
      require_value "$@"
      PROVIDER_ARGS+=(--providers "$2")
      shift 2
      ;;
    --provider-policy)
      require_value "$@"
      PROVIDER_ARGS+=(--provider-policy "$2")
      shift 2
      ;;
    --force)
      FORCE=(--force)
      shift
      ;;
    --dry-run)
      DRY_RUN=(--dry-run)
      shift
      ;;
    --verify-only)
      VERIFY_ONLY=true
      shift
      ;;
    --audit-only)
      AUDIT_ONLY=true
      shift
      ;;
    --detect-providers)
      DETECT_PROVIDERS=true
      shift
      ;;
    --markdown)
      MARKDOWN=(--markdown)
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

run_grimoire() {
  PYTHONPATH="${KIT_DIR}/src:${PYTHONPATH:-}" python3 -c 'from grimoire.cli.app import cli; cli()' "$@"
}

if [[ ! "${TASK_ID}" =~ ^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$ ]]; then
  echo "Invalid task id: ${TASK_ID}" >&2
  echo "Use 1-128 letters, numbers, dots, underscores, or hyphens, starting with a letter or number." >&2
  exit 2
fi

if [[ ! -d "${KIT_DIR}/src/grimoire" ]]; then
  echo "Missing grimoire-kit checkout at ${KIT_DIR}" >&2
  echo "Clone or checkout Grimoire-kit into ./grimoire-kit before running standard commands." >&2
  exit 2
fi

if [[ "${AUDIT_ONLY}" == "true" ]]; then
  run_grimoire standard audit "${PROJECT_ROOT}" --profile "${PROFILE}" --task-id "${TASK_ID}" "${MARKDOWN[@]}"
  exit 0
fi

if [[ "${DETECT_PROVIDERS}" == "true" ]]; then
  run_grimoire standard detect-providers
  exit 0
fi

if [[ "${VERIFY_ONLY}" != "true" ]]; then
  run_grimoire standard init "${PROJECT_ROOT}" --profile "${PROFILE}" --task-id "${TASK_ID}" "${PROVIDER_ARGS[@]}" "${FORCE[@]}" "${DRY_RUN[@]}"
fi

if [[ ${#DRY_RUN[@]} -eq 0 ]]; then
  run_grimoire standard verify "${PROJECT_ROOT}" --profile "${PROFILE}" --task-id "${TASK_ID}"
fi
