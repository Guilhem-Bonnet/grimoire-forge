#!/usr/bin/env python3
"""Journal append-only des transitions du kanban gouverne (chantier C1).

Trois modes :
  record     — compare task-board.yaml au cache de statuts, appende les
               transitions detectees au journal, met a jour le cache.
               Fail-open : toute erreur est silencieuse (exit 0), le hook
               appelant ne doit jamais bloquer le runtime.
  check      — rejoue le journal, verifie la coherence avec le board courant
               et la legalite des transitions selon evidence-gates.yaml.
               Exit 1 si erreur (consomme par npm run quality).
  reconcile  — comme record --force mais marque les entrees via=reconcile :
               le drift (edition manuelle hors hook) est acte, pas masque.

Le journal vit sous _grimoire-runtime/_memory/ : ce prefixe est protege en
ecriture agent par le memory-guard existant (guardrail-policy.py), ce qui
garantit que seuls les hooks ecrivent ici. Ne pas le deplacer.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

def _make_yaml_loader():
    """ruamel.yaml (dep du kit) en priorite, PyYAML en repli, None sinon."""
    try:
        from ruamel.yaml import YAML

        _ruamel = YAML(typ="safe")
        return lambda text: _ruamel.load(text)
    except ImportError:
        pass
    try:
        import yaml as _pyyaml

        return _pyyaml.safe_load
    except ImportError:
        return None


yaml_load = _make_yaml_loader()

BOARD_REL = Path("_grimoire/standard/task-board.yaml")
GATES_REL = Path("_grimoire/standard/evidence-gates.yaml")
JOURNAL_REL = Path("_grimoire-runtime/_memory/board-transitions.jsonl")
CACHE_REL = Path("_grimoire-runtime/_memory/board-status-cache.json")

# Ordre nominal du cycle de vie (blocked est hors sequence).
STATE_ORDER = ["proposed", "ready", "in_progress", "review", "accepted", "released", "archived"]


def now_iso() -> str:
    return datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_board_statuses(root: Path) -> dict[str, str]:
    data = yaml_load((root / BOARD_REL).read_text(encoding="utf-8"))
    statuses: dict[str, str] = {}
    for task in data.get("tasks") or []:
        if isinstance(task, dict) and task.get("task_id"):
            statuses[str(task["task_id"])] = str(task.get("status", ""))
    return statuses


def load_cache(root: Path) -> dict[str, str] | None:
    path = root / CACHE_REL
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_cache(root: Path, statuses: dict[str, str]) -> None:
    path = root / CACHE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(statuses, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def append_journal(root: Path, entries: list[dict]) -> None:
    path = root / JOURNAL_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        for entry in entries:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def payload_mentions_board(payload: str) -> bool:
    return "task-board.yaml" in payload


def extract_session(payload: str) -> str:
    try:
        data = json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        return ""
    for key in ("session_id", "sessionId", "conversation_id", "conversationId"):
        value = data.get(key)
        if value:
            return str(value)
    return ""


def cmd_record(root: Path, *, via: str, force: bool, session: str, payload: str) -> int:
    if yaml_load is None:
        return 0
    if not force and payload and not payload_mentions_board(payload):
        return 0
    try:
        current = load_board_statuses(root)
        cached = load_cache(root)
        ts = now_iso()
        entries: list[dict] = []
        if cached is None:
            # Premier passage : baseline, aucune transition fabriquee.
            for task_id, status in sorted(current.items()):
                entries.append({"ts": ts, "task_id": task_id, "from": None, "to": status, "via": "baseline", "session": session})
        else:
            for task_id, status in sorted(current.items()):
                previous = cached.get(task_id)
                if previous != status:
                    entries.append({"ts": ts, "task_id": task_id, "from": previous, "to": status, "via": via, "session": session})
            for task_id in sorted(set(cached) - set(current)):
                entries.append({"ts": ts, "task_id": task_id, "from": cached[task_id], "to": None, "via": via, "session": session})
        if entries:
            append_journal(root, entries)
        write_cache(root, current)
        return 0
    except Exception:
        return 0  # fail-open : un hook ne bloque jamais le runtime


def load_legal_transitions(root: Path) -> set[tuple[str, str]]:
    data = yaml_load((root / GATES_REL).read_text(encoding="utf-8"))
    legal: set[tuple[str, str]] = set()
    for transition in data.get("transitions") or []:
        if isinstance(transition, dict) and transition.get("from") and transition.get("to"):
            legal.add((str(transition["from"]), str(transition["to"])))
    return legal


def classify_transition(src: str | None, dst: str | None, legal: set[tuple[str, str]]) -> tuple[str, str]:
    """Retourne (severite, motif). Severite : ok | warning | error."""
    if src is None:
        if dst == "proposed":
            return "ok", ""
        return "warning", f"nouvelle tache entrant en {dst!r} au lieu de 'proposed'"
    if dst is None:
        if src == "archived":
            return "ok", ""
        return "warning", f"tache retiree du board depuis {src!r} sans passer par 'archived'"
    if (src, dst) in legal:
        return "ok", ""
    if dst == "blocked" or src == "blocked":
        return "ok", ""  # any_to_blocked et deblocage sont admis
    if src in STATE_ORDER and dst in STATE_ORDER:
        if STATE_ORDER.index(dst) > STATE_ORDER.index(src):
            return "error", f"transition avant non declaree {src!r} -> {dst!r} (gate sautee)"
        return "warning", f"retour en arriere {src!r} -> {dst!r} (reprise non gouvernee par les gates)"
    return "error", f"etat inconnu dans la transition {src!r} -> {dst!r}"


def cmd_check(root: Path) -> int:
    if yaml_load is None:
        print("board-transitions check: PyYAML indisponible", file=sys.stderr)
        return 1
    journal_path = root / JOURNAL_REL
    if not journal_path.is_file():
        print("board-transitions check: journal absent (aucun record encore effectue) — OK")
        return 0

    errors: list[str] = []
    warnings: list[str] = []
    replayed: dict[str, str | None] = {}
    legal = load_legal_transitions(root)

    for line_no, line in enumerate(journal_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"ligne {line_no}: JSON invalide")
            continue
        task_id = entry.get("task_id")
        src, dst, via = entry.get("from"), entry.get("to"), entry.get("via")
        if not task_id:
            errors.append(f"ligne {line_no}: task_id manquant")
            continue
        # Coherence de rejeu : le from de l'entree doit etre l'etat rejoue.
        if via != "baseline" and task_id in replayed and replayed[task_id] != src:
            errors.append(f"ligne {line_no}: {task_id} — from={src!r} mais etat rejoue {replayed[task_id]!r}")
        if via not in ("baseline",):
            severity, reason = classify_transition(src, dst, legal)
            label = f"ligne {line_no}: {task_id} — {reason}" + (f" [via={via}]" if via != "hook" else "")
            if severity == "error":
                errors.append(label)
            elif severity == "warning":
                warnings.append(label)
        replayed[task_id] = dst

    # Drift : board courant vs etat rejoue.
    current = load_board_statuses(root)
    for task_id, status in sorted(current.items()):
        if task_id not in replayed:
            errors.append(f"drift: {task_id} present sur le board mais absent du journal (edition hors hook) — lancer 'reconcile'")
        elif replayed[task_id] != status:
            errors.append(f"drift: {task_id} — board={status!r}, journal={replayed[task_id]!r} (edition hors hook) — lancer 'reconcile'")
    for task_id, status in sorted(replayed.items()):
        if status is not None and task_id not in current:
            errors.append(f"drift: {task_id} dans le journal (etat {status!r}) mais absent du board — lancer 'reconcile'")

    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"board-transitions check: ECHEC ({len(errors)} erreur(s), {len(warnings)} warning(s))")
        return 1
    print(f"board-transitions check: OK ({len(replayed)} tache(s) rejouee(s), {len(warnings)} warning(s))")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)

    p_record = sub.add_parser("record", help="detecte et journalise les transitions (fail-open)")
    p_record.add_argument("--force", action="store_true", help="ignorer le filtre task-board.yaml sur stdin")
    p_record.add_argument("--session", default="")
    p_record.add_argument("--stdin-json", action="store_true", help="lire le payload hook sur stdin")

    sub.add_parser("check", help="verifie coherence journal/board et legalite des transitions")

    p_reconcile = sub.add_parser("reconcile", help="acte un drift (edition hors hook) dans le journal")
    p_reconcile.add_argument("--session", default="")

    args = parser.parse_args()
    root = args.project_root.resolve()

    if args.command == "record":
        payload = sys.stdin.read() if args.stdin_json else ""
        session = args.session or extract_session(payload)
        return cmd_record(root, via="hook", force=args.force, session=session, payload=payload)
    if args.command == "check":
        return cmd_check(root)
    if args.command == "reconcile":
        return cmd_record(root, via="reconcile", force=True, session=args.session, payload="")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
