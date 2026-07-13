# C3 Step proof — Evidence Pack

## Summary

- Task id: `c3-step-proof`
- Profile: `governed`
- Outcome: chaque step d'un workflow declare doit laisser son artefact ; step saute detecte sans audit manuel.
- Final state: review

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Manifest etendu | `_grimoire/standard/workflow-state-manifest.yaml` | chantier C3 | states/transitions kit-valides + workflows/steps/expected_artifact + exemptions. |
| Checker | `scripts/workflow-step-check.py` | chantier C3 | Globs par step relatifs a l'instance, exclusion des matches des steps suivants, ordre opt-in. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Suppression d'artefact | retrait temporaire du GUIDE du package preuve-workflows | pass | ERROR avec identification du step guide-utilisation, puis OK apres restauration. |
| Etat courant | `scripts/workflow-step-check.py --project-root .` | pass | 11 instances verifiees, 8 exemptees, 0 erreur. |
| Compat kit | `bash scripts/run-standard.sh verify` | pass | Manifest accepte par _verify_workflow_state_manifest. |
