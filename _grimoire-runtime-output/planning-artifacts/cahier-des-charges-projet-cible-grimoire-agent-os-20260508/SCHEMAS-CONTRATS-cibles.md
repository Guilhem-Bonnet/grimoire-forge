---
title: Schemas et contrats cibles - Grimoire Agent OS
description: Contrats de donnees, manifests, events, policies et packs pour le projet cible.
author: Codex
date: 2026-05-08
---

# Schemas et contrats cibles - Grimoire Agent OS

## 1. Conventions

### 1.1 Identifiants

| Type | Format | Exemple |
| --- | --- | --- |
| Mission | `MIS-<slug>-<seq>` | `MIS-pack-registry-001` |
| Task | `GAO-<area>-<seq>` | `GAO-ledger-014` |
| Workflow instance | `WFI-<mission>-<seq>` | `WFI-pack-registry-003` |
| Run | `RUN-<ulid>` | `RUN-01HXEXAMPLE` |
| Evidence pack | `EVD-<task>-<seq>` | `EVD-GAO-ledger-014-001` |
| Policy verdict | `POL-<run>-<seq>` | `POL-RUN-01HXEXAMPLE-001` |
| Pack | reverse DNS or org slug | `grimoire.pack.gascity` |

### 1.2 Champs communs

Tous les objets persistants doivent porter :

- `id` ;
- `schema_version` ;
- `created_at` ;
- `created_by` ;
- `source` ;
- `provenance` ;
- `status` ;
- `links`.

### 1.3 Versionnement

Chaque contrat public doit indiquer :

- `schema_version` ;
- `compatibility_min` ;
- `compatibility_max` ;
- `migration` ;
- `deprecation`.

## 2. Mission

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.grimoire.dev/mission.schema.json",
  "title": "Mission",
  "type": "object",
  "required": ["id", "schema_version", "title", "status", "origin", "created_at"],
  "properties": {
    "id": { "type": "string", "pattern": "^MIS-[a-z0-9-]+-[0-9]{3,}$" },
    "schema_version": { "type": "string" },
    "title": { "type": "string", "minLength": 3 },
    "description": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["draft", "open", "blocked", "verifying", "closed", "cancelled"]
    },
    "origin": { "type": "string" },
    "risk_profile": { "$ref": "#/$defs/risk_profile" },
    "created_at": { "type": "string", "format": "date-time" },
    "created_by": { "type": "string" },
    "scope": {
      "type": "object",
      "properties": {
        "repos": { "type": "array", "items": { "type": "string" } },
        "surfaces": { "type": "array", "items": { "type": "string" } },
        "packs": { "type": "array", "items": { "type": "string" } }
      }
    },
    "links": { "$ref": "#/$defs/links" }
  },
  "$defs": {
    "risk_profile": {
      "type": "string",
      "enum": ["light", "standard", "strict", "security_critical", "release"]
    },
    "links": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "target"],
        "properties": {
          "kind": { "type": "string" },
          "target": { "type": "string" }
        }
      }
    }
  }
}
```

## 3. MissionTask

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.grimoire.dev/mission-task.schema.json",
  "title": "MissionTask",
  "type": "object",
  "required": [
    "id",
    "schema_version",
    "mission_id",
    "title",
    "status",
    "type",
    "risk_profile",
    "acceptance",
    "created_at"
  ],
  "properties": {
    "id": { "type": "string", "pattern": "^GAO-[a-z0-9-]+-[0-9]{3,}$" },
    "schema_version": { "type": "string" },
    "mission_id": { "type": "string" },
    "title": { "type": "string" },
    "description": { "type": "string" },
    "status": {
      "type": "string",
      "enum": [
        "proposed",
        "ready",
        "claimed",
        "running",
        "blocked",
        "needs_verification",
        "failed",
        "closed",
        "cancelled"
      ]
    },
    "type": {
      "type": "string",
      "enum": [
        "analysis",
        "architecture",
        "implementation",
        "test",
        "documentation",
        "migration",
        "security",
        "operation",
        "cleanup"
      ]
    },
    "risk_profile": {
      "type": "string",
      "enum": ["light", "standard", "strict", "security_critical", "release"]
    },
    "surface": { "type": "string" },
    "owner": { "type": "string" },
    "claim": {
      "type": "object",
      "properties": {
        "actor_id": { "type": "string" },
        "host_id": { "type": "string" },
        "exclusive_files": { "type": "array", "items": { "type": "string" } }
      }
    },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "target"],
        "properties": {
          "kind": {
            "type": "string",
            "enum": ["blocks", "relates", "parent_child", "discovered_from", "supersedes"]
          },
          "target": { "type": "string" }
        }
      }
    },
    "acceptance": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" }
    },
    "guardrails": {
      "type": "array",
      "items": { "type": "string" }
    },
    "expected_evidence": {
      "type": "array",
      "items": { "type": "string" }
    },
    "links": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "target"],
        "properties": {
          "kind": { "type": "string" },
          "target": { "type": "string" }
        }
      }
    },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

## 4. Recipe

```yaml
schema_version: grimoire.recipe.v1
id: recipe.pack.convert-gascity
name: convert-gascity-pack
version: 1.0.0
description: Convertit un pack Gas City en pack Grimoire controle.
inputs:
  type: object
  required:
    - source_pack
    - target_pack
  properties:
    source_pack:
      type: string
    target_pack:
      type: string
outputs:
  type: object
  required:
    - pack_manifest
    - pack_lock
    - doctor_result
steps:
  - id: read-source
    kind: tool
    tool: filesystem.read
    policy: read_only
  - id: parse-pack
    kind: transform
    output_schema: gascity.pack.normalized.v1
  - id: map-manifest
    kind: transform
    output_schema: grimoire.pack.v1
  - id: validate
    kind: validation
    validator: grimoire.pack.validate
  - id: lock
    kind: tool
    tool: grimoire.pack.lock
    policy: mutation_controlled
  - id: doctor
    kind: tool
    tool: grimoire.pack.doctor
    policy: read_only
policies:
  profile: strict
  required:
    - pack-manifest-valid
    - pack-lock-present
    - no-shell-command-enabled-by-default
evidence:
  profile: strict
  expected:
    - converted_manifest
    - validation_output
    - lock_digest
    - doctor_output
```

## 5. WorkflowInstance

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.grimoire.dev/workflow-instance.schema.json",
  "title": "WorkflowInstance",
  "type": "object",
  "required": ["id", "recipe_id", "mission_id", "task_id", "status", "created_at"],
  "properties": {
    "id": { "type": "string", "pattern": "^WFI-[a-z0-9-]+-[0-9]{3,}$" },
    "recipe_id": { "type": "string" },
    "recipe_version": { "type": "string" },
    "mission_id": { "type": "string" },
    "task_id": { "type": "string" },
    "run_id": { "type": "string" },
    "status": {
      "type": "string",
      "enum": [
        "created",
        "running",
        "checkpointed",
        "paused",
        "blocked",
        "aborted",
        "completed",
        "verified"
      ]
    },
    "host_id": { "type": "string" },
    "actor_id": { "type": "string" },
    "inputs_ref": { "type": "string" },
    "outputs_ref": { "type": "string" },
    "checkpoint_refs": { "type": "array", "items": { "type": "string" } },
    "evidence_pack_id": { "type": "string" },
    "abort_reason": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

## 6. RunEvent

```yaml
schema_version: grimoire.run_event.v1
id: evt-01HXEXAMPLE
run_id: RUN-01HXEXAMPLE
mission_id: MIS-pack-registry-001
task_id: GAO-pack-001
workflow_instance_id: WFI-pack-registry-001
event_type: tool.requested
actor:
  actor_id: agent-pack-worker
  host_id: host-codex
payload:
  tool_name: grimoire.pack.validate
  tool_kind: validator
  mutation_class: read_only
policy:
  required: true
  verdict_id: POL-RUN-01HXEXAMPLE-001
trace:
  span_id: span-pack-validate
  parent_span_id: span-workflow
created_at: "2026-05-08T00:00:00Z"
```

## 7. Checkpoint

```yaml
schema_version: grimoire.checkpoint.v1
id: chk-WFI-pack-registry-001-001
workflow_instance_id: WFI-pack-registry-001
run_id: RUN-01HXEXAMPLE
step_id: validate
state:
  completed_steps:
    - read-source
    - parse-pack
    - map-manifest
    - validate
  pending_steps:
    - lock
    - doctor
  side_effects:
    - path: _grimoire-runtime/packs/generated/grimoire.pack.gascity/pack.yaml
      mutation: create
      digest: sha256-example
resume:
  idempotency_key: idem-WFI-pack-registry-001-validate
  safe_to_resume: true
evidence_refs:
  - evitem-validation-output
created_at: "2026-05-08T00:00:00Z"
```

## 8. PolicyRequest

```yaml
schema_version: grimoire.policy_request.v1
id: pretool-RUN-01HXEXAMPLE-001
run_id: RUN-01HXEXAMPLE
task_id: GAO-pack-001
actor:
  actor_id: agent-pack-worker
  host_id: host-codex
action:
  kind: tool_use
  tool: shell
  command: grimoire pack activate grimoire.pack.gascity
  mutation_class: pack_activation
resources:
  files:
    - _grimoire-runtime/packs/generated/grimoire.pack.gascity/pack.yaml
  network: []
  secrets: []
risk_profile: strict
context:
  pack_id: grimoire.pack.gascity
  evidence_required: true
```

## 9. PolicyVerdict

```yaml
schema_version: grimoire.policy_verdict.v1
id: POL-RUN-01HXEXAMPLE-001
request_id: pretool-RUN-01HXEXAMPLE-001
run_id: RUN-01HXEXAMPLE
verdict: block
mode: enforced
reason: pack activation requires pack.lock.json and doctor success
rules:
  matched:
    - pack-lock-required
    - doctor-success-required
  missing:
    - lock_digest
    - doctor_result
actions:
  create_incident: true
  allow_retry_after:
    - grimoire pack lock
    - grimoire pack doctor
created_at: "2026-05-08T00:00:00Z"
```

## 10. EvidencePack

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.grimoire.dev/evidence-pack.schema.json",
  "title": "EvidencePack",
  "type": "object",
  "required": ["id", "task_id", "profile", "items", "created_at"],
  "properties": {
    "id": { "type": "string", "pattern": "^EVD-GAO-[a-z0-9-]+-[0-9]{3,}-[0-9]{3,}$" },
    "task_id": { "type": "string" },
    "workflow_instance_id": { "type": "string" },
    "profile": {
      "type": "string",
      "enum": ["light", "standard", "strict", "security_critical", "release"]
    },
    "items": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "kind", "uri", "digest"],
        "properties": {
          "id": { "type": "string" },
          "kind": {
            "type": "string",
            "enum": ["test", "log", "diff", "doc", "schema", "trace", "screenshot", "report"]
          },
          "uri": { "type": "string" },
          "digest": { "type": "string" },
          "summary": { "type": "string" }
        }
      }
    },
    "coverage": {
      "type": "object",
      "properties": {
        "acceptance_covered": { "type": "array", "items": { "type": "string" } },
        "acceptance_missing": { "type": "array", "items": { "type": "string" } }
      }
    },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

## 11. VerificationVerdict

```yaml
schema_version: grimoire.verification_verdict.v1
id: ver-GAO-pack-001-001
task_id: GAO-pack-001
evidence_pack_id: EVD-GAO-pack-001-001
verdict: failed
profile: strict
checks:
  - id: evidence-present
    result: passed
  - id: pack-lock-present
    result: failed
    reason: lock file missing
  - id: no-enabled-shell-by-default
    result: passed
decision:
  close_task: false
  reopen_task: true
  create_incident: true
created_by: verifier-runtime
created_at: "2026-05-08T00:00:00Z"
```

## 12. MemoryRecord

```yaml
schema_version: grimoire.memory_record.v1
id: mem-GAO-ledger-014-001
kind: decision
scope: project
title: Mission Ledger is the source of truth
content_ref: memory://grimoire/decisions/mission-ledger-source-of-truth
source:
  type: document
  uri: _grimoire-runtime-output/planning-artifacts/plan-directeur-grimoire-gastown-unifie-20260508/PLAN-DIRECTEUR-nouveau-projet-grimoire-agent-os.md
provenance:
  mission_id: MIS-runtime-kernel-001
  task_id: GAO-ledger-014
freshness:
  status: current
  confidence: high
contradictions:
  detected: false
promotion:
  promoted_by: verifier-memory
  reason: architecture decision used by multiple plans
created_at: "2026-05-08T00:00:00Z"
```

## 13. RecallRequest

```yaml
schema_version: grimoire.recall_request.v1
id: recall-RUN-01HXEXAMPLE-001
run_id: RUN-01HXEXAMPLE
task_id: GAO-ledger-014
query: ledger source of truth implementation constraints
scope:
  project: grimoire-forge
  repos:
    - Grimoire-Forge
  collections:
    - grimoire_memory
    - grimoire_code
risk_profile: strict
filters:
  require_provenance: true
  freshness:
    - current
    - review_required
  include_contradictions: true
limits:
  max_records: 12
  max_context_chars: 12000
```

## 13.1 Memory backend config cible

```yaml
memory:
  backend: qdrant-server
  collection_prefix: grimoire_kit
  embedding_model: sentence-transformers/all-MiniLM-L6-v2
  qdrant_url: http://localhost:6333
  weaviate_url: http://localhost:8080
  weaviate_collection: GrimoireKitMemory
  neo4j_uri: bolt://localhost:7687
  neo4j_user: neo4j
  neo4j_password_env: GRIMOIRE_NEO4J_PASSWORD
  neo4j_database: neo4j
  migration_source_backend: qdrant-server
  migration_target_backend: weaviate-server
  migration_bundle_path: _grimoire/_memory/migration/weaviate-neo4j
  layer_profile: weaviate-neo4j-migration
  knowledge_graph: neo4j
  memory_graph: neo4j
  code_graph: neo4j
  task_memory: neo4j
```

Regle :

- `backend` reste `qdrant-server` tant que la migration n'est pas vector-lossless ;
- `migration_target_backend` declare la cible ;
- `neo4j_password_env` pointe vers une variable d'environnement, jamais vers un secret en clair.

## 13.2 MigrationBundle

```yaml
schema_version: grimoire.memory_migration.v1
source_backend: qdrant-server
target_vector_backend: weaviate-server
target_graph_backend: neo4j
record_count: 1200
vector_count: 1200
vector_lossless: true
files:
  memories: memories.jsonl
  weaviate_objects: weaviate-objects.jsonl
  neo4j_cypher: neo4j-import.cypher
```

Gate :

- `vector_lossless` doit etre `true` avant cutover ;
- chaque objet Weaviate garde `source_id` ;
- chaque node Neo4j garde le meme `id` source ;
- les payloads Qdrant restent serialises dans `memories.jsonl`.

## 14. PackManifest

```yaml
schema_version: grimoire.pack.v1
id: grimoire.pack.gascity
name: gascity-imported-primitives
version: 0.1.0
status: experimental
owner: grimoire-core
source:
  kind: converted
  upstream: gascity-packs
  converter: grimoire.pack.convert-gascity
compatibility:
  grimoire_min: 0.1.0
  grimoire_max: 0.x
components:
  recipes:
    - recipe.pack.convert-gascity
  commands:
    - grimoire.gascity.doctor
  policies:
    - policy.pack.shell-disabled-by-default
commands:
  - id: grimoire.gascity.doctor
    command: grimoire pack doctor grimoire.pack.gascity
    mutation_class: read_only
    default_enabled: true
  - id: grimoire.gascity.activate
    command: grimoire pack activate grimoire.pack.gascity
    mutation_class: pack_activation
    default_enabled: false
doctor:
  checks:
    - id: manifest-valid
      kind: schema
    - id: no-enabled-shell-by-default
      kind: policy
permissions:
  filesystem:
    read:
      - _grimoire-runtime/packs/generated/grimoire.pack.gascity/**
    write:
      - _grimoire-runtime/packs/generated/grimoire.pack.gascity/**
  network: []
  secrets: []
activation:
  default_mode: shadow
  requires:
    - pack.lock.json
    - doctor_success
    - policy_verdict
```

## 15. PackLock

```yaml
schema_version: grimoire.pack_lock.v1
pack_id: grimoire.pack.gascity
pack_version: 0.1.0
manifest_digest: sha256-example
files:
  - path: pack.yaml
    digest: sha256-example
  - path: recipes/convert-gascity.yaml
    digest: sha256-example
dependencies: []
generated_by:
  tool: grimoire pack lock
  version: 0.1.0
created_at: "2026-05-08T00:00:00Z"
```

## 16. HostCapabilityManifest

```yaml
schema_version: grimoire.host_capability.v1
host_id: host-codex
display_name: Codex
supports:
  hooks:
    session_start: false
    user_prompt_submit: false
    pre_tool_use: false
    post_tool_use: false
    subagent_start: true
    subagent_stop: true
    pre_compact: false
    stop: false
  mcp: true
  streaming: true
  workspace_mutation: true
  tool_policy_native: false
fallback:
  mode: cli_guarded
  required_controls:
    - preview_before_write
    - validation_before_durable_write
    - explicit_proof_for_risky_changes
```

## 17. Incident

```yaml
schema_version: grimoire.incident.v1
id: inc-GAO-pack-001-001
mission_id: MIS-pack-registry-001
task_id: GAO-pack-001
workflow_instance_id: WFI-pack-registry-001
kind: policy_block
severity: medium
status: open
summary: Pack activation blocked because lock is missing
causes:
  - pack-lock-required
  - doctor-success-required
recommended_actions:
  - run grimoire pack lock
  - run grimoire pack doctor
links:
  - kind: policy_verdict
    target: POL-RUN-01HXEXAMPLE-001
created_at: "2026-05-08T00:00:00Z"
```

## 18. Cockpit projections

```yaml
schema_version: grimoire.projection.mission_board.v1
mission:
  id: MIS-pack-registry-001
  title: Pack Registry cible
  status: open
summary:
  total_tasks: 12
  ready: 3
  blocked: 2
  running: 1
  needs_verification: 2
  closed: 4
risks:
  strict: 5
  security_critical: 2
incidents:
  open: 2
verification:
  queue: 2
performance:
  replay_success_ratio: 0.94
  evidence_completeness_ratio: 0.88
links:
  ledger_query: ledger://missions/MIS-pack-registry-001
```

## 19. Mapping Beads vers Grimoire

| Beads | Grimoire |
| --- | --- |
| issue | MissionTask |
| dependency | TaskDependency |
| ready query | ledger query `ready` |
| comment | LedgerEvent or EvidenceItem |
| JSONL export | import/export adapter |
| multi-repo route | `scope.repos` and `source_repo` |

## 20. Mapping CrewAI vers Grimoire

| CrewAI | Grimoire |
| --- | --- |
| Crew | Recipe group or external runner adapter |
| Agent | internal actor capability |
| Task | MissionTask or recipe step |
| Flow | Recipe |
| guardrail | PolicyRule or VerificationGate |
| output schema | Recipe output schema |
| Knowledge | Memory OS adapter |
| tracing | Trace Ledger export |

## 21. Mapping Gas City vers Grimoire

| Gas City | Grimoire |
| --- | --- |
| Mayor | grimoire-master |
| formula | Recipe |
| order | controller-side automation |
| pack.toml | pack.yaml |
| supervisor | Runtime Kernel |
| provider tier | HostCapabilityManifest |
| convoy | workflow group |

## 22. Contrat minimal pour fermeture de task

```yaml
closure_request:
  task_id: GAO-ledger-014
  requested_by: agent-ledger-worker
  required:
    - status is needs_verification
    - evidence_pack present
    - acceptance covered
    - policy blocks resolved
    - incidents closed or accepted
    - verification verdict passed
  forbidden:
    - close without ledger event
    - close from UI-only state
    - close with missing evidence
    - close with unresolved critical incident
```
