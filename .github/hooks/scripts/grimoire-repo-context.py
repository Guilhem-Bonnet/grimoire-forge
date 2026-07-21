#!/usr/bin/env python3
"""Matérialise un context-pack durable par repo (C4.3).

Le répertoire ``repo-contexts/`` prévu pour le contexte de repo persistant était
vide. Ce script y écrit un ``context-pack`` **conforme au contrat du catalogue**
(champs lus dans ``grimoire-kit/web/data/catalogue-export.json`` — le contrat
n'est pas défini ici, seulement honoré) : une source réutilisable et durable
pour l'intake, sous l'ordre d'autorité ORC-06 (source active > preuve vérifiée >
mémoire durable > similarité).

Déterministe et sans effet de bord hors du fichier produit. Wiré en task VS Code
(``grimoire: repo-context``), pas en hook — c'est de l'hygiène ponctuelle.

Usage : ``grimoire-repo-context.py [--root <repo>] [--out <dir>] [--ttl-days N]``
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

CONTEXT_PACK_SCHEMA_VERSION = "grimoire-context-pack/v1"

# Sources candidates par ordre d'autorité ORC-06 décroissant (source active de
# gouvernance d'abord, puis structure, puis preuve). (chemin relatif, raison).
_CANDIDATES: tuple[tuple[str, str], ...] = (
    ("CLAUDE.md", "Instructions actives de gouvernance du repo"),
    ("AGENTS.md", "Contrat d'agents actif"),
    (".github/copilot-instructions.md", "Instructions actives de l'atelier"),
    ("README.md", "Description de référence du repo"),
    ("pyproject.toml", "Manifeste de build / dépendances"),
    ("CHANGELOG.md", "Historique vérifié des changements"),
)


def _git_head(root: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5, check=True,
        )
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def _confidence(rel: str) -> str:
    # Gouvernance active = haute confiance ; README/manifeste = moyenne.
    return "high" if rel in {"CLAUDE.md", "AGENTS.md",
                             ".github/copilot-instructions.md"} else "medium"


def build_context_pack(root: Path, now: datetime, ttl_days: int) -> dict[str, object]:
    included: list[dict[str, object]] = []
    excluded: list[dict[str, object]] = []
    for rel, reason in _CANDIDATES:
        path = root / rel
        if path.is_file():
            raw = path.read_bytes()
            included.append({
                "path": rel,
                "status": "included",
                "reason": reason,
                "confidence": _confidence(rel),
                "sha256": hashlib.sha256(raw).hexdigest()[:16],
                "lines": len(raw.splitlines()),
            })
        else:
            excluded.append({
                "path": rel,
                "status": "absent",
                "reason": "non présent dans le repo",
            })
    head = _git_head(root)
    sufficiency = "sufficient" if any(
        s["path"] in {"CLAUDE.md", "AGENTS.md", "README.md"} for s in included
    ) else "partial"
    return {
        "schemaVersion": CONTEXT_PACK_SCHEMA_VERSION,
        "contract": "context-pack",
        "mission_id": f"repo-context:{root.name}",
        "context_profile": "repo-durable",
        "budget": "medium",
        "objective": (
            "Contexte durable et réutilisable du repo pour l'intake, sous "
            "l'ordre d'autorité ORC-06."
        ),
        "included_sources": included,
        "excluded_sources": excluded,
        "constraints": [
            "Vérité : les sources incluses priment sur la mémoire ou la similarité (ORC-06).",
            "Fraîcheur : invalider si HEAD change ou après expiry.",
        ],
        "scorecard": {
            "sufficiency": sufficiency,
            "provenance": "repo-local",
            "freshness": head or "unknown",
            "included": len(included),
            "excluded": len(excluded),
        },
        "open_questions": [] if sufficiency == "sufficient" else [
            "Aucune source de gouvernance active (CLAUDE.md/AGENTS.md) trouvée.",
        ],
        "expiry": {
            "generatedAt": now.isoformat(),
            "ttlDays": ttl_days,
            "expiresAt": (now + timedelta(days=ttl_days)).isoformat(),
            "invalidateOn": "git HEAD change",
            "head": head,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="")
    parser.add_argument("--ttl-days", type=int, default=30)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out_dir = Path(args.out) if args.out else (
        root / "_grimoire-runtime-output" / "repo-contexts"
    )
    now = datetime.now(timezone.utc).replace(microsecond=0)
    pack = build_context_pack(root, now, args.ttl_days)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{root.name}.context-pack.json"
    out_file.write_text(
        json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    scorecard = pack["scorecard"]
    assert isinstance(scorecard, dict)
    print(
        f"[repo-context] {out_file} — {scorecard['included']} sources incluses, "
        f"suffisance : {scorecard['sufficiency']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
