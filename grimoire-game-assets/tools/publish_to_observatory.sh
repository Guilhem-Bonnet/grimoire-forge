#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${ROOT_DIR}/.." && pwd)"
CURATED_DIR="${CURATED_DIR:-${ROOT_DIR}/10-curated}"
TARGET_DIR="${TARGET_DIR:-${REPO_ROOT}/_grimoire-output/assets}"
INDEX_FILE="${INDEX_FILE:-${ROOT_DIR}/manifests/assets-index.csv}"
SOURCES_FILE="${SOURCES_FILE:-${ROOT_DIR}/manifests/sources.yaml}"
ATTRIBUTION_FILE="${ATTRIBUTION_FILE:-${ROOT_DIR}/manifests/attribution.md}"
DRY_RUN="${DRY_RUN:-0}"

echo "[assets] source: ${CURATED_DIR}"
echo "[assets] target: ${TARGET_DIR}"
echo "[assets] index: ${INDEX_FILE}"
echo "[assets] sources: ${SOURCES_FILE}"
echo "[assets] attribution: ${ATTRIBUTION_FILE}"

if [[ ! -f "${INDEX_FILE}" ]]; then
  echo "[assets] error: missing index file ${INDEX_FILE}" >&2
  exit 1
fi

if [[ ! -f "${SOURCES_FILE}" ]]; then
  echo "[assets] error: missing sources file ${SOURCES_FILE}" >&2
  exit 1
fi

if [[ ! -f "${ATTRIBUTION_FILE}" ]]; then
  echo "[assets] error: missing attribution file ${ATTRIBUTION_FILE}" >&2
  exit 1
fi

if [[ ! -d "${CURATED_DIR}" ]]; then
  echo "[assets] error: missing curated directory ${CURATED_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

python3 - "${INDEX_FILE}" "${SOURCES_FILE}" "${ATTRIBUTION_FILE}" "${CURATED_DIR}" "${TARGET_DIR}" "${DRY_RUN}" <<'PY'
import csv
import re
import shutil
import sys
from pathlib import Path, PurePosixPath


def normalize_bool(value: str) -> str:
  return value.strip().lower()


def unquote(value: str) -> str:
  value = value.strip()
  if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
    return value[1:-1]
  return value


def parse_sources_yaml(path: Path) -> dict[str, dict[str, str]]:
  sources: dict[str, dict[str, str]] = {}
  current_source_id: str | None = None

  for raw_line in path.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#"):
      continue

    item_match = re.match(r"^-\s+id:\s*(.+)$", line)
    if item_match:
      current_source_id = unquote(item_match.group(1))
      sources[current_source_id] = {}
      continue

    if current_source_id is None:
      continue

    status_match = re.match(r"^status:\s*(.+)$", line)
    if status_match:
      sources[current_source_id]["status"] = unquote(status_match.group(1))
      continue

    license_match = re.match(r"^license:\s*(.+)$", line)
    if license_match:
      sources[current_source_id]["license"] = unquote(license_match.group(1))

  return sources


def parse_attribution_ids(path: Path) -> set[str]:
  ids: set[str] = set()
  for raw_line in path.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if not line.startswith("|"):
      continue

    cells = [cell.strip() for cell in line.strip("|").split("|")]
    if not cells:
      continue

    first = cells[0]
    if first in {"", "asset_or_pack", "---"}:
      continue

    ids.add(first)

  return ids


def is_safe_relative_path(path_value: str) -> bool:
  path_obj = PurePosixPath(path_value)
  return (not path_obj.is_absolute()) and (".." not in path_obj.parts)


index_file = Path(sys.argv[1])
sources_file = Path(sys.argv[2])
attribution_file = Path(sys.argv[3])
curated_dir = Path(sys.argv[4]).resolve()
target_dir = Path(sys.argv[5]).resolve()
dry_run = normalize_bool(sys.argv[6]) in {"1", "true", "yes", "on"}

allowed_statuses = {"approved", "approved-with-attribution"}
sources = parse_sources_yaml(sources_file)
attribution_ids = parse_attribution_ids(attribution_file)

required_columns = {
  "asset_id",
  "source_id",
  "license",
  "relative_path",
  "validated",
}

indexed_rows = 0
validated_rows = 0
publishable_paths: set[str] = set()
errors: list[str] = []

with index_file.open("r", encoding="utf-8", newline="") as handle:
  reader = csv.DictReader(handle)
  if not reader.fieldnames:
    errors.append(f"[assets] error: empty or invalid CSV header in {index_file}")
  else:
    missing_columns = required_columns.difference(reader.fieldnames)
    if missing_columns:
      missing = ", ".join(sorted(missing_columns))
      errors.append(f"[assets] error: missing required CSV columns: {missing}")

  for line_number, row in enumerate(reader, start=2):
    asset_id = (row.get("asset_id") or "").strip()
    if not asset_id:
      continue

    indexed_rows += 1

    validated = normalize_bool(row.get("validated") or "")
    if validated != "true":
      continue
    validated_rows += 1

    source_id = (row.get("source_id") or "").strip()
    row_license = (row.get("license") or "").strip()
    relative_path = (row.get("relative_path") or "").strip()

    if not source_id:
      errors.append(f"[assets] line {line_number}: missing source_id for asset {asset_id}")
      continue

    source_meta = sources.get(source_id)
    if source_meta is None:
      errors.append(
        f"[assets] line {line_number}: source_id '{source_id}' not found in {sources_file}"
      )
      continue

    source_status = source_meta.get("status", "")
    if source_status not in allowed_statuses:
      errors.append(
        f"[assets] line {line_number}: source_id '{source_id}' has disallowed status '{source_status}'"
      )

    source_license = source_meta.get("license", "")
    if source_license and row_license and source_license != row_license:
      errors.append(
        f"[assets] line {line_number}: license mismatch for source_id '{source_id}' "
        f"(index='{row_license}', sources='{source_license}')"
      )

    if source_status == "approved-with-attribution" and source_id not in attribution_ids:
      errors.append(
        f"[assets] line {line_number}: source_id '{source_id}' requires attribution but is missing in {attribution_file}"
      )

    if not relative_path.startswith("10-curated/"):
      errors.append(
        f"[assets] line {line_number}: invalid relative_path '{relative_path}' (must start with 10-curated/)"
      )
      continue

    rel_path = relative_path[len("10-curated/") :]
    if not rel_path or not is_safe_relative_path(rel_path):
      errors.append(
        f"[assets] line {line_number}: unsafe relative_path '{relative_path}'"
      )
      continue

    src_file = (curated_dir / rel_path).resolve()
    try:
      src_file.relative_to(curated_dir)
    except ValueError:
      errors.append(
        f"[assets] line {line_number}: path escapes curated directory: '{relative_path}'"
      )
      continue

    if not src_file.is_file():
      errors.append(
        f"[assets] line {line_number}: missing indexed asset file '{relative_path}'"
      )
      continue

    publishable_paths.add(PurePosixPath(rel_path).as_posix())

if errors:
  for error in errors:
    print(error, file=sys.stderr)
  print("[assets] publish aborted (fail-closed)", file=sys.stderr)
  sys.exit(1)

if not publishable_paths:
  print(f"[assets] error: no validated assets found in {index_file}", file=sys.stderr)
  sys.exit(1)

print(f"[assets] indexed rows: {indexed_rows}")
print(f"[assets] validated rows: {validated_rows}")
print(f"[assets] publishable rows: {len(publishable_paths)}")
if dry_run:
  print("[assets] dry-run mode enabled")

published_rows = 0
for rel_path in sorted(publishable_paths):
  src_file = curated_dir / rel_path
  dst_file = target_dir / rel_path

  if dry_run:
    print(f"[assets] dry-run publish: {rel_path}")
    continue

  dst_file.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(src_file, dst_file)
  published_rows += 1
  print(f"[assets] published: {rel_path}")

if not dry_run:
  print(f"[assets] published files: {published_rows}")

print("[assets] publish completed (manifest-governed, fail-closed)")
PY
