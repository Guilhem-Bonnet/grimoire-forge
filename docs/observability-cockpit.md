# Cockpit d'observabilite gouverne

Le cockpit Forge est une projection lisible des artefacts gouvernes. Il aide a diagnostiquer la memoire, les gates, les taches, les preuves et les scores, mais il ne modifie jamais l'etat canonique.

## Sources autorisees

Les entrees sont declarees dans `_grimoire/standard/observability-policy.yaml` :

- `task-board.yaml` pour les statuts, blockers et references de preuves ;
- `memory-policy.yaml` pour le contrat Memory OS ;
- `compliance-score.yaml` pour les dimensions et seuils ;
- `runtime-journal.jsonl` pour les evenements d'execution ;
- `evidence-pack.md` pour les validations et gaps acceptes.

## Vues minimales R10

| Vue | Role | Source de verite |
|---|---|---|
| Memory OS health | Exposer hot/semantic/graph/sidecar/legacy et les degradations | `memory-policy.yaml` + events + evidence |
| Task and evidence overlay | Voir les taches, statuts et preuves manquantes | `task-board.yaml` + evidence packs |
| Governance status | Suivre score, gates, risques et waivers | `compliance-score.yaml` + gates + evidence |

## Regle de securite

Les exports cockpit doivent etre regenerables, relus comme des preuves, et expurges des secrets. Toute mutation doit revenir aux artefacts sources ou aux commandes standard, jamais au rapport cockpit lui-meme.
