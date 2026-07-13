#!/usr/bin/env python3
"""Reconciliateur evidence contre realite (chantier C2).

Confronte chaque claim des evidence packs aux sources machine :
  - refs du task-board (context/decision/evidence) : existence sur disque,
    exigee des que la tache atteint review ;
  - inventaire des packs markdown : chaque token cite (chemin, commit,
    branche) est verifie contre le disque et les depots git ;
  - packs JSONL EvidenceService : recalcul sha256 des uri locales et
    comparaison au digest declare, correlation TEST/LOG avec les events
    task-flow (exitCode 0) ;

Verdicts par claim :
  VERIFIED      — corrobore par une source machine
  UNVERIFIABLE  — aucune source machine ne peut corroborer (warning en
                  profil governed, erreur en production)
  CONTRADICTED  — une source machine contredit le claim (toujours erreur)

Exit 1 des qu'un claim atteint la severite erreur. Consomme par
npm run quality (section Preuve).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def _make_yaml_loader():
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
PROFILE_REL = Path("_grimoire/standard/standard-profile.yaml")
EVENTS_REL = Path("_grimoire-runtime-output/task-flow/events.jsonl")
JSONL_PACKS_REL = Path("_grimoire-runtime-output/evidence/packs.jsonl")

REF_KEYS = ("context_bundle_ref", "decision_trace_ref", "evidence_pack_ref")
REFS_REQUIRED_STATUSES = {"review", "accepted", "released"}
REFS_EXPECTED_STATUSES = {"in_progress"} | REFS_REQUIRED_STATUSES

COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")
BACKTICK_RE = re.compile(r"`([^`]+)`")
PATHLIKE_SUFFIXES = (".yaml", ".yml", ".md", ".py", ".sh", ".json", ".toml", ".txt", ".csv")


class Report:
    def __init__(self) -> None:
        self.verified: list[str] = []
        self.unverifiable: list[str] = []
        self.contradicted: list[str] = []

    def add(self, verdict: str, message: str) -> None:
        getattr(self, verdict.lower()).append(message)


def git_repos(root: Path) -> list[Path]:
    repos = [root]
    kit = root / "grimoire-kit"
    if (kit / ".git").exists():
        repos.append(kit)
    return repos


def git_commit_exists(repos: list[Path], sha: str) -> bool:
    for repo in repos:
        result = subprocess.run(
            ["git", "-C", str(repo), "cat-file", "-e", f"{sha}^{{commit}}"],
            capture_output=True, timeout=10, check=False,
        )
        if result.returncode == 0:
            return True
    return False


def git_ref_exists(repos: list[Path], ref: str) -> bool:
    for repo in repos:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", ref],
            capture_output=True, timeout=10, check=False,
        )
        if result.returncode == 0:
            return True
    return False


def path_exists(root: Path, token: str, pack_dir: Path | None) -> bool:
    candidates = [root / token, root / "grimoire-kit" / token]
    if pack_dir is not None:
        candidates.append(pack_dir / token)
    if token.startswith("/"):
        candidates.append(Path(token))
    return any(p.exists() for p in candidates)


def looks_pathlike(token: str) -> bool:
    if token.endswith(PATHLIKE_SUFFIXES):
        return True
    return "/" in token and " " not in token and not token.startswith("--")


def classify_token(root: Path, repos: list[Path], token: str, pack_dir: Path, context: str, report: Report) -> None:
    token = token.strip()
    if not token:
        return
    if COMMIT_RE.match(token):
        if git_commit_exists(repos, token):
            report.add("VERIFIED", f"{context}: commit `{token}` present")
        else:
            report.add("UNVERIFIABLE", f"{context}: commit `{token}` introuvable dans les depots locaux")
        return
    if "@" in token and not token.startswith("@") and "/" in token.split("@", 1)[1]:
        branch = token.split("@", 1)[1]
        if git_ref_exists(repos, branch):
            report.add("VERIFIED", f"{context}: branche `{branch}` presente")
        else:
            report.add("UNVERIFIABLE", f"{context}: branche `{branch}` introuvable dans les depots locaux")
        return
    if looks_pathlike(token):
        if path_exists(root, token, pack_dir):
            report.add("VERIFIED", f"{context}: chemin `{token}` present")
        else:
            report.add("CONTRADICTED", f"{context}: chemin `{token}` cite comme evidence mais absent du disque")
        return
    report.add("UNVERIFIABLE", f"{context}: token `{token}` inclassable (ni chemin, ni commit, ni branche)")


def markdown_inventory_rows(text: str) -> list[str]:
    """Cellules Location de la table '## Evidence inventory'."""
    rows: list[str] = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line.strip().lower() == "## evidence inventory"
            continue
        if in_section and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0] not in ("Evidence", "---") and not set(cells[0]) <= {"-", " "}:
                rows.append(cells[1])
    return rows


def reconcile_markdown_pack(root: Path, repos: list[Path], task_id: str, pack_path: Path, report: Report) -> None:
    text = pack_path.read_text(encoding="utf-8")
    locations = markdown_inventory_rows(text)
    if not locations:
        report.add("UNVERIFIABLE", f"{task_id}: pack `{pack_path.name}` sans table 'Evidence inventory' exploitable")
        return
    for location in locations:
        tokens = BACKTICK_RE.findall(location) or [location]
        for token in tokens:
            classify_token(root, repos, token, pack_path.parent, f"{task_id}/{pack_path.name}", report)


def load_events_commands(root: Path) -> list[str]:
    path = root / EVENTS_REL
    if not path.is_file():
        return []
    commands: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("exitCode") == 0 and event.get("status") in ("passed", "ok", "success", "running", None) or (
            event.get("exitCode") == 0 and event.get("event") == "task-finish"
        ):
            commands.append(f"{event.get('task', '')} {event.get('command', '')}")
    return commands


def reconcile_jsonl_packs(root: Path, report: Report) -> None:
    path = root / JSONL_PACKS_REL
    if not path.is_file():
        return
    commands = load_events_commands(root)
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            pack = json.loads(line)
        except json.JSONDecodeError:
            report.add("CONTRADICTED", f"packs.jsonl: ligne JSON invalide")
            continue
        pack_id = pack.get("id", "?")
        for item in pack.get("items") or []:
            item_id = item.get("id", "?")
            uri, digest, kind = item.get("uri", ""), item.get("digest", ""), item.get("kind", "")
            context = f"{pack_id}/{item_id}"
            local = root / uri if uri and not uri.startswith(("http://", "https://")) else None
            if local is not None and uri:
                if not local.is_file():
                    report.add("CONTRADICTED", f"{context}: uri `{uri}` absente du disque")
                    continue
                if digest.startswith("sha256-"):
                    actual = "sha256-" + hashlib.sha256(local.read_bytes()).hexdigest()
                    if actual == digest:
                        report.add("VERIFIED", f"{context}: digest sha256 conforme pour `{uri}`")
                    else:
                        report.add("CONTRADICTED", f"{context}: digest declare {digest[:19]}… != recalcule {actual[:19]}… pour `{uri}`")
                    continue
            if kind in ("test", "log"):
                needle = Path(uri).name if uri else item.get("summary", "")[:40]
                if needle and any(needle in command for command in commands):
                    report.add("VERIFIED", f"{context}: event task-flow exitCode 0 correspondant a `{needle}`")
                else:
                    report.add("UNVERIFIABLE", f"{context}: aucun event task-flow exitCode 0 ne corrobore `{needle}`")
            else:
                report.add("UNVERIFIABLE", f"{context}: uri non locale ou digest non sha256, rien a recalculer")


def read_profile_id(root: Path) -> str:
    path = root / PROFILE_REL
    if yaml_load is None or not path.is_file():
        return "governed"
    try:
        data = yaml_load(path.read_text(encoding="utf-8")) or {}
        for key in ("profile", "id", "profile_id"):
            if isinstance(data.get(key), str):
                return data[key]
    except Exception:
        pass
    return "governed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", type=Path)
    parser.add_argument("--strict", action="store_true", help="UNVERIFIABLE devient une erreur (force le profil production)")
    args = parser.parse_args()
    root = args.project_root.resolve()

    if yaml_load is None:
        print("evidence-reconcile: aucun loader YAML disponible", file=sys.stderr)
        return 1

    report = Report()
    repos = git_repos(root)
    board = yaml_load((root / BOARD_REL).read_text(encoding="utf-8"))

    for task in board.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        task_id = str(task.get("task_id", "?"))
        status = str(task.get("status", ""))
        for ref_key in REF_KEYS:
            ref = str(task.get(ref_key, "") or "").strip()
            if not ref:
                continue
            ref_path = root / ref
            if ref_path.is_file():
                report.add("VERIFIED", f"{task_id}: {ref_key} present (`{ref}`)")
                if ref_key == "evidence_pack_ref" and ref.endswith(".md"):
                    reconcile_markdown_pack(root, repos, task_id, ref_path, report)
            elif status in REFS_REQUIRED_STATUSES:
                report.add("CONTRADICTED", f"{task_id}: statut {status!r} mais {ref_key} absent (`{ref}`)")
            elif status in REFS_EXPECTED_STATUSES:
                report.add("UNVERIFIABLE", f"{task_id}: {ref_key} declare mais pas encore materialise (`{ref}`)")

    reconcile_jsonl_packs(root, report)

    profile = "production" if args.strict else read_profile_id(root)
    unverifiable_is_error = profile == "production"

    for message in report.contradicted:
        print(f"[CONTRADICTED] {message}")
    for message in report.unverifiable:
        print(f"[{'ERROR' if unverifiable_is_error else 'WARN'}] UNVERIFIABLE — {message}")
    if "-v" in sys.argv or "--verbose" in sys.argv:
        for message in report.verified:
            print(f"[VERIFIED] {message}")

    errors = len(report.contradicted) + (len(report.unverifiable) if unverifiable_is_error else 0)
    print(
        f"evidence-reconcile ({profile}): {len(report.verified)} VERIFIED, "
        f"{len(report.unverifiable)} UNVERIFIABLE, {len(report.contradicted)} CONTRADICTED"
    )
    if errors:
        print("evidence-reconcile: ECHEC")
        return 1
    print("evidence-reconcile: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
