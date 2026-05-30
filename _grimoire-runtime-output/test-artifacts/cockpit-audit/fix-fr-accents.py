#!/usr/bin/env python3
"""One-shot fixer: add missing French accents inside TS string literals.

Scope: grimoire-kit/apps/grimoire-game/{src,app}/**/*.ts (excluding .d.ts, dist, .release).
Only rewrites content inside '...', "...", and `...` literals.
Uses a conservative word-boundary map of pure-French words (no clash with
English keywords or identifiers).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "grimoire-kit/apps/grimoire-game"
TARGETS = [ROOT / "src", ROOT / "app"]

# word -> replacement. Word boundaries applied via regex.
MAP: dict[str, str] = {
    # nouns / common verbs
    "entree": "entrée", "entrees": "entrées",
    "evenement": "événement", "evenements": "événements",
    "securite": "sécurité",
    "execution": "exécution", "Execution": "Exécution",
    "Reveler": "Révéler", "reveler": "révéler",
    "cloture": "clôture", "Cloture": "Clôture",
    "derive": "dérive",
    "detecte": "détecte", "detectee": "détectée",
    "detectes": "détectés", "detectees": "détectées",
    "dedie": "dédié", "dediee": "dédiée",
    "dedies": "dédiés", "dediees": "dédiées",
    "synchronise": "synchronisé", "synchronisee": "synchronisée",
    "synchronises": "synchronisés", "synchronisees": "synchronisées",
    "prepare": "préparé", "preparee": "préparée",
    "prepares": "préparés", "preparees": "préparées",
    "emis": "émis", "emise": "émise",
    "aligne": "aligné", "alignee": "alignée",
    "alignes": "alignés", "alignees": "alignées",
    "meme": "même", "memes": "mêmes",
    "bloquee": "bloquée", "bloquees": "bloquées",
    "seance": "séance", "seances": "séances",
    "Seance": "Séance", "Seances": "Séances",
    "decision": "décision", "decisions": "décisions",
    "theatre": "théâtre", "Theatre": "Théâtre",
    "recent": "récent", "recente": "récente",
    "recents": "récents", "recentes": "récentes",
    "Reference": "Référence",
    "Chaine": "Chaîne", "chaine": "chaîne",
    "prete": "prête",
    "tache": "tâche", "taches": "tâches",
    "verification": "vérification", "Verification": "Vérification",
    "operateur": "opérateur", "operateurs": "opérateurs",
    "observee": "observée", "observees": "observées",
    "attache": "attaché", "attachee": "attachée",
    "attaches": "attachés", "attachees": "attachées",
    "auditee": "auditée", "auditees": "auditées",
    "borne": "borné", "bornee": "bornée",
    "bornes": "bornés", "bornees": "bornées",
    "relies": "reliés", "reliee": "reliée",
    "reliees": "reliées",
    "bloquante": "bloquante",  # noop, just to keep doc
    "causalite": "causalité",
    "lisibilite": "lisibilité",
    "traces": "traces",  # noop
    "donnee": "donnée", "donnees": "données",
    "noeud": "nœud", "noeuds": "nœuds",
    "Noeud": "Nœud", "Noeuds": "Nœuds",
    "oeil": "œil",
    "Systeme": "Système", "systeme": "système",
    "archivee": "archivée",
    "archivees": "archivées",
    "activee": "activée", "activees": "activées",
    "declaree": "déclarée", "declarees": "déclarées",
    "declare": "déclaré", "declares": "déclarés",
    "capacite": "capacité", "capacites": "capacités",
    "interdite": "interdite",
    "interdites": "interdites",
    "specialisee": "spécialisée",
    "specialisees": "spécialisées",
    "scenario": "scénario", "scenarios": "scénarios",
    "verifie": "vérifié", "verifiee": "vérifiée",
    "verifies": "vérifiés", "verifiees": "vérifiées",
    "verifier": "vérifier",
    "lisible": "lisible",  # noop
    "legible": "lisible",
    "derniers": "derniers",  # noop
    "ete": "été",
    "rejetee": "rejetée", "rejetees": "rejetées",
    "rejete": "rejeté", "rejetes": "rejetés",
    "Arbitrer": "Arbitrer",  # already ok
    "arbitrage": "arbitrage",  # ok
    "Escalation": "Escalation",  # ok
    "acceptee": "acceptée", "acceptees": "acceptées",
    "refusee": "refusée", "refusees": "refusées",
    "detaille": "détaillé", "detaillee": "détaillée",
    "concernee": "concernée",
    "filtree": "filtrée", "filtrees": "filtrées",
    "hote": "hôte", "hotes": "hôtes",
    "Hote": "Hôte", "Hotes": "Hôtes",
    "operatoire": "opératoire",
    "lineage": "lineage",  # ok (anglais)
    "Bloques": "Bloqués",  # UI chip
    "rejete": "rejeté",
    "a": "a",  # noop
}

# Precompute word-boundary regex per key (longer keys first to avoid partial).
keys_sorted = sorted(MAP.keys(), key=len, reverse=True)
PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(rf"(?<![A-Za-zÀ-ÿ_0-9]){re.escape(k)}(?![A-Za-zÀ-ÿ_0-9])"), MAP[k])
    for k in keys_sorted
    if MAP[k] != k
]

# Match single/double/backtick strings. Backtick includes ${...} interp which
# we must not rewrite (code is inside). For simplicity, strip-inplace approach:
STRING_RE = re.compile(
    r"""
    (?P<q>'(?:\\.|[^'\\])*'         # single-quoted
      | "(?:\\.|[^"\\])*"           # double-quoted
      | `(?:\\.|\$\{[^}]*\}|[^`\\])*`  # backtick
    )
    """,
    re.VERBOSE,
)


def rewrite_string(lit: str) -> str:
    # For backtick, split on ${...} to keep interpolations intact.
    if lit.startswith("`"):
        parts: list[str] = []
        i = 1
        buf = ""
        while i < len(lit) - 1:
            if lit[i] == "$" and i + 1 < len(lit) and lit[i + 1] == "{":
                # flush buf
                parts.append(apply(buf))
                buf = ""
                # capture ${...} verbatim
                depth = 1
                j = i + 2
                while j < len(lit) and depth > 0:
                    if lit[j] == "{":
                        depth += 1
                    elif lit[j] == "}":
                        depth -= 1
                    j += 1
                parts.append(lit[i:j])
                i = j
            else:
                buf += lit[i]
                i += 1
        parts.append(apply(buf))
        return "`" + "".join(parts) + "`"
    # single/double quoted: just apply inside.
    quote = lit[0]
    inner = lit[1:-1]
    return quote + apply(inner) + quote


def apply(s: str) -> str:
    for pat, rep in PATTERNS:
        s = pat.sub(rep, s)
    return s


def process(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    new = STRING_RE.sub(lambda m: rewrite_string(m.group("q")), text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return 1
    return 0


def main() -> int:
    changed = 0
    scanned = 0
    for base in TARGETS:
        if not base.exists():
            continue
        for p in base.rglob("*.ts"):
            if p.suffix != ".ts":
                continue
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
