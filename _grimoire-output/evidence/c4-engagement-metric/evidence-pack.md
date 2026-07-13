# C4 Engagement metric — Evidence Pack

## Summary

- Task id: `c4-engagement-metric`
- Profile: `governed`
- Outcome: signaux d'engagement des workflows journalises par hook, rapport agregeable pour la campagne d'evals.
- Final state: review

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Logique record/report | `scripts/engagement-log.py` | chantier C4 | Detection slash-command et prompt-mention depuis workflow-manifest.csv, rapport par artefact/canal/jour. |
| Hook UserPromptSubmit | `.github/hooks/scripts/grimoire-engagement.sh` | chantier C4 | Fail-open, aucune sortie active. |
| Manifest hook | `.github/hooks/grimoire-engagement.json` | chantier C4 | Route via gateway, timeout 15s. |
| Journal | `_grimoire-runtime/_memory/engagement.jsonl` | hook via gateway | Signaux test slash-command et prompt-mention journalises. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Invocation gateway | payload UserPromptSubmit simule | pass | 2 signaux journalises (dev-story slash-command, task-board mention), session identifiee. |
| Rapport | `scripts/engagement-log.py report` | pass | Agregation par artefact, canal et jour. |
