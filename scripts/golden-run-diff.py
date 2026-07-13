#!/usr/bin/env python3
"""Golden run — referentiel et diff des runs de workflow (chantier C5).

Deux modes :
  capture — fige le referentiel d'une instance auditee manuellement :
            pour chaque step du workflow (workflow-state-manifest.yaml),
            fichiers apparies, sha256 et taille. Stocke sous
            _grimoire-runtime-output/test-artifacts/golden-runs/<workflow>/golden.json
  diff    — compare une instance courante au referentiel : step sans artefact
            la ou le golden en avait -> ERROR ; famille d'artefacts amaigrie
            (moins de fichiers que le golden) -> WARN. Le contenu n'est pas
            compare (les slugs different d'une instance a l'autre) : c'est la
            STRUCTURE du run qui fait foi.

Procedure de rafraichissement : quand le workflow evolue (steps ajoutes ou
retires du manifest), re-auditer un run complet a la main puis relancer
capture. Le referentiel est versionne ; un diff du golden.json dans git
documente l'evolution du contrat.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
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

MANIFEST_REL = Path("_grimoire/standard/workflow-state-manifest.yaml")
GOLDEN_DIR_REL = Path("_grimoire-runtime-output/test-artifacts/golden-runs")


def load_workflow(root: Path, workflow_id: str) -> dict | None:
    manifest = yaml_load((root / MANIFEST_REL).read_text(encoding="utf-8")) or {}
    for workflow in manifest.get("workflows") or []:
        if isinstance(workflow, dict) and str(workflow.get("id")) == workflow_id:
            return workflow
    return None


def snapshot_instance(instance: Path, steps: list[dict]) -> dict:
    snapshot: dict = {"steps": {}}
    for step in steps:
        step_id = str(step.get("id", "?"))
        pattern = str(step.get("expected_artifact", "")).strip()
        files = []
        for path in sorted(instance.glob(pattern)):
            if path.is_file():
                data = path.read_bytes()
                files.append({
                    "name": path.name,
                    "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                })
        snapshot["steps"][step_id] = {"pattern": pattern, "files": files}
    return snapshot


def cmd_capture(root: Path, workflow_id: str, instance: Path) -> int:
    workflow = load_workflow(root, workflow_id)
    if workflow is None:
        print(f"golden-run: workflow {workflow_id!r} absent du manifest", file=sys.stderr)
        return 1
    steps = [s for s in workflow.get("steps") or [] if isinstance(s, dict)]
    snapshot = snapshot_instance(instance, steps)
    empty = [sid for sid, data in snapshot["steps"].items() if not data["files"]]
    if empty:
        print(f"golden-run capture: REFUS — steps sans artefact dans l'instance de reference : {empty}", file=sys.stderr)
        print("Un golden run doit etre un run complet audite ; completer l'instance d'abord.", file=sys.stderr)
        return 1
    golden = {
        "$schema": "grimoire-golden-run/v1",
        "workflow": workflow_id,
        "reference_instance": str(instance.relative_to(root)) if instance.is_relative_to(root) else str(instance),
        "captured_at": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "audit_statement": "Referentiel capture apres audit manuel de l'instance de reference.",
        **snapshot,
    }
    out = root / GOLDEN_DIR_REL / workflow_id / "golden.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(golden, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"golden-run capture: OK — {out.relative_to(root)}")
    return 0


def cmd_diff(root: Path, workflow_id: str, instance: Path) -> int:
    golden_path = root / GOLDEN_DIR_REL / workflow_id / "golden.json"
    if not golden_path.is_file():
        print(f"golden-run diff: aucun referentiel pour {workflow_id!r} — lancer capture d'abord", file=sys.stderr)
        return 1
    golden = json.loads(golden_path.read_text(encoding="utf-8"))
    workflow = load_workflow(root, workflow_id)
    if workflow is None:
        print(f"golden-run diff: workflow {workflow_id!r} absent du manifest", file=sys.stderr)
        return 1
    steps = [s for s in workflow.get("steps") or [] if isinstance(s, dict)]
    current = snapshot_instance(instance, steps)

    errors: list[str] = []
    warnings: list[str] = []
    golden_steps = golden.get("steps", {})
    for step_id, golden_data in golden_steps.items():
        current_files = current["steps"].get(step_id, {}).get("files", [])
        golden_count = len(golden_data.get("files", []))
        if golden_count and not current_files:
            errors.append(f"step {step_id!r}: le golden a {golden_count} artefact(s), le run courant zero — step degrade")
        elif len(current_files) < golden_count:
            warnings.append(f"step {step_id!r}: {len(current_files)} artefact(s) contre {golden_count} au golden")
    for step_id in current["steps"]:
        if step_id not in golden_steps:
            warnings.append(f"step {step_id!r}: absent du golden (manifest plus recent ?) — rafraichir le referentiel")

    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[ERROR] {error}")
    print(f"golden-run diff ({workflow_id}): {len(errors)} erreur(s), {len(warnings)} warning(s)")
    if errors:
        print("golden-run diff: ECHEC")
        return 1
    print("golden-run diff: OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("capture", "diff"):
        p = sub.add_parser(name)
        p.add_argument("--workflow", required=True)
        p.add_argument("--instance", required=True, type=Path)
    args = parser.parse_args()
    root = args.project_root.resolve()
    if yaml_load is None:
        print("golden-run: aucun loader YAML disponible", file=sys.stderr)
        return 1
    instance = args.instance if args.instance.is_absolute() else root / args.instance
    if args.command == "capture":
        return cmd_capture(root, args.workflow, instance)
    return cmd_diff(root, args.workflow, instance)


if __name__ == "__main__":
    raise SystemExit(main())
