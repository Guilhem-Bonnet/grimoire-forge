#!/usr/bin/env python3
"""Prototype — Import OKF v0.1 bundle -> Grimoire Memory OS (round-trip degrade).

Sens inverse de okf_export.py. Lit un bundle OKF (le tien reimporte OU un bundle
externe) et l'ingere comme memoires Grimoire, EN PASSANT par les promotion gates
declares dans memory-policy.yaml (config-driven, pas de regles en dur).

Mode "degrade" : ne depend PAS d'un Neo4j peuple. Les aretes sont reconstruites
depuis les liens markdown du bundle (graphe non type, rel=links_to).

--- ABSTRACTION DE BACKEND (reponse contrainte corpo "pas de DB vectorielle locale") ---
La source-of-truth est le bundle markdown. Le store est un INDEX DERIVE, pluggable :

  * FileStore  (defaut)  -> JSONL + graph-edges.json + sqlite FTS5 plein-texte.
                            ZERO service, ZERO DB vectorielle. 100% fichiers locaux.
  * weaviate-server / qdrant-server -> point de branchement documente (non requis ici).

Le plein-texte BM25 (sqlite FTS5, embarque dans la stdlib) couvre la recherche sans
aucun vecteur : c'est l'alternative a proposer aux entreprises qui interdisent une
DB vectorielle locale.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BUNDLE = Path(__file__).resolve().parent / "bundle"
DEFAULT_STORE = Path(__file__).resolve().parent / "store"
DEFAULT_POLICY = REPO_ROOT / "_grimoire" / "standard" / "memory-policy.yaml"

MD_LINK = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")
SECRET = re.compile(
    r"(?i)(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*\S+|sk-[A-Za-z0-9]{16,}"
)
RESERVED_FILES = {"index.md", "log.md"}


def iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def governed_mode() -> str:
    """Lit l'option de setup memory.vector_database depuis project-context.yaml."""
    ctx_file = REPO_ROOT / "project-context.yaml"
    if not ctx_file.exists():
        return "vector (defaut)"
    mem = (yaml.safe_load(ctx_file.read_text(encoding="utf-8")) or {}).get("memory", {})
    if mem.get("vector_database") is False or str(mem.get("retrieval_mode")) == "lexical":
        return "lexical (sans DB vectorielle) -> sqlite FTS5 BM25"
    return "vector (DB vectorielle activee) -> weaviate/qdrant en prod"


def split_frontmatter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = yaml.safe_load(text[3:end]) or {}
            return (fm if isinstance(fm, dict) else {}), text[end + 4 :].lstrip("\n")
    return {}, text


# --------------------------------------------------------------------------- #
# Lecture du bundle -> concepts + aretes
# --------------------------------------------------------------------------- #
def parse_bundle(bundle: Path) -> list[dict]:
    concepts = []
    for md in sorted(bundle.rglob("*.md")):
        if md.name in RESERVED_FILES:
            continue
        rel = md.relative_to(bundle).as_posix()
        fm, body = split_frontmatter(md.read_text(encoding="utf-8"))

        # Aretes : liens markdown du corps qui resolvent DANS le bundle.
        edges = []
        for link in MD_LINK.findall(body):
            target = (md.parent / link).resolve()
            try:
                trel = target.relative_to(bundle.resolve()).as_posix()
            except ValueError:
                continue
            if (bundle / trel).exists() and Path(trel).name not in RESERVED_FILES:
                edges.append({"rel": "links_to", "target": trel})
        # Relations typees explicites (forward-compat prop 2)
        for r in fm.get("grimoire_relations", []) or []:
            edges.append({"rel": r.get("rel", "related"), "target": r.get("target")})

        concepts.append(
            {
                "path": rel,
                "type": str(fm.get("type", "")),
                "title": str(fm.get("title", Path(rel).stem)),
                "description": str(fm.get("description", "")),
                "resource": fm.get("resource"),
                "tags": fm.get("tags", []),
                "timestamp": fm.get("timestamp"),
                "body": body.strip(),
                "edges": edges,
            }
        )
    return concepts


# --------------------------------------------------------------------------- #
# Memory gate — promotion gates lus depuis memory-policy.yaml (config-driven)
# --------------------------------------------------------------------------- #
def load_gates(policy: Path) -> list[str]:
    if not policy.exists():
        return ["semantic_write_has_evidence", "graph_projection_has_source_refs"]
    data = yaml.safe_load(policy.read_text(encoding="utf-8")) or {}
    return (data.get("memory_os", {}) or {}).get("promotion_gates", [])


def gate_concept(c: dict, gates: list[str], known_paths: set[str]) -> dict:
    reasons, redactions = [], []
    passed = True

    # Redaction (memory-policy: redaction_policy required) avant tout backend.
    if SECRET.search(c["body"]):
        redactions.append("secret-pattern detecte -> a caviarder avant provider hosted")

    for g in gates:
        if g == "semantic_write_has_evidence":
            # Evidence = resource tracable OU timestamp source.
            if not (c.get("resource") or c.get("timestamp")):
                passed = False
                reasons.append("semantic_write_has_evidence: ni resource ni timestamp")
        elif g == "graph_projection_has_source_refs":
            # Toute arete doit pointer vers une cible connue du bundle.
            dangling = [e["target"] for e in c["edges"] if e["target"] not in known_paths]
            if dangling:
                reasons.append(
                    f"graph_projection_has_source_refs: cibles pendantes {dangling} "
                    "(arete degradee, conservee mais signalee)"
                )
        # hot_memory_ttl_declared / qdrant_migration_bundle_verified : N/A en import durable
    return {"accepted": passed, "reasons": reasons, "redactions": redactions}


# --------------------------------------------------------------------------- #
# Backend : FileStore (defaut, zero service, zero DB vectorielle)
# --------------------------------------------------------------------------- #
class FileStore:
    """Index derive, 100% fichiers. Reconstructible a tout moment depuis le bundle."""

    def __init__(self, store: Path):
        self.store = store
        store.mkdir(parents=True, exist_ok=True)
        self.records: list[dict] = []
        self.edges: list[dict] = []

    def upsert(self, c: dict) -> None:
        self.records.append(
            {
                "id": c["path"],
                "type": c["type"],
                "title": c["title"],
                "description": c["description"],
                "resource": c.get("resource"),
                "tags": c.get("tags", []),
                "timestamp": c.get("timestamp"),
                "text": c["body"],
                "ingested_at": iso(),
            }
        )
        for e in c["edges"]:
            self.edges.append({"source": c["path"], **e})

    def commit(self) -> dict:
        store = self.store
        (store / "memory-store.jsonl").write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in self.records) + "\n",
            encoding="utf-8",
        )
        (store / "graph-edges.json").write_text(
            json.dumps(self.edges, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        fts = self._build_fts(store / "memory-fts.sqlite")
        return {"records": len(self.records), "edges": len(self.edges), "fts": fts}

    def _build_fts(self, db_path: Path) -> str:
        """Recherche plein-texte BM25 SANS vecteur ni service (sqlite FTS5 embarque)."""
        if db_path.exists():
            db_path.unlink()
        con = sqlite3.connect(db_path)
        try:
            con.execute(
                "CREATE VIRTUAL TABLE mem USING fts5(id, title, tags, text, "
                "tokenize='unicode61 remove_diacritics 2')"
            )
        except sqlite3.OperationalError:
            con.close()
            db_path.unlink(missing_ok=True)
            return "FTS5 indisponible dans ce build sqlite (fallback: grep sur le bundle)"
        con.executemany(
            "INSERT INTO mem(id, title, tags, text) VALUES (?,?,?,?)",
            [(r["id"], r["title"], " ".join(r["tags"]), r["text"]) for r in self.records],
        )
        con.commit()
        con.close()
        return f"FTS5 BM25 pret ({len(self.records)} docs) — recherche sans DB vectorielle"


def fts_query(raw: str) -> str:
    """Requete FTS5-safe : chaque token cite (neutralise -, :, * et autres operateurs)."""
    tokens = re.findall(r"\w+", raw, flags=re.UNICODE)
    return " OR ".join(f'"{t}"' for t in tokens)  # recall: match any term, BM25 classe


def search_demo(store: Path, query: str) -> list[tuple]:
    db = store / "memory-fts.sqlite"
    if not db.exists():
        return []
    con = sqlite3.connect(db)
    rows = con.execute(
        "SELECT id, title, bm25(mem) AS score FROM mem WHERE mem MATCH ? "
        "ORDER BY score LIMIT 5",
        (fts_query(query),),
    ).fetchall()
    con.close()
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Import OKF bundle -> Grimoire Memory (degrade)")
    ap.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    ap.add_argument("--store", type=Path, default=DEFAULT_STORE)
    ap.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    ap.add_argument("--search", type=str, help="Demo recherche plein-texte (sans vecteur)")
    args = ap.parse_args()

    if args.search:
        for cid, title, score in search_demo(args.store, args.search):
            print(f"  {score:7.2f}  {title}  [{cid}]")
        return 0

    if not args.bundle.exists():
        print(f"Bundle introuvable : {args.bundle}", file=sys.stderr)
        return 1

    gates = load_gates(args.policy)
    concepts = parse_bundle(args.bundle)
    known = {c["path"] for c in concepts}
    print(f"Mode de retrieval gouverne (setup) : {governed_mode()}")
    print(f"Import OKF degrade : {len(concepts)} concepts, gates={gates}")

    store = FileStore(args.store)
    report = {"accepted": [], "quarantined": [], "flagged": []}
    for c in concepts:
        verdict = gate_concept(c, gates, known)
        if verdict["redactions"]:
            report["flagged"].append({"id": c["path"], "redactions": verdict["redactions"]})
        if verdict["accepted"]:
            store.upsert(c)
            entry = {"id": c["path"], "edges": len(c["edges"])}
            if verdict["reasons"]:
                entry["warnings"] = verdict["reasons"]
            report["accepted"].append(entry)
        else:
            report["quarantined"].append({"id": c["path"], "reasons": verdict["reasons"]})

    stats = store.commit()
    (args.store / "import-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        f"  accepte={len(report['accepted'])}  "
        f"quarantaine={len(report['quarantined'])}  "
        f"flag-redaction={len(report['flagged'])}"
    )
    print(f"  store: {stats['records']} records, {stats['edges']} aretes")
    print(f"  {stats['fts']}")
    print(f"  -> {args.store}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
