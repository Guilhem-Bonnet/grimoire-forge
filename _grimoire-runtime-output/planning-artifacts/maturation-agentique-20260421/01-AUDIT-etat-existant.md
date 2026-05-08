# 01 — Audit de l'état existant

> Inventaire mesuré au 2026-04-21. Toutes les valeurs sont vérifiables à la commande.

## 1. Surfaces utilisateur

### Déjà en production (site MkDocs)

Publiées via `mkdocs_hooks/copy_cockpit.py` qui copie `grimoire-kit/apps/grimoire-game/.release/cockpit-app/` vers `site/cockpit/` après chaque `mkdocs build`.

| Surface | URL (site public) | Source | État |
|---|---|---|---|
| Cockpit | `/cockpit/?mode=cockpit` | [docs/produit/cockpit-live.md](../../../docs/produit/cockpit-live.md) | Publié, interactif via iframe |
| Kanban (Mission Board) | `/cockpit/?mode=mission-board` | [docs/produit/kanban-live.md](../../../docs/produit/kanban-live.md) | Publié, **données mock** |
| Observability | `/cockpit/?mode=observability` | [docs/produit/observability-live.md](../../../docs/produit/observability-live.md) | Publié, **données mock** |

Les query params `?mode=` supportés par la SPA : `cockpit`, `mission-board`, `observability`, `game-ui`, `war-room`, `proofs`, `kernel`, `observatory`, `spectator`.

### Runtime sous-jacent

`grimoire-kit/apps/grimoire-game/` :

- 94 tests (`*.test.ts` / `*.test.tsx`)
- `src/` organisé en : `bridge/`, `state/`, `contracts/`, `server/` (avec `control-plane/` + `auth/`)
- Scripts NPM clés : `cockpit:build`, `cockpit:verify`, `demo:views`, `demo:report`, `test:coverage`
- Artefacts publiables : `.release/cockpit-app/`, `.release/runtime-views-report.html`

**Trou critique** : `control-plane` et `bridge` existent, mais **rien ne les alimente depuis les hooks réels**. Le Kanban n'observe pas les agents, il affiche un état simulé.

## 2. Hooks

Installés dans `.github/hooks/` avec gateway `.github/hooks/scripts/grimoire-hook-gateway.sh` + registry `_grimoire-runtime/_config/hook-safety-registry.json`.

### Inventaire

- **9 hooks déclarés** dans le registry — tous en mode `enforced` (validés 2026-04-16T20:36:50Z)
- **13 scripts** dans `.github/hooks/scripts/`

| Événement | Script | Rôle |
|---|---|---|
| `SessionStart` | `grimoire-session-start.sh` | Injection contexte Grimoire via `additionalContext` |
| `UserPromptSubmit` | `grimoire-prompt-submit.sh` | Audit prompt, refs hooks/task-flow |
| `PreToolUse` | `grimoire-memory-guard.sh` | Protège `_grimoire-runtime/_memory/` |
| `PreToolUse` | `grimoire-control-surface-guard.sh` | Garde-fous sur surfaces de contrôle agentiques |
| `PostToolUse` | `grimoire-post-edit.sh` | Validation locale (ruff, bash -n, JSON hooks, frontmatter YAML) |
| `SubagentStart` | `grimoire-subagent-context.sh` | Injection contexte concis sub-agents |
| `SubagentStart/Stop` | `grimoire-subagent-trace.sh` | Tracing transitions SOG |
| `PreCompact` | `grimoire-pre-compact.sh` | Capsule contexte avant summarization |
| `Stop` | `grimoire-master-stop-hook.sh` | Empêche clôture sèche |

### Signaux observables

- `_grimoire-runtime-output/hook-runtime/` : journal runtime (selon config scripts)
- `_grimoire-runtime-output/GRIMOIRE_TRACE.jsonl` : trace SOG unifiée
- `_grimoire-runtime/_config/hook-safety-registry.json` : empreintes SHA par script

### Trous identifiés (détaillés dans `03-GAP-ANALYSIS-hooks.md`)

1. Aucun hook **n'émet vers un bus d'événements consommable par les surfaces** (le Kanban ne sait rien des `PreToolUse`)
2. Pas de normalisation uniforme des événements (chaque script a son propre format)
3. Pas de replay/rewind depuis la trace vers les surfaces
4. Pas de hook d'erreur métier (failure counters) branché sur observability

## 3. Agents, workflows, skills, instructions, prompts

| Catégorie | Répertoire | Nombre | État |
|---|---|---|---|
| Agents | `.github/agents/*.agent.md` | 23 | SOG : 1 user-facing (`grimoire-master`) + 22 sub-agents + `bmad-master` legacy |
| Skills | `.github/skills/grimoire-*/` | 41 | Tous actifs, auto-découverts VS Code |
| Instructions | `.github/instructions/*.md` | 7 | `applyTo` ciblé (Python, MD, `.github/`, runtime, 2D assets, game-runtime, compiled-flow) |
| Prompts user-facing | `.github/prompts/*.prompt.md` | 6 | Mission packs user-facing (non dynamiques) |
| Artefacts `_dyn-*` | `.github/` | 0 | Pas de cache dynamique en cours |

### Runtime BMM

- `_grimoire-runtime/bmm/agents/` : 9 agents méthode Grimoire
- `_grimoire-runtime/cis/agents/` : 8 agents créativité
- `_grimoire-runtime/bmb/agents/` : 3 builders (agent/module/workflow)
- `_grimoire-runtime/tea/agents/` : 1 architecte test
- `_grimoire-runtime/core/agents/` : orchestrateur master

**Observation** : SOG est respecté (1 seul agent exposé), les 22 sub-agents sont correctement masqués.

## 4. Concepts BM-*

42 identifiants `BM-*` référencés dans le code. Détail dans `04-CARTOGRAPHIE-concepts.md`.

Aperçu :

| ID | Concept | Statut éclair |
|---|---|---|
| BM-50 | HUP (anti-hallucination) | Implémenté, actif dans SOG |
| BM-51 | QEC (batching questions) | Implémenté, actif |
| BM-52 | CVTL (cross-validation) | Implémenté, actif |
| BM-53 | SOG (Smart Orchestrator Gateway) | Cœur du runtime, actif |
| BM-57 | ARG (Agent Relationship Graph) | Implémenté dans routing |
| BM-07 | Context Router | Implémenté (`src/grimoire/tools/context_router.py`) |
| BM-22 | Mémoire structurée Qdrant | Partiel (mem0-bridge.py, pas de Qdrant branché) |
| BM-41 | Semantic Cache LLM | Partiel (script existe, pas actif) |
| BM-11 | Boomerang task chains | Documenté, pas d'exécuteur |

**Distribution estimée** : ~24 actifs, ~10 partiels, ~8 théoriques/archivables.

## 5. Baseline quantitative

Obtenue via `framework/tools/harmony-check.py` et `pytest --co` dans `grimoire-kit/`.

| Mesure | Valeur | Commande de vérification |
|---|---|---|
| Score harmony | **96/100 — Grade A** | `python framework/tools/harmony-check.py --project-root .. score --json` |
| Fichiers scannés | 1389 | idem |
| Agents indexés | 84 | idem |
| Workflows indexés | 567 | idem |
| Tools indexés | 148 | idem |
| Dissonances | 46 total | `orphan=4`, `size=32`, `duplication=10` |
| Tests kit (non-e2e) | ≥ 600 (collectés partiellement) | `pytest --co --ignore=tests/e2e -q` |
| Tests grimoire-game | 94 | `find tests -name "*.test.ts*"` |
| Lint | Clean | `ruff check` → all checks passed |

### Dette structurelle identifiée

**Framework tools encore > 800 lignes** (candidats à canoniser vers `src/grimoire/tools/`) :

| Fichier | Lignes |
|---|---|
| `framework/tools/guardrail-policy.py` | 5936 |
| `framework/tools/observatory.py` | 4242 |
| `framework/tools/dream.py` | 1348 |
| `framework/tools/preflight-check.py` | 1287 |
| `framework/tools/tool-resolver.py` | 1236 |
| `framework/tools/context-guard.py` | 1107 |
| `framework/tools/hpe-runner.py` | 1102 |
| `framework/tools/rag-indexer.py` | 1054 |
| `framework/tools/hpe-monitor.py` | 1030 |
| `framework/tools/web-browser.py` | 997 |
| `framework/tools/stigmergy.py` | 985 |
| `framework/tools/agent-darwinism.py` | 972 |
| `framework/tools/agent-task-system.py` | 946 |
| `framework/tools/agent-forge.py` | 927 |
| `framework/tools/agent-debugger.py` | 884 |

Déjà canonisés (6 achevés cette session) : `compiled_flow`, `token_budget`, `llm_router`, `agent_lint`, `memory_lint`, `harmony_check`, `preflight_check`, `stigmergy`, `context_router`, `context_guard`, `learnings`, `agent_forge` (total 13 modules dans `src/grimoire/tools/`).

## 6. Forks de référence dormants

Présents dans `grimoire-kit/apps/` mais non intégrés au runtime :

| Fork | Chemin | Langage | Forces à extraire |
|---|---|---|---|
| Pixel Agents | `apps/pixel-agents-fork/` | TS + React + Canvas 2D | `OfficeState`, BFS, state machine character, JSONL transcript parser, office layout editor, sub-agent visualization |
| Switchboard | `apps/switchboard-fork/` | TS + HTML webviews | Kanban drag→trigger via `terminal.sendText`, rôles (Planner/Coder/Reviewer/...), complexity routing |

Détail de l'extraction dans `02-EXTRACTIONS-refs.md`.

## 7. Ce qui est réellement terminé versus promis

### Terminé et vivant ✓

- SOG orchestrateur (BM-53) + HUP/QEC/CVTL/ARG
- Hooks gateway avec registry de sécurité
- 3 surfaces cockpit publiées (iframe integration MkDocs)
- 41 skills auto-découvertes
- UDF (Unified Dynamic Factory) — 4 types d'artefacts créables dynamiquement
- Charte graphique + design system (v20260417p/q)
- 13 modules canoniques dans `src/grimoire/tools/`

### Livré partiellement

- Mission Board : UI existe, données mock
- Observability : UI existe, données mock
- BM-22 (Qdrant memory) : bridge existe, store non branché
- BM-41 (Semantic Cache) : script existe, pas dans chain LLM

### Promis mais non exécuté

- Pont hooks → surfaces (Mission Board alimenté par événements réels)
- Office view style Pixel Agents dans `observatory`
- Kanban drag→trigger style Switchboard
- Replay/rewind timeline depuis `GRIMOIRE_TRACE.jsonl`
- Intégration visible des 10 BM-* partiels
