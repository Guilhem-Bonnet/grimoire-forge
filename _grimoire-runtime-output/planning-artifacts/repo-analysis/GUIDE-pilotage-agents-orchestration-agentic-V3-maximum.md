---
title: "Guide d'Enseignement — Pilotage Agentique & Orchestration LLM (V3 — Maximum)"
subtitle: "Analyse maximale · 33 repos · 8 agents Explore parallèles · Repos inédits + approfondissements V2"
date: 2026-04-26
version: "3.0 — Profondeur maximale"
author: Grimoire Master (SOG)
repos_analyzed: 33
agents_used: 8
confidence: very_high
grounding: "Code source lu directement sur tous les repos (V2 + 8 nouveaux agents en parallèle)"
prerequisite: "Lire V2 d'abord — ce document complète sans répéter"
---

# Guide V3 — Pilotage Agentique : Profondeur Maximale

> Ce document complète la V2. V2 = code source des patterns principaux. V3 = repos inédits + approfondissements code.
> Chaque section couvre ce qui N'EST PAS dans la V2.

---

## Table des matières

**Partie I — Repos inédits (jamais couverts en V2)**
1. [vscode-copilot-chat — Architecture interne Copilot](#1-vscode-copilot-chat)
2. [shannon — Pentest IA avec Temporal Workflows](#2-shannon)
3. [andrej-karpathy-skills + claude-skills + superpowers](#3-skill-ecosysteme)
4. [openclaw — Platform multi-channel avec Plugin SDK](#4-openclaw)
5. [LLMSecurityGuide — OWASP Agentic Top 10](#5-llmsecurityguide)

**Partie II — Approfondissements V2 (bien plus profonds)**
6. [LangGraph — Streaming, channels, interrupt/resume, scheduler](#6-langgraph-v3)
7. [CrewAI — Guardrails+retry, LanceDB, hierarchical process](#7-crewai-v3)
8. [OpenAI Agents — Lifecycle complet, streaming, tracing, tool execution](#8-openai-agents-v3)
9. [agent-sandbox — CRDs complètes, warm pool reconciler](#9-agent-sandbox-v3)
10. [pixel-agents — Dual-mode detection, animation](#10-pixel-agents-v3)
11. [OpenMythos — RDT complet : LTI, ACT, LoRA, MoE](#11-openmythos-v3)
12. [Haystack — ConditionalRouter, error handling, sérialisation, OTel](#12-haystack-v3)
13. [Dify — Chunking, retrieval hybride parallèle, reranking](#13-dify-v3)

**Partie III — Synthèse transversale V3**
14. [Patterns d'erreur et récupération](#14-error-recovery)
15. [Architectures de skill — 4 modèles](#15-skill-architectures)
16. [Sécurité agentique — ASI01-ASI10 avec code](#16-agentic-security)
17. [Stack complète mise à jour V3](#17-stack-v3)

---

## Partie I — Repos inédits

---

## 1. vscode-copilot-chat

> Repo : `/mnt/Travail/Projets/Dev/Référence-Agentique/vscode-copilot-chat/`
> Code source TypeScript de l'extension GitHub Copilot Chat pour VS Code.

### 1.1 Architecture des hooks — processus externes

Les hooks ne sont PAS des callbacks JavaScript dans le process de l'extension. Ce sont des **processus externes** (child processes) invoqués via stdin/stdout JSON.

```typescript
// src/platform/chat/node/hookExecutor.ts
class NodeHookExecutor {
  async executeCommand(hookCommand: ChatHookCommand, input: unknown, token: CancellationToken) {
    const child = spawn(hook.command, [], {
      stdio: 'pipe',
      cwd,
      env: { ...process.env, ...hook.env },
      shell: getShell(),
    });

    child.stdin.write(JSON.stringify(input));  // Input = JSON sur stdin
    child.stdout.on('data', data => stdout.push(data.toString()));

    // Timeout avec escalade SIGTERM → SIGKILL
    const timeoutTimer = setTimeout(
      () => killWithEscalation('timeout'),
      (hook.timeout ?? DEFAULT_TIMEOUT_SEC) * 1000
    );

    // Exit codes:
    // 0 → success (parse stdout JSON)
    // 2 → blocking error (affiché au modèle)
    // autres → non-blocking warning (affiché à l'utilisateur)
    if (code === 0) {
      result = JSON.parse(stdoutStr);
      return { kind: HookCommandResultKind.Success, result };
    } else if (code === 2) {
      return { kind: HookCommandResultKind.Error, result: stderrStr };
    }
  }
}
```

**Input commun injecté par ChatHookService :**

```typescript
const commonInput = {
  timestamp: new Date().toISOString(),
  hook_event_name: hookType,
  session_id: sessionId,
  transcript_path: transcriptPath?.fsPath,  // Transcript sur disque (flushé avant)
  ...hookType_specific_input
};
```

**Règle de priorité pour PreToolUse multi-hooks :**

```typescript
const permissionPriority: Record<string, number> = { 'deny': 2, 'ask': 1, 'allow': 0 };
// deny > ask > allow (plus restrictif gagne)
```

**Types de hooks et leur décision :**

| Hook | Peut bloquer | Peut modifier | Décision possible |
|------|-------------|---------------|-------------------|
| `UserPromptSubmit` | Oui (code 2) | `additionalContext` | — |
| `PreToolUse` | Oui | `updatedInput` | `allow / deny / ask` |
| `PostToolUse` | Oui | — | `block + reason` |
| `Stop` | Oui | `reason` (relance) | `block` |
| `PreCompact` | Non | `custom_instructions` | — |
| `SessionStart` | Non | `additionalContext` | — |
| `SubagentStart` | Non | `additionalContext` | — |

### 1.2 ToolCallingLoop — orchestration agentique abstraite

```typescript
// src/extension/intents/node/toolCallingLoop.ts
export abstract class ToolCallingLoop<TOptions extends IToolCallingLoopOptions> extends Disposable {
  private static readonly TASK_COMPLETE_TOOL_NAME = 'task_complete';
  private toolCallResults: Record<string, LanguageModelToolResult2> = {};
  private toolCallRounds: IToolCallRound[] = [];
  private stopHookReason: string | undefined;
  private additionalHookContext: string | undefined;

  // Abstractions à implémenter par les subclasses spécialisées
  protected abstract buildPrompt(...): Promise<IBuildPromptResult>;
  protected abstract getAvailableTools(...): Promise<LanguageModelToolInformation[]>;
  protected abstract fetch(...): Promise<ChatResponse>;
}
```

**Boucle principale :**
1. Build prompt (AgentPrompt React/TSX element)
2. Fetch LLM response (streaming)
3. Parse tool calls
4. **PreToolUse hooks** → modifier/bloquer inputs
5. Invoke tools en parallèle (IToolsService)
6. **PostToolUse hooks** → filtrer résultats
7. Accumulate → `toolCallRounds`
8. **Stop hooks** → vérifier si la boucle doit continuer
9. Décision : continuer ou terminer

**Stop hook — comment la raison devient une relance :**

```typescript
// Si Stop hook retourne decision: 'block', la raison est injectée comme query
if (this.stopHookReason) {
  query = formatHookContext([this.stopHookReason]);
  // "You were about to complete but a hook blocked you: {reason}"
}
```

**Subclasses disponibles :**
- `DefaultToolCallingLoop` — agent panel standard
- `SearchSubagentToolCallingLoop` — sous-agent de recherche de code
- `ExecutionSubagentToolCallingLoop` — sous-agent d'exécution

### 1.3 AgentPrompt — React/TSX elements

```typescript
// src/extension/prompts/node/agent/agentPrompt.tsx
export class AgentPrompt extends PromptElement<AgentPromptProps> {
  async render(state: void, sizing: PromptSizing) {
    const customizations = this.props.customizations;
    // Customizations depuis PromptRegistry.resolveAllCustomizations()

    return <>
      <SystemMessage>
        You are an expert AI programming assistant in VS Code.<br />
        <CopilotIdentityRules />  {/* Identité personnalisée */}
        <SafetyRules />           {/* Règles de sécurité */}
      </SystemMessage>
      {instructions}
      {/* Historical conversation, tool calls, etc. */}
    </>;
  }
}
```

### 1.4 Model routing — 5 stratégies en cascade

```typescript
// src/extension/prompt/vscode-node/endpointProviderImpl.ts
async getChatEndpoint(requestOrFamilyOrModel): Promise<IChatEndpoint> {
  // Stratégie 1: string → résoudre famille (copilot-base ou copilot-fast)
  if (typeof requestOrFamilyOrModel === 'string') {
    const modelMetadata = await this._modelFetcher.getChatModelFromFamily(requestOrFamilyOrModel);
    return this.getOrCreateChatEndpointInstance(modelMetadata!);
  }

  // Stratégie 2: extraire le modèle depuis ChatRequest / LanguageModelChat
  const model = 'model' in requestOrFamilyOrModel ? requestOrFamilyOrModel.model : requestOrFamilyOrModel;

  if (!model) return this.getChatEndpoint('copilot-base');  // Fallback

  // Stratégie 3: modèle tiers (non Copilot) → ExtensionContributedChatEndpoint
  if (model.vendor !== 'copilot') {
    return this._instantiationService.createInstance(ExtensionContributedChatEndpoint, model);
  }

  // Stratégie 4: pseudo-modèle AutoMode → AutomodeService.resolveAutoModeEndpoint()
  if (model.id === AutoChatEndpoint.pseudoModelId) {
    const allEndpoints = await this.getAllChatEndpoints();
    return this._autoModeService.resolveAutoModeEndpoint(requestOrFamilyOrModel, allEndpoints);
  }

  // Stratégie 5: modèle standard → métadonnées API
  const modelMetadata = await this._modelFetcher.getChatModelFromApiModel(model);
  return modelMetadata ? this.getOrCreateChatEndpointInstance(modelMetadata) : this.getChatEndpoint('copilot-base');
}
```

**Tool selection model-aware :**

```typescript
// agentIntent.ts — Sélection conditionnelle selon le modèle
allowTools[ToolName.ApplyPatch] = modelSupportsApplyPatch(model);
allowTools[ToolName.SearchSubagent] = isGptOrAnthropic(model) && searchSubagentEnabled;

// Gemini-3 special handling via experimentation service
if (model.family.toLowerCase().includes('gemini-3')) {
  allowTools[ToolName.MultiReplaceString] = configurationService.getExperimentBasedConfig(
    ConfigKey.Advanced.Gemini3MultiReplaceString, experimentationService
  );
}
```

### 1.5 Conversation summarization — template hiérarchique

```typescript
// src/extension/prompt/node/summarizer.ts
// Le prompt de summarization utilise une structure en 8 sections :

/*
<analysis>
  1. Chronological Review: phases du conversation
  2. Intent Mapping: intentions utilisateur explicites
  3. Technical Inventory: technologies/patterns
  4. Code Archaeology: fichiers/fonctions modifiés
  5. Progress Assessment: complété vs en attente
  6. Context Validation: contexte pour continuation
  7. Recent Commands Analysis: dernières actions tool
</analysis>

<summary>
  1. Conversation Overview: objectifs + évolution
  2. Technical Foundation: stack technique
  3. Codebase Status: fichiers modifiés + statut
  4. Problem Resolution: problèmes/solutions
  5. Progress Tracking: tâches complétées
  6. Active Work State: travail avant summarization
  7. Recent Operations: tool calls + résultats
  8. Continuation Plan: tâches en attente
</summary>
*/
```

**Modèle utilisé pour la summarization :** `copilot-fast` (budget-conscious)  
**Tokens max summary :** `7_000`  
**Max tool result length dans résumé :** `2_000`

---

## 2. shannon

> Repo : `/mnt/Travail/Projets/Dev/Référence-Agentique/shannon/`
> Pentesteur IA autonome orchestré par Temporal Workflows + Claude Agent SDK.

### 2.1 Pipeline d'orchestration — Temporal Workflows

```typescript
// apps/worker/src/temporal/workflows.ts
// 5 phases séquentielles + parallèles :
//
// Phase 1: pre-recon      (séquentiel, modelTier: 'large')
// Phase 2: recon          (séquentiel)
// Phases 3-4: 5 paires parallèles pipelinées :
//   injection-vuln → [queue check] → injection-exploit
//   xss-vuln       → [queue check] → xss-exploit
//   auth-vuln      → [queue check] → auth-exploit
//   ssrf-vuln      → [queue check] → ssrf-exploit
//   authz-vuln     → [queue check] → authz-exploit
// Phase 5: report         (séquentiel, assemble les 5 evidences)

// Retry policies
const PRODUCTION_RETRY = {
  initialInterval: '5 minutes',
  maximumInterval: '30 minutes',
  backoffCoefficient: 2,
  maximumAttempts: 50,
  nonRetryableErrorTypes: ['AuthenticationError', 'InvalidRequestError', ...]
};
```

**Mécanisme de reprise après crash :**
- Détecte agents complétés via `session.json` dans workspace
- Restaure checkpoints git correspondants
- 13 agents peuvent reprendre indépendamment (Temporal durable execution)

### 2.2 Cycle de vie d'un agent — 10 étapes

```typescript
// apps/worker/src/services/agent-execution.ts
async execute(agentName, input, auditSession, logger) {
  // 1. Load config (cascade: parsed → YAML → file path)
  // 2. Load prompt template from AGENTS[agentName].promptTemplate
  // 3. git commit "pre-${agentName}-attempt-${N}"       ← checkpoint AVANT
  // 4. Start audit logging
  // 5. runClaudePrompt() avec :
  //    - maxTurns: 10_000
  //    - permissionMode: 'bypassPermissions'
  //    - outputFormat: JsonSchemaOutputFormat (agents vuln uniquement)
  // 6. Check spending cap: turns ≤ 2 && cost == 0 && billing text
  // 7. Handle execution failure (retryable vs non-retryable)
  // 8. Write structured output JSON à disk
  // 9. validateQueueSafe(vulnType) → ExploitationDecision
  // 10. git commit "${agentName}-complete"               ← checkpoint APRÈS
}
```

### 2.3 Intégration Claude Agent SDK

```typescript
// apps/worker/src/ai/claude-executor.ts
export async function runClaudePrompt(
  prompt, sourceDir, context, agentName, modelTier, outputFormat, ...
) {
  const options = {
    model: resolveModel(modelTier),   // claude-opus-4 | claude-sonnet-4 | claude-haiku-4
    maxTurns: 10_000,                 // Très élevé pour agents autonomes
    cwd: sourceDir,
    permissionMode: 'bypassPermissions',   // Pas de prompts permission
    allowDangerouslySkipPermissions: true,
    outputFormat: outputFormat             // JSON Schema pour agents vuln
  };

  // Provider routing via env vars
  if (providerConfig.providerType === 'bedrock')    sdkEnv.CLAUDE_CODE_USE_BEDROCK = '1';
  else if (providerConfig.providerType === 'vertex') sdkEnv.CLAUDE_CODE_USE_VERTEX = '1';
  else if (providerConfig.providerType === 'litellm_router') sdkEnv.ANTHROPIC_BASE_URL = baseUrl;
}
```

### 2.4 Schéma de sortie structurée — validation Zod + JSON Schema

```typescript
// Schéma d'une vulnérabilité injection
const InjectionVulnerability = baseVulnerability.extend({
  source: z.string().optional(),          // "paramName @ file:line"
  sink_call: z.string().optional(),       // "file:line + method"
  slot_type: z.string().optional(),       // "SQL-val|SQL-ident|CMD-argument|FILE-path"
  sanitization_observed: z.string().optional(),
  verdict: z.string().optional(),         // "safe | vulnerable"
  witness_payload: z.string().optional(), // Payload pour phase exploitation
});

// Queue entre phases vuln → exploit
// injection_exploitation_queue.json contient les witness_payloads
// L'agent d'exploit lit la queue et prouve chaque vulnérabilité dynamiquement
```

### 2.5 Prompt d'exploitation — persona actif

Extrait du prompt `exploit-injection.txt` (300+ lignes) :

```
<role>
You are a world-class Injection Exploitation Specialist.
You are NOT an analyst; you are an active penetration tester.
Your persona is methodical, persistent, laser-focused on proving tangible impact.
</role>

<proof_stages>
SQLi progression:
1. Confirm injection: Error-based OR time-based OR boolean-based
2. Enumerate: table names, column names, schema
3. Extract sensitive data (credentials, PII, secrets)
4. Document: input → query construction → exfiltration

Command Injection:
1. Confirm: time-based delay OR output capture
2. Prove: whoami, id, uname -a
3. Achieve: reverse shell, data exfiltration, lateral movement
</proof_stages>
```

### 2.6 Classification des erreurs pour Temporal

```typescript
function classifyErrorForTemporal(error: PentestError): ApplicationFailure {
  if (!retryable) {
    return ApplicationFailure.nonRetryable(error.message, mapErrorCodeToType(errorCode));
    // Non-retryable: CONFIG_NOT_FOUND, PROMPT_LOAD_FAILED, AuthenticationError
  }
  // Retryable: SPENDING_CAP_REACHED, API_RATE_LIMITED, GIT_CHECKPOINT_FAILED
  // → Temporal applique retry policy (5-30 min backoff)
  return ApplicationFailure.retryable(error.message, ...);
}

// Détection spending cap
function isSpendingCapBehavior(turns, cost, resultText) {
  return turns <= 2 && cost === 0 && /spending\s+cap|rate\s+limit|quota\s+exceeded/i.test(resultText);
}
```

---

## 3. Skill Ecosystem

### 3.1 andrej-karpathy-skills — 4 principes comportementaux

Structure minimaliste : 1 skill, 4 principes, SKILL.md global.

```
# Karpathy Coding Guidelines

1. Think Before Coding
   - Surface assumptions BEFORE writing code
   - Don't hide confusion — ask clarifying questions
   - Verify understanding with the user first

2. Simplicity First
   - Minimum viable code — zero speculation
   - No abstractions beyond what's explicitly requested
   - Match the existing style of the codebase

3. Surgical Changes
   - ONLY touch what was explicitly requested
   - Don't refactor surrounding code
   - Don't clean up "while you're there"

4. Goal-Driven Execution
   - Transform tasks into verifiable success criteria
   - Write tests FIRST to define done
   - Return: [task done] vs [blocked: reason]
```

**Pattern d'installation** : injection globale via CLAUDE.md append — s'applique à tous les agents.

### 3.2 claude-skills — Bibliothèque professionnelle de 66 skills

**Structure standardisée :**

```
skills/
  {category}/               # language, backend, frontend, infrastructure, ...
    {skill-name}/
      SKILL.md              # Persona + instructions + exemples
      references/           # Documentation deep-dive
        architecture.md
        best-practices.md
        common-patterns.md
```

**Activation contextuelle :**
- "Implement JWT in NestJS" → `nestjs-expert` + `secure-code-guardian` s'activent automatiquement
- Decision trees dans SKILLS_GUIDE.md pour choisir la bonne combinaison
- 9 workflow commands qui combinent des skills

**9 Workflow Commands :**
- `feature-development` : spec → design → implement → test → document
- `bug-fixing` : reproduce → diagnose → fix → verify
- `code-review` : analyze → assess → suggest → summarize
- `common-ground` : valide les assomptions cachées avant d'exécuter
- ... (5 autres)

### 3.3 superpowers — Méthodologie subagent-driven

**13 skills formant une pipeline complète :**

```
brainstorming (approval requis)
  → writing-plans (approval requis)
    → dispatching-parallel-agents
      → subagent-driven-development
        → test-driven-development (RED-GREEN-REFACTOR mandatory)
          → requesting-code-review (2-stage: spec + code quality)
            → finishing-a-development-branch
```

**Règle stricte (AGENTS.md) :** 94% PR rejection rate — protection anti-slop.

**Multi-stage gating :**
1. Design approval (human)
2. Plan approval (human)
3. Subagent dispatch (automated)
4. 2-stage review (spec compliance → code quality)
5. PR merge (human)

**Hook-driven activation :**
```yaml
# hooks/session-start/config.json
{
  "triggers": ["session_start"],
  "context": "Load workflow pipeline and activate relevant skills"
}
```

**Git worktree isolation :** chaque feature branch = worktree isolé avec subagents dédiés.

### 3.4 Comparaison des 3 modèles de skill

| Aspect | karpathy-skills | claude-skills | superpowers |
|--------|-----------------|---------------|-------------|
| **Volume** | 1 skill | 66 skills | 13 skills |
| **Focus** | Comportement LLM | Expertise domaine | Workflow complet |
| **Activation** | Globale | Contextuelle | Hook-triggered |
| **Multi-agent** | Non | Non | Oui (dispatch + review) |
| **Gating** | Non | Non | Oui (approbation humaine) |
| **Persistance** | Non | Non | Oui (plans, designs) |

---

## 4. openclaw

> Repo : `/mnt/Travail/Projets/Dev/Référence-Agentique/openclaw/`
> Personal AI assistant multi-channel, multi-platform.

### 4.1 Architecture plugin-first

```
Core (extension-agnostic)
  └── Plugin SDK (public API)
        └── Extensions (55+ plugins)
              └── ClawHub registry (trust + versioning)

Channels (20+): Telegram, Discord, Slack, WhatsApp, Signal, iMessage, Matrix, Teams...
Apps: iOS, macOS, Android (natifs)
```

**Règle fondamentale :** Le core ne connaît JAMAIS les IDs de plugins — il utilise uniquement les manifests et les registry contracts.

### 4.2 Plugin SDK — 2 types de plugins

**Bundle-style plugins (preferred) :**
- Surfaces stables : skills, MCP servers, config
- Pas de code custom dans le runtime
- Manifest declaratif + capability contracts

**Code plugins :**
- Hooks runtime : `PreToolUse`, `PostToolUse`, `SessionStart`
- Providers : LLM providers, storage backends
- Tools : outils custom exposés via MCP

**Manifest structure :**
```json
{
  "id": "github-plugin",
  "version": "1.2.0",
  "capabilities": ["read:repos", "write:issues"],
  "permissions": ["network:api.github.com"],
  "requirements": ["oauth:github"],
  "hooks": ["PreToolUse", "PostToolUse"]
}
```

### 4.3 Prompt cache determinism

Pattern critique identifié dans AGENTS.md :

> "Prefix cache: every message must start with the same bytes as the previous message. If the system prompt changes between turns, cache invalidation destroys cost savings."

→ **Ne jamais modifier le system prompt entre les turns** — utiliser `additionalContext` pour les injections dynamiques.

---

## 5. LLMSecurityGuide

> Repo : `/mnt/Travail/Projets/Dev/Référence-Agentique/LLMSecurityGuide/`
> 1956 lignes, Février 2026. OWASP Top 10 LLMs 2025 + OWASP Agentic Top 10 2026.

### 5.1 OWASP Agentic Top 10 — ASI01 à ASI10

| ID | Vulnérabilité | Description |
|----|--------------|-------------|
| **ASI01** | Agent Goal Hijack | Redirection des objectifs via sub-goal injection, context poisoning |
| **ASI02** | Tool Misuse & Exploitation | Agents abusent des outils légitimes pour des actions non autorisées |
| **ASI03** | Identity & Privilege Abuse | Exploitation des NHI (Non-Human Identity) credentials |
| **ASI04** | Agentic Supply Chain | Serveurs MCP malveillants, outils empoisonnés |
| **ASI05** | Unexpected Code Execution | Agents génèrent du code contrôlé par l'attaquant |
| **ASI06** | Memory & Context Poisoning | Corruption persistante de la mémoire agent |
| **ASI07** | Insecure Inter-Agent Communication | Messages inter-agent forgés/usurpés |
| **ASI08** | Cascading Failures | Faux signaux qui se propagent en cascade |
| **ASI09** | Human-Agent Trust Exploitation | Mensonges polis et confiants |
| **ASI10** | Rogue Agents | Agents malveillants ou compromis |

### 5.2 Défenses avec code — ASI01, ASI06, ASI10

**ASI01 — Agent Goal Hijack :**

```python
class AgentBehaviorMonitor:
    def monitor_agent_action(self, agent_id: str, action: str, stated_goal: str):
        # Check goal consistency
        if not self._is_consistent(action, stated_goal):
            self._quarantine(agent_id)
            raise GoalHijackDetected(f"Action '{action}' inconsistent with goal '{stated_goal}'")

    def _is_consistent(self, action, goal) -> bool:
        # LLM-based consistency check (ironique mais efficace)
        # Ou règles déterministes : action ∈ allowed_actions_for_goal
        ...
```

**ASI06 — Memory Poisoning :**

```python
class MemoryIntegrityValidator:
    def validate_memory_update(self, agent_id: str, memory_key: str,
                                new_value: Any, source: str) -> bool:
        # 1. Vérifier la source (trusted vs untrusted)
        if source not in self.trusted_sources:
            return False
        # 2. Hash-based integrity: compare with expected hash
        expected_hash = self.memory_hashes.get(f"{agent_id}:{memory_key}")
        if expected_hash and hash(new_value) != expected_hash:
            self._alert(f"Memory tampering detected: {memory_key}")
            return False
        # 3. Lineage tracking: qui a écrit quoi quand
        self.lineage[f"{agent_id}:{memory_key}"] = {
            "source": source, "timestamp": now(), "value_hash": hash(new_value)
        }
        return True
```

**ASI10 — Rogue Agents :**

```python
class AgentBehaviorMonitor:
    def detect_rogue_behavior(self, agent_id: str, recent_actions: list[str]) -> bool:
        # Anomalies : actions hors périmètre, fréquence anormale, actions destructives
        anomaly_score = self._compute_anomaly_score(agent_id, recent_actions)
        if anomaly_score > ROGUE_THRESHOLD:
            self._quarantine(agent_id)
            self._notify_operators(agent_id, anomaly_score)
            return True
        return False
```

### 5.3 Sécurité MCP (ASI04)

```python
# Règles strictes pour serveurs MCP
class MCPSecurityGateway:
    ALLOWLIST = {"filesystem", "git", "fetch"}  # Serveurs autorisés uniquement

    def connect_server(self, server_name: str, server_url: str) -> bool:
        if server_name not in self.ALLOWLIST:
            raise MCPServerNotAllowed(f"Server '{server_name}' not in allowlist")
        # Vérifier la signature/certificat du serveur
        if not self._verify_signature(server_url):
            raise MCPServerUntrusted(...)
        return True
```

---

## Partie II — Approfondissements V2

---

## 6. LangGraph V3

> Complète la V2 §4 — Pregel supersteps déjà documentés. Cette section couvre streaming, channels, interrupt/resume, scheduler.

### 6.1 Streaming — 7 modes et la queue SyncQueue

```python
# pregel/main.py
def stream(self, input, config=None, *, stream_mode=None, ...) -> Iterator:
    stream = SyncQueue()  # File thread-safe

    # StreamMessagesHandler : callback sur chaque token LLM
    if "messages" in self._stream_modes:
        callback_manager.add_handler(
            StreamMessagesHandler(
                stream=StreamProtocol(stream.put_nowait, self._stream_modes),
                subgraphs=subgraphs,
            )
        )

    with SyncPregelLoop(...) as loop:
        loop.tick()

    while True:
        try:
            yield stream.get(block=False)
        except queue.Empty:
            break
```

**Comment les tokens arrivent dans la queue :**

```python
# pregel/_messages.py — StreamMessagesHandler
class StreamMessagesHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, *, chunk=None, run_id, ...):
        # Appelé par LangChain pour chaque token LLM
        # meta = (namespace_tuple, {langgraph_step, langgraph_node, ...})
        self._emit(meta, message)

    def _emit(self, meta: Meta, message: BaseMessage, *, dedupe=False):
        # namespace_tuple = ("parent_node", "child_node", ...) pour subgraphs
        self.stream((meta[0], "messages", (message, meta[1])))
```

**7 modes de stream et leurs données :**

| Mode | Données | Quand émis |
|------|---------|------------|
| `values` | Full state après chaque step | `tick()` après apply_writes |
| `updates` | `{node: output}` diffs seulement | Après writes |
| `messages` | `(BaseMessage, metadata)` token par token | `on_llm_new_token` callback |
| `custom` | Anything via `get_stream_writer()` | Dans les nodes |
| `checkpoints` | Snapshot complet du checkpoint | Après chaque step |
| `tasks` | `{task_id: PregelTask}` avant exécution | Avant `tick()` |
| `debug` | Wrapper `{step, timestamp, type, payload}` | Alias de checkpoints+tasks |

### 6.2 Channel types — gestion des conflits de writes

**LastValue — strictement une write par step :**

```python
# channels/last_value.py
class LastValue(Generic[Value], BaseChannel[Value, Value, Value]):
    def update(self, values: Sequence[Value]) -> bool:
        if len(values) != 1:
            raise InvalidUpdateError(
                "Can receive only one value per step. "
                "Use Annotated key to handle multiple values."
            )
        self.value = values[-1]
        return True
```

**Topic — accumule tous les writes (PubSub) :**

```python
# channels/topic.py
class Topic(Generic[Value], BaseChannel[Sequence[Value], Value | list[Value], list[Value]]):
    def __init__(self, typ, accumulate: bool = False):
        self.accumulate = accumulate  # False = vider après chaque step
        self.values = list[Value]()

    def update(self, values: Sequence[Value | list[Value]]) -> bool:
        if not self.accumulate:
            self.values = list[Value]()  # Clear à chaque step
        if flat_values := tuple(_flatten(values)):
            self.values.extend(flat_values)
        return True
```

**BinaryOperatorAggregate — merge avec opérateur :**

```python
# channels/binop.py
# Exemple: state["messages"] = Annotated[list, operator.add]  → accumule tous les messages
class BinaryOperatorAggregate(Generic[Value], BaseChannel[Value, Value, Value]):
    def update(self, values: Sequence[Value]) -> bool:
        for value in values:
            is_overwrite, overwrite_value = _get_overwrite(value)
            if is_overwrite:
                self.value = overwrite_value  # Overwrite() remplace tout
            else:
                self.value = self.operator(self.value, value)  # Applique l'opérateur
        return True

# Conflit : 2 writes LastValue → InvalidUpdateError
# Conflit : 2 writes Topic → s'accumulent (pas d'erreur)
# Conflit : 2 writes BinaryOp → agrégées via l'opérateur
# Force override : Overwrite(new_value) dans BinaryOp
```

### 6.3 Interrupt/Resume — pending_writes + Command

```python
# types.py — La fonction interrupt()
def interrupt(value: Any) -> Any:
    """
    1ère invocation dans un node → lève GraphInterrupt (arrêt)
    value est inclus dans l'exception → retourné au client
    Reprise → appeler graph.invoke(Command(resume=value))
    """

# types.py — Command
@dataclass
class Command(Generic[N]):
    resume: dict[str, Any] | Any | None = None
    # dict[interrupt_id → value] pour multi-interrupts
    # valeur simple pour single-interrupt
    update: Any | None = None  # Mettre à jour le state en reprenant
    goto: Send | Sequence[Send | N] | N = ()  # Router vers des nodes
```

**Pending writes — comment le checkpoint mémorise l'interrupt :**

```python
# pregel/_loop.py — _pending_interrupts()
def _pending_interrupts(self) -> set[str]:
    pending_interrupts: dict[str, str] = {}  # task_id → interrupt_id
    pending_resumes: set[str] = set()

    for task_id, write_type, value in self.checkpoint_pending_writes:
        if write_type == INTERRUPT:
            pending_interrupts[task_id] = value[0].id
        elif write_type == RESUME:
            pending_resumes.add(task_id)

    # Pending = interrompus sans résumé correspondant
    return {v for k, v in pending_interrupts.items() if k not in pending_resumes}
```

**Cas spécial multi-interrupt :**

```python
# Plusieurs interrupts → Command(resume={interrupt_id_1: val1, interrupt_id_2: val2})
if resume_is_map := (
    isinstance(resume, dict)
    and all(is_xxh3_128_hexdigest(k) for k in resume)
):
    self.config[CONF][CONFIG_KEY_RESUME_MAP] = resume
else:
    if len(self._pending_interrupts()) > 1:
        raise RuntimeError("Multiple pending interrupts: must specify interrupt id when resuming.")
```

### 6.4 Scheduler — PUSH vs PULL tasks

```python
# pregel/_algo.py — prepare_next_tasks()
def prepare_next_tasks(checkpoint, pending_writes, processes, channels, ...):
    tasks = []

    # 1. PUSH tasks — depuis le canal TASKS (envoyés via Send())
    tasks_channel = cast(Topic[Send] | None, channels.get(TASKS))
    if tasks_channel and tasks_channel.is_available():
        for idx, send in enumerate(tasks_channel.get()):
            if task := prepare_single_task((PUSH, idx), ...):
                tasks.append(task)

    # 2. PULL tasks — nodes déclenchés par les edges
    # Optimisation : si updated_channels connu → trigger_to_nodes pour filtrer
    if updated_channels and trigger_to_nodes:
        triggered_nodes = set()
        for channel in updated_channels:
            if node_ids := trigger_to_nodes.get(channel):
                triggered_nodes.update(node_ids)
        candidate_nodes = sorted(triggered_nodes)  # Ordre déterministe
    else:
        candidate_nodes = processes.keys()

    for name in candidate_nodes:
        if task := prepare_single_task((PULL, name), ...):
            tasks.append(task)

    return {t.id: t for t in tasks}
```

**Exécution parallèle des tasks :**

```python
# pregel/_executor.py
class BackgroundExecutor:
    """ThreadPoolExecutor pour tasks synchrones"""
    def submit(self, fn, *args,
               __cancel_on_exit__=False,
               __reraise_on_exit__=True,
               __next_tick__=False, **kwargs):
        ctx = copy_context()  # Copie le contexte Python (vars, etc.)
        task = self.executor.submit(ctx.run, fn, *args, **kwargs)
        self.tasks[task] = (__cancel_on_exit__, __reraise_on_exit__)
        return task

class AsyncBackgroundExecutor:
    """asyncio.Semaphore pour max_concurrency"""
```

---

## 7. CrewAI V3

> Complète la V2 §2 — RecallFlow déjà documenté. Cette section couvre guardrails+retry, mémoire LanceDB, hierarchical.

### 7.1 Guardrails — cascade + retry par guardrail

```python
# task.py — _invoke_guardrail_function()
def _invoke_guardrail_function(self, task_output, agent, tools, guardrail, guardrail_index=None):
    max_attempts = self.guardrail_max_retries + 1  # Défaut: 3 retries + 1 essai initial

    for attempt in range(max_attempts):
        guardrail_result = process_guardrail(
            output=task_output,
            guardrail=guardrail,
            retry_count=self._guardrail_retry_counts.get(guardrail_index, 0),
        )

        if guardrail_result.success:
            return task_output

        if attempt >= self.guardrail_max_retries:
            raise Exception(
                f"Task failed validation after {self.guardrail_max_retries} retries. "
                f"Last error: {guardrail_result.error}"
            )

        # Incrémenter le compteur PER GUARDRAIL (indépendant)
        current_retry_count += 1
        self._guardrail_retry_counts[guardrail_index] = current_retry_count

        # Régénérer la sortie depuis l'agent (retry réel)
        result = agent.execute_task(task=self, context=context, tools=tools)

# Application des guardrails en CASCADE :
if self._guardrails:
    for idx, guardrail in enumerate(self._guardrails):
        task_output = self._invoke_guardrail_function(
            task_output=task_output, guardrail=guardrail, guardrail_index=idx
        )
```

**GuardrailResult — interface simple :**

```python
class GuardrailResult(BaseModel):
    success: bool
    result: Any | None = None    # Résultat validé si success
    error: str | None = None     # Message d'erreur si échec

    @classmethod
    def from_tuple(cls, result: tuple[bool, Any | str]) -> Self:
        success, data = result
        return cls(success=success, result=data if success else None, error=data if not success else None)
```

### 7.2 Mémoire — LanceDB avec locking + retry exponentiel

```python
# memory/storage/lancedb_storage.py — save()
def save(self, records: list[MemoryRecord]) -> None:
    with store_lock(self._lock_name):  # Verrou pour accès concurrent
        self._ensure_table(vector_dim=dim)  # Auto-détection de dimension
        rows = [self._record_to_row(rec) for rec in records]

        # Remplir les vecteurs zéro si embeddings manquants
        for row in rows:
            if row["vector"] is None or len(row["vector"]) != self._vector_dim:
                row["vector"] = [0.0] * self._vector_dim

        self._do_write("add", rows)  # Max 5 retries exponentiels sur conflit commit

        if is_new_table:
            self._ensure_scope_index()  # Index sur scope pour recherche filtrée
            self._compact_if_needed()   # Compaction LanceDB
```

**Barrière drain_writes — cohérence lecture/écriture :**

```python
# memory/unified_memory.py — recall()
def recall(self, query, scope=None, depth="deep", ...) -> list[MemoryMatch]:
    self.drain_writes()  # Attendre que les saves en background soient terminés
    # Sans cela : recall après remember peut retourner des résultats obsolètes
    ...
```

### 7.3 Hierarchical process — manager automatique

```python
# crew.py — _create_manager_agent()
def _create_manager_agent(self) -> None:
    if self.manager_agent is not None:
        # Manager fourni explicitement
        self.manager_agent.allow_delegation = True
        if manager.tools:
            raise Exception("Manager agent should not have tools")
    else:
        # Création automatique
        manager = Agent(
            role=i18n.retrieve("hierarchical_manager_agent", "role"),
            goal=i18n.retrieve("hierarchical_manager_agent", "goal"),
            backstory=i18n.retrieve("hierarchical_manager_agent", "backstory"),
            tools=AgentTools(agents=self.agents).tools(),  # CLEF: délégation via tools
            allow_delegation=True,
            llm=self.manager_llm,
        )
    manager.crew = self
```

**Différence séquentiel vs hiérarchique :**

| Aspect | Sequential | Hierarchical |
|--------|-----------|--------------|
| Ordre des tasks | Strict (liste) | Dynamique (manager décide) |
| Context entre tasks | Propagé linéairement | Géré par le manager |
| Allocation | Statique (1 agent = 1 task) | Dynamique (manager choisit) |
| Tools du manager | N/A | `AgentTools(agents=all_workers).tools()` |

---

## 8. OpenAI Agents V3

> Complète la V2 §3 — Guardrails + Handoffs déjà documentés.

### 8.1 Lifecycle complet de run() — 3 phases

```python
# run.py — AgentRunner.run()

# PHASE 1 : SETUP
# - Résoudre RunState (reprise ou nouveau)
# - Initialiser TraceCtxManager (OpenTelemetry)
# - Créer SandboxRuntime (code execution agents)
# - Setup tool_use_tracker + prompt_cache_key_resolver

# PHASE 2 : MAIN LOOP
while True:
    # Guard maxTurns → MaxTurnsExceeded ou error_handler
    # Input guardrails : séquentiels PUIS parallèles avec le model task
    if current_turn <= 1:
        parallel_results, turn_result = await asyncio.gather(
            run_input_guardrails(...),
            run_single_turn(...),       # Model task lancé en parallèle
        )
    # Résultats → NextStep (FinalOutput | Handoff | Interruption | RunAgain)
    if isinstance(next_step, NextStepHandoff):
        current_agent = next_step.new_agent  # Switch agent, continue
    elif isinstance(next_step, NextStepInterruption):
        return build_interruption_result(...)  # Approvals requis
    # Session persistence après chaque turn
    if session_persistence_enabled:
        await save_result_to_session(session, ...)

# PHASE 3 : CLEANUP
# - Enqueue sandbox memory result
# - Cleanup SandboxRuntime
# - Finalize tracing spans
```

### 8.2 Streaming — asyncio.Queue + background task

```python
# run.py — run_streamed()
def run_streamed(self, agent, input, ...) -> RunResultStreaming:
    streamed_result = RunResultStreaming(
        _event_queue=asyncio.Queue(),      # Queue partagée
        is_complete=False,
        final_output=None,
    )

    # Lance le loop en BACKGROUND (l'appelant reçoit l'objet AVANT le démarrage)
    streamed_result.run_loop_task = asyncio.create_task(
        start_streaming(streamed_result=streamed_result, ...)
    )

    return streamed_result  # Immédiatement

# result.py — stream_events()
async def stream_events(self) -> AsyncIterator[StreamEvent]:
    while True:
        self._check_errors()
        if self.is_complete and self._event_queue.empty():
            break
        item = await self._event_queue.get()  # Bloque jusqu'à event
        if isinstance(item, QueueCompleteSentinel):
            break
        yield item
```

**Types d'events streamés :**

```python
# streaming.py — stream_step_items_to_queue()
for item in new_step_items:
    if isinstance(item, MessageOutputItem):
        event = RunItemStreamEvent(item=item, name="message_output_created")
    elif isinstance(item, ToolCallItem):
        event = RunItemStreamEvent(item=item, name="tool_called")
    elif isinstance(item, ToolCallOutputItem):
        event = RunItemStreamEvent(item=item, name="tool_output")
    elif isinstance(item, HandoffCallItem):
        event = RunItemStreamEvent(item=item, name="handoff_requested")
    # + ReasoningItem, MCPApprovalRequestItem, AgentUpdatedStreamEvent
    queue.put_nowait(event)  # Non-blocking
```

### 8.3 Tracing — 4 types de spans

```python
# run.py — Structure des spans

# 1. Task Span (wraps tout le run)
current_task_span = task_span(name=trace_workflow_name)
current_task_span.start(mark_as_current=True)

# 2. Agent Span (par agent, regroupe tous ses turns)
current_span = agent_span(
    name=current_agent.name,
    handoffs=[h.agent_name for h in handoffs],
    output_type=output_schema.name() or "str",
    tools=[get_tool_trace_name(t) for t in all_tools],
)

# 3. Turn Span (par turn, nested sous Agent Span)
current_turn_span = turn_span(turn=current_turn, agent_name=current_agent.name)

# 4. Function Span (par tool call, nested sous Turn Span)
with function_span(tool_name) as span:
    result = await invoke_function_tool(...)
```

**Erreur attachée à un span :**

```python
# Si max_turns dépassé
_error_tracing.attach_error_to_span(
    current_span,
    SpanError(message="Max turns exceeded", data={"max_turns": max_turns})
)
```

### 8.4 Tool execution — _FunctionToolBatchExecutor en 4 stages

```python
# run_internal/tool_execution.py — _FunctionToolBatchExecutor.execute()

# STAGE 1: Approval Resolution
for tool_run in tool_runs:
    approval_status = await resolve_approval_status(...)
    if approval_status is False:
        results[id(tool_run)] = function_rejection_item(...)  # Rejeté
    elif approval_status is None:
        return await handle_approval_interrupt(...)  # Pause → interruption

# STAGE 2: Input Guardrails
for tool_run in tool_runs:
    igr = await run_tool_input_guardrails(tool_run)
    if igr.tripwire_triggered:
        raise ToolInputGuardrailTripwireTriggered(...)

# STAGE 3: Parallel Execution avec tracing
invoke_tasks = {
    asyncio.create_task(
        with_tool_function_span(
            tool_name=tool_run.tool.name,
            fn=lambda span: invoke_function_tool(tool_run.tool, args, context_wrapper, span)
        )
    ): tool_run
    for tool_run in tool_runs
}
# await asyncio.wait() avec FIRST_COMPLETED
# Agrégation d'erreurs par priorité (Exception > CancelledError)

# STAGE 4: Output Guardrails
for result in results:
    ogr = await run_tool_output_guardrails(result)
    if ogr.tripwire_triggered:
        raise ToolOutputGuardrailTripwireTriggered(...)
```

**RunContextWrapper — suivi d'usage :**

```python
@dataclass
class RunContextWrapper(Generic[TContext]):
    context: TContext
    usage: Usage = field(default_factory=Usage)
    _approvals: dict[str, _ApprovalRecord] = field(default_factory=dict)

@dataclass
class Usage:
    requests: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    request_usage_entries: list[RequestUsage] = field(default_factory=list)

    def add(self, other: Usage) -> None:
        # Agrège usage depuis les requêtes séquentielles
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        if other.total_tokens > 0:
            self.request_usage_entries.append(RequestUsage(...))
```

---

## 9. agent-sandbox V3

> Section 20 V2 = 3 lignes. Cette section couvre l'implémentation complète.

### 9.1 Les 3 CRDs imbriquées

```go
// SandboxClaim — l'API que le client crée
type SandboxClaimSpec struct {
    TemplateRef SandboxTemplateRef   // Quel template utiliser
    Lifecycle   *Lifecycle           // TTL + ShutdownPolicy
    WarmPool    *WarmPoolPolicy      // "none" | "default" | "pool-name"
    Env         []EnvVar             // Injection dynamique d'env vars
}

// SandboxTemplate — réutilisable, sécurisé par défaut
type SandboxTemplateSpec struct {
    PodTemplate          sandboxv1alpha1.PodTemplate
    NetworkPolicy        *NetworkPolicySpec     // Ingress + Egress rules
    EnvVarsInjectionPolicy string              // "Allowed" | "Overrides" | "Disallowed"
}

// SandboxWarmPool — pool de pods pré-alloués
type SandboxWarmPoolSpec struct {
    Replicas       int32                // Nombre de pods en attente
    TemplateRef    SandboxTemplateRef
    UpdateStrategy *SandboxWarmPoolUpdateStrategy  // "Recreate" | "OnReplenish"
}
```

### 9.2 Warm Pool Reconciler — logique de tri

```go
// Suppression priorisée : unready first, puis newest first
slices.SortFunc(activeSandboxes, func(a, b Sandbox) int {
    aReady, bReady := isSandboxReady(&a), isSandboxReady(&b)
    if aReady != bReady {
        return cmp(aReady, bReady)  // unready en premier
    }
    return cmpByCreationTime(a, b)  // newest en premier (LIFO)
})

// Grace period : 5 min hardcoded (non configurable)
const warmPoolReadinessGracePeriod = 5 * time.Minute
for _, sb := range activeSandboxes {
    if !isSandboxReady(&sb) && age(sb) > warmPoolReadinessGracePeriod {
        r.Delete(ctx, &sb)
    }
}
```

### 9.3 Lifecycle policies

| Policy | Comportement | Usage |
|--------|-------------|-------|
| `Retain` (défaut) | Laisse le pod en place après TTL expiry | Audit post-mortem |
| `Delete` | Suppression immédiate | Production normale |
| `DeleteForeground` | Attend la terminaison du pod | Cleanup gracieux |

---

## 10. pixel-agents V3

> Section 20 V2 = 2 lignes. Architecture complète de détection d'activité.

### 10.1 Dual-mode detection

```typescript
/**
 * HOOKS MODE (preferred):
 *   Claude Code Hooks API → SessionStart, SessionEnd, PermissionRequest, Stop
 *   Instant + reliable, supprime les timers heuristiques
 *
 * HEURISTIC MODE (fallback):
 *   - Per-agent 500ms JSONL polling (fichier transcript)
 *   - 1s main scanner (terminal adoption)
 *   - 3s external scanner (VS Code panel sessions)
 *   - 30s stale check (orphaned external agents)
 */
```

### 10.2 Tool → Animation mapping

```typescript
// Parsing du JSONL transcript
switch (record.type) {
    case 'PreToolUse':
        agent.activeToolIds.add(record.tool_use_id);
        if (record.name === 'claude-interaction') {
            webview?.postMessage({ type: 'updateCharacter', id: agentId, state: 'TYPE' });
        }
        break;
    case 'ToolResult':
        agent.activeToolIds.delete(toolId);
        if (agent.activeToolIds.size === 0) {
            // Aucun tool actif → retour IDLE
            webview?.postMessage({ type: 'updateCharacter', id: agentId, state: 'IDLE' });
        }
        break;
    case 'PermissionRequest':
        webview?.postMessage({ type: 'setPermission', id: agentId, pending: true });
        // Timer permission : 7s
        break;
}

// Token tracking par agent
if (record.type === 'Message') {
    agent.inputTokens += record.input_tokens || 0;
    agent.outputTokens += record.output_tokens || 0;
}
```

### 10.3 Colorisation pixel art — Photoshop palette shift

```typescript
// Luminance perçue (formule standard)
let lightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

// Contraste : expansion/compression autour de 0.5
const factor = (100 + c) / 100;
lightness = 0.5 + (lightness - 0.5) * factor;

// Convertit HSL → RGB → hex
const hex = hslToHex(h, s / 100, lightness);
```

---

## 11. OpenMythos V3

> Section 20 V2 = 3 lignes. Architecture RDT complète.

### 11.1 Architecture Prelude → Recurrent → Coda

```python
class OpenMythos(nn.Module):
    def forward(self, input_ids, n_loops=None, kv_cache=None, start_pos=0):
        x = self.embed(input_ids)

        # PRELUDE : 2 blocs transformer standard
        for i, layer in enumerate(self.prelude):
            x = layer(x, freqs_cis, mask, kv_cache, cache_key=f"prelude_{i}")

        # RECURRENT : 1 bloc loopé n_loops fois (variable à l'inférence !)
        e = x  # Input congelé — injecté à chaque itération
        x = self.recurrent(x, e, freqs_cis, mask, n_loops, kv_cache)

        # CODA : 2 blocs transformer standard
        for i, layer in enumerate(self.coda):
            x = layer(x, freqs_cis, mask, kv_cache, cache_key=f"coda_{i}")

        return self.head(self.norm(x))  # Weight tying avec embed
```

### 11.2 LTI Injection — stabilité garantie

```python
class LTIInjection(nn.Module):
    """
    h_{t+1} = A·h_t + B·e + transformer_out
    Spectral radius ρ(A) < 1 garanti par construction via ZOH discretization.
    """
    def __init__(self, dim: int):
        self.log_A = nn.Parameter(torch.zeros(dim))
        self.log_dt = nn.Parameter(torch.zeros(1))
        self.B = nn.Parameter(torch.ones(dim) * 0.1)

    def get_A(self) -> torch.Tensor:
        # A_discrete = exp(-exp(log_dt + log_A)) → toujours dans (0, 1)
        return torch.exp(-torch.exp((self.log_dt + self.log_A).clamp(-20, 20)))

    def forward(self, h, e, transformer_out):
        A = self.get_A()
        return A * h + self.B * e + transformer_out
```

**Pourquoi c'est important :** Sans cette contrainte, le spectral radius de A peut être ≥ 1, causant une explosion du gradient lors du backpropagation à travers les boucles récurrentes.

### 11.3 ACT Halting — sortie variable par position

```python
# RecurrentBlock.forward()
for t in range(n_loops):
    # ... transformer + LoRA + LTI ...
    p = self.act(h)  # Probabilité de halting par position (B, T)

    remainder = (1.0 - cumulative_p).clamp(min=0)
    weight = torch.where(
        cumulative_p + p >= self.cfg.act_threshold,  # 0.99
        remainder,   # masse restante (final step)
        p,           # probabilité courante
    )

    h_out = h_out + weight.unsqueeze(-1) * h  # Somme pondérée
    cumulative_p = cumulative_p + p * (~halted).float()
    halted = halted | (cumulative_p >= self.cfg.act_threshold)

    if halted.all() and kv_cache is None:
        break  # Early exit si toutes les positions ont halted
```

**Inference depth extrapolation :**

```python
# Entraîné sur max_loop_iters=16, peut inférer avec n_loops=32
logits_deep = model(ids, n_loops=32)
# LoRA scale clampé au dernier index → extrapolation approximative
```

### 11.4 MoE FFN — DeepSeek-V3 aux-loss-free balancing

```python
class MoEFFN(nn.Module):
    def forward(self, x):
        # Logits de routing (unbiased pour le gradient)
        logits = self.router(flat)
        scores = F.softmax(logits, dim=-1)

        # Top-K selection avec biais (n'affecte pas le gradient)
        _, topk_idx = (logits + self.router_bias).topk(self.topk, dim=-1)
        topk_scores = scores.gather(-1, topk_idx)
        topk_scores = topk_scores / topk_scores.sum(dim=-1, keepdim=True)

        # Dispatch + weighted sum (64 routed + 2 shared always-on)
        out = torch.zeros_like(flat)
        for i in range(self.topk):
            for eid in range(self.n_experts):
                mask = expert_ids == eid
                if mask.any():
                    out[mask] += topk_scores[mask, i:i+1] * self.routed_experts[eid](flat[mask])

        for shared in self.shared_experts:
            out = out + shared(flat)  # Toujours actifs
```

---

## 12. Haystack V3

> Complète la V2 §6 — Typed sockets déjà documentés.

### 12.1 ConditionalRouter — Jinja2 sandboxé + AST eval

```python
# components/routers/conditional_router.py
for route in self.routes:
    t = self._env.from_string(route["condition"])
    rendered = t.render(**kwargs)

    if not self._unsafe:
        # AST literal_eval : évalue UNIQUEMENT des littéraux Python
        # Sécurité : bloque imports, builtins dangereux
        rendered = ast.literal_eval(rendered)

    if not rendered:
        continue  # Cette route ne correspond pas

    output_value = t_output.render(**kwargs)
    if not self._unsafe:
        with contextlib.suppress(Exception):
            output_value = ast.literal_eval(output_value)

    if self._validate_output_type:
        if not self._output_matches_type(output_value, output_type):
            raise ValueError(...)

    return {output_name: output_value}

raise NoRouteSelectedException(...)  # Aucune route ne correspond
```

**Sécurité :**
- `unsafe=False` (défaut) : `SandboxedEnvironment()` → bloque RCE
- `unsafe=True` : `NativeEnvironment()` → RCE possible → usage interne uniquement
- `optional_variables` → fallback None si variable manquante

### 12.2 Error handling — PipelineRuntimeError

```python
# core/pipeline/base.py
try:
    component_outputs = self._run_component(component_name, inputs, ...)
except Exception as error:
    raise PipelineRuntimeError.from_exception(component_name, type(instance), error)
    # Wraps avec contexte : "Component 'X' (Y) failed: Z"

# Limites :
# - Pas de retry built-in au niveau pipeline
# - Erreur = cascade failure immédiate
# - max_runs_per_component = 100 (anti-boucle infinie)
```

**Classe PipelineComponentsBlockedError :** détecte les deadlocks (tous les composants bloqués).

### 12.3 Sérialisation YAML — SafeLoader avec tuples

```python
# marshal/yaml.py
class YamlLoader(yaml.SafeLoader):
    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

class YamlDumper(yaml.SafeDumper):
    def represent_tuple(self, data):
        return self.represent_sequence("tag:yaml.org,2002:python/tuple", data)

# SafeLoader uniquement → pas de pickle → pas de RCE via YAML
```

**Introspection automatique pour les composants sans to_dict() :**

```python
for param_name, param in inspect.signature(obj.__init__).parameters.items():
    try:
        param_value = getattr(obj, param_name)
    except AttributeError:
        if param.default is param.empty:
            raise SerializationError(f"Cannot find value for {param_name}")
        continue  # Utilise le défaut
```

### 12.4 OpenTelemetry — opt-in pour le contenu sensible

```python
# tracing/opentelemetry.py
class OpenTelemetryTracer(Tracer):
    @contextlib.contextmanager
    def trace(self, operation_name, tags=None, parent_span=None):
        with self._tracer.start_as_current_span(operation_name) as raw_span:
            span = OpenTelemetrySpan(raw_span)
            if tags:
                span.set_tags(tags)
            yield span

# Pipeline tags :
with tracing.tracer.trace("haystack.pipeline.run", tags={
    "haystack.pipeline.input_data": data,       # Opt-in via env var
    "haystack.pipeline.output_data": outputs,   # HAYSTACK_CONTENT_TRACING_ENABLED
}) as span:
    with PipelineBase._create_component_span(component_name, ...) as span:
        span.set_content_tag(_COMPONENT_INPUT, inputs)  # Opt-in
        component_output = instance.run(**inputs)
        span.set_content_tag(_COMPONENT_OUTPUT, component_output)
```

---

## 13. Dify V3

> Complète la V2 §7 — graphon adapter + Celery déjà documentés. Cette section couvre le pipeline RAG.

### 13.1 Chunking — TextSplitter configurable

```python
# core/rag/splitter/text_splitter.py
class TextSplitter:
    def __init__(
        self,
        chunk_size: int = 4000,       # En CARACTÈRES (pas tokens !)
        chunk_overlap: int = 200,     # 5% de 4000
        length_function: Callable = lambda x: [len(x) for x in x],  # Custom → token-based
        keep_separator: bool = False,
        add_start_index: bool = False,
    ):
        if chunk_overlap > chunk_size:
            raise ValueError("overlap must be < size")
```

**Nettoyage avant chunking :**

```python
# core/rag/cleaner/clean_processor.py
class CleanProcessor:
    @classmethod
    def clean(cls, text: str, process_rule: dict) -> str:
        # Systématique : chars de contrôle, délimiteurs invalides, Unicode poison
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F\xEF\xBF\xBE]", "", text)
        text = re.sub("￾", "", text)  # Unicode FFFE = poison

        # Optionnel via rules :
        # remove_extra_spaces → collapse \n{3,} et whitespace multiple
        # remove_urls_emails → placeholder strategy : protect markdownlinks, remove bare URLs
```

### 13.2 Retrieval hybride — ThreadPoolExecutor + fail-fast

```python
# core/rag/retrieval/datasource/retrieval_service.py
def _retrieve(self, retrieval_method, dataset, ...):
    with ThreadPoolExecutor(max_workers=RETRIEVAL_SERVICE_EXECUTORS) as executor:
        futures = []

        # Keyword search
        if RetrievalMethod.KEYWORD_SEARCH or HYBRID_SEARCH:
            futures.append(executor.submit(self.keyword_search, ...))

        # Semantic search (text + image optionnel)
        if RetrievalMethod.is_support_semantic_search(retrieval_method):
            if query:
                futures.append(executor.submit(self.embedding_search, query_type=QueryType.TEXT_QUERY, ...))
            if attachment_id:
                futures.append(executor.submit(self.embedding_search, query_type=QueryType.IMAGE_QUERY, ...))

        # Full-text index
        if RetrievalMethod.is_support_fulltext_search(retrieval_method):
            futures.append(executor.submit(self.full_text_index_search, ...))

        # Fail-fast : 1 thread exception → annule tous les autres
        for future in concurrent.futures.as_completed(futures, timeout=300):
            if future.exception():
                for f in futures:
                    f.cancel()
                break
```

### 13.3 Déduplication hybride — O(n) avec score-based merging

```python
def _deduplicate_documents(documents: list[Document]) -> list[Document]:
    chosen: dict[tuple, Document] = {}
    order: list[tuple] = []

    for doc in documents:
        is_dify = doc.provider == "dify"
        doc_id = (doc.metadata or {}).get("doc_id") if is_dify else None

        if is_dify and doc_id:
            key = ("dify", doc_id)
            if key not in chosen:
                chosen[key] = doc; order.append(key)
            else:
                # Si doc apparaît via keyword ET semantic → garder le plus haut score
                if doc.metadata.get("score", 0) > chosen[key].metadata.get("score", 0):
                    chosen[key] = doc
        else:
            # Déduplication par contenu pour les sources non-Dify
            content_key = (doc.provider or "dify", doc.page_content)
            if content_key not in chosen:
                chosen[content_key] = doc; order.append(content_key)

    return [chosen[k] for k in order]  # Preservation d'ordre de première apparition
```

### 13.4 Reranking — 2 modes

**Mode pondéré (BM25 + cosine, sans API) :**

```python
# core/rag/rerank/weight_rerank.py
score = (
    self.weights.vector_setting.vector_weight * query_vector_score +
    self.weights.keyword_setting.keyword_weight * query_score
)
# Déterministe, rapide, sans API externe
```

**Mode model-based (cross-encoder, avec API) :**

```python
# core/rag/rerank/rerank_model.py
# Multimodal si le modèle supporte vision (image queries)
if not is_support_vision:
    rerank_result = self.fetch_text_rerank(query, documents, ...)
else:
    rerank_result = self.fetch_multimodal_rerank(query, documents, ...)
```

**DataPostProcessor — orchestration reranking + reordering :**

```python
class DataPostProcessor:
    def invoke(self, query, documents, score_threshold=None, top_n=None):
        if self.rerank_runner:
            documents = self.rerank_runner.run(query, documents, score_threshold, top_n)
        if self.reorder_runner:
            documents = self.reorder_runner.run(documents)  # Lost In The Middle mitigation
        return documents
```

---

## Partie III — Synthèse transversale V3

---

## 14. Patterns d'erreur et récupération

### 14.1 Matrice des approches par framework

| Framework | Retry | Timeout | Circuit breaker | State recovery |
|-----------|-------|---------|-----------------|----------------|
| **CrewAI** | `guardrail_max_retries=3` par guardrail | `max_execution_time` par agent | Non | `RunState` sérialisable |
| **OpenAI Agents** | Non (caller) | Non (asyncio.timeout wrapper) | `max_turns` | `RunState` + checkpointer |
| **LangGraph** | Non (node) | Non (node) | `max_steps` | Checkpoint complet (replay exact) |
| **Shannon** | Temporal retry policy (50 attempts, 5-30 min) | SDK interne | Spending cap detection | Git checkpoints par agent |
| **Haystack** | Non (pipeline) | Non (composant) | `max_runs_per_component=100` | Non |
| **Dify** | ThreadPool fail-fast + cancel | 300s timeout | Non | Celery queue (persistente) |
| **agent-sandbox** | Reconciler (K8s natif) | Grace period 5 min | Non | CRD status conditions |
| **Octogent** | Non | `MAX_ITERATIONS=50` | Non | SQLite sessions |

### 14.2 Patterns universels identifiés

**Pattern 1 — Checkpoint avant/après (Shannon, LangGraph, CrewAI)**
```
git commit "pre-{agent}-attempt-{N}"  →  exécution  →  git commit "{agent}-complete"
```

**Pattern 2 — Circuit breaker par compteur (tous)**
```python
MAX_TURNS = 50  # OpenAI Agents
MAX_STEPS = 100  # LangGraph
MAX_ITERATIONS = 50  # Octogent
max_runs_per_component = 100  # Haystack
```

**Pattern 3 — Error wrapping avec contexte (Haystack, Shannon)**
```python
raise PipelineRuntimeError.from_exception(component_name, type(instance), error)
# → "Component 'X' (Y) failed: Z" — jamais d'exception nue
```

**Pattern 4 — Fail-fast avec cancel (Dify, OpenAI Agents)**
```python
# Dès qu'une task échoue → cancel toutes les autres → raise immédiatement
for future in as_completed(futures):
    if future.exception():
        for f in futures: f.cancel()
        break
```

---

## 15. Architectures de skill — 4 modèles

### 15.1 Comparaison complète

| Modèle | Exemple | Activation | Granularité | Multi-agent |
|--------|---------|-----------|------------|-------------|
| **Guidelines globales** | karpathy-skills | Toujours (CLAUDE.md) | Comportement LLM | Non |
| **Library thématique** | claude-skills | Contextuelle (auto-detect) | Expertise domaine | Non |
| **Workflow pipeline** | superpowers | Hook-triggered | Phase projet | Oui (dispatch) |
| **Platform + SDK** | openclaw | Manifest + registry | Plugin capability | Oui (channels) |

### 15.2 Quand utiliser quel modèle

```
Besoin de discipliner la qualité du code ?
  → Guidelines globales (karpathy-skills pattern)
  → SKILL.md injecté via CLAUDE.md

Besoin d'expertise domaine spécialisée ?
  → Library thématique (claude-skills pattern)
  → 66 skills catégorisés, activation contextuelle, decision trees

Besoin d'orchestrer un processus multi-étapes avec approbations ?
  → Workflow pipeline (superpowers pattern)
  → Gating humain, subagents, TDD mandatory, persistent artifacts

Besoin d'une plateforme multi-channel extensible ?
  → Platform + SDK (openclaw pattern)
  → Plugin manifests, ClawHub registry, core agnostique
```

---

## 16. Sécurité agentique — ASI01-ASI10 avec défenses

### 16.1 Modèles de menace implémentés

```python
# Défense ASI01 (Goal Hijack) — vérification cohérence
class GoalConsistencyValidator:
    def validate(self, action: str, current_goal: str) -> bool:
        allowed_actions = self.goal_to_actions_map.get(current_goal, set())
        return action in allowed_actions

# Défense ASI03 (Identity Abuse) — credentials scopés + TTL
class NHICredentialManager:
    def issue_credential(self, agent_id: str, scopes: list[str], ttl_minutes: int = 15):
        token = jwt.encode({"agent_id": agent_id, "scopes": scopes,
                           "exp": now() + timedelta(minutes=ttl_minutes)}, secret)
        return token  # Expire automatiquement

# Défense ASI04 (Supply Chain) — allowlist MCP
ALLOWED_MCP_SERVERS = {"filesystem", "git", "fetch", "memory"}
def connect_mcp(server_name: str) -> bool:
    if server_name not in ALLOWED_MCP_SERVERS:
        raise MCPServerNotAllowed(server_name)

# Défense ASI06 (Memory Poisoning) — lineage + hash
class MemoryLineageTracker:
    def record_write(self, key: str, value: Any, source: str, agent_id: str):
        self.ledger[key] = {"hash": hashlib.sha256(str(value).encode()).hexdigest(),
                           "source": source, "agent": agent_id, "ts": now()}
    def verify(self, key: str, value: Any) -> bool:
        expected_hash = self.ledger.get(key, {}).get("hash")
        return expected_hash == hashlib.sha256(str(value).encode()).hexdigest()

# Défense ASI07 (Inter-Agent Communication) — message signing
class SignedAgentMessage:
    def sign(self, payload: dict, private_key: str) -> str:
        return jwt.encode({"payload": payload, "from": self.agent_id}, private_key)
    def verify(self, token: str, expected_sender: str, public_keys: dict) -> dict:
        data = jwt.decode(token, public_keys[expected_sender])
        assert data["from"] == expected_sender
        return data["payload"]
```

### 16.2 Cas réels documentés dans LLMSecurityGuide

| Cas | Attaque | Impact |
|-----|---------|--------|
| **EchoLeak (CVE-2025-32711)** | Exfiltration mémoire via prompt injection dans GitHub Copilot | Données sensibles exposées à l'attaquant |
| **DeepSeek R1 jailbreaks** | Contournement des guardrails via encodage multi-step | Génération de contenu interdit |
| **Premier serveur MCP malveillant** | Serveur MCP forge les résultats d'outils pour rediriger l'agent | ASI04 + ASI01 combinés |
| **Samsung data leak** | Développeurs collent du code propriétaire dans ChatGPT | ASI09 — confiance excessive |

---

## 17. Stack complète V3

### Stack de production recommandée (mise à jour)

```
┌─ ORCHESTRATION ─────────────────────────────────────────────┐
│  LangGraph (StateGraph) pour workflows complexes déterministes│
│  OpenAI Agents (Handoffs) pour pipelines avec guardrails     │
│  Raison V3 : LangGraph = replay exact (version-based sync),  │
│             OpenAI = 4-stage tool execution avec validation   │
└──────────────────────────────────────────────────────────────┘

┌─ MÉMOIRE ────────────────────────────────────────────────────┐
│  CrewAI UnifiedMemory (LanceDB) pour mémoire sémantique      │
│  mempalace pour RAG verbatim long-context (96.6% R@5)        │
│  Raison V3 : LanceDB = store_lock + retry exponentiel +      │
│             drain_writes pour cohérence lecture/écriture      │
└──────────────────────────────────────────────────────────────┘

┌─ RETRIEVAL (RAG) ────────────────────────────────────────────┐
│  Dify pour multi-tenant avec retrieval hybride               │
│  Haystack pour pipelines composables avec routing Jinja2     │
│  Raison V3 : Dify = ThreadPool parallèle + dedup score-based │
│             Haystack = ConditionalRouter sandboxé + OTel     │
└──────────────────────────────────────────────────────────────┘

┌─ SÉCURITÉ ───────────────────────────────────────────────────┐
│  Implémenter ASI01-ASI10 (OWASP Agentic 2026)               │
│  GoalConsistencyValidator (ASI01)                            │
│  NHI credentials scopés + TTL (ASI03)                       │
│  MCP allowlist (ASI04)                                       │
│  MemoryLineageTracker + hash (ASI06)                         │
│  SignedAgentMessage (ASI07)                                  │
│  AgentBehaviorMonitor + quarantine (ASI10)                   │
└──────────────────────────────────────────────────────────────┘

┌─ OBSERVABILITÉ ──────────────────────────────────────────────┐
│  Langfuse (traces + spans + cost tracking)                   │
│  OpenTelemetry (standardisation)                             │
│  pixel-agents pour visualisation temps-réel (optionnel)      │
│  Raison V3 : Langfuse = schéma complet tokens/coût/scores   │
└──────────────────────────────────────────────────────────────┘

┌─ COMPRESSION CONTEXTE ──────────────────────────────────────┐
│  LLMLingua v2 (3 niveaux, xlm-roberta-large)                │
│  Raison V3 : v2 plus rapide que v1 en production            │
└──────────────────────────────────────────────────────────────┘

┌─ INFRASTRUCTURE ─────────────────────────────────────────────┐
│  kagent (K8s) : CRD déclaratif + skills-as-images            │
│  agent-sandbox (K8s) : Warm pool + NetworkPolicy sécurisé    │
│  Shannon (pentesting) : Temporal + Claude SDK + git checkpts │
│  Raison V3 : agent-sandbox = ~90% réduction startup time     │
│             Shannon = pattern pour agents autonomes durables  │
└──────────────────────────────────────────────────────────────┘

┌─ QUALITÉ ET GOUVERNANCE ─────────────────────────────────────┐
│  karpathy-skills : 4 principes comportementaux LLM           │
│  superpowers : pipeline multi-stage avec gating humain       │
│  LLMSecurityGuide : OWASP Agentic Top 10 comme checklist     │
│  Raison V3 : superpowers = seul framework qui adresse         │
│             explicitement le "agent slop" avec 94% reject     │
└──────────────────────────────────────────────────────────────┘
```

### Stack minimale viable V3 (startup/solo)

```
Orchestration    : LangGraph (streams + checkpoints natifs)
Mémoire          : CrewAI memory (SQLite via LanceDB, 0 infra)
Guardrails       : Pattern OpenAI (copier guardrail.py)
RAG              : Haystack InMemory + ConditionalRouter
Observabilité    : Langfuse cloud (free tier)
Sécurité         : ASI01 + ASI04 + ASI06 (minimum vital)
Qualité          : karpathy-skills injecté via CLAUDE.md
```

---

## Conclusion V3

La V3 révèle 3 niveaux d'enseignement que V1 et V2 ne couvraient pas :

**Niveau 1 — Infrastructure production-ready (nouveau en V3) :**
- `shannon` prouve qu'un système de pentest autonome est réalisable avec 13 agents Temporal + Claude SDK
- `agent-sandbox` montre que le Kubernetes warm pool résout le cold start problem (~90% réduction)
- `openclaw` démontre qu'une platform multi-channel complète est faisable avec Plugin SDK + manifest contracts

**Niveau 2 — Détails d'implémentation critiques (approfondis en V3) :**
- LangGraph : 7 stream modes, 3 channel types avec sémantiques de conflit différentes
- OpenAI Agents : tool execution en 4 stages (approval → input guardrails → parallel → output guardrails)
- CrewAI : retries per-guardrail (pas global), drain_writes pour cohérence mémoire
- vscode-copilot-chat : hooks = processus externes (pas des callbacks) — architectural pattern réutilisable

**Niveau 3 — Sécurité et gouvernance agentique (absent des V1+V2) :**
- OWASP Agentic Top 10 (ASI01-ASI10) = référence 2026 pour les systèmes multi-agents
- EchoLeak CVE-2025-32711 = premier exploit réel sur un système agentique commercial
- karpathy-skills + superpowers = seuls frameworks qui s'attaquent au "agent slop" problem

**La leçon V3 :** Les frameworks traitent l'orchestration. La gouvernance, la qualité, et la sécurité restent la responsabilité du système qui les orchestre — et aucun framework ne les offre out-of-the-box.

---

*V3 — 8 agents Explore parallèles lancés le 2026-04-26.*
*Fichiers lus en V3 : `hookExecutor.ts`, `toolCallingLoop.ts`, `temporal/workflows.ts`, `agent-execution.ts`, `claude-executor.ts`, `prompt-manager.ts`, `RecurrentBlock.py`, `LTIInjection.py`, `MoEFFN.py`, `conditional_router.py`, `text_splitter.py`, `retrieval_service.py`, `weight_rerank.py`, `sandbox_claim_controller.go`, `warm_pool_reconciler.go`, `last_value.py`, `topic.py`, `binop.py`, `_messages.py`, `run.py` (AgentRunner), `tool_execution.py`, et 40+ autres.*
