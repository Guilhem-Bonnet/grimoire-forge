#!/usr/bin/env bash
# Rotate GRIMOIRE_TRACE files when they exceed the size threshold.
# Archives to _grimoire-runtime-output/trace-archives/ with a datestamp.
# Safe to run multiple times (idempotent).
set -euo pipefail

ROOT_DIR="${1:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)}"
TRACE_DIR="${ROOT_DIR}/_grimoire-runtime-output"
ARCHIVE_DIR="${TRACE_DIR}/trace-archives"
MAX_BYTES="${TRACE_ROTATE_MAX_BYTES:-5242880}"  # 5 MB default

mkdir -p "${ARCHIVE_DIR}"

rotate_if_large() {
  local file="$1"
  local prefix="${2:-}"
  local ext="${file##*.}"
  [[ -f "${file}" ]] || return 0
  local size
  size=$(stat -c%s "${file}" 2>/dev/null || echo 0)
  if (( size >= MAX_BYTES )); then
    local ts
    ts=$(date +%Y%m%d-%H%M%S)
    local base
    base=$(basename "${file}" ".${ext}")
    [[ -n "${prefix}" ]] && base="${prefix}-${base}"
    local dest="${ARCHIVE_DIR}/${base}-${ts}.${ext}"
    mv "${file}" "${dest}"
    touch "${file}"
    echo "[trace-rotate] archived ${file##*/} (${size} bytes) → trace-archives/${base}-${ts}.${ext}"
  fi
}

rotate_if_large "${TRACE_DIR}/GRIMOIRE_TRACE.md"
rotate_if_large "${TRACE_DIR}/GRIMOIRE_TRACE.jsonl"
rotate_if_large "${TRACE_DIR}/GRIMOIRE_TRACE.legacy.txt"

# Ledgers de contexte bornes (audit "tout-indexer" — KNO-01/RUN-02,
# SPEC-ingenierie-contexte C4.2) : memes seuil et purge que la trace.
rotate_if_large "${TRACE_DIR}/hook-runtime/precompact/events.jsonl" "precompact"
rotate_if_large "${TRACE_DIR}/hook-runtime/subagent-stop/events.jsonl" "subagent-stop"
rotate_if_large "${ROOT_DIR}/_grimoire-runtime/_memory/activity.jsonl" "activity"

# Purge archives older than 30 days
find "${ARCHIVE_DIR}" -maxdepth 1 -type f -mtime +30 -delete 2>/dev/null || true
