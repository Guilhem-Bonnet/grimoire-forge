---
title: Documentation technique - Mission Board Grimoire
description: Vue technique consolidee du Mission Board, de ses contrats, de ses read models, de ses hooks et de ses landing zones runtime.
author: GitHub Copilot
date: 2026-04-16
---

## Documentation technique — Mission Board Grimoire

## 1. Objet

Cette documentation technique consolide le package `Mission Board` sous un angle implementation-ready.

Elle ne remplace pas la spec, l'ADR, le contrat runtime ni le plan d'implementation. Elle les assemble pour repondre a la question suivante : **comment le Mission Board doit etre branche techniquement dans Grimoire sans devenir une source de verite parallele**.

## 2. Decision technique directrice

Le `Mission Board` est une **projection causale** du control plane, pas un kanban autonome.

Cela implique :

- les colonnes et cartes sont derivees des etats canoniques ;
- les actions UI emettent des commandes bornees ;
- les verdicts de verification et de supervision vivent hors UI ;
- la cloture est fail-closed ;
- les projections restent frugales en memoire, contexte et tokens.

## 3. Surfaces canoniques mobilisees

### Control plane

- [SPEC-mission-board-grimoire.md](./SPEC-mission-board-grimoire.md)
- [ADR-007-mission-board-control-plane-causal.md](./ADR-007-mission-board-control-plane-causal.md)
- [CONTRAT-mission-board-grimoire.md](./CONTRAT-mission-board-grimoire.md)

### Runtime cible

- `grimoire-kit/apps/grimoire-game/src/contracts/schemas.ts`
- `grimoire-kit/apps/grimoire-game/src/contracts/events.ts`
- `grimoire-kit/apps/grimoire-game/src/state/board-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/kanban-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/task-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/mission-ledger-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/verification-queue-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/verification-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/supervision-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/session-lineage-view.ts`

## 4. Objets techniques de premier rang

### `MissionTask`

Objet canonique de travail pilote par le board.

Responsabilites :

- porter l'intention utilisateur ;
- fixer le niveau de preuve attendu ;
- raccorder routing, workflow instance, verification et evidence refs ;
- rendre la cloture testable.

Schema : `contracts/mission-task.schema.json`

### `RoutingDecision`

Objet de decision explicable.

Responsabilites :

- materialiser `lane`, `recipeRef`, `verificationProfile` et `reviewMode` ;
- exposer une `rationale[]` lisible ;
- conserver la causalite des overrides.

Schema : `contracts/routing-decision.schema.json`

### `BoardCommandEnvelope`

Enveloppe unique des commandes board.

Responsabilites :

- garantir `requestId`, `idempotencyKey` et `preview` ;
- permettre `ALLOW`, `DENY`, `DEFER` et `DEGRADE` cote policy ;
- faire du board une surface de commande plutot qu'une surface d'ecriture libre.

Schema : `contracts/board-command-envelope.schema.json`

### `BoardCardProjection`

Projection compacte de pilotage.

Responsabilites :

- afficher l'etat operatoire ;
- rester lisible a faible charge de contexte ;
- deleguer les details lourds au drawer et au deep fetch.

Schema : `contracts/board-card-projection.schema.json`

## 5. Plane d'evenements cible

Le board s'alimente sur un plan d'evenements explicite :

- `MISSION_TASK_STATE`
- `MISSION_ROUTING_DECISION`
- `MISSION_BOARD_COMMAND_DECISION`
- `MISSION_VERIFICATION_STATE`
- `MISSION_SUPERVISION_STATE`

Chaque evenement doit rester :

- serialisable ;
- rejouable ;
- lisible sans transcript complet ;
- exploitable par les read models board, verification et supervision.

## 6. Regles de projection

### Colonnes

Les colonnes ne sont jamais stockees comme autorite metier. Elles sont derivees de la combinaison :

- `lifecycle`
- `qualification`
- `assignment`
- `execution`
- `verification`
- `supervision`

### Drawer et deep fetch

Le board suit une lecture en trois niveaux :

- `L1`: carte compacte ;
- `L2`: drawer decisionnel ;
- `L3`: fetch profond sur demande.

Interdictions :

- pas de transcript brut sur la carte ;
- pas de transcript brut par defaut dans le drawer ;
- pas de deep fetch implicite au chargement du board.

## 7. Hooks et garde documentaire

Le package impose maintenant deux compagnons documentaires explicites pour tout livrable stable de planning artifacts :

- `DOC-TECHNIQUE-<slug>.md`
- `GUIDE-utilisation-<slug>.md`

Le controle se fait dans la policy hook, cote `grimoire-kit/framework/tools/guardrail-policy.py` :

- `PostToolUse` recontrole les compagnons sur les packages modifies et memorise les fichiers recents de l'activite ;
- `Stop` bloque la cloture si un livrable touche n'a pas sa doc technique et son guide d'utilisation, ou si ces deux compagnons ne sont plus synchronises avec les fichiers modifies du package.

## 8. Verification technique minimale

La mise en oeuvre technique n'est acceptable que si les preuves suivantes existent :

- schemas valides ;
- projections rejouables ;
- routage explicable ;
- `close_task` refuse sans verification acceptee ;
- `close_mission` refuse si un enfant requis reste ouvert ;
- stale, escalation et quarantine visibles dans `supervision-view` ;
- charge de contexte bornee sur la carte et le drawer.

References :

- [PLAN-implementation-mission-board-grimoire.md](./PLAN-implementation-mission-board-grimoire.md)
- [MATRICE-verification-mission-board-grimoire.md](./MATRICE-verification-mission-board-grimoire.md)
- [SUITE-tests-mission-board-grimoire.md](./SUITE-tests-mission-board-grimoire.md)

## 9. Lecture rapide pour implementation

1. Etendre les contracts et events.
2. Deriver les projections board depuis le canon.
3. Brancher le routeur et les decisions preview/deny.
4. Brancher verification et closure guard.
5. Brancher supervision stale/escalation.
6. Finir par les rooms et la frugalite de contexte.

## 10. Non-objectifs de cette documentation

- confirmer que l'implementation code existe deja ;
- remplacer la spec source ;
- servir de backlog ;
- decrire une UX speculative hors read models canoniques.
