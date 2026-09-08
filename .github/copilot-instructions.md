<!-- Grimoire:START -->
# Grimoire — Project Instructions

## Project Configuration

- **Project**: Grimoire-Forge
- **User**: Guilhem
- **Communication Language**: Français
- **Document Output Language**: Français
- **User Skill Level**: expert
- **Output Folder**: {project-root}/_grimoire-runtime-output
- **Planning Artifacts**: {project-root}/_grimoire-runtime-output/planning-artifacts
- **Implementation Artifacts**: {project-root}/_grimoire-runtime-output/implementation-artifacts
- **Project Knowledge**: {project-root}/docs

## Doctrine — la Forge est un atelier, Grimoire est le produit

Cette section est la seule source de la doctrine atelier/produit du projet ;
`AGENTS.md` et `.github/agents/grimoire-master.agent.md` y renvoient sans la recopier.

La Forge (ce repo) n'est pas un projet à développer. C'est l'atelier qui sert à créer Grimoire.
Le produit est **grimoire-kit** (repo `Grimoire-kit`, cloné localement en `grimoire-kit/`) : c'est là que vivent le code produit, ses issues et son planning.

Règles opposables à tout agent et à toute session :

1. **Un chantier n'existe que s'il change ce que reçoit un utilisateur de grimoire-kit.** Le planning produit vit dans le repo Grimoire-kit, pas dans `planning-artifacts/`.
2. **Améliorer la Forge elle-même est interdit par défaut** (hooks, task-flow, runtime, patterns d'atelier, preuve, stigmergie…). On touche la Forge uniquement en maintenance corrective : quand elle casse, ou quand elle bloque un chantier produit identifiable.
3. **Verrou de triage** : avant tout nouveau chantier ou dispatch, répondre à « cible = produit ou atelier ? ». Cible atelier → confirmation explicite de Guilhem obligatoire, avec le chantier produit bloqué nommé. Pas de réponse → pas de travail.
4. Les plans d'atelier existants sont gelés ou archivés dans `_grimoire-runtime-output/planning-artifacts/deprecated-plans-registry.yaml` — ne pas les rouvrir sans demande explicite.

## Références et structure

- **Runtime Grimoire** (agents, workflows, config, mémoire) : `.github/instructions/grimoire-runtime.instructions.md`, chargé automatiquement sous `_grimoire-runtime/**`.
- **Carte des agents** (deux piles, doublons, graphe de dispatch) : `docs/agent-map.md`, générée par `scripts/agent-index.py` — ne pas éditer à la main.
- **Hooks du cycle de vie agent** : `docs/hooks-reference.md`.
- **Routing des modèles** (task-aware, fallback) : source de vérité `_grimoire-runtime/_config/model-routing.yaml`, détail dans `docs/model-routing-reference.md`.
- **Instructions par pattern** (`applyTo`) : `.github/instructions/*.instructions.md`.
- **Documentation externe** (VS Code Copilot, DeepWiki, Ruff, Pytest, Typer, Mermaid) : `docs/external-references.md`.

## Key Conventions

- Always load `_grimoire-runtime/bmm/config.yaml` before any agent activation or workflow execution
- Store all config fields as session variables: `{user_name}`, `{communication_language}`, `{output_folder}`, `{planning_artifacts}`, `{implementation_artifacts}`, `{project_knowledge}`
- MD-based workflows execute directly — load and follow the `.md` file; YAML-based workflows require the workflow engine — load `workflow.xml` first, then pass the `.yaml` config
- Follow step-based workflow execution: load steps JIT, never multiple at once; save outputs after EACH step when using the workflow engine
- The `{project-root}` variable resolves to the workspace root at runtime
- **Documentation charter**: Avant de créer ou modifier un fichier `.md`, charger `_grimoire-runtime/_memory/tech-writer-sidecar/documentation-standards.md` et respecter la charte (CommonMark, style guide, quality checklist)
- **Documentation companions**: Tout package de livrable sous `_grimoire-runtime-output/planning-artifacts/` doit inclure une `DOC-TECHNIQUE-<slug>.md` et une `GUIDE-utilisation-<slug>.md`; toute modification de package doit revalider ces deux compagnons avant cloture.
- **Autonomy protocols**: L'orchestrateur applique ALS (Autonomy Level System), Session Momentum, et Friction Budget. Voir `grimoire-kit/framework/agent-base.md` et `grimoire-kit/framework/orchestrator-gateway.md`. PIP (initiative proactive) est en statut observer-only (non instrumenté — cartographie 2026-04-21) ; AORA et DCF sont retirés (aucun artefact exécutable, purge du 2026-07-12, voir `_grimoire-runtime-output/planning-artifacts/durcissement-agentique-20260712/`).
- **Completion discipline**: Si une tâche révèle une suite logique alignée avec l'objectif courant et restant en risque L1/L2, l'agent doit l'exécuter dans le même tour. Ne proposer des prochaines étapes qu'en cas de blocage, de changement d'objectif, ou pour du travail optionnel, exploratoire, ou L3+.
- **Activation SOG**: Si le premier message utilisateur contient déjà une demande actionable, le master ne doit pas afficher le menu ni attendre une sélection; il doit traiter la demande directement. Le menu n'est montré que lors d'une activation sans tâche explicite.
- **Stability guard**: Pour éviter les crashs de l'extension host VSCode, respecter ces limites : jamais de grep_search sans `includePattern` ciblé, toujours un timeout raisonnable sur les commandes terminal. Le file watcher est configuré pour exclure `.venv`, `__pycache__`, `.pytest_cache`, `.ruff_cache` etc. (voir `.vscode/settings.json`).
- **Terminal lifecycle guard**: Pour chaque commande terminal en background, conserver l'ID, suivre son état via `await_terminal` ou `get_terminal_output`, puis appeler `kill_terminal` dès que le process n'est plus utile. Ne jamais garder plusieurs terminaux background pour le même objectif.
- **Terminal recovery guard**: Si un shell `/usr/bin/zsh` se termine avec code 1 sans diagnostic exploitable, relancer une fois dans un shell propre (`zsh -f`) avant d'escalader.
- **Hooks vs tasks**: Les hooks natifs VS Code/Copilot couvrent le cycle agent (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Subagent*`, `Stop`) mais pas `tasks.json`; l'orchestration et la preuve task-level restent deleguees a `.github/hooks/scripts/grimoire-task-flow.sh` et `.vscode/tasks.json`. Détail par hook : `docs/hooks-reference.md`.
- **Hook promotion guard**: Les hooks workspace et agent passent par `.github/hooks/scripts/grimoire-hook-gateway.sh` avec registre `_grimoire-runtime/_config/hook-safety-registry.json`; si le script cible ou sa surface de controle change apres validation, le hook est degrade en mode non bloquant (`shadow` ou `canary`) jusqu'a `grimoire: hooks-promote`. Les bascules manuelles passent par `hook-safety-gate.py set-mode ...` ou les tasks `grimoire: hooks-shadow` / `grimoire: hooks-canary`. Tout hook nouveau doit etre branche via le gateway et declare dans le registre, sinon `hooks-status` et `grimoire-hooks-smoke.sh` echouent.

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

## Slash Commands

Type `/grimoire-` in Copilot Chat to see all available Grimoire workflows. L'orchestrateur est disponible dans le dropdown agents sous `grimoire-master`.
<!-- Grimoire:END -->
