#!/usr/bin/env python3
"""instructions-budget.py — mesure les lignes chargées au démarrage d'une session.

Lot F (B15) du plan durcissement-agentique-20260908 : « lignes chargées » =
lignes de `CLAUDE.md` plus celles de chaque import `@chemin` résolu
récursivement, jusqu'à 4 sauts — la même profondeur que Claude Code applique
à ses propres imports. Le script échoue (exit 1) si le total dépasse un
seuil (`--max`, défaut 200 lignes).

Usage :
    python3 scripts/instructions-budget.py                # rapport + seuil 200
    python3 scripts/instructions-budget.py --max 150       # seuil personnalisé
    python3 scripts/instructions-budget.py --root /autre/repo
    python3 scripts/instructions-budget.py --entry AGENTS.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

MAX_HOPS = 4
IMPORT_PATTERN = re.compile(r"^@(\S+)\s*$")


@dataclass
class LoadedFile:
    path: Path
    lines: int
    hop: int


def find_imports(text: str) -> list[str]:
    """Retourne les chemins des lignes `@chemin` (imports Claude Code)."""
    imports: list[str] = []
    for raw_line in text.splitlines():
        match = IMPORT_PATTERN.match(raw_line.strip())
        if match:
            imports.append(match.group(1))
    return imports


def count_lines(text: str) -> int:
    if not text:
        return 0
    # Une ligne finale sans retour chariot compte toujours comme une ligne ;
    # un fichier terminé par un retour chariot n'ajoute pas de ligne fantôme.
    return len(text.splitlines())


def resolve_imports(
    entry: Path,
    root: Path,
    max_hops: int = MAX_HOPS,
) -> tuple[list[LoadedFile], list[str]]:
    """Résout récursivement les imports `@chemin` depuis `entry`.

    Retourne la liste des fichiers chargés (dédupliqués par chemin résolu,
    dans l'ordre de première rencontre) et la liste des avertissements
    (import introuvable, ou profondeur maximale atteinte).
    """
    loaded: list[LoadedFile] = []
    seen: set[Path] = set()
    warnings: list[str] = []

    def visit(path: Path, hop: int) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        if not resolved.is_file():
            warnings.append(f"import introuvable : {path} (référencé à {hop} saut(s))")
            return
        seen.add(resolved)
        text = resolved.read_text(encoding="utf-8")
        loaded.append(LoadedFile(path=resolved, lines=count_lines(text), hop=hop))

        if hop >= max_hops:
            for target in find_imports(text):
                warnings.append(
                    f"import {target!r} depuis {resolved.relative_to(root) if _is_relative(resolved, root) else resolved} "
                    f"ignoré : profondeur maximale ({max_hops} sauts) atteinte"
                )
            return

        for target in find_imports(text):
            target_path = (resolved.parent / target).resolve()
            visit(target_path, hop + 1)

    visit(entry, 0)
    return loaded, warnings


def _is_relative(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _display(path: Path, root: Path) -> str:
    return str(path.relative_to(root)) if _is_relative(path, root) else str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="racine du dépôt (défaut : répertoire courant)")
    parser.add_argument("--entry", default="CLAUDE.md", help="fichier d'entrée, relatif à --root (défaut : CLAUDE.md)")
    parser.add_argument("--max", type=int, default=200, help="seuil de lignes chargées (défaut : 200)")
    parser.add_argument("--max-hops", type=int, default=MAX_HOPS, help=f"profondeur maximale d'import (défaut : {MAX_HOPS})")
    parser.add_argument("--quiet", action="store_true", help="n'imprimer que le total et le verdict")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    entry = root / args.entry
    if not entry.is_file():
        print(f"[ERREUR] fichier d'entrée introuvable : {entry}", file=sys.stderr)
        return 2

    loaded, warnings = resolve_imports(entry, root, max_hops=args.max_hops)
    total = sum(f.lines for f in loaded)

    if not args.quiet:
        print(f"Budget d'instructions — entrée {_display(entry, root)}")
        print(f"{'fichier':<70} {'sauts':>5} {'lignes':>7}")
        for item in loaded:
            print(f"{_display(item.path, root):<70} {item.hop:>5} {item.lines:>7}")
        print("-" * 84)
        for warning in warnings:
            print(f"[AVERTISSEMENT] {warning}", file=sys.stderr)

    verdict = "OK" if total <= args.max else "DEPASSEMENT"
    print(f"Total lignes chargées : {total} / seuil {args.max} — {verdict}")

    return 0 if total <= args.max else 1


if __name__ == "__main__":
    raise SystemExit(main())
