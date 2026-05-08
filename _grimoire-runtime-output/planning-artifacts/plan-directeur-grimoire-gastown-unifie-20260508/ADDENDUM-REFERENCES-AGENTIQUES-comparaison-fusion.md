---
title: Addendum references agentiques - comparaison et fusion
description: Fiches de decision pour chaque projet du corpus Reference-Agentique et traduction vers Grimoire Agent OS.
author: Codex
date: 2026-05-08
---

# Addendum references agentiques - comparaison et fusion

## But

Ce document applique le meme exercice que l'addendum CrewAI a chaque projet du corpus local :

`/mnt/Travail/Projets/Dev/Référence-Agentique/`

Chaque fiche repond a quatre questions :

- quoi prendre ;
- comment le traduire dans Grimoire ;
- quoi refuser ;
- quel garde-fou appliquer.

## Regles de decision

| Decision | Sens |
| --- | --- |
| `core-reference` | Influence directe sur le noyau Grimoire. |
| `fusion-selective` | Primitive utile a absorber par contrat ou pack. |
| `adapter` | A connecter comme runner, provider, exporter ou importer. |
| `incubator` | Idee interessante mais hors noyau. |
| `source-doc` | Reference pedagogique ou documentaire. |
| `reject-as-core` | Ne doit pas devenir dependance ou architecture principale. |

## Synthese executive

| Projet | Decision | Integration prioritaire |
| --- | --- | --- |
| `BMAD-METHOD` | `fusion-selective` | Templates, roles, workflows, governance docs vers Pack Registry. |
| `CodeGraphContext` | `core-reference` | Code graph, context packing, MCP/code retrieval vers Memory OS. |
| `Design/ui` | `source-doc` | Reference UI components, pas agentique. |
| `LLMLingua` | `adapter` | Compression contexte et prompt budget. |
| `LLMSecurityGuide` | `core-reference` | Security gates, red-team harness, MCP/tool/memory poisoning checks. |
| `Octogent` | `incubator` | Multi-agent desktop/operator patterns, pas noyau. |
| `OpenHands` | `adapter` | Workspace executor et action/observation loop sous policy. |
| `OpenMythos` | `incubator` | Narrative/model training ideas, pas prioritaire. |
| `agent-framework` | `core-reference` | Workflows typables, A2A/MCP, .NET/Python interop. |
| `agent-sandbox` | `core-reference` | Isolation stateful singleton workloads pour tools mutateurs. |
| `agent-skills` | `fusion-selective` | Skills distribuables, install/pack metadata. |
| `ai-agents-for-beginners` | `source-doc` | Curriculum et checklists pedagogiques. |
| `andrej-karpathy-skills` | `source-doc` | Coding-agent discipline et instruction style. |
| `autogen` | `adapter` | Conversation multi-agent et group chat comme runner externe. |
| `browser-use` | `adapter` | Browser automation provider borne par policy. |
| `claude-skills` | `fusion-selective` | Skill packaging, activation contextuelle. |
| `crewAI` | `fusion-selective` | Voir addendum CrewAI. |
| `dify` | `adapter` | Workflow/RAG/app-builder UX et dataset ops. |
| `gas town/*` | `fusion-selective` | Voir analyse Gastownhall complete. |
| `graphify` | `core-reference` | Graph extraction code/docs vers Code Graph. |
| `haystack` | `core-reference` | Pipelines RAG, routing, evaluation et retrieval components. |
| `kagent` | `adapter` | Kubernetes/cloud-native agent runtime futur. |
| `langflow` | `adapter` | Visual flow builder, import/export workflows. |
| `langfuse` | `adapter` | Observability, tracing, evals, prompt/version tracking. |
| `langgraph` | `core-reference` | Durable execution, checkpoints, graph runtime. |
| `mempalace` | `fusion-selective` | Memory palace/scoped recall concepts. |
| `openai-agents-python` | `core-reference` | Agent primitives, handoffs, guardrails, tracing. |
| `openclaw` | `incubator` | Personal assistant shell, hooks, local UX ideas. |
| `pixel-agents` | `source-doc` | Game/cockpit metaphor and operator UI. |
| `ruflo` | `incubator` | Claude Code orchestration and self-learning patterns. |
| `shannon` | `core-reference` | AI pentest/red-team flows. |
| `superpowers` | `fusion-selective` | Skill distribution and Claude marketplace style. |
| `switchboard` | `fusion-selective` | Agent team board, task dispatch, operator routing. |
| `vscode-copilot-chat` | `core-reference` | Host bridge, IDE-native agent UX, MCP/customization. |

## Fiches par projet

### BMAD-METHOD

Decision : `fusion-selective`.

Primitives utiles :

- role catalog ;
- workflows de delivery ;
- templates PRD/architecture/story ;
- module ecosystem ;
- discipline "agent-driven agile development".

Traduction Grimoire :

- packs `methodology`;
- templates de mission ;
- recipes documentaires ;
- gates de Definition of Ready et Definition of Done ;
- source de migration pour anciens concepts BMAD deja dans Grimoire.

Refus :

- ne pas garder deux taxonomies agentiques concurrentes ;
- ne pas laisser BMAD redevenir le centre de gravite runtime.

Garde-fou :

- tout role BMAD absorbe devient agent interne, recipe ou skill ; le point user-facing reste `grimoire-master`.

### CodeGraphContext

Decision : `core-reference`.

Primitives utiles :

- indexation code ;
- context graph ;
- MCP/code context ;
- retrieval oriente symboles ;
- contexte agent compact.

Traduction Grimoire :

- `grimoire_code` collection ;
- graph SQLite symboles/tests/fichiers ;
- code impact view ;
- recall code borne dans Memory OS.

Refus :

- ne pas remplacer le Mission Ledger par un code graph ;
- ne pas injecter tout le contexte code dans les prompts.

Garde-fou :

- chaque chunk code doit pointer vers fichier, symbole, test, hash et freshness.

### Design/ui

Decision : `source-doc`.

Primitives utiles :

- conventions UI ;
- composants shadcn ;
- patterns d'interface.

Traduction Grimoire :

- inspiration pour composants cockpit ;
- pas de primitive agentique.

Refus :

- ne pas faire du design system une source de verite runtime.

Garde-fou :

- UI lit les read models, jamais l'inverse.

### LLMLingua

Decision : `adapter`.

Primitives utiles :

- compression prompt ;
- budget contexte ;
- reduction du bruit ;
- preparation RAG/context.

Traduction Grimoire :

- `ContextCompressionProvider`;
- hook `UserPromptSubmit` ou pre-dispatch ;
- compression des memory recalls ;
- evaluation de perte d'information.

Refus :

- ne pas compresser les preuves brutes ;
- ne pas compresser sans trace quand le run est critique.

Garde-fou :

- garder original ref + compressed ref + score de confiance.

### LLMSecurityGuide

Decision : `core-reference`.

Primitives utiles :

- prompt injection ;
- tool misuse ;
- data exfiltration ;
- MCP risk ;
- memory poisoning ;
- least privilege ;
- supply-chain.

Traduction Grimoire :

- red-team harness ;
- pack policy ;
- MCP allowlist ;
- memory provenance gate ;
- security evidence profile.

Refus :

- ne pas traiter la securite comme doc externe seulement.

Garde-fou :

- chaque pack/tool mutateur doit passer un profil `security_critical` si la surface est sensible.

### Octogent

Decision : `incubator`.

Primitives utiles :

- autonomous multi-agent operator UX ;
- local workspace ;
- model/tool bootstrap ;
- possible desktop patterns.

Traduction Grimoire :

- inspiration pour cockpit et operator loop ;
- eventuellement pack experimental local assistant.

Refus :

- ne pas importer comme runtime ;
- ne pas multiplier les assistants user-facing.

Garde-fou :

- toute idee Octogent passe par Mission Board ou Host Bridge, pas par un second orchestrateur.

### OpenHands

Decision : `adapter`.

Primitives utiles :

- software agent SDK ;
- workspace mutation loop ;
- browser/frontend surface ;
- evaluation/dev environment ;
- action/observation patterns.

Traduction Grimoire :

- `ExternalWorkspaceExecutor`;
- sandbox mutating tool provider ;
- evidence from action/observation ;
- comparison harness for coding agents.

Refus :

- ne pas remplacer Codex/Copilot/Claude host flow ;
- ne pas donner acces workspace mutateur sans policy.

Garde-fou :

- preview -> policy -> bounded mutation -> validation -> evidence.

### OpenMythos

Decision : `incubator`.

Primitives utiles :

- model/story/narrative workflows ;
- training/eval ideas ;
- possible synthetic data patterns.

Traduction Grimoire :

- incubateur pour creative/knowledge packs ;
- pas prioritaire pour kernel.

Refus :

- ne pas lier le noyau a un workflow narratif.

Garde-fou :

- experimental pack uniquement.

### agent-framework

Decision : `core-reference`.

Primitives utiles :

- Microsoft Agent Framework ;
- workflows sequentiels/concurrents/handoff ;
- typed outputs ;
- MCP/A2A ;
- multi-language .NET/Python.

Traduction Grimoire :

- benchmark pour `WorkflowInstance`;
- schema interop ;
- host bridge enterprise ;
- A2A contract tests.

Refus :

- ne pas importer un second framework comme noyau obligatoire.

Garde-fou :

- compatibilite par adapter et tests contractuels.

### agent-sandbox

Decision : `core-reference`.

Primitives utiles :

- isolated stateful singleton workloads ;
- API/control plane ;
- Kubernetes patterns ;
- sandbox lifecycle.

Traduction Grimoire :

- `SandboxProvider`;
- pack command isolation ;
- external tool execution ;
- unsafe tool quarantine.

Refus :

- ne pas rendre Kubernetes obligatoire.

Garde-fou :

- tout outil mutateur a risque eleve doit pouvoir etre route vers sandbox ou etre refuse.

### agent-skills

Decision : `fusion-selective`.

Primitives utiles :

- skills installables ;
- skill catalog ;
- infrastructure/domain skills ;
- package metadata.

Traduction Grimoire :

- `SkillComponent` dans `pack.yaml`;
- import skills ;
- scanning supply-chain ;
- compatibility matrix.

Refus :

- ne pas installer une skill comme code de confiance par defaut.

Garde-fou :

- provenance, hash, permissions et status requis.

### ai-agents-for-beginners

Decision : `source-doc`.

Primitives utiles :

- curriculum agents ;
- design patterns ;
- tool use ;
- RAG ;
- trustworthiness ;
- protocols ;
- memory.

Traduction Grimoire :

- documentation d'enseignement ;
- checklists onboarding ;
- examples de recipes.

Refus :

- ne pas prendre comme architecture produit.

Garde-fou :

- utiliser comme support pedagogique, pas source de verite.

### andrej-karpathy-skills

Decision : `source-doc`.

Primitives utiles :

- style de travail coding agents ;
- think before coding ;
- simplicity ;
- verification ;
- code discipline.

Traduction Grimoire :

- guide de comportement agents ;
- hooks de rappel proceduriel ;
- lint de plans trop flous.

Refus :

- ne pas transformer guidelines en blocages automatiques agressifs.

Garde-fou :

- guidance en `UserPromptSubmit` ou skill, pas policy dure sauf cas deterministe.

### autogen

Decision : `adapter`.

Primitives utiles :

- multi-agent conversations ;
- group chat ;
- agent runtime ;
- tools ;
- Studio/no-code ;
- A2A/MCP signals.

Traduction Grimoire :

- `ExternalConversationRunner`;
- import conversation trace ;
- group discussion recipe ;
- comparison harness.

Refus :

- ne pas faire du chat multi-agent la source de verite du travail.

Garde-fou :

- toute conversation AutoGen doit produire MissionTask/Evidence si elle influence une decision.

### browser-use

Decision : `adapter`.

Primitives utiles :

- browser automation ;
- visual/browser agent ;
- extraction web ;
- action execution.

Traduction Grimoire :

- `BrowserToolProvider`;
- research recipe ;
- web validation ;
- UI regression assistance.

Refus :

- ne pas autoriser navigation ou actions web non bornees.

Garde-fou :

- domains allowlist, secrets redaction, screenshot/evidence refs.

### claude-skills

Decision : `fusion-selective`.

Primitives utiles :

- skills ;
- commands ;
- context-aware activation ;
- marketplace-like packaging ;
- documentation patterns.

Traduction Grimoire :

- pack components `skill`, `command`, `prompt`;
- activation rules ;
- skill registry governance.

Refus :

- ne pas copier une marketplace sans trust model.

Garde-fou :

- install disabled until policy + hash + compatibility pass.

### crewAI

Decision : `fusion-selective`.

Voir :

- [ADDENDUM-CREWAI-comparaison-fusion.md](./ADDENDUM-CREWAI-comparaison-fusion.md)

Resume :

- importer tasks/crews/flows comme packs experimentaux ;
- mapper Flows vers Recipes ;
- garder CrewAI comme runner externe, pas noyau ;
- absorber task guardrails, output schemas, checkpoint/fork, Knowledge, MCP DSL et tracing.

### dify

Decision : `adapter`.

Primitives utiles :

- app builder ;
- workflow builder ;
- datasets/RAG ;
- prompt/model provider management ;
- observability/app logs ;
- enterprise UX.

Traduction Grimoire :

- inspiration Pack/Workflow Studio ;
- dataset import ;
- external app deployment adapter ;
- RAG UX patterns.

Refus :

- ne pas transformer Grimoire en Dify-like app platform generaliste.

Garde-fou :

- workflows Dify importes restent projections/adapters, pas kernel.

### gas town

Decision : `fusion-selective`.

Voir les documents principaux du paquet.

Resume :

- Beads -> Mission Ledger ;
- Gas City -> Runtime/Pack/Order/Formulas ;
- gascity-packs -> Pack Registry ;
- gascity-otel -> observability ;
- community/docs -> ecosysteme ;
- Wasteland -> incubator.

Sous-projets couverts :

| Sous-projet | Decision | Integration |
| --- | --- | --- |
| `gas town/beads` | `core-reference` | Mission Ledger, dependencies, ready query, ids anti-collision. |
| `gas town/gastown` | `fusion-selective` | Mayor pattern, rigs, hooks, convoys, provider tiers. |
| `gas town/gascity` | `core-reference` | Runtime providers, supervisor, orders, formulas, packs. |
| `gas town/gascity-packs` | `fusion-selective` | `pack.toml`, commands, doctor checks, services, formulas. |
| `gas town/gascity-otel` | `adapter` | OTel metrics, logs, dashboards. |
| `gas town/community` | `source-doc` | Contributor-first ecosystem and support loop. |
| `gas town/docs` | `source-doc` | Docs structure and publishing model. |
| `gas town/gch-website` | `source-doc` | Public site and launch surface. |
| `gas town/homebrew-beads` | `source-doc` | Distribution formula pattern for Beads. |
| `gas town/homebrew-gascity` | `source-doc` | Distribution formula pattern for Gas City. |
| `gas town/marketplace` | `incubator` | Verified marketplace ideas after Pack Registry. |
| `gas town/overwatch` | `incubator` | Convoy dashboard ideas for Mission Board. |
| `gas town/tim` | `incubator` | Inference mesh concepts after host/provider contracts. |
| `gas town/tmux-adapter` | `adapter` | Optional terminal provider, never required kernel. |
| `gas town/wasteland` | `incubator` | Commons/federation only after trust and evidence gates. |

### graphify

Decision : `core-reference`.

Primitives utiles :

- graph extraction ;
- code/docs graph ;
- repo understanding ;
- MCP/tooling potential.

Traduction Grimoire :

- `CodeGraphProvider`;
- doc graph ;
- task-file-symbol edges ;
- visual graph in cockpit.

Refus :

- ne pas confondre graph de connaissance et ledger causal.

Garde-fou :

- edges graph doivent porter source, confidence et freshness.

### haystack

Decision : `core-reference`.

Primitives utiles :

- pipelines modulaires ;
- RAG ;
- retrieval/routing ;
- agents ;
- evaluation ;
- observability.

Traduction Grimoire :

- `RetrievalPipelineProvider`;
- RAG recipes ;
- memory evaluation ;
- source ingestion patterns.

Refus :

- ne pas remplacer Memory OS par une pipeline RAG non reliee aux tasks.

Garde-fou :

- tout document retrieved doit lier source_ref et memory_ref.

### kagent

Decision : `adapter`.

Primitives utiles :

- cloud-native agent platform ;
- Kubernetes operations ;
- MCP/tool integration ;
- observability ;
- policy around infra agents.

Traduction Grimoire :

- future `KubernetesProvider`;
- infra-ops pack ;
- cluster action policy ;
- sandboxed ops runner.

Refus :

- ne pas mettre K8s dans le chemin critique.

Garde-fou :

- infra mutations require `security_critical` profile.

### langflow

Decision : `adapter`.

Primitives utiles :

- visual flow builder ;
- components ;
- agent/RAG graph UX ;
- import/export ;
- local desktop/cloud modes.

Traduction Grimoire :

- inspiration Workflow Studio ;
- visual Recipe editor ;
- adapter import graph -> recipe draft.

Refus :

- ne pas faire du graphe visuel la source de verite.

Garde-fou :

- flow visuel doit compiler vers Recipe versionnee.

### langfuse

Decision : `adapter`.

Primitives utiles :

- tracing ;
- prompt management ;
- evals ;
- datasets ;
- observability ;
- model cost tracking.

Traduction Grimoire :

- export traces/evals ;
- optional prompt registry mirror ;
- dataset source for eval ledger.

Refus :

- ne pas rendre Langfuse source canonique des runs.

Garde-fou :

- Grimoire trace remains canonical ; Langfuse is sink or mirror.

### langgraph

Decision : `core-reference`.

Primitives utiles :

- durable graph execution ;
- checkpointer ;
- interrupt/resume ;
- state ;
- time travel ;
- long-running agents.

Traduction Grimoire :

- model for Runtime Kernel ;
- `WorkflowInstance` ;
- `Checkpoint` ;
- idempotent task wrappers.

Refus :

- ne pas importer LangGraph comme dependance obligatoire si le kernel Grimoire peut rester plus petit.

Garde-fou :

- toute adoption passe par contrat `WorkflowInstance`.

### mempalace

Decision : `fusion-selective`.

Primitives utiles :

- memory palace ;
- scoped recall ;
- organization spatiale/conceptuelle ;
- MCP/memory tool potential.

Traduction Grimoire :

- Memory OS scopes ;
- visual memory cockpit ;
- recall neighborhoods.

Refus :

- ne pas laisser la metaphore remplacer les sources verifiables.

Garde-fou :

- memory node doit lier provenance et evidence.

### openai-agents-python

Decision : `core-reference`.

Primitives utiles :

- Agent ;
- Runner ;
- tools ;
- handoffs ;
- guardrails ;
- tracing ;
- MCP ;
- sessions.

Traduction Grimoire :

- minimal primitives benchmark ;
- guardrail/handoff semantics ;
- trace spans ;
- model/tool adapter.

Refus :

- ne pas enfermer Grimoire dans un seul fournisseur.

Garde-fou :

- adapter provider-agnostic et tests de parite.

### openclaw

Decision : `incubator`.

Primitives utiles :

- personal AI assistant ;
- local shell ;
- skills/hooks ;
- user UX.

Traduction Grimoire :

- inspiration local assistant pack ;
- possible UX onboarding.

Refus :

- ne pas creer un second assistant Grimoire concurrent.

Garde-fou :

- toute fonctionnalite devient pack ou host adapter.

### pixel-agents

Decision : `source-doc`.

Primitives utiles :

- game interface ;
- operator cockpit ;
- agents building visible artifacts ;
- visual metaphors.

Traduction Grimoire :

- inspiration grimoire-game ;
- Mission Board UX ;
- visible work states.

Refus :

- ne pas prioriser visuel avant preuve runtime.

Garde-fou :

- chaque animation doit correspondre a un event ou read model.

### ruflo

Decision : `incubator`.

Primitives utiles :

- Claude Code orchestration ;
- self-learning/self-optimizing agents ;
- vector memory ;
- hooks ;
- MCP.

Traduction Grimoire :

- learning loop ideas ;
- routeur/flow ideas ;
- hooks comparison.

Refus :

- ne pas importer self-learning non borne dans le noyau.

Garde-fou :

- learning candidate -> verification -> promotion seulement.

### shannon

Decision : `core-reference`.

Primitives utiles :

- AI pentester ;
- security workflows ;
- threat hunting ;
- evidence-oriented security output.

Traduction Grimoire :

- red-team recipes ;
- security eval packs ;
- prompt/tool attack tests ;
- pack safety audit.

Refus :

- ne pas lancer de scans offensifs sans scope explicite.

Garde-fou :

- target allowlist, no destructive actions, evidence and authorization refs.

### superpowers

Decision : `fusion-selective`.

Primitives utiles :

- skills ;
- marketplace/distribution ;
- Claude Code integration ;
- lightweight enhancement packs.

Traduction Grimoire :

- Pack Registry ;
- skill metadata ;
- install UX ;
- capability tags.

Refus :

- ne pas activer skills sans provenance et policy.

Garde-fou :

- skill scan and trust verdict before activation.

### switchboard

Decision : `fusion-selective`.

Primitives utiles :

- agent team setup ;
- board/task dispatch ;
- routing ;
- memory/context around work ;
- operator-oriented orchestration.

Traduction Grimoire :

- Mission Board ;
- routing matrix ;
- task lanes ;
- dispatch policies.

Refus :

- ne pas remplacer Mission Ledger par un board state.

Garde-fou :

- board actions compile to ledger events.

### vscode-copilot-chat

Decision : `core-reference`.

Primitives utiles :

- IDE-native agent UX ;
- Copilot instructions ;
- MCP/customization ;
- workspace edit loop ;
- chat/agent modes.

Traduction Grimoire :

- Host Bridge ;
- Copilot bootstrap ;
- instruction compatibility ;
- IDE event constraints.

Refus :

- ne pas supposer que Copilot expose tous les hooks necessaires.

Garde-fou :

- capability manifest per host, fallback when hooks are absent.

## Backlog transversal ajoute

| ID | Titre | Projets sources |
| --- | --- | --- |
| `GAO-F005` | Importer catalogues de skills vers Pack Registry | `agent-skills`, `claude-skills`, `superpowers`, `andrej-karpathy-skills` |
| `GAO-G005` | Construire provider Code Graph unifie | `CodeGraphContext`, `graphify` |
| `GAO-G006` | Ajouter compression contexte bornee | `LLMLingua` |
| `GAO-J005` | Construire red-team harness agentique | `LLMSecurityGuide`, `shannon`, `agent-sandbox` |
| `GAO-H005` | Compiler inspiration board/visual builders vers cockpit | `switchboard`, `pixel-agents`, `langflow`, `dify` |
| `GAO-I005` | Ajouter external runners experimentaux | `OpenHands`, `autogen`, `browser-use`, `kagent`, `CrewAI` |
| `GAO-K005` | Construire documentation enseignement Agent OS | `ai-agents-for-beginners`, `BMAD-METHOD`, `CrewAI`, `Gas City` |

## Verdict global

Le corpus ne pointe pas vers un seul projet a copier.

Il pointe vers une formule stable :

```text
Kernel durable de LangGraph / CrewAI checkpointing
+ primitives agent simples de OpenAI Agents SDK
+ interop MCP/A2A de Microsoft Agent Framework, CrewAI et OpenAI
+ ledger/pack/supervisor de Gastownhall
+ Memory OS enrichi par CodeGraphContext, Graphify, MemPalace, Haystack
+ security plane par LLMSecurityGuide, Shannon et agent-sandbox
+ cockpit par Switchboard, Pixel Agents, Dify et Langflow
+ skills/packaging par Claude Skills, agent-skills, Superpowers
```

Grimoire doit rester l'integrateur gouverne de ces primitives, pas un clone d'un seul framework.
