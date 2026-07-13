#!/usr/bin/env python3
"""Mesure d'engagement des workflows (chantier C4).

Deux modes :
  record  — lit le payload UserPromptSubmit sur stdin, detecte les artefacts
            workflow/standard references (slash command /grimoire-*, nom de
            workflow du manifest, fichier workflow cite) et appende les
            signaux dans _grimoire-runtime/_memory/engagement.jsonl.
            Fail-open : jamais d'erreur bloquante.
  report  — agrege le journal : signaux par artefact, par canal, par jour.
            Ce rapport est la metrique d'entree du bras « active » de la
            campagne d'evals : il distingue « jamais engage » de « engage
            sans effet ».

Le journal vit sous _grimoire-runtime/_memory/ (protege par memory-guard,
ecrit par hook uniquement), comme board-transitions.jsonl (C1).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

MANIFEST_REL = Path("_grimoire-runtime/_config/workflow-manifest.csv")
JOURNAL_REL = Path("_grimoire-runtime/_memory/engagement.jsonl")


def now_iso() -> str:
    return datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_workflow_names(root: Path) -> list[str]:
    path = root / MANIFEST_REL
    if not path.is_file():
        return []
    names: list[str] = []
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            name = (row.get("name") or "").strip().strip('"')
            if name:
                names.append(name)
    return names


def extract_prompt(payload: str) -> tuple[str, str]:
    try:
        data = json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        return payload, ""
    prompt = ""
    for key in ("prompt", "userPrompt", "user_prompt", "text", "message"):
        value = data.get(key)
        if isinstance(value, str) and value:
            prompt = value
            break
    session = ""
    for key in ("session_id", "sessionId", "conversation_id", "conversationId"):
        value = data.get(key)
        if value:
            session = str(value)
            break
    return prompt or payload, session


def detect_signals(prompt: str, names: list[str]) -> list[dict]:
    lowered = prompt.lower()
    signals: list[dict] = []
    for name in names:
        needle = name.lower()
        if f"/grimoire-{needle}" in lowered or f"/{needle}" in lowered:
            signals.append({"artifact": name, "kind": "workflow", "signal": "slash-command"})
        elif needle in lowered and len(needle) >= 6:
            # Noms courts exclus : trop de faux positifs en prose libre.
            signals.append({"artifact": name, "kind": "workflow", "signal": "prompt-mention"})
    if "task-board.yaml" in lowered or "kanban" in lowered:
        signals.append({"artifact": "task-board", "kind": "standard", "signal": "prompt-mention"})
    return signals


def cmd_record(root: Path, payload: str) -> int:
    try:
        prompt, session = extract_prompt(payload)
        if not prompt:
            return 0
        signals = detect_signals(prompt, load_workflow_names(root))
        if not signals:
            return 0
        path = root / JOURNAL_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        ts = now_iso()
        with open(path, "a", encoding="utf-8") as fh:
            for signal in signals:
                signal.update({"ts": ts, "session": session})
                fh.write(json.dumps(signal, ensure_ascii=False) + "\n")
        return 0
    except Exception:
        return 0  # fail-open


def cmd_report(root: Path) -> int:
    path = root / JOURNAL_REL
    if not path.is_file():
        print("engagement-report: journal vide — aucun engagement enregistre encore.")
        print("Interpretation campagne : un effet nul avec engagement nul ne dit rien du workflow, seulement de son declenchement.")
        return 0
    by_artifact: Counter[str] = Counter()
    by_signal: Counter[str] = Counter()
    by_day: Counter[str] = Counter()
    sessions: set[str] = set()
    total = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        total += 1
        by_artifact[entry.get("artifact", "?")] += 1
        by_signal[entry.get("signal", "?")] += 1
        by_day[str(entry.get("ts", ""))[:10]] += 1
        if entry.get("session"):
            sessions.add(entry["session"])
    print(f"engagement-report: {total} signal(s), {len(sessions)} session(s) identifiee(s)")
    print("\nPar artefact :")
    for artifact, count in by_artifact.most_common():
        print(f"  {artifact}: {count}")
    print("\nPar canal :")
    for signal, count in by_signal.most_common():
        print(f"  {signal}: {count}")
    print("\nPar jour :")
    for day in sorted(by_day):
        print(f"  {day}: {by_day[day]}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("record", help="detecte les signaux d'engagement du prompt (stdin)")
    sub.add_parser("report", help="agrege le journal d'engagement")
    args = parser.parse_args()
    root = args.project_root.resolve()
    if args.command == "record":
        return cmd_record(root, sys.stdin.read())
    return cmd_report(root)


if __name__ == "__main__":
    raise SystemExit(main())
