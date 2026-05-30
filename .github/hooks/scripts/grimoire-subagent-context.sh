#!/usr/bin/env bash
# grimoire-subagent-context.sh — SubagentStart hook (V2 compresse)
# Capsule minimale : session ID + objectif tronque + 3 contraintes critiques.
# Le contexte statique (regles, routing, persona) est dans grimoire-master.md.
set -euo pipefail

root="$(cd "$(dirname "$0")/../../.." && pwd)"
state="$root/_grimoire-runtime-output/hook-runtime/user-prompt-latest.json"

sid=""; obj=""
if [[ -f "$state" ]] && command -v jq &>/dev/null; then
  sid=$(jq -r '.sessionId // ""' "$state" 2>/dev/null || true)
  obj=$(jq -r '.promptPreview // ""' "$state" 2>/dev/null | cut -c1-80 || true)
fi

ctx="RULES:no-hallucination,evidence-before-close,fr${sid:+|SID:$sid}${obj:+|OBJ:$obj}"
ctx="${ctx:0:200}"
jq -n --arg c "$ctx" '{"additionalContext":$c}'

emit="$root/.github/hooks/scripts/grimoire-emit-event.sh"
[[ -x "$emit" ]] && "$emit" --scope subagent --phase info \
  --source-hook "grimoire-subagent-context.sh" \
  --payload-json '{"hook":"subagent-context","v":2}' 2>/dev/null || true
