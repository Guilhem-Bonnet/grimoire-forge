---
title: Addendum CrewAI - comparaison et fusion
description: Analyse ciblee de CrewAI pour completer la matrice de fusion Grimoire Agent OS.
author: Codex
date: 2026-05-08
---

# Addendum CrewAI - comparaison et fusion

## Reponse honnete

Non, CrewAI n'avait pas encore ete traite au meme niveau que Gastownhall.

Il etait cite dans les anciens rapports comme reference multi-agent, mais sans decision de fusion complete. Ce document corrige ce manque.

## Sources analysees

| Source | Signal exploite |
| --- | --- |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/README.md` | Positionnement Crews + Flows, AMP Suite, skills officielles pour agents codeurs. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/crews.mdx` | Attributs Crew : agents, tasks, process, memory, planning, knowledge, tracing, skills, security, checkpoint. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/tasks.mdx` | Task contract : expected output, context, tools, output JSON/Pydantic, guardrails, human input. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/processes.mdx` | Process sequential et hierarchical, consensual planifie. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/flows.mdx` | Flows event-driven avec `@start`, `@listen`, `@router`, state et plot. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/checkpointing.mdx` | Checkpointing crew/flow/agent, restore, fork, JsonProvider et SqliteProvider. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/memory.mdx` | Memoire unifiee, scopes hierarchiques, extraction, recall composite, memory dans crews/agents/flows. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/knowledge.mdx` | Knowledge sources, ChromaDB par defaut, Qdrant supporte, sources text/PDF/CSV/Excel/JSON/web. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/tools.mdx` | Taxonomie tools, MCPs, Apps, Skills, Knowledge. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/mcp/overview.mdx` | MCP comme tools via DSL agent, stdio, HTTP, SSE, filters, cache. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/observability/tracing.mdx` | Tracing Crews/Flows, agent decisions, task timeline, tools, LLM calls, metrics. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/testing.mdx` | CLI `crewai test` pour evaluer crews. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/docs/en/concepts/training.mdx` | CLI `crewai train`, feedback humain, suggestions persistantes. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/lib/crewai/src/crewai/` | Code local : modules `a2a`, `flow/persistence`, `events`, `mcp`, `knowledge`, `memory`, `hooks`, CLI checkpoint/test/train. |

Sources docs verifiees via Context7 :

- [CrewAI Crews](https://docs.crewai.com/en/concepts/crews)
- [CrewAI Tasks](https://docs.crewai.com/en/concepts/tasks)
- [CrewAI Processes](https://docs.crewai.com/en/concepts/processes)
- [CrewAI Flows](https://docs.crewai.com/en/concepts/flows)
- [CrewAI Checkpointing](https://docs.crewai.com/en/concepts/checkpointing)
- [CrewAI Memory](https://docs.crewai.com/en/concepts/memory)
- [CrewAI Knowledge](https://docs.crewai.com/en/concepts/knowledge)
- [CrewAI MCP](https://docs.crewai.com/en/mcp/overview)
- [CrewAI Tracing](https://docs.crewai.com/en/observability/tracing)

## Ce que CrewAI fait mieux que Grimoire aujourd'hui

| Axe | Signal CrewAI | Lecon pour Grimoire |
| --- | --- | --- |
| Developer ergonomics | `crewai create crew`, YAML agents/tasks, decorators `@agent`, `@task`, `@crew` | Grimoire doit offrir un scaffold pack/recipe plus simple. |
| Workflow DSL | Flows avec `@start`, `@listen`, `@router` et state Pydantic | Bonne inspiration pour un DSL `Recipe` Python ou YAML. |
| Output contracts | `output_json`, `output_pydantic`, `TaskOutput`, `CrewOutput` | Grimoire doit rendre les outputs de tasks typables et verifiables. |
| Task guardrails | Guardrails par task avec retries | A traduire en `Verification Profile` et `Policy Verdict`, pas seulement prompt guidance. |
| Checkpointing | Restore/fork pour Crew, Flow et Agent | Confirme que `Checkpoint` et branch lineage sont noyau, pas option. |
| Knowledge sources | Text, PDF, CSV, Excel, JSON, web, Qdrant support | A absorber dans `PackKnowledgeSource` et Memory OS. |
| MCP integration | DSL `mcps` sur agents, stdio/HTTP/SSE, filters | Inspiration forte pour `Capability Manifest` et tool filters. |
| Observability | Tracing Crews/Flows + integrations nombreuses | Grimoire doit exporter ses traces canoniques, pas inventer un format ferme. |
| Testing/training | CLI de test/eval et boucle feedback humain | A adapter en eval ledger et learning candidate gate. |
| A2A local code | Module `a2a` dans le repo local | Confirme que A2A doit etre dans Track I. |

## Ce que Grimoire doit garder comme avantage

| Axe | Avantage Grimoire |
| --- | --- |
| IDE-native | Grimoire vit deja dans Copilot, Claude, Codex et le repo. |
| Source de verite projet | Mission Ledger + Evidence + Board doivent rester au-dessus du runtime externe. |
| Hooks host | Grimoire a une vraie surface de hooks host avec registry et modes. |
| Cockpit visuel | Mission Board et grimoire-game donnent un wedge produit plus distinctif. |
| Memory OS gouverne | Grimoire peut imposer provenance, fraicheur, task refs et code graph. |
| Pack governance | Grimoire peut combiner skills, hooks, policies, tools, docs et assets dans un pack verifie. |

## Decision de fusion

| Primitive CrewAI | Decision | Traduction Grimoire |
| --- | --- | --- |
| `Agent` | Absorber partiellement | `AgentCapability` ou agent interne, jamais nouvel acteur user-facing par defaut. |
| `Task` | Absorber fortement | Renforcer `MissionTask` : expected output, context refs, output schema, human input, guardrails. |
| `Crew` | Absorber comme execution team | `ExecutionTeam` interne liee a une `WorkflowInstance`. |
| `Process.sequential` | Absorber | `WorkflowStrategy.sequential`. |
| `Process.hierarchical` | Absorber avec garde-fous | `WorkflowStrategy.manager_routed` avec policy et trace du manager. |
| Consensual process | Incubator | Mode challenge/consensus plus tard, jamais prerequis noyau. |
| `Flow` | Absorber fortement | `Recipe` event-driven avec `start/listen/router` ou equivalent YAML. |
| `Flow state` Pydantic | Absorber | `WorkflowState` type et versionne. |
| Checkpoint restore/fork | Absorber fortement | `Checkpoint`, `BranchLineage`, `RunFork`. |
| Task guardrails | Absorber | `VerificationProfile`, `PolicyVerdict`, retries bornes. |
| Memory scopes | Absorber avec restrictions | `MemoryScope` dans Memory OS, mais promotion gouvernee. |
| Knowledge sources | Absorber | `PackKnowledgeSource` + Qdrant/local index. |
| Tools taxonomy | Absorber fortement | Capacites : `tool`, `mcp`, `app`, `skill`, `knowledge`. |
| MCP DSL | Absorber partiellement | Declarer tool servers dans pack/provider manifest, deny par defaut. |
| Tracing | Absorber via standard | Export OTel/Langfuse/AMP optional depuis trace canonique. |
| `crewai test` | Absorber concept | `grimoire eval run` sur Mission Packs. |
| `crewai train` | Incubator controle | Learning candidates + human feedback, pas fichier `.pkl` comme source canonique. |
| AMP control plane | Adapter optionnel | Ne jamais devenir control plane obligatoire de Grimoire. |

## Comment le fusionner proprement

### Mode 1 - Import de projet CrewAI

```text
agents.yaml + tasks.yaml + crew.py
-> grimoire crewai import
-> pack.yaml
-> AgentCapability[]
-> MissionTask template[]
-> Recipe
-> VerificationProfile
```

Gates :

- outputs typables ;
- tools et MCP deny par defaut ;
- tasks avec provenance ;
- aucune memoire auto-promue sans policy ;
- import idempotent.

### Mode 2 - Adaptateur runtime CrewAI

```text
CrewAI Crew/Flow
-> ExternalWorkflowRunner
-> WorkflowInstance
-> RunEvent stream
-> Checkpoint/Evidence
-> VerificationQueue
```

Gates :

- CrewAI reste runner externe ;
- Grimoire garde ledger, evidence et board ;
- traces CrewAI sont mappees vers RunEvent ;
- erreurs deviennent incidents Grimoire ;
- pas de fermeture sans verification Grimoire.

### Mode 3 - Traduction Flow vers Recipe

```text
@start / @listen / @router
-> Recipe graph
-> WorkflowState schema
-> branch conditions
-> checkpoints
-> cockpit flow view
```

Gates :

- state Pydantic ou schema JSON ;
- routers explicites ;
- side effects declares ;
- resume idempotent.

### Mode 4 - Knowledge source pack

```text
CrewAI Knowledge Source
-> PackKnowledgeSource
-> ingestion policy
-> Qdrant/local index
-> MemoryRef
-> recall guard
```

Gates :

- source path ou URL explicite ;
- hash et freshness ;
- scope ;
- poison checks ;
- pas de recall critique sans provenance.

### Mode 5 - Eval et training controle

```text
crewai test/train pattern
-> Grimoire Eval Ledger
-> human feedback event
-> learning candidate
-> verification before promotion
```

Gates :

- feedback humain versionne ;
- suggestions non appliquees automatiquement au noyau ;
- promotion par evidence ;
- pas de `.pkl` opaque comme contrat durable.

## Ce qu'il ne faut pas faire

| Anti-pattern | Pourquoi |
| --- | --- |
| Remplacer le Runtime Kernel par CrewAI | Grimoire perdrait son controle IDE-native, ledger, hooks et cockpit. |
| Importer CrewAI comme dependance obligatoire | Grimoire doit rester host-agnostic et provider-agnostic. |
| Laisser CrewAI memory ecrire directement dans Memory OS | Risque de memoire non prouvee et auto-organisee sans provenance suffisante. |
| Brancher AMP comme cockpit principal | Grimoire doit garder son cockpit comme projection du ledger. |
| Copier `crewai train` tel quel | Le feedback doit devenir evidence/learning candidate, pas prompt patch opaque. |
| Utiliser le planning implicite comme source de verite | Le plan doit etre materialise en tasks/recipes/checkpoints Grimoire. |

## Backlog ajoute

| ID | Titre | Track |
| --- | --- | --- |
| `GAO-F004` | Importer projet CrewAI vers pack Grimoire experimental | Pack Registry |
| `GAO-D003` | Mapper CrewAI Flow vers Recipe Grimoire | Workflow Instances |
| `GAO-I004` | Adapter runtime CrewAI comme ExternalWorkflowRunner | Host Bridge |
| `GAO-G004` | Mapper CrewAI Knowledge/Memory scopes vers Memory OS | Memory OS |
| `GAO-J004` | Adapter patterns `crewai test/train` vers Eval Ledger | Observabilite et evals |

## Verdict

CrewAI est plus important que je ne l'avais capture dans le plan initial.

Il ne doit pas devenir le noyau de Grimoire, mais il doit devenir une reference de premier niveau pour :

- task contracts ;
- workflow DSL ;
- checkpoint/fork ;
- output schemas ;
- task guardrails ;
- knowledge sources ;
- MCP tool declaration ;
- tracing/evals ;
- agent coding skills.

La posture recommandee : importer, convertir, adapter et verifier. Pas remplacer.

