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
  local ext="${file##*.}"
  [[ -f "${file}" ]] || return 0
  local size
  size=$(stat -c%s "${file}" 2>/dev/null || echo 0)
  if (( size >= MAX_BYTES )); then
    local ts
    ts=$(date +%Y%m%d-%H%M%S)
    local base
    base=$(basename "${file}" ".${ext}")
    local dest="${ARCHIVE_DIR}/${base}-${ts}.${ext}"
    mv "${file}" "${dest}"
    touch "${file}"
    echo "[trace-rotate] archived ${file##*/} (${size} bytes) → trace-archives/${base}-${ts}.${ext}"
  fi
}

rotate_if_large "${TRACE_DIR}/GRIMOIRE_TRACE.md"
rotate_if_large "${TRACE_DIR}/GRIMOIRE_TRACE.jsonl"
rotate_if_large "${TRACE_DIR}/GRIMOIRE_TRACE.legacy.txt"

# Ledgers de hooks append-only (C4.2 — bornage effectif). Ces flux
# (`hook-runtime/**/events.jsonl`, `task-flow/events.jsonl`) grandissaient sans
# borne — exactement le constat « tout-indexer » de l'audit. Même seuil, mais
# archivés à plat sous trace-archives/ledgers/ avec un préfixe préservant
# l'origine (plusieurs fichiers `events.jsonl` cohabitent).
LEDGER_ARCHIVE_DIR="${ARCHIVE_DIR}/ledgers"
mkdir -p "${LEDGER_ARCHIVE_DIR}"

rotate_ledger() {
  local file="$1"
  local label="$2"
  [[ -f "${file}" ]] || return 0
  local size
  size=$(stat -c%s "${file}" 2>/dev/null || echo 0)
  if (( size >= MAX_BYTES )); then
    local ts
    ts=$(date +%Y%m%d-%H%M%S)
    mv "${file}" "${LEDGER_ARCHIVE_DIR}/${label}-${ts}.jsonl"
    touch "${file}"
    echo "[trace-rotate] archived ledger ${label} (${size} bytes) → trace-archives/ledgers/${label}-${ts}.jsonl"
  fi
}

HR="${TRACE_DIR}/hook-runtime"
rotate_ledger "${HR}/precompact/events.jsonl" "precompact-events"
rotate_ledger "${HR}/subagent-stop/events.jsonl" "subagent-stop-events"
rotate_ledger "${HR}/safety-gate/events.jsonl" "safety-gate-events"
rotate_ledger "${HR}/events-errors.jsonl" "events-errors"
rotate_ledger "${HR}/user-prompts.jsonl" "user-prompts"
rotate_ledger "${TRACE_DIR}/task-flow/events.jsonl" "task-flow-events"

# Purge archives older than 30 days (traces + ledgers, récursif).
find "${ARCHIVE_DIR}" -type f -mtime +30 -delete 2>/dev/null || true
