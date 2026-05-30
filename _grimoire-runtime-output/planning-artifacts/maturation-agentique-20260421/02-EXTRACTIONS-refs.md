# 02 — Extractions depuis les références

> Deux forks dorment sous `grimoire-kit/apps/`. On extrait ce qui colle au runtime Grimoire, on laisse le reste.

## Principes d'extraction

1. **Aucun fork n'est adopté en l'état.** Chaque fork est une mine de patterns, pas un runtime second.
2. **Tout converge vers `grimoire-kit/apps/grimoire-game/`** (le runtime canonique).
3. **Pas de port JS → Python.** Les extensions VS Code TypeScript inspirent, mais la cible est la SPA existante.
4. **Les événements passent par le bus défini en V1** (voir `06-PLAN-execution-phases.md`). Aucun fork ne créera son propre canal.

## Référence 1 — Pixel Agents (`apps/pixel-agents-fork/`)

### Ce que c'est

Extension VS Code qui rend chaque agent Claude Code comme un personnage dans un bureau pixel-art. Watch les fichiers JSONL transcript, mappe `tool_use` → animation, gère sous-agents Task comme personnages liés.

### Forces identifiées

| Pattern | Fichier source | Réutilisabilité |
|---|---|---|
| **OfficeState unifié** | `webview-ui/src/office/engine/officeState.ts` | Modèle mental : layout + tileMap + seats + blockedTiles + characters dérivés. Pattern à reproduire dans notre `GameState`. |
| **Character state machine** | `webview-ui/src/office/engine/characters.ts` | `idle → walk → type/read` piloté par événements externes. Directement applicable à un agent SOG. |
| **BFS pathfinding** | `webview-ui/src/office/layout/tileMap.ts` | Algorithme compact pour placement agent → siège. |
| **Sub-agent visualization** | `AgentState.activeSubagentToolIds` dans `src/types.ts` | Chaque `Task` spawn un personnage lié. Colle parfaitement au modèle SOG (master + sub-agents invisibles). Ici, on rend les sub-agents visibles pour l'observateur. |
| **Layout editor (floor/walls/furniture)** | `webview-ui/src/office/editor/` + `webview-ui/src/office/layout/` | Permet à l'utilisateur de designer son "bureau agentique". Grosse valeur UX démo. |
| **Manifest-driven assets** | `webview-ui/public/assets/furniture/*/manifest.json` | Pattern d'extensibilité propre. Compatible avec notre `grimoire-game-assets/`. |
| **Debug view JSONL** | `src/PixelAgentsViewProvider.ts` | Diagnostics par agent : file status, lines parsed, last data timestamp. À intégrer dans `observability`. |

### Ce qu'on NE prend PAS

| Pattern | Pourquoi on ignore |
|---|---|
| Couplage Claude Code JSONL | On a déjà `GRIMOIRE_TRACE.jsonl` qui est notre source unique. Pas besoin de parser Claude JSONL. |
| VS Code Webview API spécifique | Notre cockpit est une SPA Vite, pas un webview. |
| `configPersistence.ts` ad hoc | Notre `_grimoire-runtime/_memory/` est le canon. |
| Heuristiques idle timer | Nos hooks `SubagentStart/Stop` donnent des signaux déterministes. |

### Plan d'adaptation (pour V3)

1. Copier mentalement `OfficeState` → `grimoire-kit/apps/grimoire-game/src/surfaces/office/state.ts`
2. Le `character.activeToolNames: Map<string, string>` devient la projection d'un événement `PreToolUse` du bus V1
3. Les `Seat` + `FurnitureInstance` restent une question UX — pour MVP on prend une grille fixe
4. Assets : réutiliser ceux déjà dans `grimoire-game-assets/` (instruction `grimoire-2d-assets.instructions.md`)
5. Sub-agents SOG → personnages liés au master par une ligne de suivi (flux visuel)

### Licence

MIT — compatible avec extraction de code, attribution à préserver dans `grimoire-game-assets/STYLE_GUIDE.md` ou équivalent.

## Référence 2 — Switchboard (`apps/switchboard-fork/`)

### Ce que c'est

Extension VS Code : Kanban visuel qui route drag→trigger vers des agents. Chaque colonne = un rôle (Planner, Lead Coder, Coder, Reviewer, Acceptance Tester, Analyst, Intern). Dispatcher via `terminal.sendText` dans des terminaux VS Code.

### Forces identifiées

| Pattern | Fichier source | Réutilisabilité |
|---|---|---|
| **Colonnes = rôles** | `src/webview/kanban.html` + `src/webview/setup.html` | Modèle Kanban orienté agent (pas tâche pure). Chaque colonne a son prompt + son agent associé. À fusionner avec notre `mission-board`. |
| **Drag → trigger** | `src/webview/implementation.html` + dispatcher | L'interaction utilisateur primaire. Directement transposable à `mission-board` (drag card → déclenche agent via hook PostToolUse). |
| **Complexity routing** | Logique Planner | Score de complexité → route vers Lead Coder ou Coder. Applicable à notre router LLM (`src/grimoire/tools/llm_router.py`). |
| **Paste mode / Trigger mode** | Dispatcher | Mode "copy prompt to clipboard" pour agents chat (Windsurf, Cursor). Utile pour multi-IDE. |
| **Review lane + Acceptance lane** | Colonnes Reviewer / Acceptance Tester | Cartographie naturelle sur notre QA + TEA sub-agents. |
| **Off-repo state** | "kanban state lives in a multi-repo database" | Évite la pollution du repo utilisateur. À comparer à notre choix actuel de persister dans `_grimoire-runtime-output/` — décision à prendre en V2. |

### Ce qu'on NE prend PAS

| Pattern | Pourquoi on ignore |
|---|---|
| Dépendance Google Drive pour state | On persiste déjà localement, pas de cloud forcé. |
| Multi-provider CLI dispatch via terminal | Notre dispatcher passe par `agent-caller.py` + SOG. Terminal direct serait un rollback. |
| Approche "pas d'orchestrateur" | On a explicitement SOG BM-53. C'est un choix architectural opposé. |

### Plan d'adaptation (pour V2)

1. Réutiliser la **taxonomie des colonnes** (Planner, Lead Coder, Coder, Reviewer, Acceptance, Intern, Analyst) comme template dans `mission-board`
2. Mapper les rôles sur nos sub-agents existants :
   - Planner → `pm` / `analyst`
   - Lead Coder → `dev`
   - Coder → `quick-flow-solo-dev`
   - Reviewer → skill `grimoire-code-review`
   - Acceptance Tester → `qa` / `tea`
   - Analyst → `analyst`
   - Intern → optionnel, pourrait être un profil `fast_iter`
3. Drag → trigger déclenche le SOG avec `runSubagent` de l'agent approprié
4. Complexity score → override le routing model pour cette carte (bridge avec `llm_router`)

### Licence

À vérifier (fork présent, LICENSE à lire au moment de l'extraction V2).

## Références documentaires déjà produites

Ne pas refaire ce qui existe :

| Document | Chemin | Rôle |
|---|---|---|
| Benchmark dimensionnel | [docs/exploitation/benchmark-github-agent-os-game-ui.md](../../../docs/exploitation/benchmark-github-agent-os-game-ui.md) | Compare 6 projets, grid GM-01..GM-30. Source de vérité patterns. |
| Plan maître Game UI | [docs/exploitation/plan-maitre-agent-os-game-ui.md](../../../docs/exploitation/plan-maitre-agent-os-game-ui.md) | Cartographie GM-* ↔ notre runtime. |
| Livrable v5 | [docs/exploitation/livrable-v5-agent-os-game-ui.md](../../../docs/exploitation/livrable-v5-agent-os-game-ui.md) | État initial livré. |
| Brainstorm Pixel Observatory V2 | `_grimoire-runtime-output/planning-artifacts/BRAINSTORM-PIXEL-OBSERVATORY-V2.md` | Exploration précédente, à rouvrir en V3. |

## Consolidation : matrice "Ref → Vague → Artefact cible"

| Source | Pattern | Vague | Artefact cible |
|---|---|---|---|
| Pixel Agents | `OfficeState` | V3 | `grimoire-kit/apps/grimoire-game/src/surfaces/office/state.ts` (à créer) |
| Pixel Agents | Character state machine | V3 | `surfaces/office/engine/character.ts` |
| Pixel Agents | Layout editor | V3 (opt.) | `surfaces/office/editor/` |
| Pixel Agents | Sub-agent visualization | V3 | Projection du bus V1 vers état office |
| Switchboard | Colonnes = rôles | V2 | Extension `mission-board` avec `column.role` + mapping sub-agents |
| Switchboard | Drag → trigger | V2 | Handler `surfaces/mission-board/triggers.ts` appelant SOG |
| Switchboard | Complexity routing | V2 | Bridge `mission-board` ↔ `src/grimoire/tools/llm_router.py` |
| Benchmark doc | GM-15/16/17/27 patterns | V1 | Contrat du bus d'événements |

## Anti-pattern explicite

**Ne pas** installer les extensions VS Code forkées. Elles restent source de lecture, pas de runtime parallèle. Si le besoin apparaît d'une extension VS Code Grimoire, c'est une vague séparée (V5+) hors de ce pack.
