#!/usr/bin/env python3
"""Prototype — Grimoire knowledge stores -> Open Knowledge Format (OKF v0.1) bundle.

OKF v0.1 (Google, 2026) : un bundle de connaissance = un repertoire de fichiers
markdown + frontmatter YAML, un seul champ obligatoire (`type`), champs reserves
{title, description, resource, tags, timestamp}, fichiers reserves index.md
(divulgation progressive) et log.md (historique), liens markdown relatifs entre
concepts -> graphe.

Ce script demontre Grimoire comme *producteur* OKF en exportant trois producteurs
de connaissance distincts vers UN format commun :

  1. Memoire agent       (~/.claude/.../memory/*.md)        -> memory/<type>/<slug>.md
  2. Registre de sources (knowledge-source-registry.yaml)   -> sources/<id>.md
  3. Policy memoire       (memory-policy.yaml: memory_types) -> policy/<memory_id>.md

Stdlib + PyYAML uniquement. Aucun lock-in : la sortie est "just markdown / just files".
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# --- Champs reserves OKF v0.1 (ordre canonique du frontmatter) ---
OKF_RESERVED = ("type", "title", "description", "resource", "tags", "timestamp")

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AGENT_MEMORY = Path(
    "~/.claude/projects/-mnt-Travail-Projets-Dev-Grimoire-Forge/memory"
).expanduser()
DEFAULT_OUT = REPO_ROOT / "_grimoire-runtime-output" / "okf-prototype" / "bundle"

WIKILINK = re.compile(r"\[\[([a-z0-9_\-]+)\]\]")


def iso(ts: float | None = None) -> str:
    dt = datetime.fromtimestamp(ts, tz=timezone.utc) if ts else datetime.now(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def humanize(slug: str) -> str:
    return re.sub(r"[_\-]+", " ", slug).strip().capitalize()


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Separe le frontmatter YAML du corps markdown. Tolere l'absence."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = yaml.safe_load(text[3:end]) or {}
            body = text[end + 4 :].lstrip("\n")
            return (fm if isinstance(fm, dict) else {}), body
    return {}, text


def emit(path: Path, frontmatter: dict, body: str) -> None:
    """Ecrit un document OKF : frontmatter reserve d'abord, puis champs libres."""
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = {k: frontmatter[k] for k in OKF_RESERVED if k in frontmatter}
    extra = {k: v for k, v in frontmatter.items() if k not in OKF_RESERVED}
    ordered.update(extra)
    fm = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True).rstrip()
    path.write_text(f"---\n{fm}\n---\n\n{body.rstrip()}\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Producteur 1 — Memoire agent (markdown + frontmatter Grimoire)
# --------------------------------------------------------------------------- #
def memory_type(fm: dict) -> str:
    meta = fm.get("metadata") or {}
    return str(fm.get("type") or meta.get("type") or "misc")


def export_agent_memory(src_dir: Path, out: Path) -> list[dict]:
    if not src_dir.exists():
        print(f"  [skip] memoire agent absente : {src_dir}")
        return []
    files = sorted(p for p in src_dir.glob("*.md") if p.name != "MEMORY.md")

    # Resolution des wikilinks : stem -> type (pour construire les chemins relatifs OKF)
    stem_type = {}
    parsed = {}
    for p in files:
        fm, body = split_frontmatter(p.read_text(encoding="utf-8"))
        stem_type[p.stem] = memory_type(fm)
        parsed[p.stem] = (p, fm, body)

    def relink(m: re.Match) -> str:
        target = m.group(1)
        ttype = stem_type.get(target)
        if ttype:
            return f"[{humanize(target)}](../{ttype}/{target}.md)"
        # Lien pendant tolere par OKF (concept pas encore ecrit)
        return f"[{humanize(target)}](../{target}.md)"

    entries = []
    for stem, (p, fm, body) in parsed.items():
        mtype = stem_type[stem]
        body = WIKILINK.sub(relink, body)
        okf = {
            "type": f"Grimoire Memory/{mtype.capitalize()}",
            "title": str(fm.get("name") or humanize(stem)),
            "description": str(fm.get("description", "")),
            "resource": f"grimoire-memory://{src_dir.name}/{p.name}",
            "tags": sorted({mtype, "memory", "agent-memory"}),
            "timestamp": iso(p.stat().st_mtime),
            "grimoire_origin_session": (fm.get("metadata") or {}).get("originSessionId")
            or fm.get("originSessionId"),
        }
        okf = {k: v for k, v in okf.items() if v is not None}
        rel = f"memory/{mtype}/{stem}.md"
        emit(out / rel, okf, body)
        entries.append({"path": rel, "type": okf["type"], "title": okf["title"]})
    print(f"  [ok] memoire agent : {len(entries)} concepts -> memory/")
    return entries


# --------------------------------------------------------------------------- #
# Producteur 2 — Registre de sources de connaissance
# --------------------------------------------------------------------------- #
def export_knowledge_sources(registry: Path, out: Path) -> list[dict]:
    if not registry.exists():
        print(f"  [skip] registre absent : {registry}")
        return []
    data = yaml.safe_load(registry.read_text(encoding="utf-8")) or {}
    entries = []
    for src in data.get("sources", []):
        sid = src["id"]
        trust = src.get("trust", {})
        idx = src.get("indexing", {})
        ev = src.get("evidence", {})
        last = ev.get("last_indexed_at", "")
        body_lines = [
            f"> {src.get('type', 'source')} — `{src.get('locator', '')}`",
            "",
            "# Indexation",
            "",
            f"- Mode : {idx.get('mode', 'n/a')} ({idx.get('cadence', 'n/a')})",
            f"- Parser : {idx.get('parser', 'n/a')}",
            f"- Chunking : {idx.get('chunking_policy', 'n/a')}",
            "",
            "# Confiance",
            "",
            f"- Niveau : {trust.get('level', 'n/a')}",
            f"- Source of truth : {trust.get('source_of_truth', False)}",
            f"- Owner : {trust.get('owner', 'n/a')}",
            f"- Freshness SLA : {trust.get('freshness_sla', 'n/a')}",
        ]
        gaps = ev.get("known_gaps") or []
        if gaps:
            body_lines += ["", "# Lacunes connues", ""] + [f"- {g}" for g in gaps]
        okf = {
            "type": "Grimoire Knowledge Source",
            "title": humanize(sid),
            "description": f"{src.get('type', 'source')} indexee depuis {src.get('locator', 'n/a')}",
            "resource": str(src.get("locator", "")),
            "tags": sorted(
                {"knowledge-source", trust.get("level", "unknown")}
                | ({"source-of-truth"} if trust.get("source_of_truth") else set())
                | ({"enabled"} if src.get("enabled") else {"disabled"})
            ),
            "timestamp": last if re.match(r"\d{4}-\d{2}-\d{2}", str(last)) else iso(),
        }
        rel = f"sources/{sid}.md"
        emit(out / rel, okf, "\n".join(body_lines))
        entries.append({"path": rel, "type": okf["type"], "title": okf["title"]})
    print(f"  [ok] registre de sources : {len(entries)} concepts -> sources/")
    return entries


# --------------------------------------------------------------------------- #
# Producteur 3 — Policy memoire (types de memoire)
# --------------------------------------------------------------------------- #
def export_memory_policy(policy: Path, out: Path) -> list[dict]:
    if not policy.exists():
        print(f"  [skip] policy absente : {policy}")
        return []
    data = yaml.safe_load(policy.read_text(encoding="utf-8")) or {}
    entries = []
    for mt in data.get("memory_types", []):
        mid = mt["memory_id"]
        rows = [
            ("Scope", mt.get("scope", "")),
            ("Read policy", mt.get("read_policy", "")),
            ("Write policy", mt.get("write_policy", "")),
            ("Retention", mt.get("retention", "")),
            ("Freshness", mt.get("freshness", "")),
            ("Trust level", mt.get("trust_level", "")),
            ("Redaction", mt.get("redaction_policy", "")),
            ("Providers", ", ".join(mt.get("provider_compatibility", []))),
            ("Context uses", ", ".join(mt.get("allowed_context_uses", []))),
        ]
        body = "\n".join(
            ["| Champ | Valeur |", "|---|---|"]
            + [f"| {k} | {v} |" for k, v in rows]
        )
        okf = {
            "type": "Grimoire Memory Policy",
            "title": humanize(mid),
            "description": str(mt.get("scope", "")),
            "tags": sorted({"memory-policy", mt.get("trust_level", "unknown")}),
            "timestamp": iso(),
        }
        rel = f"policy/{mid}.md"
        emit(out / rel, okf, body)
        entries.append({"path": rel, "type": okf["type"], "title": okf["title"]})
    print(f"  [ok] policy memoire : {len(entries)} concepts -> policy/")
    return entries


# --------------------------------------------------------------------------- #
# Fichiers reserves OKF : index.md (par dossier + racine) et log.md
# --------------------------------------------------------------------------- #
def write_section_indexes(out: Path, all_entries: list[dict]) -> None:
    by_dir: dict[str, list[dict]] = {}
    for e in all_entries:
        section = e["path"].split("/")[0]
        by_dir.setdefault(section, []).append(e)
    for section, items in by_dir.items():
        lines = [f"# {humanize(section)}", "", f"{len(items)} concepts.", ""]
        for e in sorted(items, key=lambda x: x["title"].lower()):
            name = e["path"].split("/", 1)[1]
            lines.append(f"- [{e['title']}]({name}) — {e['type']}")
        emit(
            out / section / "index.md",
            {
                "type": "OKF Index",
                "title": humanize(section),
                "description": f"Index du producteur '{section}'.",
                "timestamp": iso(),
            },
            "\n".join(lines),
        )


def write_root(out: Path, all_entries: list[dict]) -> None:
    sections = sorted({e["path"].split("/")[0] for e in all_entries})
    lines = [
        "# Grimoire Knowledge — OKF Bundle",
        "",
        "Bundle Open Knowledge Format v0.1 genere depuis les stores de connaissance Grimoire.",
        "Producteurs heterogenes, un seul format.",
        "",
        "# Producteurs",
        "",
    ]
    for s in sections:
        n = sum(1 for e in all_entries if e["path"].startswith(f"{s}/"))
        lines.append(f"- [{humanize(s)}]({s}/index.md) — {n} concepts")
    lines += ["", f"Total : {len(all_entries)} concepts.", "", "Voir [log.md](log.md)."]
    emit(
        out / "index.md",
        {
            "type": "OKF Index",
            "title": "Grimoire Knowledge Bundle",
            "description": "Racine du bundle OKF — divulgation progressive.",
            "tags": ["okf", "grimoire", "knowledge"],
            "timestamp": iso(),
        },
        "\n".join(lines),
    )


def write_log(out: Path, all_entries: list[dict]) -> None:
    body = (
        f"# Historique\n\n## {iso()}\n\n"
        f"- Export OKF v0.1 genere : {len(all_entries)} concepts.\n"
        f"- Producteurs : "
        + ", ".join(sorted({e['path'].split('/')[0] for e in all_entries}))
        + ".\n"
    )
    emit(
        out / "log.md",
        {
            "type": "OKF Log",
            "title": "Change history",
            "description": "Historique de generation du bundle.",
            "timestamp": iso(),
        },
        body,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Export Grimoire knowledge -> OKF v0.1 bundle")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--agent-memory", type=Path, default=DEFAULT_AGENT_MEMORY)
    ap.add_argument(
        "--registry",
        type=Path,
        default=REPO_ROOT / "_grimoire" / "standard" / "knowledge-source-registry.yaml",
    )
    ap.add_argument(
        "--policy",
        type=Path,
        default=REPO_ROOT / "_grimoire" / "standard" / "memory-policy.yaml",
    )
    args = ap.parse_args()

    out = args.out
    print(f"Export OKF v0.1 -> {out}")
    entries: list[dict] = []
    entries += export_agent_memory(args.agent_memory, out)
    entries += export_knowledge_sources(args.registry, out)
    entries += export_memory_policy(args.policy, out)

    if not entries:
        print("Aucun concept exporte.", file=sys.stderr)
        return 1

    write_section_indexes(out, entries)
    write_root(out, entries)
    write_log(out, entries)
    print(f"Bundle OKF complet : {len(entries)} concepts + index/log -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
