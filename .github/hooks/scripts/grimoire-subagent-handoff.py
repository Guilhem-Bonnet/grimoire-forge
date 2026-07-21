#!/usr/bin/env python3
"""Produit un handoff-packet (ORC-03) à chaque SubagentStop (C4.4).

Le seul handoff runtime effectif était la trace subagent brute. Ce helper en
dérive un ``handoff-packet`` conforme au contrat du catalogue (ORC-03), de
façon **déterministe** : il lit la capsule ``subagent-stop/latest.json`` que le
hook de trace vient d'écrire et en produit un digest structuré, sans dépendre
d'un moteur LLM. ``context-summarizer.py`` réveillé pourra plus tard enrichir le
champ ``digest`` ; ici on garantit au moins un handoff au bon format.

Best-effort : toute erreur (fichier absent, JSON invalide) est silencieuse et
n'émet rien — un hook ne doit jamais casser le cycle agent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HANDOFF_SCHEMA_VERSION = "grimoire-handoff-packet/v1"
_PREVIEW_MAX = 600


def build_handoff(latest: dict[str, object]) -> dict[str, object]:
    """Dérive un handoff-packet ORC-03 d'une capsule subagent-stop."""
    failed = bool(latest.get("explicitFailure"))
    preview = str(latest.get("outputPreview") or "").strip()
    task = str(latest.get("task") or "").strip()
    digest = preview or (f"(pas d'aperçu de sortie) tâche : {task}" if task else "")
    return {
        "schemaVersion": HANDOFF_SCHEMA_VERSION,
        "contract": "handoff-packet",
        "pattern": "ORC-03",
        "from": {"agent": latest.get("agent") or "unknown", "role": "subagent"},
        "task": task,
        "taskType": latest.get("taskType") or "",
        "digest": digest[:_PREVIEW_MAX],
        "status": "failed" if failed else "ok",
        "producedAt": latest.get("timestamp") or "",
    }


def main() -> int:
    # Args : <latest.json> <handoff-latest.json> <handoff-events.jsonl>
    if len(sys.argv) < 4:
        return 0
    latest_path = Path(sys.argv[1])
    out_latest = Path(sys.argv[2])
    out_events = Path(sys.argv[3])
    try:
        latest = json.loads(latest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0
    if not isinstance(latest, dict) or latest.get("event") != "SubagentStop":
        return 0
    packet = build_handoff(latest)
    try:
        out_latest.parent.mkdir(parents=True, exist_ok=True)
        out_latest.write_text(
            json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        with out_events.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(packet, ensure_ascii=False) + "\n")
    except OSError:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
