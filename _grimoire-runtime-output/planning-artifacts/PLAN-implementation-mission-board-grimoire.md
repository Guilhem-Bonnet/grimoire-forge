# Plan d'Implementation — Mission Board Grimoire

> Projet : **Grimoire**
> Statut : **plan d'execution canonique**
> Sources : [SPEC-mission-board-grimoire.md](./SPEC-mission-board-grimoire.md), [CONTRAT-mission-board-grimoire.md](./CONTRAT-mission-board-grimoire.md), [MATRICE-verification-mission-board-grimoire.md](./MATRICE-verification-mission-board-grimoire.md), [WIREFRAMES-mission-board-grimoire.md](./WIREFRAMES-mission-board-grimoire.md)

---

## 1. Objectif

Transformer le package `Mission Board` en plan d'implementation unique, ordonne, testable et directement executable pour les surfaces runtime et board de Grimoire.

Le but produit n'est pas de creer un nouveau kanban "intelligent". Le but est de fournir un control plane visuel, causal et frugal en contexte, qui reste aligne sur le `Mission Ledger`, la `Verification Queue`, les `Workflow Instances` et le `Session Lineage`.

## 2. Priorites normatives

- **Canonical state first** : le board ne porte pas son etat primaire.
- **Evidence before completion** : aucune cloture sans preuve et verdict.
- **Memory, context, tokens first** : progressive disclosure obligatoire, pas de transcript brut dans les projections.
- **Deterministic routing** : le routage est versionne, explicable et surchargeable.
- **No silent stall** : stale, blocked, escalated et quarantined sont visibles et actionnables.
- **Board as command surface** : les interactions UI emettent des commandes runtime, elles n'ecrivent pas directement l'etat final.

## 3. Landing zones cibles

| Nature | Landing zone cible |
| --- | --- |
| Schemas runtime | `grimoire-kit/apps/grimoire-game/src/contracts/schemas.ts` |
| Events runtime | `grimoire-kit/apps/grimoire-game/src/contracts/events.ts` |
| Etat et projections board | `grimoire-kit/apps/grimoire-game/src/state/board-view.ts`, `kanban-view.ts`, `task-view.ts`, `mission-ledger-view.ts` |
| Verification et supervision | `verification-queue-view.ts`, `verification-view.ts`, `supervision-view.ts` |
| Lineage et archive | `session-lineage-view.ts`, `library-view.ts`, `library-memory-view.ts` |
| Tests contracts | `grimoire-kit/apps/grimoire-game/tests/contracts/` |
| Tests integration et e2e | `grimoire-kit/apps/grimoire-game/tests/integration/` |

## 4. Slices d'implementation

### Slice 0 - Contracts et evenements

**But** : rendre le runtime capable de parler la langue du `Mission Board`.

**Travaux** :

- ajouter `MissionTaskSchema`, `RoutingDecisionSchema`, `BoardCommandEnvelopeSchema` et `BoardCardProjectionSchema` ;
- ajouter les events `MISSION_TASK_STATE`, `MISSION_ROUTING_DECISION`, `MISSION_BOARD_COMMAND_DECISION`, `MISSION_VERIFICATION_STATE`, `MISSION_SUPERVISION_STATE` ;
- garantir la compatibilite additive avec les contracts existants.

**Gate** : payloads valides et invalides testes, sans regression sur les schemas existants.

### Slice 1 - Mapping canonique et projections board

**But** : projeter l'etat du ledger et du runtime dans les colonnes du board sans double source de verite.

**Travaux** :

- definir le predicate exact des colonnes ;
- alimenter `board-view.ts`, `kanban-view.ts`, `task-view.ts` depuis le canon ;
- brancher `mission-ledger-view.ts` comme reference de comparaison ;
- garantir l'idempotence et le replay.

**Gate** : le meme flux d'evenements reconstruit la meme projection.

### Slice 2 - Routeur et hook plane

**But** : faire de l'auto-assignation un mecanisme fiable et traçable.

**Travaux** :

- implementer la matrice de routage minimale ;
- exposer rationale et override ;
- brancher les hooks sur les evenements canoniques, pas sur l'UI ;
- gerer `preview` et `deny` pour les commandes sensibles.

**Gate** : chaque decision de routage et chaque refus de commande sont explicables.

### Slice 3 - Verification, closure guard et supervision

**But** : interdire les clotures trompeuses et traiter les stalls comme incidents.

**Travaux** :

- brancher `verification-queue-view.ts` et `verification-view.ts` sur les verdicts ;
- implementer le `closure guard` de task et de mission ;
- brancher `supervision-view.ts` sur stale, escalated et quarantined ;
- ajouter `nextAction` sur incidents critiques.

**Gate** : aucun `done` ni `mission completed` hors conditions canoniques.

### Slice 4 - Rooms, drawer et progressive disclosure

**But** : livrer la valeur operatoire visible sans exploser le contexte.

**Travaux** :

- implementer `Intake Desk`, `War Room`, `Workshop`, `Branch Finisher`, `Seance Archive`, `Watchtower` comme vues ou modes sur des read models existants ou adjacents ;
- livrer la carte compacte et le dossier lateral ;
- appliquer la discipline `L1/L2/L3` sur les surfaces ;
- interdire les deep fetch implicites.

**Gate** : une mission dense reste pilotable sans transcript ni drawer surcharges par defaut.

### Slice 5 - Fin de lot et evidence package

**But** : cloturer le front `Mission Board` avec preuves et non-regression.

**Travaux** :

- produire la suite de tests complete ;
- compiler la matrice de verification et l'evidence pack ;
- verifier la coherence board <-> ledger <-> verification <-> supervision ;
- controler la conformite aux wireframes et a la grammaire visuelle.

**Gate** : le scenario e2e nominal et les scenarios negatifs passent avec preuves rejouables.

## 5. Ordre recommande

1. Slice 0
2. Slice 1
3. Slice 2
4. Slice 3
5. Slice 4
6. Slice 5

## 6. Sequence de fichiers recommandees

| Lot | Fichiers cibles |
| --- | --- |
| Contracts | `src/contracts/schemas.ts`, `src/contracts/events.ts` |
| Projection board | `src/state/board-view.ts`, `src/state/kanban-view.ts`, `src/state/task-view.ts`, `src/state/mission-ledger-view.ts` |
| Verification et supervision | `src/state/verification-queue-view.ts`, `src/state/verification-view.ts`, `src/state/supervision-view.ts` |
| Archive et lineage | `src/state/session-lineage-view.ts`, `src/state/library-view.ts`, `src/state/library-memory-view.ts` |
| Tests | `tests/contracts/*`, `tests/integration/*` |

## 7. Couverture verification obligatoire

- validation schema des payloads canoniques ;
- replay stable des projections ;
- routage deterministe et overrideable ;
- refus explicite de cloture sans verification ;
- stale detection et escalation ;
- progressive disclosure respectee ;
- read models board coherents avec ledger et verification queue.

## 8. Red flags de livraison

- une carte ou une colonne stockee comme etat primaire ;
- un drag and drop qui change l'etat sans commande enveloppee ;
- un drawer qui charge tout le lineage a l'ouverture ;
- un routeur sans rationale ;
- un `done` sans verification acceptee ;
- une mission parente close alors qu'un enfant requis reste ouvert.

## 9. Definition of Done du plan

- les contracts runtime existent et sont testes ;
- les projections board sont derivees et rejouables ;
- le routeur est deterministe, overrideable et trace ;
- la verification et la supervision verrouillent la realite ;
- les rooms principales existent et respectent la discipline de contexte ;
- les preuves de non-regression sont rattachees au package final.
