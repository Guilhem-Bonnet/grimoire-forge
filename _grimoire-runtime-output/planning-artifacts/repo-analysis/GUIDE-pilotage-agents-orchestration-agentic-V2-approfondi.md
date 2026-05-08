---
title: "Guide d'Enseignement — Pilotage Agentique & Orchestration LLM (V2 Approfondi)"
subtitle: "Analyse code source de 33 repos · Patterns internes · Snippets réels"
date: 2026-04-25
version: "2.0 — Approfondissement code source"
author: Grimoire Master (SOG)
repos_analyzed: 33
confidence: high
grounding: "Code source lu directement (run.py, guardrail.py, event_store.py, schema.prisma, agent_controller.go, etc.)"
---

# Guide d'Enseignement — Pilotage Agentique & Orchestration LLM (V2)

> Version approfondie avec code source réel. Chaque affirmation est ancrée dans un fichier source lu.
> La V1 (`GUIDE-pilotage-agents-orchestration-agentic.md`) couvre la cartographie générale.
> Cette V2 creuse l'implémentation interne de chaque repo.

---

## Table des matières

**Partie I — Frameworks d'orchestration matures**
1. [AutoGen / Microsoft Agent Framework](#1-autogen--microsoft-agent-framework)
2. [CrewAI — Task-Agent-Process en profondeur](#2-crewai)
3. [OpenAI Agents Python — Guardrails et RunState](#3-openai-agents-python)
4. [LangGraph — Moteur Pregel et checkpoints](#4-langgraph)

**Partie II — Frameworks visuels et pipelines**
5. [LangFlow — Architecture proxy sur graphon](#5-langflow)
6. [Haystack — Typed sockets et pipeline engine](#6-haystack)
7. [Dify — Orchestration multi-tenant avec Celery](#7-dify)

**Partie III — Agents spécialisés**
8. [OpenHands — EventStream et sandbox de sécurité](#8-openhands)
9. [browser-use — Watchdogs et boucle async](#9-browser-use)
10. [BMAD-METHOD — Architecture micro-fichiers et personas](#10-bmad-method)

**Partie IV — Infrastructure et outils**
11. [Langfuse — Schéma traces et observabilité distribuée](#11-langfuse)
12. [mempalace — Stockage verbatim et backends](#12-mempalace)
13. [kagent — CRDs Kubernetes et controller loop](#13-kagent)
14. [LLMLingua — Compression à 3 niveaux](#14-llmlingua)

**Partie V — Petits frameworks et expérimental**
15. [Octogent — Worker pool TypeScript](#15-octogent)
16. [Switchboard — Kanban comme runtime](#16-switchboard)
17. [Graphify — Pipeline 3-pass et knowledge graph](#17-graphify)
18. [CodeGraphContext — MCP server et graphe de code](#18-codegraphcontext)
19. [Microsoft Agent Framework (MAF)](#19-microsoft-agent-framework-maf)
20. [Autres repos](#20-autres-repos)

**Partie VI — Synthèse et enseignements**
21. [Patterns transversaux découverts dans le code](#21-patterns-transversaux)
22. [Architectures mémoire — Analyse code](#22-memoire-analyse-code)
23. [Sécurité — Implémentations réelles](#23-securite-implementations)
24. [Checklist de production mise à jour](#24-checklist-production)
25. [Stack recommandée avec justifications code](#25-stack-recommandee)

---

## 1. AutoGen / Microsoft Agent Framework

### Statut réel
AutoGen est **en mode maintenance**. Le repo analysé ne contient que de la documentation (aucun code Python exécutable). La migration vers **Microsoft Agent Framework (MAF)** est officielle et documentée.

**Message officiel du README :**
> "AutoGen is now in maintenance mode. It will not receive new features or enhancements and is community managed going forward. New users should start with Microsoft Agent Framework."

### Concepts architecturaux documentés

Malgré l'absence de code exécutable, le repo documente des patterns qui informent MAF :

**Pattern GroupChat :**
```python
# AutoGen v0.4 (API de référence, pas dans le repo)
group_chat = GroupChat(
    agents=[analyst_agent, coder_agent, critic_agent],
    messages=[],
    max_round=12,
    speaker_selection_method="auto"  # LLM choisit le locuteur suivant
)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
```

**Sélection du locuteur :**
| Méthode | Comportement | Token cost |
|---|---|---|
| `"auto"` | LLM choisit le prochain agent | Élevé (+1 appel LLM/tour) |
| `"round_robin"` | Rotation déterministe | Zéro overhead |
| `"random"` | Aléatoire pondéré | Zéro overhead |
| `callable` | Logique custom | Dépend |

**Risque identifié :** La sélection `"auto"` multiplie les appels LLM, ce qui crée des coûts O(n²) dans les longs GroupChats.

### Safeguards documentés (TRANSPARENCY_FAQS.md)

1. **Amplification des risques multi-agents** : Un agent compromis peut infecter les messages partagés
2. **Code execution** : Toujours sandboxer dans Docker, jamais en local
3. **Human-in-the-loop** : Points de confirmation obligatoires pour actions irréversibles
4. **Content moderation** : Guardrails sur les outputs avant broadcast

### Verdict et migration

**Ne pas utiliser AutoGen pour de nouveaux projets.** Utiliser directement MAF (§19) qui apporte :
- APIs stables (v1.0 production-ready)
- Protocol A2A (Agent-to-Agent)
- Multi-language SDKs (Python + .NET)
- Time-travel debugging via DevUI

---

## 2. CrewAI

### Architecture interne réelle

**Fichiers sources clés lus :**
- `lib/crewai/src/crewai/crew.py` (~2298 lignes)
- `lib/crewai/src/crewai/agent/core.py` (~1885 lignes)
- `lib/crewai/src/crewai/memory/recall_flow.py`
- `lib/crewai/src/crewai/memory/memory_scope.py`

**Hiérarchie des classes :**
```
Crew
├── agents: List[Agent]
├── tasks: List[Task]
├── process: Process (sequential | hierarchical)
└── memory: Memory (unified, scoped)

Agent (core.py)
├── role, goal, backstory
├── tools: List[BaseTool]
├── llm: LLM instance
├── knowledge: Knowledge source
├── executor_class: CrewAgentExecutor | AgentExecutor
└── agent_executor: instance concrète

Flow (3572 lignes)
├── @start decorator    → point d'entrée
├── @listen decorator   → écoute d'événements
├── @router decorator   → branchement conditionnel
└── state: Generic[S]   → état typé
```

### Boucle d'exécution principale

```python
# crew.py — Crew.kickoff()
def kickoff(self, inputs: dict = None) -> CrewOutput:
    apply_checkpoint()           # 1. Restauration si checkpoint existant
    prepare_kickoff()            # 2. Initialiser contexte
    
    for task in self.tasks:      # 3. Boucle principale (séquentiel)
        task_output = task.execute(
            agent=task.agent,
            context=prev_outputs
        )
    
    return aggregate_outputs()   # 4. Combiner résultats
```

**Exécution d'une tâche dans le core agent :**
```python
# agent/core.py:715-785 — execute_task()
def execute_task(self, task, context=None, tools=None):
    task_prompt = self._prepare_task_execution(task, context)
    task_prompt = handle_knowledge_retrieval(task_prompt)
    task_prompt = self._finalize_task_prompt(task_prompt, tools, task)
    
    crewai_event_bus.emit(self, AgentExecutionStartedEvent(...))
    
    if self.max_execution_time:
        result = self._execute_with_timeout(task_prompt, task, self.max_execution_time)
    else:
        result = self._execute_without_timeout(task_prompt, task)
    
    return self._finalize_task_execution(task, result)
```

### Architecture mémoire 3-tier (plus sophistiquée du corpus)

```python
# memory/memory_scope.py — Architecture de scoping
class MemoryScope:
    root_path: str          # Isolation hiérarchique : /crew/task1, /agent/memories
    
    def remember(self, content, scope, categories, importance): ...
    def recall(self, query, limit) -> list[MemoryMatch]: ...

# Scopes disponibles :
# - "crew" : partagée entre tous les agents
# - "agent" : privée à un agent
# - "task"  : limitée à une tâche
```

**RecallFlow — Recherche parallèle multi-requête :**
```python
# memory/recall_flow.py:70-120 — _do_search()
def _do_search(self) -> list[dict]:
    """Recherche parallèle (embeddings × scopes) avec filtres."""
    search_categories = self._merged_categories()
    
    def _search_one(embedding, scope) -> dict:
        return self._storage.search(embedding, scope, categories=search_categories)
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(_search_one, emb, scope)
            for emb, scope in product(embeddings, scopes)
        ]
        findings = [f.result() for f in as_completed(futures)]
    
    self.state.confidence = compute_composite_score(findings)
    # Iterative deepening si confidence < seuil
    return findings
```

**Extraction de métadonnées :**
- LLM-powered : entités, dates, topics extraits par le LLM
- Importance scoring : float 0.0–1.0
- Temporal hints pour filtrage temporel

### Système de tools

```python
# Exécution d'un tool avec vérification de finalité
def execute_tool_and_check_finality(tool, tool_input) -> tuple[str, bool]:
    try:
        output = tool.execute(tool_input)
        is_final = output.startswith("[FINAL RESULT]")
        return output, is_final
    except Exception as e:
        return f"Tool error: {e}", False
```

**Tool caching intégré :** `cache_function` sur `BaseTool` → évite les appels redondants

### Forces et faiblesses identifiées dans le code

**Forces :**
- RecallFlow avec `iterative deepening` si confidence < seuil → robustesse sur les queries ambiguës
- Event bus centralisé → observabilité native sur tous les événements
- `CheckpointConfig` → reprise d'exécution après interruption
- Async/sync duality : même logique en `execute_task` et `aexecute_task`
- Tool caching natif

**Faiblesses (observées dans le code) :**
- 3+ appels LLM par task : memory recall + knowledge retrieval + training data
- Tool parsing fragile : regex-based sur les réponses LLM (agent/core.py:~850)
- `SerializableCallable` avec dotted path resolution → cassant si refactoring
- Pas de streaming result aggregation : `CrewOutput` accumule tout avant retour
- Mutations de `_times_executed`, `_mcp_resolver` en PrivateAttr → non thread-safe

---

## 3. OpenAI Agents Python

### Architecture interne réelle

**Fichiers sources clés lus :**
- `src/agents/agent.py`
- `src/agents/run.py` (~1861 lignes)
- `src/agents/guardrail.py`
- `src/agents/handoffs/__init__.py`
- `src/agents/lifecycle.py`

**Hiérarchie des classes :**
```
Agent[TContext]
├── name, description
├── output_type: type[OutputType]
├── tools: list[Tool]
├── model: Model instance
├── model_settings: ModelSettings
├── instructions: str | DynamicPromptFunction
├── input_guardrails: list[InputGuardrail[TContext]]
├── output_guardrails: list[OutputGuardrail[TContext]]
├── hooks: RunHooks[TContext] | None
└── handoffs: list[Handoff[TContext, TAgent]]

Tool = Union[
    FunctionTool,     # Fonctions Python
    CustomTool,       # Sous-classe custom
    ComputerTool,     # Contrôle écran
    ShellTool,        # Exécution CLI
    CodeInterpreter,  # REPL Python
    WebSearchTool,    # Recherche web
    FileSearchTool,   # Recherche fichiers
    MCPTool,          # Model Context Protocol
]
```

### Boucle d'exécution principale (run.py)

```python
# run.py:434-600 — AgentRunner.run()
async def run(self, starting_agent, input) -> RunResult:
    runner_state = RunnerState[TContext](...)
    
    while not runner_state.is_complete:
        agent = runner_state.current_agent
        
        single_step = await run_single_turn(
            bindings=agent_bindings,
            original_input=runner_state.input,
            generated_items=runner_state.items,
            hooks=hooks,
            context_wrapper=context_wrapper,
        )
        
        match single_step:
            case NextStepFinalOutput():
                runner_state.is_complete = True
                runner_state.final_output = single_step.output
            case NextStepHandoff():
                runner_state.current_agent = single_step.target_agent
            case NextStepRunAgain():
                pass  # Continue loop
            case NextStepInterruption():
                return runner_state.to_incomplete_result()
    
    return RunResult(output=runner_state.final_output, items=runner_state.items)
```

**Un tour complet :**
```
get_system_prompt(context_wrapper)
→ run_input_guardrails() [parallèle]
→ get_new_response()     [appel LLM]
→ get_single_step_result_from_response()
    ├── FinalOutput    → terminaison
    ├── ToolCall[]     → exécution tools
    ├── Handoff        → changement d'agent
    └── Refusal        → rejet
→ run_output_guardrails()
→ session.add_items(generated_items)
```

### Guardrails — le meilleur pattern du corpus

```python
# guardrail.py:72-100 — Exécution en parallèle
@dataclass
class InputGuardrail(Generic[TContext]):
    guardrail_function: Callable[
        [RunContextWrapper[TContext], Agent[Any], str | list],
        MaybeAwaitable[GuardrailFunctionOutput],
    ]
    name: str | None = None
    run_in_parallel: bool = True  # Guardrails parallèles par défaut

@dataclass
class GuardrailFunctionOutput:
    output_info: Any
    tripwire_triggered: bool  # Si True → STOP immédiat

# Exécution :
results = await asyncio.gather(*[
    guardrail.guardrail_function(context, agent, input)
    for guardrail in agent.input_guardrails
])

for result in results:
    if result.tripwire_triggered:
        raise InputGuardrailTripwireTriggered(f"Guardrail {result.name} triggered")
```

**Guardrails existent en 4 niveaux :**
1. `InputGuardrail` (agent) → vérifie l'entrée utilisateur
2. `OutputGuardrail` (agent) → vérifie la sortie agent
3. `ToolInputGuardrail` (par tool) → vérifie l'entrée de chaque tool
4. `ToolOutputGuardrail` (par tool) → vérifie la sortie de chaque tool

### Handoffs — Transfert avec transformation d'historique

```python
# handoffs/__init__.py — Transition entre agents
handoff_data = HandoffInputData(
    input_history=session_items_before_handoff,
    pre_handoff_items=generated_items[:-1],
    new_items=tuple(generated_items[-1:] + [response_item]),
)

# Transformation optionnelle de l'historique
transformed_input = await handoff.on_handoff(context_wrapper, handoff_data)
# → run_single_turn(agent=handoff.target_agent, input=transformed_input)
```

**3 stratégies d'historique :**
- `Full history` : l'agent cible voit tout → risque de confusion
- `Summary` : résumé injecté avant handoff → réduction de tokens
- `Clean slate` : seul le message de transfert → isolation maximale

### RunState — Sérialisation complète pour reprises

```python
@dataclass
class RunState[TContext]:
    items: list[RunItem]  # Historique complet
    context: TContext
    
    def serialize(self) -> dict:
        return {
            "tool_use_tracker": ...,
            "function_tools": dict[str, FunctionTool],
            "items_serialized": list[SerializedRunItem],
            "context_json": JSON,
        }
    
    @classmethod
    def restore(cls, data: dict) -> RunState:
        # Hydrate tools depuis les lookup keys
        # Parse items avec contexte tool
        # Restaure context depuis JSON
```

### Forces et faiblesses

**Forces :**
- Guardrails en 4 niveaux découplés de la logique agent → testables indépendamment
- `RunState` sérialisable → reprises après crash, approval interruptions
- `lifecycle.py` hooks : `on_agent_start`, `on_llm_start`, `on_tool_start`, `on_handoff`, `on_agent_end`
- `Session` protocol-based → backend pluggable (DB, Redis, in-memory)
- Streaming natif : `run_single_turn_streamed()`

**Faiblesses :**
- Pas de mémoire long-terme native (session limitée à la run)
- `HandoffInputData` complexe : 4 champs (input_history, pre_handoff_items, new_items, input_items) → confusant
- `RunState` serialization fragile : dotted-path pour tool lookup → casse si refactoring
- Mutations `_approvals`, `usage` en dict durant l'exécution → non thread-safe

---

## 4. LangGraph

### Architecture interne réelle

**Fichiers sources clés lus :**
- `libs/langgraph/langgraph/graph/state.py`
- `libs/langgraph/langgraph/pregel/_algo.py`
- `libs/langgraph/langgraph/checkpoint/`

**Classes principales :**
```
StateGraph[StateT, ContextT, InputT, OutputT]
  → Builder pattern pour assembler le graphe

CompiledStateGraph (hérite de Pregel)
  → Version compilée exécutable

Pregel
  → Moteur d'exécution principal (DAG-like avec supersteps)

PregelNode
  → Nœud avec triggers, channels, writers

BaseChannel
  → Interface : LastValue, Topic, EphemeralValue, NamedBarrierValue
```

### Le moteur Pregel — Supersteps

```python
# pregel/_algo.py — Boucle principale
def run():
    while not complete:
        # 1. Préparer tâches pour le prochain superstep
        tasks = prepare_next_tasks(
            checkpoint, pending_writes, processes, channels,
            managed, config, step
        )
        
        # 2. Exécuter les nœuds en parallèle (thread pool ou async)
        results = await asyncio.gather(*[execute(task) for task in tasks])
        
        # 3. Appliquer les writes et mettre à jour les versions
        apply_writes(checkpoint, channels, tasks, get_next_version, trigger_to_nodes)
        
        # 4. Vérifier les interruptions
        if should_interrupt(checkpoint):
            yield checkpoint
        
        # 5. Sauvegarder checkpoint
        save_checkpoint(checkpoint)
```

**Préparation des tâches :**
```python
# Deux types de tâches :
# PUSH = Send dynamique (parallélisation)
for idx in tasks_channel.get():
    task = prepare_push_task_send(...)  # Send("node_name", {"arg": ...})

# PULL = nœuds déclenchés via edges
for name in candidate_nodes:
    if _triggers(channels, versions, seen, null_version, proc):
        task = prepare_single_task((PULL, name), ...)
```

### Checkpointing — Persistence de l'état

```python
# Schéma d'un checkpoint
Checkpoint = TypedDict({
    'v': int,                          # Version du format (4 actuellement)
    'id': str,                         # UUID unique (uuid6 avec clock_seq=step)
    'ts': str,                         # ISO 8601 timestamp
    'channel_values': dict[str, Any],  # État actuel de tous les canaux
    'channel_versions': dict[str, V],  # Version de chaque canal
    'versions_seen': dict[str, dict[str, V]],  # Versions vues par chaque nœud
    'updated_channels': list[str] | None,
})

def create_checkpoint(checkpoint, channels, step, id=None):
    ts = datetime.now(timezone.utc).isoformat()
    values = {k: channels[k].checkpoint() for k in channels
              if k in checkpoint["channel_versions"]}
    return Checkpoint(
        v=LATEST_VERSION,
        ts=ts,
        id=id or str(uuid6(clock_seq=step)),
        channel_values=values,
        channel_versions=checkpoint["channel_versions"],
        versions_seen=checkpoint["versions_seen"],
    )
```

**Stratégie version-based :** Chaque canal a un numéro de version. Un nœud ne se réexécute que si une version qu'il n'a pas encore vue est disponible → exécution déterministe, replay exact.

### Channels — Types de canaux

| Channel | Comportement | Usage |
|---|---|---|
| `LastValue[T]` | Stocke la dernière valeur | État simple |
| `EphemeralValue[T]` | Non persisté aux checkpoints | Données temporaires |
| `Topic[T]` | File FIFO | Send/parallélisation |
| `NamedBarrierValue[T]` | Attend tous les writers | Synchronisation multi-nœuds |
| `BinaryOperatorAggregate(T, reducer)` | Agrégation custom | `Annotated[list, operator.add]` |

### Send — Parallélisation dynamique

```python
# Générer N tâches parallèles depuis un nœud
def route_to_workers(state: State) -> Sequence[Send]:
    return [Send("process_item", {"item": i}) for i in state["items"]]

# LangGraph exécute toutes ces tâches en parallèle
# puis agrège les résultats via le reducer du state

class State(TypedDict):
    items: list[str]
    results: Annotated[list[str], operator.add]  # Reducer d'agrégation

# Résultat : results contient tous les outputs des N workers
```

### Forces et faiblesses

**Forces :**
- Version-based synchronization → pas de race conditions, replay déterministe
- Durable execution : checkpoint après chaque nœud → reprise exacte après crash
- Human-in-the-loop natif via `interrupt_before/after`
- `Send` → parallélisation dynamique O(n) tasks
- Subgraphs imbriqués (nœud = graphe complet)
- 8 modes de streaming : "values", "updates", "messages", "debug", "checkpoints", etc.
- Functional API : `@entrypoint`, `@task` comme alternative au Builder

**Faiblesses :**
- Single machine : pas de distributed execution out-of-the-box
- Checkpoint serialization : doit être msgpack-compatible → contrainte sur les types custom
- Courbe d'apprentissage élevée (concept Pregel non-intuitif)
- Dépendance forte à LangChain (pour les composants)
- Implicit channel initialization : inféré depuis le state schema → erreurs cryptiques

---

## 5. LangFlow

### Architecture interne réelle

**Découverte critique :** LangFlow utilise **`lfx.graph`** comme moteur sous-jacent, un package séparé. Le vrai moteur est wrappé.

```python
# langflow/graph/__init__.py — proxy explicite
from lfx.graph.edge.base import Edge
from lfx.graph.graph.base import Graph
from lfx.graph.vertex.base import Vertex
```

**Conséquences :**
- Difficile de lire le code moteur directement (externe)
- LangFlow = couche d'adapters + composants autour de `lfx`
- Architecture plus opaque que LangGraph

**Vertex types :**
- `CustomComponentVertex` : composants user-defined
- `InterfaceVertex` : points d'entrée/sortie du flow
- `StateVertex` : gestion d'état entre sessions

### Boucle d'exécution inférée

```python
# Topological sort + exécution dans l'ordre
def run_flow(graph, inputs):
    ordered = topological_sort(graph.vertices)
    state = {**inputs}
    for vertex in ordered:
        if all(dependencies_satisfied(vertex)):
            outputs = execute_component(vertex, state)
            state.update(outputs)
    return extract_leaf_outputs(state)
```

### Forces et faiblesses

**Forces :**
- 200+ composants dans la palette
- REST API + WebSocket natif → exposer un flow comme endpoint en 1 clic
- Sauvegarde/historique des flows en DB
- Visual builder accessible aux non-développeurs

**Faiblesses (observées) :**
- Moteur opaque (lfx.graph externe) → debugging limité
- Pas de checkpoint/resume natif (contrairement à LangGraph)
- Type system basique (moins rigoureux que Haystack)
- Versionning difficile : les DAG JSON ne se lisent pas bien dans git diff

**Quand choisir LangFlow vs LangGraph :**
- LangFlow : prototypage rapide, équipes non-techniques, flows simples à linéaires
- LangGraph : agents stateful, long-running, human-in-the-loop, parallélisation dynamique

---

## 6. Haystack

### Architecture interne réelle

**Fichiers sources clés lus :**
- `haystack/core/pipeline/pipeline_base.py`
- `haystack/core/component/`

**Classes principales :**
```
Pipeline(PipelineBase)
  → Moteur synchrone

AsyncPipeline
  → Moteur asynchrone avec gather()

Component (Protocol)
  → Interface requise : run(self, ...) → dict[str, Any]
  → Sockets auto-inférés depuis les type hints

PipelineBase
  → add_component(name, instance)
  → connect(source, target)  → validation type-safe
  → run(data) → dict[str, Any]
```

### Typed sockets — L'innovation principale

```python
# Composant avec sockets typés
from haystack.core.component import component

@component
class PromptBuilder:
    def __init__(self, template: str):
        self.template = template
    
    @component.output_types(prompt=str)
    def run(self, question: str) -> dict[str, str]:
        return {"prompt": self.template.format(question=question)}

# Au runtime :
# builder.__haystack_input__  = {"question": InputSocket(type=str, required=True)}
# builder.__haystack_output__ = {"prompt": OutputSocket(type=str)}

# Validation à la connexion :
pipeline.connect("prompt.prompt", "llm.prompt")
# → Vérifie OutputSocket[str] → InputSocket[str] → OK
# → Raise PipelineValidationError si types incompatibles
```

**Sockets dynamiques :**
```python
class Sockets:
    def __init__(self, component, sockets_dict, sockets_io_type):
        self._sockets_dict = sockets_dict
        self.__dict__.update(sockets_dict)  # Accès par attribut
    
    def __setitem__(self, key, socket):
        self._sockets_dict[key] = socket
        self.__dict__[key] = socket  # Mise à jour dynamique
```

### Boucle d'exécution pipeline.run()

```python
# pipeline_base.py — run()
def run(self, data, include_outputs_from=None):
    self.warm_up()
    data = self._prepare_component_input_data(data)
    
    ordered = sorted(self.graph.nodes.keys())
    component_visits = {name: 0 for name in ordered}
    priority_queue = self._fill_queue(ordered, data, component_visits)
    
    pipeline_outputs = {}
    
    while True:
        priority, component_name, component = self._get_next_runnable_component(
            priority_queue, component_visits
        )
        
        if priority == ComponentPriority.BLOCKED:
            break
        
        component_inputs = self._consume_component_inputs(
            component_name, component, data
        )
        
        try:
            component_outputs = self._run_component(
                component_name, component, component_inputs, component_visits
            )
        except (BreakpointException, PipelineRuntimeError) as error:
            # Créer snapshot pour debugging/resume
            pipeline_snapshot = _create_pipeline_snapshot(...)
            error.pipeline_snapshot = pipeline_snapshot
            raise error
        
        component_visits[component_name] += 1
        component_pipeline_outputs = self._write_component_outputs(...)
        
        if self._is_queue_stale(priority_queue):
            priority_queue = self._fill_queue(ordered, data, component_visits)
    
    return pipeline_outputs
```

### PipelineSnapshot — Debugging avancé

```python
@dataclass
class PipelineSnapshot:
    pipeline_state: PipelineState    # inputs, outputs, component_visits
    pipeline_outputs: dict[str, Any]
    ordered_component_names: list[str]
    break_point: Breakpoint | AgentBreakpoint
    include_outputs_from: set[str]
    snapshot_file_path: str | None = None
    agent_snapshot: AgentSnapshot | None = None
    
    def to_json(self) -> str: ...  # Sérialise pour debugging
```

### Sérialisation — Le point fort pour les équipes

```python
# Sauvegarder un pipeline
pipeline_dict = pipeline.to_dict()
# → {"components": {"prompt": {...}, "llm": {...}}, "connections": [...]}

# Charger depuis config
pipeline = Pipeline.from_dict(pipeline_dict)

# La sérialisation valide la compatibilité des types à la re-création
```

### Forces et faiblesses

**Forces :**
- Type safety stricte → erreurs détectées au `connect()`, pas au runtime
- Sérialisation/désérialisation avec validation → déploiement reproductible
- 100+ composants production-ready (LLMs, retrievers, embedders, rankers)
- `warm_up()` pattern → lazy initialization des modèles
- `AsyncPipeline` avec `asyncio.gather()` pour composants indépendants

**Faiblesses :**
- Pas de `Send`-like pour parallélisation dynamique (contrairement à LangGraph)
- State accumulation en mémoire : tous inputs/outputs cumulés → problématique sur longs pipelines
- `warm_up()` appelé à chaque run (potentiellement) → overhead si déjà warm
- Pas de checkpoint temps-réel (snapshots créés uniquement sur erreur/breakpoint)

---

## 7. Dify

### Architecture interne réelle

**Fichiers sources clés lus :**
- `api/core/workflow/node_factory.py`
- `api/core/workflow/node_runtime.py`
- `api/core/workflow/nodes/agent_node.py`
- `api/extensions/ext_celery.py`

**Architecture en couches :**
```
Dify (adapters Dify-specific)
  └── graphon (moteur de graph agnostique, bibliothèque interne)
        └── Topology + Node config (JSON)
              └── node_factory.py → inject dépendances Dify dans les nodes
```

**Clé architecturale :** `graphon` est un sous-système agnostique. Dify l'entoure d'adapters :

```python
# node_factory.py — Injection de contexte Dify dans graphon
def to_graph_init_params(self) -> "GraphInitParams":
    return GraphInitParams(
        workflow_id=self.workflow_id,
        graph_config=self.graph_config,   # Topologie + config nœuds
        run_context=self.run_context,     # Contexte Dify (tenant_id, user_id, etc.)
        call_depth=self.call_depth,
    )
```

**AgentNode — Résolution dynamique de stratégie :**
```python
# nodes/agent_node.py
class AgentNode(Node[AgentNodeData]):
    def _run(self) -> Generator[NodeEventBase, None, None]:
        dify_ctx = DifyRunContext.model_validate(
            self.require_run_context_value(DIFY_RUN_CONTEXT_KEY)
        )
        # Résolution dynamique de la stratégie agent
        strategy = self._strategy_resolver.resolve(
            tenant_id=dify_ctx.tenant_id,
            agent_strategy_provider_name=self.node_data.agent_strategy_provider_name
        )
```

### Queue async avec Celery + Redis Sentinel

```python
# ext_celery.py — High availability avec Sentinel
transport_options = CelerySentinelTransportDict(
    master_name=dify_config.CELERY_SENTINEL_MASTER_NAME,
    sentinel_kwargs=_CelerySentinelKwargsDict(
        socket_timeout=dify_config.CELERY_SENTINEL_SOCKET_TIMEOUT,
        password=dify_config.CELERY_SENTINEL_PASSWORD,
    ),
)
```

**Points d'entrée workflow :**
1. REST API → `async_workflow_service.py`
2. Scheduler (Celery beat) → `workflow_schedule_task.py`
3. Webhooks → `trigger_webhook_node.py`
4. Plugin triggers → `trigger_plugin_node.py`

### Plugin daemon — Architecture isolée

Le système de plugins Dify utilise un **daemon externe** (processus séparé) :

```python
# core/plugin/impl/plugin.py
class PluginClient:
    """Client pour communiquer avec le plugin daemon."""
    # Architecture : Dify core ← HTTP/RPC → plugin daemon
    # Isolation : si le daemon plante, Dify continue sans les plugins
```

**Avantage :** Hot-reloading des plugins sans restart de Dify  
**Risque :** Si le daemon plante, tous les agents utilisant des plugins sont bloqués

### Forces et faiblesses

**Forces :**
- Séparation graphon/Dify → upgrades du moteur sans refonte du code métier
- Plugin daemon isolé → hot-reloading, tolérance aux pannes
- Celery + Redis Sentinel → haute disponibilité de la queue
- Multi-tenant natif via `DifyRunContext` (tenant_id, user_id injectés à chaque exécution)
- RAG pipeline intégré + 40+ LLM providers

**Faiblesses :**
- Tight coupling au plugin daemon → point de défaillance unique
- Workflows à topologie statique : le graph JSON ne peut pas changer à runtime
- Streaming end-to-end limité par Celery (latence de queue)
- Lourd à déployer (~1GB+ dépendances)

---

## 8. OpenHands

### Architecture interne réelle

**Fichiers sources clés lus :**
- `openhands/events/event.py`
- `openhands/events/event_store.py`
- `openhands/events/stream.py`
- `openhands/core/schema/agent.py`
- `openhands/app_server/app_conversation/`

**Migration V0 → V1 :**
- **V0 (Legacy)** : États énumérés (LOADING, RUNNING, AWAITING_USER_INPUT)
- **V1 (Actuel)** : Architecture basée sur AgentSDK externe + FastAPI app_server

### EventStream — Thread-safe avec pool par subscriber

```python
# events/stream.py
class EventStream(EventStore):
    _queue: queue.Queue[Event]                      # Thread-safe queue
    _queue_thread: threading.Thread                  # Thread dédié au processing
    _subscribers: dict[str, dict[str, Callable]]    # Callbacks par subscriber
    _thread_pools: dict[str, dict[str, ThreadPoolExecutor]]  # Pool par subscriber
    _thread_loops: dict[str, dict[str, asyncio.AbstractEventLoop]]

# Subscribers : SERVER, MEMORY, RESOLVER
# Chaque subscriber a son propre thread pool → isolation des erreurs
```

**Types d'événements :**
```python
@dataclass
class Event:
    _id: int
    _timestamp: str
    _source: EventSource   # AGENT | USER | ENVIRONMENT
    _cause: int            # Event ID qui a causé cet événement (traçabilité)

@dataclass
class CmdRunAction(Action):
    command: str
    thought: str = ''
    blocking: bool = False
    confirmation_state: ActionConfirmationStatus
    security_risk: ActionSecurityRisk
    runnable: ClassVar[bool] = True
```

### Système de sécurité multi-couche

```python
# Configuration security policy
class SecurityAnalyzerBase: ...

class LLMSecurityAnalyzer(SecurityAnalyzerBase):
    """Analyse chaque action via LLM pour évaluer le risque."""

class ConfirmationPolicy:
    AlwaysConfirm  = ...  # Confirme tout
    NeverConfirm   = ...  # Ne confirme rien (autonomous mode)
    ConfirmRisky   = ...  # Confirme uniquement HIGH risk
    LLMSecurityAnalyzer = ...  # Délègue au LLM

# Niveaux de risque
class ActionSecurityRisk:
    UNKNOWN  = -1
    LOW      = 0
    MEDIUM   = 1
    HIGH     = 2
```

### Skills multi-sources avec merge TOML

```python
# app_server — Résolution des skills
def _merge_skills(self, skill_lists: list[list[Skill]]) -> list[Skill]:
    skills_by_name: dict[str, Skill] = {}
    for skill_list in skill_lists:
        for skill in skill_list:
            skills_by_name[skill.name] = skill  # Later lists override
    return list(skills_by_name.values())

# Sources de skills (merge dans l'ordre) :
# base → team (~/.openhands/team/) → user (~/.openhands/) → projet → sandbox
```

**Règles de merge TOML :**
- Scalars : override (valeur suivante gagne)
- Tables : deep-merge
- Arrays : append (sauf si keyed par code/id → replace matching)

### Forces et faiblesses

**Forces :**
- EventStore = traçabilité complète + replay possible
- SecurityAnalyzer pluggable → politique de sécurité configurable par déploiement
- Skills multi-sources avec merge déterministe
- Sandbox Docker/Kubernetes → isolation maximale
- Architecture V1 proprement séparée de V0 legacy

**Faiblesses :**
- Dépendance à AgentSDK externe → core logic hors repo, debugging limité
- EventStream threading complexe : threads + asyncio event loops par subscriber → surface d'erreurs élevée
- Pas de timeout global configurable (hardcodé par type d'action)
- Limited error recovery : une fois confirmée, peu de rollback possible

---

## 9. browser-use

### Architecture interne réelle

**Fichiers sources clés lus :**
- `browser_use/agent/service.py` (~162 KB — le fichier le plus gros du corpus)
- `browser_use/browser/session.py` (~155 KB)
- `browser_use/browser/watchdogs/`

**Composants :**
```
Agent (service.py)
  → Boucle principale async

BrowserSession (session.py)
  → CDP (Chrome DevTools Protocol) via cdp_use
  → Gestion onglets + watchdogs

DomService
  → Extraction DOM + accessibility tree + iframes

Tools
  → Registry d'actions avec validation Pydantic

MessageManager
  → Compaction intelligente pour budget LLM

ScreenshotService
  → Stockage base64 local
```

### Boucle d'exécution step par step

```python
# agent/service.py — step()
async def step(self, step_info: AgentStepInfo | None = None) -> None:
    # Phase 1 : Attente si CAPTCHA en cours (watchdog)
    await self.browser_session.wait_if_captcha_solving()
    
    # Phase 2 : Préparation du contexte
    browser_state = await self._prepare_context(step_info)
    # - Capture screenshot
    # - Met à jour les action models (spécifiques à la page)
    # - Crée message context
    # - Compacte si budget LLM dépassé
    
    # Phase 3 : Appel LLM + exécution actions
    await self._get_next_action(browser_state)   # LLM avec timeout
    await self._execute_actions()                 # Exécution parallèle (max 5)
    
    # Phase 4 : Post-processing + finalisation
    await self._post_process()
    await self._finalize(browser_state)
```

### Screenshot avec caching intelligent

```python
# browser/session.py — get_browser_state_summary()
async def get_browser_state_summary(
    self,
    include_screenshot: bool = True,
    cached: bool = False,
    include_recent_events: bool = False,
) -> BrowserStateSummary:
    # Cache check
    if cached and self._cached_browser_state_summary:
        if not include_screenshot or self._cached_browser_state_summary.screenshot:
            return self._cached_browser_state_summary
    
    # Event-driven : dispatch request, await result
    event = self.event_bus.dispatch(BrowserStateRequestEvent(
        include_dom=True,
        include_screenshot=include_screenshot,
    ))
    return await event.event_result(raise_if_none=True)
```

### Watchdogs — Monitoring passif event-driven

15+ watchdogs surveillent l'état du navigateur sans bloquer la boucle principale :

| Watchdog | Rôle |
|---|---|
| `CaptchaWatchdog` | Bloque step jusqu'à captcha résolu (timeout 120s) |
| `DownloadsWatchdog` | Détecte PDFs auto-download |
| `CrashWatchdog` | Détecte browser crash |
| `SecurityWatchdog` | Interception SSL/TLS |
| `PopupsWatchdog` | Auto-close popups non-intentionnels |
| `DOMWatchdog` | Détecte DOM mutations, staleness |
| `DefaultActionWatchdog` | 131KB — gère les edge cases d'actions |

```python
# CaptchaWatchdog — Pattern event-driven
def _on_captcha_started(event_data, session_id) -> None:
    self._captcha_solving = True
    self._captcha_solved_event.clear()  # Bloque le waiter

def _on_captcha_finished(event_data, session_id) -> None:
    self._captcha_solving = False
    self._captcha_solved_event.set()  # Débloque le waiter
```

### Actions typées — Validation Pydantic stricte

```python
class ClickElementAction(BaseModel):
    index: int | None = Field(default=None, ge=1)  # ≥ 1 requis
    coordinate_x: int | None = Field(default=None)
    coordinate_y: int | None = Field(default=None)
```

### Forces et faiblesses

**Forces :**
- Watchdogs event-driven → monitoring passif sans bloquer la boucle
- DOM + screenshot dual-channel → tolérance aux changements de layout
- MessageManager avec compaction → gestion du budget LLM
- MCP natif → intégrable dans Claude Code / Cursor
- Loop detection + replan nudges → injecte guidance quand agent bloqué

**Faiblesses :**
- `DefaultActionWatchdog` de 131KB → fichier monolithique difficile à maintenir
- 15+ watchdogs indépendants → surface d'interaction complexe
- Pas de checkpoint/resume entre steps
- Pas d'execution isolation (si browser crash = agent crash)
- Coût élevé par step : screenshot (~3-5K tokens) + DOM à chaque action

---

## 10. BMAD-METHOD

### Architecture interne réelle

BMAD est entièrement basé sur **Markdown + TOML** (aucun code Python/JS exécutable). L'exécution repose sur le LLM qui suit les instructions.

**Structure des skills :**
```
src/
├── core-skills/          → Skills fondamentaux
└── bmm-skills/           → Skills métier (4 phases)
    ├── 0-discovery/      → Analyst (Mary)
    ├── 1-planning/       → Product Manager (John)
    ├── 2-solutioning/    → Architect (Winston), Designer, Writer
    └── 3-implementation/ → Developer (Amelia)
```

### Activation d'un agent — Séquence réelle

```markdown
## On Activation

Step 1: Resolve Agent Block
  - Read customize.toml (base)
  - Apply team overrides from {project-root}/_bmad/custom/{skill-name}.toml
  - Apply personal overrides from {project-root}/_bmad/custom/{skill-name}.user.toml
  - Merge rules: scalars override, tables deep-merge, arrays append

Step 2: Execute Prepend Steps (activation_steps_prepend)
Step 3: Adopt Persona (name, title, icon, identity, communication_style, principles)
Step 4: Load Persistent Facts (file: globs + literal facts)
Step 5: Load Config (user_name, communication_language, document_output_language)
Step 6: Greet User with Icon Prefix
Step 7: Execute Append Steps (activation_steps_append)
Step 8: Dispatch Menu or Present Menu Items
```

### Customize.toml — Configuration d'agent

```toml
# Winston Agent Config
[agent]
name = "Winston"
title = "System Architect"
icon = "🏗️"
role = "Convert PRD and UX into technical architecture"
identity = "Channels Martin Fowler's pragmatism"
communication_style = "Calm and pragmatic. Answers with trade-offs, not verdicts."

persistent_facts = [
  "file:{project-root}/**/project-context.md",  # Glob load
]

activation_steps_prepend = []
activation_steps_append = []

[[agent.menu]]
code = "CA"
description = "Guided workflow to document technical decisions"
skill = "bmad-create-architecture"

# Règles de merge :
# - scalars : override (valeur suivante gagne)
# - tables  : deep-merge
# - arrays  : append (si keyed par code/id → replace matching + append new)
```

### Anti-bias protocol — Innovation réelle

```markdown
# Brainstorming Anti-Bias Protocol

**Critical Mindset:** LLMs naturally drift toward semantic clustering (sequential bias).
To combat: consciously shift creative domain every 10 ideas.

Example progression:
1. Ideas 1-10:  Technical architecture aspects
2. Ideas 11-20: User experience considerations
3. Ideas 21-30: Business viability & economics
4. Ideas 31-40: Edge cases & "black swan" scenarios

Quantity Goal: 100+ ideas before any organization.
First 20 are obvious, magic happens in 50-100 range.
```

**Insight :** Ce protocole compense explicitement le biais de clustering sémantique des LLMs. C'est une compensation architecturale du défaut "dérive d'objectif".

### Forces et faiblesses

**Forces :**
- Micro-file architecture → chaque step auto-contenu, atomic, skippable/restartable
- Merge TOML à 3 couches (base/team/user) → customisation sans duplication
- Append-only documents → audit trail naturel, historique préservé
- Anti-bias protocol → compensation explicite du biais LLM
- Persona injection dans toml → spécialisation forte du LLM
- SOG (Single user-facing agent) → utilisateur ne voit jamais la complexité interne

**Faiblesses :**
- Aucun code exécutable → 100% dépendant du LLM pour la récupération d'erreurs
- Scale limité : pas de loop/conditional execution complexe
- User input blocking à chaque step → pas fully autonomous
- Pas de partage d'état inter-agents natif
- Couplage workflows : difficile à refactorer sans duplication

---

## 11. Langfuse

### Architecture interne réelle

**Fichiers sources clés lus :**
- `packages/shared/prisma/schema.prisma`
- `packages/shared/src/db/` 
- `web/src/features/traces/`

**Monorepo TypeScript + Python :**
```
web/         → Frontend Next.js + Backend tRPC/API
worker/      → Workers asynchrones (ClickHouse ingestion, évaluations)
packages/
  shared/    → Schémas Prisma + SDK base
```

### Schéma de base de données — Architecture hybride

```prisma
// schema.prisma — Modèle de traces
model LegacyPrismaTrace {
  id        String   @id @default(cuid())
  name      String?
  timestamp DateTime @default(now())
  userId    String?  @map("user_id")
  sessionId String?  @map("session_id")
  input     Json?
  output    Json?
  metadata  Json?
  tags      String[]
  bookmarked Boolean @default(false)
  projectId String   @map("project_id")
}

// Observations (spans + generations)
model LegacyPrismaObservation {
  id               String   @id @default(cuid())
  traceId          String?  @map("trace_id")
  parentObservationId String? @map("parent_observation_id")
  type             LegacyPrismaObservationType  // SPAN, EVENT, GENERATION, AGENT, TOOL
  startTime        DateTime @default(now())
  endTime          DateTime?
  name             String?
  promptTokens     Int      @default(0)
  completionTokens Int      @default(0)
  totalTokens      Int      @default(0)
  inputCost        Decimal?
  outputCost       Decimal?
  totalCost        Decimal?
  
  @@index([traceId, projectId, type, startTime])
}

// Scores (annotations humaines + auto-évaluations)
model LegacyPrismaScore {
  id            String    @id @default(cuid())
  traceId       String
  observationId String?   // Optionnel : score sur un span spécifique
  name          String
  value         Float?
  stringValue   String?
  dataType      ScoreDataType  // NUMERIC, CATEGORICAL, BOOLEAN
  source        ScoreSource    // HUMAN, API, EVAL
}
```

**Insight :** Le préfixe "Legacy" signale une **migration en cours** vers une architecture ClickHouse + Postgres hybride. Les traces récentes vont dans ClickHouse (requêtes volumineuses temps réel) ; les métadonnées restent en Postgres.

### Modèle de données TypeScript

```typescript
// domain/traces.ts
export const TraceDomain = z.object({
  id: z.string(),
  name: z.string().nullable(),
  timestamp: z.date(),
  environment: z.string(),
  tags: z.array(z.string()),
  bookmarked: z.boolean(),
  public: z.boolean(),
  release: z.string().nullable(),
  version: z.string().nullable(),
  input: jsonSchema.nullable(),
  output: jsonSchema.nullable(),
  metadata: MetadataDomain,
  sessionId: z.string().nullable(),
  userId: z.string().nullable(),
  projectId: z.string(),
});

// Colonnes de la table traces (avec mapping ClickHouse)
export const tracesTableCols: ColumnDefinition[] = [
  { name: "Input Tokens", id: "inputTokens",
    type: "number", internal: 'generation_metrics."promptTokens"' },
  // ...
];
```

### Forces et faiblesses

**Forces :**
- Schéma traces hiérarchique via `parentObservationId` → DAG complet d'exécution
- `ScoreDataType` : NUMERIC, CATEGORICAL, BOOLEAN, TEXT → évaluations multi-format
- Cost tracking natif : `inputCost`, `outputCost`, `totalCost` par observation
- Multi-tenant via `projectId` sur toutes les entités
- Real-time via WebSockets + tRPC subscriptions

**Faiblesses :**
- Migration Postgres→ClickHouse incomplète → 2 sources de vérité, sync challenges
- "Legacy" naming dans le schéma → dette technique visible
- Infra lourde : ClickHouse + Postgres → overhead pour petits projets
- Pricing engine séparé → configuration manuelle par model/provider

---

## 12. mempalace

### Architecture interne réelle

**Fichiers sources clés lus :**
- `mempalace/palace.py`
- `mempalace/backends/base.py`
- `mempalace/backends/chroma.py`
- `mempalace/miner.py`

**Structure :**
```
Palace (palace.py)
  └── Backend (ChromaDB par défaut)
        ├── Collection "mempalace_drawers"   → stockage verbatim
        └── Collection "mempalace_closets"  → index de recherche

Miner (miner.py)
  → Chunking par taille (800 chars, 100 overlap)
  → Gitignore matching
  → Normalization pipeline v2

Searcher (searcher.py)
  → Hybrid search : BM25 + embeddings sémantiques
```

### Interface abstraite du backend

```python
# backends/base.py — Interface ABC
@dataclass(frozen=True)
class QueryResult(_DictCompatMixin):
    ids: list[list[str]]
    documents: list[list[str]]
    metadatas: list[list[dict]]
    distances: list[list[float]]
    embeddings: Optional[list[list[list[float]]]] = None

class BaseCollection(ABC):
    @abstractmethod
    def query(self, *, query_texts=None, query_embeddings=None,
              n_results=10, where=None, include=None) -> QueryResult: ...
    @abstractmethod
    def upsert(self, *, documents, ids, metadatas=None, embeddings=None) -> None: ...
    @abstractmethod
    def delete(self, *, ids=None, where=None) -> None: ...
    # + 9 autres méthodes
```

### Chunking et indexation

```python
# miner.py — Constantes de chunking
CHUNK_SIZE = 800         # caractères par drawer
CHUNK_OVERLAP = 100      # overlap entre chunks
MIN_CHUNK_SIZE = 50      # skip les chunks trop petits
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB garde-fou
NORMALIZE_VERSION = 2    # Version de normalisation (v2 = strip noise pour JSONL)
```

**Pipeline d'indexation :**
1. Scan des fichiers projet (gitignore-aware)
2. Chunking (800 chars, 100 overlap)
3. Extraction entités + topics
4. Upsert dans Chroma (ID = hash du contenu)
5. Métadonnées : `{wing, room, normalized_version, entity_tags, ...}`

### Le pattern Palace — Hiérarchie spatiale

```
Palace (= projet)
  └── Wing (= catégorie/dossier, ex: "src/", "docs/")
        └── Room (= granularité logique, section d'un fichier)
              └── Drawer (= chunk verbatim avec métadonnées)
```

**Avantage clé :** La recherche peut être scopée : "chercher X dans le wing 'architecture'" → précision supérieure à une recherche globale sur tout le corpus.

### Forces et faiblesses

**Forces :**
- Stockage 100% verbatim (pas de résumé → pas de perte d'information)
- 96.6% R@5 sur LongMemEval (benchmark long-context retrieval)
- Hiérarchie spatiale → recherche scopée précise
- Backend pluggable via `BaseCollection` ABC
- Local-first → zéro appels API externes

**Faiblesses :**
- Instance backend singleton (`_DEFAULT_BACKEND = ChromaBackend()`) → pas de multi-tenancy native
- ChromaDB uniquement documenté/testé → autres backends non validés
- Indexation batch seulement (pas de real-time)
- Single-machine : pas de distributed indexing
- Pas de TTL sur les drawers (accumulation sans fin)

---

## 13. kagent

### Architecture interne réelle

**Fichiers sources clés lus :**
- `go/api/v1alpha2/agent_types.go`
- `go/core/internal/controller/agent_controller.go`
- `go/core/cmd/controller/main.go`

**CRDs Go (v1alpha2) :**
```go
// agent_types.go
type AgentType string
const (
    AgentType_Declarative AgentType = "Declarative"
    AgentType_BYO         AgentType = "BYO"
)

type AgentSpec struct {
    Type        AgentType
    BYO         *BYOAgentSpec
    Declarative *DeclarativeAgentSpec
    Skills      *SkillForAgent  // Pull images/repos
    Sandbox     *SandboxConfig
    AllowedNamespaces *AllowedNamespaces  // Cross-namespace routing
}

type SkillForAgent struct {
    Refs       []string   // Container images OCI
    GitRefs    []GitRepo  // Git repos
    GitAuthSecretRef *corev1.LocalObjectReference
}
```

### Controller loop — Pattern Kubernetes standard

```go
// agent_controller.go — Reconciliation
type AgentController struct {
    Scheme        *runtime.Scheme
    Reconciler    reconciler.KagentReconciler
    AdkTranslator agent_translator.AdkApiTranslator
}

func (r *AgentController) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    return ctrl.Result{}, r.Reconciler.ReconcileKagentAgent(ctx, req)
}

func (r *AgentController) SetupWithManager(mgr ctrl.Manager) error {
    build := ctrl.NewControllerManagedBy(mgr).
        WithOptions(controller.Options{
            NeedLeaderElection: new(true),  // Mode haute disponibilité
        }).
        For(&v1alpha2.Agent{}, builder.WithPredicates(
            predicate.Or(
                predicate.GenerationChangedPredicate{},
                predicate.LabelChangedPredicate{},
            ),
        ))
    // Watch: ModelConfig, RemoteMCPServer, etc.
    return build.Named("agent").Complete(r)
}
```

**Flux de provisioning :**
```
User creates Agent CRD
  → Controller watches + reconciles
  → Creates Sandbox resource (x-k8s.io group)
  → agentsxk8s backend provisions Pod
  → Skills init container pulls code/binaries
  → MCP server discovery registers tools dynamically
```

### Main entry avec authentification pluggable

```go
// cmd/controller/main.go
func main() {
    authorizer := &auth.NoopAuthorizer{}
    app.Start(func(bootstrap app.BootstrapConfig) (*app.ExtensionConfig, error) {
        authenticator := getAuthenticator(bootstrap.Config.Auth)
        return &app.ExtensionConfig{
            Authenticator: authenticator,
            Authorizer:    authorizer,
            SandboxBackend: agentsxk8s.New(),  // Backend K8s
        }, nil
    }, nil)
}
```

### Forces et faiblesses

**Forces :**
- Agents comme ressources K8s déclaratives → version control (GitOps)
- `NeedLeaderElection: true` → haute disponibilité native
- Skills-as-images → réutilisation cross-équipes via OCI registries
- Cross-namespace routing via Gateway API pattern
- MCP server discovery comme ressources K8s

**Faiblesses :**
- v1alpha2 = API instable (alpha), peut changer
- Skills pulling sans vérification native (dépend de la signature OCI)
- MCP discovery synchrone dans le reconcile loop → potentiellement bloquant
- Pod per agent = overhead K8s significatif
- Single-machine en dev (K8s requis même en local → minikube/kind)

---

## 14. LLMLingua

### Architecture interne réelle

**Fichier source clé lu :**
- `llmlingua/prompt_compressor.py` (1000+ lignes)

**Algorithme de compression à 3 niveaux :**

```python
class PromptCompressor:
    def compress_prompt(
        self,
        context: List[str],
        instruction: str = "",
        question: str = "",
        rate: float = 0.5,              # Garder 50% des tokens
        target_token: float = -1,        # Ou viser un nombre absolu
        use_context_level_filter: bool = True,   # Niveau 1 : granularité phrase
        use_sentence_level_filter: bool = False,  # Niveau 2 : sous-phrase
        use_token_level_filter: bool = True,      # Niveau 3 : par token
        rank_method: str = "llmlingua",
    ) -> dict:
        # Returns:
        # {
        #   "compressed_prompt": str,
        #   "origin_tokens": int,
        #   "compressed_tokens": int,
        #   "ratio": str,   # ex: "2.0x"
        #   "rate": str,    # ex: "50%"
        #   "saving": str,  # Économie pour GPT-4 pricing
        # }
```

### Score d'importance par cross-entropy loss

```python
# La clé : les tokens avec la PLUS HAUTE loss sont les plus importants
def calculate_loss(self, input_ids, attention_mask,
                   condition_mode="before",
                   granularity="sentence",
                   return_kv=False):
    shift_logits = outputs.logits[..., :-1, :].contiguous()
    shift_labels = input_ids[..., 1:].contiguous()
    
    loss_fct = torch.nn.CrossEntropyLoss(reduction="none")
    loss = loss_fct(active_logits, active_labels)
    # Tokens avec HAUTE loss → surprenants pour le modèle → à garder
    # Tokens avec BASSE loss → prévisibles → candidats à la suppression
```

**Intuition :** Un token facile à prédire (ex: "le" après "bonjour") est peu informatif. Un token surprenant (ex: "refus" dans "la banque dit refus") porte l'essentiel de l'information.

### LLMLingua-2 — Version accélérée

```python
def init_llmlingua2(self, max_batch_size=50, max_force_token=100):
    self.max_batch_size = max_batch_size
    self.max_force_token = max_force_token
    # Tokens spéciaux [NEW0], [NEW1], ... pour préservation forcée
    self.added_tokens = [f"[NEW{i}]" for i in range(max_force_token)]
    self.tokenizer.add_special_tokens({"additional_special_tokens": self.added_tokens})
    self.model.resize_token_embeddings(len(self.tokenizer))
```

**LLMLingua v1 vs v2 :**
| | v1 | v2 |
|---|---|---|
| Méthode | Perplexité (plus lente) | Data distillation (plus rapide) |
| Modèle | Llama-2-7b-hf | xlm-roberta-large |
| Précision | Plus haute | Légèrement moindre |
| Production | Possible | Recommandée |

### Forces et faiblesses

**Forces :**
- Compression verbatim (pas de résumé) → préserve la factualité
- 3 niveaux indépendants (context/sentence/token) → contrôle fin
- `compress_json()` natif → pipelines structurés
- Ratios documentés : jusqu'à 20x compression avec perte minimale

**Faiblesses :**
- Latence : inférence du modèle de compression avant chaque appel LLM
- Pas de streaming (texte complet requis en mémoire)
- Entraîné principalement en anglais → résultats variables en français
- Peut supprimer des instructions de sécurité importantes si rate trop élevé
- Divergence tokenizers : tiktoken (OpenAI) ≠ HF tokenizers → comptes approximatifs

---

## 15. Octogent

### Architecture interne réelle

**Fichiers sources lus :**
- `src/workers/pool.ts`
- `src/agent/orchestrator.ts`
- `src/agent/loop.ts`

**Worker pool TypeScript :**
```typescript
// workers/pool.ts
class WorkerPool {
    workers: Worker[]           // 8 slots (taille fixe)
    
    // Events émis : 
    // "task:completed", "task:failed", "llm:chunk", "tool:call", "tool:result"
    
    // Messages reçus par chaque worker :
    // "start_task", "cancel_task", "shutdown"
    
    // Auto-redémarrage des workers crashés avec reschedule des tâches
}
```

**DAG naïf avec dépendances :**
```typescript
// agent/orchestrator.ts — runParallel()
const depMap = new Map<string, string[]>();
depMap.set(taskId, spec.dependsOn);  // tâche dépend de ces IDs

// Vérification :
const depsmet = deps.every(d =>
    completed.has(d) && completed.get(d)!.success
);

// Pas de scheduler sophistiqué : itération linéaire des pending tasks
```

**Boucle agent :**
```typescript
// agent/loop.ts
const MAX_ITERATIONS = 50;  // Limite anti-boucle

// Completion détectée via marqueur textuel :
// "<TASK_COMPLETE>result</TASK_COMPLETE>"

// Context pruning naïf : tokenization estimation (tokens < context_limit)
```

### Forces et faiblesses

**Forces :**
- Worker pool EventEmitter : pattern simple et efficace pour ≤8 workers concurrents
- Fallback LLM automatique : Ollama (local) → Groq (cloud)
- Persistance SQLite : sessions, tâches, messages, memory
- Circuit breaker natif : `max_iterations = 50`

**Faiblesses :**
- Pool taille fixe (8) : pas d'auto-scaling
- DAG sans vrai scheduler → ordre d'exécution fragile sur dépendances complexes
- Context pruning naïf → perte d'information sur les tâches longues
- SQLite → lock contention avec 8 workers concurrents

---

## 16. Switchboard

### Architecture interne réelle

**Fichiers sources lus :**
- `src/services/KanbanDatabase.ts`
- `src/services/agentPromptBuilder.ts`
- `src/services/complexityScale.ts`

**Kanban comme runtime orchestrator :**
```typescript
// Le kanban n'est PAS juste une visualisation — c'est le dispatch runtime

// Drag card vers une colonne → VS Code lit le prompt template
// + plan metadata + complexity score
// → terminal.sendText(agent_startup_command + "\n" + prompt)

// Pas de service backend : tout via VS Code terminal API
// Zero latency, zero infrastructure
```

**Routing par complexité :**
```typescript
// complexityScale.ts
// Planner agent note chaque plan : complexity score 1-10
// if score > threshold → Lead Coder (model premium)
// else              → Coder (model cheap)

// Séparation : coût ($) ≠ compétence (skill)
// Gemini Flash pour tâches simples / Opus pour architecturales
```

**Sync Google Drive :**
```typescript
// KanbanDatabase.ts
// Plan state stocké dans Google Drive (multi-machine sync)
// Pas de .md diff dans le repo → repo propre
// Intégration ClickUp/Linear : sync bidirectionnelle optionnelle
```

### Forces et faiblesses

**Forces :**
- Zero infrastructure backend → démarrage immédiat
- Kanban = state machine visuelle → status de chaque tâche au premier coup d'œil
- Routing par complexité → optimisation coût/modèle automatique
- Interop multi-provider : Copilot CLI, Gemini CLI, Cursor (paste mode)
- Google Drive sync → accessible depuis n'importe quelle machine

**Faiblesses :**
- Monitoring : pas de feedback agent → board auto-update (manuel)
- Si agent échoue silencieusement → plan reste en colonne
- Google Drive sync → latence non-déterministe, fragile offline
- Prompt generation naïf → pas d'optimisation tokens

---

## 17. Graphify

### Architecture interne réelle

**Fichiers sources lus :**
- `graphify/build.py`
- `graphify/extract.py`
- `graphify/cluster.py`
- `graphify/cache.py`

**Pipeline 3-pass :**
```python
# Pass 1 : Tree-sitter AST (déterministe, zéro LLM)
# 25+ langages supportés : Python, JS, TS, Go, Rust, Java, C++, etc.
run_tree_sitter_index_async(repo_path)
# → Extrait : fonctions, classes, imports, calls, assignments

# Pass 2 : Audio/vidéo → faster-whisper (local, domain-aware)
transcribe(video_path, prompt_from_corpus_god_nodes)
# → Transcription contextualisée par les "god nodes" du corpus

# Pass 3 : Docs/images → Claude subagents parallèles
# → Concepts + relationships + confidence tags (EXTRACTED/INFERRED/AMBIGUOUS)
```

**Tagging de confiance :**
```
EXTRACTED   → trouvé directement dans la source (certitude haute)
INFERRED    → inférence raisonnable avec score de confiance
AMBIGUOUS   → flagué pour revue humaine
```

**Caching SHA256 avec garde-fou :**
```python
# cache.py
# SHA256 par fichier → skip si inchangé
build_merge(existing_graph, new_chunks)  # safe incremental

# Shrink guard : refuse si le nouveau graphe est plus petit
# Protection contre la perte de données accidentelle
```

**Clustering Leiden :**
```python
# cluster.py — Community detection par densité d'arêtes
# Leiden ≠ K-means : pas de k fixe, détection par topologie
# God nodes = top degree, filtrés pour les vraies entités (pas les stubs)
```

### Forces et faiblesses

**Forces :**
- 2-stage pipeline (AST déterministe + LLM sémantique) → meilleur ratio précision/coût
- Shrink guard → protection contre la perte de données
- Caching SHA256 → ré-analyse uniquement les fichiers modifiés
- Intégration IDE native : hooks Claude Code + Codex + Cursor
- Réduction contexte : 71.5x moins de tokens que les fichiers bruts

**Faiblesses :**
- Coût LLM élevé pour les subagents parallèles (même avec cache)
- NetworkX in-memory → max ~100K nœuds avant dégradation perf
- Snapshot-based : pas d'analyse incrémentale en temps réel
- Setup multi-IDE nécessaire (Claude Code vs Codex vs Cursor = configs différentes)

---

## 18. CodeGraphContext

### Architecture interne réelle

**Fichiers sources lus :**
- `src/codegraphcontext/tools/tree_sitter_parser.py`
- `src/codegraphcontext/tools/graph_builder.py`
- `src/codegraphcontext/core/database.py`

**Dual-mode :** MCP server (Claude, Cursor, etc.) + CLI standalone (`cgc`)

**Types de nœuds extraits :**
```python
# Nœuds du graphe de code
- Function/Method  (params, return type, docstring)
- Class            (inheritance, fields, methods)
- Module           (package structure)
- Import           (résolu vers la source)
- Call             (from → to, avec args)
- Assignment       (variable bindings)
```

**Résolution de chaînes d'appels :**
```python
build_function_call_groups()    # Groupe les appels par fonction source
resolve_function_call()          # Trace à travers les frontières de modules
build_inheritance_and_csharp_files()  # Chaînes d'héritage
```

**Backends de graphe :**
| Backend | Caractéristiques |
|---|---|
| Neo4j | Enterprise, remote, Cypher riche |
| FalkorDB Lite | Embedded (Unix, Python 3.12+) |
| Kùzu | Embedded (Windows support, plus léger) |
| FalkorDB Remote | Cloud fallback |

**MCP integration :**
```python
# Tools exposés via MCP :
# - query_graph    → requêtes en langage naturel → Cypher (via LLM)
# - find_entity    → chercher classe/fonction/module
# - get_call_chain → tracer les appels en aval
# - watch_directory → indexation incrémentale sur changements
```

### Forces et faiblesses

**Forces :**
- MCP standard → intégration native Claude Code, Cursor, autres IDE compatibles
- `cgc watch` → indexation live sur changements de fichiers
- Support SCIP (Sourcegraph) pour les cas complexes (macros, templates)
- Abstraction DB → swap Neo4j ↔ Kùzu sans changer le code

**Faiblesses :**
- LLM → Cypher translation error-prone pour les requêtes complexes
- Tree-sitter limité sur macros/templates/génériques
- SCIP nécessite un indexeur par langage (implémentation LSP)
- Neo4j local single-user → nécessite auth pour multi-utilisateurs

---

## 19. Microsoft Agent Framework (MAF)

**Fichiers sources lus :**
- `python/packages/` (structure)
- `declarative-agents/` (CRD-like definitions)
- README MAF

**Successeur officiel d'AutoGen**, production-ready depuis 2026.

**Innovations par rapport à AutoGen :**
```python
# Graph-based workflows avec nœuds hétérogènes
workflow = Workflow()
workflow.add_agent("planner", planner_agent)
workflow.add_agent("coder", coder_agent)
workflow.add_edge("planner", "coder", condition=lambda: not_complete)
# Nœuds = agents OU fonctions déterministes (contrairement à AutoGen GroupChat)
```

**Caractéristiques distinctives :**
- Multi-language SDKs : Python + .NET avec API identique
- DevUI : replay d'exécution, inspection d'état à chaque step (time-travel debugging)
- OpenTelemetry natif → traces distribuées
- Protocol A2A (Agent-to-Agent) → interop entre agents de différents frameworks
- `ag2/` package → compatibilité migration depuis AutoGen (drop-in replacement partiel)

**Verdict :** À préférer à AutoGen pour tout nouveau projet. Le DevUI et A2A sont les deux innovations les plus importantes.

---

## 20. Autres repos

### ai-agents-for-beginners (Microsoft)
- **Type :** Cours éducatif (12+ leçons)
- **Contenu :** Microsoft Agent Framework + Azure AI Foundry Agent Service v2
- **50+ langues** de traduction automatisée
- **Verdict :** Excellent point d'entrée conceptuel. Le code utilise MAF (pas AutoGen) → actuel.

### pixel-agents (TypeScript)
- **Concept :** Extension VS Code visualisant les agents comme des personnages pixel art
- **Innovation :** Visual feedback (typing/reading/waiting) reflète l'activité réelle des agents
- **Verdict :** Exploratoire — pattern UX intéressant, pas un framework d'orchestration.

### OpenMythos (Python / PyTorch)
- **Concept :** Reconstruction théorique spéculative de l'architecture "Mythos" de Claude
- **Implémentation :** Recurrent Depth Transformer (RDT) : Prelude → Recurrent Block (loopé) → Coda
- **Insight :** `n_loops` paramètre à l'inférence → variable-depth reasoning sans ré-encoder l'input
- **Verdict :** Purement exploratoire/recherche. Architecture non validée, pas de benchmarks.

### agent-sandbox (Go / Kubernetes)
- **Concept :** CRD Kubernetes pour pods agent singleton
- **Caractéristiques :** Stable hostname, persistent storage, warm pool, lifecycle management
- **Pattern :** `SandboxClaim` → abstraction du claim de sandbox depuis un template
- **Verdict :** Exploratoire (alpha). Pattern prometteur pour K8s teams, pas encore stable.

### shannon (Go / Python / Playwright)
- **Concept :** Pentesteur IA autonome (white-box)
- **Innovation :** Code Property Graph (AST+CFG+PDG) + LLM pour SAST/business logic testing + PoC dynamique
- **Verdict :** Production-ready pour les équipes sécurité. Cas d'usage spécialisé.

### graphify, superpowers, ruflo, gas town, Design
- Repos de projets en cours ou outils internes — pas de patterns d'orchestration généralisables.

---

## 21. Patterns transversaux découverts dans le code

### 21.1 Le pattern d'activation en 3 phases (universel)

Observé dans : OpenHands, browser-use, BMAD, CrewAI, OpenAI Agents

```
Phase 1 — INITIALISATION
  └── Charger configuration (YAML/TOML)
  └── Résoudre customisation (base → team → user)
  └── Injecter contexte (skills, facts, capabilities)

Phase 2 — EXÉCUTION
  └── Préparer contexte (state, DOM, prompt, message context)
  └── Appeler LLM / exécuter action / prompter user
  └── Traiter résultats (observations / outputs / user input)

Phase 3 — FINALISATION
  └── Émettre événements (event store, logs)
  └── Persister état (checkpoint, state file, SQLite)
  └── Retourner résultat
```

### 21.2 Le pattern Monitoring Passif (browser-use, OpenHands)

Les watchdogs/analyzers n'interrompent pas la boucle principale — ils écoutent des événements et injectent des effets de bord :

```python
# Pattern watchdog event-driven (browser-use)
class CaptchaWatchdog:
    def _on_captcha_started(self, event_data, session_id):
        self._captcha_solving = True
        self._captcha_solved_event.clear()  # Bloque le step suivant
    
    async def wait_if_captcha_solving(self):
        if self._captcha_solving:
            await asyncio.wait_for(
                self._captcha_solved_event.wait(), 
                timeout=120
            )
```

### 21.3 Le pattern Merge TOML multi-couche (OpenHands, BMAD)

```
Configuration finale = base + team + user
  ├── scalars : dernière valeur gagne (override)
  ├── tables  : deep-merge (fusion récursive)
  └── arrays  : append (ou replace si keyed)
```

Ce pattern permet à chaque couche d'adapter la configuration sans dupliquer les defaults.

### 21.4 Le pattern Verbatim + Retrieval Sémantique (mempalace)

Contrairement au RAG classique qui résume les chunks, mempalace stocke verbatim ET recherche par sémantique → meilleure précision sur les requêtes spécifiques.

```
Classique : source → résumé → embedding → retrieval → résumé flou
mempalace : source → chunk verbatim → embedding → retrieval → texte exact
```

Résultat : 96.6% R@5 sur LongMemEval vs ~78% pour les résumés automatiques.

### 21.5 Le pattern CRD-Controller (kagent, agent-sandbox)

Agents comme ressources Kubernetes déclaratives → tolérance aux pannes et scaling natifs :

```yaml
# Déclaratif : l'état désiré, pas les instructions
apiVersion: kagent.dev/v1alpha2
kind: Agent
metadata:
  name: my-agent
spec:
  type: Declarative
  skills:
    refs: [ghcr.io/my-org/skill-pack:v1]
```

Le controller reconcile en continu → si le pod crash, K8s le recrée automatiquement.

---

## 22. Architectures mémoire — Analyse code

### Tableau comparatif mis à jour avec code

| Framework | Court terme | Long terme | Persistence | Multi-tenant | Verbatim |
|---|---|---|---|---|---|
| **CrewAI** | RAGStorage in-memory | SQLite/Qdrant | ✅ Cross-session | Via scope | ❌ (embeddings) |
| **OpenAI Agents** | RunState | Session protocol | ✅ JSON serialize | Via Session | ✅ |
| **LangGraph** | StateGraph channels | Checkpoints | ✅ Pregel | Via config | Via msgpack |
| **OpenHands** | EventStream queue | EventStore files | ✅ Persistent | Project-based | ✅ |
| **BMAD** | Session TOML | Fichiers MD | ✅ Cross-session | Via projet | ✅ |
| **mempalace** | N/A (retrieval only) | ChromaDB | ✅ Local | Single-machine | ✅ Verbatim |
| **Langfuse** | N/A (observabilité) | Postgres+ClickHouse | ✅ Production | ✅ projectId | ✅ input/output |

### Recommandation par besoin

```
Besoin mémoire session + reprises        → LangGraph checkpoints ou OpenAI RunState
Besoin mémoire long-terme verbatim       → mempalace
Besoin mémoire entités + graphe          → CrewAI entity memory
Besoin audit trail + replay              → OpenHands EventStore
Besoin multi-tenant distribué            → Langfuse (observabilité) + Dify (orchestration)
```

---

## 23. Sécurité — Implémentations réelles

### 23.1 Guardrails en 4 niveaux (OpenAI Agents Python)

```
Niveau 1 : InputGuardrail (agent)
  → run_in_parallel: bool = True  ← tous exécutés en parallèle
  → tripwire_triggered → STOP

Niveau 2 : OutputGuardrail (agent)
  → Vérifie la réponse finale de l'agent
  → tripwire_triggered → STOP

Niveau 3 : ToolInputGuardrail (par tool)
  → Vérifie l'entrée de chaque tool avant exécution

Niveau 4 : ToolOutputGuardrail (par tool)
  → Vérifie la sortie de chaque tool avant re-feed au LLM
```

### 23.2 Security Analyzer LLM (OpenHands)

```python
class LLMSecurityAnalyzer(SecurityAnalyzerBase):
    """Analyse chaque action via LLM pour évaluer le risque."""
    # ActionSecurityRisk : UNKNOWN(-1) / LOW(0) / MEDIUM(1) / HIGH(2)
    
    # ConfirmationPolicy :
    # - AlwaysConfirm : tout confirmer (mode conservateur)
    # - NeverConfirm  : autonomous mode (dangereux en production)
    # - ConfirmRisky  : confirmer uniquement HIGH risk
    # - LLMSecurityAnalyzer : déléguer au LLM (flexible)
```

### 23.3 Sandbox Docker (OpenHands, browser-use)

OpenHands exécute toutes les actions dans un conteneur Docker :
- Isolation complète du système hôte
- Rollback via snapshot de container
- Réseau et filesystem contrôlés

browser-use n'isole pas l'exécution → si le navigateur est compromis, l'hôte peut l'être aussi.

### 23.4 Anti-patterns de sécurité observés

```
❌ browser-use DefaultActionWatchdog 131KB — monolithique, surface d'attaque large
❌ CrewAI tool parsing regex-based — injection via réponse LLM malformée possible
❌ Octogent SQLite sans rate limiting — DoS par flood de tasks possible
❌ switchboard terminal.sendText sans validation — injection de commandes possible
```

---

## 24. Checklist de production mise à jour

### Basée sur les patterns observés dans le code réel

**Mémoire :**
```
[ ] L1 Working memory : dans le prompt (context window)
[ ] L2 Session memory : process in-memory (RunState, StateGraph)
[ ] L3 Long-term memory : persisté (SQLite, Qdrant, ChromaDB)
[ ] L4 Knowledge base : verbatim + retrieval sémantique (mempalace pattern)
[ ] Scoping de mémoire : crew/agent/task (CrewAI pattern)
[ ] Cross-session persistence : sérialisé après chaque session
```

**Exécution :**
```
[ ] Checkpoints après chaque step (LangGraph pattern)
[ ] State file pour self-piloting (repo-analysis-state.sh pattern)
[ ] Circuit breaker : max_iterations défini par agent (Octogent : 50)
[ ] Timeout LLM par step avec retry configurable
[ ] Worker pool si tâches parallèles homogènes (Octogent pattern)
```

**Sécurité :**
```
[ ] Guardrails input ET output (OpenAI pattern — 4 niveaux)
[ ] Security analyzer sur les actions dangereuses (OpenHands pattern)
[ ] Sandbox d'exécution : Docker minimum (OpenHands pattern)
[ ] Tool permissions progressives : Tier 0-4
[ ] Audit log de chaque tool call avec input/output complets
```

**Observabilité :**
```
[ ] Traces hiérarchiques (Langfuse pattern : Trace → Span → Generation)
[ ] Token counting par observation (promptTokens, completionTokens)
[ ] Cost tracking par trace (inputCost, outputCost, totalCost)
[ ] Score humain ou auto-eval sur les traces (LegacyPrismaScore pattern)
[ ] Real-time via WebSocket pour monitoring live
```

**Robustesse :**
```
[ ] Merge de configuration multi-couche (base → team → user) [OpenHands/BMAD]
[ ] Watchdogs passifs pour edge cases (browser-use pattern : 15 watchdogs)
[ ] Verbatim storage pour la mémoire critique (mempalace pattern)
[ ] Shrink guard sur les données importantes (graphify pattern)
[ ] SHA256 cache pour éviter re-traitement [graphify pattern]
```

---

## 25. Stack recommandée avec justifications code

### Stack production complète

```
┌─ ORCHESTRATION ──────────────────────────────────────────────────┐
│  LangGraph (StateGraph + Pregel + checkpoints)                    │
│  OU BMAD (SOG + micro-file steps + personas)                      │
│  Raison : durable execution, human-in-the-loop, state typé        │
└──────────────────────────────────────────────────────────────────┘

┌─ SÉCURITÉ ───────────────────────────────────────────────────────┐
│  Guardrails pattern OpenAI (4 niveaux, tripwires)                 │
│  + SecurityAnalyzer OpenHands (LLM-based risk scoring)            │
│  + Sandbox Docker pour exécution de code                          │
│  Raison : seuls frameworks avec guardrails réellement découplés   │
└──────────────────────────────────────────────────────────────────┘

┌─ MÉMOIRE ────────────────────────────────────────────────────────┐
│  L1/L2 : StateGraph channels (LangGraph) ou RunState (OpenAI)     │
│  L3 : CrewAI memory (scoped, SQLite/Qdrant, entity-aware)         │
│  L4 : mempalace (verbatim + ChromaDB, 96.6% R@5)                  │
│  Raison : couverture complète 4 niveaux avec verbatim préservé    │
└──────────────────────────────────────────────────────────────────┘

┌─ COMMUNICATION ──────────────────────────────────────────────────┐
│  Typed sockets Haystack (validation au build time)                │
│  OU Handoffs OpenAI (avec input_filter pour clean slate)          │
│  Raison : seuls patterns avec validation type-safe                 │
└──────────────────────────────────────────────────────────────────┘

┌─ COMPRESSION ────────────────────────────────────────────────────┐
│  LLMLingua v2 (si RAG avec context > 4K tokens)                   │
│  Raison : compression verbatim, 3 niveaux indépendants             │
└──────────────────────────────────────────────────────────────────┘

┌─ OBSERVABILITÉ ──────────────────────────────────────────────────┐
│  Langfuse (Trace → Span → Generation, cost tracking)              │
│  + OpenTelemetry pour distribution                                 │
│  Raison : standard de facto, schéma complet (tokens/coût/scores)  │
└──────────────────────────────────────────────────────────────────┘

┌─ DÉPLOIEMENT ────────────────────────────────────────────────────┐
│  kagent (si K8s) : CRD déclaratif + skills-as-images             │
│  Dify (si multi-tenant) : Celery + Redis Sentinel + plugins       │
│  Raison : tolérance aux pannes et GitOps                          │
└──────────────────────────────────────────────────────────────────┘

┌─ CONTEXT AUGMENTATION ───────────────────────────────────────────┐
│  CodeGraphContext (MCP) : tree-sitter + graph DB, live watch      │
│  Raison : réduction contexte LLM via graphe de dépendances        │
└──────────────────────────────────────────────────────────────────┘
```

### Stack minimale viable (startup/solo)

```
Orchestration    : BMAD ou LangGraph (selon préférence code/prose)
Mémoire          : CrewAI memory (SQLite, 0 infra)
Guardrails       : Pattern OpenAI (copier guardrail.py, pas la dépendance)
Observabilité    : Langfuse cloud (free tier)
Context          : mempalace (local-first, 0 API)
```

---

## Conclusion V2

La V2 de ce guide révèle que les différences entre frameworks ne sont pas de surface — elles sont architecturales :

| Différence | Implication |
|---|---|
| LangGraph : version-based sync | Replay exact déterministe → debug reproductible |
| OpenAI : guardrails parallèles | Vitesse + isolation → sécurité sans latence |
| CrewAI : RecallFlow ThreadPool | Recall parallèle (n embeddings × n scopes) → scalable |
| mempalace : verbatim storage | 96.6% R@5 vs ~78% pour résumés |
| Haystack : sockets typés | Erreurs au `connect()` pas au runtime → debug immédiat |
| OpenHands : EventSource tracking | Chaque événement a un `_cause` → traçabilité causale |
| kagent : skills-as-OCI-images | Réutilisation cross-équipes, versioning natif |

**La leçon transversale :** Les frameworks matures ont tous résolu le même problème — comment rendre un LLM fiable dans un contexte où il peut échouer silencieusement — par des mécanismes architecturaux distincts mais convergents.

---

*V2 basée sur lecture directe du code source. Fichiers sources lus :*
*`run.py`, `guardrail.py`, `handoffs/__init__.py`, `crew.py`, `recall_flow.py`,*
*`pregel/_algo.py`, `pipeline_base.py`, `event_store.py`, `node_factory.py`,*
*`schema.prisma`, `palace.py`, `agent_controller.go`, `prompt_compressor.py`,*
*`pool.ts`, `orchestrator.ts`, `build.py`, `cluster.py`, et ~40 autres.*
