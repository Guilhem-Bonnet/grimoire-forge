---
title: Contrat runtime - Guardrails agentiques
description: Spec additive pour surfaces d'execution, verification chain et enveloppe canonique pilote.
author: GitHub Copilot
date: 2026-04-09
---

## But

Donner une descente technique concrete aux tickets `GAME-TKT-037`, `GAME-TKT-038` et `GAME-TKT-039`, compatible avec le runtime `v1` actuel de `grimoire-kit/apps/grimoire-game`.

Ce document ne decrit pas une conformite normative. Il decrit le contrat interne cible du projet pour:

- gouverner les surfaces d'execution,
- fiabiliser la verification,
- piloter une enveloppe canonique bornee.

## Sources techniques du package runtime

- `grimoire-kit/apps/grimoire-game/src/contracts/schemas.ts`
- `grimoire-kit/apps/grimoire-game/src/contracts/events.ts`
- `grimoire-kit/apps/grimoire-game/src/state/game-state.ts`
- `grimoire-kit/apps/grimoire-game/src/state/verification-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/audit-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/session-view.ts`

## Regles de compatibilite

- Le protocole courant `v1` reste la source de verite de compatibilite descendante.
- Les ajouts presentes ici sont additifs tant qu'ils ne remplacent pas les champs deja consommes.
- Toute nouvelle information critique doit pouvoir etre projettee soit dans `meta`, soit dans un event dedie sans casser les parseurs existants.
- Le pilote d'enveloppe canonique n'a pas le droit d'imposer une migration globale avant validation sur le panier borne.

## 1. Metadata minimale commune

### 1.1 Objet `EventMeta`

`EventMeta` est l'objet minimal rattache aux activations, decisions de verification et projections read-only.

```typescript
const EventMetaSchema = z
  .object({
    source: z.enum(['ui', 'runtime', 'adapter', 'verification', 'security', 'replay', 'spectator']),
    actor: z
      .object({
        kind: z.enum(['user', 'orchestrator', 'agent', 'system', 'spectator']),
        id: z.string().min(1),
        role: z.enum(['orchestrator', 'agent', 'spectator']).optional()
      })
      .strict(),
    correlationId: z.string().min(1),
    traceId: z.string().min(1).optional(),
    sessionId: z.string().min(1).optional(),
    taskId: z.string().min(1).optional(),
    surfaceId: z.string().min(1).optional(),
    verificationRef: z.string().min(1).optional()
  })
  .strict();
```

### 1.2 Regle d'usage

- `correlationId` est obligatoire pour toute activation de surface et toute transition critique.
- `traceId` devient obligatoire des qu'une transition alimente `verification-view`, `audit-view` ou `session-view`.
- `surfaceId` devient obligatoire pour toute action sur skill, plugin, power card, tool, hook ou noeud MCP activable.

## 2. Registre des surfaces d'execution

### 2.1 Objet `SurfaceExecutionRecord`

```typescript
const SurfaceExecutionRecordSchema = z
  .object({
    surfaceId: z.string().min(1),
    surfaceType: z.enum(['skill', 'plugin', 'power_card', 'tool', 'mcp', 'hook']),
    displayName: z.string().min(1),
    origin: z.string().min(1),
    trustStatus: z.enum(['trusted', 'review', 'restricted', 'blocked']),
    riskLevel: z.enum(['low', 'moderate', 'high', 'critical']),
    requiredPolicy: z
      .object({
        requiresApproval: z.boolean(),
        fileSystem: z.boolean(),
        network: z.boolean(),
        secrets: z.boolean(),
        exec: z.boolean(),
        configWrite: z.boolean()
      })
      .strict(),
    capabilities: z.array(z.enum(['fs', 'network', 'secrets', 'exec', 'config_write'])).default([]),
    owner: z.string().min(1).optional(),
    lastReviewedAt: z.string().min(1).optional(),
    notes: z.string().min(1).optional()
  })
  .strict();
```

### 2.2 Regles de gate

- `trustStatus=blocked` interdit toute activation.
- `origin` absent interdit toute activation.
- `requiredPolicy` absent interdit toute activation.
- Toute activation reussie ou refusee doit etre reportee dans `audit-view`.

## 3. Evenements cibles a ajouter ou enrichir

### 3.1 Client events mutateurs enrichis

Les events mutateurs existants peuvent etre etendus additivement avec `meta`.

```typescript
const MutatingClientMetaSchema = EventMetaSchema.extend({
  source: z.enum(['ui', 'runtime', 'adapter'])
}).strict();

const ConfigUpdateEventSchemaV1Plus = ConfigUpdateEventSchema.extend({
  meta: MutatingClientMetaSchema.optional()
}).strict();
```

Meme logique pour:

- `TASK_TRANSITION`
- `TASK_ASSIGN`
- `AGENT_STATUS_UPDATE`

### 3.2 Server event `VERIFICATION_GATE`

```typescript
const VerificationGateEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('VERIFICATION_GATE'),
  result: z.enum(['PASS', 'FAIL']),
  actionId: z.string().min(1),
  verificationRef: z.string().min(1),
  evidenceRefs: z.array(
    z
      .object({
        kind: z.enum(['test', 'log', 'coverage', 'artifact', 'screenshot']),
        ref: z.string().min(1)
      })
      .strict()
  ),
  controlsExecuted: z.array(z.string().min(1)).min(1),
  unmetControls: z.array(z.string().min(1)).default([]),
  meta: EventMetaSchema
}).strict();
```

### 3.3 Server event `SURFACE_POLICY_STATE`

```typescript
const SurfacePolicyStateEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('SURFACE_POLICY_STATE'),
  surface: SurfaceExecutionRecordSchema,
  decision: z.enum(['ALLOWED', 'DENIED']),
  reason: z.string().min(1),
  meta: EventMetaSchema
}).strict();
```

### 3.4 Server event `SECURITY_FINDING`

```typescript
const SecurityFindingEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('SECURITY_FINDING'),
  severity: z.enum(['CRITICAL', 'HIGH', 'MEDIUM', 'INFO']),
  owaspCategory: z.string().min(1),
  agenticSkillCategory: z.string().min(1).optional(),
  strideCategory: z.string().min(1).optional(),
  surfaceId: z.string().min(1).optional(),
  exploit: z.string().min(1),
  confidence: z.number().min(0).max(10),
  meta: EventMetaSchema
}).strict();
```

## 4. Chaine de verification orientee AIVS

### 4.1 Objet `VerificationChain`

```typescript
const VerificationChainSchema = z
  .object({
    actionId: z.string().min(1),
    traceId: z.string().min(1),
    taskId: z.string().min(1).optional(),
    verdict: z.enum(['PASS', 'FAIL']),
    controlsExecuted: z.array(z.string().min(1)).min(1),
    unmetControls: z.array(z.string().min(1)).default([]),
    evidenceRefs: z.array(z.string().min(1)).min(1),
    verificationRef: z.string().min(1),
    lastUpdatedAt: z.string().min(1)
  })
  .strict();
```

### 4.2 Projection attendue dans les vues

| Vue | Lecture minimale attendue |
| --- | --- |
| `verification-view` | statut pret/pas pret, `verificationRef`, `traceId`, controles manquants |
| `audit-view` | refus, findings, activations, decisions et evidence refs |
| `session-view` | regroupement par `traceId`, `correlationId`, `verificationRef` |

### 4.3 Regle de blocage

Une transition critique reste bloquee si au moins une de ces conditions est vraie:

- `traceId` absent,
- `actionId` absent,
- `controlsExecuted` vide,
- `evidenceRefs` vide,
- `verificationRef` absent.

## 5. Pilote d'enveloppe canonique de message

### 5.1 Intention du pilote

Le pilote d'enveloppe canonique n'a pas pour but de remplacer `ClientEvent` et `ServerEvent`.

Il a pour but de fournir une projection commune bornee pour les lectures critiques runtime, replay, spectateur et multi-session.

### 5.2 Objet `CanonicalEnvelopePilot`

```typescript
const CanonicalEnvelopePilotSchema = z
  .object({
    header: z
      .object({
        messageType: z.string().min(1),
        messageVersion: z.literal('pilot-v1'),
        messageId: z.string().min(1),
        emittedAt: z.string().min(1),
        channel: z.enum(['runtime', 'replay', 'spectator', 'session'])
      })
      .strict(),
    context: EventMetaSchema.extend({
      protocolVersion: z.literal('v1')
    }).strict(),
    body: JsonValueSchema
  })
  .strict();
```

### 5.3 Mapping borne

| Event courant | `header.messageType` pilote | `body` |
| --- | --- | --- |
| `TASK_UPDATE` | `task.update` | `task` + `agent` optionnel |
| `WORKFLOW_STEP` | `workflow.step` | `step` |
| `VERIFICATION_GATE` | `verification.gate` | verdict + evidence refs + controles |
| `ERROR` | `runtime.error` | `code`, `message`, `retryable` |
| `SURFACE_POLICY_STATE` | `surface.policy` | fiche surface + decision |

### 5.4 Regles de compatibilite

- Le pilote doit etre genere par projection ou adapter, pas par remplacement immediat du contrat principal.
- Les consommateurs existants peuvent continuer a lire les payloads `v1` tant que le pilote n'est pas leur source explicite.
- Toute divergence semantique entre l'event d'origine et l'enveloppe pilote invalide le pilote.

## 6. Cibles de tests

| Ticket | Tests runtime prioritaires |
| --- | --- |
| `GAME-TKT-037` | `auth-rbac.test.ts`, `runtime-source-fs.test.ts`, nouveaux tests de contrat de surfaces |
| `GAME-TKT-038` | `verification-view.test.ts`, `audit-view.test.ts`, `runtime-source-fs.test.ts` |
| `GAME-TKT-039` | `session-view.test.ts`, `audit-view.test.ts`, nouveaux tests de projection canonique |

## 7. Claims et non-claims

- Claim autorise: le projet aligne ses garde-fous runtime sur un modele interne inspire d'OWASP Agentic Skills, d'une verification d'integrite exploitable et d'une enveloppe canonique pilote.
- Non-claim obligatoire: aucune conformite complete a OWASP Agentic Skills Top 10, AIVS ou IEEE P3394 UMF n'est revendiquee par ce document.
