#!/usr/bin/env python3
"""Revert accent corruption inside import/export specifier paths.

The previous accent-fix ran on all string literals including ESM import
paths. This script undoes the accent changes ONLY inside quoted paths
appearing on import/export/require/dynamic-import lines.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path("/mnt/Travail/Projets/Dev/Grimoire-Forge/grimoire-kit/apps/grimoire-game")
TARGETS = [ROOT / "src", ROOT / "app"]

# Accented -> ASCII. Applied only inside path quotes.
REVERT = {
    "vérification": "verification",
    "décision": "decision",
    "séance": "seance",
    "entrée": "entree",
    "exécution": "execution",
    "évé": "eve",
    "référence": "reference",
    "exécut": "execut",
    "détect": "detect",
    "sécurité": "securite",
    "bloqué": "bloque",
    "bloquée": "bloquee",
    "préparé": "prepare",
    "préparée": "preparee",
    "opérateur": "operateur",
    "récent": "recent",
    "récente": "recente",
    "théâtre": "theatre",
    "chaîne": "chaine",
    "aligné": "aligne",
    "alignée": "alignee",
    "même": "meme",
    "Séance": "Seance",
    "Décision": "Decision",
    "Vérification": "Verification",
    "Exécution": "Execution",
    "Reférence": "Reference",
    "Référence": "Reference",
    "Révéler": "Reveler",
    "révéler": "reveler",
    "clôture": "cloture",
    "dérive": "derive",
    "émis": "emis",
    "été": "ete",
    "déclaré": "declare",
    "déclarée": "declaree",
    "rejeté": "rejete",
    "rejetée": "rejetee",
    "événement": "evenement",
    "événements": "evenements",
    "synchronisé": "synchronise",
    "synchronisée": "synchronisee",
    "tâche": "tache",
    "tâches": "taches",
    "prête": "prete",
    "Nœud": "Noeud",
    "nœud": "noeud",
    "nœuds": "noeuds",
    "œil": "oeil",
    "œuvre": "oeuvre",
    "capacité": "capacite",
    "causalité": "causalite",
    "spécialisée": "specialisee",
    "scénario": "scenario",
    "système": "systeme",
    "Système": "Systeme",
    "verifié": "verifie",
    "vérifié": "verifie",
    "vérifiée": "verifiee",
    "vérifier": "verifier",
    "dédié": "dedie",
    "dédiée": "dediee",
    "attaché": "attache",
    "attachée": "attachee",
    "auditée": "auditee",
    "observée": "observee",
    "borné": "borne",
    "bornée": "bornee",
    "relié": "relie",
    "reliée": "reliee",
    "donnée": "donnee",
    "données": "donnees",
    "archivée": "archivee",
    "activée": "activee",
    "Bloqués": "Bloques",
    "lisibilité": "lisibilite",
    "opératoire": "operatoire",
}

# Pattern to capture paths in import/export/require/dynamic-import.
PATH_RE = re.compile(
    r"""
    (?:
      (?:import|export)\s+(?:type\s+)?
      (?:[^'"`;]+?\s+from\s+)?
      (['"`])(?P<p1>(?:\\.|(?!\1).)*)\1
    |
      require\(\s*(['"`])(?P<p2>(?:\\.|(?!\3).)*)\3\s*\)
    |
      import\(\s*(['"`])(?P<p3>(?:\\.|(?!\5).)*)\5\s*\)
    )
    """,
    re.VERBOSE,
)


def revert_path(s: str) -> str:
    for k, v in REVERT.items():
        s = s.replace(k, v)
    return s


def process_line(line: str) -> str:
    def sub(m: re.Match[str]) -> str:
        full = m.group(0)
        # Figure out which named group has the path
        for name in ("p1", "p2", "p3"):
            p = m.group(name)
            if p is not None:
                new = revert_path(p)
                if new != p:
                    return full.replace(p, new, 1)
                return full
        return full
    return PATH_RE.sub(sub, line)


def process(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    # Apply per-line for simplicity and safety.
    new_lines: list[str] = []
    changed = False
    for line in text.splitlines(keepends=True):
        new_line = process_line(line)
        if new_line != line:
            changed = True
        new_lines.append(new_line)
    if changed:
        path.write_text("".join(new_lines), encoding="utf-8")
        return 1
    return 0


def main() -> int:
    changed = 0
    scanned = 0
    for base in TARGETS:
        for p in base.rglob("*.ts"):
            if p.name.endswith(".d.ts"):
                continue
            if any(seg in {"dist", ".release", "node_modules"} for seg in p.parts):
                continue
            scanned += 1
            changed += process(p)
    print(f"scanned={scanned} changed={changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
