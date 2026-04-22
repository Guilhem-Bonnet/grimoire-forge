#!/usr/bin/env bash
# grimoire-prompt-submit.sh — UserPromptSubmit hook
# Audite le prompt utilisateur, journalise un etat minimal et injecte des
# references/capsules de contexte sur les sujets hooks/task-flow.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
hook_state_dir="$project_root/_grimoire-runtime-output/hook-runtime"
latest_file="$hook_state_dir/user-prompt-latest.json"
events_file="$hook_state_dir/user-prompts.jsonl"
policy_script="$project_root/grimoire-kit/framework/tools/guardrail-policy.py"
accelerator_script="$project_root/grimoire-kit/framework/tools/compiled-flow.py"
policy_python="$project_root/grimoire-kit/.venv/bin/python"
input=$(cat)

mkdir -p "$hook_state_dir"

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -z "$policy_python" || ! -f "$policy_script" ]]; then
  echo "{}"
  exit 0
fi

merge_additional_context() {
  local raw_output="$1"
  local extra_context="$2"

  printf '%s' "$raw_output" | "$policy_python" - "$extra_context" <<'PY'
import json
import sys

ctx = sys.argv[1]
raw = sys.stdin.read().strip()

if not raw:
    payload = {}
else:
    try:
        payload = json.loads(raw)
    except Exception:
        payload = {}

hook_output = payload.get("hookSpecificOutput")
if not isinstance(hook_output, dict):
    hook_output = {}

existing = str(hook_output.get("additionalContext") or "").strip()
if existing:
    merged = f"{existing} | {ctx}"
else:
    merged = ctx

hook_output["additionalContext"] = merged[:1400]
payload["hookSpecificOutput"] = hook_output

print(json.dumps(payload, ensure_ascii=True))
PY
}

if ! output=$(printf '%s' "$input" | "$policy_python" "$policy_script" prompt-signals --project-root "$project_root" --latest-file "$latest_file" --events-file "$events_file" 2>/dev/null); then
  echo "{}"
  exit 0
fi

if [[ -f "$accelerator_script" ]]; then
  if compiled_context=$(printf '%s' "$input" | "$policy_python" "$accelerator_script" --project-root "$project_root" hook-context 2>/dev/null); then
    if [[ -n "${compiled_context:-}" ]]; then
      output=$(merge_additional_context "$output" "$compiled_context")
    fi
  fi
fi

# Inject a visual pre-brief context when the prompt indicates visual creation work.
if [[ -f "$latest_file" ]]; then
  if visual_context=$(printf '%s' "$input" | "$policy_python" - "$latest_file" <<'PY'
import json
import re
import sys

latest_file = sys.argv[1]
raw = sys.stdin.read()

prompt_chunks = []

try:
  payload = json.loads(raw)
except Exception:
  payload = {}

if isinstance(payload, dict):
  for key in ("prompt", "text", "message", "promptPreview"):
    value = payload.get(key)
    if isinstance(value, str) and value.strip():
      prompt_chunks.append(value.strip())

try:
  with open(latest_file, "r", encoding="utf-8") as handle:
    latest_payload = json.load(handle)
except Exception:
  latest_payload = {}

if isinstance(latest_payload, dict):
  preview = latest_payload.get("promptPreview")
  if isinstance(preview, str) and preview.strip():
    prompt_chunks.append(preview.strip())

full_prompt = " ".join(prompt_chunks).lower()

keywords = [
  "visuel",
  "ui",
  "ux",
  "graphique",
  "animation",
  "logo",
  "brand",
  "charte",
  "assets",
  "sprite",
  "pixel",
  "png",
  "jpeg",
  "jpg",
  "svg",
  "gif",
  "css",
  "motion",
  "illustration",
  "front",
]

if not any(token in full_prompt for token in keywords):
  print("")
  raise SystemExit(0)

context = (
  "VISUAL_PREBRIEF_REQUIRED: ask one mandatory batch before heavy generation. "
  "Batch must cover intent, audience, style mood, anti-goals, priority information, "
  "interaction model, motion role, asset list, output formats, and technical constraints. "
  "If user is non-designer, reformulate in plain language with options. "
  "After batch, produce canonical visual brief and then execute."
)

print(context)
PY
  ); then
  if [[ -n "${visual_context:-}" ]]; then
    output=$(merge_additional_context "$output" "$visual_context")
  fi
  fi
fi

if transcript_guard_output=$(GRIMOIRE_PROMPT_INPUT="$input" "$policy_python" - "$project_root" <<'PY'
import json
import os
import sys
from pathlib import Path

project_root = Path(sys.argv[1]).resolve()
raw = os.environ.get("GRIMOIRE_PROMPT_INPUT", "")

try:
  payload = json.loads(raw)
except Exception:
  payload = {}

prompt_chunks = []
if isinstance(payload, dict):
  for key in ("prompt", "text", "message", "promptPreview"):
    value = payload.get(key)
    if isinstance(value, str) and value.strip():
      prompt_chunks.append(value.strip())

prompt_text = " ".join(prompt_chunks).lower()
if any(token in prompt_text for token in ("/compact", "compact conversation", "compacte la conversation")):
  print("{}")
  raise SystemExit(0)

config_home = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))
workspace_storage = config_home / "Code" / "User" / "workspaceStorage"
if not workspace_storage.exists():
  print("{}")
  raise SystemExit(0)

target_uri = project_root.as_uri().rstrip("/")
latest_transcript = None
latest_mtime = -1.0
latest_size = 0
session_resources_dir = None
session_resource_size = 0

for workspace_file in workspace_storage.glob("*/workspace.json"):
  try:
    workspace_payload = json.loads(workspace_file.read_text(encoding="utf-8"))
  except Exception:
    continue
  folder = str(workspace_payload.get("folder") or "").rstrip("/")
  if folder != target_uri:
    continue

  transcripts_dir = workspace_file.parent / "GitHub.copilot-chat" / "transcripts"
  if not transcripts_dir.is_dir():
    continue

  for transcript_path in transcripts_dir.glob("*.jsonl"):
    try:
      stat = transcript_path.stat()
    except OSError:
      continue
    if stat.st_mtime > latest_mtime:
      latest_transcript = transcript_path
      latest_mtime = stat.st_mtime
      latest_size = stat.st_size
      candidate_resources_dir = workspace_file.parent / "GitHub.copilot-chat" / "chat-session-resources" / transcript_path.stem
      session_resources_dir = candidate_resources_dir

if session_resources_dir is not None and session_resources_dir.is_dir():
  try:
    session_resource_size = sum(
      entry.stat().st_size
      for entry in session_resources_dir.rglob("*")
      if entry.is_file()
    )
  except OSError:
    session_resource_size = 0

if latest_transcript is None:
  print("{}")
  raise SystemExit(0)

size_mib = latest_size / (1024 * 1024)

def env_bytes(name: str, default: int) -> int:
  raw = os.environ.get(name)
  if not raw:
    return default
  try:
    value = int(raw)
  except ValueError:
    return default
  return max(1, value)

MIB = 1024 * 1024
transcript_warning_bytes = env_bytes("GRIMOIRE_COPILOT_TRANSCRIPT_WARNING_BYTES", 2 * MIB)
transcript_block_bytes = env_bytes("GRIMOIRE_COPILOT_TRANSCRIPT_BLOCK_BYTES", 4 * MIB)
combined_warning_bytes = env_bytes("GRIMOIRE_COPILOT_COMBINED_WARNING_BYTES", 3 * MIB)
combined_block_bytes = env_bytes("GRIMOIRE_COPILOT_COMBINED_BLOCK_BYTES", 5 * MIB)

transcript_block_bytes = max(transcript_block_bytes, transcript_warning_bytes + 1)
combined_block_bytes = max(combined_block_bytes, combined_warning_bytes + 1)

combined_size = latest_size + session_resource_size
combined_size_mib = combined_size / (1024 * 1024)

if combined_size >= combined_block_bytes:
  reason = (
    f"Cette session Copilot est devenue trop lourde ({combined_size_mib:.1f} MiB au total entre transcript et sorties d'outils) "
    "et risque fortement de provoquer un 413. Lance /compact dans ce chat, puis renvoie ton message. "
    "Si le probleme persiste, ouvre une nouvelle session Chat ou evite les commandes qui renvoient de gros diffs."
  )
  payload = {
    "decision": "block",
    "reason": reason,
    "hookSpecificOutput": {
      "hookEventName": "UserPromptSubmit",
      "additionalContext": (
        f"Session active {latest_transcript.stem}: transcript {size_mib:.1f} MiB + artefacts outils {session_resource_size / (1024 * 1024):.1f} MiB; "
        "compaction requise avant nouvel envoi."
      ),
    },
  }
  print(json.dumps(payload, ensure_ascii=True))
  raise SystemExit(0)

if latest_size >= transcript_block_bytes:
  reason = (
    f"Cette session Copilot est devenue trop volumineuse ({size_mib:.1f} MiB de transcript) "
    "et risque de provoquer un 413. Lance /compact dans ce chat, puis renvoie ton message. "
    "Si le probleme persiste, ouvre une nouvelle session Chat."
  )
  payload = {
    "decision": "block",
    "reason": reason,
    "hookSpecificOutput": {
      "hookEventName": "UserPromptSubmit",
      "additionalContext": (
        f"Transcript actif {latest_transcript.name} a {size_mib:.1f} MiB; "
        "compaction requise avant nouvel envoi."
      ),
    },
  }
  print(json.dumps(payload, ensure_ascii=True))
  raise SystemExit(0)

if combined_size >= combined_warning_bytes:
  payload = {
    "hookSpecificOutput": {
      "hookEventName": "UserPromptSubmit",
      "additionalContext": (
        f"Session Copilot chargee ({combined_size_mib:.1f} MiB total, dont {session_resource_size / (1024 * 1024):.1f} MiB de sorties d'outils). "
        "Eviter les gros diffs/outils verbeux et demander /compact en fin de tour."
      ),
    }
  }
  print(json.dumps(payload, ensure_ascii=True))
  raise SystemExit(0)

if latest_size >= transcript_warning_bytes:
  payload = {
    "hookSpecificOutput": {
      "hookEventName": "UserPromptSubmit",
      "additionalContext": (
        f"Session Copilot volumineuse ({size_mib:.1f} MiB). Garder la reponse tres compacte "
        "et demander /compact en fin de tour si l'objectif est atteint."
      ),
    }
  }
  print(json.dumps(payload, ensure_ascii=True))
  raise SystemExit(0)

print("{}")
PY
); then
  if [[ -n "${transcript_guard_output:-}" && "$transcript_guard_output" != "{}" ]]; then
    output=$(GRIMOIRE_BASE_OUTPUT="$output" GRIMOIRE_GUARD_OUTPUT="$transcript_guard_output" "$policy_python" - <<'PY'
import json
import os

incoming_raw = os.environ.get("GRIMOIRE_GUARD_OUTPUT", "")
base_raw = os.environ.get("GRIMOIRE_BASE_OUTPUT", "").strip()

def load(raw: str):
  if not raw:
    return {}
  try:
    return json.loads(raw)
  except Exception:
    return {}

base = load(base_raw)
incoming = load(incoming_raw)

base_hook = base.get("hookSpecificOutput") if isinstance(base.get("hookSpecificOutput"), dict) else {}
incoming_hook = incoming.get("hookSpecificOutput") if isinstance(incoming.get("hookSpecificOutput"), dict) else {}

contexts = [
  str(base_hook.get("additionalContext") or "").strip(),
  str(incoming_hook.get("additionalContext") or "").strip(),
]
merged_context = " | ".join(part for part in contexts if part)[:1400]

if incoming.get("decision") == "block":
  payload = {
    "decision": "block",
    "reason": str(incoming.get("reason") or base.get("reason") or "Request blocked by transcript guard."),
    "hookSpecificOutput": {
      "hookEventName": "UserPromptSubmit",
    },
  }
  if merged_context:
    payload["hookSpecificOutput"]["additionalContext"] = merged_context
  print(json.dumps(payload, ensure_ascii=True))
  raise SystemExit(0)

if not base and incoming:
  if merged_context:
    incoming_hook = incoming.get("hookSpecificOutput") if isinstance(incoming.get("hookSpecificOutput"), dict) else {}
    incoming_hook["additionalContext"] = merged_context
    incoming_hook.setdefault("hookEventName", "UserPromptSubmit")
    incoming["hookSpecificOutput"] = incoming_hook
  print(json.dumps(incoming, ensure_ascii=True))
  raise SystemExit(0)

if merged_context:
  base_hook["additionalContext"] = merged_context
  base_hook.setdefault("hookEventName", "UserPromptSubmit")
  base["hookSpecificOutput"] = base_hook

print(json.dumps(base, ensure_ascii=True))
PY
)
  fi
fi

# V1 ledger: scope=prompt, phase=info.
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  "$emit_event_script" --scope prompt --phase info --source-hook "grimoire-prompt-submit.sh" --payload-json '{"hook":"prompt-submit"}' 2>/dev/null || true
fi

printf '%s\n' "$output"