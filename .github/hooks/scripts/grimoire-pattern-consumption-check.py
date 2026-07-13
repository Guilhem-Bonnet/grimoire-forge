#!/usr/bin/env python3
"""grimoire-pattern-consumption-check.py — garde-fou « fonctionnel = consommé ».

Lot 4 du plan durcissement-agentique-20260712 (items 4.1-4.3).

Deux niveaux de contrôle :

1. Statique (bloquant, exit 1 si violation) : chaque sigle de protocole
   agentique trouvé dans les instructions (`.github/copilot-instructions.md`,
   `.github/agents/*.agent.md`) doit être déclaré dans le manifeste de
   gouvernance `_grimoire-runtime/_config/pattern-consumption-manifest.json`.
   Un sigle `executable` doit pointer un artefact existant ; un sigle
   `retired` ne peut apparaître que dans une phrase de retrait.

2. Dynamique (avertissement, n'affecte pas l'exit code) : chaque hook
   `mode: enforced` du registre `hook-safety-registry.json` doit avoir au
   moins un événement dans le journal safety-gate sur une fenêtre glissante
   (30 jours par défaut). Le journal est lu en streaming (hookId/ts
   uniquement, jamais chargé entièrement en mémoire).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SIGLES = (
    "SOG",
    "HUP",
    "QEC",
    "CVTL",
    "PCE",
    "ALS",
    "ARG",
    "PIP",
    "AORA",
    "DCF",
    "ELSS",
    "UDF",
)
SIGLE_PATTERN = re.compile(r"\b(" + "|".join(SIGLES) + r")\b")
RETIREMENT_PATTERN = re.compile(r"retir|retrait", re.IGNORECASE)
VALID_STATUSES = frozenset({"executable", "prose-pending-lot3", "observer-only", "retired"})

MANIFEST_RELATIVE = Path("_grimoire-runtime/_config/pattern-consumption-manifest.json")
REGISTRY_RELATIVE = Path("_grimoire-runtime/_config/hook-safety-registry.json")
EVENTS_RELATIVE = Path("_grimoire-runtime-output/hook-runtime/safety-gate/events.jsonl")
INSTRUCTIONS_RELATIVE = Path(".github/copilot-instructions.md")
AGENTS_GLOB = ".github/agents/*.agent.md"


def default_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_manifest(path: Path) -> tuple[dict[str, dict], list[str]]:
    """Charge le manifeste de gouvernance. Retourne (patterns, erreurs)."""
    errors: list[str] = []
    if not path.is_file():
        return {}, [f"Manifeste de gouvernance introuvable: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"Manifeste de gouvernance invalide ({exc.msg} ligne {exc.lineno})"]
    patterns = payload.get("patterns")
    if not isinstance(patterns, dict):
        return {}, ["Le manifeste doit contenir un mapping 'patterns'."]
    for sigle, entry in patterns.items():
        if not isinstance(entry, dict):
            errors.append(f"Entrée manifeste invalide pour {sigle} (objet attendu).")
            continue
        status = entry.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"Statut inconnu pour {sigle}: {status!r}.")
        if status == "executable" and not str(entry.get("artifact") or "").strip():
            errors.append(f"Sigle {sigle} déclaré 'executable' sans champ 'artifact'.")
    return patterns, errors


def collect_scan_files(project_root: Path, extra_files: list[str]) -> list[Path]:
    files: list[Path] = []
    instructions = project_root / INSTRUCTIONS_RELATIVE
    if instructions.is_file():
        files.append(instructions)
    files.extend(sorted(project_root.glob(AGENTS_GLOB)))
    for raw in extra_files:
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = project_root / candidate
        files.append(candidate)
    return files


def static_check(project_root: Path, extra_files: list[str]) -> dict:
    """Contrôle statique bloquant. Retourne un rapport structuré."""
    manifest_path = project_root / MANIFEST_RELATIVE
    patterns, manifest_errors = load_manifest(manifest_path)
    violations: list[dict] = [{"kind": "manifest", "detail": err} for err in manifest_errors]
    occurrences: dict[str, int] = {}
    checked_files: list[str] = []
    artifact_cache: dict[str, bool] = {}

    for file_path in collect_scan_files(project_root, extra_files):
        if not file_path.is_file():
            violations.append({"kind": "scan", "detail": f"Fichier à scanner introuvable: {file_path}"})
            continue
        try:
            rel = str(file_path.relative_to(project_root))
        except ValueError:
            rel = str(file_path)
        checked_files.append(rel)
        for lineno, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            for match in SIGLE_PATTERN.finditer(line):
                sigle = match.group(1)
                occurrences[sigle] = occurrences.get(sigle, 0) + 1
                entry = patterns.get(sigle)
                where = f"{rel}:{lineno}"
                if entry is None:
                    violations.append(
                        {
                            "kind": "unknown-sigle",
                            "sigle": sigle,
                            "location": where,
                            "detail": f"Sigle {sigle} absent du manifeste de gouvernance ({where}).",
                        }
                    )
                    continue
                status = str(entry.get("status") or "")
                if status == "executable":
                    artifact = str(entry.get("artifact") or "")
                    if artifact not in artifact_cache:
                        artifact_cache[artifact] = bool(artifact) and (project_root / artifact).is_file()
                    if not artifact_cache[artifact]:
                        violations.append(
                            {
                                "kind": "missing-artifact",
                                "sigle": sigle,
                                "location": where,
                                "detail": (
                                    f"Sigle {sigle} déclaré 'executable' mais l'artefact "
                                    f"{artifact or '∅'} est introuvable ({where})."
                                ),
                            }
                        )
                elif status == "retired" and not RETIREMENT_PATTERN.search(line):
                    violations.append(
                        {
                            "kind": "retired-sigle",
                            "sigle": sigle,
                            "location": where,
                            "detail": (
                                f"Sigle retiré {sigle} présent hors phrase de retrait ({where}) — "
                                "protocole-papier réinjecté."
                            ),
                        }
                    )

    # Déduplication des violations 'missing-artifact' répétées (une par sigle suffit).
    seen: set[tuple] = set()
    deduped: list[dict] = []
    for violation in violations:
        key = (violation["kind"], violation.get("sigle"), violation.get("location"))
        if violation["kind"] == "missing-artifact":
            key = (violation["kind"], violation.get("sigle"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(violation)

    return {
        "checked_files": checked_files,
        "occurrences": occurrences,
        "violations": deduped,
        "ok": not deduped,
    }


def parse_ts(raw: str) -> datetime | None:
    try:
        return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def scan_events(events_path: Path) -> tuple[dict[str, datetime], datetime | None]:
    """Streame le journal safety-gate en ne gardant que hookId -> dernier ts.

    Lecture ligne à ligne : le fichier (plusieurs Mo) n'est jamais chargé en
    mémoire, et seuls hookId/ts sont conservés.
    """
    last_seen: dict[str, datetime] = {}
    last_overall: datetime | None = None
    if not events_path.is_file():
        return last_seen, last_overall
    with events_path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            hook_id = event.get("hookId")
            ts = parse_ts(str(event.get("ts") or ""))
            if not hook_id or ts is None:
                continue
            previous = last_seen.get(hook_id)
            if previous is None or ts > previous:
                last_seen[hook_id] = ts
            if last_overall is None or ts > last_overall:
                last_overall = ts
    return last_seen, last_overall


def dynamic_check(project_root: Path, window_days: int, now: datetime) -> dict:
    """Contrôle dynamique non bloquant : hooks enforced sans événement récent."""
    warnings: list[str] = []
    registry_path = project_root / REGISTRY_RELATIVE
    events_path = project_root / EVENTS_RELATIVE

    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        hooks = registry.get("hooks", {})
        assert isinstance(hooks, dict)
    except (OSError, json.JSONDecodeError, AssertionError):
        return {"warnings": [f"Registre hooks illisible: {registry_path}"], "enforced": [], "dormant": []}

    enforced = sorted(h for h, entry in hooks.items() if isinstance(entry, dict) and entry.get("mode") == "enforced")
    last_seen, last_overall = scan_events(events_path)
    cutoff = now - timedelta(days=window_days)

    dormant: list[str] = []
    for hook_id in enforced:
        ts = last_seen.get(hook_id)
        if ts is None or ts < cutoff:
            dormant.append(hook_id)

    if enforced and len(dormant) == len(enforced):
        enforced_ts = [last_seen[h] for h in enforced if h in last_seen]
        last_enforced = max(enforced_ts).strftime("%Y-%m-%d") if enforced_ts else "jamais"
        overall = last_overall.strftime("%Y-%m-%d") if last_overall else "jamais"
        warnings.append(
            f"Canal gateway dormant pour les hooks enforced : {len(enforced)}/{len(enforced)} hooks "
            f"'enforced' sans événement sur {window_days} jours. Dernier événement enforced : "
            f"{last_enforced} ; dernier événement du journal (tous modes) : {overall}. "
            "Le runtime actuel ne joue pas ce canal — la promesse 'enforced' n'est pas exercée."
        )
    else:
        for hook_id in dormant:
            ts = last_seen.get(hook_id)
            last = ts.strftime("%Y-%m-%d") if ts else "jamais"
            warnings.append(
                f"Hook enforced dormant: {hook_id} — aucun événement sur {window_days} jours "
                f"(dernier événement: {last})."
            )

    return {"warnings": warnings, "enforced": enforced, "dormant": dormant}


def render_text(static_report: dict, dynamic_report: dict | None, window_days: int) -> str:
    lines: list[str] = []
    lines.append("== Contrôle statique (bloquant) : sigles de protocoles agentiques ==")
    lines.append(f"Fichiers scannés : {len(static_report['checked_files'])}")
    if static_report["occurrences"]:
        summary = ", ".join(f"{sigle}={count}" for sigle, count in sorted(static_report["occurrences"].items()))
        lines.append(f"Occurrences : {summary}")
    else:
        lines.append("Occurrences : aucune")
    if static_report["ok"]:
        lines.append("OK — chaque sigle est gouverné par le manifeste (artefact présent ou retrait explicite).")
    else:
        lines.append(f"VIOLATIONS ({len(static_report['violations'])}) :")
        for violation in static_report["violations"]:
            lines.append(f"  [FAIL] {violation['detail']}")

    if dynamic_report is not None:
        lines.append("")
        lines.append(f"== Contrôle dynamique (avertissement) : consommation des hooks enforced ({window_days} j) ==")
        lines.append(
            f"Hooks enforced : {len(dynamic_report['enforced'])} ; dormants : {len(dynamic_report['dormant'])}"
        )
        if dynamic_report["warnings"]:
            for warning in dynamic_report["warnings"]:
                lines.append(f"  [WARN] {warning}")
        else:
            lines.append("OK — tous les hooks enforced ont une activité récente.")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Garde-fou « fonctionnel = consommé » (lot 4 durcissement agentique)")
    parser.add_argument("--project-root", type=Path, default=default_project_root())
    parser.add_argument("--window-days", type=int, default=30, help="Fenêtre glissante du contrôle dynamique (jours)")
    parser.add_argument("--json", action="store_true", help="Sortie JSON structurée")
    parser.add_argument("--static-only", action="store_true", help="Ne joue que le contrôle statique (mode rapide hook)")
    parser.add_argument(
        "--extra-file",
        action="append",
        default=[],
        help="Fichier supplémentaire à inclure dans le scan statique (tests)",
    )
    args = parser.parse_args(argv)
    project_root = args.project_root.resolve()

    static_report = static_check(project_root, list(args.extra_file))
    dynamic_report = None if args.static_only else dynamic_check(project_root, args.window_days, datetime.now(timezone.utc))

    exit_code = 0 if static_report["ok"] else 1

    if args.json:
        payload = {
            "static": static_report,
            "dynamic": dynamic_report,
            "windowDays": args.window_days,
            "exitCode": exit_code,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    else:
        print(render_text(static_report, dynamic_report, args.window_days))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
