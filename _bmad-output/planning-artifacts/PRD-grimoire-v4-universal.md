# PRD — Grimoire v4 : Universal Agent Platform

> **Statut** : Draft v1 — 6 mars 2026  
> **Auteur** : John (PM) + Winston (Architect) + Amelia (Dev) — orchestrés par SOG  
> **Version cible** : 4.0.0  
> **Précédent** : PRD-bmad-kit-v3-platform.md (en cours)  
> **Nom de code** : **Nexus**  
> **Brainstorm** : BRAINSTORM-GRIMOIRE-V4-UNIVERSAL.md

---

## 1. Vision

> **Grimoire est le système nerveux universel de l'IA agentique** : une plateforme qui connecte n'importe quel IDE, n'importe quel outil créatif, n'importe quel LLM, et n'importe quel protocole — avec le système de guardrails le plus avancé de l'industrie.

**En une phrase** : Si un outil accepte du texte, une API ou un protocole standard, Grimoire peut s'y brancher et y déployer des agents intelligents.

---

## 2. Principes Directeurs

### P1 — Protocol-Agnostic, Not Protocol-Exclusive
Grimoire ne dépend d'aucun protocole spécifique. MCP est le protocole par défaut, mais REST, LSP, gRPC, WebSocket, CLI pipes et SDK Python sont des citoyens de première classe. Une entreprise qui refuse MCP obtient la même expérience via REST.

### P2 — Packaged Complexity (Iceberg Architecture)
La complexité est la valeur. Mais elle est empaquetée en couches progressives :
- **Surface** (3 commandes) : suffisant pour 80% des utilisateurs
- **Power** (15 commandes) : pour les power users
- **Expert** (87+ outils) : pour les experts
- **SDK** (Python import) : pour les agent builders
Chaque couche est auto-suffisante. La découverte est progressive, jamais forcée.

### P3 — IDE-Agnostic, IDE-Optimized
Grimoire fonctionne dans n'importe quel IDE via MCP/REST. Mais pour les IDE Tier Gold (VS Code, Cursor, Claude Desktop), l'intégration est native et optimisée — fichiers de configuration pré-générés, extensions dédiées, prompts systèmes adaptés.

### P4 — Async-Native, Graceful Degradation
Le runtime est asyncio-natif avec 3 modes (simulated, parallel-local, distributed). Le fallback est automatique et transparent : si Redis n'est pas disponible → InProcess. Si le LLM rate-limite → queue et retry. Le système ne casse JAMAIS.

### P5 — Plug Anything (Creative Bridge)
Tout outil qui offre une API (Python, REST, CLI, MCP) peut être branché via le Creative Bridge. Un agent Grimoire spécialisé peut alors COMMANDER cet outil — pas juste en parler.

### P6 — Agent-First (les agents font le travail)
Le framework est conçu pour être consommé par des agents IA, pas seulement par des humains. Le SDK Python est l'interface principale. Le CLI et le MCP sont des wrappers. Les agents Grimoire peuvent se modifier, s'améliorer, et évoluer eux-mêmes (Darwinism, CRISPR, Cognitive Flywheel).

---

## 3. Architecture Globale

```
                         ┌───────────────────────────────┐
                         │        UTILISATEUR            │
                         │  (Humain OU Agent externe)    │
                         └──────────────┬────────────────┘
                                        │
         ┌──────────────────────────────┼──────────────────────────────┐
         │                              │                              │
    ┌────▼─────┐                ┌───────▼───────┐              ┌──────▼──────┐
    │   IDE     │                │  CLI / Shell  │              │  API / SDK  │
    │ (12 IDE)  │                │               │              │  (Python)   │
    └────┬─────┘                └───────┬───────┘              └──────┬──────┘
         │                              │                              │
    ┌────▼──────────────────────────────▼──────────────────────────────▼──────┐
    │                   PROTOCOL ADAPTER LAYER (PAL)                          │
    │                                                                         │
    │   ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐        │
    │   │ MCP  │  │ REST │  │  WS  │  │ LSP  │  │ gRPC │  │ CLI  │        │
    │   │stdio │  │ HTTP │  │      │  │      │  │(opt) │  │pipes │        │
    │   │+ SSE │  │+ JWT │  │      │  │      │  │      │  │      │        │
    │   └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘        │
    │      └─────────┴────────┴────────┴────────┴────────┴──────┘           │
    │                              │                                         │
    └──────────────────────────────┼─────────────────────────────────────────┘
                                   │
    ┌──────────────────────────────▼─────────────────────────────────────────┐
    │                      GRIMOIRE CORE (Python SDK)                        │
    │                                                                        │
    │   ┌────────────┐  ┌────────────┐  ┌─────────────┐  ┌──────────────┐  │
    │   │ Agent API   │  │ Memory API │  │ Workflow API │  │  Config API  │  │
    │   └──────┬─────┘  └──────┬─────┘  └──────┬──────┘  └──────┬───────┘  │
    │          │               │               │                 │          │
    │   ┌──────▼──────────────▼───────────────▼─────────────────▼───────┐  │
    │   │            GRIMOIRE RUNTIME ENGINE (GRE)                       │  │
    │   │                                                                │  │
    │   │  ┌──────────┐  ┌──────────────┐  ┌─────────────┐             │  │
    │   │  │ Scheduler │  │ LLM Pool     │  │ Event Bus   │             │  │
    │   │  │ (DAG)     │  │ (multi-prov) │  │ (ELSS)      │             │  │
    │   │  └──────────┘  └──────────────┘  └─────────────┘             │  │
    │   │                                                                │  │
    │   │  Modes: simulated │ parallel-local │ distributed              │  │
    │   └────────────────────────────────────────────────────────────────┘  │
    │                                                                        │
    │   ┌────────────────────────────────────────────────────────────────┐  │
    │   │              GUARDRAILS (HUP + QEC + CVTL + CC)                │  │
    │   └────────────────────────────────────────────────────────────────┘  │
    │                                                                        │
    │   ┌────────────────────────────────────────────────────────────────┐  │
    │   │              EVOLUTION ENGINE (Darwinism + CRISPR + Dream)      │  │
    │   └────────────────────────────────────────────────────────────────┘  │
    └────────────────────────────────────────────────────────────────────────┘
                                   │
    ┌──────────────────────────────▼─────────────────────────────────────────┐
    │                    CREATIVE BRIDGE (plugin architecture)               │
    │                                                                        │
    │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
    │   │ Godot  │ │Blender │ │ Unity  │ │ Figma  │ │Unreal  │ │  ...   │ │
    │   └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │
    └────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Composants Détaillés

### 4.1 Protocol Adapter Layer (PAL)

**Problème résolu** : Les entreprises ont des politiques de sécurité variées. Certaines acceptent MCP, d'autres non. Aucune ne devrait être exclue.

**Solution** : Une interface `ProtocolAdapter` unique que chaque protocole implémente :

```python
class ProtocolAdapter(ABC):
    """Interface commune pour tous les protocoles d'accès à Grimoire."""
    
    @abstractmethod
    async def handle_request(self, request: GrimoireRequest) -> GrimoireResponse: ...
    
    @abstractmethod
    async def start(self) -> None: ...
    
    @abstractmethod
    async def stop(self) -> None: ...

class MCPAdapter(ProtocolAdapter):
    """MCP stdio + SSE — Standard Anthropic/Microsoft."""

class RESTAdapter(ProtocolAdapter):
    """REST HTTP + JWT auth — Fallback universel enterprise."""

class WSAdapter(ProtocolAdapter):
    """WebSocket bidirectionnel — Streaming temps réel."""

class LSPAdapter(ProtocolAdapter):
    """Language Server Protocol — Intégration IDE native."""

class CLIAdapter(ProtocolAdapter):
    """CLI pipes stdin/stdout JSON — Pour scripts et CI."""
```

**Contract testing** : Chaque adapter passe le MÊME jeu de 50+ tests fonctionnels. Si un adapter passe les tests, il est garanti compatible.

**Configuration** :
```yaml
# grimoire.yaml
server:
  adapters:
    mcp:
      enabled: true
      transport: stdio    # stdio | sse
    rest:
      enabled: true
      port: 9473
      auth: jwt           # jwt | api-key | none
      cors: ["*"]
    websocket:
      enabled: false
    lsp:
      enabled: false      # Activé auto si IDE détecté
    grpc:
      enabled: false
```

### 4.2 Grimoire Runtime Engine (GRE)

**Problème résolu** : Les agents ne sont que des prompts sans capacité d'exécution parallèle réelle.

**Solution** : Un runtime asyncio-natif avec 3 modes et fallback automatique.

#### Mode 1 — Simulated (in-process)
```python
# Un seul LLM, persona switching
# Coût : 1x | Latence : minimale | Use case : discussions, party mode
async def run_simulated(workflow: Workflow, agents: list[Agent]):
    llm = await llm_pool.acquire(tier="mid")
    for step in workflow.steps:
        agent = agents[step.agent_id]
        prompt = agent.persona.format(task=step.task)
        result = await llm.complete(prompt)
        step.result = result
    await llm_pool.release(llm)
```

#### Mode 2 — Parallel-Local (multi-worker asyncio)
```python
# N workers dans le même process, chacun avec son LLM
# Coût : Nx | Latence : min(steps) | Use case : cross-validation, parallel analysis
async def run_parallel(workflow: Workflow, agents: list[Agent]):
    dag = build_dag(workflow)
    async with asyncio.TaskGroup() as tg:
        for batch in dag.parallel_batches():
            tasks = []
            for step in batch:
                agent = agents[step.agent_id]
                llm = await llm_pool.acquire(tier=agent.model_tier)
                tasks.append(tg.create_task(execute_step(step, agent, llm)))
            # Batch terminé → passer au suivant
```

#### Mode 3 — Distributed (multi-process, multi-machine)
```python
# Workers comme processus séparés, message-bus Redis/NATS
# Coût : Nx + infra | Latence : optimale | Use case : scaling enterprise
async def run_distributed(workflow: Workflow, agents: list[Agent]):
    bus = await MessageBus.connect(backend="redis")  # ou "nats"
    for step in workflow.steps:
        await bus.send(
            recipient=step.agent_id,
            msg_type="task-request",
            payload=step.to_dict()
        )
    # Résultats collectés via pub-sub
    async for result in bus.subscribe("task-response"):
        workflow.update_step(result)
```

#### Fallback Chain
```
distributed → (Redis indisponible) → parallel-local → (LLM pool saturé) → simulated
```

#### LLM Pool
```python
class LLMPool:
    """Pool de connexions LLM avec rate limiting et circuit breaker."""
    
    providers: dict[str, LLMProvider]  # copilot, anthropic, openai, ollama, openrouter
    
    async def acquire(self, tier: str = "mid", task_type: str = "coding") -> LLMConnection:
        """Acquiert une connexion LLM optimale pour la tâche."""
        provider = self.router.select(tier=tier, task_type=task_type)
        connection = await provider.acquire()
        return connection
    
    async def release(self, connection: LLMConnection) -> None:
        """Libère une connexion dans le pool."""
```

### 4.3 IDE Adapter System

**Problème résolu** : Grimoire est marié à VS Code. Le monde a 12+ IDE.

**Solution** : `grimoire ide setup --ide <name>` génère les fichiers de configuration optimaux.

#### Fichiers générés par IDE

| IDE | Fichiers générés |
|---|---|
| VS Code | `.github/copilot-instructions.md`, `.vscode/mcp.json`, `.vscode/settings.json`, `.github/skills/` |
| Cursor | `.cursor/rules`, `.cursor/mcp.json`, `.cursorrules` |
| Windsurf | `.windsurfrules`, `.windsurf/mcp.json` |
| Claude Desktop | `~/.config/claude/claude_desktop_config.json` (MCP entry) |
| Cline | `.clinerules`, VS Code MCP config |
| IntelliJ | `.idea/grimoire.xml`, MCP plugin config |
| Neovim | `.nvim/grimoire.lua`, MCP plugin config |
| Zed | `.zed/settings.json` (MCP), `.zed/tasks.json` |
| Generic | README avec instructions MCP/REST |

#### Contenu des fichiers de configuration

Chaque IDE adapter génère :
1. **System prompts** adaptés à l'IDE (copilot-instructions, cursorrules, etc.)
2. **MCP server configuration** pointant vers `grimoire serve`
3. **Skills/tools** adaptés aux capacités de l'IDE
4. **Agent definitions** si l'IDE les supporte (VS Code modes, Cursor agents)

```python
class IDEAdapter(ABC):
    """Adaptateur pour un IDE spécifique."""
    
    @abstractmethod
    def generate_config(self, project: GrimoireProject) -> list[GeneratedFile]: ...
    
    @abstractmethod
    def supports_mcp(self) -> bool: ...
    
    @abstractmethod
    def supports_agents(self) -> bool: ...
    
    @abstractmethod
    def supports_skills(self) -> bool: ...
```

### 4.4 Creative Bridge

**Problème résolu** : Les agents ne peuvent interagir qu'avec du code. Le monde créatif (jeux, 3D, design) est inaccessible.

**Solution** : Plugin architecture où chaque outil créatif est un bridge indépendant.

```python
class CreativeBridge(ABC):
    """Interface commune pour les bridges vers outils créatifs."""
    
    @abstractmethod
    async def connect(self) -> bool: ...
    
    @abstractmethod
    async def execute(self, action: str, params: dict) -> BridgeResult: ...
    
    @abstractmethod
    def capabilities(self) -> list[str]: ...
    
    @abstractmethod
    async def health_check(self) -> bool: ...

class GodotBridge(CreativeBridge):
    """Bridge vers Godot 4 via EditorPlugin + GDScript CLI."""
    
    async def execute(self, action: str, params: dict) -> BridgeResult:
        if action == "create_scene":
            return await self._create_scene(params)
        elif action == "add_node":
            return await self._add_node(params)
        # ...

class BlenderBridge(CreativeBridge):
    """Bridge vers Blender via bpy Python over socket."""
    
    async def execute(self, action: str, params: dict) -> BridgeResult:
        script = self._generate_bpy_script(action, params)
        return await self._send_to_blender(script)
```

**Installation** :
```bash
pip install grimoire-bridge-godot
pip install grimoire-bridge-blender
grimoire bridge add godot --path /usr/bin/godot4
```

### 4.5 Iceberg CLI (Progressive Disclosure)

**Surface (3 commandes)** :
```bash
grimoire init                    # Bootstrap projet
grimoire status                  # Dashboard santé
grimoire ask "..."               # Parle au Grimoire (route vers le bon agent)
```

**Power (15 commandes)** :
```bash
grimoire agent list              # Agents disponibles
grimoire agent forge "..."       # Créer un agent
grimoire workflow run <file>     # Lancer un workflow
grimoire memory search "..."     # Chercher en mémoire
grimoire bench                   # Benchmark agents
grimoire tool <name> <args>      # Outil direct
grimoire ide setup --ide cursor  # Configurer un IDE
grimoire bridge add godot        # Ajouter un bridge créatif
grimoire serve                   # Lancer le serveur (MCP+REST)
grimoire party                   # Party mode
grimoire dream                   # Dream mode consolidation
grimoire explain <command>       # Explique ce que fait une commande
grimoire doctor                  # Diagnostic complet
grimoire upgrade                 # Mise à jour
```

**Expert (accès direct aux 87+ outils)** :
```bash
grimoire expert                  # Déverrouille tout
grimoire tool harmony-check --project-root .
grimoire tool stigmergy emit --project-root . --signal "..."
grimoire tool agent-darwinism evolve --project-root .
```

**SDK (Python)** :
```python
from grimoire import GrimoireProject
from grimoire.agents import Agent, AgentForge
from grimoire.memory import Memory, SemanticSearch
from grimoire.runtime import Runtime, LLMPool
from grimoire.bridges import GodotBridge, BlenderBridge
```

---

## 5. Sécurité

### 5.1 Auth Layer Unifié

```yaml
security:
  # REST API
  rest_auth:
    method: jwt             # jwt | api-key | none
    jwt_secret: "${GRIMOIRE_JWT_SECRET}"
    token_expiry: 3600
  
  # MCP capabilities
  mcp_capabilities:
    tool_approval: auto     # auto | prompt | whitelist
    whitelisted_tools: ["*"]
  
  # Sandbox
  sandbox:
    enabled: true
    allowed_commands: ["ruff", "pytest", "go", "npm", "godot"]
    network_access: false
    max_execution_time: 120
    filesystem_scope: "${PROJECT_ROOT}"  # Pas d'accès hors projet
  
  # Agent permissions (RBAC)
  agent_permissions:
    dev:
      file_write: ["src/**", "tests/**"]
      file_read: ["**"]
      execute: ["cc-verify", "pytest"]
      bridges: ["godot", "blender"]
    analyst:
      file_write: ["_bmad-output/**"]
      file_read: ["**"]
      execute: []
      bridges: []
```

### 5.2 Audit Trail

Chaque action via PAL est loguée dans BMAD_TRACE avec :
- Source (IDE, CLI, API, agent)
- Protocole utilisé (MCP, REST, SDK)
- Action exécutée
- Résultat + trust score
- Durée + coût LLM

---

## 6. Métriques de Succès

| Métrique | Cible | Mesure |
|---|---|---|
| Time-to-first-value | < 60 secondes | `grimoire init` → premier `grimoire status` |
| IDE supportés (Gold) | 3 | VS Code, Cursor, Claude Desktop |
| IDE supportés (Silver+) | 8 | + Windsurf, Cline, IntelliJ, Neovim, Zed |
| Protocoles actifs | 3 (Tier 1) | MCP, REST, Python SDK |
| Tests passing | > 4000 | pytest total |
| Contract tests par adapter | > 50 | Même suite pour chaque PAL adapter |
| Creative bridges | 2 natifs | Godot, Blender |
| LLM providers supportés | 5 | Copilot, Anthropic, OpenAI, Ollama, OpenRouter |
| Runtime modes | 3 | Simulated, Parallel, Distributed |
| Zero-downgrade guarantee | 100% | Fallback chain automatique, jamais de crash |

---

## 7. Hors Scope v4

| Feature | Raison | Quand |
|---|---|---|
| Agent Marketplace public | Nécessite infra hosting + modération | v5 |
| Voice Interface | Dépendance API audio pas encore stable | v5 |
| Visual Workflow Editor (web UI) | Scope massif, nécessite frontend dédié | v5 |
| Mobile IDE support | Marché trop petit | Pas planifié |

---

## 8. Dépendances Techniques

| Dépendance | Usage | Installation |
|---|---|---|
| Python 3.12+ | Core runtime | Requis |
| `uv` (Astral) | Package manager + distribution | Recommandé |
| `asyncio` | Runtime async | Stdlib |
| `aiohttp` | LLM API calls async | Optional (REST adapter + LLM pool) |
| `mcp` (SDK) | MCP server | Optional (MCP adapter) |
| `fastapi` | REST adapter | Optional |
| `qdrant-client` | Mémoire sémantique | Optional |
| `sentence-transformers` | Embeddings | Optional |
| Redis | Distributed message bus | Optional (mode distributed) |
| NATS | Haute-perf message bus | Optional (mode distributed) |

**Principe zero-dep pour le core** : Le core Grimoire fonctionne avec ZERO dépendance externe (stdlib only). Les dépendances sont des extras optionnels : `pip install grimoire-kit[mcp,rest,semantic]`.
