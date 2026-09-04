#!/usr/bin/env bash
# grimoire-inject-context.sh — SessionStart hook
# Injecte un contexte Grimoire court via additionalContext et en garde
# une capsule dans _grimoire-runtime-output/hook-runtime/.

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
config_file="$project_root/_grimoire-runtime/core/config.yaml"
shared_context_file="$project_root/_grimoire-runtime/_memory/shared-context.md"
latest_file="$project_root/_grimoire-runtime-output/hook-runtime/session-start-latest.json"
policy_script="$project_root/.github/hooks/lib/guardrail-policy.py"
policy_python="$project_root/.venv/bin/python"

if [[ ! -x "$policy_python" ]]; then
  policy_python="$(command -v python3 || true)"
fi

if [[ -z "$policy_python" || ! -f "$policy_script" ]]; then
  echo "{}"
  exit 0
fi

if ! output=$(printf '{}' | "$policy_python" "$policy_script" session-start --config-file "$config_file" --shared-context-file "$shared_context_file" --latest-file "$latest_file" 2>/dev/null); then
  echo "{}"
  exit 0
fi

# V1 ledger: scope=session, phase=start.
emit_event_script="$project_root/.github/hooks/scripts/grimoire-emit-event.sh"
if [[ -x "$emit_event_script" ]]; then
  "$emit_event_script" --scope session --phase start --source-hook "grimoire-inject-context.sh" --payload-json '{"hook":"session-start"}' 2>/dev/null || true
fi

printf '%s\n' "$output"
