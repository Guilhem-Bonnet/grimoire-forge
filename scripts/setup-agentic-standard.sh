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

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-root)
      PROJECT_ROOT="$2"
      shift 2
      ;;
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --task-id)
      TASK_ID="$2"
      shift 2
      ;;
    --provider)
      PROVIDER_ARGS+=(--provider "$2")
      shift 2
      ;;
    --providers)
      PROVIDER_ARGS+=(--providers "$2")
      shift 2
      ;;
    --provider-policy)
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
