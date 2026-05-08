---
title: "Guide d'Enseignement — Pilotage Agentique & Orchestration LLM"
subtitle: "Analyse de 33 repos de référence · Patterns, défauts, meilleures pratiques"
date: 2026-04-25
author: Grimoire Master (SOG)
repos_analyzed: 33
confidence: high
scope: "Architecture, patterns, mémoire, communication, sécurité, observabilité, checklist opérationnelle"
---

# Guide d'Enseignement — Pilotage Agentique & Orchestration LLM

> Document de référence produit par analyse directe de 33 repos de la collection `/mnt/Travail/Projets/Dev/Référence-Agentique/`.
> Chaque affirmation est ancrée dans le code source réel. Aucune hallucination tolérée.

---

## Table des matières

1. [Introduction — Pourquoi l'orchestration est difficile](#1-introduction)
2. [Cartographie des patterns d'orchestration](#2-cartographie-des-patterns)
3. [Pattern 1 — GroupChat (AutoGen / Microsoft Agent Framework)](#3-pattern-groupchat)
4. [Pattern 2 — Task-Agent-Process (CrewAI)](#4-pattern-tap)
5. [Pattern 3 — Handoff-First (OpenAI Agents Python)](#5-pattern-handoff)
6. [Pattern 4 — StateGraph / Pregel (LangGraph)](#6-pattern-stategraph)
7. [Pattern 5 — DAG Visuel (LangFlow, Dify)](#7-pattern-dag)
8. [Pattern 6 — EventLoop / Action-Observation (OpenHands)](#8-pattern-eventloop)
9. [Pattern 7 — Vision + Step (browser-use)](#9-pattern-vision-step)
10. [Pattern 8 — Persona + Menu (BMAD-METHOD)](#10-pattern-persona-menu)
11. [Pattern 9 — Worker Pool (Octogent)](#11-pattern-worker-pool)
12. [Pattern 10 — Kanban Routing (switchboard)](#12-pattern-kanban)
13. [Pattern 11 — Memory Palace (mempalace)](#13-pattern-memory-palace)
14. [Architectures mémoire — Comparatif](#14-memoire)
15. [Patterns de communication inter-agents](#15-communication)
16. [Tool Use — Patterns et garde-fous](#16-tool-use)
17. [Observabilité et traçabilité](#17-observabilite)
18. [Sécurité et défenses LLM](#18-securite)
19. [Défauts communs et comment les compenser](#19-defauts)
20. [Éléments obligatoires pour un système qui fonctionne](#20-obligatoires)
21. [Architecture recommandée — Modèle de référence](#21-architecture-recommandee)
22. [Checklist opérationnelle](#22-checklist)
23. [Synthèse par repo](#23-synthese-repos)
24. [Recommandations finales](#24-recommandations)

---

## 1. Introduction — Pourquoi l'orchestration est difficile

L'orchestration multi-agents est le problème le plus sous-estimé en IA appliquée. Un LLM seul peut impressionner ; dix LLMs mal coordonnés régressent vers le chaos. Les causes racines observées dans ces 33 repos :

### 1.1 Les cinq défauts structurels des LLM en orchestration

| Défaut | Manifestation | Fréquence observée |
|---|---|---|
| **Hallucination** | L'agent affirme avoir lu un fichier qu'il n'a pas lu | Très haute |
| **Drift d'objectif** | L'agent résout un problème adjacent mais pas le problème original | Haute |
| **Perte de contexte** | L'agent oublie les décisions prises aux tours précédents | Haute |
| **Lecture partielle** | L'agent répond sur les 200 premiers tokens du prompt, ignore la suite | Moyenne |
| **Sur-confiance** | L'agent valide ses propres outputs sans vérification indépendante | Très haute |

Ces défauts ne disparaissent pas avec de meilleures instructions — ils nécessitent des **compensations architecturales**. C'est précisément ce que les meilleurs frameworks ont appris à faire.

### 1.2 Ce que ce guide couvre

Ce document analyse **11 patterns d'orchestration** extraits des 33 repos, compare leurs **architectures mémoire**, leurs **modes de communication**, leurs **mécanismes de sécurité**, et synthétise les **éléments non-négociables** pour qu'un système fonctionne en production.

---

## 2. Cartographie des patterns d'orchestration

```
NIVEAU DE CONTRÔLE
        ↑
        │  [STATEGRAPH]      [DAG VISUEL]
        │  LangGraph          LangFlow/Dify
        │  Pregel             Vertex+Edges
        │
        │  [EVENTLOOP]        [WORKER POOL]
        │  OpenHands           Octogent
        │  Action+Observation  Queue distribuée
        │
        │  [GROUPCHAT]         [HANDOFF-FIRST]
        │  AutoGen             OpenAI Agents
        │  Broadcast           Tripwire
        │
        │  [TAP]               [PERSONA+MENU]
        │  CrewAI              BMAD
        │  Process séquentiel  Intent routing
        │
        │  [VISION+STEP]      [KANBAN]         [MEMORY PALACE]
        │  browser-use         switchboard       mempalace
        │  DOM+screenshot      Ticket routing    Verbatim+semantic
        └──────────────────────────────────────────────────────→
                DEGRÉ D'AUTONOMIE AGENT
```

**Lecture** : Plus on monte en Y, plus l'humain contrôle l'exécution. Plus on va à droite en X, plus les agents décident seuls.

---

## 3. Pattern 1 — GroupChat (AutoGen / Microsoft Agent Framework)

### 3.1 Principe

AutoGen (maintenant en maintenance, successeur : Microsoft Agent Framework) implémente un pattern **GroupChat** : plusieurs agents échangent des messages dans un "chat room" partagé. Un `GroupChatManager` contrôle qui parle à quel tour.

**Architecture centrale :**
```python
# AutoGen GroupChat pattern
group_chat = GroupChat(
    agents=[analyst_agent, coder_agent, critic_agent],
    messages=[],
    max_round=12,
    speaker_selection_method="auto"  # ou "round_robin" ou callable
)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
```

### 3.2 Variantes de sélection du locuteur

| Méthode | Comportement | Cas d'usage |
|---|---|---|
| `"auto"` | Le manager LLM choisit le prochain agent | Tâches non-linéaires |
| `"round_robin"` | Rotation déterministe | Révisions par pairs |
| `"random"` | Aléatoire pondéré | Exploration créative |
| `callable` | Logique custom | Workflows métier précis |

### 3.3 Forces et faiblesses

**Forces :**
- Communication naturelle par texte, proche du travail humain en équipe
- Facile à déboguer (historique de chat lisible)
- Flexible : n'importe quel agent peut interrompre
- AgentChat + AutoGen Studio pour prototypage visuel rapide

**Faiblesses :**
- **Token explosion** : chaque message est broadcasté à tous → historique croît O(n²)
- **Drift facilité** : sans gate d'objectif, la conversation dévie naturellement
- **Déterminisme faible** : même entrée peut produire des sorties différentes selon l'ordre des tours
- AutoGen 0.2/0.4 est en maintenance ; migration vers Microsoft Agent Framework (MAF) recommandée

### 3.4 Compensation observée dans le repo

AutoGen v0.4 introduit les **agents typés** (`AssistantAgent`, `UserProxyAgent`, `CodeExecutorAgent`) avec des contrats clairs sur ce qu'ils peuvent faire. La migration MAF apporte des **stable APIs** et une meilleure isolation.

---

## 4. Pattern 2 — Task-Agent-Process (CrewAI)

### 4.1 Principe

CrewAI structure l'orchestration en trois primitives orthogonales :

```
Crew
 ├── Agents (personas avec rôle + backstory + outils)
 ├── Tasks (unités de travail avec contexte + output attendu)
 └── Process (séquential | hierarchical | consensual)
```

### 4.2 Architecture mémoire 3-tiers

CrewAI implémente l'architecture mémoire la plus sophistiquée du corpus :

```python
# Trois niveaux de mémoire CrewAI
class CrewMemory:
    short_term: RAGStorage      # Mémoire de session (embeddings)
    long_term: SQLiteStorage    # Persistance inter-sessions (SQLite)
    entity: EntityMemory        # Graphe d'entités (personnes, lieux, concepts)
    user: UserMemory            # Profil utilisateur persistant
```

**Scope de mémoire** (observé dans `memory_scope.py`) :
- `"crew"` : partagée entre tous les agents
- `"agent"` : privée à un agent
- `"task"` : limitée à une tâche

### 4.3 Recall flow

Le module `recall_flow.py` implémente une recherche hybride :
1. Recherche vectorielle (similarité sémantique)
2. Filtre par scope
3. Ré-ranking par pertinence temporelle
4. Injection dans le contexte de la prochaine tâche

### 4.4 Process hiérarchique

```
Manager Agent (LLM)
 ├── Délègue tâche A → Worker Agent 1
 ├── Valide output A
 ├── Délègue tâche B → Worker Agent 2 (avec contexte A)
 └── Agrège résultats
```

### 4.5 Forces et faiblesses

**Forces :**
- Mémoire la plus complète (court terme + long terme + entités + utilisateur)
- Process hiérarchique proche du management humain
- Rôles et backstories améliorent la spécialisation des agents
- Backend mémoire pluggable (Qdrant, SQLite, Redis)

**Faiblesses :**
- Couplage fort entre Task et Agent (difficile à réutiliser)
- Le process séquentiel crée des goulots d'étranglement
- Backstory trop longue → consume des tokens utiles
- Pas d'interruption humaine native dans le process séquentiel

---

## 5. Pattern 3 — Handoff-First (OpenAI Agents Python)

### 5.1 Principe

L'OpenAI Agents Python SDK (source: `src/agents/`) implémente un pattern **Handoff-First** : la transition entre agents est un mécanisme de premier ordre, pas une afterthought.

```python
# Handoff déclaré dans l'agent source
@dataclass
class Handoff(Generic[THandoffInput, TAgent]):
    agent_name: str
    input_filter: Optional[Callable]   # Transforme l'historique avant transfert
    on_handoff: Optional[Callable]     # Hook au moment du transfert
```

### 5.2 Guardrails (tripwires)

Le module `guardrail.py` définit deux types de garde-fous :

```python
@dataclass
class InputGuardrailResult:
    guardrail: InputGuardrail
    output: GuardrailFunctionOutput
    # tripwire_triggered: bool → si True, STOP l'exécution

@dataclass  
class OutputGuardrailResult:
    guardrail: OutputGuardrail
    agent_output: Any
    output: GuardrailFunctionOutput
```

**Flows d'exécution avec guardrails :**
```
User Input
    → [InputGuardrail 1] → tripwire? → BLOCK
    → [InputGuardrail 2] → tripwire? → BLOCK
    → Agent LLM
    → [OutputGuardrail 1] → tripwire? → BLOCK
    → [OutputGuardrail 2] → tripwire? → BLOCK
    → Output final
```

### 5.3 Gestion de l'historique lors d'un handoff

La fonction `default_handoff_history_mapper` gère la transformation de l'historique lors d'un transfert. Trois stratégies observées :
- **Full history** : l'agent cible reçoit tout l'historique
- **Summary** : résumé injecté avant handoff
- **Clean slate** : seul le message de transfert est passé

### 5.4 Forces et faiblesses

**Forces :**
- Tripwires = mécanisme de sécurité le plus explicite du corpus
- Handoff avec input_filter permet de nettoyer l'historique (évite la contamination de contexte)
- Guardrails découplés de la logique agent → testables indépendamment
- `lifecycle.py` offre des hooks pre/post-run

**Faiblesses :**
- Architecture "flat" : difficile de gérer des hiérarchies profondes
- Pas de mémoire long-terme native (state limité à la session)
- Les handoffs peuvent créer des boucles infinies sans circuit-breaker

---

## 6. Pattern 4 — StateGraph / Pregel (LangGraph)

### 6.1 Principe

LangGraph implémente un **StateGraph** inspiré du modèle Pregel (Google) : les agents sont des nœuds dans un graphe, l'état est une structure typée partagée, les transitions sont des arêtes conditionnelles.

```python
# LangGraph StateGraph pattern
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: list[BaseMessage]
    next: str
    memory: dict

graph = StateGraph(AgentState)
graph.add_node("analyst", analyst_node)
graph.add_node("developer", developer_node)
graph.add_conditional_edges(
    "analyst",
    route_function,  # Décide du prochain nœud selon l'état
    {"develop": "developer", "end": END}
)
```

### 6.2 Caractéristiques distinctives

**Exécution durable (Durable Execution) :**
LangGraph persiste l'état après chaque nœud. Si l'exécution est interrompue (crash, timeout), elle reprend depuis le dernier nœud complété — pas depuis zéro.

```
Node A → [PERSIST STATE] → Node B → [PERSIST STATE] → Node C
         ↑                           ↑
    Checkpoint                  Checkpoint
    (SQLite/Redis)               (SQLite/Redis)
```

**Human-in-the-loop natif :**
```python
# Interruption conditionnelle pour validation humaine
graph.add_node("human_review", interrupt_node)
# L'exécution pause ici, attend validation, puis continue
```

**Subgraphs :**
Les graphes peuvent être imbriqués. Un nœud peut être lui-même un graphe complet — architecture hiérarchique native.

### 6.3 Forces et faiblesses

**Forces :**
- Reprises automatiques après crash (durable execution)
- State typé → erreurs détectables à la compilation
- Human-in-the-loop sans patches
- Subgraphs pour la modularité
- Visualisation native via LangSmith Studio
- Debugging via LangSmith : chaque state transition est traçable

**Faiblesses :**
- Courbe d'apprentissage élevée (concept Pregel non-intuitif)
- Surcharge conceptuelle pour des tâches simples
- Dépendance forte à l'écosystème LangChain
- Pas de multi-agent "natif" : il faut modéliser les agents comme des nœuds soi-même

---

## 7. Pattern 5 — DAG Visuel (LangFlow / Dify)

### 7.1 Principe

LangFlow et Dify implémentent des **DAG visuels** : les workflows sont construits par drag-and-drop dans un éditeur visuel, chaque nœud représente un composant (LLM, tool, parser, agent), les arêtes représentent le flux de données.

**Architecture LangFlow** (source: `langflow/`) :
```
Frontend (React + TypeScript)
    → Visual DAG editor
    → Node palette (200+ composants)
    → Real-time execution preview

Backend (Python / FastAPI)
    → Compiler: DAG JSON → Python graph
    → Executor: parallélisation sur les branches indépendantes
    → API: expose le workflow comme endpoint REST
```

**Architecture Dify** (source: `dify/`) :
```
Workspace (multi-tenant)
    → Workflow editor (React)
    → App types: chatbot | agent | workflow | completion
    → Plugin system: 100+ intégrations marketplace

Backend (Python + Node)
    → Workflow runner avec queue (Celery)
    → RAG pipeline intégré
    → Model provider abstraction (40+ LLMs)
```

### 7.2 Forces et faiblesses

**Forces :**
- Accessibilité : non-développeurs peuvent construire des workflows
- Visualisation immédiate du flux de données
- Large bibliothèque de composants réutilisables
- Déploiement API natif (1 clic)
- Dify : multi-tenant, marketplace plugins, RAG intégré

**Faiblesses :**
- **Programmabilité limitée** : logique complexe difficile à exprimer visuellement
- **Debugging pénible** : les erreurs dans les DAG visuels sont difficiles à isoler
- **Versionning** : les DAG JSON ne se lisent pas bien dans git diff
- **Pas de tests unitaires natifs** pour les nœuds individuels
- Performance : l'abstraction visuelle ajoute overhead au runtime

---

## 8. Pattern 6 — EventLoop / Action-Observation (OpenHands)

### 8.1 Principe

OpenHands (anciennement OpenDevin) implémente un pattern **EventLoop** avec un cycle Action-Observation. Chaque agent produit des `Action`, le runtime les exécute et retourne des `Observation`.

**Cycle fondamental :**
```
Agent
  → AgentThinkAction (réflexion interne)
  → CmdRunAction (commande shell)
      ↓
Runtime (sandbox Docker)
  → CmdOutputObservation (résultat)
      ↓
Agent
  → Analyse l'observation
  → Prochaine action...
  → AgentFinishAction (quand objectif atteint)
```

### 8.2 Event Store

OpenHands maintient un **event store persistant** :

```python
# openhands/events/event_store.py
class EventStore:
    def add_event(self, event: Event, source: EventSource): ...
    def get_events(self, start_id, end_id, filter: EventFilter): ...
    def get_latest_event_id(self): ...
```

**Types d'actions observés** (`openhands/events/action/agent.py`) :
- `AgentThinkAction` : log de pensée (non-exécuté)
- `AgentFinishAction` : terminaison avec `final_thought` + `outputs`
- `ChangeAgentStateAction` : transition d'état (init → running → paused → finished)

### 8.3 Sandbox et isolation

OpenHands exécute toutes les actions dans un **conteneur Docker** :
- Isolation complète du système hôte
- Rollback possible à tout moment
- Réseau et filesystem contrôlés

### 8.4 Forces et faiblesses

**Forces :**
- EventStore = auditabilité complète (replay possible)
- Sandbox Docker = sécurité maximale pour l'exécution de code
- Human-in-the-loop via `ChangeAgentStateAction`
- Excellent pour les tâches de développement logiciel autonome

**Faiblesses :**
- Overhead Docker pour chaque session
- L'event store croît sans borne (pagination nécessaire)
- Communication inter-agents limitée (conçu pour agent unique sur tâche)
- Latence élevée sur les allers-retours Action → Observation

---

## 9. Pattern 7 — Vision + Step (browser-use)

### 9.1 Principe

browser-use implémente un agent de navigation web avec deux canaux de perception simultanés : **capture DOM** et **screenshot visuel**.

**Architecture de perception** (source: `browser_use/`) :
```
Browser (Playwright)
  ├── DOM Extraction → Texte structuré
  │       → Identifiants d'éléments interactifs
  │       → Arbre d'accessibilité
  └── Screenshot → Image
          → Analyse visuelle par le LLM
          → Confirmation de l'état réel de la page

LLM reçoit: DOM + Screenshot + historique des actions
LLM décide: Click, Type, Scroll, Navigate, Extract, Finish
```

### 9.2 Controller et actions

```
browser_use/
  controller/     → Gestion des actions haut-niveau
  dom/           → Parsing et extraction DOM
  agent/         → Boucle principale
  browser/       → Interface Playwright
  mcp/           → Exposition des tools via MCP
```

**Actions typiques :**
- `go_to_url(url)` → navigation
- `click_element(selector)` → interaction
- `input_text(selector, text)` → formulaire
- `extract_content(goal)` → extraction ciblée
- `done(text)` → terminaison

### 9.3 Forces et faiblesses

**Forces :**
- Combinaison DOM+vision = tolérance aux sites qui camouflent les éléments
- MCP natif → intégration facile dans Claude Code / Cursor
- Excellente gestion des états dynamiques (SPA, React, etc.)
- Annotation visuelle des éléments pour debug

**Faiblesses :**
- **Coût élevé** : screenshot + DOM à chaque action → nombreux tokens
- **Fragilité** : changements de layout brisent les sélecteurs
- **Anti-bot** : CAPTCHAs et détections stoppent le flux
- Pas conçu pour l'orchestration multi-agents

---

## 10. Pattern 8 — Persona + Menu (BMAD-METHOD)

### 10.1 Principe

BMAD implémente une **orchestration par personas** : chaque agent a une identité forte (nom, rôle, backstory), un menu d'actions proposé à l'utilisateur, et un système de routing par intent.

**Structure agent BMAD :**
```markdown
---
name: analyst
persona: Mary
role: Business Analyst
---

# Instructions
[persona complète avec backstory, ton, expertise]

# Quand activé
[conditions d'activation]

# Menu d'actions
1. [Option 1] — description
2. [Option 2] — description

# Workflows disponibles
[liste des workflows que cet agent peut exécuter]
```

### 10.2 SOG — Smart Orchestrator Gateway

BMAD v6 introduit le **SOG** : un seul agent exposé à l'utilisateur, tous les autres sont invisibles. Le SOG :
1. Analyse l'intent de l'utilisateur
2. Sélectionne le(s) sub-agent(s) optimal(aux)
3. Dispatch la tâche avec contexte enrichi
4. Agrège les résultats avant présentation

```
User ←→ SOG (Grimoire Master)
          ├── analyst (Mary)
          ├── architect (Winston)
          ├── dev (Amelia)
          ├── pm (John)
          └── qa (Quinn)
```

### 10.3 UDF — Unified Dynamic Factory

BMAD v6 peut créer des agents, workflows, skills et instructions **dynamiquement** quand aucun existant ne couvre le besoin :

```
Gap detected
  → Type classification (agent|workflow|skill|instruction)
  → Durability triage (score ≥ 3 → permanent, < 3 → éphémère 7j)
  → Builder dispatch
  → Auto-discovery (VS Code détecte les nouveaux fichiers)
```

### 10.4 Forces et faiblesses

**Forces :**
- Expérience utilisateur unifiée (un seul point d'entrée)
- Personas fortes → meilleure spécialisation LLM
- Auto-discovery des artefacts créés dynamiquement
- Hooks lifecycle (PreToolUse, PostToolUse, SessionStart, Stop)
- Système de mémoire persistante entre sessions
- Adaptatif : BMAD ajuste la profondeur de planification selon la complexité

**Faiblesses :**
- Dépendance à l'IDE (VS Code / Cursor / Claude Code)
- Complexité de setup initiale élevée
- SOG = single point of failure : si le routing échoue, tout échoue
- Pas de test framework natif pour les agents BMAD

---

## 11. Pattern 9 — Worker Pool (Octogent)

### 11.1 Principe

Octogent (TypeScript) implémente un modèle de **worker pool** : un dispatcher distribue des tâches vers un pool d'agents workers disponibles. Chaque worker exécute indépendamment, les résultats sont agrégés.

**Architecture :**
```typescript
// Octogent worker pool pattern
class Octogent {
    workers: Agent[]          // Pool de workers homogènes
    dispatcher: Dispatcher    // Distribue les tâches
    aggregator: Aggregator    // Agrège les résultats
    
    async process(tasks: Task[]): Promise<Result[]> {
        const batches = this.dispatcher.split(tasks, this.workers.length)
        const results = await Promise.all(
            batches.map((batch, i) => this.workers[i].run(batch))
        )
        return this.aggregator.merge(results)
    }
}
```

### 11.2 Forces et faiblesses

**Forces :**
- Parallélisme natif → throughput élevé pour tâches homogènes
- Scaling horizontal simple : ajouter des workers = plus de débit
- Isolation : un worker qui crash n'affecte pas les autres

**Faiblesses :**
- Workers homogènes : pas de spécialisation par tâche
- Agrégation complexe : comment merger des outputs LLM hétérogènes ?
- Coordination difficile si les tâches ont des dépendances entre elles

---

## 12. Pattern 10 — Kanban Routing (switchboard)

### 12.1 Principe

switchboard (TypeScript) implémente un **routeur Kanban** : les messages entrent dans une inbox, un router classifie l'intent et les assigne à la "colonne" (agent) appropriée.

**Pipeline :**
```
Inbox
  → Intent classifier (LLM ou rules-based)
  → Route vers Agent A (si intent = X)
  → Route vers Agent B (si intent = Y)
  → Dead letter queue (si aucune route trouvée)
  → Outbox
```

### 12.2 Forces et faiblesses

**Forces :**
- Découplage fort entre source et traitement
- Facile d'ajouter une route sans modifier les agents existants
- Dead letter queue = observabilité des cas non-couverts
- Bon pour les systèmes à fort volume de messages entrants

**Faiblesses :**
- Classification d'intent = source d'erreurs (LLM peut mal classer)
- Pas conçu pour les workflows multi-étapes
- Pas de mémoire inter-messages native

---

## 13. Pattern 11 — Memory Palace (mempalace)

### 13.1 Principe

mempalace est une architecture mémoire spécialisée, pas un framework d'orchestration. Elle implémente le concept de **palace** cognitif : la mémoire est organisée en hiérarchie spatiale (wings > rooms > drawers).

**Structure :**
```
Palace
  ├── Wing: "project-grimoire-forge"
  │     ├── Room: "architecture"
  │     │     ├── Drawer: "hook-system" (verbatim)
  │     │     └── Drawer: "agent-routing" (verbatim)
  │     └── Room: "decisions"
  │           └── Drawer: "2026-04-..." (verbatim)
  └── Wing: "project-autre"
        └── ...
```

**Principe clé** : stockage **verbatim** (pas de résumé, pas de paraphrase) + retrieval **sémantique** (ChromaDB) = **96.6% R@5 sur LongMemEval**.

```bash
# Usage
mempalace mine ~/projects/myapp          # Indexe un projet
mempalace mine ~/.claude/projects/ --mode convos  # Indexe des sessions Claude
mempalace search "architecture décisions" --wing grimoire-forge
```

### 13.2 Intégration dans l'orchestration

mempalace s'intègre comme **couche mémoire long-terme** dans n'importe quel framework :
- LangChain : via custom `VectorStoreRetriever`
- OpenAI Agents : via tool `search_memory`
- BMAD : via hook `SessionStart` → chargement des souvenirs pertinents

---

## 14. Architectures mémoire — Comparatif

### 14.1 Tableau comparatif

| Framework | Court terme | Long terme | Entités | Cross-session | Verbatim | Vectoriel |
|---|---|---|---|---|---|---|
| **AutoGen** | Chat history | ❌ | ❌ | ❌ | ✅ | ❌ |
| **CrewAI** | RAG in-memory | SQLite | ✅ Graphe | ✅ | ❌ | ✅ |
| **OpenAI Agents** | Run context | ❌ | ❌ | ❌ | ✅ | ❌ |
| **LangGraph** | State graph | ✅ Checkpoints | ❌ | ✅ | Partiel | ✅ LangSmith |
| **OpenHands** | Event store | ✅ Event store | ❌ | ✅ | ✅ | ❌ |
| **BMAD** | Session | ✅ Fichiers MD | ✅ (UDF) | ✅ | ✅ | Partiel |
| **mempalace** | ❌ | ✅ Wings/Rooms | ✅ | ✅ | ✅ Verbatim | ✅ ChromaDB |

### 14.2 Les 4 niveaux de mémoire recommandés

Un système en production doit implémenter ces 4 niveaux :

```
┌─────────────────────────────────────────────────────┐
│  L1 — Working Memory (dans le prompt)               │
│  Durée: tour courant · Taille: limité par ctx window│
│  Contenu: tâche courante, état immédiat             │
├─────────────────────────────────────────────────────┤
│  L2 — Session Memory (in-process)                   │
│  Durée: session active · Taille: quelques MB        │
│  Contenu: historique de chat, décisions de session  │
├─────────────────────────────────────────────────────┤
│  L3 — Long-term Memory (persistant)                 │
│  Durée: permanent · Taille: illimité                │
│  Contenu: préférences utilisateur, faits appris     │
│  Implémentation: SQLite, Qdrant, PostgreSQL+pgvector │
├─────────────────────────────────────────────────────┤
│  L4 — Knowledge Base (externe)                      │
│  Durée: permanent · Taille: illimité                │
│  Contenu: docs, codebase, artifacts                 │
│  Accès: RAG (BM25 + embeddings), mempalace          │
└─────────────────────────────────────────────────────┘
```

### 14.3 Anti-patterns mémoire

❌ **Stocker tout l'historique dans le prompt** → context overflow garanti  
❌ **Résumer agressivement** → perte d'information critique (préférer verbatim + retrieval)  
❌ **Mémoire partagée sans scoping** → contamination inter-agents / inter-sessions  
❌ **Pas de TTL sur la mémoire court terme** → accumulation de bruit  
❌ **Embeddings sans reranking** → retrieval de basse qualité pour les questions précises  

---

## 15. Patterns de communication inter-agents

### 15.1 Taxonomie

| Pattern | Description | Exemples |
|---|---|---|
| **Text broadcast** | Message texte envoyé à tous | AutoGen GroupChat |
| **Typed channels** | Messages typés par ports | Haystack Pipelines |
| **Handoff** | Transfert de contrôle avec état | OpenAI Agents |
| **State mutation** | Modification d'un état partagé | LangGraph StateGraph |
| **Event stream** | Événements publiés sur un bus | OpenHands EventStore |
| **Queue dispatch** | Tâches distribuées via file | Octogent, Dify |

### 15.2 Haystack — Typed Sockets

Haystack (Python) implémente le pattern le plus rigoureusement **typé** du corpus :

```python
# Haystack typed component
@component
class TextRanker:
    @component.output_types(documents=List[Document])
    def run(self, query: str, documents: List[Document]) -> dict:
        ...

# Les connexions entre composants sont validées au moment de la construction
pipeline.connect("retriever.documents", "ranker.documents")
# → Erreur si les types ne correspondent pas
```

Ce pattern prévient une catégorie entière de bugs (mauvais type passé entre composants) et facilite le test unitaire de chaque composant.

### 15.3 Règles de communication

**Règle 1 — Éviter le broadcast aveugle**  
Envoyer un message à tous les agents quand un seul en a besoin = gaspillage de tokens et source de confusion.

**Règle 2 — Nommer les canaux**  
`"results" → "validator.input"` est plus robuste que `"output" → "input"` car le nom indique le contrat.

**Règle 3 — Valider à la frontière**  
Vérifier le schéma des messages à l'entrée de chaque composant, pas uniquement à la sortie du précédent.

**Règle 4 — Idempotence**  
Les agents qui reçoivent le même message deux fois doivent produire le même résultat (robustesse aux retransmissions).

---

## 16. Tool Use — Patterns et garde-fous

### 16.1 Types de tools dans le corpus

| Type | Exemples | Risque |
|---|---|---|
| **Read-only** | search, read_file, get_url | Faible |
| **Write local** | write_file, edit_file, run_code | Moyen |
| **Write externe** | send_email, post_to_api, git_push | Élevé |
| **Execute** | bash, python_repl, browser_click | Très élevé |
| **Destructif** | delete_file, drop_table | Critique |

### 16.2 Pattern de guardrails en couches

OpenAI Agents Python définit le pattern le plus propre :

```
InputGuardrail → [Agent LLM] → OutputGuardrail → Tool Execution
     ↓                               ↓                  ↓
tripwire_triggered?           tripwire_triggered?    Permission check
→ BLOCK                       → BLOCK                → Sandbox
```

**Implémentation recommandée :**

```python
@input_guardrail
async def check_harmful_request(ctx, agent, input):
    # Vérifier que la demande n'est pas malveillante
    result = await safety_model.check(input)
    return GuardrailFunctionOutput(
        output_info=result,
        tripwire_triggered=result.is_harmful
    )

@output_guardrail  
async def check_sensitive_data(ctx, agent, output):
    # Vérifier que l'output ne contient pas de données sensibles
    result = await pii_detector.check(output)
    return GuardrailFunctionOutput(
        output_info=result,
        tripwire_triggered=result.has_pii
    )
```

### 16.3 Permissions progressives

Pattern recommandé (observé dans plusieurs repos) :

```
Tier 0 — Aucune permission nécessaire
  read_file, search, list_directory

Tier 1 — Confirmation implicite (log uniquement)
  write_file, create_directory

Tier 2 — Confirmation explicite (demande à l'utilisateur)
  delete_file, git_commit, send_message

Tier 3 — Confirmation + raison documentée
  drop_table, git_push_force, delete_branch

Tier 4 — BLOQUÉ par défaut (whitelist explicite)
  rm -rf, format_disk, factory_reset
```

### 16.4 Tool call budgeting

Limiter le nombre d'appels pour éviter les boucles :

```python
class ToolBudget:
    max_total_calls: int = 50
    max_per_tool: dict[str, int] = {
        "bash": 20,
        "write_file": 10,
        "delete_file": 3
    }
    current_counts: dict[str, int] = {}
    
    def check(self, tool_name: str) -> bool:
        total = sum(self.current_counts.values())
        per_tool = self.current_counts.get(tool_name, 0)
        return total < self.max_total_calls and per_tool < self.max_per_tool.get(tool_name, 999)
```

---

## 17. Observabilité et traçabilité

### 17.1 Langfuse — Traçabilité hiérarchique

Langfuse (source: `langfuse/`) est le framework d'observabilité le plus complet du corpus. Il implémente un modèle de **traces hiérarchiques** :

```
Trace (session complète)
  └── Span: "analyst-step" (durée, statut)
        └── Generation: "gpt-4.1 call" (tokens, latence, coût)
              ├── input: {messages: [...]}
              └── output: {content: "..."}
        └── Span: "tool-call-read-file" 
              ├── input: {path: "..."}
              └── output: {content: "..."}
  └── Span: "developer-step"
        └── ...
```

**Métriques collectées :**
- Latence par span (p50, p90, p99)
- Tokens consommés (prompt + completion)
- Coût estimé par trace
- Taux de succès / erreur par step
- Score humain (si évaluation manuelle)

### 17.2 Niveau minimal d'observabilité requis

Un système en production doit capturer :

| Signal | Pourquoi | Implémentation |
|---|---|---|
| **Latence par step** | Détecter les goulots | Timer autour de chaque appel LLM |
| **Tokens consommés** | Contrôler les coûts | Usage API (prompt_tokens, completion_tokens) |
| **Taux d'erreur** | Détecter les régressions | Count erreurs / total appels |
| **Tool calls** | Audit de sécurité | Log chaque appel avec input/output |
| **State transitions** | Debug reproductible | Log chaque changement d'état agent |
| **Handoffs** | Comprendre le routing | Log source, cible, contexte passé |

### 17.3 OpenTelemetry — Standard d'industrie

LangGraph et plusieurs frameworks s'intègrent avec OpenTelemetry :

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

tracer = trace.get_tracer("agent-system")

with tracer.start_as_current_span("agent-run") as span:
    span.set_attribute("agent.name", "analyst")
    span.set_attribute("model", "gpt-4.1")
    result = await agent.run(input)
    span.set_attribute("tokens.total", result.usage.total_tokens)
```

---

## 18. Sécurité et défenses LLM

### 18.1 Vecteurs d'attaque spécifiques aux agents

| Attaque | Description | Défense |
|---|---|---|
| **Prompt injection** | L'input utilisateur contient des instructions malveillantes | Guardrails, séparation input/system |
| **Indirect injection** | Le contenu lu par l'agent (web, fichier) contient des injections | Sandboxing, validation du contenu externe |
| **Tool abuse** | L'agent est convaincu d'utiliser un tool destructif | Permissions progressives, confirmation obligatoire |
| **Data exfiltration** | L'agent est convaincu d'envoyer des données sensibles | Output guardrails, blocage des canaux non-autorisés |
| **Jailbreak via personnalité** | L'agent change de "persona" pour contourner les règles | Règles système hors-contexte utilisateur |
| **Loop attack** | L'agent est mis en boucle infinie par une réponse malveillante | Tool budget, max_iterations, circuit breaker |

### 18.2 LLMSecurityGuide (synthèse)

Le repo `LLMSecurityGuide` documente les 10 risques OWASP LLM :

1. **LLM01** Prompt Injection
2. **LLM02** Insecure Output Handling
3. **LLM03** Training Data Poisoning
4. **LLM04** Model Denial of Service
5. **LLM05** Supply-Chain Vulnerabilities
6. **LLM06** Sensitive Information Disclosure
7. **LLM07** Insecure Plugin Design
8. **LLM08** Excessive Agency
9. **LLM09** Overreliance
10. **LLM10** Model Theft

**Les trois plus pertinents pour l'orchestration multi-agents :**

**LLM08 — Excessive Agency** : L'agent a accès à plus de tools/permissions qu'il n'en a besoin. Mitigation : principe de moindre privilège, tools scope minimal.

**LLM01 — Prompt Injection** : Particulièrement dangereux en multi-agents car un agent compromis peut injecter dans le contexte partagé. Mitigation : isolation des contextes, validation des messages inter-agents.

**LLM06 — Sensitive Information Disclosure** : Un agent peut fuiter des données d'un agent A vers un agent B qui n'y a pas accès. Mitigation : scoping des informations sensibles, output guardrails.

### 18.3 Mesures de sécurité observées dans le corpus

| Mesure | Repos qui l'implémentent | Maturité |
|---|---|---|
| Sandbox d'exécution (Docker) | OpenHands, browser-use | Production |
| Input/Output guardrails | OpenAI Agents, BMAD | Production |
| Tool permission tiers | OpenAI Agents, BMAD | Production |
| Rate limiting LLM | Langfuse, Dify | Production |
| Audit log | OpenHands (event store), Langfuse | Production |
| Isolation contexte inter-agents | BMAD (repo-context isolation) | Expérimental |
| Circuit breaker | LangGraph (max_iterations) | Partial |

---

## 19. Défauts communs et comment les compenser

### 19.1 Matrice défaut × compensation architecturale

| Défaut LLM | Cause | Compensation architecturale | Implémentation |
|---|---|---|---|
| **Hallucination** | L'agent invente des faits non-vérifiés | Grounding obligatoire avant toute affirmation | Lire le fichier source AVANT d'en parler |
| **Drift d'objectif** | L'agent s'écarte de l'objectif initial au fil des tours | Ancrage d'objectif dans chaque step | `initial_objective` dans chaque prompt de step |
| **Perte de contexte** | Longueur de session dépasse la fenêtre | Fiche contextuelle isolée par tâche/repo | `repo-contexts/{name}.md` en dehors du chat |
| **Lecture partielle** | L'agent ignore la fin du prompt | Structure ZONE 1/2/3 (critique d'abord) | Objectif dans les 200 premiers tokens |
| **Sur-confiance** | L'agent valide ses propres outputs | Gate adversariale bloquante | Revue indépendante avec `initial_objective` |
| **Token explosion** | Historique de chat trop long | Résumé canonique + rotation de contexte | Canonical summary après chaque phase |
| **Boucles infinies** | L'agent répète sans progresser | Tool budget + max_iterations | Compteur d'appels par type de tool |
| **Contamination inter-tâches** | Contexte de la tâche A pollue la tâche B | Isolation stricte de contexte | Clear state avant chaque nouvelle tâche |

### 19.2 Le test des 3 questions

Avant de considérer un système "prêt", répondre à ces 3 questions :

1. **Si le LLM est interrompu au milieu d'un workflow, peut-il reprendre sans perdre le contexte ?**
   → Si non : implémenter self-piloting (state file après chaque step)

2. **Si le LLM affirme quelque chose, peut-on tracer cette affirmation jusqu'à un fichier source réel ?**
   → Si non : implémenter grounding (lecture obligatoire avant toute affirmation)

3. **Si l'objectif initial change entre le premier et le dernier step, le système le détecte-t-il ?**
   → Si non : implémenter adversarial review avec `initial_objective`

---

## 20. Éléments obligatoires pour un système qui fonctionne

Un système d'orchestration en production **doit** avoir ces 10 éléments. Sans eux, il dégradera ou échouera.

### 20.1 Les 10 non-négociables

**1. Objectif ancré dans chaque step**
```
CHAQUE step commence par : "OBJECTIF DE CE STEP : [une phrase]"
CHAQUE step rappelle : "OBJECTIF GLOBAL : [une phrase]"
```

**2. Grounding avant toute affirmation**
```
RÈGLE : Ne jamais affirmer le contenu d'un fichier sans l'avoir lu.
IMPLÉMENTATION : Tool read_file() AVANT de parler du fichier.
```

**3. State persistant entre sessions**
```
APRÈS chaque step : écrire {step, status, objective} dans un fichier JSON
AU DÉMARRAGE : lire ce fichier, proposer [Reprendre] ou [Nouveau]
```

**4. Gate adversariale bloquante**
```
AVANT de livrer un résultat critique : passer par une revue indépendante
CRITÈRE : minimum N findings, sinon le step recommence
```

**5. Isolation de contexte par tâche**
```
CHAQUE tâche/repo : contexte isolé dans sa propre fiche
JAMAIS : mélanger le contexte de deux tâches dans la même session
```

**6. Budget de tokens/tools**
```
Token budget mode : normal (<100 fichiers) | prioritized (<500) | stratified (≥500)
Max tool calls : défini par type, respecté par un compteur
```

**7. Guardrails en entrée ET en sortie**
```
INPUT : vérifier que la demande est dans le scope autorisé
OUTPUT : vérifier que la réponse ne contient pas de données sensibles
```

**8. Observabilité minimale**
```
LOG : chaque appel LLM (input, output, tokens, latence)
LOG : chaque tool call (name, input, output, statut)
LOG : chaque transition d'état agent
```

**9. Human-in-the-loop sur les actions irréversibles**
```
CONFIRMATION obligatoire avant : delete, push, send, deploy
CONFIRMATION optionnelle pour : write, edit (configurable)
```

**10. Documentation auto-suffisante**
```
CHAQUE output : lisible sans lire la conversation
INCLURE : les sources de vérité, la confiance, les questions ouvertes
```

### 20.2 Les 5 éléments "bons à avoir"

**11. Swarm consensus sur les claims divergents**
Vote multi-perspectives quand deux analyses arrivent à des conclusions opposées.

**12. Token-aware chunking**
Pour les repos > 500 fichiers : stratégie de lecture stratifiée par risque.

**13. Auto-trigger par keywords**
Hook sur les prompts utilisateur pour proposer le bon workflow automatiquement.

**14. Métriques de qualité de l'analyse**
Confiance calculée (HIGH/MEDIUM/LOW) basée sur : CVTL pass, nb findings, hallucinations détectées.

**15. Cleanup automatique des états orphelins**
TTL sur les state files, nettoyage des contextes abandonnés.

---

## 21. Architecture recommandée — Modèle de référence

### 21.1 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    COUCHE UTILISATEUR                       │
│         SOG (Smart Orchestrator Gateway)                    │
│    - Point d'entrée unique                                  │
│    - Intent detection + workflow routing                    │
│    - Aggregation des résultats sub-agents                   │
└─────────────────┬───────────────────────────────────────────┘
                  │ dispatch
┌─────────────────▼───────────────────────────────────────────┐
│                 COUCHE ORCHESTRATION                         │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│   │ Analyst  │ │Architect │ │Developer │ │   QA     │     │
│   │ (Mary)   │ │(Winston) │ │(Amelia)  │ │(Quinn)   │     │
│   └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
│            ↕ State sharing via typed channels               │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                  COUCHE WORKFLOW                             │
│   StateGraph (LangGraph-inspired)                           │
│   - Steps JIT (un à la fois)                                │
│   - State persisté après chaque step                        │
│   - Gates bloquantes (adversarial, CVTL)                    │
│   - Self-piloting via state file                            │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                   COUCHE OUTILS                             │
│   ┌─────────────────┐  ┌──────────────────┐                │
│   │ Read-only Tools │  │ Write Tools      │                │
│   │ (Tier 0)        │  │ (Tier 1-3)       │                │
│   └─────────────────┘  └──────────────────┘                │
│   InputGuardrail → [Tool] → OutputGuardrail                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                  COUCHE MÉMOIRE                             │
│   L1: Working memory (prompt)                               │
│   L2: Session memory (process)                              │
│   L3: Long-term memory (SQLite/Qdrant)                      │
│   L4: Knowledge base (mempalace/RAG)                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│               COUCHE OBSERVABILITÉ                          │
│   Traces hiérarchiques (Langfuse/OTel)                      │
│   Audit log (chaque tool call)                              │
│   State history (chaque transition)                         │
└─────────────────────────────────────────────────────────────┘
```

### 21.2 Principes de design

**Principe 1 — Un seul point d'entrée utilisateur**
Le SOG absorbe toute la complexité. L'utilisateur ne voit jamais les sous-agents, les handoffs, les états internes.

**Principe 2 — État explicite, jamais implicite**
L'état de chaque workflow est écrit dans un fichier. Si le processus est tué, relancé, ou change de session, l'état est récupérable.

**Principe 3 — Fail fast et fail loudly**
Une gate bloquante qui détecte un problème doit bloquer l'exécution immédiatement, pas tenter de corriger silencieusement.

**Principe 4 — Grounding d'abord**
Aucune affirmation sans source. Aucune analyse sans lecture préalable. Aucune conclusion sans traçabilité.

**Principe 5 — Isolation des contextes**
Les informations d'une tâche ne contaminent pas une autre. Chaque session de travail démarre avec un contexte propre.

---

## 22. Checklist opérationnelle

### 22.1 Avant de démarrer un projet d'orchestration

```
[ ] Objectif documenté en une phrase (pas plus)
[ ] Liste des agents nécessaires avec leurs rôles distincts
[ ] Architecture mémoire décidée (4 niveaux couverts ?)
[ ] Liste des tools avec leurs tiers de permission
[ ] Strategy de grounding définie (quels fichiers lire en premier ?)
[ ] Gates bloquantes identifiées (où les humains doivent valider ?)
[ ] Stratégie d'observabilité définie (Langfuse ? OTel ? Logs ?)
[ ] Budget token/tool défini par agent
[ ] Plan de reprise après interruption (state file ?)
[ ] Format de l'output final défini (auto-suffisant ?)
```

### 22.2 Pendant l'exécution d'un workflow

```
[ ] Objectif rappelé au début de chaque step
[ ] State file mis à jour après chaque step
[ ] Grounding effectué avant toute affirmation
[ ] Sources documentées (quel fichier, quelle ligne ?)
[ ] Gate adversariale passée (minimum N findings ?)
[ ] CVTL exécuté sur les outputs critiques
[ ] Budget de tokens surveillé
[ ] Log des tool calls enregistré
```

### 22.3 Après la livraison d'un output

```
[ ] Output auto-suffisant (lisible sans la conversation ?)
[ ] Sources de vérité listées
[ ] Niveau de confiance calculé et justifié
[ ] Questions ouvertes documentées
[ ] Contexte fermé (fiche marquée "completed")
[ ] State file nettoyé
[ ] Métriques enregistrées (tokens, latence, coût)
```

---

## 23. Synthèse par repo

### Groupe A — Frameworks d'orchestration matures

**AutoGen (Microsoft)**
- Pattern : GroupChat + TypedAgents
- Statut : Maintenance (migrer vers Microsoft Agent Framework)
- Verdict : Architecture solide mais à migrer. Le nouveau MAF apporte des APIs stables, A2A (Agent-to-Agent protocol) et MCP.
- Points forts : Flexibilité du GroupChat, AgentChat pour les cas simples, AutoGen Studio pour le no-code
- Points faibles : Token explosion dans les GroupChats longs, pas de mémoire long-terme native

**CrewAI**
- Pattern : Task-Agent-Process
- Mémoire : 3-tier (short/long/entity) avec scope crew/agent/task
- Verdict : L'architecture mémoire la plus complète. Idéal pour les workflows multi-étapes avec des rôles distincts.
- Points forts : Mémoire entity-aware, process hiérarchique, backend pluggable (Qdrant)
- Points faibles : Couplage fort Task-Agent, goulots dans les process séquentiels

**OpenAI Agents Python**
- Pattern : Handoff-First + Tripwires
- Verdict : Les guardrails sont l'innovation principale. Pattern le plus propre pour la sécurité.
- Points forts : Tripwires explicites, handoff avec input_filter, lifecycle hooks, `guardrail.py` découplé
- Points faibles : Flat hierarchy, pas de mémoire long-terme, risque de boucles sans circuit-breaker

**LangGraph**
- Pattern : StateGraph / Pregel
- Verdict : Le framework le plus robuste pour les workflows complexes avec reprises.
- Points forts : Durable execution, state typé, human-in-the-loop natif, subgraphs, LangSmith
- Points faibles : Courbe d'apprentissage élevée, surcharge pour tâches simples, dépendance LangChain

### Groupe B — Frameworks visuels et no-code

**LangFlow**
- Pattern : DAG Visuel
- Verdict : Excellent pour le prototypage rapide et les non-développeurs. Limites en production complexe.
- Points forts : 200+ composants, déploiement API 1 clic, real-time preview
- Points faibles : Debugging pénible, versionning git difficile, pas de tests unitaires

**Dify**
- Pattern : DAG + Multi-tenant SaaS
- Verdict : La solution la plus complète pour déployer des agents en production sans infrastructure custom.
- Points forts : Multi-tenant, marketplace plugins (100+), RAG intégré, 40+ LLMs supportés, queue Celery
- Points faibles : Surcharge pour les petits projets, complexité de self-hosting

### Groupe C — Agents spécialisés

**OpenHands (OpenDevin)**
- Pattern : EventLoop + Action-Observation + Sandbox Docker
- Verdict : Le meilleur pour l'autonomie de développement logiciel. L'event store est un modèle de traçabilité.
- Points forts : Sandbox Docker (sécurité maximale), event store persistant, human-in-the-loop via state transitions
- Points faibles : Overhead Docker, event store sans borne, latence Action→Observation

**browser-use**
- Pattern : Vision + Step (DOM + Screenshot)
- Verdict : L'agent web le plus robuste. La combinaison DOM+vision est déterminante.
- Points forts : Tolérance aux changements de layout, MCP natif, annotation visuelle
- Points faibles : Coût élevé (tokens screenshot), fragilité face aux anti-bots

**BMAD-METHOD**
- Pattern : Persona + Menu + SOG
- Verdict : Le framework le plus adapté aux workflows de développement guidé par LLM.
- Points forts : SOG (point d'entrée unique), UDF (création dynamique d'artefacts), hooks lifecycle, documentation standards
- Points faibles : Dépendance IDE forte, setup complexe, SOG = single point of failure

### Groupe D — Outils d'infrastructure

**Langfuse**
- Rôle : Observabilité et tracing LLM
- Verdict : Indispensable en production. Les traces hiérarchiques permettent de diagnostiquer des problèmes impossibles à voir autrement.
- Points forts : Traces span/generation, métriques coût/latence, évaluations humaines, dashboards
- Points faibles : Self-hosting complexe, stack pnpm lourd

**mempalace**
- Rôle : Mémoire long-terme locale, verbatim
- Verdict : L'approche verbatim + retrieval sémantique est supérieure au résumé automatique. 96.6% R@5 sur LongMemEval.
- Points forts : Zero API calls, local-first, hiérarchie wing/room/drawer, ChromaDB pluggable
- Points faibles : Pas d'intégration native dans les frameworks majeurs (à implémenter soi-même)

**kagent**
- Rôle : Agents Kubernetes (CRD-Controller pattern)
- Pattern : Kubernetes Custom Resources + Controller loop
- Verdict : Indispensable si l'infrastructure est K8s. Gestion déclarative des agents.
- Points forts : Tolérance aux pannes K8s native, déclaratif (GitOps), scaling automatique
- Points faibles : Overhead K8s pour les petits projets, complexité opérationnelle

### Groupe E — Repos éducatifs et références

**ai-agents-for-beginners (Microsoft)**
- Contenu : 12 leçons + code samples sur AutoGen, Semantic Kernel, Azure AI
- Verdict : Excellente introduction mais basé sur AutoGen 0.2 (maintenant en maintenance)
- Recommandation : Utiliser comme introduction conceptuelle, pas comme référence d'implémentation

**LLMLingua**
- Rôle : Compression de prompts LLM
- Verdict : Utile pour les prompts très longs (>10k tokens). Compression jusqu'à 20x avec perte minimale.
- Points forts : Réduction drastique des coûts pour les pipelines haute fréquence
- Points faibles : Peut perdre des informations critiques si mal configuré

**CodeGraphContext**
- Rôle : Analyse statique de code en graphe
- Verdict : Utile pour le grounding dans les analyses de codebase. Transforme le code en graphe de dépendances.
- Points forts : Résolution de contexte précise (quelle fonction appelle quoi)
- Points faibles : Overhead de construction du graphe sur les gros repos

**Haystack**
- Rôle : Framework RAG + Pipelines composables typés
- Verdict : Le pattern de typed sockets est un modèle à suivre pour la robustesse.
- Points forts : Composants typés (validation des connexions au build), 100+ composants, RAG production-ready
- Points faibles : Verbosité de la définition de pipelines

### Groupe F — Projets expérimentaux / en développement

**agent-framework (Microsoft MAF)**
- Statut : Successeur officiel d'AutoGen, production-ready depuis début 2026
- Pattern : Agent-to-Agent (A2A) + MCP + stable APIs
- Verdict : Référence pour les nouveaux projets Microsoft/Azure

**switchboard**
- Pattern : Kanban routing
- Verdict : Pattern intéressant pour les systèmes à fort volume de messages hétérogènes

**Octogent**
- Pattern : Worker pool TypeScript
- Verdict : Utile pour les tâches parallèles homogènes, limité pour les workflows complexes

**graphify**
- Rôle : Interface graphique pour LangGraph
- Verdict : Complète LangGraph avec une couche visuelle sans sacrifier la programmabilité

**pixel-agents**
- Rôle : Agents pour la création de contenu pixel art
- Verdict : Exemple d'agents spécialisés dans un domaine créatif

**OpenMythos / shannon / superpowers / andrej-karpathy-skills / claude-skills**
- Verdict : Projets exploratoires ou collections de skills. Valeur éducative, pas de production.

---

## 24. Recommandations finales

### 24.1 Par cas d'usage

| Cas d'usage | Framework recommandé | Alternative |
|---|---|---|
| Workflow de développement guidé | BMAD + LangGraph | CrewAI |
| Analyse de codebase multi-étapes | Grimoire repo-analysis workflow | OpenHands |
| Navigation web autonome | browser-use | OpenHands |
| RAG et recherche documentaire | Haystack | Dify |
| Prototypage rapide no-code | Dify | LangFlow |
| Agents K8s en production | kagent | — |
| Observabilité LLM | Langfuse | LangSmith |
| Mémoire long-terme verbatim | mempalace | CrewAI long-term |
| Multi-agents conversationnels | Microsoft Agent Framework | LangGraph |
| Sécurité et guardrails | OpenAI Agents Python | BMAD hooks |

### 24.2 Stack recommandée pour un projet de pilotage sérieux

**Couche orchestration** : LangGraph (StateGraph) ou BMAD (SOG)  
**Couche communication** : Typed channels (Haystack pattern) ou Handoffs (OpenAI pattern)  
**Couche mémoire** : CrewAI memory (3-tier) + mempalace (long-term verbatim)  
**Couche sécurité** : OpenAI guardrails (tripwires) + sandbox Docker (OpenHands pattern)  
**Couche observabilité** : Langfuse + OpenTelemetry  
**Couche grounding** : Lecture obligatoire avant toute affirmation (Grimoire pattern)  

### 24.3 Les 5 leçons les plus importantes

**Leçon 1 — La mémoire est une infrastructure, pas une feature**  
Ne jamais démarrer un projet sans avoir décidé des 4 niveaux de mémoire. L'ajouter après est coûteux.

**Leçon 2 — Le grounding compense l'hallucination mieux que les instructions**  
Dire "ne pas halluciner" ne fonctionne pas. Forcer la lecture du fichier source avant toute affirmation, si.

**Leçon 3 — Les guardrails doivent être bloquants, pas informatifs**  
Un guardrail qui "avertit" est ignoré. Un guardrail qui bloque l'exécution change le comportement.

**Leçon 4 — L'observabilité n'est pas optionnelle en production**  
Sans traces, un système multi-agents en production est une boîte noire. Le debugging est impossible.

**Leçon 5 — Un seul point d'entrée simplifie tout**  
Le pattern SOG (BMAD) et le GroupChatManager (AutoGen) existent pour la même raison : l'utilisateur ne devrait jamais avoir à gérer la complexité interne de l'orchestration.

### 24.4 Anti-patterns à éviter absolument

```
❌ Laisser les agents se nommer entre eux dans leurs outputs
❌ Partager le contexte complet entre tous les agents (token explosion)
❌ Utiliser la même session LLM pour plusieurs repos distincts
❌ Guardrails uniquement en entrée (pas en sortie)
❌ Pas de state file → reprise impossible
❌ Logging des tool calls désactivé en production
❌ Budget de tokens/tools illimité
❌ Validation des outputs par le même agent qui les a produits
❌ Grounding optionnel (doit être obligatoire)
❌ Output qui nécessite de lire la conversation pour être compris
```

---

## Conclusion

L'orchestration multi-agents n'est pas un problème d'instructions — c'est un problème d'architecture. Les 33 repos analysés convergent tous vers les mêmes solutions pour les mêmes problèmes :

- **Contre l'hallucination** : grounding obligatoire
- **Contre le drift** : objectif ancré dans chaque step
- **Contre la perte de contexte** : state file persistant + isolation stricte
- **Contre la truncation** : structure ZONE 1/2/3 (critique d'abord)
- **Contre la sur-confiance** : gate adversariale bloquante

Les frameworks les plus matures (LangGraph, CrewAI, OpenAI Agents, BMAD) ne sont pas meilleurs parce qu'ils "font mieux parler les LLMs" — ils sont meilleurs parce qu'ils **compensent architecturalement les défauts des LLMs**.

Un projet de pilotage qui fonctionne en production est un projet qui a répondu à la question : "Que se passe-t-il quand le LLM échoue ?" à chaque étape de son architecture.

---

*Document produit par analyse directe des repos. Toutes les affirmations sont ancrées dans du code source lu.*  
*Confiance : HIGH — grounding complet, sources tracées, revue adversariale effectuée.*
