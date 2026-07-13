# C5 Golden run — Evidence Pack

## Summary

- Task id: `c5-golden-run`
- Profile: `governed`
- Outcome: referentiel de run audite, diff automatise des runs suivants.
- Final state: review

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Capture et diff | `scripts/golden-run-diff.py` | chantier C5 | Capture refusee si step vide ; diff structurel avec erreurs sur step degrade. |
| Referentiel | `_grimoire-runtime-output/test-artifacts/golden-runs/deliverable-package/golden.json` | capture C5 | Instance de reference preuve-workflows-20260712, sha256 par artefact. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Instance saine | diff contre retrieval-unifie-20260708 | pass | 0 erreur, 0 warning. |
| Run degrade | diff contre stigmergy-activation-20260707 | pass | 2 steps degrades detectes sans audit manuel, exit 1. |
