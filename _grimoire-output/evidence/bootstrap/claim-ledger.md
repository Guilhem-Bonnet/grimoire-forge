# Agentic Claim Ledger

Une affirmation sans preuve reste une hypothèse. Ce registre relie chaque
affirmation qui pèse sur une décision ou une livraison à ce qui la prouve.

- Task id: bootstrap (manifeste du standard) — affirmations du cycle du 2026-09-03
- Profile: governed

## Claims

| ID | Affirmation | Type | Source ou preuve | Statut | Confiance | Décision |
|---|---|---|---|---|---|---|
| CL-001 | La Forge exécute la release publiée 3.37.0, pas un établi | fait | `pip show grimoire-kit` → Version 3.37.0, Location .venv (plus d'editable) | prouvé | élevée | utiliser |
| CL-002 | La jambe Windows des tests d'outils est verte et bloquante | résultat | run 33808425204 (#257) et jambe Windows de #255 : pass ; `continue-on-error` retiré par #259 (54aed9ff) | prouvé | élevée | utiliser |
| CL-003 | Les seize tests Windows de #231 échouent encore | hypothèse | log Windows de #256 : aucun `FAILED tests/test_init_commands` — ils sont sautés par `requires_bash` sous win32 | contredit | élevée | rejeter |
| CL-004 | Le bridge du standard trace ses artefacts vers la norme | fait | `grimoire standard traceability --profile governed` → 38 exigences couvertes, 17 trous listés ; `traceability.yaml` 43 artefacts | prouvé | élevée | utiliser |
| CL-005 | La révision du standard est épinglée et à jour | fait | `grimoire standard upstream` → tête distante identique (53b2c342) | prouvé | élevée | utiliser |
| CL-006 | Le hook `SessionStart` injecte deux personas de triage sur la Forge | fait | `grimoire-hook --event SessionStart` → persona concierge + directive ; `CLAUDE.md` charge grimoire-master | prouvé | élevée | vérifier |
| CL-007 | Chaque changement fusionné depuis v3.36.0 a son entrée de changelog | résultat | `scripts/check-changelog-release.py` sur main avant #260 : couverture OK (8 commits feat/fix) | prouvé | élevée | utiliser |
| CL-008 | Les 30 agents cartographiés servent | hypothèse | GRIMOIRE_TRACE.jsonl : 432 activations, 14 agents jamais activés, trace arrêtée le 2026-04-26 | hypothèse | faible | vérifier |

Types : `fait`, `hypothèse`, `résultat`, `décision`. Statuts : `prouvé`,
`hypothèse`, `contredit`. Confiance : `faible`, `moyenne`, `élevée`. Décision :
`utiliser`, `vérifier`, `rejeter`.

## Preuve minimale par type d'affirmation

| Type | Preuve minimale |
|---|---|
| Fichier ou code | chemin lu, diff ou extrait |
| Test | commande et résultat |
| API ou norme | contrat, documentation officielle ou code |
| Design | charte, design system, maquette ou validation |
| Sécurité | scan, règle, revue ou threat model |
| Mémoire | source originale, date, score, portée |
| Décision client | validation explicite ou ticket |

## Synthèse

| Question | Réponse |
|---|---|
| Affirmations bloquantes non prouvées | aucune ; CL-008 n'est pas bloquante |
| Contradictions détectées | CL-003 : l'issue #231 décrit un état antérieur au skip |
| Hypothèses acceptées temporairement | CL-008, jusqu'à branchement de la mesure d'activation côté Claude Code |
| Preuves à obtenir avant livraison | CL-006 : choisir `agents.entry` pour la Forge (master ou concierge) |
