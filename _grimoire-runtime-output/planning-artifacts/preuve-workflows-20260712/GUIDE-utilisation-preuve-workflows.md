# Guide d'utilisation — Package preuve-workflows

Compagnon d'usage du package `preuve-workflows-20260712`.

## Contenu du package

| Fichier | Rôle |
| --- | --- |
| `PLAN-preuve-workflows.md` | Plan de travail : 5 chantiers, séquencement, cartes kanban prêtes, risques |
| `DOC-TECHNIQUE-preuve-workflows.md` | Ancrages code, schémas de données, décisions d'architecture |
| `GUIDE-utilisation-preuve-workflows.md` | Ce document |

## Comment démarrer un chantier

1. Ouvrir `PLAN-preuve-workflows.md`, section du chantier visé.
2. Copier la carte kanban correspondante (section « Cartes kanban prêtes à
   intégrer ») dans `_grimoire/standard/task-board.yaml`.
3. Créer les trois refs de la carte (context bundle, decision trace, evidence
   pack) selon la convention `_grimoire-output/{context,decisions,evidence}/<task_id>/`.
4. Passer la carte en `ready` puis `in_progress` en respectant les gates de
   `evidence-gates.yaml`.
5. À la clôture, l'evidence pack doit satisfaire les critères d'acceptation
   listés dans le plan — et, dès que C2 est livré, passer la réconciliation.

## Ordre recommandé

C1 puis C2 puis C3 puis C5, avec C4 en parallèle calé sur la campagne
d'evals web-app-todo (bras « activé »). Ne pas démarrer C5 avant la livraison
de C3 : le golden run consomme le format du checker par step.

## Vérifications à chaque étape

- `npm run quality` reste vert après chaque livraison de chantier.
- `grimoire standard verify` reste vert depuis la racine de la Forge.
- Tout nouveau hook passe par `grimoire-hooks-smoke.sh` et démarre en
  mode `shadow`.

## Commandes opérationnelles (as-built)

Toutes depuis la racine de la Forge, avec `PY=grimoire-kit/.venv/bin/python` :

| Besoin | Commande |
| --- | --- |
| Vérifier la chaîne de preuve complète | `npm run quality` (section `6/6 Preuve`) |
| Cohérence journal/kanban + légalité des transitions | `$PY scripts/board-transitions-log.py --project-root . check` |
| Acter une édition manuelle du kanban (drift) | `$PY scripts/board-transitions-log.py --project-root . reconcile --session <id>` |
| Réconcilier les evidence packs | `$PY scripts/evidence-reconcile.py --project-root .` (`--strict` pour profil production) |
| Vérifier les steps des workflows déclarés | `$PY scripts/workflow-step-check.py --project-root .` |
| Capturer un golden run (instance auditée) | `$PY scripts/golden-run-diff.py --project-root . capture --workflow <id> --instance <dir>` |
| Diff d'un run contre le golden | `$PY scripts/golden-run-diff.py --project-root . diff --workflow <id> --instance <dir>` |
| Rapport d'engagement | `$PY scripts/engagement-log.py --project-root . report` |

Les journaux `board-transitions.jsonl` et `engagement.jsonl` vivent sous
`_grimoire-runtime/_memory/` : écrits par hooks uniquement, protégés du côté
agent par le memory-guard. Ne jamais les éditer à la main ; un drift du kanban
se résout par `reconcile`, qui le trace au lieu de le masquer.

Les hooks `grimoire-board-transitions` et `grimoire-engagement` sont en mode
`shadow` ; promotion par la task `grimoire: hooks-promote` après période
d'observation.

## Mise à jour du package

Toute modification du plan (périmètre, séquencement, décisions) doit
revalider les deux compagnons (`DOC-TECHNIQUE`, `GUIDE-utilisation`) avant
clôture, conformément à la convention des packages de livrables.
