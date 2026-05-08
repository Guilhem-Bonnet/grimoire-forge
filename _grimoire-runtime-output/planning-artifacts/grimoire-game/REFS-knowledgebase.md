# Base de connaissance — Références du Grimoire Game

> Projet : **Grimoire Game** — Catalogue de références
> Version : 2.0 — Avril 2026

---

## 1. Vue d'ensemble des références

| Projet | Stars | Stack | Maturité | Pertinence |
|---|---|---|---|---|
| pixel-agents | ~800 | TypeScript+React+Canvas2D | Prototype actif | ⭐⭐⭐⭐⭐ Directe |
| DeskRPG | ~120 | Next.js+TypeScript 91.3% | v0.2.3 actif | ⭐⭐⭐⭐ Très haute |
| superpowers | ~135k | Shell+JS+TypeScript | v5.0.7 actif | ⭐⭐⭐⭐⭐ Workflow dev |
| claude-mem | ~45k | TypeScript 80.8% | v10.6.3 actif | ⭐⭐⭐⭐⭐ Mémoire directe |
| gstack | ~63.8k | TypeScript 69.7%+Go | v0.15.4 actif | ⭐⭐⭐⭐ Design+QA+Sécurité |
| OpenClaw | ~348k | Multi-lang, Gateway | Production | ⭐⭐⭐ Gateway pattern |
| WorkAdventure | ~5.4k | TypeScript+Svelte | v1.30 stable | ⭐⭐⭐ Architecture |
| Gather.town | N/A | Propriétaire | Production | ⭐⭐⭐ UX référence |

---

## 2. pixel-agents (pablodelucca)

**URL** : `https://github.com/pablodelucca/pixel-agents`

### Ce que c'est

Un outil de visualisation d'agents IA dans un open-space virtuel. Les agents s'affichent comme des personnages pixel art qui bougent et agissent en fonction de leur activité réelle (lire des transcripts JSONL).

### Stack technique

```
Frontend : TypeScript + React + Canvas2D
Backend  : Node.js (minimal)
État     : State machine custom
Pathfinding: BFS (breadth-first search)
Data     : JSONL transcripts (lecture de fichiers)
```

### Points clés à réutiliser

1. **Le pattern de lecture JSONL** : `src/agentTracker.ts` — watch les fichiers de transcripts et en extrait les events. C'est exactement ce dont nous avons besoin pour le bridge vers grimoire-kit.

2. **La state machine des agents** : États simples mais efficaces (idle, working, communicating). Notre implémentation sera plus riche (XState) mais le mapping tool→action est directement réutilisable.

3. **Le pixel art Canvas2D** : Approche sans framework (pas de Phaser/Pixi), rendu direct. Valide notre choix architectural.

4. **Les animations procédurales** : Pas de sprites externes au départ — des formes colorées animées. Permet de libérer l'équipe de la dépendance aux assets.

### Code de référence clé

```typescript
// Exemple du pattern de mapping tool→animation (à adapter)
const TOOL_ACTION_MAP: Record<string, AgentAction> = {
  'read_file':         'reading',
  'write_file':        'working',
  'run_in_terminal':   'executing',
  'search':            'searching',
  'default':           'thinking'
};
```

### Limites / Différences avec notre projet

- Pas de multi-rooms (une seule pièce)
- Pas de Kanban intégré
- Pas de serveur WebSocket (juste file watching)
- UX minimale (pas de panels de détails)
- Pas d'intégration grimoire-kit

### Status du projet

Prototype actif, développement en cours. L'auteur a mentionné une version "platform-agnostic" en cours de conception, qui correspond exactement à notre bridge pattern.

---

## 3. DeskRPG (dandacompany)

**URL** : `https://github.com/dandacompany/DeskRPG`

### Ce que c'est

Bureau virtuel 2D avec des personnages animés pour les équipes distribuées. Intègre un Kanban, les IA comme NPCs, et un éditeur de map. Stack Next.js avec SQLite/PostgreSQL.

### Stack technique

```
Frontend : Next.js + TypeScript (91.3% TS)
Rendu    : Canvas 2D (custom)
Backend  : Node.js + tRPC
DB       : SQLite (dev) / PostgreSQL (prod)
Assets   : LPC sprites (Liberated Pixel Cup)
Map      : Tiled editor (.tmj format)
IA       : OpenClaw gateway + AI meetings room
Auth     : NextAuth.js
```

### Points clés à réutiliser

1. **Schéma de base de données** : DeskRPG a résolu le problème de la persistence d'état pour les bureaux virtuels. Leur schéma (users, rooms, tasks, files, ai_sessions) est une bonne base.

2. **Tiled map format** : Utilise les mêmes formats Tiled JSON (.tmj) que nous voulons utiliser. Leur loader est une référence directe.

3. **LPC sprites** : Les sprites du Liberated Pixel Cup (LPC) sont en licence libre et appropriés pour notre style pixel art.
  - URL assets: `https://lpc.opengameart.org/`
  - Incluent: personnages, meubles, intérieurs

4. **Kanban in-world** : DeskRPG a un task board (대기/진행중/중단/완료 = backlog/in_progress/blocked/done) avec rendu in-world. Peut servir de référence UX.

5. **AI meetings room** : La salle de réunion AI de DeskRPG est conceptuellement similaire à notre Challenge Room.

### Différences avec notre projet

- DeskRPG est orienté équipes humaines, nous sommes centrés sur des agents IA
- Pas de grimoire-kit integration
- Pas de ECS (OOP classique)
- Plus lourd (Next.js vs SvelteKit)

### Assets LPC recommandés

```
Personnages:
  - Universal LPC Spritesheet: https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator/
  - Catégories disponibles: body, hairstyle, clothes, tools, weapons
  
Mobilier:
  - LPC Office Furniture: https://opengameart.org/content/lpc-office-furniture
  - LPC Computer Equipment: https://opengameart.org/content/lpc-computer-equipment
  
Tilesets:
  - LPC Floors and Walls: https://opengameart.org/content/lpc-floors-and-walls
  - LPC Interior Castle: https://opengameart.org/content/lpc-terrains
```

---

## 4. OpenClaw

**URL** : `https://github.com/openclaw/openclaw`

### Ce que c'est

Framework multi-agents multi-canaux avec 348k stars. Gère la connexion entre agents IA et de nombreux canaux (WhatsApp, Telegram, Discord, Slack, etc.) via une passerelle WebSocket centralisée.

### Ce qui est pertinent pour nous

1. **Gateway WebSocket pattern** : OpenClaw utilise un serveur WebSocket central qui reçoit tous les events et distribue selon les sessions. Notre `GameServer.ts` peut s'en inspirer.

2. **sessions_* tools** : Les outils `sessions_list`, `sessions_subscribe`, `sessions_unsubscribe` définissent un pattern propre pour s'abonner à des streams d'events.

3. **Live Canvas A2UI** : OpenClaw a un "Canvas A2UI" pour visualiser les agents. C'est exactement ce que nous construisons. La différence : notre canvas est une vue 2D gamifiée, le leur est plus abstrait.

4. **Skills platform (ClawHub)** : Concept de skills modulaires que les agents peuvent utiliser. Correspond à notre `SkillTreeConfig`.

### Pattern de connexion d'agent (à adapter)

```typescript
// Pattern OpenClaw (simplifié)
interface AgentSession {
  id: string;
  created_at: string;
  state: 'active' | 'idle' | 'terminated';
  channels: ChannelRef[];
  messages: Message[];
}

// Dans notre cas: 
interface GameAgentSession extends AgentSession {
  roomId: RoomId;
  position: Position;
  currentTask?: TaskId;
  workflowState?: WorkflowStep;
}
```

---

## 5. WorkAdventure

**URL** : `https://github.com/workadventure/workadventure`

### Ce que c'est

Monde virtuel temps-réel open-source avec 5.4k stars. Permet de créer des bureaux virtuels collaboratifs où on peut se déplacer et se voir. Utilise TypeScript + Svelte.

### Ce qui est pertinent pour nous

1. **Architecture microservices** : WorkAdventure utilise une architecture Docker compose avec services séparés (back-api, front, pusher, maps, etc.). Notre architecture est plus simple (monolith léger), mais leur découpage en services est une référence pour la phase de scale.

2. **TypeScript + Svelte** : Exactement notre stack. Leur choix est validé par une production à large échelle.

3. **Map management** : Leur système de gestion de maps multiples avec transitions entre rooms est une référence directe.

4. **WebRTC intégration** : WorkAdventure supporte la vidéo. Pas besoin pour nous dans un premier temps, mais c'est une feature possible pour une future salle de visio entre équipes.

5. **Tiled map support** : Utilise aussi Tiled JSON, cohérent avec notre choix.

### Ce qui est trop complexe pour nous

- Architecture microservices (pas pour la v1)
- WebRTC (pas nécessaire)
- Multi-tenant (pas nécessaire)
- Scaling horizontal (la cible est locale/single-user)

---

## 6. Gather.town (référence UX)

**URL** : `https://gather.town`

### Ce que c'est

Bureau virtuel commercial très utilisé pour les équipes remote. Interface inspirante pour l'UX de notre projet.

### Patterns UX à s'inspirer

1. **Click-to-move** : Cliquer sur une destination et l'avatar marche vers elle. Simple et intuitif.

2. **Zone de proximity** : Quand deux personnages sont proches, une fenêtre vidéo s'ouvre. Pour nous : zone de "discussion" qui affiche les messages échangés entre agents.

3. **Objets interactifs** : Cliquer sur un objet déclenche une action (tableau → mode présentation, machine à café → "prendre un café"). Inspirant pour notre mobilier interactif.

4. **Minimap** : Gather a une minimap compact dans le coin. Référence directe pour notre minimap.

5. **Screenshare area** : Zone dédiée à la présentation d'écran. Pour nous : la zone des grands écrans dans la Challenge Room.

---

## 7. superpowers (obra)

**URL** : `https://github.com/obra/superpowers`

### Ce que c'est

Framework de skills pour agents de code (Claude Code, Cursor, Codex, Gemini CLI). 135k stars, v5.0.7. Un ensemble de skills composables qui transforment Claude Code en équipe de dev complète. Chaque skill s'active automatiquement au bon moment.

### Stack technique

```
Shell 58.8% + JavaScript 29.6% + TypeScript 2.8%
Écosystème: Claude Code plugin marketplace (et Cursor, Codex, Gemini)
Installation: /plugin install superpowers@claude-plugins-official
```

### Skills pertinents pour notre projet

1. **`brainstorming`** — Raffinement socratique des idées via questions. Modèle direct pour notre Challenge Room (poser des questions forçantes avant d'écrire du code).

2. **`writing-plans`** — Décompose le travail en tâches bite-sized (2-5 minutes chacune). Chaque tâche a : chemins de fichiers exacts, code complet, étapes de vérification. C'est exactement notre format TASK-xxx dans EPICS.

3. **`subagent-driven-development`** — Lance un sous-agent frais par tâche avec une review en 2 étapes (conformité spec + qualité code). **Référence directe pour notre EPIC-02 multi-agent pattern**.

4. **`test-driven-development`** — Cycle RED-GREEN-REFACTOR strict. Supprime le code écrit avant les tests. **La méthodologie TDD obligatoire du projet**.

5. **`systematic-debugging`** — 4 phases de root cause analysis. Iron Law: aucun fix sans investigation. **Modèle pour notre Debug Console gamifiée**.

6. **`verification-before-completion`** — Vérifie que c'est réellement done avant de déclarer victoire. **Critères d'acceptation de chaque TASK**.

### Workflow complet (à adopter comme processus)

```
brainstorming → writing-plans → subagent-driven-development
     ↓                                      ↓
  [design doc]               [test-driven-development par tâche]
                                           ↓
                              requesting-code-review
                                           ↓
                              finishing-a-development-branch
```

### Ce qui est différent chez nous

- Superpowers est pour *créer* du code ; nous l'utilisons *et* le visualisons
- Notre Challenge Room est une version gamifiée de leur `requesting-code-review`
- Notre War Room = leur concept de "10-15 parallel sprints" rendu visible

---

## 8. claude-mem (thedotmack)

**URL** : `https://github.com/thedotmack/claude-mem`

### Ce que c'est

Système de compression et persistance de mémoire pour Claude Code. **45k stars, v10.6.3.** Capture automatiquement tout ce que Claude fait pendant les sessions, compresse avec l'agent-sdk, et injecte le contexte pertinent dans les sessions futures.

### Stack technique

```
TypeScript 80.8% + JavaScript 13.2%
Runtime: Bun (process manager)
DB: SQLite (sessions, observations, summaries) + Chroma (vector search)
Port local: 37777 (Web Viewer UI)
Hooks: SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd
Search: MCP tools (search → timeline → get_observations)
```

### Architecture — Référence directe pour notre Library Room

Claude-mem résout exactement le problème que nous voulons visualiser. Leur architecture est notre référence :

```
Lifecycle Hooks:
  SessionStart     → charge context des sessions passées
  UserPromptSubmit → prépare le contexte avant requête
  PostToolUse      → capture l'observation après chaque tool call
  Stop             → génère un summary de la session
  SessionEnd       → persiste en DB

DB Schema:
  sessions         → id, created_at, project_path, agent_model
  observations     → id, session_id, tool_name, input, output, timestamp
  summaries        → id, session_id, content, tokens_saved

Search MCP (3 couches — progressive disclosure):
  1. search()          → index compact avec IDs (~50-100 tokens/résultat)
  2. timeline()        → contexte chronologique autour d'un résultat
  3. get_observations() → détails complets par IDs (~500-1000 tokens/résultat)
```

### Points clés à adapter

1. **ClaudeMemAdapter** (déjà dans TECH-grimoire-game.md) : Lire la DB SQLite de claude-mem pour afficher les mémoires des agents dans la Library Room.

2. **Web Viewer localhost:37777** : Peut être intégré comme iframe ou source de données pour notre bibliothèque.

3. **Lifecycle hooks → animations** :
   - `PostToolUse` = déclencher l'animation memory write (livre qui se range)
   - `SessionStart` = animation memory read (agent qui ouvre un livre)

4. **Progressive disclosure** : Notre panneau Library Room adopte les mêmes 3 couches (liste compacte → timeline → détail complet).

### Licence

AGPL-3.0 — Si on intègre en réseau, on doit publier notre code source. Utiliser uniquement en lecture locale (lecture DB SQLite) pour rester en dehors du scope de l'AGPL.

---

## 9. gstack (garrytan)

**URL** : `https://github.com/garrytan/gstack`

### Ce que c'est

Le setup exact de Garry Tan (CEO de Y Combinator) pour Claude Code. 63.8k stars. 23+ skills qui couvrent tout le sprint : office-hours → plan → build → review → test → ship → retro. MIT License.

### Stack technique

```
TypeScript 69.7% + Go Template 20.9% + Shell 4.3%
Runtime: Bun
Méthodologie: Sprint structuré (Think → Plan → Build → Review → Test → Ship → Reflect)
Parallélisme: via Conductor (conductor.build) — 10-15 sprints simultanés
```

### Skills pertinents pour notre projet

1. **`/design-html`** — Génère du HTML de production avec Pretext (texte qui reflow sur resize, hauteurs qui s'adaptent au contenu). **Utiliser pour générer les composants UI du board** (panels, modals, HUD). Détecte React/Svelte/Vue automatiquement → nos composants Svelte.

2. **`/design-consultation`** — Construit un design system complet depuis zéro, propose des risques créatifs, génère des mockups produit réalistes. **Utiliser avec l'Anthropic Frontend Design plugin pour la DA**.

3. **`/design-shotgun`** — Génère plusieurs variantes visuelles et ouvre un tableau de comparaison dans le browser. **Utiliser pour choisir la direction visuelle des rooms**.

4. **`/cso`** — OWASP Top 10 + STRIDE threat model. Zero-noise : 17 exclusions de faux positifs, gate de confiance 8/10+, vérification indépendante. **Utiliser pour auditer notre serveur WebSocket et l'accès à la DB**.

5. **`/browse`** — Chromium headless réel. **Modèle pour visualiser l'activité de navigation des agents** (quand un agent fait `fetch_webpage`, l'animation montre un mini-browser).

6. **`/retro`** — Analyse de sprint par personne, shipping streaks, test health trends. **Modèle pour notre vue "Retrospective" à ajouter en v0.6**.

### Concept Conductor → War Room

Conductor (conductor.build) = outil qui lance 10-15 sessions Claude Code en parallèle, chacune isolée. 10,000-20,000 lignes de code par jour.

**Lien direct avec notre War Room** : La War Room de l'Orchestrateur est la visualisation gamifiée de ce que Conductor fait en arrière-plan. Chaque "session parallel" de Conductor devient un agent visible sur le canvas.

---

## 10. Plugins Anthropic (références)

### Frontend Design — `https://claude.com/plugins/frontend-design`

Plugin officiel Anthropic pour la conception UI. Génère des designs, mockups, et code frontend. **Utiliser pour générer les assets UI du board** (pas les sprites in-game, mais l'interface de configuration, les panels, les modals).

**Workflow recommandé** :
1. Utiliser gstack `/design-consultation` pour définir le design system
2. Utiliser le plugin Frontend Design pour générer des mockups HTML
3. Utiliser gstack `/design-html` pour transformer en composants Svelte production

### Code Review — `https://claude.com/plugins/code-review`

Plugin Anthropic pour la review de code. Peut être intégré comme outil de **pre-push validation**. Complète notre workflow Challenge Room.

### Security Guidance — `https://claude.com/plugins/security-guidance`

Plugin Anthropic pour la guidance sécurité. Référence pour :
- Sécuriser le serveur WebSocket (auth token)
- Protéger les fichiers de config locaux
- XSS prevention sur l'affichage du contenu agent

**En pratique** : utiliser gstack `/cso` (plus opérationnel, OWASP+STRIDE automatisé) et ce plugin pour la guidance manuelle.

---

## 11. Ressources additionnelles (ancienne section 7)

### Assets libres recommandés

```
Musique lo-fi (licence CC0/CC-BY):
  - ccMixter: http://ccmixter.org (tags: lofi, ambient, chiptune)
  - freesound.org: sons libre pour effets
  - itch.io/game-assets: nombreux packs pixel art et musique

Fonts pixel:
  - VT323: https://fonts.google.com/specimen/VT323
  - Press Start 2P: https://fonts.google.com/specimen/Press+Start+2P
  - Silkscreen: https://fonts.google.com/specimen/Silkscreen

Tilesets libres:
  - Kenney.nl: https://kenney.nl/assets (CC0, qualité!)
    * Kenney Tiny Town (intérieurs)  
    * Kenney UI Pack (interface)
  - OpenGameArt: https://opengameart.org (licence variable)
  - LPC sprites: https://lpc.opengameart.org
```

### Bibliothèques NPM pertinentes

```
ECS:
  - bitecs: ultra-fast ECS pour TypeScript (alternative si custom trop long)
  - miniplex: ECS réactif pour React/Svelte (option légère)

State machine:
  - xstate: machine d'état formelle (notre choix)
  - zag: alternative plus légère

Moteur jeu léger:
  - Kaboom.js: si on veut quand même un moteur minimal
  - Excalibur.js: TypeScript natif, Canvas 2D, leger

Charting pour les vues analytics:
  - D3.js: DAG visualization
  - vis-network: graph networks

DB:
  - better-sqlite3: SQLite sync pour Node.js (notre choix)
  - Drizzle ORM: TypeScript-first ORM
```

---

## 12. Ce qu'on construit vs ce qui existe

### Matrice "Build vs Buy vs Adapt"

| Feature | Action | Source | Effort |
|---|---|---|---------|
| Canvas 2D renderer | Build custom | - | L |
| ECS core | Build custom | - | M |
| JSONL bridge | Adapt | pixel-agents | S |
| Agent state machine | Adapt | pixel-agents | S |
| Tilemap loader | Adapt | DeskRPG + Tiled | S |
| LPC sprites | Buy/Download | lpc.opengameart | XS |
| Pathfinding A* | Build | - | S |
| WebSocket server | Build | - | S |
| Kanban board | Build (in-world) | DeskRPG (référence) | M |
| Multi-room navigation | Build | WorkAdventure (référence UX) | M |
| Memory visualization | Adapt | claude-mem (DB SQLite+Chroma) | M |
| Memory lifecycle hooks | Adapt | claude-mem (hooks pattern) | S |
| Dev workflow | Adopt | superpowers (TDD+subagent-dev) | XS |
| UI components | Adapt | gstack /design-html (Svelte) | S |
| Security review | Invoke | gstack /cso (OWASP+STRIDE) | XS |
| Investigation workflow (debug) | Adopt | gstack /investigate + INVESTIGATION_PROMPT | XS |
| DX Review challenge | Adopt | gstack /devex-review (8 dimensions Addy Osmani) | XS |
| Auto-Challenge pipeline | Build | gstack /autoplan (inspiration séquence) | S |
| Workflow DAG | Adapt | D3.js | S |
| grimoire-kit bridge | Build | - | M |
| Configuration skill tree | Build | - | M |
| Web Audio API (sons in-game) | Build | Web Audio API native | S |
| Système XP / achievements | Build | - | M |
| Observatory (supervisor read-only) | Adapt | observatory.html existant (iframe sandbox) | XS |
| Timeline scrubber | Build | - | M |
| AgentAdapter pattern (multi-plateforme) | Build | GrimoireJSONLAdapter (implémenté) + ClaudeCodeAdapter/OpenClawAdapter (stubs) | S |
| Stats RPG agents (focus, speed, precision) | Build | - | S |
| Mode spectateur read-only | Build | - | S |
| Retro Room sprint gamifiée | Build | gstack /retro (streak, per-agent breakdown, tweetable summary, JSON snapshot) | M |
| Performance/Canary Panel (War Room) | Build | gstack /benchmark + /canary (LCP/CLS/INP, baselines) | S |
| Learnings Shelf (Library Room) | Adapt | gstack /learn (learnings.jsonl : confidence, insight, files) | S |
| Completeness Gate LAKE detector | Adopt | gstack Completeness Principle — « Boil the Lake » | XS |
| pixel-agents (canvas ECS + JSONL monitoring) | Adapt | pablodelucca/pixel-agents v1.2.0 (6.1k★) — sub-agent viz, external assets, BFS pathfinding, debug view | L |
| superpowers (workflow 7étapes) | Adopt | obra/superpowers v5.0.7 (135k★) — worktrees, two-stage review, parallel dispatch, finishing-branch | M |
| Claude plugins officiels (Power Cards) | Adopt | Anthropic : frontend-design (455k), code-review (212k), security-guidance (107k) | XS |

| superpowers/systematic-debugging | Adopt | 4 phases (Root Cause → Pattern → Hypothesis → Implementation), Iron Law, condition-based-waiting, ~15-30min vs 2-3h thrashing | XS |
| superpowers/verification-before-completion | Adopt | Gate Function 5 étapes (IDENTIFY → RUN → READ → VERIFY → CLAIM), evidence before claims, audit log JSONL | XS |
| superpowers/dispatching-parallel-agents | Adopt | Context isolation (no inheritance), domain decomposition, 1 agent/domaine, conflict detection | S |

| superpowers/requesting-code-review | Adopt | Dispatch reviewer subagent avec contexte isolé (SHAs), review après chaque tâche, Critical bloque progression | XS |
| superpowers/receiving-code-review | Adopt | Vérification technique avant implémentation, pushback raisonné, YAGNI check, zéro accord performatif | XS |
| superpowers/finishing-a-development-branch | Adopt | 4 options (merge/PR/keep/discard), tests oblig, typed discard, nettoyage worktree | XS |
| superpowers/subagent-driven-development | Adopt | Fresh subagent par tâche, 2-stage review (spec puis qualité), sélection modèle par complexité, statuts DONE/BLOCKED | S |
| gstack /investigate | Adopt | Systématic root-cause debug, Iron Law, auto-freeze au module, stop après 3 échecs | XS |
| gstack /cso | Adopt | OWASP Top 10 + STRIDE, confidence ≥ 8/10, zero-noise 17 exclusions, exploit scenario obligatoire | S |
| gstack /autoplan | Adopt | Pipeline one-shot : CEO → design → eng review, décisions de goût seulement pour validation humaine | XS |
| gstack /codex | Adopt | Second opinion OpenAI Codex CLI, 3 modes (review/adversarial/consultation), cross-model analysis | S |

**Légende** : XS=<1j · S=1-3j · M=3-7j · L=7-14j

---

*Fin de la Base de Connaissance Références — Version 2.0*
