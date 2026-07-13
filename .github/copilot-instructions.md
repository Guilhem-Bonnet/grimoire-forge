<!-- Grimoire:START -->
# Grimoire — Project Instructions

## Project Configuration

- **Project**: grimoire-forge
- **User**: Guilhem
- **Communication Language**: Français
- **Document Output Language**: Français
- **User Skill Level**: expert
- **Output Folder**: {project-root}/_grimoire-runtime-output
- **Planning Artifacts**: {project-root}/_grimoire-runtime-output/planning-artifacts
- **Implementation Artifacts**: {project-root}/_grimoire-runtime-output/implementation-artifacts
- **Project Knowledge**: {project-root}/docs

## Grimoire Runtime Structure

- **Agent definitions**: `_grimoire-runtime/bmm/agents/` (BMM module) and `_grimoire-runtime/core/agents/` (core)
- **Workflow definitions**: `_grimoire-runtime/bmm/workflows/` (organized by phase)
- **Core tasks**: `_grimoire-runtime/core/tasks/` (help, editorial review, indexing, sharding, adversarial review)
- **Core workflows**: `_grimoire-runtime/core/workflows/` (brainstorming, party-mode, advanced-elicitation)
- **Workflow engine**: `_grimoire-runtime/core/tasks/workflow.xml` (executes YAML-based workflows)
- **Module configuration**: `_grimoire-runtime/bmm/config.yaml`
- **Core configuration**: `_grimoire-runtime/core/config.yaml`
- **Agent manifest**: `_grimoire-runtime/_config/agent-manifest.csv`
- **Workflow manifest**: `_grimoire-runtime/_config/workflow-manifest.csv`
- **Help manifest**: `_grimoire-runtime/_config/grimoire-help.csv`
- **Agent memory**: `_grimoire-runtime/_memory/`

## Key Conventions

- Always load `_grimoire-runtime/bmm/config.yaml` before any agent activation or workflow execution
- Store all config fields as session variables: `{user_name}`, `{communication_language}`, `{output_folder}`, `{planning_artifacts}`, `{implementation_artifacts}`, `{project_knowledge}`
- MD-based workflows execute directly — load and follow the `.md` file
- YAML-based workflows require the workflow engine — load `workflow.xml` first, then pass the `.yaml` config
- Follow step-based workflow execution: load steps JIT, never multiple at once
- Save outputs after EACH step when using the workflow engine
- The `{project-root}` variable resolves to the workspace root at runtime
- **Documentation charter**: Avant de créer ou modifier un fichier `.md`, charger `_grimoire-runtime/_memory/tech-writer-sidecar/documentation-standards.md` et respecter la charte (CommonMark, style guide, quality checklist)
- **Documentation companions**: Tout package de livrable sous `_grimoire-runtime-output/planning-artifacts/` doit inclure une `DOC-TECHNIQUE-<slug>.md` et une `GUIDE-utilisation-<slug>.md`; toute modification de package doit revalider ces deux compagnons avant cloture.
- **Autonomy protocols**: L'orchestrateur applique ALS (Autonomy Level System), Session Momentum, et Friction Budget. Voir `grimoire-kit/framework/agent-base.md` et `grimoire-kit/framework/orchestrator-gateway.md`. PIP (initiative proactive) est en statut observer-only (non instrumenté — cartographie 2026-04-21) ; AORA et DCF sont retirés (aucun artefact exécutable, purge du 2026-07-12, voir `_grimoire-runtime-output/planning-artifacts/durcissement-agentique-20260712/`).
- **Completion discipline**: Si une tâche révèle une suite logique alignée avec l'objectif courant et restant en risque L1/L2, l'agent doit l'exécuter dans le même tour. Ne proposer des prochaines étapes qu'en cas de blocage, de changement d'objectif, ou pour du travail optionnel, exploratoire, ou L3+.
- **Activation SOG**: Si le premier message utilisateur contient déjà une demande actionable, le master ne doit pas afficher le menu ni attendre une sélection; il doit traiter la demande directement. Le menu n'est montré que lors d'une activation sans tâche explicite.
- **Stability guard**: Pour éviter les crashs de l'extension host VSCode, respecter ces limites : jamais de grep_search sans `includePattern` ciblé, toujours un timeout raisonnable sur les commandes terminal. Le file watcher est configuré pour exclure `.venv`, `__pycache__`, `.pytest_cache`, `.ruff_cache` etc. (voir `.vscode/settings.json`).
- **Terminal lifecycle guard**: Pour chaque commande terminal en background, conserver l'ID, suivre son état via `await_terminal` ou `get_terminal_output`, puis appeler `kill_terminal` dès que le process n'est plus utile. Ne jamais garder plusieurs terminaux background pour le même objectif.
- **Terminal recovery guard**: Si un shell `/usr/bin/zsh` se termine avec code 1 sans diagnostic exploitable, relancer une fois dans un shell propre (`zsh -f`) avant d'escalader.
- **Hooks vs tasks**: Les hooks natifs VS Code/Copilot couvrent le cycle agent (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Subagent*`, `Stop`) mais pas `tasks.json`; l'orchestration et la preuve task-level restent deleguees a `.github/hooks/scripts/grimoire-task-flow.sh` et `.vscode/tasks.json`.
- **Hook promotion guard**: Les hooks workspace et agent passent par `.github/hooks/scripts/grimoire-hook-gateway.sh` avec registre `_grimoire-runtime/_config/hook-safety-registry.json`; si le script cible ou sa surface de controle change apres validation, le hook est degrade en mode non bloquant (`shadow` ou `canary`) jusqu'a `grimoire: hooks-promote`. Les bascules manuelles passent par `hook-safety-gate.py set-mode ...` ou les tasks `grimoire: hooks-shadow` / `grimoire: hooks-canary`. Tout hook nouveau doit etre branche via le gateway et declare dans le registre, sinon `hooks-status` et `grimoire-hooks-smoke.sh` echouent.

## Available Agents

> **Architecture SOG (BM-53)** : Un seul agent est exposé à l'utilisateur — le Grimoire Master Orchestrator.
> Tous les autres agents fonctionnent comme sub-agents invisibles, dispatchés automatiquement
> par l'orchestrateur selon l'intention détectée. Voir `grimoire-kit/framework/orchestrator-gateway.md`.

| Agent | Persona | Title | Capabilities |
|---|---|---|---|
| grimoire-master | Grimoire Master | Smart Orchestrator Gateway — Point d'entrée unique | orchestration SOG, dispatch intelligent, anti-hallucination HUP, escalation QEC, validation CVTL, party mode PCE, autonomy ALS |

### Sub-agents internes (invisibles à l'utilisateur)

L'orchestrateur dispatche automatiquement vers ces agents selon le besoin :

#### BMM — Méthode Grimoire

| Sub-agent | Persona | Outils | Handoffs | Spécialité |
|---|---|---|---|---|
| analyst | Mary | read, search | pm, architect | Business analysis, requirements |
| architect | Winston | read, edit, search | dev, sm | Architecture, infrastructure |
| dev | Amelia | read, edit, search, execute | qa, tea | Implémentation, TDD |
| pm | John | read, edit, search | architect, sm, ux-designer | Product management, PRD |
| qa | Quinn | read, search, execute | dev, tech-writer | Tests, QA |
| quick-flow-solo-dev | Barry | read, edit, search, execute | qa | Rapid spec + implementation |
| sm | Bob | read, edit, search | dev, qa | Scrum, stories, backlog |
| tech-writer | Paige | read, edit, search | — | Documentation |
| ux-designer | Sally | read, search | — | UX/UI design |

#### BMB — Builders

| Sub-agent | Persona | Outils | Spécialité |
|---|---|---|---|
| agent-builder | Bond | read, edit, search | Création d'agents Grimoire |
| module-builder | Morgan | read, edit, search | Création de modules |
| workflow-builder | Wendy | read, edit, search | Création de workflows |

#### CIS — Créativité et Innovation

| Sub-agent | Persona | Outils | Spécialité |
|---|---|---|---|
| brainstorming-coach | Carson | read, search | Brainstorming, idéation |
| creative-problem-solver | Dr. Quinn | read, search | TRIZ, problem solving |
| design-thinking-coach | Maya | read, search | Design thinking |
| art-director | Iris | read, edit, search | Direction artistique pixel, hero FX, room kits, review de style |
| innovation-strategist | Victor | read, search | Innovation, Blue Ocean |
| presentation-master | Caravaggio | read, edit, search | Présentations, pitch decks |
| rodin | Rodin | read, edit, search | Débats socratiques, anti-chambre d'écho |
| storyteller | Sophia | read, search | Narratives, storytelling |

#### TEA — Test Architecture

| Sub-agent | Persona | Outils | Handoffs | Spécialité |
|---|---|---|---|---|
| tea | Murat | read, search, execute | dev, qa | Test architecture, ATDD, CI/CD |

## Agent Lifecycle Hooks

| Hook | Événement | Action |
|---|---|---|
| grimoire-session-start | SessionStart | Injection d'un contexte Grimoire court via `additionalContext` |
| grimoire-prompt-submit | UserPromptSubmit | Audit du prompt, references hooks/task-flow, contraintes de session |
| grimoire-memory-guard | PreToolUse | Protection mémoire `_grimoire-runtime/_memory/` |
| grimoire-control-surface-guard | PreToolUse | Garde-fous sur surfaces de controle agentiques et patterns destructifs |
| grimoire-post-edit | PostToolUse | Validation locale deterministe (`ruff`, `bash -n`, JSON hooks, frontmatter YAML) |
| grimoire-memory-gate | PostToolUse | Gate enforced Memory OS pour bloquer les drifts Weaviate/Neo4j/code graph quand l'environnement est disponible |
| grimoire-subagent-context | SubagentStart | Injection d'un contexte concis aux sub-agents |
| grimoire-subagent-trace | SubagentStart/Stop | Tracing des transitions SOG |
| grimoire-pre-compact | PreCompact | Capsule de contexte avant compaction/summarization |
| grimoire-master-stop-hook | Stop (agent scope) | Empeche une cloture seche et force une relance utilisateur concise |
| grimoire-rtk-rewrite | PreToolUse | Reecriture des commandes shell via RTK (Rust Token Killer) — compresse les sorties verboses (git, pytest, ruff, build...) avant l'agent. `mode: enforced` (actif). Repli non bloquant via `hook-safety-gate.py set-mode shadow grimoire-rtk-rewrite` |

## Runtime Routing & Diagnostics (DeepWiki)

Alignement avec les recommandations VS Code wiki (Getting Started + Performance & Diagnostics).

### Politique de choix de modèle (task-aware)

**Architecture SOG pur + Auto-first** — les agents n'ont pas de `model:` dans leur frontmatter. Le routing est géré entièrement par le SOG, avec fallback dynamique.
Source de vérité complète : `_grimoire-runtime/_config/model-routing.yaml`
Base de décision :
- `https://docs.github.com/en/copilot/reference/ai-models/supported-models`
- `https://docs.github.com/en/copilot/reference/ai-models/model-comparison`
Commande override session : `/set-model <agent|all|reset> <model-id|auto>` — ex: `/set-model dev gpt-5.3-codex`

| Profil de routing | Primary | Preferred (ordre de fallback) | Agents par défaut |
|---|---|---|---|
| **deep_reasoning** | `auto` | `gpt-5.4`, `gpt-5.3-codex`, `claude-opus-4.6`, `gemini-3.1-pro`, `gemini-2.5-pro` | `grimoire-master`, `rodin`, `architect`, `creative-problem-solver`, `innovation-strategist` |
| **general_code** | `auto` | `gpt-5.3-codex`, `gpt-5-mini`, `claude-sonnet-4.6`, `gemini-2.5-pro` | `dev`, `quick-flow-solo-dev`, `qa`, `tea` |
| **writing_structured** | `auto` | `gpt-5-mini`, `claude-sonnet-4.6`, `gemini-3-flash` | `pm`, `analyst`, `sm`, `tech-writer`, `ux-designer`, `art-director`, `storyteller`, `presentation-master`, `workflow-builder`, `agent-builder`, `module-builder` |
| **fast_iter** | `auto` | `gpt-5.4-mini`, `gpt-5-mini`, `claude-haiku-4.5`, `gemini-3-flash` | `brainstorming-coach`, `design-thinking-coach` |
| **local_coder** | `qwen3-coder` | Ollama `localhost:11434` — 256K ctx, AMD ROCm | usage offline/privé via `/set-model dev qwen3-coder` |

**Overrides task-aware (orchestrateur) :**

| Profil de tâche | Override vers | Raison |
|---|---|---|
| Cross-validation CVTL, second opinion critique, décision nuancée | `deep_reasoning` | Raisonnement indépendant et profondeur argumentative |
| Refactoring complexe, debug multi-fichiers, large codebase, ADR | `deep_reasoning` | Analyse technique profonde + contexte large |
| Contexte long (1000+ lignes, codebase entière) | `deep_reasoning` | Besoin multi-étapes à forte mémoire de contexte |
| Prompt engineering, création workflow/instruction, YAML | `writing_structured` | Sortie structurée, stabilité rédactionnelle |
| Tâches simples, checks d'état, opérations shell | `fast_iter` | Latence/coût optimisés |

Note: la disponibilité des modèles varie selon plan Copilot, client IDE et région; le fallback vers `auto` est obligatoire si un modèle explicite n'est pas disponible.

### Politique de parallélisme

- **Toujours paralléliser** les lectures/recherches indépendantes (read/search/grep/list).
- **Ne pas paralléliser** les commandes terminal mutables dans un shell partagé (ordre strict).
- `runSubagent` est utile pour spécialisation/isolation de contexte; le gain principal n'est pas la vitesse brute.

### Politique diagnostics VS Code (télémétrie opérationnelle)

- Utiliser `code --status` pour snapshot process/perf quand un ralentissement est suspecté.
- Compléter avec Process Explorer (`Help > Open Process Explorer`) et Running Extensions si besoin.
- Archiver les diagnostics dans `_grimoire-runtime-output/test-artifacts/` pour traçabilité.

## Création d'artefacts

> Le mécanisme UDF (Unified Dynamic Factory, artefacts éphémères `_dyn-*`) est retiré depuis le 2026-07-12 : zéro usage constaté sur toute sa durée de vie (tracker vide, aucun artefact créé). Décision et archive : `_grimoire-runtime-output/planning-artifacts/durcissement-agentique-20260712/`.

Toute création d'artefact est permanente et passe par le builder approprié :

| Type | Builder | Emplacement |
|---|---|---|
| Agent | agent-builder | `.github/agents/{slug}.agent.md` |
| Workflow prompt | workflow-builder | `.github/prompts/{slug}.prompt.md` |
| Skill | grimoire-skill-forge (gated by grimoire-skill-analyzer) | `.github/skills/{slug}/SKILL.md` |
| Hook | grimoire-skill-forge (gated by grimoire-skill-analyzer) | `.github/hooks/{hook-id}.json` + script |
| Instruction | tech-writer | `.github/instructions/{slug}.instructions.md` |

Par defaut, une capacite multi-etapes recurrente devient un skill. Le type `Workflow prompt` est reserve aux mission packs user-facing, manuels, avec un contrat de sortie explicite. La création de skills et de hooks passe obligatoirement par `grimoire-skill-forge`, qui invoque `grimoire-skill-analyzer` comme gate qualité bloquant (score minimum 75/100, ≥90 en mode strict). Les hooks démarrent toujours en `mode: shadow` dans `hook-safety-registry.json`.

## File-Specific Instructions

Instructions auto-chargées par VS Code selon le pattern `applyTo` :

| Instruction | Pattern | Contenu |
|---|---|---|
| `python-conventions` | `**/*.py` | Conventions Python, ruff, dataclasses, imports, tests |
| `markdown-standards` | `**/*.md` | CommonMark strict, Mermaid v10+, pas d'estimations temporelles |
| `artefact-governance` | `.github/**/*.md` | Statut, compatibilite, preuve et choix du plus petit artefact suffisant |
| `grimoire-runtime` | `_grimoire-runtime/**` | Structure Grimoire, config YAML, agents, workflows, mémoire |

## External Documentation References

Pour la documentation approfondie des dépendances et frameworks :

| Ressource | URL | Usage |
|---|---|---|
| VS Code Copilot Hooks (official) | `https://code.visualstudio.com/docs/copilot/customization/hooks` | Contrat JSON stdin/stdout, evenements, `permissionDecision`, `decision: block`, securite |
| VS Code Copilot Chat System | `https://deepwiki.com/microsoft/vscode-copilot-chat` | Vue d'ensemble custom agents, prompts, skills, hooks, instructions |
| VS Code Copilot Tool Calling Loop | `https://deepwiki.com/microsoft/vscode-copilot-chat/5.4-tool-calling-loop-and-execution` | Ordre d'execution des hooks, accumulation de `additionalHookContext`, boucle autopilot |
| VS Code Copilot Chat Hooks | `https://deepwiki.com/microsoft/vscode-copilot-chat/5.5-chat-hooks-and-extensibility` | Execution source-level des hooks, result processing, telemetry, output channel |
| VS Code Copilot Conversation Summarization | `https://deepwiki.com/microsoft/vscode-copilot-chat/5.6-conversation-summarization` | Integration `PreCompact`, compaction et preservation du contexte |
| Ruff Linter | `https://deepwiki.com/astral-sh/ruff` | Règles, configuration, per-file-ignores |
| Pytest | `https://deepwiki.com/pytest-dev/pytest` | Fixtures, markers, plugins |
| Typer CLI | `https://deepwiki.com/fastapi/typer` | CLI framework utilisé par grimoire |
| Mermaid | `https://deepwiki.com/mermaid-js/mermaid` | Syntaxe diagrammes v10+ |

> **Note** : Les URLs DeepWiki sont disponibles via MCP `deepwiki` si configuré, ou via navigateur.
> Pour consulter en session : utiliser `fetch` MCP ou demander une recherche ciblée.

## Slash Commands

Type `/grimoire-` in Copilot Chat to see all available Grimoire workflows. L'orchestrateur est disponible dans le dropdown agents sous `grimoire-master`.
<!-- Grimoire:END -->
