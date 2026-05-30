---
title: Contrat runtime - Mission Board Grimoire
description: Contrat additif pour tasks canoniques, decisions de routage, commandes board, projections de cartes et discipline de contexte.
author: GitHub Copilot
date: 2026-04-16
---

## But

Donner une descente technique concrete au `Mission Board` Grimoire, compatible avec les surfaces runtime existantes de `grimoire-kit/apps/grimoire-game`.

Ce document ne decrit pas une UI libre. Il decrit le contrat interne cible pour :

- porter un backlog natif sans etat parallele UI ;
- brancher le board sur le `Mission Ledger`, les `Workflow Instances`, la `Verification Queue` et la `Supervision Chain` ;
- borner les commandes, le routage, la cloture et la reprise ;
- appliquer une discipline stricte de memoire, contexte et tokens.

## Sources techniques du package runtime

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
- `grimoire-kit/apps/grimoire-game/src/state/runtime-dashboard-view.ts`

## Regles de compatibilite

- Le board reste une projection du runtime canonique ;
- Les ajouts presentes ici sont additifs tant qu'ils n'imposent pas une redefinition globale des contracts existants ;
- Toute mutation board passe par une commande enveloppee, jamais par une simple interaction UI ;
- Toute projection du board doit etre reconstructible depuis les etats et evenements canoniques ;
- Les payloads board ne transportent jamais un transcript complet par defaut.

## 1. Objet `MissionTask`

Schema machine-readable de reference : `contracts/mission-task.schema.json`

### Regles d'usage `MissionTask`

- Une task doit toujours avoir `taskId`, `missionId`, `requestId`, `idempotencyKey`, `type`, `complexity`, `evidenceProfile` et `acceptanceCriteria`.
- `recipeRef`, `workflowInstanceId`, `verificationRef` et `evidenceRefs` restent secondaires mais normaux dans la vie de la task.
- `done` n'est valide que si la facette `verification` est `accepted`.

## 2. Objet `RoutingDecision`

Schema machine-readable de reference : `contracts/routing-decision.schema.json`

### Regles d'usage `RoutingDecision`

- Toute decision porte une `rationale[]` lisible.
- Toute surcharge operateur preserve la decision precedente et ajoute un nouvel episode causal.
- La decision est fondee sur `type`, `complexity`, `severity`, `evidenceProfile`, `policyPack` et `flowHint` eventuel.

## 3. Objet `BoardCommandEnvelope`

Schema machine-readable de reference : `contracts/board-command-envelope.schema.json`

### Commandes autorisees en V1

- `create_task`
- `qualify_task`
- `approve_route`
- `override_route`
- `start_execution`
- `record_checkpoint`
- `request_verification`
- `accept_verification`
- `reject_verification`
- `block_task`
- `unblock_task`
- `escalate_task`
- `close_task`
- `close_mission`

### Regles d'usage `BoardCommandEnvelope`

- Toute commande porte `requestId` et `idempotencyKey`.
- Toute commande peut etre refusee avec raison explicite.
- `preview=true` est la norme pour les actions sensibles et les actions a fort impact de contexte.

## 4. Objet `BoardCardProjection`

Schema machine-readable de reference : `contracts/board-card-projection.schema.json`

### Regles d'usage `BoardCardProjection`

- La carte ne contient qu'un resume utile au pilotage.
- Les champs lourds vivent hors projection et sont recuperees a la demande.
- Les colonnes sont derivees ; elles ne sont pas stockees comme autorite metier.

## 5. Events cibles a ajouter ou enrichir

### 5.1 Event `MISSION_TASK_STATE`

```typescript
const MissionTaskStateEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('MISSION_TASK_STATE'),
  task: MissionTaskSchema,
  meta: EventMetaSchema
}).strict();
```

### 5.2 Event `MISSION_ROUTING_DECISION`

```typescript
const MissionRoutingDecisionEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('MISSION_ROUTING_DECISION'),
  decision: RoutingDecisionSchema,
  meta: EventMetaSchema
}).strict();
```

### 5.3 Event `MISSION_BOARD_COMMAND_DECISION`

```typescript
const MissionBoardCommandDecisionEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('MISSION_BOARD_COMMAND_DECISION'),
  envelope: BoardCommandEnvelopeSchema,
  decision: z.enum(['ALLOW', 'DENY', 'DEFER', 'DEGRADE']),
  reason: z.string().min(1),
  meta: EventMetaSchema
}).strict();
```

### 5.4 Event `MISSION_VERIFICATION_STATE`

```typescript
const MissionVerificationStateEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('MISSION_VERIFICATION_STATE'),
  taskId: z.string().min(1),
  verificationRef: z.string().min(1),
  verificationState: z.enum(['queued', 'verifying', 'accepted', 'rejected', 'needs_work']),
  evidenceRefs: z.array(z.string().min(1)).default([]),
  meta: EventMetaSchema
}).strict();
```

### 5.5 Event `MISSION_SUPERVISION_STATE`

```typescript
const MissionSupervisionStateEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('MISSION_SUPERVISION_STATE'),
  taskId: z.string().min(1),
  supervisionState: z.enum(['healthy', 'stale', 'escalated', 'quarantined']),
  reason: z.string().min(1),
  nextAction: z.string().min(1).optional(),
  meta: EventMetaSchema
}).strict();
```

## 6. Discipline memoire, contexte et tokens

### 6.1 Regle generale

Le board optimise la lecture causale avec **progressive disclosure**. Le niveau de contexte transporte doit rester proportionnel a la tache de l'utilisateur.

### 6.2 Trois couches

| Couche | Usage | Donnees exposees |
| --- | --- | --- |
| `L1 Card` | lecture du board | titre, statuts, badges, counts, lane, dernier evenement |
| `L2 Drawer` | decision operatoire | acceptance criteria, rationale, refs, checkpoint recent, evidence gap |
| `L3 Deep Fetch` | investigation | lineage detaille, preuves, trace refs, historique complet |

### 6.3 Regles non negociables

- Aucun transcript brut en projection de carte ;
- Aucun transcript brut dans le drawer par defaut ;
- Toute vue profonde se fait par fetch explicite et reference, pas par duplication ;
- Les reviews, traces et preuves sont references par identifiants et resumes, puis dereferencees a la demande ;
- Toute action de routage doit rester comprehensible sans ouvrir un transcript externe.

## 7. Projections attendues dans les vues runtime

| Vue | Lecture minimale attendue |
| --- | --- |
| `board-view` | colonnes derivees, ordre de lecture par mission, badges de causalite |
| `kanban-view` | projection synthetique des colonnes et drag restrint aux commandes preview |
| `task-view` | detail complet d'une task et commandes autorisees |
| `mission-ledger-view` | lecture canonique et comparaison avec la projection board |
| `verification-queue-view` | file de verification et reasons de refus |
| `supervision-view` | stale, escalated, quarantined, nextAction |
| `session-lineage-view` | reprise des episodes et reouvertures |

## 8. Regles non negociables

- Le board ne sait rien que le control plane ignore.
- Toute commande est journalisee et rejouable.
- Toute decision de routage est explicable.
- Toute task stale doit produire un signal canonique.
- Toute cloture sans verification acceptee est refusee.

## 9. Mapping direct du package final

| Artefact | Role |
| --- | --- |
| [SPEC-mission-board-grimoire.md](./SPEC-mission-board-grimoire.md) | cadre produit et systeme |
| [ADR-007-mission-board-control-plane-causal.md](./ADR-007-mission-board-control-plane-causal.md) | decision directrice |
| `contracts/mission-task.schema.json` | schema task canonique |
| `contracts/routing-decision.schema.json` | schema de routage |
| `contracts/board-command-envelope.schema.json` | schema commandes |
| `contracts/board-card-projection.schema.json` | schema carte compacte |
