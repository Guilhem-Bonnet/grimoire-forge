---
title: "Documentation Technique — Guide Pilotage Agentique"
slug: pilotage-agents-orchestration-agentic
type: doc-technique
date: 2026-04-26
version: "3.0"
relates_to:
  - GUIDE-pilotage-agents-orchestration-agentic.md
  - GUIDE-pilotage-agents-orchestration-agentic-V2-approfondi.md
  - GUIDE-pilotage-agents-orchestration-agentic-V3-maximum.md
---

# Documentation Technique — Guide Pilotage Agentique

## Documents produits

| Document | Version | Contenu |
|---|---|---|
| `GUIDE-pilotage-agents-orchestration-agentic.md` | V1 | Cartographie générale, 11 patterns, mémoire, sécurité, checklist, recommandations |
| `GUIDE-pilotage-agents-orchestration-agentic-V2-approfondi.md` | V2 | Code source réel, snippets, architecture interne, 25 sections, 2261 lignes |
| `GUIDE-pilotage-agents-orchestration-agentic-V3-maximum.md` | V3 | Repos inédits (vscode-copilot-chat, shannon, skill ecosystems, openclaw, LLMSecurityGuide) + approfondissements + OWASP Agentic Top 10, 1923 lignes |

## Périmètre de l'analyse

| Dimension | Valeur |
|---|---|
| Repos analysés | 33 (V1+V2) + 6 inédits V3 |
| Chemin source | `/mnt/Travail/Projets/Dev/Référence-Agentique/` |
| Patterns identifiés | 11 (V1) + 25 approfondissements (V2) + 3 niveaux V3 |
| Couverture stack | Python, TypeScript, Go |
| Date dernière analyse | 2026-04-26 |

## Méthode d'analyse

### V1 — Cartographie
1. **Grounding automatique** : `grimoire-kit/framework/tools/repo-analysis-grounding.sh` sur chaque repo
2. **Lecture directe** des fichiers sources clés (README, architecture, code patterns)
3. **Analyse comparative** des patterns entre frameworks
4. **Validation croisée** des claims via confrontation inter-repos

### V2 — Approfondissement code source
1. **5 agents Explore en parallèle** : lecture du code source réel (`.py`, `.go`, `.ts`, `.prisma`)
2. **Fichiers internes lus** (pas seulement README) : `run.py` (1861 lignes), `crew.py` (2298), `recall_flow.py`, `pregel/_algo.py`, `guardrail.py`, `event_store.py`, `schema.prisma`, `agent_controller.go`, `prompt_compressor.py`, etc.
3. **Extraction de snippets vérifiés** : chaque affirmation est ancrée dans un fichier source
4. **Synthèse transversale** : patterns découverts uniquement à la lecture du code (ex: version-based sync Pregel, ThreadPool RecallFlow, CRD leader election)

### V3 — Maximum depth + repos inédits
1. **8 agents Explore en parallèle** couvrant des zones jamais analysées et des approfondissements ciblés
2. **5 repos inédits analysés** : `vscode-copilot-chat`, `shannon`, écosystème skills (karpathy-skills, claude-skills, superpowers), `openclaw`, `LLMSecurityGuide`
3. **8 approfondissements ciblés** : LangGraph (7 stream modes, 3 channel types, interrupt/resume), CrewAI (per-guardrail retry, LanceDB drain_writes), OpenAI Agents (3-phase lifecycle, asyncio.Queue streaming), agent-sandbox (CRDs warm pool), pixel-agents (dual-mode detection), OpenMythos (RDT: LTI + ACT + MoE), Haystack (ConditionalRouter Jinja2+AST), Dify (parallel retrieval + reranking)
4. **Sécurité agentique** : OWASP Agentic Top 10 2026 (ASI01-ASI10) avec code défensif réel, EchoLeak CVE-2025-32711
5. **Synthèse transversale inédite** : matrice error recovery 8 frameworks, 4 modèles skill architectures, stack V3 startup/enterprise

## Repos sources par pattern

| Pattern | Repo principal | Repos secondaires |
|---|---|---|
| GroupChat | `autogen` | `agent-framework`, `ai-agents-for-beginners` |
| Task-Agent-Process | `crewAI` | — |
| Handoff-First | `openai-agents-python` | — |
| StateGraph/Pregel | `langgraph` | `graphify` |
| DAG Visuel | `langflow` | `dify` |
| EventLoop | `OpenHands` | — |
| Vision+Step | `browser-use` | — |
| Persona+Menu | `BMAD-METHOD` | — |
| Worker Pool | `Octogent` | — |
| Kanban Routing | `switchboard` | — |
| Memory Palace | `mempalace` | — |

## Fichiers sources clés lus (V1 + V2 + V3)

| Fichier | Framework | Mécanisme clé extrait |
|---|---|---|
| `openai-agents-python/src/agents/guardrail.py` | OpenAI Agents | `GuardrailFunctionOutput`, `tripwire_triggered`, 4 niveaux guardrails |
| `openai-agents-python/src/agents/handoffs/__init__.py` | OpenAI Agents | `Handoff`, `default_handoff_history_mapper`, `input_filter` |
| `openai-agents-python/src/agents/run.py` | OpenAI Agents | 3-phase lifecycle, `asyncio.Queue` streaming, `_FunctionToolBatchExecutor` 4 stages |
| `crewAI/lib/crewai/src/crewai/memory/recall_flow.py` | CrewAI | `ThreadPoolExecutor`, product(embeddings × scopes), `compute_composite_score` |
| `crewAI/lib/crewai/src/crewai/crew.py` | CrewAI | 2298 lignes, `RunState` serializable, `kickoff()` |
| `crewAI/lib/crewai/src/crewai/memory/storage/lancedb_storage.py` | CrewAI | `store_lock`, exponential retry, `drain_writes()` barrier |
| `OpenHands/openhands/events/action/agent.py` | OpenHands | `AgentFinishAction`, `ChangeAgentStateAction`, `_cause` tracking |
| `OpenHands/openhands/events/event_store.py` | OpenHands | `EventStore.add_event`, per-subscriber `ThreadPool`, `_queue: queue.Queue[Event]` |
| `langgraph/langgraph/pregel/_algo.py` | LangGraph | `prepare_next_tasks()`, `apply_writes()`, version-based channel sync |
| `langgraph/langgraph/channels/last_value.py` | LangGraph | `LastValue.update()` — 1 seule valeur par step, sinon `InvalidUpdateError` |
| `langgraph/langgraph/channels/topic.py` | LangGraph | `Topic` accumulator, deduplication optionnelle |
| `langgraph/langgraph/channels/binop.py` | LangGraph | `BinaryOperatorAggregate` — `operator(self.value, value)` par update |
| `langgraph/langgraph/pregel/runner.py` | LangGraph | `BackgroundExecutor`, PUSH+PULL scheduler, `trigger_to_nodes` optimization |
| `browser-use/browser_use/agent/service.py` | browser-use | 162KB, 15 watchdogs passifs, `CaptchaWatchdog`, `DefaultActionWatchdog` (131KB) |
| `browser-use/browser_use/browser/session.py` | browser-use | 155KB, `step()` async, max 5 actions parallèles |
| `BMAD-METHOD/customize.toml` | BMAD | 3-layer merge (base → team → user), scalars override, tables deep-merge |
| `dify/api/core/retrieval/retrieval_service.py` | Dify | ThreadPool parallel retrieval, fail-fast cancel, score deduplication |
| `dify/api/core/retrieval/rerank/weight_rerank.py` | Dify | BM25+cosine weighted vs cross-encoder model-based reranking |
| `dify/api/core/splitter/text_splitter.py` | Dify | `chunk_size=4000` chars (pas tokens), `DataPostProcessor` pipeline |
| `langfuse/prisma/schema.prisma` | Langfuse | `LegacyPrismaObservation`, tokens + cost, ClickHouse + Postgres hybrid |
| `mempalace/palace.py` | mempalace | `CHUNK_SIZE=800`, verbatim storage, Wings/Rooms/Drawers |
| `kagent/controllers/agent_controller.go` | kagent | `NeedLeaderElection: true`, CRD v1alpha2, skills-as-OCI-images |
| `LLMLingua/llmlingua/prompt_compressor.py` | LLMLingua | cross-entropy loss ranking, 3 niveaux indépendants (context/sentence/token) |
| `Octogent/src/orchestrator.ts` | Octogent | 8 workers fixes, `MAX_ITERATIONS=50`, `<TASK_COMPLETE>` marker |
| `haystack/haystack/core/pipeline/base.py` | Haystack | `@component.output_types()`, validation au `connect()` |
| `haystack/haystack/components/routers/conditional_router.py` | Haystack | `SandboxedEnvironment` Jinja2 + AST `literal_eval`, `PipelineRuntimeError` wrapping |
| `mempalace/README.md` | mempalace | 96.6% R@5 sur LongMemEval |
| `autogen/README.md` | AutoGen | Statut maintenance, migration officielle vers MAF |
| `vscode-copilot-chat/src/extension/hooks/nodeHookExecutor.ts` | vscode-copilot-chat | `spawn()` child processes, stdin/stdout JSON, exit code 2 = blocking |
| `vscode-copilot-chat/src/extension/agent/toolCallingLoop.ts` | vscode-copilot-chat | `ToolCallingLoop` abstract base class, autopilot mode |
| `vscode-copilot-chat/src/extension/prompt/agentPrompt.tsx` | vscode-copilot-chat | `AgentPrompt` as React/TSX elements |
| `vscode-copilot-chat/src/extension/model/productionEndpointProvider.ts` | vscode-copilot-chat | 5-strategy model cascade, `copilotTokenProvider` |
| `shannon/temporal/workflows.ts` | shannon | 13 agents Temporal, 5 phases, crash recovery, spending cap detection |
| `shannon/src/core/agent-execution.ts` | shannon | Claude Agent SDK `maxTurns=10000`, `permissionMode='bypassPermissions'` |
| `shannon/src/core/claude-executor.ts` | shannon | `PRODUCTION_RETRY` config, Zod structured output, git checkpoint per agent |
| `agent-sandbox/controllers/sandbox_claim_controller.go` | agent-sandbox | 3 CRDs (SandboxClaim/Template/WarmPool), `Retain/Delete/DeleteForeground` lifecycle |
| `agent-sandbox/controllers/warm_pool_reconciler.go` | agent-sandbox | priority sort (unready first then newest), 5 min hardcoded grace period |
| `OpenMythos/model/recurrent_block.py` | OpenMythos | `RecurrentBlock`, `LTIInjection`, `ACTHalting`, `LoRADepth` |
| `OpenMythos/model/moe_ffn.py` | OpenMythos | DeepSeek-V3 aux-loss-free MoE, `router_logits` |
| `LLMSecurityGuide/owasp_agentic.py` | LLMSecurityGuide | ASI01-ASI10 offensive + defensive code, `MemoryIntegrityValidator` |

## Limites et incertitudes

- Certains repos (openclaw, gas town, Design, ruflo) contiennent peu de code agentique analysable
- Les benchmarks de performance cités (96.6% R@5 mempalace) proviennent des README, non vérifiés indépendamment
- L'état de maintenance d'AutoGen est documenté dans le README officiel mais peut évoluer
- LangGraph v0.x vs v1.x : certaines APIs ont changé entre versions
- AutoGen V2 : le repo ne contient que de la documentation (pas de code Python exécutable) — les snippets V2 dans le guide sont des reconstructions documentées
- OpenMythos : état de recherche expérimental, pas de production-ready deployment documenté

## Dépendances de ce document

Ce document est produit par le workflow `repo-analysis` (steps 02-06) + approfondissements V2 (5 agents Explore parallèles) + V3 (8 agents Explore parallèles).
Il référence les analyses intermédiaires des steps 02-05 (non persistées séparément).
