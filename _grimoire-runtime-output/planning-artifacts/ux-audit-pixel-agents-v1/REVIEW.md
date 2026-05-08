# UX Audit — Pixel Agents v1 (Grimoire-adapté)

- **Contexte** : fork de `pablodelucca/pixel-agents` (React 19 + Vite + Canvas 2D + Tailwind 4). Webview buildé standalone (`dist/webview/`, 804 KB) puis embarqué en iframe via `?mode=game-ui` + direct `/pixel-agents/index.html`.
- **Approche** : runtime "browser" natif (via `runtime.ts` → `isBrowserRuntime=true`), shim Grimoire qui n'intercepte PAS `acquireVsCodeApi` et dispatch uniquement les agents Grimoire par-dessus.
- **État** : canvas 2560×1440 rendu, layout office par défaut chargé, FX + DA Grimoire appliqués, **0 erreur console**. Roster de 13 agents Grimoire (9 BMM + 2 BMB + 1 CIS + 1 core) défini. Les seats ne sont pas encore auto-assignés aux 13 agents (layout par défaut pixel-agents vide de seats) → à câbler au scope 3.

## 1. Forces reprises de pixel-agents

1. **Moteur visuel mature** — canvas pixel-perfect, BFS pathfinding, state machine characters (idle/walk/type/read).
2. **Assets open-source complets** — 6 characters JIK-A-4, walls auto-tiling, floors HSB, furniture avec manifests.
3. **Layout editor** — grille 64×64 extensible, undo/redo, export/import JSON.
4. **Observable par design** — `useExtensionMessages` hook écoute 20+ types d'événements (agentCreated, agentStatus, agentToolStart, agentTeamInfo, agentTokenUsage, subagent*).

## 2. Adaptation Grimoire v1 (livré)

- **DA overlay** — [grimoire-pixel-da.css](../../grimoire-kit/apps/grimoire-game/public/pixel-agents/grimoire-pixel-da.css) : fond `#0B0C0E`, accent `#FF6B3D`, Geist, FX ambient, palette sémantique (green/orange/red soft).
- **Shim dispatch** — [grimoire-pixel-shim.js](../../grimoire-kit/apps/grimoire-game/public/pixel-agents/grimoire-pixel-shim.js) : roster Grimoire (13 agents : grimoire-master, analyst, architect, dev, pm, qa, sm, tea, tech-writer, ux-designer, agent-builder, workflow-builder, rodin) + mapping `team` (core/bmm/bmb/tea/cis) et `role` (orchestrator/coder/reviewer/tester/...).
- **Branding** — badge bottom-left orange, legend bottom-right (active/waiting/idle/agent count).
- **Embed cockpit** — `renderGameUiMode` remplacé par iframe `pixel-agents/index.html`, sandbox `allow-scripts allow-same-origin`.

## 3. Points à améliorer (prioritisés)

| # | Severité | Problème | Recommandation |
|---|---|---|---|
| 1 | **HIGH** | Les 13 agents Grimoire ne s'affichent pas dans l'office (layout par défaut n'a pas de seats) | Créer `grimoire-office-layout.json` avec 13 seats pré-placés par room (war-room, workshop, intake-desk...) et forcer son chargement via `layoutLoaded` |
| 2 | **HIGH** | Pas de mapping room Grimoire → zone pixel-agents | Étendre le layout editor : quadrants nommés (intake NW, workshop N, war-room NE, watchtower E, branch-finisher S, seance-archive SW) |
| 3 | **HIGH** | Status démo statique, sans flux temps réel | Adapter `transcriptParser.ts` pour consommer `_grimoire-runtime-output/GRIMOIRE_TRACE.jsonl` ou WebSocket depuis AgentAdapter |
| 4 | **MED** | 6 palettes character seulement → 13 agents cyclent les sprites | Commission de sprites Grimoire-spécifiques OU mapping rôle→palette cohérent (coders=bleu, reviewers=rouge, designers=violet...) |
| 5 | **MED** | Token usage randomisé au scope 1, irréaliste | Lire `_grimoire-runtime/_memory/*.jsonl` pour contexte usage réel par agent |
| 6 | **MED** | Banner "v1.3" et "Updated to v1.3!" reste visible upstream | Masquer via CSS overlay OU patcher le changelogData.ts |
| 7 | **LOW** | Layout per-workspace non persistant (localStorage par domaine) | Brancher sur `_grimoire-runtime-output/cockpit-layout.json` via adapter HTTP |
| 8 | **LOW** | Sound notifications off par défaut | Activer pour les états `waiting` (Grimoire QEC batching trigger) |

## 4. Opportunités conceptuelles Grimoire

- **Rooms = kanban columns inversés** : un agent "dans la war-room" est visible sur le board game-ui ET comme colonne de cards. Bidirectionnel.
- **Seat = desk = assignation** : drag-and-drop un agent sur un desk = `/agent:<name> attach-room war-room`.
- **Speech bubbles QEC** : quand un sub-agent trigger QEC (batching questions), afficher un speech bubble "?" au-dessus du character jusqu'à réponse orchestrator.
- **Party mode (PCE)** : 2 agents côte-à-côte + speech bubbles échangées = visualiser un debate Rodin / CVTL.
- **Antifragile score** : couleur du sol de la room reflète le score antifragile (vert sain, orange fragile, rouge critique) cf. skill `grimoire-antifragile`.
- **Trust status overlay** : character avec `trustStatus: blocked` entouré d'un cercle rouge + "BLOCKED" bubble.

## 5. Scope 3 — deferred

- Pipeline GRIMOIRE_TRACE.jsonl → WebSocket → pixel-agents events (AgentAdapter).
- Layout Grimoire custom (fichier `grimoire-office-layout.json`) avec 6 rooms dimensionnées.
- Sprites Grimoire-specific (commission art-director avec rodin + workflow-builder).
- Bidirectional sync avec Switchboard (carte déplacée = agent déplacé).

## 6. Artefacts livrés

- **Fork** : `grimoire-kit/apps/pixel-agents-fork/` (shallow clone, non-trackable volontairement)
- **Bundle statique** : `grimoire-kit/apps/grimoire-game/public/pixel-agents/` (804 KB, assets+JS+CSS)
- **Shim Grimoire** : [grimoire-pixel-shim.js](../../grimoire-kit/apps/grimoire-game/public/pixel-agents/grimoire-pixel-shim.js)
- **DA overlay** : [grimoire-pixel-da.css](../../grimoire-kit/apps/grimoire-game/public/pixel-agents/grimoire-pixel-da.css)
- **Embed cockpit** : [main.ts renderGameUiMode](../../grimoire-kit/apps/grimoire-game/app/main.ts#L2050)
- **Mirror build** : [prepare-runtime-cockpit-app.ts](../../grimoire-kit/apps/grimoire-game/examples/prepare-runtime-cockpit-app.ts)

## 7. URLs

| Surface | URL |
|---|---|
| Cockpit Game UI (iframe) | http://127.0.0.1:4175/?mode=game-ui |
| Pixel Agents direct | http://127.0.0.1:4175/pixel-agents/index.html |
