#!/usr/bin/env python3
"""Preuve par step des workflows (chantier C3).

Lit _grimoire/standard/workflow-state-manifest.yaml et verifie, pour chaque
workflow declare, que chaque step a laisse son artefact attendu :
  - glob de step vide -> ERROR (step saute silencieusement) ;
  - ordre chronologique des steps viole (mtime) -> WARN (les mtimes sont une
    source d'ordre faible : copies et checkouts les reecrivent) ;
  - instance listee dans exempt_instances -> ignoree, comptee dans le rapport
    (dette actee, jamais silencieuse).

Les globs sont relatifs au dossier d'instance quand instance_glob est declare,
sinon relatifs a la racine projet. Exit 1 si au moins une erreur. Consomme par
npm run quality (section Preuve).
"""

from __future__ import annotations

import argparse
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

MANIFEST_REL = Path("_grimoire/standard/workflow-state-manifest.yaml")


def newest_mtime(matches: list[Path]) -> float:
    return max(p.stat().st_mtime for p in matches)


def check_steps(base: Path, steps: list[dict], label: str, errors: list[str], warnings: list[str], *, enforce_order: bool) -> None:
    previous_mtime: float | None = None
    previous_id = ""
    for index, step in enumerate(steps):
        step_id = str(step.get("id", "?"))
        pattern = str(step.get("expected_artifact", "")).strip()
        if not pattern:
            errors.append(f"{label}: step {step_id!r} sans expected_artifact")
            continue
        matches = [p for p in base.glob(pattern) if p.is_file()]
        # Un glob large (ex. *.md) ne doit pas capter les artefacts des steps
        # suivants, sinon la preuve d'un step vaut pour un autre.
        later = set()
        for later_step in steps[index + 1:]:
            later_pattern = str(later_step.get("expected_artifact", "")).strip()
            if later_pattern and later_pattern != pattern:
                later.update(p for p in base.glob(later_pattern) if p.is_file())
        matches = [p for p in matches if p not in later]
        if not matches:
            errors.append(f"{label}: step {step_id!r} sans artefact (glob `{pattern}` vide) — step saute ou livrable manquant")
            previous_mtime = None
            continue
        if enforce_order:
            mtime = newest_mtime(matches)
            if previous_mtime is not None and mtime < previous_mtime:
                warnings.append(f"{label}: artefact du step {step_id!r} anterieur au step {previous_id!r} (ordre mtime incoherent)")
            previous_mtime = mtime
            previous_id = step_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", type=Path)
    parser.add_argument("--workflow", default="", help="restreindre a un workflow id")
    args = parser.parse_args()
    root = args.project_root.resolve()

    if yaml_load is None:
        print("workflow-step-check: aucun loader YAML disponible", file=sys.stderr)
        return 1
    manifest_path = root / MANIFEST_REL
    if not manifest_path.is_file():
        print("workflow-step-check: manifest absent — OK (rien a verifier)")
        return 0

    manifest = yaml_load(manifest_path.read_text(encoding="utf-8")) or {}
    errors: list[str] = []
    warnings: list[str] = []
    checked = exempted = 0

    for workflow in manifest.get("workflows") or []:
        if not isinstance(workflow, dict):
            continue
        workflow_id = str(workflow.get("id", "?"))
        if args.workflow and workflow_id != args.workflow:
            continue
        steps = [s for s in workflow.get("steps") or [] if isinstance(s, dict)]
        if not steps:
            warnings.append(f"{workflow_id}: aucun step declare")
            continue
        instance_glob = str(workflow.get("instance_glob", "")).strip()
        exempt = {str(e) for e in workflow.get("exempt_instances") or []}
        # L'ordre mtime est une preuve faible (reeditions, checkouts) :
        # opt-in par workflow, le golden run (C5) porte la preuve d'ordre forte.
        enforce_order = bool(workflow.get("enforce_order"))
        if instance_glob:
            instances = sorted(p for p in root.glob(instance_glob) if p.is_dir())
            for instance in instances:
                if instance.name in exempt:
                    exempted += 1
                    continue
                checked += 1
                check_steps(instance, steps, f"{workflow_id}/{instance.name}", errors, warnings, enforce_order=enforce_order)
        else:
            checked += 1
            check_steps(root, steps, workflow_id, errors, warnings, enforce_order=enforce_order)

    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[ERROR] {error}")
    print(
        f"workflow-step-check: {checked} instance(s) verifiee(s), {exempted} exemptee(s) (dette actee), "
        f"{len(errors)} erreur(s), {len(warnings)} warning(s)"
    )
    if errors:
        print("workflow-step-check: ECHEC")
        return 1
    print("workflow-step-check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
