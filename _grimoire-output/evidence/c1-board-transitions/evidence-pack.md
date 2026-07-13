# C1 Board transitions — Evidence Pack

## Summary

- Task id: `c1-board-transitions`
- Profile: `governed`
- Outcome: journal append-only des transitions kanban, ecrit par hook, verifie par quality.
- Final state: review

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Logique record/check/reconcile | `scripts/board-transitions-log.py` | chantier C1 | Baseline, diff de statuts, rejeu, legalite des transitions selon evidence-gates. |
| Hook PostToolUse | `.github/hooks/scripts/grimoire-board-transitions.sh` | chantier C1 | Fail-open, filtre task-board.yaml, emission d'event ledger. |
| Manifest hook | `.github/hooks/grimoire-board-transitions.json` | chantier C1 | Route via grimoire-hook-gateway.sh, timeout 15s. |
| Registre de promotion | `_grimoire-runtime/_config/hook-safety-registry.json` | chantier C1 | Entree grimoire-board-transitions en mode shadow, digest stampe. |
| Journal reel | `_grimoire-runtime/_memory/board-transitions.jsonl` | hook via gateway | Baseline r7-r10 posee par invocation gateway reelle. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Sandbox record/check | `scripts/board-transitions-log.py check` sur sandbox | pass | Saut de gate ready vers accepted detecte en erreur, drift detecte puis reconcilie. |
| Invocation gateway | payload PostToolUse simule via grimoire-hook-gateway.sh | pass | Baseline reelle journalisee, check OK sur le board courant. |
| Hooks smoke | `.github/hooks/scripts/grimoire-hooks-smoke.sh` | pass | Manifest valide, syntaxe bash, registre inspecte. |
