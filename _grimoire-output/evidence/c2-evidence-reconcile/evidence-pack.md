# C2 Evidence reconcile — Evidence Pack

## Summary

- Task id: `c2-evidence-reconcile`
- Profile: `governed`
- Outcome: chaque claim des evidence packs est confronte au disque, aux depots git et aux events task-flow.
- Final state: review

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Reconciliateur | `scripts/evidence-reconcile.py` | chantier C2 | Refs du board, tokens des inventaires markdown, packs JSONL EvidenceService (digest sha256, correlation events). |
| Requalification r8 context | `_grimoire-output/context/r8-redis-adapter/context-bundle.yaml` | chantier C2 | Trou de gouvernance acte, contenu d'origine non reconstitue. |
| Requalification r8 decision | `_grimoire-output/decisions/r8-redis-adapter/decision-trace.yaml` | chantier C2 | Idem. |
| Requalification r7 | `_grimoire-output/evidence/r7-forge-kit-adoption/evidence-pack.md` | chantier C2 | Pack retro-qualifie, refs context et decision materialisees. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Detection reelle | premier run du reconciliateur | pass | 2 CONTRADICTED (refs r8 absentes en statut review) et 3 UNVERIFIABLE (r7) detectes avant requalification. |
| Etat final | `scripts/evidence-reconcile.py --project-root .` | pass | 34 VERIFIED, 0 UNVERIFIABLE, 0 CONTRADICTED. |
