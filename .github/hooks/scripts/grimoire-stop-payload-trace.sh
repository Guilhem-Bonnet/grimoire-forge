#!/usr/bin/env bash
# grimoire-stop-payload-trace.sh — trace TEMPORAIRE (Grimoire-kit#627) : quelles
# clés le hook Stop de Copilot reçoit-il sur stdin ? Écrit les NOMS de clés et
# la présence d'un transcript_path, jamais le contenu. À retirer une fois le
# fait établi.
set -euo pipefail
project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
out="$project_root/_grimoire-output/traces/stop-payload-keys.jsonl"
mkdir -p "$(dirname "$out")"
payload="$(cat || true)"
python3 -c '
import datetime, json, sys
try:
    d = json.loads(sys.argv[2] or "{}")
except Exception:
    d = {"_unparsed": True}
line = {"at": datetime.datetime.now().isoformat(timespec="seconds"), "keys": sorted(d) if isinstance(d, dict) else [], "has_transcript_path": bool(isinstance(d, dict) and d.get("transcript_path"))}
with open(sys.argv[1], "a", encoding="utf-8") as f:
    f.write(json.dumps(line) + "\n")
' "$out" "$payload" || true
echo '{"continue": true}'
