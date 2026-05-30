---
title: Contrat runtime - Host Bridge agentique externe
description: Spec additive pour hotes externes, invocations bornees, reviews importees et ledger de contexte.
author: GitHub Copilot
date: 2026-04-10
---

## But

Donner une descente technique concrete aux tickets `GAME-TKT-047` a `GAME-TKT-051`, compatible avec le runtime `v1` actuel de `grimoire-kit/apps/grimoire-game`.

Ce document ne decrit pas une conformite vendeur. Il decrit le contrat interne cible du projet pour:

- absorber des hotes externes sans lock-in produit,
- borner les actions, reviews et imports de contexte,
- garder Forge comme source de verite.

## Sources techniques du package runtime

- `grimoire-kit/apps/grimoire-game/src/contracts/schemas.ts`
- `grimoire-kit/apps/grimoire-game/src/contracts/events.ts`
- `grimoire-kit/apps/grimoire-game/src/bridge/agent-adapter.ts`
- `grimoire-kit/apps/grimoire-game/src/bridge/agent-connection-health.ts`
- `grimoire-kit/apps/grimoire-game/src/state/audit-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/session-view.ts`
- `grimoire-kit/apps/grimoire-game/src/state/runtime-dashboard-view.ts`
- `grimoire-kit/framework/tools/tool-registry.py`
- `grimoire-kit/framework/tools/mcp-proxy.py`
- `grimoire-kit/framework/tools/llm-router.py`

## Regles de compatibilite

- Le protocole courant `v1` reste la source de verite de compatibilite descendante.
- Les ajouts presentes ici sont additifs tant qu'ils n'imposent pas un remplacement global des payloads existants.
- Les noms vendeurs vivent dans les metadata d'hote, jamais dans les champs canoniques du coeur runtime.
- Toute information critique issue d'un hote externe doit pouvoir etre projetee dans un event dedie et rejouable.
- Les hotes externes restent des sources secondaires d'entree, de review et de contexte.

## 1. Registre canonique des hotes externes

### 1.1 Objet `HostBinding`

```typescript
const HostBindingSchema = z
  .object({
    hostId: z.string().min(1),
    hostType: z.enum(['copilot', 'claude', 'mcp', 'ide', 'other']),
    displayName: z.string().min(1),
    version: z.string().min(1).optional(),
    authMode: z.enum(['none', 'session', 'token', 'oauth', 'delegated']),
    connectionState: z.enum(['online', 'stale', 'degraded', 'offline', 'blocked']),
    trustStatus: z.enum(['trusted', 'review', 'restricted', 'blocked']),
    scopes: z.array(z.enum(['fs', 'network', 'secrets', 'exec', 'config_write', 'write_budget'])).default([]),
    capabilityManifestRef: z.string().min(1),
    sourceOfTruth: z.literal('secondary'),
    lastSeenAt: z.string().min(1).optional(),
    notes: z.string().min(1).optional()
  })
  .strict();
```

### 1.2 Regles d'usage

- Aucun hote externe n'entre dans le runtime sans `hostId`, `hostType`, `connectionState`, `trustStatus` et `capabilityManifestRef`.
- `sourceOfTruth` reste toujours `secondary`.
- `connectionState=blocked` interdit toute mutation et tout import.

## 2. Declaration des capabilities

### 2.1 Objet `CapabilityManifest`

```typescript
const CapabilityManifestSchema = z
  .object({
    manifestId: z.string().min(1),
    hostId: z.string().min(1),
    routines: z.array(z.string().min(1)).default([]),
    toolProviders: z.array(z.string().min(1)).default([]),
    reviewChannels: z.array(z.string().min(1)).default([]),
    contextSources: z.array(z.string().min(1)).default([]),
    permissionMode: z.enum(['none', 'prompt', 'policy', 'hybrid']),
    supportsStreaming: z.boolean(),
    supportsReviewImport: z.boolean(),
    supportsContextImport: z.boolean(),
    supportsPreviewCommit: z.boolean()
  })
  .strict();
```

### 2.2 Regles de gate

- Un hote sans `CapabilityManifest` ne peut faire que de la lecture diagnostique.
- `supportsPreviewCommit=false` interdit toute mutation durable.
- Toute capability exposee doit etre journalisee dans l'audit au moment du binding.

## 3. Enveloppe d'invocation canonique

### 3.1 Objet `InvocationEnvelope`

```typescript
const InvocationEnvelopeSchema = z
  .object({
    envelopeId: z.string().min(1),
    hostId: z.string().min(1),
    actionKind: z.enum(['tool_call', 'routine', 'review_import', 'context_import', 'permission_prompt']),
    mode: z.enum(['read', 'preview', 'validate', 'commit']),
    correlationId: z.string().min(1),
    idempotencyKey: z.string().min(1),
    traceId: z.string().min(1).optional(),
    taskId: z.string().min(1).optional(),
    requestedScopes: z.array(z.enum(['fs', 'network', 'secrets', 'exec', 'config_write', 'write_budget'])).default([]),
    payload: JsonValueSchema,
    evidencePolicy: z.enum(['none', 'basic', 'strict'])
  })
  .strict();
```

### 3.2 Regles d'usage

- Toute mutation issue d'un hote externe commence en `preview` ou `validate`, jamais en `commit` direct.
- `idempotencyKey` est obligatoire pour toute action non read-only.
- `evidencePolicy=strict` est obligatoire pour toute action qui touche `Done`, `merge`, `review verdict` ou configuration durable.

## 4. Ledger de contexte importe

### 4.1 Objet `ContextLedgerEntry`

```typescript
const ContextLedgerEntrySchema = z
  .object({
    entryId: z.string().min(1),
    hostId: z.string().min(1),
    sourceType: z.enum(['instructions', 'memory', 'selection', 'session_context', 'review_summary']),
    visibility: z.enum(['private', 'shared', 'audit_only']),
    confidence: z.number().min(0).max(10),
    importedAt: z.string().min(1),
    ttlSeconds: z.number().int().positive(),
    contentRef: z.string().min(1),
    supersedes: z.string().min(1).optional(),
    trustStatus: z.enum(['trusted', 'review', 'restricted'])
  })
  .strict();
```

### 4.2 Regles d'usage

- Un contexte importe ne remplace jamais silencieusement la memoire interne.
- `ttlSeconds` est obligatoire pour tout contexte non persistant.
- `visibility=private` interdit toute promotion vers la memoire projet sans action explicite.

## 5. Artefact de review canonique

### 5.1 Objet `ReviewArtifact`

```typescript
const ReviewArtifactSchema = z
  .object({
    reviewId: z.string().min(1),
    hostId: z.string().min(1),
    sourceType: z.enum(['copilot_review', 'claude_review', 'github_check', 'github_pr_comment', 'mcp_review', 'other']),
    subjectRef: z.string().min(1),
    verdict: z.enum(['pass', 'warn', 'fail', 'comment']),
    findings: z.array(
      z
        .object({
          id: z.string().min(1),
          severity: z.enum(['critical', 'high', 'medium', 'low', 'info']),
          message: z.string().min(1),
          resolutionStatus: z.enum(['open', 'acknowledged', 'resolved', 'wont_fix']).default('open')
        })
        .strict()
    ),
    linkedEvidenceRefs: z.array(z.string().min(1)).default([]),
    importedAt: z.string().min(1),
    traceId: z.string().min(1).optional(),
    taskId: z.string().min(1).optional()
  })
  .strict();
```

### 5.2 Regles d'usage

- Toute review importee doit pouvoir se relire sans l'UI du vendeur.
- Un `ReviewArtifact` sans `subjectRef` ni `findings` est invalide.
- Les severites externes sont remappees sur l'echelle canonique ci-dessus.

## 6. Events cibles a ajouter ou enrichir

### 6.1 Server event `HOST_BINDING_STATE`

```typescript
const HostBindingStateEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('HOST_BINDING_STATE'),
  binding: HostBindingSchema,
  manifest: CapabilityManifestSchema,
  reason: z.string().min(1).optional()
}).strict();
```

### 6.2 Server event `HOST_INVOCATION_DECISION`

```typescript
const HostInvocationDecisionEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('HOST_INVOCATION_DECISION'),
  envelope: InvocationEnvelopeSchema,
  decision: z.enum(['ALLOW', 'PROMPT', 'DENY', 'DEGRADE']),
  reason: z.string().min(1),
  meta: EventMetaSchema
}).strict();
```

### 6.3 Server event `HOST_REVIEW_ARTIFACT`

```typescript
const HostReviewArtifactEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('HOST_REVIEW_ARTIFACT'),
  review: ReviewArtifactSchema,
  meta: EventMetaSchema
}).strict();
```

### 6.4 Server event `HOST_CONTEXT_LEDGER_UPDATE`

```typescript
const HostContextLedgerUpdateEventSchema = ServerEventBaseSchema.extend({
  type: z.literal('HOST_CONTEXT_LEDGER_UPDATE'),
  entry: ContextLedgerEntrySchema,
  meta: EventMetaSchema
}).strict();
```

## 7. Projection attendue dans les vues

| Vue | Lecture minimale attendue |
| --- | --- |
| `audit-view` | decisions de policy, permission prompts, reviews importees, degradations |
| `session-view` | correlation `hostId` / `traceId` / `taskId` sur les runs concernes |
| `runtime-dashboard-view` | statut des hotes, health, routines actives, imports de contexte |
| `agent-connection-health` | etat `online`, `stale`, `degraded`, `blocked` des hotes relies a un agent ou a une session |

## 8. Regles non negociables

- Forge garde la source unique de verite pour runs, taches, policies, memoires et preuves.
- Les hotes externes sont `deny-by-default`.
- Toute mutation issue d'un hote externe passe par `preview -> validation -> commit`.
- Une panne ou un drift de feature degrade le host, jamais le noyau.
- Les reviews et contextes externes sont importes comme evidence ou contexte secondaire, jamais comme verite silencieuse.

## 9. Mapping direct des tickets

| Ticket | Portee dans ce contrat |
| --- | --- |
| `GAME-TKT-047` | `HostBinding` + `CapabilityManifest` |
| `GAME-TKT-048` | `InvocationEnvelope` + `ContextLedgerEntry` + `ReviewArtifact` |
| `GAME-TKT-049` | decisions `ALLOW`, `PROMPT`, `DENY`, `DEGRADE` et scopes fail-closed |
| `GAME-TKT-050` | `ReviewArtifact` relies aux evidence refs |
| `GAME-TKT-051` | projections runtime lisibles par cockpit et surface multi-host |
