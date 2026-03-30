<!-- BMAD:START -->
# BMAD Method — Project Instructions

## Project Configuration

- **Project**: grimoire
- **User**: Guilhem
- **Communication Language**: Français
- **Document Output Language**: Français
- **User Skill Level**: expert
- **Output Folder**: {project-root}/_bmad-output
- **Planning Artifacts**: {project-root}/_bmad-output/planning-artifacts
- **Implementation Artifacts**: {project-root}/_bmad-output/implementation-artifacts
- **Project Knowledge**: {project-root}/docs

## BMAD Runtime Structure

- **Agent definitions**: `_bmad/bmm/agents/` (BMM module) and `_bmad/core/agents/` (core)
- **Workflow definitions**: `_bmad/bmm/workflows/` (organized by phase)
- **Core tasks**: `_bmad/core/tasks/` (help, editorial review, indexing, sharding, adversarial review)
- **Core workflows**: `_bmad/core/workflows/` (brainstorming, party-mode, advanced-elicitation)
- **Workflow engine**: `_bmad/core/tasks/workflow.xml` (executes YAML-based workflows)
- **Module configuration**: `_bmad/bmm/config.yaml`
- **Core configuration**: `_bmad/core/config.yaml`
- **Agent manifest**: `_bmad/_config/agent-manifest.csv`
- **Workflow manifest**: `_bmad/_config/workflow-manifest.csv`
- **Help manifest**: `_bmad/_config/bmad-help.csv`
- **Agent memory**: `_bmad/_memory/`

## Key Conventions

- Always load `_bmad/bmm/config.yaml` before any agent activation or workflow execution
- Store all config fields as session variables: `{user_name}`, `{communication_language}`, `{output_folder}`, `{planning_artifacts}`, `{implementation_artifacts}`, `{project_knowledge}`
- MD-based workflows execute directly — load and follow the `.md` file
- YAML-based workflows require the workflow engine — load `workflow.xml` first, then pass the `.yaml` config
- Follow step-based workflow execution: load steps JIT, never multiple at once
- Save outputs after EACH step when using the workflow engine
- The `{project-root}` variable resolves to the workspace root at runtime
- **Documentation charter**: Avant de créer ou modifier un fichier `.md`, charger `_bmad/_memory/tech-writer-sidecar/documentation-standards.md` et respecter la charte (CommonMark, style guide, quality checklist)
- **Autonomy protocols**: L'orchestrateur applique ALS (Autonomy Level System), AORA (boucle d'itération autonome), PIP (initiative proactive), DCF (confiance contextuelle), Session Momentum, et Friction Budget. Voir `bmad-custom-kit/framework/agent-base.md` et `bmad-custom-kit/framework/orchestrator-gateway.md`.
- **Stability guard**: Pour éviter les crashs de l'extension host VSCode, respecter ces limites : jamais de grep_search sans `includePattern` ciblé, toujours un timeout raisonnable sur les commandes terminal. Le file watcher est configuré pour exclure `.venv`, `__pycache__`, `.pytest_cache`, `.ruff_cache` etc. (voir `.vscode/settings.json`).

## Available Agents

> **Architecture SOG (BM-53)** : Un seul agent est exposé à l'utilisateur — le BMad Master Orchestrator.
> Tous les autres agents fonctionnent comme sub-agents invisibles, dispatchés automatiquement
> par l'orchestrateur selon l'intention détectée. Voir `bmad-custom-kit/framework/orchestrator-gateway.md`.

| Agent | Persona | Title | Capabilities |
|---|---|---|---|
| bmad-master | BMad Master | Smart Orchestrator Gateway — Point d'entrée unique | orchestration SOG, dispatch intelligent, anti-hallucination HUP, escalation QEC, validation CVTL, party mode PCE, autonomy ALS, iteration AORA, proactive PIP, confidence DCF |

### Sub-agents internes (invisibles à l'utilisateur)

L'orchestrateur dispatche automatiquement vers ces agents selon le besoin :

#### BMM — Méthode BMAD

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
| agent-builder | Bond | read, edit, search | Création d'agents BMAD |
| module-builder | Morgan | read, edit, search | Création de modules |
| workflow-builder | Wendy | read, edit, search | Création de workflows |

#### CIS — Créativité et Innovation

| Sub-agent | Persona | Outils | Spécialité |
|---|---|---|---|
| brainstorming-coach | Carson | read, search | Brainstorming, idéation |
| creative-problem-solver | Dr. Quinn | read, search | TRIZ, problem solving |
| design-thinking-coach | Maya | read, search | Design thinking |
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
| bmad-session-start | SessionStart | Injection automatique du contexte BMAD |
| bmad-memory-guard | PreToolUse | Protection mémoire `_bmad/_memory/` |
| bmad-post-edit | PostToolUse | Auto-lint ruff (Python) + validation frontmatter YAML (artefacts UDF) |
| bmad-subagent-trace | SubagentStart/Stop | Tracing des transitions SOG |

## Unified Dynamic Factory (UDF)

L'orchestrateur peut créer dynamiquement 4 types d'artefacts quand aucun existant ne couvre le besoin.

**Registre centralisé** : `_bmad/_config/udf-registry.yaml` — source de vérité pour les conventions (paths, templates, seuils) de chaque type d'artefact.

### Types d'artefacts

| Type | Builder | Éphémère | Permanent | Emplacement |
|---|---|---|---|---|
| Agent | agent-builder | `_dyn-*.agent.md` | `{slug}.agent.md` | `.github/agents/` |
| Workflow | workflow-builder | `_dyn-*.prompt.md` | `{slug}.prompt.md` | `.github/prompts/` |
| Skill | workflow-builder + dev | `_dyn-*/SKILL.md` | `{slug}/SKILL.md` | `.github/skills/` |
| Instruction | tech-writer | `_dyn-*.instructions.md` | `{slug}.instructions.md` | `.github/instructions/` |

### Processus

1. **Gap detection** : le SOG analyse la requête et identifie qu'aucun artefact existant ne correspond
2. **Type classification** : le SOG détermine le type d'artefact nécessaire (agent, workflow, skill, instruction)
3. **Triage de durabilité** : score de durabilité pour décider entre création éphémère ou permanente
4. **Création** : dispatch vers le builder approprié en mode Rapid (éphémère) ou Full (permanent)
5. **Post-use** : promotion automatique des éphémères réutilisés 3+ fois

### Triage de durabilité

| Signal | Score |
|---|---|
| Domaine lié au stack technique du projet | +2 |
| Besoin déjà exprimé dans une session précédente | +2 |
| Domaine transversal (sécurité, performance, accessibilité, data) | +2 |
| Besoin récurrent dans le cycle de vie produit | +1 |
| Besoin ponctuel/exploratoire | -2 |
| Domaine très niche | -1 |

- **Score ≥ 3** → Création permanente via template `permanent-*.tpl.md`
- **Score < 3** → Création éphémère via template `dynamic-*.tpl.md` (expire 7j)
- **Nettoyage** : task `bmad: cleanup-dynamic-artifacts` nettoie tous les artefacts expirés

## File-Specific Instructions

Instructions auto-chargées par VS Code selon le pattern `applyTo` :

| Instruction | Pattern | Contenu |
|---|---|---|
| `python-conventions` | `**/*.py` | Conventions Python, ruff, dataclasses, imports, tests |
| `markdown-standards` | `**/*.md` | CommonMark strict, Mermaid v10+, pas d'estimations temporelles |
| `bmad-framework` | `_bmad/**` | Structure BMAD, config YAML, agents, workflows, mémoire |

## External Documentation References

Pour la documentation approfondie des dépendances et frameworks :

| Ressource | URL DeepWiki | Usage |
|---|---|---|
| VS Code Copilot Custom Agents | `https://deepwiki.com/microsoft/vscode-copilot-chat` | Format `.agent.md`, `.prompt.md`, skills, hooks, instructions |
| Ruff Linter | `https://deepwiki.com/astral-sh/ruff` | Règles, configuration, per-file-ignores |
| Pytest | `https://deepwiki.com/pytest-dev/pytest` | Fixtures, markers, plugins |
| MkDocs Material | `https://deepwiki.com/squidfunk/mkdocs-material` | Documentation site generation |
| Typer CLI | `https://deepwiki.com/fastapi/typer` | CLI framework utilisé par grimoire |
| Mermaid | `https://deepwiki.com/mermaid-js/mermaid` | Syntaxe diagrammes v10+ |

> **Note** : Les URLs DeepWiki sont disponibles via MCP `deepwiki` si configuré, ou via navigateur.
> Pour consulter en session : utiliser `fetch` MCP ou demander une recherche ciblée.

## Slash Commands

Type `/bmad-` in Copilot Chat to see all available BMAD workflows. L'orchestrateur est disponible dans le dropdown agents sous `bmad-master`.
<!-- BMAD:END -->
