---
title: Architecture cible et diagrammes - Grimoire Agent OS
description: Diagrammes Mermaid pour le cahier des charges cible.
author: Codex
date: 2026-05-08
---

# Architecture cible et diagrammes - Grimoire Agent OS

## 1. Vue contexte

```mermaid
flowchart TD
    Human[Operateur humain] --> Experience[Experience Plane]
    IDE[IDE hosts] --> Experience
    CLI[CLI] --> Experience
    MCP[MCP clients] --> Experience
    External[External runners] --> Interop[Interop Adapters]
    Experience --> Orchestrator[grimoire-master]
    Interop --> Orchestrator
    Orchestrator --> Ledger[Mission Ledger]
    Orchestrator --> Runtime[Runtime Kernel]
    Runtime --> Tools[Tools and Providers]
    Runtime --> Policy[Policy Engine]
    Runtime --> Evidence[Evidence Service]
    Runtime --> Memory[Memory OS]
    Runtime --> Trace[Trace and Eval Ledger]
    Packs[Pack Registry] --> Runtime
    Packs --> Policy
    Ledger --> Cockpit[Mission Board Cockpit]
    Evidence --> Cockpit
    Trace --> Cockpit
    Memory --> Cockpit
```

Lecture :

- l'humain ne parle pas a une armee d'agents visibles ;
- `grimoire-master` reste le point d'entree ;
- le ledger tient l'etat metier ;
- le runtime execute ;
- le cockpit lit des projections.

## 2. Vue conteneurs

```mermaid
flowchart LR
    subgraph Forge[Grimoire Forge]
        Master[grimoire-master]
        Board[Mission Board]
        ForgeHooks[Host Hooks]
        ForgeDocs[Docs and Plans]
    end

    subgraph Kit[grimoire-kit]
        Kernel[Runtime Kernel]
        SDK[SDK]
        KitCLI[CLI]
        MCPServer[MCP Server]
        Validators[Validators]
    end

    subgraph Data[Data Stores]
        LedgerDB[(Ledger Store)]
        EventLog[(Event Log)]
        Checkpoints[(Checkpoints)]
        EvidenceStore[(Evidence Store)]
        Weaviate[(Weaviate Vector Store)]
        Neo4j[(Neo4j Graph Store)]
        TraceStore[(Trace Store)]
        PackStore[(Pack Registry)]
    end

    subgraph External[External Ecosystem]
        CrewAI[CrewAI Adapter]
        LangGraph[LangGraph Adapter]
        OpenAI[OpenAI Agents Adapter]
        A2A[A2A Adapter]
        GasCity[Gas City Converter]
        Beads[Beads Import Export]
    end

    Master --> Kernel
    Board --> LedgerDB
    Board --> TraceStore
    ForgeHooks --> Kernel
    ForgeDocs --> Validators
    SDK --> Kernel
    KitCLI --> Kernel
    MCPServer --> Kernel
    Kernel --> LedgerDB
    Kernel --> EventLog
    Kernel --> Checkpoints
    Kernel --> EvidenceStore
    Kernel --> Weaviate
    Kernel --> Neo4j
    Kernel --> TraceStore
    Kernel --> PackStore
    External --> Kernel
    External --> PackStore
```

## 3. Architecture en plans

```mermaid
flowchart TB
    subgraph UX[Experience Plane]
        IDEHost[IDE Host]
        CLIHost[CLI]
        Cockpit[Mission Board]
        Reports[Reports]
    end

    subgraph ORCH[Orchestration Plane]
        Intake[Mission Intake]
        Router[Task Router]
        Ledger[Mission Ledger]
    end

    subgraph EXEC[Execution Plane]
        Runtime[Runtime Kernel]
        Workflows[Workflow Instances]
        Providers[Host Bridge Providers]
        Tools[Tools]
    end

    subgraph CTRL[Control Plane]
        Hooks[Hooks]
        Policies[Policy Engine]
        Guardrails[Guardrails]
    end

    subgraph KNOW[Knowledge Plane]
        Memory[Memory OS]
        Weaviate[Weaviate Vector Recall]
        Neo4j[Neo4j Knowledge and Code Graph]
        Docs[Docs Graph]
    end

    subgraph EXT[Extension Plane]
        Packs[Pack Registry]
        Adapters[Adapters]
        Converters[Converters]
    end

    subgraph OBS[Observability Plane]
        Trace[Trace Ledger]
        Evals[Eval Ledger]
        Metrics[Metrics Export]
    end

    UX --> ORCH
    ORCH --> EXEC
    EXEC --> CTRL
    EXEC --> KNOW
    EXT --> EXEC
    EXEC --> OBS
    CTRL --> OBS
    KNOW --> ORCH
```

## 4. Sequence mission vers fermeture

```mermaid
sequenceDiagram
    participant U as Human
    participant M as grimoire-master
    participant L as Mission Ledger
    participant R as Runtime Kernel
    participant P as Policy Engine
    participant A as Agent or Runner
    participant E as Evidence Service
    participant V as Verification
    participant B as Cockpit

    U->>M: Submit mission
    M->>L: mission.created
    M->>L: task.created and task.qualified
    L-->>M: ready tasks
    M->>R: create WorkflowInstance
    R->>P: policy preview
    P-->>R: allow or warn or block
    R->>A: execution context
    A->>R: tool requested
    R->>P: PolicyRequest
    P-->>R: PolicyVerdict
    R->>A: tool allowed
    A->>R: output
    R->>E: evidence candidate
    R->>L: workflow.checkpointed
    E->>V: verification.requested
    V-->>L: verification.passed
    L->>B: projection refreshed
    B-->>U: task closed with evidence
```

## 5. Lifecycle d'une task

```mermaid
stateDiagram-v2
    [*] --> proposed
    proposed --> ready: qualified
    proposed --> cancelled: rejected
    ready --> claimed: claim
    ready --> blocked: dependency_missing
    claimed --> running: workflow_started
    running --> blocked: incident_or_policy_block
    running --> needs_verification: output_ready
    blocked --> ready: unblock
    needs_verification --> closed: verification_passed
    needs_verification --> running: verification_failed_rework
    running --> failed: unrecoverable_error
    failed --> ready: retry_authorized
    failed --> cancelled: abandoned_with_reason
    closed --> [*]
    cancelled --> [*]
```

## 6. Lifecycle d'un workflow

```mermaid
stateDiagram-v2
    [*] --> created
    created --> running: start
    running --> checkpointed: checkpoint
    checkpointed --> running: continue
    running --> paused: pause
    paused --> running: resume
    running --> blocked: policy_or_incident
    blocked --> running: resolved
    running --> completed: outputs_ready
    completed --> verified: verification_passed
    completed --> running: verification_failed
    running --> aborted: abort
    verified --> [*]
    aborted --> [*]
```

## 7. Hook and Guardrail Plane

```mermaid
flowchart TD
    Event[Host or Runtime Event] --> HookRouter[Hook Router]
    HookRouter --> Risk[Risk Classifier]
    Risk --> Policy[Policy Engine]
    Policy --> Decision{Verdict}
    Decision -->|allow| Execute[Execute]
    Decision -->|warn| ExecuteWarn[Execute with warning]
    Decision -->|block| Block[Block with reason]
    Execute --> Evidence[Evidence Candidate]
    ExecuteWarn --> Evidence
    Block --> Incident[Incident Created]
    Evidence --> Trace[Trace Event]
    Incident --> Trace
    Trace --> Ledger[Mission Ledger]
```

## 8. Pack activation

```mermaid
flowchart LR
    Source[Pack Source] --> Discover[Discover]
    Discover --> Validate[Validate Manifest]
    Validate --> Lock[Compute Lock]
    Lock --> Doctor[Run Doctor Checks]
    Doctor --> Policy[Activation Policy]
    Policy --> Verdict{Activation Verdict}
    Verdict -->|block| Quarantine[Quarantined]
    Verdict -->|warn| Canary[Active Canary]
    Verdict -->|allow| Shadow[Active Shadow]
    Shadow --> Promote[Promote after proof]
    Canary --> Promote
    Promote --> Enforced[Active Enforced]
    Enforced --> Runtime[Runtime Kernel]
```

## 9. Memory OS flow

```mermaid
flowchart TD
    Task[Task Context] --> RecallReq[Recall Request]
    RecallReq --> Policy[Memory Policy]
    Policy --> Hot[Hot Memory]
    Policy --> Vector[Weaviate Vector Memory]
    Policy --> Graph[Neo4j Code and Docs Graph]
    Hot --> Merge[Context Merge]
    Vector --> Merge
    Graph --> Merge
    Merge --> Freshness[Freshness and Contradiction Check]
    Freshness --> Capsule[Context Capsule]
    Capsule --> Agent[Agent or Workflow]
    Agent --> Output[Output]
    Output --> Candidate[Promotion Candidate]
    Candidate --> Verify[Promotion Gate]
    Verify --> Store[Weaviate and Neo4j Stores]
    Store --> Trace[Memory Event]
```

## 10. Data stores et ownership

```mermaid
erDiagram
    MISSION ||--o{ TASK : contains
    TASK ||--o{ TASK_DEPENDENCY : declares
    TASK ||--o{ WORKFLOW_INSTANCE : executes
    WORKFLOW_INSTANCE ||--o{ RUN_EVENT : emits
    WORKFLOW_INSTANCE ||--o{ CHECKPOINT : saves
    TASK ||--o{ EVIDENCE_PACK : proves
    EVIDENCE_PACK ||--o{ EVIDENCE_ITEM : contains
    TASK ||--o{ VERIFICATION_VERDICT : closes
    TASK ||--o{ INCIDENT : raises
    TASK ||--o{ MEMORY_REF : uses
    PACK ||--o{ PACK_ACTIVATION : activates
    PACK ||--o{ POLICY_RULE : declares
    HOST ||--o{ HOST_SESSION : opens
    HOST_SESSION ||--o{ RUN_EVENT : emits
```

## 11. Host Bridge routing

```mermaid
flowchart TD
    Request[Execution Request] --> Cap[Capability Manifest]
    Cap --> Hooks{Hooks supported}
    Cap --> MCP{MCP supported}
    Cap --> Mutation{Workspace mutation supported}
    Hooks -->|yes| HookMode[Native Hook Mode]
    Hooks -->|no| FallbackMode[CLI API Fallback]
    MCP -->|yes| MCPTools[MCP Tool Mediation]
    MCP -->|no| LocalTools[Local Tool Wrapper]
    Mutation -->|yes| StrictPolicy[Strict Mutation Policy]
    Mutation -->|no| ReadOnly[Read Only or Report Mode]
    HookMode --> Runtime[Runtime Kernel]
    FallbackMode --> Runtime
    MCPTools --> Runtime
    LocalTools --> Runtime
    StrictPolicy --> Runtime
    ReadOnly --> Runtime
```

## 12. Interop externe

```mermaid
flowchart LR
    ExternalAgent[External Agent System] --> Adapter[Adapter]
    Adapter --> Normalize[Normalize Task Message Artifact]
    Normalize --> Policy[Policy Boundary]
    Policy --> Runtime[Runtime Kernel]
    Runtime --> Ledger[Mission Ledger]
    Runtime --> Trace[Trace Ledger]
    Runtime --> Evidence[Evidence Service]
    Evidence --> Adapter
    Adapter --> ExternalAgent
```

Regle :

- l'agent externe peut executer ;
- Grimoire conserve task, policy, trace, evidence et closure.

## 13. Deploiements cibles

### 13.1 Local developer

```mermaid
flowchart TD
    Repo[Workspace Repo] --> Forge[Grimoire Forge]
    Forge --> Kit[grimoire-kit local]
    Kit --> SQLite[(SQLite Ledger)]
    Kit --> Files[(Evidence Files)]
    Kit --> LocalVector[(Local Vector Store)]
    Kit --> MCP[MCP stdio]
    Kit --> IDE[IDE Host]
```

### 13.2 Team shared

```mermaid
flowchart TD
    Users[Team Users] --> Cockpit[Shared Cockpit]
    Cockpit --> API[Grimoire API]
    API --> Ledger[(Shared Ledger)]
    API --> ObjectStore[(Evidence Store)]
    API --> Vector[(Vector DB)]
    API --> Trace[(Trace Store)]
    API --> Registry[(Pack Registry)]
    API --> Runners[Agent Runners]
    Runners --> Sandboxes[Sandboxed Tools]
```

### 13.3 Enterprise controlled

```mermaid
flowchart TD
    SSO[Identity Provider] --> Gateway[Grimoire Gateway]
    Gateway --> Policy[Central Policy]
    Gateway --> Cockpit[Enterprise Cockpit]
    Cockpit --> Runtime[Runtime Cluster]
    Runtime --> Ledger[(HA Ledger)]
    Runtime --> Evidence[(Encrypted Evidence)]
    Runtime --> Trace[(Observability)]
    Runtime --> Memory[(Governed Memory)]
    Runtime --> Registry[(Approved Pack Registry)]
    Runtime --> Audit[(Audit Export)]
```

## 14. Trust boundaries

```mermaid
flowchart TD
    subgraph TrustedCore[Trusted Core]
        Kernel[Runtime Kernel]
        Ledger[Mission Ledger]
        Policy[Policy Engine]
        Evidence[Evidence Service]
    end

    subgraph Controlled[Controlled Extensions]
        Packs[Reviewed Packs]
        Providers[Host Providers]
        Memory[Memory Stores]
    end

    subgraph Untrusted[Untrusted Inputs]
        Web[Web Content]
        ExternalRepos[External Repos]
        ExternalAgents[External Agents]
        UserFiles[User Files]
    end

    Untrusted --> Sanitize[Sanitize and Classify]
    Sanitize --> Policy
    Controlled --> Policy
    Policy --> TrustedCore
    TrustedCore --> Audit[Audit Trail]
```

## 15. Projection cockpit

```mermaid
flowchart LR
    Ledger[Mission Ledger] --> ReadModel[Read Model Builder]
    EventLog[Event Log] --> ReadModel
    Evidence[Evidence Store] --> ReadModel
    Trace[Trace Store] --> ReadModel
    Memory[Weaviate Vector Store] --> ReadModel
    Graph[Neo4j Graph Store] --> ReadModel
    Packs[Pack Registry] --> ReadModel
    ReadModel --> API[Cockpit API]
    API --> Board[Task Graph View]
    API --> Workflow[Workflow View]
    API --> Policy[Policy View]
    API --> EvidenceView[Evidence View]
    API --> MemoryView[Memory View]
    API --> PackView[Pack View]
```

## 16. Schema mental final

```text
Forge = preuve vivante et cockpit.
kit = noyau distribuable.
ledger = source de verite.
runtime = execution.
policy = controle.
evidence = fermeture.
memory = contexte gouverne.
packs = extension.
trace = mesure.
adapters = interop.
```
