#!/usr/bin/env python3
"""Glue I/O du handoff-packet à SubagentStop (C4.4, recâblé sur le kit).

La logique de dérivation (contrat ORC-03) vit désormais dans le produit :
``grimoire.tools.handoff`` (rapatriée de l'atelier vers grimoire-kit). Ce script
d'atelier n'est plus qu'une glue : il lit la capsule ``subagent-stop/latest.json``
et écrit le handoff produit par le kit. Source de vérité unique.

Best-effort : toute erreur (kit absent, JSON invalide) est silencieuse — un hook
ne doit jamais casser le cycle agent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from grimoire.tools.handoff import build_handoff, is_subagent_stop
except ImportError:
    # Kit indisponible (venv absent) : no-op silencieux.
    def build_handoff(capsule: dict[str, Any]) -> dict[str, Any]:  # type: ignore[misc]
        return {}

    def is_subagent_stop(capsule: dict[str, Any]) -> bool:  # type: ignore[misc]
        return False


def main() -> int:
    if len(sys.argv) < 4:
        return 0
    latest_path, out_latest, out_events = (Path(sys.argv[i]) for i in (1, 2, 3))
    try:
        capsule = json.loads(latest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0
    if not is_subagent_stop(capsule):
        return 0
    packet = build_handoff(capsule)
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
