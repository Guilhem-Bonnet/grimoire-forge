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

## Available Agents

> **Architecture SOG (BM-53)** : Un seul agent est exposé à l'utilisateur — le BMad Master Orchestrator.
> Tous les autres agents fonctionnent comme sub-agents invisibles, dispatchés automatiquement
> par l'orchestrateur selon l'intention détectée. Voir `bmad-custom-kit/framework/orchestrator-gateway.md`.

| Agent | Persona | Title | Capabilities |
|---|---|---|---|
| bmad-master | BMad Master | Smart Orchestrator Gateway — Point d'entrée unique | orchestration SOG, dispatch intelligent, anti-hallucination HUP, escalation QEC, validation CVTL, party mode PCE |

### Sub-agents internes (invisibles à l'utilisateur)

L'orchestrateur dispatche automatiquement vers ces agents selon le besoin :

| Sub-agent | Persona | Spécialité |
|---|---|---|
| analyst | Mary | Business analysis, requirements |
| architect | Winston | Architecture, infrastructure |
| dev | Amelia | Implémentation, TDD |
| pm | John | Product management, PRD |
| qa | Quinn | Tests, QA |
| quick-flow-solo-dev | Barry | Rapid spec + implementation |
| sm | Bob | Scrum, stories, backlog |
| tech-writer | Paige | Documentation |
| ux-designer | Sally | UX/UI design |

## Slash Commands

Type `/bmad-` in Copilot Chat to see all available BMAD workflows. L'orchestrateur est disponible dans le dropdown agents sous `bmad-master`.
<!-- BMAD:END -->
