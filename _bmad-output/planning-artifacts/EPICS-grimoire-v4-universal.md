# ÉPICS — Grimoire v4 : Universal Agent Platform

> **Référence PRD** : PRD-grimoire-v4-universal.md  
> **Brainstorm** : BRAINSTORM-GRIMOIRE-V4-UNIVERSAL.md  
> **Date** : 6 mars 2026  
> **Convention** : `G4-EP{epic}-S{story}` — T-shirt sizing (XS < 0.5j, S = 0.5-1j, M = 1-2j, L = 3-5j, XL = 5-8j)  
> **Note** : S'articule avec les épics v3 (EP01-EP15). Les épics v4 prennent les numéros EP20+.

---

## Vue d'Ensemble

```
Phase A — CORE ASYNC          Phase B — PROTOCOL LAYER      Phase C — IDE UNIVERSE
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│ EP20 Runtime Engine  │─────▶│ EP23 MCP Server      │─────▶│ EP26 IDE Adapters    │
│ EP21 LLM Pool        │      │ EP24 REST Server     │      │ EP27 Cursor Support  │
│ EP22 DAG Scheduler   │      │ EP25 PAL Contract    │      │ EP28 Multi-IDE CLI   │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                                                                       │
Phase D — CREATIVE BRIDGES    Phase E — ICEBERG UX           Phase F — HARDENING
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│ EP29 Bridge Framework│      │ EP32 Iceberg CLI     │      │ EP35 Security Layer  │
│ EP30 Godot Bridge    │      │ EP33 grimoire ask    │      │ EP36 Telemetry       │
│ EP31 Blender Bridge  │      │ EP34 Explain Mode    │      │ EP37 Benchmark Suite │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

**Dépendances critiques :**
- EP21 (LLM Pool) dépend de EP20 (Runtime Engine)
- EP22 (Scheduler) dépend de EP20 (Runtime) + EP21 (Pool)
- EP23 (MCP) dépend de EP20 (Runtime) — puisque les tools appellent le core async
- EP24 (REST) dépend de EP20 (Runtime)
- EP25 (Contract tests) dépend de EP23 + EP24
- EP26 (IDE Adapters) dépend de EP23 (MCP est le canal principal)
- EP29 (Bridge Framework) est indépendant du reste
- EP32 (Iceberg CLI) dépend de EP20 (core) — wraps le runtime
- EP35 (Security) peut démarrer en parallèle de tout

**Parallélisables immédiatement :**
- EP20 + EP29 + EP35 (Runtime, Bridge Framework, Security — indépendants)
- EP23 + EP24 (MCP + REST — même interface PAL, backends différents)
- EP30 + EP31 (Godot + Blender — bridges indépendants)
- EP26 + EP32 (IDE Adapters + CLI — pas de dépendance directe)

---

## Phase A — CORE ASYNC RUNTIME

### EP20 — Grimoire Runtime Engine (GRE)

> **Objectif** : Créer le runtime asyncio-natif avec 3 modes d'exécution et fallback automatique.  
> **Valeur** : Transforme Grimoire de "scripts CLI" en "plateforme d'exécution d'agents".  
> **Prérequis** : EP01-EP04 de la v3 (package Python + core lib)  
> **Critère de Done** : `await runtime.execute(workflow)` fonctionne dans les 3 modes.

#### G4-EP20-S01 — AsyncEventLoop base + TaskGroup structured concurrency [L]

**Description** : Créer `src/grimoire/runtime/engine.py` avec la boucle événementielle asyncio qui supporte l'exécution structurée via `TaskGroup`. Implémenter le pattern structured concurrency pour garantir qu'aucune tâche orpheline ne survit à un scope parent.

**Tâches** :
- [ ] Créer `src/grimoire/runtime/__init__.py`
- [ ] Créer `RuntimeEngine` avec `async def execute(workflow, mode="auto") -> ExecutionResult`
- [ ] Implémenter mode auto-detection : `_detect_optimal_mode(workflow) -> Mode`
- [ ] Implémenter `Mode.SIMULATED` : exécution séquentielle single-LLM avec persona switching
- [ ] Implémenter `Mode.PARALLEL` : `asyncio.TaskGroup` avec N workers locaux
- [ ] Implémenter `Mode.DISTRIBUTED` : dispatch via `MessageBus` (import conditionnel)
- [ ] Fallback chain : distributed → parallel → simulated (automatique, logué)
- [ ] Grace period sur annulation : `asyncio.shield` pour les tâches critiques (mémoire save)
- [ ] Lifecycle hooks : `on_start`, `on_step_complete`, `on_error`, `on_complete`
- [ ] Tests : 40+ tests couvrant les 3 modes, le fallback, l'annulation, les hooks

**Critères d'acceptation** :
- [ ] `await engine.execute(workflow, mode=Mode.SIMULATED)` retourne un résultat structuré
- [ ] `await engine.execute(workflow, mode=Mode.PARALLEL)` lance N tâches concurrentes
- [ ] Le fallback se déclenche automatiquement si le mode demandé n'est pas disponible
- [ ] Aucune tâche orpheline après `TaskGroup.__aexit__`
- [ ] Tests : 100% des paths

**Fichiers** :
- `src/grimoire/runtime/__init__.py`
- `src/grimoire/runtime/engine.py`
- `src/grimoire/runtime/models.py` (Mode, ExecutionResult, WorkflowStep)
- `tests/unit/runtime/test_engine.py`

---

#### G4-EP20-S02 — Message Bus async wrapper (InProcess + Redis + NATS) [L]

**Description** : Refactoriser `message-bus.py` en module Python async importable. Le bus InProcess utilise `asyncio.Queue`. Les backends Redis et NATS utilisent leurs clients async respectifs. Interface commune `MessageBus`.

**Tâches** :
- [ ] Créer `src/grimoire/runtime/bus.py`
- [ ] Interface abstraite `MessageBus` avec `send()`, `receive()`, `subscribe()`, `publish()`
- [ ] `InProcessBus` : `asyncio.Queue` par agent, `asyncio.Event` pour le signaling
- [ ] `RedisBus` : `aioredis` (optionnel) wrappant Redis Streams
- [ ] `NATSBus` : `nats-py` (optionnel) wrappant NATS JetStream
- [ ] Auto-detection : try Redis → try NATS → fallback InProcess
- [ ] Sérialisation : JSON par défaut, MessagePack optionnel
- [ ] Tests : 30+ tests (InProcess obligatoire, Redis/NATS mockés)

**Critères d'acceptation** :
- [ ] `async with InProcessBus() as bus:` fonctionne
- [ ] `await bus.send(agent="dev", msg=AgentMessage(...))` délivre au bon agent
- [ ] `async for msg in bus.subscribe("task-response"):` stream les résultats
- [ ] Fallback automatique Redis → InProcess si Redis indisponible
- [ ] Zero-dep : InProcess fonctionne sans aucune dépendance externe

---

#### G4-EP20-S03 — Agent Worker async (isolated execution context) [M]

**Description** : Refactoriser `agent-worker.py` en worker async qui tourne dans un `TaskGroup` ou comme subprocess. Chaque worker a son propre contexte (persona, mémoire, LLM connection).

**Tâches** :
- [ ] Créer `src/grimoire/runtime/worker.py`
- [ ] `AgentWorker` class avec `async def run(task: AgentTask) -> AgentResult`
- [ ] Isolation de contexte : chaque worker charge sa persona + ses learnings
- [ ] Intégration LLM Pool : worker `await pool.acquire()` au démarrage
- [ ] Heartbeat : le worker émet un heartbeat périodique sur le bus
- [ ] Graceful shutdown : `asyncio.CancelledError` → save state → exit clean
- [ ] Tests : 25+ tests

**Critères d'acceptation** :
- [ ] Un worker peut exécuter une tâche agent isolément
- [ ] Le worker relâche sa connexion LLM à la fin de la tâche
- [ ] Le heartbeat est émis et observable via le bus

---

### EP21 — LLM Pool (Multi-Provider Connection Pooling)

> **Objectif** : Pool de connexions LLM avec routing intelligent, rate limiting, circuit breaker, et cost tracking.  
> **Valeur** : Permet le vrai multi-LLM : chaque agent utilise le LLM optimal pour sa tâche.  
> **Critère de Done** : `connection = await pool.acquire(tier="high", task="coding")` retourne une connexion du meilleur provider disponible.

#### G4-EP21-S01 — LLM Provider abstraction + Copilot/Anthropic/OpenAI backends [L]

**Description** : Créer l'interface `LLMProvider` et les implémentations pour les 5 providers principaux : Copilot (via IDE LSP), Anthropic (API directe), OpenAI (API directe), Ollama (local), OpenRouter (proxy).

**Tâches** :
- [ ] Créer `src/grimoire/llm/__init__.py`
- [ ] Interface abstraite `LLMProvider` : `connect()`, `complete()`, `stream()`, `disconnect()`
- [ ] `CopilotProvider` : utilise le LSP de l'IDE (quand disponible)
- [ ] `AnthropicProvider` : `aiohttp` vers `api.anthropic.com`
- [ ] `OpenAIProvider` : `aiohttp` vers `api.openai.com`
- [ ] `OllamaProvider` : `aiohttp` vers `localhost:11434`
- [ ] `OpenRouterProvider` : `aiohttp` vers `openrouter.ai`
- [ ] Chaque provider : retry avec exponential backoff, timeout configurable
- [ ] Tests : 40+ tests (providers mockés, pas de vrais appels API)

**Critères d'acceptation** :
- [ ] Chaque provider respecte l'interface `LLMProvider`
- [ ] Les providers se construisent depuis la configuration YAML
- [ ] Zero-dep pour Copilot (utilise subprocess/LSP). Optional deps pour les autres.

---

#### G4-EP21-S02 — Connection Pool + Rate Limiter + Circuit Breaker [L]

**Description** : Implémenter le pool de connexions avec gestion de la concurrence, rate limiting par provider, et circuit breaker.

**Tâches** :
- [ ] `LLMPool` : pool `asyncio.Semaphore`-based par provider
- [ ] `acquire(tier, task_type)` → sélectionne le meilleur provider disponible
- [ ] `release(connection)` → retourne la connexion dans le pool
- [ ] Rate Limiter : `TokenBucketRateLimiter` par provider (configurable)
- [ ] Circuit Breaker : 3 failures → OPEN (30s) → HALF-OPEN (1 tentative) → CLOSED
- [ ] Fallback chain : si provider A est OPEN → essayer B → C → ...
- [ ] Cost tracker : compteur de tokens estimés par provider → alerte budget
- [ ] Tests : 35+ tests

**Critères d'acceptation** :
- [ ] N workers peuvent `acquire()` en parallèle sans deadlock
- [ ] Le rate limiter bloque (await) quand la limite est atteinte
- [ ] Le circuit breaker s'ouvre après 3 échecs et basculle sur le fallback
- [ ] Le cost tracker émet un warning à 80% du budget daily

---

#### G4-EP21-S03 — Task Classifier + Model Router intelligent [M]

**Description** : Intégrer le `llm-router.py` existant comme module du LLM Pool. Le router classifie chaque tâche (trivial/standard/complex/expert) et sélectionne le modèle optimal.

**Tâches** :
- [ ] Refactoriser `llm-router.py` → `src/grimoire/llm/router.py`
- [ ] `classify(prompt, agent) -> TaskClassification`
- [ ] `route(classification) -> ModelSpec` utilisant la config provider
- [ ] Intégration avec `LLMPool.acquire()` : le pool utilise le router automatiquement
- [ ] Stats d'utilisation : quel modèle pour quel type de tâche, coût moyen
- [ ] Tests : 20+ tests

---

### EP22 — DAG Scheduler (Dependency-Aware Task Scheduling)

> **Objectif** : Scheduler qui parse un workflow en DAG, identifie les tâches parallélisables, et les dispatch de manière optimale.  
> **Valeur** : Permet l'exécution intelligente — parallèle quand possible, séquentielle quand nécessaire.  
> **Critère de Done** : `schedule = scheduler.plan(workflow)` retourne un plan avec les batchs parallèles identifiés.

#### G4-EP22-S01 — DAG Builder + Critical Path Analysis [M]

**Description** : Parser les workflows (YAML ou code) en DAG (Directed Acyclic Graph). Identifier le chemin critique, les tâches parallélisables, et les dépendances.

**Tâches** :
- [ ] Créer `src/grimoire/runtime/scheduler.py`
- [ ] `DAGBuilder` : parse un workflow → `DAG` (nœuds = tâches, arêtes = dépendances)
- [ ] `DAG.parallel_batches()` → iterator de batches exécutables en parallèle
- [ ] `DAG.critical_path()` → chemin le plus long (bottleneck)
- [ ] Détection de cycles → erreur explicite
- [ ] Visualisation Mermaid : `dag.to_mermaid()` pour debug
- [ ] Tests : 25+ tests

---

#### G4-EP22-S02 — Smart Scheduler (dynamic dispatch + opportunistic execution) [L]

**Description** : Le scheduler dispatch les tâches du DAG vers les workers. Supporte l'exécution opportuniste : si un worker libre peut démarrer une tâche avec des résultats partiels, il le fait.

**Tâches** :
- [ ] `Scheduler` : consomme un `DAG` + `RuntimeEngine` + `LLMPool`
- [ ] `async def run(dag) -> ScheduleResult` : exécute le DAG
- [ ] Dispatch batch-par-batch : chaque batch parallélisé via `TaskGroup`
- [ ] Opportunistic execution : si une tâche a 80%+ de ses dépendances résolues → start early
- [ ] Timeout par tâche + timeout global
- [ ] Re-scheduling : si un worker échoue → retry sur un autre
- [ ] Progress reporting : callback `on_progress(completed, total, current_batch)`
- [ ] Tests : 30+ tests

---

## Phase B — PROTOCOL ADAPTER LAYER (PAL)

### EP23 — MCP Server (Tier 1 Protocol)

> **Objectif** : Implémenter un vrai serveur MCP Python qui expose les tools Grimoire.  
> **Valeur** : Tout IDE MCP-compatible obtient Grimoire nativement.  
> **Critère de Done** : `grimoire serve --mcp` lance un serveur MCP stdio fonctionnel testable dans Claude Desktop.

#### G4-EP23-S01 — MCP Server core (stdio transport) [L]

**Description** : Implémenter un serveur MCP utilisant le SDK officiel `mcp` (Python). Transport stdio pour usage IDE local.

**Tâches** :
- [ ] Créer `src/grimoire/server/mcp_adapter.py`
- [ ] Utiliser `mcp.server.Server` (SDK officiel Anthropic)
- [ ] Exposer les tools Tier 1 : `get_project_context`, `remember`, `recall`, `run_cc`, `list_tools`, `ask_agent`
- [ ] Exposer les resources MCP : `project-context`, `agent-memory/{agent}`, `workflow-status`
- [ ] Exposer les prompts MCP : `activate-agent`, `run-workflow`, `party-mode`
- [ ] Transport stdio : `mcp.server.stdio.stdio_server()`
- [ ] Tests : 30+ tests (mock MCP protocol)

**Critères d'acceptation** :
- [ ] `grimoire serve --mcp` lance le serveur sans erreur
- [ ] Claude Desktop peut appeler `get_project_context` et recevoir le JSON
- [ ] VS Code MCP peut lister les tools et les appeler
- [ ] Les resources sont accessibles via `mcp://`

---

#### G4-EP23-S02 — MCP SSE transport (multi-client) [M]

**Description** : Ajouter le transport SSE (Server-Sent Events) au serveur MCP pour le multi-client simultané (plusieurs IDE connectés au même serveur).

**Tâches** :
- [ ] Implémenter SSE transport via `aiohttp` ou `starlette`
- [ ] Support multi-client : N IDE peuvent se connecter simultanément
- [ ] Session management : chaque client a son contexte
- [ ] Graceful reconnection : SSE auto-reconnect
- [ ] Tests : 15+ tests

---

#### G4-EP23-S03 — MCP Tools dynamiques (auto-discovery depuis tool-registry) [M]

**Description** : Au lieu d'hardcoder les tools, le serveur MCP auto-découvre les outils disponibles via `tool-registry.py` et les expose dynamiquement.

**Tâches** :
- [ ] Intégrer `tool-registry.py` (refactorisé en module)
- [ ] Au startup : scanner `framework/tools/` → construire les schemas MCP
- [ ] Hot-reload : si un outil est ajouté/modifié → refresh sans restart
- [ ] Filtrage : config YAML pour whitelist/blacklist d'outils exposés
- [ ] Tests : 15+ tests

---

### EP24 — REST Server (Tier 1 Protocol, Enterprise Fallback)

> **Objectif** : API REST HTTP avec auth JWT — le fallback pour les entreprises qui refusent MCP.  
> **Valeur** : Grimoire accessible depuis N'IMPORTE QUEL client HTTP (curl, Postman, CI/CD, scripts).  
> **Critère de Done** : `grimoire serve --rest` expose une API REST documentée avec Swagger.

#### G4-EP24-S01 — REST API core (FastAPI + JWT auth) [L]

**Description** : Implémenter l'API REST via FastAPI (optionnel, fallback stdlib HTTPServer si FastAPI absent).

**Tâches** :
- [ ] Créer `src/grimoire/server/rest_adapter.py`
- [ ] Routes : `POST /api/v1/tools/{tool_name}`, `GET /api/v1/context`, `POST /api/v1/memory/remember`, `GET /api/v1/memory/recall`, `POST /api/v1/agent/{agent_id}/ask`
- [ ] Auth : JWT bearer token (configurable, désactivable pour dev)
- [ ] Swagger auto-documentation : `/docs` (FastAPI natif)
- [ ] Rate limiting : par IP et par token
- [ ] CORS configurable
- [ ] Fallback : si FastAPI absent → `http.server` stdlib minimal (read-only)
- [ ] Tests : 35+ tests

**Critères d'acceptation** :
- [ ] `curl -H "Authorization: Bearer <token>" http://localhost:9473/api/v1/context` retourne le JSON
- [ ] Swagger UI accessible sur `/docs`
- [ ] Rate limiter bloque après N requêtes/minute
- [ ] Fonctionne en mode stdlib si FastAPI n'est pas installé (dégradé mais fonctionnel)

---

#### G4-EP24-S02 — WebSocket streaming (temps réel) [M]

**Description** : Ajouter un endpoint WebSocket pour le streaming temps réel des résultats d'agents, des events ELSS, et du progress des workflows.

**Tâches** :
- [ ] Route WS : `ws://localhost:9473/ws/v1/stream`
- [ ] Channels : `agent-output`, `workflow-progress`, `events`, `dashboard`
- [ ] Client peut s'abonner à des channels spécifiques
- [ ] Heartbeat WebSocket pour détection déconnexion
- [ ] Tests : 15+ tests

---

### EP25 — PAL Contract Testing

> **Objectif** : Suite de tests contractuels que TOUT protocol adapter doit passer.  
> **Valeur** : Garantie que MCP, REST, et tout futur adapter offrent la même expérience.  
> **Critère de Done** : `pytest tests/contract/` passe pour MCP ET REST avec le même résultat.

#### G4-EP25-S01 — Définir la suite de tests contractuels [M]

**Description** : Créer une suite de 50+ tests qui vérifient les fonctionnalités core via une interface abstraite `ProtocolClient`. Chaque adapter fournit son propre `ProtocolClient`.

**Tâches** :
- [ ] Créer `tests/contract/test_protocol_contract.py`
- [ ] Interface `ProtocolClient` : `call_tool(name, params)`, `get_resource(uri)`, `list_tools()`
- [ ] `MCPClient(ProtocolClient)` : appelle via le protocole MCP
- [ ] `RESTClient(ProtocolClient)` : appelle via HTTP
- [ ] 50+ tests paramétrés : chaque test s'exécute avec chaque client
- [ ] Catégories : tools, resources, auth, errors, streaming, concurrent

**Critères d'acceptation** :
- [ ] Même test, même résultat via MCP et REST
- [ ] Si un nouvel adapter est ajouté, il suffit d'implémenter `ProtocolClient`

---

## Phase C — IDE UNIVERSE

### EP26 — IDE Adapter Framework

> **Objectif** : Créer le framework d'adaptation multi-IDE avec génération de fichiers de configuration.  
> **Valeur** : `grimoire ide setup --ide <name>` configure n'importe quel IDE en une commande.  
> **Critère de Done** : Setup fonctionnel pour VS Code, Cursor, et Claude Desktop.

#### G4-EP26-S01 — IDEAdapter interface + VS Code adapter [M]

**Description** : Créer l'interface `IDEAdapter` et l'implémentation pour VS Code.

**Tâches** :
- [ ] Créer `src/grimoire/ide/__init__.py`
- [ ] Interface `IDEAdapter` : `generate_config()`, `supports_mcp()`, `supports_agents()`, `detect() -> bool`
- [ ] `VSCodeAdapter` : génère `.github/copilot-instructions.md`, `.vscode/mcp.json`, `.github/skills/`
- [ ] Le contenu de `copilot-instructions.md` est généré DYNAMIQUEMENT depuis la config projet
- [ ] Les skills sont copiés depuis les templates Grimoire
- [ ] Auto-detection : cherche `.vscode/` ou `code` dans PATH
- [ ] Tests : 20+ tests

---

#### G4-EP26-S02 — Claude Desktop adapter [S]

**Description** : Adapter pour Claude Desktop — configuration MCP dans `claude_desktop_config.json`.

**Tâches** :
- [ ] `ClaudeDesktopAdapter` : modifie/crée `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) ou `~/.config/claude/claude_desktop_config.json` (Linux)
- [ ] Ajoute l'entrée Grimoire MCP server dans la config
- [ ] Auto-detect Claude Desktop installé
- [ ] Tests : 10+ tests

---

### EP27 — Cursor Deep Integration

> **Objectif** : Support Cursor first-class — rules, MCP, composer prompts.  
> **Valeur** : Cursor est l'IDE IA le plus populaire (2026). L'intégration doit être parfaite.  
> **Critère de Done** : `grimoire ide setup --ide cursor` → projet Grimoire fonctionnel dans Cursor en 30 secondes.

#### G4-EP27-S01 — Cursor adapter (rules + MCP + composer) [M]

**Description** : Adapter Cursor complet.

**Tâches** :
- [ ] `CursorAdapter` : génère `.cursor/rules/grimoire.mdc` (rules Cursor format)
- [ ] Génère `.cursor/mcp.json` pointant vers `grimoire serve --mcp`
- [ ] Génère des composer prompts pour les workflows fréquents
- [ ] Le `.cursorrules` global pointant vers les rules générées
- [ ] Mapping des features VS Code → Cursor (skills → rules, modes → agents)
- [ ] Auto-detect Cursor installé
- [ ] Documentation : guide "Grimoire + Cursor en 5 minutes"
- [ ] Tests : 15+ tests

---

#### G4-EP27-S02 — Windsurf + Cline adapters [S]

**Description** : Adapters légers pour Windsurf et Cline (forks/extensions VS Code).

**Tâches** :
- [ ] `WindsurfAdapter` : génère `.windsurfrules` + MCP config
- [ ] `ClineAdapter` : génère `.clinerules` + MCP config via VS Code
- [ ] Tests : 10+ tests chacun

---

### EP28 — Multi-IDE CLI + Détection Automatique

> **Objectif** : `grimoire ide` comme commande unifiée pour la gestion multi-IDE.  
> **Critère de Done** : `grimoire ide detect` trouve tous les IDE installés et propose la configuration.

#### G4-EP28-S01 — IDE detection + setup wizard [M]

**Description** : Détection automatique des IDE installés et wizard de configuration.

**Tâches** :
- [ ] `grimoire ide detect` : scanne le système pour les IDE connus
- [ ] `grimoire ide setup --ide <name>` : configure l'IDE sélectionné
- [ ] `grimoire ide setup --all` : configure tous les IDE détectés
- [ ] `grimoire ide status` : vérifie la santé de la configuration de chaque IDE
- [ ] `grimoire ide update` : met à jour les configs (ex: après ajout d'agent)
- [ ] Wizard interactif si `--ide` non spécifié : propose les IDE détectés
- [ ] Tests : 20+ tests

---

#### G4-EP28-S02 — IntelliJ + Neovim + Zed adapters [L]

**Description** : Adapters Tier Silver pour IntelliJ, Neovim, et Zed.

**Tâches** :
- [ ] `IntelliJAdapter` : génère config MCP plugin + `.idea/grimoire.xml`
- [ ] `NeovimAdapter` : génère `.nvim/grimoire.lua` + MCP config
- [ ] `ZedAdapter` : génère `.zed/settings.json` MCP entry
- [ ] Chaque adapter : instructions d'installation du plugin MCP si nécessaire
- [ ] Tests : 10+ tests par adapter

---

## Phase D — CREATIVE BRIDGES

### EP29 — Creative Bridge Framework

> **Objectif** : Interface commune pour connecter des outils créatifs (Godot, Blender, etc.) à Grimoire.  
> **Valeur** : Ouvre le marché gamedev, 3D, design — AUCUN concurrent ne fait ça.  
> **Critère de Done** : `CreativeBridge` interface implémentée + `mcp-proxy` étendu.

#### G4-EP29-S01 — CreativeBridge interface + MCP proxy extension [M]

**Description** : Définir l'interface `CreativeBridge` et étendre `mcp-proxy.py` pour router vers les bridges créatifs.

**Tâches** :
- [ ] Créer `src/grimoire/bridges/__init__.py`
- [ ] Interface `CreativeBridge` : `connect()`, `execute(action, params)`, `capabilities()`, `health_check()`
- [ ] `BridgeResult` dataclass : `success`, `output`, `artifacts`, `errors`
- [ ] `BridgeRegistry` : registre de bridges disponibles
- [ ] Extension `mcp-proxy.py` : si tool call = bridge → route vers le bridge
- [ ] Configuration YAML : `bridges:` section dans `grimoire.yaml`
- [ ] Tests : 20+ tests

---

#### G4-EP29-S02 — Agent archetypes créatifs (templates) [M]

**Description** : Créer des templates d'agents spécialisés pour les outils créatifs.

**Tâches** :
- [ ] Archétype `creative-studio` enrichi avec agents par outil
- [ ] `godot-expert.md` : agent spécialisé GDScript, scènes, shaders, TileMap
- [ ] `blender-expert.md` : agent spécialisé bpy, modélisation, texturing, animation
- [ ] `unity-expert.md` : agent spécialisé C#, MonoBehaviour, scenes
- [ ] `figma-expert.md` : agent spécialisé design system, composants, auto-layout
- [ ] `pixel-artist.md` : agent spécialisé pixel art, spritesheets, animation 2D
- [ ] Chaque agent : context_budget, tools_required, best_practices
- [ ] Tests : validation des templates (structure, champs requis)

---

### EP30 — Godot Bridge

> **Objectif** : Connecter Grimoire à Godot 4 — les agents peuvent créer des scènes, écrire du GDScript, manipuler des nodes.  
> **Critère de Done** : `await godot.execute("create_scene", {...})` crée une scène dans un projet Godot.

#### G4-EP30-S01 — Godot MCP bridge (via godot-mcp existant + fallback CLI) [L]

**Description** : Bridge vers Godot 4 utilisant godot-mcp (communautaire) comme backend principal, avec fallback CLI Godot.

**Tâches** :
- [ ] `GodotBridge(CreativeBridge)` : implémentation complète
- [ ] Mode MCP : proxy vers `godot-mcp` server si installé
- [ ] Mode CLI : utilise `godot --headless --script` pour exécuter des scripts GDScript
- [ ] Mode FileGen : génère des fichiers `.tscn` et `.gd` directement (sans Godot lancé)
- [ ] Actions supportées : `create_scene`, `add_node`, `set_property`, `connect_signal`, `generate_script`, `export_project`
- [ ] Validation : vérifie que les node types existent, que les properties sont valides
- [ ] Package séparé : `pip install grimoire-bridge-godot`
- [ ] Tests : 25+ tests

---

#### G4-EP30-S02 — GDScript generator + Godot best practices [M]

**Description** : Module de génération GDScript idiomatique avec les best practices Godot 4.

**Tâches** :
- [ ] Templates GDScript pour les patterns courants (movement, AI, UI, networking)
- [ ] Linter GDScript basique : détecte les anti-patterns courants
- [ ] Documentation des best practices Godot 4 dans le context_budget de l'agent
- [ ] Tests : 15+ tests

---

### EP31 — Blender Bridge

> **Objectif** : Connecter Grimoire à Blender — les agents peuvent modéliser, texturer, animer.  
> **Critère de Done** : `await blender.execute("create_mesh", {...})` crée un mesh dans Blender.

#### G4-EP31-S01 — Blender bpy bridge (Python socket + fallback CLI) [L]

**Description** : Bridge vers Blender 4 utilisant bpy (Python API de Blender) via socket ou CLI.

**Tâches** :
- [ ] `BlenderBridge(CreativeBridge)` : implémentation complète
- [ ] Mode Socket : communication avec Blender via Python socket (addon Blender côté serveur)
- [ ] Mode CLI : `blender --background --python script.py` pour le headless
- [ ] Mode MCP : via `blender-mcp` si installé
- [ ] Actions : `create_mesh`, `add_material`, `set_keyframe`, `render`, `export`
- [ ] Script generator : traduit les actions en scripts bpy idiomatiques
- [ ] Package séparé : `pip install grimoire-bridge-blender`
- [ ] Tests : 25+ tests

---

## Phase E — ICEBERG UX

### EP32 — Iceberg CLI (Progressive Disclosure)

> **Objectif** : CLI à 3 niveaux de profondeur — surface, power, expert.  
> **Valeur** : Onboarding en 60 secondes. Pas besoin de lire 43 docs.  
> **Critère de Done** : `grimoire init && grimoire status` fonctionne pour un débutant. `grimoire expert` déverrouille tout pour un expert.

#### G4-EP32-S01 — Surface CLI (init, status, ask) [M]

**Description** : Les 3 commandes de surface qui suffisent pour 80% des utilisateurs.

**Tâches** :
- [ ] `grimoire init [--auto] [--archetype <name>]` : bootstrap projet
- [ ] `grimoire status` : dashboard ASCII compact (santé, agents, mémoire, dernière action)
- [ ] `grimoire ask "question"` : route vers le bon agent via le SOG et retourne la réponse
- [ ] Output coloré, clair, avec emojis pertinents
- [ ] `--json` flag pour output machine-readable
- [ ] Tests : 15+ tests

---

#### G4-EP32-S02 — Power CLI (agent, workflow, memory, tool, serve, ide) [L]

**Description** : Les 15 commandes power user.

**Tâches** :
- [ ] `grimoire agent list|forge|bench|info`
- [ ] `grimoire workflow run|list|status`
- [ ] `grimoire memory search|add|status`
- [ ] `grimoire tool <name> [args]`
- [ ] `grimoire serve [--mcp] [--rest] [--port N]`
- [ ] `grimoire ide setup|detect|status`
- [ ] `grimoire bridge add|list|status`
- [ ] `grimoire party` (shortcut party mode)
- [ ] `grimoire dream` (shortcut dream mode)
- [ ] `grimoire doctor` (diagnostic complet)
- [ ] `grimoire explain <command>` (explique ce que fait une commande sous le capot)
- [ ] Tab completion (zsh + bash + fish)
- [ ] Tests : 30+ tests

---

#### G4-EP32-S03 — Expert CLI (unlock all tools) [S]

**Description** : `grimoire expert` déverrouille l'accès direct aux 87+ outils.

**Tâches** :
- [ ] `grimoire expert` : affiche un message et déverrouille les commandes avancées
- [ ] `grimoire tool <name> --help` : aide de chaque outil
- [ ] `grimoire tool list --verbose` : liste tous les outils avec description
- [ ] Auto-completion pour les noms d'outils
- [ ] Tests : 10+ tests

---

### EP33 — `grimoire ask` (Interface Conversationnelle)

> **Objectif** : L'utilisateur parle au Grimoire en langage naturel. Le SOG route vers le bon agent.  
> **Valeur** : L'ultime simplification. Pas besoin de connaître les commandes.  
> **Critère de Done** : `grimoire ask "comment améliorer les perfs de mon API"` → réponse structurée du bon agent.

#### G4-EP33-S01 — Intent routing + agent dispatch via CLI [L]

**Description** : `grimoire ask` analyse l'intention, route vers le bon agent, et retourne la réponse.

**Tâches** :
- [ ] Parser l'intention (reuse Intention Analyzer du SOG)
- [ ] Router vers l'agent optimal (reuse du Route Engine)
- [ ] Enrichir le prompt (reuse du Prompt Enricher)
- [ ] Appeler le LLM Pool pour obtenir la réponse
- [ ] Formatter la sortie (Markdown dans le terminal)
- [ ] Mode interactif : `grimoire ask` sans argument → mode chat REPL
- [ ] Mode pipe : `echo "question" | grimoire ask` pour les scripts
- [ ] Tests : 20+ tests

---

### EP34 — Explain Mode (Transparency Toggle)

> **Objectif** : Chaque commande peut être "expliquée" — montrer ce qui se passe sous le capot.  
> **Valeur** : La complexité est packagée mais jamais cachée. L'utilisateur curieux voit tout.

#### G4-EP34-S01 — --explain flag + grimoire explain <command> [M]

**Description** : Ajouter un mode explication à chaque commande.

**Tâches** :
- [ ] Flag `--explain` sur toutes les commandes : affiche les étapes internes
- [ ] `grimoire explain init` : explique ce que fait `init` sans l'exécuter
- [ ] `grimoire explain ask` : montre le pipeline SOG (intention → routing → enrichment → LLM → response)
- [ ] Format : numéroté, avec les fichiers touchés et les outils appelés
- [ ] Tests : 10+ tests

---

## Phase F — HARDENING

### EP35 — Security Layer

> **Objectif** : Auth, sandbox, RBAC agents, audit trail complet.  
> **Valeur** : Obligatoire pour l'adoption enterprise. Sans ça, les DSI bloquent.  
> **Critère de Done** : Les endpoints REST sont protégés par JWT. Les tools s'exécutent dans un sandbox.

#### G4-EP35-S01 — JWT Auth layer pour REST adapter [M]

**Description** : Auth JWT pour l'API REST.

**Tâches** :
- [ ] Génération de JWT : `grimoire auth token --user <name> --ttl 3600`
- [ ] Validation JWT sur chaque requête REST
- [ ] API keys comme alternative à JWT
- [ ] Refresh token flow
- [ ] Rate limiting par token
- [ ] Tests : 20+ tests

---

#### G4-EP35-S02 — Tool Sandbox (subprocess isolation) [M]

**Description** : Les outils CLI s'exécutent dans un subprocess avec restrictions.

**Tâches** :
- [ ] `Sandbox` class : wraps `asyncio.create_subprocess_exec` avec restrictions
- [ ] Timeout configurable par outil
- [ ] Whitelist de commandes (configurée dans `grimoire.yaml`)
- [ ] Filesystem scope : accès limité au `${PROJECT_ROOT}` (pas de `../../etc/passwd`)
- [ ] Network access : désactivé par défaut (opt-in par outil)
- [ ] Resource limits : mémoire max, CPU max (via `ulimit` ou cgroups)
- [ ] Tests : 25+ tests

---

#### G4-EP35-S03 — Agent RBAC (Role-Based Access Control) [M]

**Description** : Chaque agent a des permissions déclaratives.

**Tâches** :
- [ ] Schema permissions dans `grimoire.yaml` : `file_write`, `file_read`, `execute`, `bridges`, `memory_write`
- [ ] Enforcement : le runtime vérifie les permissions AVANT chaque action
- [ ] Audit : chaque dépassement de permission est logué dans BMAD_TRACE
- [ ] Default : permissions raisonnables par rôle (dev = write src/, qa = read only, etc.)
- [ ] Tests : 20+ tests

---

### EP36 — Telemetry & Observability

> **Objectif** : Dashboard temps réel de l'activité des agents.  
> **Valeur** : Voir ce que font les agents, combien ça coûte, et où sont les bottlenecks.

#### G4-EP36-S01 — Structured logging + OpenTelemetry spans [M]

**Description** : Logging structuré JSON + export OpenTelemetry optionnel.

**Tâches** :
- [ ] Logging structuré : chaque événement = JSON avec `agent`, `action`, `duration`, `cost`
- [ ] OpenTelemetry spans : optionnel, pour les utilisateurs avec Grafana/Jaeger
- [ ] BMAD_TRACE enrichi : append-only, compatible avec le format existant
- [ ] Export : `grimoire telemetry export --format json|otlp|csv`
- [ ] Tests : 15+ tests

---

#### G4-EP36-S02 — Terminal dashboard (live TUI) [M]

**Description** : `grimoire dashboard` affiche un TUI (Text User Interface) temps réel.

**Tâches** :
- [ ] Utiliser `rich` ou `textual` (optionnel) pour le TUI
- [ ] Panneaux : agents actifs, workflow progress, LLM usage, cost tracker, events
- [ ] Refresh auto (WebSocket ou polling)
- [ ] Fallback ASCII si `rich`/`textual` non installé
- [ ] Tests : 10+ tests

---

### EP37 — Benchmark Suite

> **Objectif** : Suite de benchmarks publics pour mesurer et comparer les performances des agents Grimoire.  
> **Valeur** : Crédibilité, reproductibilité, amélioration continue objective.

#### G4-EP37-S01 — Agent benchmark framework [L]

**Description** : Framework de benchmarking avec scénarios standardisés.

**Tâches** :
- [ ] Scénarios : coding (SWE-Bench style), architecture review, bug fixing, documentation
- [ ] Métriques : accuracy, latency, cost, trust score, CC pass rate
- [ ] Runner : `grimoire bench run --scenario coding --agent dev`
- [ ] Comparaison : `grimoire bench compare --agents dev,architect`
- [ ] Export : rapport Markdown + JSON
- [ ] Intégration `agent-bench.py` existant
- [ ] Tests : 20+ tests

---

#### G4-EP37-S02 — Leaderboard + publicité des résultats [S]

**Description** : Leaderboard des agents par scénario, exportable pour README/site.

**Tâches** :
- [ ] `grimoire bench leaderboard` : affiche le classement
- [ ] Export Markdown pour README
- [ ] Historique des benchmarks (tracking progression)
- [ ] Badge de score pour README : `![Agent Score](badge.svg)`
- [ ] Tests : 10+ tests

---

## Résumé Chiffré

| Phase | Épics | Stories | Estimation cumulative | Tests estimés |
|---|---|---|---|---|
| A — Core Async | 3 (EP20-22) | 8 | XL cumulé | ~250 tests |
| B — Protocol Layer | 3 (EP23-25) | 6 | XL cumulé | ~160 tests |
| C — IDE Universe | 3 (EP26-28) | 5 | L cumulé | ~85 tests |
| D — Creative Bridges | 3 (EP29-31) | 5 | L cumulé | ~110 tests |
| E — Iceberg UX | 3 (EP32-34) | 6 | L cumulé | ~95 tests |
| F — Hardening | 3 (EP35-37) | 7 | L cumulé | ~130 tests |
| **TOTAL** | **18 épics** | **37 stories** | | **~830 nouveaux tests** |

Score total après v4 : **3177 + 830 = ~4000 tests**

---

## Ordre d'Exécution Recommandé

```
Semaine 1-2:  EP20 (Runtime) + EP35 (Security) en parallèle
Semaine 3-4:  EP21 (LLM Pool) + EP29 (Bridge Framework) en parallèle
Semaine 5-6:  EP22 (Scheduler) + EP23 (MCP Server) en parallèle
Semaine 7-8:  EP24 (REST) + EP26 (IDE Adapters) en parallèle
Semaine 9-10: EP25 (Contract Tests) + EP27 (Cursor) + EP32 (Iceberg CLI)
Semaine 11-12: EP30 (Godot) + EP31 (Blender) en parallèle
Semaine 13-14: EP33 (ask) + EP34 (explain) + EP28 (Multi-IDE)
Semaine 15-16: EP36 (Telemetry) + EP37 (Benchmark) + polish

Critical path: EP20 → EP21 → EP22 → EP23 → EP25
```

---

## Relation avec les Épics v3

Les épics v3 (EP01-EP15) restent valides et sont les **prérequis** de v4 :
- **EP01 (Package Python)** → requis par TOUT v4
- **EP02 (Config)** → requis par EP23, EP24, EP26
- **EP04 (Core Lib)** → requis par EP20
- **EP07 (CLI Typer)** → requis par EP32
- **EP08 (MCP Server v3)** → SUPERSÉDÉ par EP23 (version enrichie)

La v4 n'annule pas la v3, elle l'ÉTEND. Les fondations v3 sont les rails sur lesquels la v4 roule.
