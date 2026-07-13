---
title: Guide d'utilisation — plan de durcissement agentique
description: Comment exécuter, suivre et arbitrer le plan de durcissement du 2026-07-12
author: Grimoire Master (session Claude)
date: 2026-07-12
---

## À quoi sert ce package

Vous voulez que chaque pattern agentique de la Forge soit soit réellement exécuté et mesuré, soit archivé. Ce package contient :

- `PLAN-durcissement-agentique.md` — les 6 lots, leurs dépendances, les critères d'acceptation et le tableau de suivi ;
- `DOC-TECHNIQUE-durcissement-agentique.md` — la base factuelle (sources, chiffres, verdicts par protocole) qui justifie chaque lot ;
- ce guide — l'ordre d'exécution et les points d'arbitrage.

## État au 2026-07-12

Les lots 0, 1, 4 et 5 sont exécutés ; le lot 2 est préparé (mécanisme validé en sandbox) ; le lot 3 attend le verdict de la campagne. Voir le tableau « Suivi » et le « Journal d'exécution » du plan.

## Ce qui reste à faire

1. **Arbitrer les décisions ouvertes du plan** : budget de la campagne (108 runs, 70 à 75 USD estimés — seul bloqueur du lot 2), re-câblage des hooks repo dans le runtime Claude Code, sort de terminal-guard côté produit kit, warning ou blocker à la compilation blueprint.
2. **Committer** : fait le 2026-07-12 — changements Forge via la branche `work/harmonisation-followup-20260703` vers `main`, pré-enregistrement kit via une branche dédiée vers `main` du kit (voir PR). Le pré-enregistrement doit rester committé AVANT le premier run de campagne — règle d'honnêteté du protocole.
3. **Lancer la campagne** (lot 2.4-2.5) après validation du budget : suivre la checklist de `grimoire-kit/evals/witnesses/web-app-todo/RUN-PROTOCOL.md` (smoke-run activated ~1 USD d'abord).
4. **Trancher le lot 3** au vu du rapport : conversion (3a) si l'activation forcée démontre un effet, archivage étendu (3b) sinon. La prose AORA/DCF/PIP restante dans `_grimoire-runtime/core/agents/grimoire-master.md` se règle à ce moment-là.

## Comment vérifier qu'un lot est terminé

Chaque item du plan porte un critère d'acceptation vérifiable. Règles transverses :

- Un hook nouveau ou modifié passe par le gateway, figure au registre et laisse `hooks-status` et `grimoire-hooks-smoke.sh` verts.
- Une purge documentaire se vérifie par recherche du sigle : zéro occurrence sans artefact exécutable associé.
- Un mécanisme converti se prouve par ses événements de trace, pas par sa documentation.
- Mettez à jour le tableau « Suivi » du plan à chaque clôture de lot.

## Points de vigilance

- **Ne réordonnez pas lot 4 avant lot 1** : le check statique échouerait sur les sigles encore présents et devrait être affaibli pour passer — ce qui le viderait de son sens.
- **Ne tirez aucune conclusion de la campagne hors du critère pré-enregistré** : l'analyse de sensibilité de juillet a montré qu'un choix de comptage post-hoc peut inverser le signe du résultat.
- **Staging chirurgical** pour tout commit côté `grimoire-kit` : jamais `git add -A` (artefacts générés non ignorés).
- Toute modification de ce package doit revalider les deux compagnons (`DOC-TECHNIQUE` et `GUIDE`) avant clôture, conformément à la convention du projet.

## Suivi de session en session

Le tableau « Suivi » du plan est la source de vérité de l'avancement. À la reprise d'une session, lisez dans l'ordre : le tableau de suivi, puis les décisions ouvertes restantes, puis le premier lot non bloqué.
