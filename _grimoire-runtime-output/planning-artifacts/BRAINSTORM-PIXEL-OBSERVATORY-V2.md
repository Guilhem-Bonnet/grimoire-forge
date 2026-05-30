# Brainstorm : Pixel Observatory V2 — Tableau de Bord Agentic Gamifié

## Contexte

Le Grimoire Observatory actuel (`observatory.py`, ~1960 lignes) génère un dashboard HTML
self-contained avec 7 vues analytiques (Overview, Timeline, Swimlane, DAG, Network, Log, Metrics).
Il est servi sur `localhost:8420` avec auto-reload.

L'objectif est d'intégrer un concept inspiré de **Pixel Agents** (6k★ GitHub) : transformer
le dashboard en une **expérience de jeu vidéo** où les agents sont visualisés comme des
personnages pixel art dans un bureau virtuel, avec contrôle temporel et configuration en temps réel.

## Contraintes

| Contrainte | Description |
|---|---|
| **Single-file** | Le HTML généré doit rester autoporté (zero CDN, zero assets externes) |
| **Stdlib only** | Le générateur Python reste sans dépendances |
| **Backward compatible** | Les 7 vues existantes doivent continuer à fonctionner |
| **Procédural** | Les sprites pixel art sont dessinés par canvas (pas de PNG/SVG inline) |
| **Performance** | Le game loop doit tourner à 30+ FPS avec 20+ agents |
| **Données existantes** | Sources : BMAD_TRACE.md, .event-log.jsonl, .agent-graph.yaml |

## Approche A : Évolution incrémentale — Nouvel onglet "Office"

**Principe** : Ajouter un 8e onglet "🎮 Office" dans l'Observatory existant avec une barre
de timeline globale en bas de page.

**Avantages** :

- Un seul fichier à maintenir
- Compatibilité assurée avec les vues existantes
- Transition douce pour les utilisateurs

**Inconvénients** :

- Le fichier devra ~4000+ lignes
- Couplage entre le code dashboard et le game engine
- Difficile à tester indépendamment

**Effort** : M

## Approche B : Module Game séparé + orchestrateur

**Principe** : Créer `observatory_game.py` qui importe les parsers d'observatory.py et génère
un HTML dédié au game view. L'observatory original expose un lien vers le game.

**Avantages** :

- Séparation des responsabilités
- Testable indépendamment
- Peut évoluer en parallèle

**Inconvénients** :

- Deux URLs à gérer
- Duplication potentielle de code CSS/JS
- L'utilisateur doit naviguer entre deux pages

**Effort** : L

## Approche C : Observatory V2 — Refonte intégrée (recommandée)

**Principe** : Étendre `observatory.py` avec une architecture modulaire interne. Le HTML template
est découpé en sections (CSS, game engine, dashboard views, timeline). Un nouvel onglet "🎮 Office"
est ajouté en position 0. La barre de timeline est un composant global visible sur tous les onglets.

**Avantages** :

- Expérience unifiée
- Un seul point d'entrée (`localhost:8420`)
- Architecture modulaire dans un seul fichier
- Le timeline scrubber enrichit TOUTES les vues (pas juste le game)

**Inconvénients** :

- Fichier plus volumineux
- Complexité accrue du template

**Effort** : L

**Risques** :

- Performance du game loop vs DOM rendering → Mitigation : canvas séparé, requestAnimationFrame discovery
- Taille du fichier → Mitigation : template strings bien structurées, code JS minifiable

**Prototype minimal** : Game engine avec 3 agents animés + timeline basique

## Recommandation

**L'approche C** est recommandée parce que :

1. L'utilisateur veut un **vrai tableau de bord unifié** — pas deux pages séparées
2. Le timeline scrubber doit piloter TOUTES les vues, pas seulement l'office
3. La structure modulaire interne permet d'évoluer sans fragmenter

## Concept détaillé — Approche C

### 1. Vue Office (Pixel Art)

```text
┌─────────────────────────────────────────────────────┐
│ 🔭 Grimoire Observatory           [Search] [Export] │
├──────┬──────┬──────┬──────┬──────┬──────┬──────┬────┤
│🎮 Off│ Ovvw │ Tmln │ Swim │ DAG  │ Netw │ Log  │Met │
├──────┴──────┴──────┴──────┴──────┴──────┴──────┴────┤
│                                                      │
│  ┌────────────────────────────────────────────┐      │
│  │       PIXEL ART OFFICE (Canvas)            │      │
│  │                                            │      │
│  │  🪴    ╔═══╗  📋    ╔═══╗  🔬    ╔═══╗   │      │
│  │       ║Mary║       ║John║       ║Quinn║  │      │
│  │       ╚═══╝        ╚═══╝        ╚═══╝   │      │
│  │  💻    ╔═════╗      🎯    ╔═════╗         │      │
│  │       ║Amelia║           ║Winston║       │      │
│  │       ╚═════╝            ╚═════╝         │      │
│  │                 🧙                        │      │
│  │              ╔═══════╗                    │      │
│  │              ║  SOG  ║                    │      │
│  │              ╚═══════╝                    │      │
│  └────────────────────────────────────────────┘      │
│                                                      │
│  ┌─ Agent Panel ──────────────────────────────┐      │
│  │ 👤 Amelia (dev)  Trust: 92  ⚡ typing      │      │
│  │ Tools: [✅ edit] [✅ search] [⬜ execute]  │      │
│  └────────────────────────────────────────────┘      │
│                                                      │
├──────────────────────────────────────────────────────┤
│ ⏮ ◀ ⏸ ▶ ⏭  ━━━━━━━●━━━━━━━━━━━  1x ⏩ │ LIVE │
│ 14:32  ▓▓▓▓░░▓▓▓▓▓▓░░▓▓  Session: 2026-03-28  14:45│
└──────────────────────────────────────────────────────┘
```

### 2. Système de sprites procéduraux

Chaque agent est un personnage 16×16 pixels dessiné programmatiquement :

| Agent | Couleur | Accessoire | Desk item |
|---|---|---|---|
| Mary (analyst) | Jaune #d29922 | Lunettes | Graphique |
| Winston (architect) | Cyan #39d2c0 | Plan | Blueprint |
| Amelia (dev) | Vert #3fb950 | Casque | Laptop |
| John (pm) | Orange #f0883e | Cravate | Clipboard |
| Quinn (qa) | Violet #bc8cff | Loupe | Bug report |
| Bob (sm) | Rose #f778ba | Post-it | Kanban |
| Paige (tech-writer) | Vert clair #7ee787 | Stylo | Document |
| SOG (orchestrator) | Bleu #58a6ff | Chapeau magique | Wand |
| Murat (tea) | Rouge #f85149 | Badge | Terminal |

**Animation frames** (par état) :

| État | Frames | Description |
|---|---|---|
| idle | 2 | Léger balancement |
| walking | 4 | Mouvement des jambes |
| typing | 3 | Mains tapant sur clavier |
| reading | 2 | Page qui tourne |
| speaking | 3 | Bulle de dialogue |
| waiting | 2 | Tap du pied |
| error | 2 | Flash rouge |
| celebrating | 3 | Bras levés |

### 3. Bureau virtuel — Layout

Layout top-down sur grille 32×24 (512×384 ou multiples) :

```text
Zone A (haut-gauche)     : Team Vision (analyst, pm, ux-designer)
Zone B (haut-droite)     : Team Architecture (architect, tech-writer)
Zone C (centre)          : Orchestrator (SOG) — point central
Zone D (bas-gauche)      : Team Dev (dev, qa, tea)
Zone E (bas-droite)      : Team Ops (sm)
Zone F (murs)            : Whiteboards, Kanban, Graphiques
```

Éléments du bureau :

- **Sol** : Tiles 16×16 (plancher bois, moquette par zone)
- **Murs** : Bordures périphériques + séparations de zones
- **Meubles** : Desks (32×16), chaises, PC, bibliothèques
- **Déco** : Plantes, machine café, fenêtres, horloge
- **Interactions** : Whiteboard (affiche les métriques live), Kanban (tâches en cours)

### 4. Timeline scrubber global

Le scrubber est un composant **global** visible en permanence en bas :

**Fonctionnalités** :

- **Playback** : ⏮ ◀ ⏸ ▶ ⏭ — joue les événements comme un film
- **Speed** : 0.5x, 1x, 2x, 4x, 8x
- **Scrub bar** : barre avec curseur draggable + heatmap de densité d'événements
- **Session selector** : dropdown pour choisir la session
- **Time range** : affiche timestamp courant + total
- **Live mode** : badge "LIVE" quand synchro temps réel

**Impact sur chaque vue** :

| Vue | Effet du scrubber |
|---|---|
| Office | Les agents se déplacent et animent selon le moment sélectionné |
| Timeline | Surligne l'événement courant, auto-scroll |
| Swimlane | Indicateur horizontal "now" qui se déplace |
| DAG | Les barres Gantt se remplissent progressivement |
| Network | Les liens s'allument quand une interaction est active |
| Log | Filtre automatique jusqu'au timestamp courant |
| Metrics | Recalcul progressif des métriques |

### 5. Agent Configuration Panel

Panneau latéral (drawer) accessible en cliquant sur un agent :

**Sections** :

- **Profil** : Nom, persona, rôle, avatar pixel art agrandi
- **Status** : État actuel (idle, typing, etc.), dernière action
- **Trust Score** : Jauge + historique graphique
- **Outils** : Liste des tools avec toggles on/off
- **Capabilities** : Static + emergent capabilities
- **Historique** : 10 dernières actions de cet agent
- **Handoffs** : Agents avec lesquels il a interagi (mini-graphe)
- **Config** : Paramètres ajustables (autonomy level, tool restrictions)

### 6. Moteur de jeu (Game Engine)

Architecture JavaScript du game engine :

```text
GameEngine
├── SpriteFactory          — Génération procédurale des sprites
│   ├── CharacterSprite    — Personnages (agents)
│   ├── FurnitureSprite    — Meubles
│   └── TileSprite         — Sols, murs
├── OfficeLayout           — Placement des éléments sur la grille
│   ├── Grid               — Matrice 2D de tiles
│   ├── ZoneManager        — Zones par équipe
│   └── PathFinder         — A* pour déplacements agents
├── AgentController        — Gestion des personnages
│   ├── StateMachine       — idle/walk/type/read/speak/error
│   ├── AnimationPlayer    — Frame cycling
│   └── BubbleManager      — Speech/thought bubbles
├── TimelineEngine         — Pilotage temporel
│   ├── EventQueue         — File d'événements ordonnés
│   ├── PlaybackControl    — play/pause/seek/speed
│   └── StateSnapshot      — État de chaque agent à chaque instant
├── InteractionManager     — Sélection, hover, click agents
└── Renderer               — Canvas 2D (requestAnimationFrame)
    ├── Camera             — Pan, zoom
    ├── LayerSystem        — Floor → Furniture → Agents → UI
    └── ParticleSystem     — Effets visuels (confettis, sparks)
```

### 7. Workflow de mise à jour continue

Le système doit se mettre à jour en temps réel :

```text
observatory.py serve --port 8420
  │
  ├── Watcher Thread (toutes les 2s)
  │   ├── Détecte changements dans BMAD_TRACE.md, .event-log.jsonl
  │   ├── Reparse les données
  │   └── Régénère observatory.html
  │
  └── Browser (JS)
      ├── HEAD polling (toutes les 3s) détecte changement ETag
      ├── Fetch du nouveau JSON embarqué
      ├── Merge avec état courant (position agents, camera, etc.)
      └── Smooth transition (agents marchent vers nouvelle position vs teleport)
```

### 8. Workflow BMAD pour le développement

```text
Phase 0: Brainstorm (ce document) ✅
Phase 1: Plan détaillé d'implémentation
Phase 2: Skill "grimoire-pixel-observatory" + instruction pour le game engine
Phase 3: Implémentation Core
  3a: Sprite Factory (génération procédurale canvas)
  3b: Office Layout (grille, zones, meubles)
  3c: Agent Controller (états, animations)
  3d: Timeline Engine (playback, seek, speed)
  3e: Renderer (camera, layers, particles)
Phase 4: Intégration Observatory
  4a: Nouvelle vue "Office" dans le HTML template
  4b: Timeline bar globale
  4c: Agent config drawer
  4d: Réactivité cross-vues
Phase 5: Polish
  5a: Effets visuels (particules, transitions)
  5b: Sons (optionnel, Web Audio API)
  5c: Mini-map
  5d: Keyboard shortcuts
Phase 6: Tests + Documentation
```

## Inspiration visuelle

### Pixel-agents (référence principale)

- Bureau top-down avec personnages qui marchent entre les postes
- Animation basée sur l'activité réelle de l'agent (JSONL parsing)
- Speech bubbles pour les demandes d'input
- Canvas 2D avec game loop + BFS pathfinding

### Compléments Grimoire

| Feature | Pixel-agents | Grimoire Observatory V2 |
|---|---|---|
| Source de données | Claude Code JSONL | BMAD_TRACE + event-log + agent-graph |
| Agents supportés | Claude Code only | Tous les agents BMAD (10+) |
| Timeline | Non | Timeline scrubber complet |
| Configuration | Non | Config tools/capabilities |
| Dashboard | Non | 7 vues analytiques intégrées |
| Office editor | Oui (drag & drop) | Auto-layout par équipe |
| Multi-session | Non | Oui (session selector) |
| Trust scores | Non | Oui (jauges + historique) |
| Handoff viz | Non | Oui (agents marchent vers destinataire) |

## Risques et mitigations

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Taille fichier HTML > 200KB | Haute | Faible | Acceptable pour single-file, gzip le réduit à ~30KB |
| Performance 10+ agents | Moyenne | Moyen | Canvas offscreen pour sprites, batch rendering |
| Complexité maintenance | Moyenne | Moyen | Architecture modulaire, code bien structuré |
| Données insuffisantes | Faible | Moyen | Mode démo avec données simulées |

## Décision

**Approche C retenue** : Observatory V2 intégré, avec game engine procédural + timeline global.
