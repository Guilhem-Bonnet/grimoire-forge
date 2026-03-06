# PRD — BMAD Intelligence Layer : Orchestration IA, Multi-Agent Réel, et Mémoire Sémantique

> **Statut** : Lot 1 COMPLET ✅ — Lot 2 COMPLET ✅ — Lot 3 COMPLET ✅ — Lot 4 COMPLET ✅ — Lot 5 PLANIFIÉ ⏳  
> **Auteurs** : John (PM) + Winston (Architect) + Mary (Analyst) + Amelia (Dev) + Barry (Quick Flow)  
> **Version cible** : 3.1.0 (extension de la v3 Platform)  
> **Précédent** : PRD-bmad-kit-v3-platform.md  
> **Nom de code** : **Synapse**  
> **Origine** : Session Party Mode — analyse orchestrateur IA, multi-agent, économie tokens, Qdrant, LLM routing
>
> ### Avancement Lot 1 — COMPLET ✅
> | Livrable | Statut | Fichier | Tests |
> |---|---|---|---|
> | LLM Router | ✅ Implémenté + testé | `framework/tools/llm-router.py` | 61 passed |
> | RAG Indexer | ✅ Implémenté + testé | `framework/tools/rag-indexer.py` | 55 passed, 2 skipped |
> | RAG Retriever | ✅ Implémenté + testé | `framework/tools/rag-retriever.py` | 61 passed |
> | Memory Sync | ✅ Implémenté + testé | `framework/tools/memory-sync.py` | 69 passed |
> | MCP Tools Server | ✅ Implémenté + testé | `framework/tools/bmad-mcp-tools.py` | 24 passed |
> | Config template | ✅ Mis à jour | `project-context.tpl.yaml` | — |
> | Ruff compliance | ✅ All checks passed | — | — |
> | **Total Lot 1** | **✅ 270 tests passed, 2 skipped** | **5 outils + 5 suites de tests** | **2.54s** |
>
> ### Avancement Lot 2 — COMPLET ✅
> | Livrable | Statut | Fichier | Tests |
> |---|---|---|---|
> | Context Summarizer (3.1) | ✅ Implémenté + testé | `framework/tools/context-summarizer.py` | 65 passed |
> | Semantic Cache (3.2) | ✅ Implémenté + testé | `framework/tools/semantic-cache.py` | 43 passed |
> | Token Budget (3.3) | ✅ Implémenté + testé | `framework/tools/token-budget.py` | 35 passed |
> | Tool Registry (6.1) | ✅ Implémenté + testé | `framework/tools/tool-registry.py` | 46 passed |
> | Agent Caller (6.2) | ✅ Implémenté + testé | `framework/tools/agent-caller.py` | 48 passed |
> | Ruff compliance | ✅ All checks passed (outils + tests) | — | — |
> | **Total Lot 2** | **✅ 237 tests passed** | **5 outils + 5 suites de tests** | **~8s** |
> | **Total cumulé Lots 1+2** | **✅ 507 tests passed, 2 skipped** | **10 outils + 10 suites de tests** | **9.83s** |
>
> ### Avancement Lot 3 — COMPLET ✅
> | Livrable | Statut | Fichier | Tests |
> |---|---|---|---|
> | Message Bus (4.1) | ✅ Implémenté + testé | `framework/tools/message-bus.py` | 27 passed |
> | Agent Worker (4.2) | ✅ Implémenté + testé | `framework/tools/agent-worker.py` | 30 passed |
> | Orchestrator (4.3) | ✅ Implémenté + testé | `framework/tools/orchestrator.py` | 30 passed |
> | Delivery Contracts (4.4) | ✅ Implémenté + testé | `framework/tools/delivery-contracts.py` | 36 passed |
> | Conversation Branch (5.1) | ✅ Implémenté + testé | `framework/tools/conversation-branch.py` | 26 passed |
> | Context Merge (5.2) | ✅ Implémenté + testé | `framework/tools/context-merge.py` | 29 passed |
> | Background Tasks (5.3) | ✅ Implémenté + testé | `framework/tools/background-tasks.py` | 27 passed |
> | Conversation History (5.4) | ✅ Implémenté + testé | `framework/tools/conversation-history.py` | 31 passed |
> | Ruff compliance | ✅ All checks passed (outils + tests) | — | — |
> | **Total Lot 3** | **✅ 246 tests passed** | **8 outils + 8 suites de tests** | **~9s** |
> | **Total cumulé Lots 1+2+3** | **✅ 753 tests passed, 2 skipped** | **18 outils + 18 suites de tests** | **~22s** |
>
> ### Avancement Lot 4 — COMPLET ✅
> | Livrable | Statut | Fichier | Tests |
> |---|---|---|---|
> | Tests intégration E2E (7.1) | ✅ Implémenté + testé | `tests/test_integration_synapse.py` | 26 passed |
> | Synapse Trace middleware (7.2) | ✅ Implémenté + testé | `framework/tools/synapse-trace.py` | 56 passed |
> | Script coverage (7.3) | ✅ Créé | `tests/run-coverage.sh` | — |
> | Token counting precision (7.4) | ✅ Implémenté | `framework/tools/token-budget.py` (v1.1.0) | inclus dans existants |
> | Synapse Config centralisée (7.5) | ✅ Implémenté + testé | `framework/tools/synapse-config.py` | 49 passed |
> | Ruff compliance | ✅ All checks passed (outils + tests) | — | — |
> | **Total Lot 4** | **✅ 131 tests passed** | **2 outils + 3 suites de tests + 1 patch** | **~0.5s** |
> | **Total cumulé Lots 1+2+3+4** | **✅ 884 tests passed, 2 skipped** | **20 outils + 21 suites de tests** | **~22s** |

---

## Table des matières

1. [Contexte et Diagnostic](#1-contexte-et-diagnostic)
2. [Vision Produit](#2-vision-produit)
3. [Architecture Cible](#3-architecture-cible)
4. [Épics Détaillées](#4-épics-détaillées)
5. [Références et Ressources](#5-références-et-ressources)
6. [Contraintes et Risques](#6-contraintes-et-risques)
7. [Métriques de Succès](#7-métriques-de-succès)
8. [Hors Scope](#8-hors-scope)

---

## 1. Contexte et Diagnostic

### 1.1 État des lieux — Ce qui existe dans BMAD aujourd'hui

| Capacité | Implémentation actuelle | Maturité | Fichier de référence |
|---|---|---|---|
| **Orchestration** | Workflow engine YAML/MD, step-based | ✅ Production | `_bmad/core/tasks/workflow.xml` |
| **Multi-agent** | Simulation mono-LLM (persona switching) | ⚠️ Simulé | Party Mode, Boomerang |
| **Mémoire structurée** | Fichiers MD + JSON dans `_bmad/_memory/` | ✅ Production | `framework/memory/` |
| **Mémoire sémantique** | `mem0-bridge.py` + backends Qdrant | 🔵 Prototype | `framework/memory/backends/` |
| **Context routing** | Context Budget Router (BM-07) | ✅ Production | `framework/context-router.md` |
| **A2A Protocol** | Stub dispatcher (BM-32) | 🔵 Stub | `framework/agent2agent.md` |
| **Session branching** | Structure `.runs/` + CLI (BM-16) | ✅ Production | `framework/sessions/README.md` |
| **Subagent orchestration** | Syntaxe YAML `type: orchestrate` (BM-19) | 🔵 Spec | `framework/workflows/subagent-orchestration.md` |
| **Boomerang orchestration** | Workflow décomposition SM→agents→SM (BM-11) | ✅ Production | `framework/workflows/boomerang-orchestration.md` |
| **LLM Routing** | ❌ Inexistant | ❌ Rien | — |
| **Function calling natif** | Via MCP (indirect) | ⚠️ Partiel | Config MCP IDE |
| **Token optimization** | JIT loading, sharding, step-based | ⚠️ Artisanal | — |
| **Conversations background** | ❌ Inexistant | ❌ Rien | — |

### 1.2 Problèmes identifiés

| # | Problème | Impact | Preuve |
|---|---|---|---|
| P1 | **Mono-LLM** : tous les agents partagent le même modèle, même contexte | Pas de spécialisation modèle, pression contexte | Party Mode = un seul LLM joue 10+ personas |
| P2 | **Pas de routing modèle** : tâches simples (formatage) consomment le même modèle coûteux que le raisonnement complexe | Coût 3-5x trop élevé pour les tâches triviales | Aucun mécanisme de sélection de modèle |
| P3 | **Mémoire sémantique non connectée** : Qdrant backends existent mais pas intégrés au flux agent | Recall sémantique inaccessible en conversation | `backend_qdrant_local.py` existe, jamais appelé par les agents IDE |
| P4 | **Pas de vrai parallélisme agent** : subagent orchestration est spécifiée (BM-19) mais en fallback séquentiel | Pas de gain de temps, pas d'isolation | `fallback.mode: sequential` est le seul mode opérationnel |
| P5 | **Context non résumé entre sessions** : chaque nouvelle session repart du fichier brut | Tokens gaspillés, risque de troncature silencieuse | Pas de summarization automatique |
| P6 | **Branches de conversation sans backend** : le branching existe pour les outputs mais pas pour le contexte conversationnel | Impossible d'explorer deux idées en parallèle dans le chat | Session branching = fichiers seulement |

### 1.3 Analyse concurrentielle

| Solution | Focus | Forces vs BMAD | Faiblesses vs BMAD |
|---|---|---|---|
| **[RTK](https://github.com/rtk-ai/rtk)** | Token optimization runtime | Compression contexte, caching sémantique, token budgeting automatique | Pas d'orchestration agent, pas de personas, pas de workflows |
| **[Open-Sandbox.ai](https://open-sandbox.ai/)** | Sandboxed code execution | Exécution isolée de code IA, APIs sécurisées | Pas d'orchestration, runtime uniquement, pas local |
| **[CrewAI](https://github.com/joaomdmoura/crewAI)** | Multi-agent framework | Vrai multi-agent avec message passing, tools intégrés | Requiert API cloud, pas de mémoire persistent, pas IDE-natif |
| **[AutoGen](https://github.com/microsoft/autogen)** | Multi-agent conversations | GroupChat, code execution, flexible topology | Complexe, over-engineered pour solo dev, pas IDE-natif |
| **[LangGraph](https://github.com/langchain-ai/langgraph)** | Stateful agent graphs | Graphes d'état, checkpointing, parallélisme | Abstraction lourde, dépendance LangChain |
| **[OpenRouter](https://openrouter.ai/)** | LLM routing API | 300+ modèles, routing intelligent, fallback auto | Cloud-only, pas local, pas gratuit |
| **[Martian](https://withmartian.com/)** | Model routing | Routing basé sur la tâche, optimisation coût/qualité | Propriétaire, cloud-only |
| **[Not Diamond](https://notdiamond.ai/)** | LLM router | Routing ML-based, prédiction performance par tâche | Propriétaire |
| **[Qdrant MCP Server](https://github.com/qdrant/mcp-server-qdrant)** | Vector DB via MCP | Accès direct depuis IDE, search/upsert via protocol standard | Pas de pipeline d'indexation, juste l'accès |
| **[mem0](https://github.com/mem0ai/mem0)** | Memory layer for AI | Mémoire long-terme, cross-session, multi-user | Cloud-first, pas IDE-natif |
| **[MemGPT/Letta](https://github.com/letta-ai/letta)** | Self-editing memory | Context window management, memory tiers | Serveur séparé requis, complexe |

---

## 2. Vision Produit

> **BMAD Intelligence Layer transforme le framework d'un orchestrateur mono-LLM simulé en une plateforme d'agents véritablement intelligente** — avec routing de modèles, mémoire sémantique intégrée, communication inter-agents réelle, et optimisation de tokens automatique — tout en restant 100% local et IDE-natif.

### Positionnement stratégique

```
                    ┌─────────────────────────────────┐
                    │     BMAD Intelligence Layer      │
                    │         (Synapse)                │
                    │                                   │
                    │  ┌───────────┐  ┌─────────────┐  │
                    │  │ LLM Router│  │ Token Optim  │  │
                    │  └───────────┘  └─────────────┘  │
                    │  ┌───────────┐  ┌─────────────┐  │
                    │  │ Real A2A  │  │ Qdrant RAG   │  │
                    │  └───────────┘  └─────────────┘  │
                    │  ┌───────────┐  ┌─────────────┐  │
                    │  │ Branch    │  │ Background   │  │
                    │  │ Context   │  │ Conversations│  │
                    │  └───────────┘  └─────────────┘  │
                    └─────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │    BMAD Kit v3 (Catalyst)     │
                    │  CLI + SDK + MCP + bmad.yaml  │
                    └───────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │    BMAD Core Platform         │
                    │  Agents + Workflows + Memory  │
                    └───────────────────────────────┘
```

---

## 3. Architecture Cible

### 3.1 Vue d'ensemble

```
┌──────────────────────────────────────────────────────────────────────┐
│                     BMAD Intelligence Layer                          │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                      LLM Router (BM-40)                        │  │
│  │                                                                 │  │
│  │  Requête agent ──▶ Classifieur ──▶ Sélection modèle ──▶ LLM   │  │
│  │                     (complexité,    (config per-agent,          │  │
│  │                      type, coût)     fallback chain)            │  │
│  └────────────────────────┬───────────────────────────────────────┘  │
│                           │                                          │
│  ┌────────────────────────▼───────────────────────────────────────┐  │
│  │                Token Optimizer (BM-41)                          │  │
│  │                                                                 │  │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────────────────────┐  │  │
│  │  │ Context  │  │ Semantic     │  │ Prompt Compression       │  │  │
│  │  │ Summarize│  │ Cache        │  │ (RTK-inspired)           │  │  │
│  │  └──────────┘  └──────────────┘  └──────────────────────────┘  │  │
│  └────────────────────────┬───────────────────────────────────────┘  │
│                           │                                          │
│  ┌────────────────────────▼───────────────────────────────────────┐  │
│  │              Qdrant RAG Pipeline (BM-42)                       │  │
│  │                                                                 │  │
│  │  Indexation ──▶ Chunking ──▶ Embedding ──▶ Qdrant Storage      │  │
│  │       │                                         │               │  │
│  │  Agent Query ──▶ Semantic Search ──▶ Reranking ──▶ Context     │  │
│  └────────────────────────┬───────────────────────────────────────┘  │
│                           │                                          │
│  ┌────────────────────────▼───────────────────────────────────────┐  │
│  │          Real Multi-Agent Communication (BM-43)                │  │
│  │                                                                 │  │
│  │  ┌──────────┐    A2A/MCP     ┌──────────┐                     │  │
│  │  │ Agent A  │◀──────────────▶│ Agent B  │                     │  │
│  │  │ (LLM 1)  │   Message Bus  │ (LLM 2)  │                     │  │
│  │  └──────────┘  (Redis/NATS)  └──────────┘                     │  │
│  └────────────────────────┬───────────────────────────────────────┘  │
│                           │                                          │
│  ┌────────────────────────▼───────────────────────────────────────┐  │
│  │      Session Intelligence (BM-44)                              │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌─────────────────┐  ┌──────────────────┐  │  │
│  │  │ Conversation │  │ Context Branch  │  │ Background       │  │  │
│  │  │ Branching    │  │ Sync & Merge    │  │ Agent Tasks      │  │  │
│  │  └──────────────┘  └─────────────────┘  └──────────────────┘  │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2 Intégration avec l'existant

| Composant existant | Comment il s'intègre | Changements requis |
|---|---|---|
| Context Router (BM-07) | Devient client du Token Optimizer — les priorités P0-P4 alimentent le budget du router | Ajouter interface vers Token Optimizer |
| mem0-bridge.py | Remplacé progressivement par le RAG Pipeline Qdrant natif | Migration dual-write → read-from-Qdrant |
| A2A Dispatcher (BM-32) | Étendu avec transport réel (Redis/NATS) au lieu de stub | Implémenter les transports réels |
| Session Branching (BM-16) | Étendu avec le branching de contexte conversationnel | Ajouter context snapshots par branche |
| Subagent Orchestration (BM-19) | Le fallback séquentiel est remplacé par du vrai parallélisme via le message bus | Implémenter le spawn réel |
| Boomerang (BM-11) | Utilise le LLM Router pour choisir le bon modèle par sous-tâche | Ajouter model selection dans les steps |

---

## 4. Épics Détaillées

---

### EPIC 1 — LLM Router (BM-40)

**Priorité** : 🔴 P0  
**Effort estimé** : M (2-3 semaines)  
**Dépendances** : BMAD Kit v3 SDK (pyproject.toml, package structure)

#### 1.1 Problème

Tous les agents BMAD utilisent le même modèle LLM, quel que soit la complexité de la tâche. Un formatage de markdown consomme le même modèle (ex: Claude Opus à ~$15/M tokens) qu'une review architecturale complexe. Pas de fallback si un modèle est down.

#### 1.2 Solution

Un **LLM Router** qui dirige chaque requête vers le modèle optimal selon :
- La **complexité** de la tâche (classification automatique)
- Le **type** de contenu (code, raisonnement, formatage)
- Le **coût** acceptable (budget per-agent configurable)
- La **disponibilité** du modèle (fallback chain)

#### 1.3 Stories détaillées

##### Story 1.1 — Configuration du Router dans `bmad.yaml`

**Description** : Permettre de déclarer plusieurs modèles LLM et les règles de routing dans `bmad.yaml`.

**Acceptance Criteria** :
- [ ] Nouveau bloc `llm_router` dans `bmad.yaml` avec validation JSON Schema
- [ ] Champs : `models[]` (name, provider, cost_per_1k, max_tokens, capabilities[])
- [ ] Champs : `rules[]` (agent_id | task_type → model_id, fallback_model_id)
- [ ] Champ `default_model` pour les cas non couverts par les rules
- [ ] Validation au `bmad up` — erreur claire si modèle référencé n'existe pas

**Spec technique** :
```yaml
# bmad.yaml — bloc llm_router
llm_router:
  enabled: true
  default_model: claude-sonnet
  
  models:
    - id: claude-opus
      provider: anthropic
      api: copilot            # via Copilot Chat | direct | ollama | openrouter
      cost_per_1m_tokens: 15.0
      max_tokens: 200000
      capabilities: [reasoning, architecture, complex-analysis]
      
    - id: claude-sonnet
      provider: anthropic
      api: copilot
      cost_per_1m_tokens: 3.0
      max_tokens: 200000
      capabilities: [coding, review, general]
      
    - id: claude-haiku
      provider: anthropic
      api: copilot
      cost_per_1m_tokens: 0.25
      max_tokens: 200000
      capabilities: [formatting, simple-qa, summarization]
      
    - id: deepseek-coder
      provider: deepseek
      api: ollama
      cost_per_1m_tokens: 0.0  # local
      max_tokens: 128000
      capabilities: [coding, refactoring]
      
    - id: nomic-embed
      provider: nomic
      api: ollama
      cost_per_1m_tokens: 0.0  # local
      capabilities: [embedding]

  rules:
    # Par agent
    - match: { agent: architect }
      model: claude-opus
      fallback: claude-sonnet
      
    - match: { agent: dev }
      model: claude-sonnet
      fallback: deepseek-coder
      
    - match: { agent: qa }
      model: claude-haiku
      fallback: claude-sonnet
    
    # Par type de tâche
    - match: { task_type: formatting }
      model: claude-haiku
      
    - match: { task_type: architecture-review }
      model: claude-opus
      
    - match: { task_type: embedding }
      model: nomic-embed
```

**Références pour l'implémentation** :
- [OpenRouter model routing API](https://openrouter.ai/docs/model-routing) — pattern de routing par capabilities
- [Not Diamond — ML-based router](https://notdiamond.ai/) — classification par performance prédite
- [Martian Router](https://docs.withmartian.com/) — fallback chains et cost optimization
- [LiteLLM](https://github.com/BerriAI/litellm) — proxy unifié multi-provider Python, 100+ modèles, API unique

##### Story 1.2 — Classifieur de complexité de tâche

**Description** : Module Python qui analyse une requête agent et classifie sa complexité (trivial / standard / complex / expert) pour alimenter le routing.

**Acceptance Criteria** :
- [ ] Classe `TaskClassifier` dans `bmad.core.llm_router`
- [ ] Classifie par heuristiques (pas de ML) : longueur prompt, mots-clés, type d'agent, historique
- [ ] Retourne `TaskClass(complexity, task_type, suggested_model, confidence)`
- [ ] Heuristiques documentées et overridables dans `bmad.yaml`
- [ ] Tests unitaires avec 20+ cas de test

**Heuristiques de classification** :
```python
# Indicateurs de complexité
COMPLEX_INDICATORS = [
    "architecture", "design", "trade-off", "compare", "migration",
    "security audit", "performance", "scalability", "distributed"
]
TRIVIAL_INDICATORS = [
    "format", "rename", "list", "count", "sort", "template",
    "linting", "typo", "indentation"
]
```

**Références** :
- [OpenAI Cookbook — LLM routing](https://cookbook.openai.com/) — patterns de classification pour routing
- [Semantic Router](https://github.com/aurelio-labs/semantic-router) — routing sémantique par embeddings, Python, open-source
- [RouteLLM (LMSYS)](https://github.com/lm-sys/RouteLLM) — framework de routing open-source avec classifieurs entraînés, benchmarks publics

##### Story 1.3 — Interface MCP pour le Router

**Description** : Exposer le LLM Router comme un outil MCP pour que l'IDE puisse faire du routing transparent.

**Acceptance Criteria** :
- [ ] Tool MCP `bmad_route_request` qui prend un prompt + agent_id et retourne le modèle recommandé
- [ ] Tool MCP `bmad_router_stats` qui retourne les stats d'utilisation par modèle
- [ ] Intégration dans le MCP server existant (`bmad.mcp.server`)
- [ ] Documentation utilisateur

**Références** :
- [Anthropic MCP SDK Python](https://github.com/modelcontextprotocol/python-sdk) — SDK officiel pour tools MCP
- [VS Code MCP integration](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) — comment les MCP servers s'intègrent à Copilot

##### Story 1.4 — Dashboard de coûts et usage

**Description** : CLI `bmad router stats` et outil MCP qui affiche l'utilisation des modèles, les coûts estimés, et les recommandations de routing.

**Acceptance Criteria** :
- [ ] `bmad router stats` affiche : requêtes par modèle, coût estimé, tokens consommés
- [ ] `bmad router stats --recommend` suggère des optimisations de routing
- [ ] Données persistées dans `_bmad-output/.router-stats.jsonl`
- [ ] Affichage `rich` avec tables et sparklines
- [ ] Tests unitaires

---

### EPIC 2 — Pipeline RAG Qdrant (BM-42)

**Priorité** : 🔴 P0  
**Effort estimé** : L (3-4 semaines)  
**Dépendances** : Qdrant (local ou serveur), modèle d'embedding

#### 2.1 Problème

BMAD possède une mémoire structurée riche (fichiers MD, decisions-log, learnings) mais pas de **retrieval sémantique intégré au flux agent**. Le `mem0-bridge.py` existe en prototype mais n'est pas connecté au cycle d'activation des agents. Les agents chargent les fichiers en entier ou pas du tout — pas de chunking intelligent.

#### 2.2 Solution

Un pipeline RAG complet : **Indexation automatique → Chunking adaptatif → Embedding → Stockage Qdrant → Retrieval sémantique au runtime agent → Reranking → Injection contexte**.

#### 2.3 Stories détaillées

##### Story 2.1 — MCP Server Qdrant — Intégration IDE

**Description** : Connecter le MCP server Qdrant officiel à VS Code Copilot pour que les agents puissent query Qdrant directement en conversation.

**Acceptance Criteria** :
- [ ] Configuration MCP dans `.vscode/mcp.json` ou `~/.config/Code/User/mcp.json`
- [ ] Le server expose : `qdrant_search`, `qdrant_upsert`, `qdrant_list_collections`
- [ ] Test : un agent peut faire un `recall` sémantique en conversation
- [ ] Documentation setup (docker-compose ou binaire local)

**Spec technique** :
```json
// mcp.json
{
  "servers": {
    "qdrant": {
      "command": "uvx",
      "args": ["mcp-server-qdrant"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "COLLECTION_NAME": "bmad-project"
      }
    }
  }
}
```

**Références** :
- [qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant) — serveur MCP officiel Qdrant
- [Qdrant Documentation](https://qdrant.tech/documentation/) — guide complet de l'API et des collections
- [Qdrant Docker Quick Start](https://qdrant.tech/documentation/quickstart/) — `docker run -p 6333:6333 qdrant/qdrant`

##### Story 2.2 — Pipeline d'indexation automatique

**Description** : Script/CLI qui indexe tous les artifacts BMAD (agents, mémoire, docs, PRDs, ADRs) dans Qdrant avec metadata typée.

**Acceptance Criteria** :
- [ ] Commande `bmad index [--full | --incremental]`
- [ ] Indexe : agents (persona, rules), memory (learnings, decisions), docs (PRDs, ADRs), code (docstrings, comments)
- [ ] Chunking adaptatif : Markdown → par header (##), Code → par fonction, YAML → par bloc
- [ ] Metadata par chunk : `source_file`, `chunk_type`, `agent_id`, `date`, `tags[]`
- [ ] Mode incrémental : ne ré-indexe que les fichiers modifiés (hash SHA256)
- [ ] Collections créées : `{project}-agents`, `{project}-memory`, `{project}-docs`, `{project}-code`
- [ ] Exécution au `bmad up` et en hook pre-commit (optionnel)

**Spec technique** :
```python
# bmad/tools/rag_indexer.py

class ChunkingStrategy:
    """Stratégie de chunking adaptative par type de fichier."""
    
    @staticmethod
    def chunk_markdown(content: str, max_tokens: int = 512) -> list[Chunk]:
        """Découpe par header ## avec overlap de contexte."""
        ...
    
    @staticmethod
    def chunk_python(content: str, max_tokens: int = 512) -> list[Chunk]:
        """Découpe par fonction/classe avec docstring."""
        ...
    
    @staticmethod
    def chunk_yaml(content: str, max_tokens: int = 512) -> list[Chunk]:
        """Découpe par bloc de premier niveau."""
        ...

class RAGIndexer:
    """Pipeline d'indexation BMAD → Qdrant."""
    
    def __init__(self, project: BmadProject, qdrant_url: str, embedding_model: str):
        ...
    
    def index_full(self) -> IndexReport:
        """Indexation complète — recrée les collections."""
        ...
    
    def index_incremental(self) -> IndexReport:
        """Indexation incrémentale — ne ré-indexe que les fichiers modifiés."""
        ...
```

**Références** :
- [LlamaIndex — Ingestion Pipeline](https://docs.llamaindex.ai/en/stable/module_guides/loading/ingestion_pipeline/) — patterns de chunking et indexation
- [Unstructured.io](https://github.com/Unstructured-IO/unstructured) — parsing multi-format (MD, PDF, code)
- [Qdrant Python client — Batch upload](https://qdrant.tech/documentation/guides/bulk-upload/) — API d'upsert batch optimisé
- [nomic-embed-text](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) — modèle d'embedding open-source, 8192 tokens, top Hugging Face MTEB

##### Story 2.3 — Retrieval sémantique au runtime agent

**Description** : Au moment de l'activation d'un agent, avant chaque réponse, le système query automatiquement Qdrant pour enrichir le contexte avec les chunks les plus pertinents.

**Acceptance Criteria** :
- [ ] Classe `RAGRetriever` dans `bmad.tools`
- [ ] Retrieval automatique basé sur : message utilisateur + agent_id + task context
- [ ] Reranking des résultats (score sémantique + metadata boost)
- [ ] Injection transparente dans le contexte agent (via Context Router BM-07 étendu)
- [ ] Configurable dans `bmad.yaml` : `rag.auto_retrieve: true`, `rag.max_chunks: 5`, `rag.min_score: 0.3`
- [ ] Fallback gracieux si Qdrant est down → fichiers MD classiques

**Références** :
- [RAG Best Practices (Anthropic)](https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation) — guidelines officielles pour RAG avec Claude
- [ColBERT v2](https://github.com/stanford-futuredata/ColBERT) — late interaction reranking, état de l'art pour le retrieval
- [Cohere Rerank](https://docs.cohere.com/docs/reranking) — API de reranking (pattern à reproduire localement)
- [BGE Reranker](https://huggingface.co/BAAI/bge-reranker-v2-m3) — modèle de reranking open-source

##### Story 2.4 — Write-back et memory sync

**Description** : Après chaque session agent, les insights/décisions sont automatiquement vectorisés et stockés dans Qdrant, avec sync bidirectionnelle avec les fichiers MD.

**Acceptance Criteria** :
- [ ] Hook post-session qui vectorise les nouvelles entrées decisions-log et learnings
- [ ] Protocol `remember` de mem0-bridge.py migré vers le RAG Pipeline
- [ ] Sync bidirectionnelle : Qdrant → MD (`bmad memory export`) et MD → Qdrant (`bmad memory import`)
- [ ] Déduplication par UUID5 (compatible avec l'existant mem0-bridge.py)
- [ ] Contradiction detection via cosine similarity > 0.85

**Références** :
- [mem0 — Memory for AI](https://github.com/mem0ai/mem0) — patterns de write-back et contradiction detection
- [Qdrant — Payload Indexing](https://qdrant.tech/documentation/concepts/indexing/#payload-index) — indexation metadata pour filtre efficace

---

### EPIC 3 — Token Optimization Layer (BM-41)

**Priorité** : 🟡 P1  
**Effort estimé** : M (2-3 semaines)  
**Dépendances** : Epic 1 (LLM Router), Epic 2 (Qdrant RAG)

#### 3.1 Problème

BMAD gère les tokens de manière artisanale (JIT loading, sharding docs). Pas de compression de contexte, pas de caching sémantique, pas de budgeting automatique. On consomme 3-5x plus de tokens que nécessaire.

#### 3.2 Solution

Une couche d'optimisation de tokens inspirée de RTK — **compression de contexte, caching sémantique des résultats, prompt optimization, et budget enforcement automatique**.

#### 3.3 Stories détaillées

##### Story 3.1 — Context Summarization automatique

**Description** : Résumer automatiquement les sections anciennes du contexte (decisions-log > 30j, learnings > 60j) pour libérer du budget token.

**Acceptance Criteria** :
- [ ] Module `ContextSummarizer` dans `bmad.tools`
- [ ] Stratégie configurable : `age_threshold`, `max_summary_tokens`, `preserve_tags[]`
- [ ] Résumé stocké dans `_bmad/_memory/archives/digest-{date}.md`
- [ ] Le résumé remplace le contenu original dans le chargement P1 du Context Router
- [ ] Métrique : réduction de 40-60% des tokens pour les projets > 1 mois
- [ ] Exécution auto au `bmad up` et option manuelle `bmad memory summarize`

**Références** :
- [RTK Context Compression](https://github.com/rtk-ai/rtk) — middleware de compression de contexte
- [LLMLingua](https://github.com/microsoft/LLMLingua) — compression de prompt Microsoft Research, 2-5x compression ratio sans perte de qualité
- [Anthropic — Long context tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — prompt caching et stratégies de contexte long

##### Story 3.2 — Semantic Cache

**Description** : Cache sémantique des réponses LLM — si une requête similaire (cosine > 0.9) a déjà été traitée, retourner la réponse cached.

**Acceptance Criteria** :
- [ ] Module `SemanticCache` utilisant Qdrant comme backend (collection `{project}-cache`)
- [ ] TTL configurable par type de requête (code review: 1h, architecture: 24h, formatting: 7j)
- [ ] Hit rate tracking et reporting dans `bmad router stats`
- [ ] Invalidation automatique quand les fichiers source changent
- [ ] Bypass explicite avec flag `--no-cache`

**Références** :
- [GPTCache](https://github.com/zilliztech/GPTCache) — cache sémantique pour LLM, multiple backends dont Qdrant
- [Redis semantic cache](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/) — pattern vector search pour caching
- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — cache côté provider (complémentaire au cache local)

##### Story 3.3 — Token Budget Enforcement

**Description** : Enforcement automatique du budget token par agent et par session, avec actions correctives (summarize, drop, alert).

**Acceptance Criteria** :
- [ ] Extension du Context Router (BM-07) avec enforcement actif
- [ ] Actions à 60% budget : warning + suggestions
- [ ] Actions à 80% budget : summarize automatique des sections P2/P3
- [ ] Actions à 95% budget : drop des sections P3/P4 + alert utilisateur
- [ ] Reporting en temps réel via MCP tool `bmad_context_budget`
- [ ] Override par agent dans `bmad.yaml`

**Références** :
- [MemGPT/Letta — Tiered memory](https://github.com/letta-ai/letta) — gestion de contexte par tiers avec eviction
- [Context Window Management patterns](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/memory/) — LlamaIndex memory patterns

---

### EPIC 4 — Communication Multi-Agent Réelle (BM-43)

**Priorité** : 🟢 P2  
**Effort estimé** : XL (4-6 semaines)  
**Dépendances** : Epic 1 (LLM Router), Epic 2 (Qdrant RAG)

#### 4.1 Problème

BMAD simule le multi-agent avec un seul LLM qui change de persona. Pas de vrai parallélisme, pas d'isolation, pas de spécialisation modèle. Le protocole A2A (BM-32) est un stub.

#### 4.2 Solution

Trois modes de multi-agent, du plus simple au plus complexe, avec un switch progressif :

| Mode | Description | Coût | Quand l'utiliser |
|---|---|---|---|
| **Simulated** (actuel) | Un LLM, persona switching | 1x | Chat, party mode, discussions légères |
| **Sequential Real** | Agents exécutés séquentiellement, chacun sur son LLM | 2-3x | Boomerang, code review croisée |
| **Parallel Real** | Agents sur LLMs séparés, communication via message bus | 3-5x | Analyse parallèle, tests adversariaux, validation croisée |

#### 4.3 Stories détaillées

##### Story 4.1 — Message Bus abstraction layer

**Description** : Couche d'abstraction pour la communication inter-agents avec backends pluggables (in-process, Redis Streams, NATS).

**Acceptance Criteria** :
- [ ] ABC `MessageBus` dans `bmad.core.messaging`
- [ ] Backend `InProcessBus` (queue mémoire — pour tests et mode simulated)
- [ ] Backend `RedisBus` (Redis Streams — pour mode sequential/parallel)
- [ ] Backend `NATSBus` (NATS JetStream — pour mode parallel haute perf)
- [ ] Protocol de message standardisé : `AgentMessage(sender, recipient, type, payload, correlation_id)`
- [ ] Patterns supportés : request-reply, pub-sub, broadcast
- [ ] Configuration dans `bmad.yaml` : `messaging.backend: in-process | redis | nats`

**Spec technique** :
```python
# bmad/core/messaging.py

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class AgentMessage:
    sender: str           # agent_id (ex: "architect")
    recipient: str        # agent_id ou "*" pour broadcast
    msg_type: str         # "task-request" | "task-response" | "observation" | "question"
    payload: dict         # contenu libre, schéma par msg_type
    correlation_id: str   # pour lier request ↔ response
    timestamp: str
    trace_id: str | None  # BMAD_TRACE integration

class MessageBus(ABC):
    @abstractmethod
    async def send(self, message: AgentMessage) -> None: ...
    
    @abstractmethod
    async def receive(self, agent_id: str, timeout: float = 30.0) -> AgentMessage | None: ...
    
    @abstractmethod
    async def subscribe(self, agent_id: str, pattern: str) -> None: ...
```

**Références** :
- [Google A2A Protocol](https://google.github.io/A2A/) — standard ouvert pour communication inter-agents
- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/) — message queue persistante, consumer groups
- [NATS JetStream](https://docs.nats.io/nats-concepts/jetstream) — messaging haute performance, at-least-once delivery
- [AutoGen — GroupChat](https://microsoft.github.io/autogen/docs/tutorial/conversation-patterns/) — patterns de conversation multi-agent
- [CrewAI — Agent Communication](https://docs.crewai.com/concepts/agents) — patterns de délégation et feedback

##### Story 4.2 — Agent Worker Process

**Description** : Chaque agent peut tourner comme un worker isolé avec son propre LLM, recevant des tâches via le message bus.

**Acceptance Criteria** :
- [ ] Classe `AgentWorker` dans `bmad.core.agent_worker`
- [ ] Chaque worker : charge sa persona, se connecte au bus, écoute les messages
- [ ] Le worker utilise le LLM Router pour sélectionner son modèle
- [ ] Support des providers : Anthropic API, OpenAI API, Ollama (local), Copilot (via MCP)
- [ ] Healthcheck et graceful shutdown
- [ ] Max parallel workers configurable dans `bmad.yaml`

**Références** :
- [LangGraph — Multi-agent](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) — patterns de multi-agent avec state sharing
- [MetaGPT — SOP](https://github.com/geekan/MetaGPT) — Standard Operating Procedures pour agents, communication par artifacts
- [Swarm (OpenAI)](https://github.com/openai/swarm) — framework minimaliste multi-agent, handoff patterns
- [Semantic Kernel — Multi-agent](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-chat) — framework Microsoft pour orchestration multi-agent

##### Story 4.3 — Orchestrateur avec mode hybride

**Description** : L'orchestrateur BMAD (SM/Bob ou BMad Master) décide dynamiquement du mode d'exécution (simulated/sequential/parallel) selon le type de tâche.

**Acceptance Criteria** :
- [ ] Logique de décision dans `bmad.core.orchestrator`
- [ ] Rules : party-mode → simulated, boomerang → sequential, adversarial-review → parallel
- [ ] Override possible dans le workflow YAML : `mode: parallel`
- [ ] Monitoring du coût en temps réel : si budget dépassé, fallback vers simulated
- [ ] Dashboard via `bmad agents status`

**Références** :
- [Roo-Code Boomerang Tasks](https://docs.roo.ai/features/boomerang-tasks) — pattern d'orchestration avec delegation et retour
- [LangGraph — Supervisor pattern](https://langchain-ai.github.io/langgraph/concepts/multi_agent/#supervisor) — agent superviseur qui route les tâches

##### Story 4.4 — Delivery Contracts inter-agents

**Description** : Formaliser les interfaces entre agents avec des contrats typés (schéma d'entrée/sortie) pour que le multi-LLM fonctionne.

**Acceptance Criteria** :
- [ ] Template `delivery-contract.tpl.md` étendu avec JSON Schema pour input/output
- [ ] Validation automatique : le output d'un agent est validé contre le schéma avant envoi
- [ ] Retry avec feedback si la validation échoue (max 3 retries)
- [ ] Registry des contrats par type de tâche
- [ ] Tests d'intégration avec 2 LLMs différents

**Spec technique** :
```yaml
# delivery-contract: architecture-review
input_schema:
  type: object
  required: [files_to_review, constraints, story_id]
  properties:
    files_to_review:
      type: array
      items: { type: string }
    constraints:
      type: string
    story_id:
      type: string

output_schema:
  type: object
  required: [decision, rationale, complexity]
  properties:
    decision:
      type: string
      enum: [approve, reject, approve-with-conditions]
    rationale:
      type: string
      minLength: 50
    complexity:
      type: string
      enum: [S, M, L, XL]
    conditions:
      type: array
      items: { type: string }
```

**Références** :
- [BMAD Delivery Contract template](bmad-custom-kit/framework/delivery-contract.tpl.md) — template existant à étendre
- [JSON Schema](https://json-schema.org/) — standard pour la validation de données
- [Pydantic](https://docs.pydantic.dev/) — validation Python basée sur les types

---

### EPIC 5 — Session Intelligence (BM-44)

**Priorité** : 🟢 P2  
**Effort estimé** : L (3-4 semaines)  
**Dépendances** : Epic 2 (Qdrant RAG), Epic 3 (Token Optimization)

#### 5.1 Problème

Le session branching (BM-16) gère les outputs (fichiers) mais pas le **contexte conversationnel**. Impossible d'explorer deux idées en parallèle dans le chat, puis de merger les conclusions. Pas de conversations en background.

#### 5.2 Solution

Un système de gestion de session intelligent avec **branching de contexte conversationnel**, **synchronisation inter-branches**, et **agents en background**.

#### 5.3 Stories détaillées

##### Story 5.1 — Conversation Branching

**Description** : Permettre de créer des branches de conversation avec snapshot de contexte indépendant.

**Acceptance Criteria** :
- [ ] Commande `bmad session branch "explore-microservices"`
- [ ] Snapshot du contexte actuel (loaded files, Qdrant state, conversation history résumée)
- [ ] Chaque branche a son propre `state.json` avec contexte isolé
- [ ] Commande `bmad session list` affiche l'arbre des branches
- [ ] Commande `bmad session switch <branch>` restaure le contexte
- [ ] Les agents travaillant dans une branche ne voient pas les artifacts des autres branches

**Spec technique** :
```yaml
# _bmad-output/.runs/explore-microservices/state.json
{
  "branch": "explore-microservices",
  "parent": "main",
  "created_at": "2026-03-03T14:00:00Z",
  "created_by": "architect",
  "context_snapshot": {
    "loaded_files_hash": "abc123",
    "qdrant_snapshot_id": "snap_001",
    "conversation_summary": "Discussion sur la migration vers microservices...",
    "active_agents": ["architect", "dev"],
    "decisions_in_branch": ["ADR-043: service decomposition"]
  },
  "status": "active"
}
```

**Références** :
- [BMAD Session Branching (BM-16)](bmad-custom-kit/framework/sessions/README.md) — implémentation existante à étendre
- [Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) — inspiration pour le modèle de branches
- [Letta — Conversation branching](https://github.com/letta-ai/letta) — conversation threads avec context isolation

##### Story 5.2 — Context Merge et Diff

**Description** : Comparer et fusionner le contexte de deux branches de conversation.

**Acceptance Criteria** :
- [ ] Commande `bmad session diff <branch-a> <branch-b>`
- [ ] Affiche : décisions différentes, artifacts créés, learnings ajoutés
- [ ] Commande `bmad session merge <source> [--into <target>]`
- [ ] Merge intelligent : décisions conflictuelles → demande à l'utilisateur
- [ ] Le BMad Master peut servir de "merge arbitre" pour résumer et trancher
- [ ] Résultat du merge tracé dans `_bmad/_memory/merge-log.md`

**Références** :
- [Three-way merge algorithm](https://en.wikipedia.org/wiki/Merge_(version_control)#Three-way_merge) — algorithme de merge standard
- [Operational Transformation](https://en.wikipedia.org/wiki/Operational_transformation) — pour la résolution de conflits concurrents

##### Story 5.3 — Background Agent Tasks

**Description** : Permettre à des agents de continuer à travailler en arrière-plan (analyse, consolidation, veille) pendant que l'utilisateur interagit avec d'autres agents.

**Acceptance Criteria** :
- [ ] Commande `bmad background start <agent> <task>` lance une tâche async
- [ ] Le background agent écrit ses résultats dans `_bmad-output/.background/<task-id>/`
- [ ] Commande `bmad background status` affiche les tâches en cours
- [ ] Commande `bmad background check-in <task-id>` affiche les résultats intermédiaires
- [ ] Notification dans le greeting agent quand une tâche background est terminée
- [ ] Limit: max 2 tâches background simultanées (configurable)

**Cas d'usage concrets** :
1. Architect analyse la codebase en background pendant que Dev code une story
2. QA génère un plan de test en background pendant la revue d'architecture
3. Mnemo consolide la mémoire en background pendant les sessions actives

**Références** :
- [Celery — task queue](https://docs.celeryq.dev/) — pattern de tâches asynchrones Python
- [Claude computer use — background tasks](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) — patterns d'agents autonomes
- [AutoGen — Async agents](https://microsoft.github.io/autogen/docs/tutorial/conversation-patterns/) — patterns de conversation asynchrone

##### Story 5.4 — Conversation History Vectorization

**Description** : Vectoriser automatiquement l'historique conversationnel dans Qdrant pour le retrieval cross-session.

**Acceptance Criteria** :
- [ ] Hook post-session qui résume et vectorise la conversation
- [ ] Collection Qdrant `{project}-conversations` avec metadata (date, agents, topic, branch)
- [ ] Au démarrage d'une nouvelle session, retrieval des conversations passées pertinentes
- [ ] Configurable : `memory.conversation_history: true`, `memory.max_conversations: 50`
- [ ] Respect du RGPD : `bmad memory forget <topic>` supprime les vectors liés

**Références** :
- [ChatGPT Memory](https://help.openai.com/en/articles/8590148-memory-in-chatgpt-faq) — pattern de mémoire cross-session user-facing
- [mem0 — Conversation memory](https://github.com/mem0ai/mem0) — extraction et stockage d'insights depuis les conversations

---

### EPIC 6 — Function Calling et Tooling Natif (BM-45)

**Priorité** : 🟡 P1  
**Effort estimé** : M (2-3 semaines)  
**Dépendances** : Epic 1 (LLM Router)

#### 6.1 Problème

BMAD utilise MCP comme seul mécanisme de function calling, ce qui fonctionne dans l'IDE mais pas pour un framework multi-agent autonome. Les agents ne peuvent pas se déclencher programmatiquement entre eux ni utiliser les tools LLM natifs (Anthropic tool_use, OpenAI function calling).

#### 6.2 Solution

Ajouter le support du **function calling natif** des LLMs en plus de MCP, pour que les agents puissent utiliser des outils directement et se déléguer des tâches programmatiquement.

#### 6.3 Stories détaillées

##### Story 6.1 — Tool Registry unifié

**Description** : Registry qui expose les outils BMAD à la fois comme MCP tools ET comme function calling schemas natifs.

**Acceptance Criteria** :
- [ ] Classe `ToolRegistry` dans `bmad.core.tools`
- [ ] Chaque outil BMAD enregistré avec : name, description, JSON Schema des paramètres
- [ ] Export automatique en format MCP (pour IDE) et en format tool_use/function_calling (pour API directe)
- [ ] Les 48 outils existants enregistrés
- [ ] Tests de conformité des schémas

**Spec technique** :
```python
# bmad/core/tools.py

@dataclass
class BmadTool:
    name: str
    description: str
    parameters: dict  # JSON Schema
    handler: Callable
    
    def to_mcp(self) -> dict:
        """Export au format MCP tool."""
        ...
    
    def to_anthropic(self) -> dict:
        """Export au format Anthropic tool_use."""
        ...
    
    def to_openai(self) -> dict:
        """Export au format OpenAI function calling."""
        ...
```

**Références** :
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — spec officielle Anthropic
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) — spec officielle OpenAI
- [MCP Tool Protocol](https://modelcontextprotocol.io/docs/concepts/tools) — spec MCP pour les outils

##### Story 6.2 — Agent-to-Agent Tool Calling

**Description** : Permettre à un agent d'appeler un autre agent comme un "tool" via function calling.

**Acceptance Criteria** :
- [ ] Chaque agent exposé comme un tool appelable par les autres
- [ ] Le caller spécifie : agent cible, tâche, contexte, format de réponse attendu
- [ ] Le LLM Router sélectionne le bon modèle pour l'agent cible
- [ ] Résultat retourné comme tool response au caller
- [ ] Trace dans BMAD_TRACE.md
- [ ] Timeout configurable, retry avec feedback

**Références** :
- [Anthropic — Agentic tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview#agentic-tool-use) — pattern d'agents qui appellent d'autres agents comme tools
- [Swarm — Handoff](https://github.com/openai/swarm) — handoff pattern entre agents

---

### EPIC 7 — Câblage, Observabilité & Hardening (BM-46)

**Priorité** : 🔴 P0  
**Effort estimé** : L (3-4 semaines)  
**Dépendances** : Epics 1-6 (tous les 18 outils existants)  
**Lot** : 4

#### 7.1 Problème

Les 18 outils Synapse fonctionnent individuellement (753 tests unitaires passent) mais il n'existe **aucune validation que les outils collaborent correctement ensemble**. L'orchestrateur importe le message-bus et l'agent-worker par importlib, l'agent-caller utilise le llm-router, le token-budget appelle le context-summarizer — mais ces chaînes d'appels n'ont jamais été testées end-to-end. De plus, aucune trace d'exécution n'est émise automatiquement par les outils Synapse vers `BMAD_TRACE.md`, rendant le debug multi-agent aveugle. Enfin, chaque outil charge indépendamment `project-context.yaml` avec son propre code de parsing, créant de la duplication et des risques de divergence.

#### 7.2 Solution

1. **Tests d'intégration E2E** validant les scénarios multi-outils réels
2. **Middleware de traçabilité** (@traced decorator) émettant vers BMAD_TRACE.md
3. **Couverture de code mesurée** avec seuil minimum
4. **Comptage tokens précis** via tiktoken/Anthropic API
5. **Configuration centralisée Synapse** avec un seul point de chargement

#### 7.3 Stories détaillées

##### Story 7.1 — Tests d'intégration E2E Synapse

**Description** : Suite de tests d'intégration qui valide les flux réels entre outils Synapse : orchestrateur→agent-worker→message-bus→delivery-contracts→conversation-history.

**Acceptance Criteria** :
- [ ] Fichier `tests/test_integration_synapse.py`
- [ ] Scénario 1 — **Workflow boomerang complet** : Orchestrator crée un plan → démarre des workers via agent-worker → les workers échangent des messages via message-bus → le résultat est validé par delivery-contracts → l'exécution est historisée dans conversation-history
- [ ] Scénario 2 — **Chaîne token optimizer** : token-budget.check() détecte seuil 80% → déclenche context-summarizer.summarize() → vérifie que le nouveau chargement est sous le seuil
- [ ] Scénario 3 — **Agent calling complet** : agent-caller.call() → llm-router.route() sélectionne le modèle → delivery-contracts.validate_input() valide le payload → résultat tracé
- [ ] Scénario 4 — **Cache hit réel** : semantic-cache.store() → rag-indexer indexe → semantic-cache.query() retrouve par similarité → tool-registry vérifie que l'outil est enregistré
- [ ] Scénario 5 — **Branch + merge** : conversation-branch.branch() → modifications sur 2 branches → context-merge.diff() → context-merge.merge() → conversation-history.index() enregistre le résultat
- [ ] ≥ 30 tests d'intégration
- [ ] Tous passent avec `pytest` sans dépendances externes (mocks pour Qdrant/Redis)
- [ ] Temps d'exécution < 30s
- [ ] Marqueur pytest `@pytest.mark.integration` pour exécution séparée

**Spec technique** :
```python
# tests/test_integration_synapse.py

import pytest
import importlib.util
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).parent.parent / "framework" / "tools"

def _load_tool(name: str):
    """Charge un outil Synapse par importlib."""
    mod_name = name.replace("-", "_")
    mod_path = TOOLS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod

@pytest.mark.integration
class TestBoomerangWorkflow:
    """Valide le flux complet orchestrator → worker → bus → contracts → history."""
    
    def test_plan_and_execute_e2e(self, tmp_path):
        bus = _load_tool("message-bus")
        worker = _load_tool("agent-worker")
        orch = _load_tool("orchestrator")
        contracts = _load_tool("delivery-contracts")
        history = _load_tool("conversation-history")
        
        # 1. Orchestrator crée un plan
        o = orch.Orchestrator(str(tmp_path))
        plan = o.create_plan("boomerang", ["dev", "qa"], "implement auth")
        assert plan.mode in ("simulated", "sequential", "parallel")
        
        # 2. Workers démarrent
        wm = worker.AgentWorkerManager(str(tmp_path))
        wm.start_worker("dev")
        wm.start_worker("qa")
        
        # 3. Message bus transmet
        in_bus = bus.InProcessBus()
        in_bus.send(bus.AgentMessage(
            source_agent="dev", target_agent="qa",
            msg_type="task-request",
            payload={"task": "review auth code"}
        ))
        msg = in_bus.receive("qa")
        assert msg is not None
        
        # 4. Contract valide
        cr = contracts.ContractRegistry()
        result = cr.validate_input("code-review", {
            "files_to_review": ["src/auth.py"],
            "review_type": "security",
            "story_id": "US-42"
        })
        assert result["valid"]
        
        # 5. History enregistre
        hm = history.ConversationHistoryManager(str(tmp_path))
        entry = hm.index({"summary": "Auth workflow completed", "agents": ["dev", "qa"]})
        assert entry["status"] == "indexed"
```

**Références** :
- [pytest markers](https://docs.pytest.org/en/stable/how-to/mark.html) — `@pytest.mark.integration`
- [Python importlib](https://docs.python.org/3/library/importlib.html) — chargement dynamique de modules

##### Story 7.2 — Synapse Trace Middleware

**Description** : Decorator `@synapse_traced` et module `synapse-trace.py` qui capture automatiquement chaque appel MCP et chaque opération inter-outils, puis les écrit dans `_bmad-output/BMAD_TRACE.md` au format structuré existant.

**Acceptance Criteria** :
- [ ] Fichier `framework/tools/synapse-trace.py` (~400 lignes)
- [ ] Decorator `@synapse_traced(tool_name, operation)` applicable à toute fonction MCP
- [ ] Chaque trace inclut : timestamp, tool, operation, agent (si dispo), durée, tokens estimés, statut (ok/error)
- [ ] Format compatible avec les parseurs BMAD_TRACE existants (`cognitive-flywheel.py`, `dream.py`, `workflow-adapt.py`, `memory-lint.py`, `dna-evolve.py`)
- [ ] Mode `--dry-run` qui log en mémoire sans écrire le fichier
- [ ] CLI : `synapse-trace.py status` (résumé des traces), `synapse-trace.py search --tool orchestrator`, `synapse-trace.py export --format json`
- [ ] MCP : `mcp_synapse_trace(action, tool, query, format)`
- [ ] Rétrofit du decorator sur les 18 fonctions MCP existantes (optionnel, opt-in via config)
- [ ] ≥ 25 tests unitaires

**Spec technique** :
```python
# framework/tools/synapse-trace.py

from __future__ import annotations
import functools
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

@dataclass
class TraceEntry:
    timestamp: str
    tool: str
    operation: str
    agent: str = ""
    duration_ms: float = 0.0
    tokens_estimated: int = 0
    status: str = "ok"  # ok | error | timeout
    details: dict = field(default_factory=dict)

class SynapseTracer:
    """Centralized tracer for all Synapse tool operations."""
    
    def __init__(self, project_root: str, *, enabled: bool = True):
        self._root = Path(project_root)
        self._enabled = enabled
        self._entries: list[TraceEntry] = []
        self._trace_path = self._root / "_bmad-output" / "BMAD_TRACE.md"
    
    def record(self, entry: TraceEntry) -> None:
        """Record and persist a trace entry."""
        self._entries.append(entry)
        if self._enabled:
            self._append_to_file(entry)
    
    def _append_to_file(self, entry: TraceEntry) -> None:
        """Append entry in BMAD_TRACE.md compatible format."""
        line = (
            f"\n### [{entry.timestamp}] [SYNAPSE] {entry.tool}.{entry.operation}\n"
            f"- **Agent** : {entry.agent or 'system'}\n"
            f"- **Durée** : {entry.duration_ms:.0f}ms\n"
            f"- **Tokens** : ~{entry.tokens_estimated}\n"
            f"- **Statut** : {entry.status}\n"
        )
        if entry.details:
            line += f"- **Détails** : {entry.details}\n"
        self._trace_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._trace_path, "a") as f:
            f.write(line)

def synapse_traced(tool_name: str, operation: str):
    """Decorator that traces MCP function calls."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracer = _get_global_tracer()
            start = time.monotonic()
            status = "ok"
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as exc:
                status = "error"
                raise
            finally:
                elapsed = (time.monotonic() - start) * 1000
                tracer.record(TraceEntry(
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    tool=tool_name, operation=operation,
                    duration_ms=elapsed, status=status,
                ))
        return wrapper
    return decorator
```

**Références** :
- [BMAD_TRACE.md format](framework/bmad-trace.md) — spec du format de trace existant
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/) — inspiration pour le pattern de traçabilité
- [functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps) — préservation des métadonnées

##### Story 7.3 — Couverture de code & CI

**Description** : Configurer `pytest-cov` pour mesurer la couverture des 18 outils Synapse et définir un seuil minimum.

**Acceptance Criteria** :
- [ ] `pytest-cov` configuré dans `ruff.toml` ou `pyproject.toml`
- [ ] Commande : `python3 -m pytest --cov=framework/tools --cov-report=term-missing tests/test_*.py`
- [ ] Rapport de couverture généré dans `_bmad-output/bench-reports/coverage-synapse.txt`
- [ ] Seuil minimum : ≥ 80% par outil, ≥ 85% global
- [ ] Branches non couvertes identifiées et documentées
- [ ] ≥ 10 tests additionnels pour couvrir les branches manquantes identifiées
- [ ] Script `tests/run-coverage.sh` pour exécution en one-liner

**Spec technique** :
```bash
#!/bin/bash
# tests/run-coverage.sh
set -e
cd "$(dirname "$0")/.."

# Tous les test files Intelligence Layer
TEST_FILES=$(find tests -name "test_*.py" | grep -E \
  "llm_router|rag_indexer|rag_retriever|memory_sync|bmad_mcp|context_summarizer|semantic_cache|token_budget|tool_registry|agent_caller|message_bus|delivery_contracts|conversation_branch|background_tasks|agent_worker|orchestrator|context_merge|conversation_history|integration_synapse|synapse_trace" \
  | sort)

python3 -m pytest $TEST_FILES \
  --cov=framework/tools \
  --cov-report=term-missing \
  --cov-report=html:_bmad-output/bench-reports/htmlcov \
  --cov-fail-under=80 \
  -q

echo "✅ Coverage report: _bmad-output/bench-reports/htmlcov/index.html"
```

**Références** :
- [pytest-cov](https://pytest-cov.readthedocs.io/) — plugin pytest pour coverage
- [coverage.py](https://coverage.readthedocs.io/) — le moteur sous-jacent

##### Story 7.4 — Comptage tokens précis

**Description** : Remplacer l'heuristique `len(text) / 4` dans `token-budget.py` par un comptage précis utilisant `tiktoken` (pour GPT) et l'API Anthropic count_tokens (pour Claude).

**Acceptance Criteria** :
- [ ] Module `TokenCounter` abstract avec backends : `HeuristicCounter` (actuel, fallback), `TiktokenCounter` (pip install tiktoken), `AnthropicCounter` (API)
- [ ] Auto-détection du backend selon le modèle (via LLM Router config)
- [ ] Fallback gracieux : si tiktoken pas installé → heuristique
- [ ] Précision : erreur ≤ 5% vs comptage réel pour Claude Sonnet sur 100 prompts de test
- [ ] Patch dans `token-budget.py` : remplacer `_estimate_tokens()` par `TokenCounter.count()`
- [ ] ≥ 20 tests unitaires comparant heuristique vs tiktoken
- [ ] Benchmark `_bmad-output/bench-reports/token-accuracy.md`

**Spec technique** :
```python
# Extension dans token-budget.py ou module séparé

class TokenCounter(ABC):
    @abstractmethod
    def count(self, text: str) -> int: ...

class HeuristicCounter(TokenCounter):
    """Fallback : len(text) / 4."""
    def count(self, text: str) -> int:
        return max(1, len(text) // 4)

class TiktokenCounter(TokenCounter):
    """Precise counting for OpenAI/GPT models."""
    def __init__(self, model: str = "gpt-4"):
        import tiktoken
        self._enc = tiktoken.encoding_for_model(model)
    
    def count(self, text: str) -> int:
        return len(self._enc.encode(text))

class AnthropicCounter(TokenCounter):
    """API-based counting for Claude models."""
    def count(self, text: str) -> int:
        # Uses anthropic.Client().count_tokens()
        ...

def get_counter(model: str) -> TokenCounter:
    """Factory — sélectionne le bon compteur selon le modèle."""
    if "gpt" in model or "o1" in model:
        try:
            return TiktokenCounter(model)
        except ImportError:
            pass
    return HeuristicCounter()
```

**Références** :
- [tiktoken](https://github.com/openai/tiktoken) — tokenizer BPE rapide d'OpenAI
- [Anthropic token counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting) — API count_tokens
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers) — alternative pour modèles locaux

##### Story 7.5 — Configuration centralisée Synapse

**Description** : Factoriser le code de chargement `project-context.yaml` dupliqué dans les 18 outils en un module commun `synapse-config.py`.

**Acceptance Criteria** :
- [ ] Fichier `framework/tools/synapse-config.py` (~250 lignes)
- [ ] Fonction `load_synapse_config(project_root) -> SynapseConfig` qui charge et valide la config
- [ ] Config consolidée : tous les paramètres Synapse dans une section `synapse:` de `project-context.yaml`
- [ ] Sections : `synapse.llm_router`, `synapse.rag`, `synapse.token_budget`, `synapse.semantic_cache`, `synapse.message_bus`, `synapse.orchestrator`, `synapse.trace`
- [ ] Defaults raisonnables pour chaque paramètre (aucune config requise pour démarrer)
- [ ] Validation des types et ranges (seuils entre 0 et 1, TTL > 0, etc.)
- [ ] Les 18 outils modifiés pour appeler `load_synapse_config()` au lieu de leur propre code de parsing
- [ ] Rétrocompat : si la section `synapse:` n'existe pas, les outils fonctionnent avec les defaults
- [ ] CLI : `synapse-config.py show`, `synapse-config.py validate`, `synapse-config.py generate-template`
- [ ] MCP : `mcp_synapse_config(action)`
- [ ] ≥ 20 tests unitaires

**Spec technique** :
```yaml
# project-context.yaml — section Synapse
synapse:
  enabled: true
  trace:
    enabled: true
    output: _bmad-output/BMAD_TRACE.md
    
  llm_router:
    default_model: claude-sonnet
    fallback_chain: [claude-haiku, deepseek-coder]
    budget_per_session: 100000  # tokens
    
  rag:
    embedding_model: all-MiniLM-L6-v2
    qdrant_path: .qdrant_data
    chunk_size: 512
    chunk_overlap: 50
    
  token_budget:
    warning_threshold: 0.6
    auto_summarize_threshold: 0.8
    critical_threshold: 0.95
    counter: auto  # auto | heuristic | tiktoken
    
  semantic_cache:
    similarity_threshold: 0.9
    ttl_hours: 168
    max_entries: 10000
    
  message_bus:
    backend: in-process  # in-process | redis | nats
    redis_url: redis://localhost:6379
    
  orchestrator:
    default_mode: auto  # auto | simulated | sequential | parallel
    budget_cap: 50000
    max_concurrent: 3
```

```python
# framework/tools/synapse-config.py

@dataclass
class SynapseConfig:
    enabled: bool = True
    trace: TraceConfig = field(default_factory=TraceConfig)
    llm_router: LLMRouterConfig = field(default_factory=LLMRouterConfig)
    rag: RAGConfig = field(default_factory=RAGConfig)
    token_budget: TokenBudgetConfig = field(default_factory=TokenBudgetConfig)
    semantic_cache: SemanticCacheConfig = field(default_factory=SemanticCacheConfig)
    message_bus: MessageBusConfig = field(default_factory=MessageBusConfig)
    orchestrator: OrchestratorConfig = field(default_factory=OrchestratorConfig)

_CONFIG_CACHE: dict[str, SynapseConfig] = {}

def load_synapse_config(project_root: str | Path) -> SynapseConfig:
    """Point d'entrée unique pour toute la config Synapse."""
    root = str(Path(project_root).resolve())
    if root in _CONFIG_CACHE:
        return _CONFIG_CACHE[root]
    # ... parse project-context.yaml, validate, cache
```

**Références** :
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — pattern de config typée avec defaults
- [12 Factor App — Config](https://12factor.net/config) — config séparée du code

---

### EPIC 8 — Production Ready (BM-47)

**Priorité** : 🟡 P1  
**Effort estimé** : XL (4-6 semaines)  
**Dépendances** : Epic 7 (câblage validé)  
**Lot** : 5

#### 8.1 Problème

Après le câblage et l'observabilité (Epic 7), les outils Synapse restent en mode **simulated** — l'agent-worker ne fait pas de vrais appels LLM, le message-bus n'a que le backend in-process, l'orchestrateur ne parallélise pas réellement, et le dashboard ne monitore pas les outils Synapse. Pour passer en production, il faut connecter chaque pièce à ses backends réels.

#### 8.2 Solution

1. **Vrais appels LLM** via LiteLLM dans agent-worker
2. **Backend Redis** réel pour message-bus
3. **Parallélisme asyncio** dans l'orchestrateur
4. **Dashboard Synapse** connecté aux 18 outils
5. **Exposition MCP complète** de tous les outils

#### 8.3 Stories détaillées

##### Story 8.1 — Vrais appels LLM (LiteLLM integration)

**Description** : Remplacer les réponses simulées d'`agent-worker.py` par de vrais appels API via LiteLLM, en respectant le routing du LLM Router.

**Acceptance Criteria** :
- [ ] `pip install litellm` comme dépendance optionnelle
- [ ] Class `LiteLLMBackend` dans `agent-worker.py` qui fait de vrais appels API
- [ ] Fallback `SimulatedBackend` (actuel) si litellm pas installé
- [ ] Chaîne complète : llm-router choisit le modèle → agent-worker appelle via litellm → résultat validé par delivery-contracts
- [ ] Support streaming (generator pour réponses longues)
- [ ] Métriques : tokens réels, coût réel, latence
- [ ] Env vars : `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OLLAMA_BASE_URL`
- [ ] ≥ 30 tests (mocks pour les appels API, 3 tests live optionnels)

**Spec technique** :
```python
# Extension agent-worker.py

class LiteLLMBackend:
    """Backend réel utilisant LiteLLM pour appels API multi-provider."""
    
    def __init__(self, router_config: dict):
        import litellm
        self._litellm = litellm
    
    def execute(self, agent_id: str, model: str, task: dict) -> dict:
        """Exécute une tâche en appelant le LLM réel."""
        messages = self._build_messages(agent_id, task)
        response = self._litellm.completion(
            model=model,
            messages=messages,
            temperature=0.3,
        )
        return {
            "result": response.choices[0].message.content,
            "model_used": model,
            "tokens": {
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
                "total": response.usage.total_tokens,
            },
            "cost": response._hidden_params.get("response_cost", 0),
        }
    
    def execute_stream(self, agent_id: str, model: str, task: dict):
        """Version streaming pour réponses longues."""
        ...
```

**Références** :
- [LiteLLM](https://github.com/BerriAI/litellm) — proxy unifié 100+ providers
- [LiteLLM Router](https://docs.litellm.ai/docs/routing) — routing + fallback intégré
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) — alternative directe

##### Story 8.2 — Backend Redis pour Message Bus

**Description** : Implémenter `RedisBus` dans `message-bus.py` avec Redis Streams pour la communication inter-agents en mode sequential/parallel.

**Acceptance Criteria** :
- [ ] `pip install redis` comme dépendance optionnelle
- [ ] Classe `RedisBus` implémentant la même interface que `InProcessBus`
- [ ] Utilisation de Redis Streams (`XADD`, `XREAD`, `XREADGROUP`)
- [ ] Consumer groups pour répartition de charge entre workers
- [ ] Messages persistés avec TTL configurable (défaut 24h)
- [ ] Auto-détection : si Redis disponible et configuré → RedisBus, sinon → InProcessBus
- [ ] Fallback gracieux si Redis tombe en cours d'exécution
- [ ] ≥ 25 tests (mocks Redis + 3 tests live optionnels avec Redis local)

**Spec technique** :
```python
# Extension message-bus.py

class RedisBus(MessageBusBackend):
    """Backend Redis Streams pour communication inter-agents."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        import redis
        self._r = redis.from_url(redis_url, decode_responses=True)
        self._consumer_group = "bmad-synapse"
    
    def send(self, message: AgentMessage) -> SendResult:
        stream_key = f"bmad:agent:{message.target_agent}"
        msg_id = self._r.xadd(stream_key, {
            "source": message.source_agent,
            "type": message.msg_type,
            "payload": json.dumps(message.payload),
        })
        return SendResult(success=True, message_id=msg_id)
    
    def receive(self, agent_id: str, timeout_ms: int = 5000) -> AgentMessage | None:
        stream_key = f"bmad:agent:{agent_id}"
        # Ensure consumer group exists
        try:
            self._r.xgroup_create(stream_key, self._consumer_group, mkstream=True)
        except redis.ResponseError:
            pass  # Group already exists
        
        entries = self._r.xreadgroup(
            self._consumer_group, agent_id,
            {stream_key: ">"}, count=1, block=timeout_ms,
        )
        if not entries:
            return None
        # Parse and acknowledge
        ...
```

**Références** :
- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/) — doc officielle
- [Redis Consumer Groups](https://redis.io/docs/latest/develop/data-types/streams/#consumer-groups) — répartition de charge
- [redis-py](https://github.com/redis/redis-py) — client Python officiel

##### Story 8.3 — Parallélisme réel dans l'orchestrateur

**Description** : Implémenter le mode `parallel` de l'orchestrateur avec `concurrent.futures.ThreadPoolExecutor` pour exécuter réellement plusieurs agents-workers sur des LLMs distincts en parallèle.

**Acceptance Criteria** :
- [ ] Mode `parallel` utilise `concurrent.futures.ThreadPoolExecutor` ou `asyncio`
- [ ] Chaque worker s'exécute dans un thread séparé avec son propre appel LLM (via agent-worker)
- [ ] Communication inter-threads via message-bus (InProcessBus suffisant car thread-safe)
- [ ] Mécanisme de barrier/join : l'orchestrateur attend tous les workers avant de consolider
- [ ] Timeout configurable par worker (défaut 120s)
- [ ] Supervision : si un worker échoue, les autres continuent + l'erreur est signalée
- [ ] Budget global : si le cumul dépasse `budget_cap`, fallback vers simulated
- [ ] ≥ 25 tests (dont 5 testant la réelle concurrence avec `threading.Event`)

**Spec technique** :
```python
# Extension orchestrator.py

from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

class ParallelExecutor:
    """Exécute les agents en parallèle réel avec supervision."""
    
    def __init__(self, bus: InProcessBus, worker_mgr: AgentWorkerManager,
                 budget_cap: int, timeout: int = 120):
        self._bus = bus
        self._worker = worker_mgr
        self._budget_cap = budget_cap
        self._timeout = timeout
    
    def execute(self, plan: ExecutionPlan) -> ExecutionResult:
        results = {}
        total_tokens = 0
        
        with ThreadPoolExecutor(max_workers=len(plan.agents)) as pool:
            futures = {}
            for step in plan.steps:
                future = pool.submit(
                    self._execute_step, step, plan.task
                )
                futures[future] = step.agent
            
            for future in as_completed(futures, timeout=self._timeout):
                agent = futures[future]
                try:
                    result = future.result()
                    results[agent] = result
                    total_tokens += result.get("tokens", {}).get("total", 0)
                    
                    # Budget check
                    if total_tokens > self._budget_cap:
                        pool.shutdown(wait=False, cancel_futures=True)
                        break
                except Exception as exc:
                    results[agent] = {"error": str(exc)}
        
        return ExecutionResult(results=results, total_tokens=total_tokens)
```

**Références** :
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) — ThreadPool/ProcessPool
- [asyncio](https://docs.python.org/3/library/asyncio.html) — alternative event-loop
- [LangGraph parallel branches](https://langchain-ai.github.io/langgraph/how-tos/branching/) — pattern d'exécution parallèle

##### Story 8.4 — Dashboard Synapse

**Description** : Connecter le `dashboard.py` existant aux 18 outils Synapse pour offrir une vue unifiée de l'état du système, des métriques et des traces.

**Acceptance Criteria** :
- [ ] Extension de `dashboard.py` avec une section "Synapse Intelligence Layer"
- [ ] Widgets : LLM Router stats, Cache hit rate, Token budget %, Workers actifs, Bus messages/s, Dernières traces
- [ ] Commande : `python3 dashboard.py --project-root . synapse`
- [ ] Output : Markdown formaté dans `_bmad-output/bench-reports/synapse-dashboard.md`
- [ ] Rafraîchissement live optionnel (`--watch` avec intervalle)
- [ ] Agrégation des données depuis : `llm-router stats`, `semantic-cache stats`, `token-budget report`, `agent-worker status`, `message-bus status`, `synapse-trace status`
- [ ] MCP : `mcp_synapse_dashboard(project_root, format)`
- [ ] ≥ 20 tests

**Spec technique** :
```python
# Extension dashboard.py

class SynapseDashboard:
    """Tableau de bord unifié pour tous les outils Synapse."""
    
    def __init__(self, project_root: str):
        self._root = Path(project_root)
        self._tools = self._load_synapse_tools()
    
    def render(self, format: str = "markdown") -> str:
        """Génère le dashboard complet."""
        sections = [
            self._render_header(),
            self._render_llm_router_stats(),
            self._render_cache_stats(),
            self._render_token_budget(),
            self._render_worker_status(),
            self._render_bus_status(),
            self._render_recent_traces(),
            self._render_coverage_summary(),
        ]
        return "\n\n".join(sections)
```

**Références** :
- [Rich Console](https://rich.readthedocs.io/) — terminal UI riche pour Python (optionnel)
- [Grafana Agent](https://grafana.com/docs/agent/latest/) — inspiration pour le pattern de dashboard

##### Story 8.5 — Exposition MCP complète

**Description** : Exposer les 18 outils Synapse + les 2 nouveaux (synapse-trace, synapse-config) comme MCP tools dans `bmad-mcp-tools.py`, pour une intégration IDE native complète.

**Acceptance Criteria** :
- [ ] Toutes les fonctions `mcp_*` des 20 outils enregistrées dans le serveur MCP
- [ ] Discovery : `bmad-mcp-tools.py list` affiche les 20 outils avec descriptions
- [ ] Chaque outil exposé avec son JSON Schema (via tool-registry)
- [ ] Tests : chaque MCP tool appelable via le protocole MCP standard
- [ ] Documentation : un tableau récapitulatif de tous les outils MCP Synapse
- [ ] Config MCP IDE générée automatiquement : `synapse-config.py generate-mcp`
- [ ] ≥ 20 tests

**Références** :
- [MCP Tools Protocol](https://modelcontextprotocol.io/docs/concepts/tools) — spec officielle
- [VS Code MCP Servers](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) — intégration IDE

---

## 5. Références et Ressources Consolidées

### 5.1 Frameworks et Libraries — À étudier pour l'implémentation

| Ressource | URL | Pertinence pour BMAD |
|---|---|---|
| **LiteLLM** | https://github.com/BerriAI/litellm | Proxy unifié 100+ LLMs, API unique Python — base pour le LLM Router |
| **Semantic Router** | https://github.com/aurelio-labs/semantic-router | Routing sémantique par embeddings — classifieur léger pour le router |
| **RouteLLM (LMSYS)** | https://github.com/lm-sys/RouteLLM | Classifieurs entraînés pour routing, benchmarks publics |
| **LLMLingua** | https://github.com/microsoft/LLMLingua | Compression de prompt 2-5x sans perte — cœur du Token Optimizer |
| **GPTCache** | https://github.com/zilliztech/GPTCache | Cache sémantique multi-backend — pattern pour le Semantic Cache |
| **Qdrant MCP Server** | https://github.com/qdrant/mcp-server-qdrant | Accès Qdrant depuis IDE — intégration immédiate |
| **nomic-embed-text** | https://huggingface.co/nomic-ai/nomic-embed-text-v1.5 | Embedding model open-source, top MTEB — pour indexation locale |
| **BGE Reranker** | https://huggingface.co/BAAI/bge-reranker-v2-m3 | Reranking open-source — pour améliorer la qualité du retrieval |
| **CrewAI** | https://github.com/joaomdmoura/crewAI | Patterns multi-agent, task delegation, tools — inspiration architecture |
| **AutoGen** | https://github.com/microsoft/autogen | GroupChat, async agents, conversation patterns |
| **LangGraph** | https://github.com/langchain-ai/langgraph | Stateful graphs, checkpointing, multi-agent patterns |
| **Swarm (OpenAI)** | https://github.com/openai/swarm | Framework minimaliste, handoff patterns — simplicité à viser |
| **MetaGPT** | https://github.com/geekan/MetaGPT | SOP-based multi-agent, communication par artifacts |
| **Letta (MemGPT)** | https://github.com/letta-ai/letta | Tiered memory, context management, conversation branching |
| **mem0** | https://github.com/mem0ai/mem0 | Memory layer, contradiction detection, cross-session |
| **RTK** | https://github.com/rtk-ai/rtk | Token optimization runtime — inspiration pour Epic 3 |

### 5.2 Documentation officielle — Pour l'implémentation

| Ressource | URL | Usage |
|---|---|---|
| **Qdrant Docs** | https://qdrant.tech/documentation/ | API collections, batch upload, filtering, snapshots |
| **Anthropic Tool Use** | https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview | Function calling spec |
| **Anthropic Prompt Caching** | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching | Cache côté provider |
| **Anthropic RAG guide** | https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation | Best practices RAG |
| **OpenAI Function Calling** | https://platform.openai.com/docs/guides/function-calling | Function calling spec |
| **MCP Protocol** | https://modelcontextprotocol.io/ | Spec complète du protocol |
| **MCP Python SDK** | https://github.com/modelcontextprotocol/python-sdk | SDK Python officiel |
| **Google A2A Protocol** | https://google.github.io/A2A/ | Standard communication inter-agents |
| **Redis Streams** | https://redis.io/docs/latest/develop/data-types/streams/ | Message bus option |
| **NATS JetStream** | https://docs.nats.io/nats-concepts/jetstream | Message bus option haute perf |
| **JSON Schema** | https://json-schema.org/ | Validation delivery contracts |
| **Pydantic v2** | https://docs.pydantic.dev/ | Validation Python typée |

### 5.3 Papers et Articles — Contexte théorique

| Ressource | Pertinence |
|---|---|
| [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) | Fondements du RAG — paper original Facebook Research |
| [RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059) | Chunking hiérarchique par arbre — Stanford, 2024 |
| [RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665) | Routing basé sur les préférences — LMSYS, 2024 |
| [LLMLingua: Compressing Prompts for Accelerated Inference](https://arxiv.org/abs/2310.05736) | Compression de prompt — Microsoft Research, 2023 |
| [Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) | MetaGPT paper — multi-agent pour dev logiciel |
| [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155) | AutoGen paper — conversations multi-agent |
| [A Survey on Large Language Model based Multi-Agent Systems](https://arxiv.org/abs/2402.01680) | Survey complet multi-agent LLM — état de l'art 2024 |

### 5.4 Fichiers BMAD existants — À réutiliser/étendre

| Fichier | Comment il s'intègre dans ce PRD |
|---|---|
| `framework/context-router.md` (BM-07) | Base du Token Optimizer — étendre avec enforcement actif |
| `framework/agent2agent.md` (BM-32) | Base du Real Multi-Agent — implémenter les transports réels |
| `framework/sessions/README.md` (BM-16) | Base du Conversation Branching — ajouter context snapshots |
| `framework/workflows/subagent-orchestration.md` (BM-19) | Base du parallélisme réel — remplacer le fallback séquentiel |
| `framework/workflows/boomerang-orchestration.md` (BM-11) | Utilise le LLM Router pour model selection par step |
| `framework/memory/mem0-bridge.py` | Migration vers le RAG Pipeline — dual-write d'abord |
| `framework/memory/backends/backend_qdrant_local.py` | Base pour le backend RAG Qdrant |
| `framework/memory/backends/backend_qdrant_server.py` | Backend pour Qdrant déployé |
| `framework/memory/maintenance.py` | Étendre avec summarization automatique |
| `framework/delivery-contract.tpl.md` | Base pour les Delivery Contracts typés (JSON Schema) |
| `framework/bmad-trace.md` | Traçabilité des appels multi-agent |

---

## 6. Contraintes et Risques

### 6.1 Contraintes non-négociables

| # | Contrainte | Rationale |
|---|---|---|
| C1 | **Local-first** | Tout doit fonctionner sans connexion internet. Les APIs cloud sont optionnelles. |
| C2 | **Dégradation gracieuse** | Si Qdrant est down → fallback fichiers MD. Si LLM Router échoue → modèle par défaut. Si message bus down → mode simulated. |
| C3 | **Coût transparent** | L'utilisateur voit toujours le coût estimé avant exécution multi-agent. |
| C4 | **Rétrocomp v3** | Tout doit être compatible avec la structure bmad.yaml v3. |
| C5 | **Opt-in** | Chaque fonctionnalité est désactivée par défaut. L'utilisateur active ce qu'il veut. |
| C6 | **Python 3.12+ stdlib-first** | Dépendances externes minimales et optionnelles. |

### 6.2 Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Le multi-LLM produit des incohérences inter-agents | Élevée | Haute | Delivery Contracts typés + validation schema |
| Qdrant ajoute de la complexité d'infra pour le solo dev | Moyenne | Haute | Mode `embedded` (qdrant-client sans serveur) + fallback fichiers |
| Le LLM Router basé sur heuristiques est trop simpliste | Moyenne | Moyenne | Commencer par rules statiques, itérer vers ML-based (RouteLLM) |
| Coût multi-agent réel prohibitif | Moyenne | Haute | Mode hybride + budget caps + dashboard coûts |
| Message bus (Redis/NATS) = over-engineering pour solo dev | Élevée | Moyenne | Backend `in-process` par défaut, Redis/NATS pour power users |
| Scope creep — trop d'epics en parallèle | Élevée | Haute | Séquencer strictement : Epic 1+2 d'abord, puis 3, puis 4+5+6 |

---

## 7. Métriques de Succès

| Métrique | Actuel | Cible v3.1 |
|---|---|---|
| Modèles utilisables simultanément | 1 | ≥ 3 (via LLM Router) |
| Coût token moyen par session | 100% (baseline) | -40% (via routing + cache) |
| Temps de retrieval mémoire sémantique | N/A (fichiers bruts) | < 200ms (Qdrant) |
| Tokens gaspillés sur contexte ancien | ~30% du budget | < 10% (via summarization) |
| Agents pouvant travailler en parallèle | 0 (séquentiel simulé) | ≥ 3 (mode parallel) |
| Hit rate cache sémantique | 0% | ≥ 25% après 1 semaine |
| Branches de conversation actives | 0 | ≥ 2 simultanées |
| Temps d'indexation full project | N/A | < 60s pour 500 fichiers |

---

## 8. Hors Scope

- **UI Web pour le monitoring** : tout reste terminal + IDE
- **Training de modèles custom** : on utilise des modèles existants, on ne les fine-tune pas
- **Multi-tenant** : BMAD est local, mono-utilisateur
- **Orchestration de containers** : les agents ne lancent pas de containers (sauf Qdrant via docker-compose)
- **Real-time streaming inter-agents** : communication par messages discrets, pas de streaming continu

---

## 9. Roadmap de livraison

```
                     Mars 2026                  Avril 2026                  Mai 2026                   Juin 2026
                ┌─────────────┐            ┌─────────────┐           ┌──────────────┐
Lot 1 (P0)     │ Epic 1: LLM │            │ Epic 2: RAG │           │              │
 ✅ COMPLET     │ Router       │            │ Qdrant      │           │   Stabilize  │
                │ (BM-40)     │            │ (BM-42)     │           │   + Docs     │
                └─────────────┘            └─────────────┘           └──────────────┘
                                                                    
                                           ┌─────────────┐           ┌──────────────┐
Lot 2 (P1)                                │ Epic 3:     │           │ Epic 6:      │
 ✅ COMPLET                                │ Token Optim │           │ Function     │
                                           │ (BM-41)     │           │ Calling      │
                                           └─────────────┘           │ (BM-45)      │
                                                                     └──────────────┘

                                                                     ┌──────────────┐
Lot 3 (P0)                                                          │ Epic 4+5:    │
 ✅ COMPLET                                                          │ Real Multi-  │
                                                                     │ Agent +      │
                                                                     │ Session Intel│
                                                                     └──────────────┘

                                                                     ┌──────────────┐  ┌──────────────┐
Lot 4 (P0)                                                          │ Epic 7:      │  │              │
 ⏳ PLANIFIÉ                                                         │ Câblage &    │  │   Tests +    │
                                                                     │ Observabilité│  │   Coverage   │
                                                                     │ (BM-46)      │  │              │
                                                                     └──────────────┘  └──────────────┘

                                                                                        ┌──────────────┐
Lot 5 (P1)                                                                             │ Epic 8:      │
 ⏳ PLANIFIÉ                                                                            │ Production   │
                                                                                        │ Ready        │
                                                                                        │ (BM-47)      │
                                                                                        └──────────────┘
```

**Séquencement** :
1. **Lot 1** ✅ : LLM Router + Qdrant RAG — les fondations
2. **Lot 2** ✅ : Token Optimization + Function Calling — efficacité et tooling
3. **Lot 3** ✅ : Multi-Agent Réel + Session Intelligence — la vision complète
4. **Lot 4** ⏳ : Câblage E2E, Observabilité, Couverture, Config centralisée — transformer 18 pièces en plateforme cohérente
5. **Lot 5** ⏳ : Production Ready — vrais appels LLM, Redis, parallélisme, Dashboard, MCP complet

---

## 10. Décision d'approbation

> **Ce PRD ajoute une couche d'intelligence à BMAD Kit v3** — LLM routing, mémoire sémantique Qdrant, optimisation de tokens, communication multi-agent réelle, et gestion de session avancée — transformant le framework d'un orchestrateur mono-LLM simulé en une plateforme d'agents véritablement intelligente et économe.

**Prochaine étape** : Sprint planning Lot 4 (Epic 7 — Câblage & Observabilité).

---

*Document rédigé le 3 mars 2026 — Session Party Mode multi-agent (John + Winston + Mary + Amelia + Barry)*  
*Mise à jour le 4 mars 2026 — Lots 1-3 livrés (753 tests), Epics 7-8 ajoutés (Lots 4-5)*
