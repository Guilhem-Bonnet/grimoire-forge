---
title: Matrice de fusion - Projets agentiques vers Grimoire
description: Decisions de fusion, absorption, rejet ou incubation pour Gastownhall et les autres projets de reference.
author: Codex
date: 2026-05-08
---

# Matrice de fusion - Projets agentiques vers Grimoire

## Regle

Fusionner ne veut pas dire copier un repo dans Grimoire.

Fusionner veut dire :

- extraire une primitive ;
- la traduire dans le vocabulaire Grimoire ;
- definir un contrat ;
- creer un adaptateur ou un pack ;
- ajouter des guardrails ;
- produire une preuve ;
- promouvoir seulement si la primitive reste utile dans Forge et grimoire-kit.

## Gastownhall complet

| Source | Decision | Ce qu'on prend | Comment fusionner | Ce qu'on refuse |
| --- | --- | --- | --- | --- |
| `gastown` | Reference forte | Mayor comme point d'entree unique, rigs, convoys, provider tiers, hooks, dogfood multi-agent | Traduire en `grimoire-master`, `Mission Bundle`, `Host Bridge Providers`, hooks Grimoire | Vocabulaire produit, filesystem comme architecture, roles source comme UX principale |
| `beads` | Core concept + adapter | Work graph, dependencies, ready query, hash ids, comments/events, multi-repo routing | Creer `Mission Ledger` Grimoire-native + import/export Beads JSONL + event mapping | Dolt obligatoire, backend unique, pollution `.beads` dans le noyau |
| `gascity` | Core concept + selective port | Runtime providers, supervisor, orders, formulas, city config, pack composition | Traduire en `Runtime Kernel`, `WorkflowInstance`, `Order`, `Pack Registry`, `Provider Capability` | tmux obligatoire, Go SDK comme dependance, roles codifies |
| `gascity-packs` | Pack importer experimental | `pack.toml`, commands, doctor, services, formulas, tests | Convertisseur `pack.toml -> pack.yaml`, packs experimentaux controles | Activation transitive, commandes shell sans policy |
| `gascity-otel` | Adapter optionnel | Metriques agent lifecycle, storage, token usage, Grafana dashboards | OTel exporter depuis `RunEvent` et `PolicyVerdict`, stack compose optionnelle | Capturer prompts, tool outputs ou secrets par defaut |
| `docs` | Reference documentation | Mintlify-style docs, quickstart, references, API docs | Adapter au site/docs grimoire-kit | Dupliquer docs Forge et kit sans ownership |
| `community` | Reference ecosysteme | Transparence, contributor-first, launches, support loop | Playbook ecosysteme Grimoire-first | Faire du marketing avant preuve produit |
| `wasteland` | Incubator | Federation, commons, trust network | `Grimoire Commons` experimental apres pack registry et verification | Le mettre dans le noyau avant gouvernance |

## Autres projets a fusionner ou utiliser

| Projet | Decision | Primitive utile | Integration Grimoire |
| --- | --- | --- | --- |
| LangGraph | Reference core | Durable execution, checkpointer, interrupt/resume, time travel | Pattern pour `WorkflowInstance`, `Checkpoint`, idempotence et side effects bornes |
| OpenAI Agents SDK | Reference core | Agents-as-tools, handoffs, guardrails, tracing | Pattern pour `Host Bridge`, `PolicyVerdict`, trace spans et choix handoff vs tool |
| Microsoft Agent Framework | Reference | Workflows typables, agent orchestration, sessions | Comparaison pour recipes et workflow taxonomy |
| CrewAI | Fusion selective | Crews, Flows, Tasks, task guardrails, output schemas, checkpointing, Knowledge, MCP DSL, tracing, test/train | Importer projets CrewAI en packs experimentaux, mapper Flows vers Recipes, adapter CrewAI comme runner externe sans remplacer le kernel |
| Langfuse | Adapter | Trace, evals, prompt observability | Export OTel/Langfuse depuis trace canonique, pas source de verite |
| OpenTelemetry GenAI | Core standard | Semantic conventions GenAI, model spans, agent spans, MCP | Schema d'export observabilite |
| MCP | Core standard | Tool protocol, resources, auth, stdio constraints | Transport principal quand disponible, policy fail-closed |
| A2A | Core standard | AgentCard, Task, Message, Artifact, Extensions | Interop externe agent-agent avec capabilities et policies |
| OWASP Agentic Applications | Core security | Risques agents autonomes, tool misuse, memory poisoning | Red-team harness et gates security |
| OWASP Agentic Skills | Core security | Supply chain skills, permissions, provenance | Pack Registry, skill registry scanning et trust tiers non sociaux |
| CodeGraphContext | Fusion selective | Repo context, symbol graph, retrieval code | `grimoire_code` collection + graph SQLite |
| Graphify | Fusion selective | Graph extraction, links code/doc | Code graph et doc graph pour Memory OS |
| MemPalace | Reference memory | Memory architecture, recall structured | Inspiration pour Memory OS, pas backend unique |
| LLMLingua | Adapter possible | Compression contexte | Pre-prompt context shaping en mode borne |
| LLMSecurityGuide | Core security | Secure agent patterns, least privilege | Policies hooks, MCP allowlist, pack activation guard |
| agent-sandbox | Fusion selective | Sandboxed execution | Provider sandbox pour tools mutateurs et pack commands |
| OpenHands | Reference | Agent coding environment, action/observation loop | Comparaison pour executor et workspace mutation governance |
| browser-use | Adapter possible | Browser automation | Tool provider browser borne par policies |
| Dify | Reference product | App workflow builder, dataset/RAG UX | Inspiration UI packs/workflows, pas noyau |
| Langflow | Reference product | Visual graph workflow editing | Inspiration future workflow visualizer |
| kagent | Adapter future | Kubernetes agent orchestration | Provider K8s optionnel apres kernel stable |
| Switchboard | Fusion selective | Board d'operations et task routing | Mission Board, routing matrix, kanban causal |
| pixel-agents | Reference UI | Visual agent cockpit patterns | Inspiration UI, pas contrat metier |
| agent-skills / claude-skills / superpowers | Fusion selective | Skills comme units distribuables | Pack Registry + skill security + provenance |

## Priorite d'absorption

| Rang | Fusion | Raison |
| --- | --- | --- |
| 1 | Beads -> Mission Ledger | Sans ledger, pas de task graph durable ni de nettoyage des plans. |
| 2 | Gas City packs -> Pack Registry | Sans packs gouvernes, Grimoire ne devient pas distribuable. |
| 3 | Gas City formulas/orders -> Workflow Instances | Sans instances, les workflows restent des textes. |
| 4 | Gas City supervisor -> Runtime Kernel | Sans supervisor, les agents restent pilotables mais pas gouvernes. |
| 5 | CrewAI Flows/Tasks -> Recipes et task contracts | Sans contrat de task et workflow ergonomique, le kernel sera puissant mais trop difficile a utiliser. |
| 6 | Hooks Grimoire + OWASP -> Guardrail Plane | Sans gates, l'autonomie devient fragile. |
| 7 | OTel + Langfuse -> Trace/Eval Ledger | Sans observabilite, impossible de prouver performance et regressions. |
| 8 | CodeGraphContext/Graphify -> Code Graph | Sans code graph, les agents chargent trop et comprennent mal l'impact. |
| 9 | A2A + MCP -> External Interop | Sans interop, Grimoire reste IDE-native mais pas Agent OS. |
| 10 | Community/docs Gastownhall -> Ecosystem Layer | Sans adoption, le kit reste interne. |

## Patterns de migration

### Pattern 1 - Importer une primitive de ledger

```text
bd issue JSONL
-> grimoire ledger import
-> MissionTask
-> dependencies
-> evidence refs
-> Mission Board projection
```

Gate :

- ids stables ;
- source repo conservee ;
- dependencies valides ;
- import idempotent ;
- pas de close sans evidence.

### Pattern 2 - Convertir un pack Gas City

```text
pack.toml
-> grimoire pack convert
-> pack.yaml
-> pack.lock.json
-> doctor checks
-> commands en mode disabled par defaut
-> activation par policy
```

Gate :

- commandes shell deny par defaut ;
- doctor read-only ;
- services en sandbox ou adapter declare ;
- hash de contenu ;
- provenance lisible.

### Pattern 3 - Promouvoir un workflow

```text
formula source
-> Recipe
-> WorkflowInstance
-> RunEvent
-> Checkpoint
-> EvidencePack
-> VerificationVerdict
```

Gate :

- resume idempotent ;
- side effects identifies ;
- abort reason ;
- replay lisible.

### Pattern 4 - Ajouter un provider host

```text
Provider externe
-> Capability Manifest
-> Host Bridge Driver
-> Policy Pack
-> Hook adapter si disponible
-> CLI/API fallback
-> trace canonique
```

Gate :

- aucune mutation sans hostId ;
- aucun tool mutateur sans policy ;
- degradation si hooks absents ;
- trace et evidence compatibles.

## Decision de non-fusion directe

Les repos externes ne doivent pas etre vendores dans le noyau par defaut.

Acceptable :

- adaptateur ;
- convertisseur ;
- pack experimental ;
- fixture de test ;
- documentation de migration ;
- export/import.

Non acceptable :

- copie brute sans ownership ;
- dependance runtime obligatoire non necessaire ;
- format canonique concurrent ;
- command shell activee sans policy ;
- backend externe comme source unique de verite.
