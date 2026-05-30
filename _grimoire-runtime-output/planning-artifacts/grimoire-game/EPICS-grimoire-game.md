# Epics, Stories & Tasks — Grimoire Game Board

> Projet : **Grimoire Game** — Plan de développement détaillé
> Version : 1.1 — Avril 2026
> Cadence : backlog séquencé par sprints relatifs (S0-S11), sans durée normative dans ce document
> Auteurs : BMad Master + SM + PM + Architect + Dev + QA (multi-agent)

---

## Légende des assignations

| Code | Rôle | Agent | Spécialité |
| --- | --- | --- | --- |
| `@arch` | Winston | Architect | Architecture, infrastructure, ADR |
| `@dev` | Amelia | Developer | Implémentation TypeScript, TDD |
| `@qa` | Quinn | QA Engineer | Tests, couverture, e2e |
| `@pm` | John | Product Manager | Specs, acceptance criteria |
| `@sm` | Bob | Scrum Master | Sprint planning, backlog |
| `@tw` | Paige | Tech Writer | Documentation |
| `@ux` | Sally | UX Designer | UI/UX, mockups, DA |
| `@anl` | Mary | Analyst | Recherche, veille tech |
| `@tea` | Murat | Test Architect | Stratégie tests, fixtures |
| `@orch` | Orchestrateur | BMad Master | Coordination globale, dispatch |

---

## Cadre de pilotage

- `S0` à `S11` décrivent un ordre relatif de livraison, pas un engagement calendaire figé.
- Une story prête à lancer doit expliciter ses dépendances, son statut de préparation et ses critères d'acceptation story.
- Le front post-challenge `GAME-TKT-052 -> GAME-TKT-053 -> GAME-TKT-054` est maintenant prouve localement sur la tranche runtime de reference ; les lots multi-PC, multi-host et rooms riches restent bloques tant qu'un reliquat explicite n'est pas redecoupe depuis cette spine deja validee.

---

## EPIC-00A — Front prioritaire post-challenge

**Vision** : Fermer d'abord le contrat canonique, la preuve d'un flux critique mono-host et le cockpit minimal expert avant d'ouvrir multi-PC, multi-host ou surfaces game plus riches.

**Assignation principale** : `@arch` + `@dev` + `@qa` + `@ux`

**Statut local** : Couvre localement sur la tranche runtime de reference; conserver cet epic comme matrice de preuve et de reliquats, pas comme front runtime encore ouvert.

**Sources opératoires** : [PAQUET-execution-front-prioritaire-post-challenge.md](./PAQUET-execution-front-prioritaire-post-challenge.md), [TICKETS-web-gaming.md](./TICKETS-web-gaming.md)

### STORY-00A-01 — Contrat canonique run/host/proof

**@arch + @dev + @qa** | **Points** : 13 | **Sprint** : 0

**Dépendances** : contrats runtime V1 existants, `GAME-TKT-001`, `GAME-TKT-003`, `GAME-TKT-004`, `GAME-TKT-037`, `GAME-TKT-047`, `GAME-TKT-048`, `GAME-TKT-049` engagés.

**Statut de preparation** : Verifiee localement sur la tranche runtime de reference.

**Critères d'acceptation story** :

- Le panier critique manipule des identités canoniques stables de bout en bout.
- Une mutation critique est refusée si provenance, policy ou vérification minimale manquent.
- Runtime, audit et verification pointent vers la même spine `run/host/proof`.

```yaml
TASK-128:
  titre: Geler les identités canoniques et les schémas du panier critique
  assigné: "@dev Amelia"
  collaboration: "@arch Winston review de contrat"
  prompt: |
    Couvrir GAME-TKT-052 avec:
    - identités canoniques `runId`, `taskId`, `workerId`, `hostId`, `traceId`, `requestId`, `idempotencyKey`
    - validation Zod stricte du panier critique
    - compatibilité additive avec les événements déjà exposés
    Tests: payloads valides/invalides, identités manquantes, identités incohérentes.

TASK-129:
  titre: Relier provenance, policy et vérification minimale aux mutations critiques
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn tests négatifs"
  prompt: |
    Étendre la spine runtime pour exiger, sur le panier critique:
    - provenance minimale
    - policy minimale
    - vérification minimale
    - refus explicites audités
    Tests: refus sur entrée incomplète, refus sur actor non autorisé, audit trail exploitable.

TASK-130:
  titre: Valider la reconstruction d'un run critique mono-host
  assigné: "@qa Quinn"
  prompt: |
    Construire les preuves de reconstruction de run pour GAME-TKT-052:
    - scénario nominal mono-host
    - alignement runtime/audit/verification
    - absence de corrélation heuristique fragile
    Tests: reconstruction complète depuis les traces critiques et lecture cohérente des identités.
```

### STORY-00A-02 — Flux critique mono-host prouvé

**@dev + @qa** | **Points** : 13 | **Sprint** : 0-1

**Dépendances** : STORY-00A-01 terminée, `GAME-TKT-005`, `GAME-TKT-008`, `GAME-TKT-010`, `GAME-TKT-038` engagés.

**Statut de preparation** : Verifiee localement sur la tranche runtime de reference.

**Critères d'acceptation story** :

- Le flux `preview -> validation -> commit borne` passe de bout en bout.
- Le scénario miroir incomplet ou non autorisé est refusé explicitement.
- La chaîne action -> décision -> vérification -> replay se relit sans synthèse manuelle fragile.

```yaml
TASK-131:
  titre: Borne du flux critique de référence
  assigné: "@arch Winston"
  collaboration: "@pm John validation fonctionnelle"
  prompt: |
    Formaliser le flux critique unique utilisé par GAME-TKT-053:
    - point d'entrée preview
    - validation attendue
    - commit borné
    - scénario miroir refusé
    Sortie: contrat de flux et critères de preuve minimaux.

TASK-132:
  titre: Implémenter replay, idempotence et refus explicites sur le flux critique
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn scénarios d'intégration"
  prompt: |
    Brancher GAME-TKT-053 dans GameState/runtime-source/verification views:
    - replay du flux critique
    - idempotence des mutations critiques
    - refus fail-closed du scénario miroir
    Tests: nominal, doublon, replay, refus non autorisé.

TASK-133:
  titre: Produire l'evidence pack borne par run et verdict
  assigné: "@qa Quinn"
  prompt: |
    Construire la preuve exploitable de GAME-TKT-053:
    - ticket -> run -> verdict
    - traces de replay
    - refus miroir
    - evidence refs consultables
    Tests: tous les artefacts de preuve sont retrouvables sans synthèse orale.
```

### STORY-00A-03 — Cockpit minimal expert

**@dev + @ux + @qa** | **Points** : 8 | **Sprint** : 1

**Dépendances** : STORY-00A-02 terminée, `GAME-TKT-011` et `GAME-TKT-014` engagés.

**Statut de preparation** : Verifiee localement sur la tranche runtime de reference.

**Critères d'acceptation story** :

- Une seule surface permet d'inspecter, expliquer, vérifier et rejouer le flux critique.
- La surface ne crée aucune logique métier parallèle.
- Le cockpit minimal suffit à répondre à `pourquoi accepté`, `pourquoi refusé`, `quel replay`.

```yaml
TASK-134:
  titre: Exposer inspection, preuve et replay dans les read models cockpit
  assigné: "@dev Amelia"
  collaboration: "@ux Sally cadrage surface experte"
  prompt: |
    Étendre board-view, observability-view et runtime-dashboard-view pour GAME-TKT-054:
    - inspection du run critique
    - lecture de la preuve et du replay
    - refus explicites visibles
    Tests: vues cohérentes, pas de seconde source de vérité.

TASK-135:
  titre: Designer et verrouiller la surface opérateur minimale
  assigné: "@ux Sally"
  collaboration: "@dev Amelia intégration"
  prompt: |
    Cadrer la surface minimale experte pour GAME-TKT-054:
    - ordre de lecture opérateur
    - zones inspection/preuve/replay
    - zéro room riche, zéro logique spatiale parallèle
    Sortie: contrat UI minimal utilisable par le runtime.

TASK-136:
  titre: Valider le walkthrough opérateur du flux critique
  assigné: "@qa Quinn"
  prompt: |
    Construire les preuves de GAME-TKT-054:
    - walkthrough opérateur borné
    - alignement inspection/preuve/replay
    - vérification qu'aucun transcript brut complet n'est nécessaire
    Tests: scénario acceptance piloté depuis le cockpit seul.
```

---

## EPIC-00 — Control plane multi-PC, cockpit live et observateur

**Vision** : Stabiliser la coordination multi-PC avant d'ouvrir davantage de surface game UI, avec un control plane logique unique, des noeuds visibles, des leases gouvernes, un cockpit expert et un observateur spatial sur les memes read models.

**Statut** : Couvert localement sur la tranche runtime multi-PC de reference; ne rouvrir qu'en cas de reliquat explicite de deploiement multi-machine ou d'exploitation etendue.

**Assignation principale** : `@arch` + `@dev` + `@qa` + `@ux`

**Prompt pour l'Architect (Winston) :**

```text
EPIC-00 ARCHITECTURE BRIEF
Tu es Winston, Architect expert en runtime distribue, eventing et surfaces operatoires.

Ton travail : fermer la V1 multi-PC du runtime grimoire-game sans creer de seconde source de verite.

Livrables attendus:
1. Contrat canonique des identifiants `projectId`, `runId`, `taskId`, `traceId`, `workerId`, `nodeId`, `leaseId`, `worktreeId`
2. Design du control plane logique V1
3. Design du registre de noeuds et du lease store TTL
4. Frontiere cockpit contre observateur contre command gateway
5. Mapping read model -> surface UI

Contraintes:
- Une seule source de verite par domaine
- Pas de browser -> shell/Git/machine direct
- Le cockpit et l'observateur lisent la meme causalite
- Toute mutation GUI doit etre authz, auditée et idempotente
```

### STORY-00-01 — Control plane logique et identifiants canoniques

**@arch + @dev** | **Points** : 8 | **Sprint** : 0-1

**Dependances** : `STORY-00A-03` terminee, contrats runtime V1 existants, `canonical-envelope-pilot` deja pose, `runtime-dashboard-session` en place.

**Statut de préparation** : Prête à lancer.

**Critères d'acceptation story** :

- Le runtime reconstruit un run multi-PC sans correlation heuristique fragile.
- Toutes les surfaces read-only manipulent les memes identifiants canoniques.
- Le registre projet devient la source de verite du projet actif.

```yaml
TASK-101:
  titre: Etendre les contrats runtime avec les identifiants multi-PC
  assigné: "@dev Amelia"
  collaboration: "@arch Winston review de contrat"
  prompt: |
    Etendre src/contracts/events.ts et src/contracts/schemas.ts avec:
    - projectId, nodeId, workerId, leaseId, worktreeId
    - envelopes de presence, ownership, claims et command audit
    - validation Zod stricte et additive
    Tests: success/failure cases sur ids manquants, ids incoherents et compatibilite ascendante.

TASK-102:
  titre: Creer le project registry V1
  assigné: "@dev Amelia"
  prompt: |
    Creer src/server/control-plane/project-registry.ts:
    - registre du projet actif
    - version de registre
    - resolution runId/source de verite
    - lecture read-only pour cockpit et observer
    Tests: reconstruction d'un run, changement de version, absence de projet actif.

TASK-103:
  titre: Etendre l'enveloppe canonique pilote
  assigné: "@dev Amelia"
  prompt: |
    Etendre src/state/canonical-envelope-pilot.ts pour projeter:
    - node heartbeat
    - lease claim/renew/expire
    - git ownership
    - command audit
    Garder l'enveloppe additive et compatible avec les payloads existants.
```

### STORY-00-02 — Node managers, heartbeats et leases TTL

**@dev + @qa** | **Points** : 13 | **Sprint** : 1

**Dependances** : STORY-00-01 terminee.

**Statut de préparation** : Prête à lancer une fois le contrat des identifiants gelé.

**Critères d'acceptation story** :

- Deux PCs rejoignent le meme projet sans etat fantome.
- Un noeud stale ou offline est visible et actionnable.
- Une perte de heartbeat ne cree pas de double mutation durable.

```yaml
TASK-104:
  titre: Node registry et projection de flotte
  assigné: "@dev Amelia"
  prompt: |
    Creer src/server/control-plane/node-registry.ts et src/state/node-fleet-view.ts:
    - identite de noeud
    - capacites
    - heartbeat
    - statuts live/stale/offline
    - projection lisible par cockpit
    Tests: double node join, stale, offline, refresh propre.

TASK-105:
  titre: Lease store TTL et reprise
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn scenarios de collision"
  prompt: |
    Creer src/server/control-plane/lease-store.ts et src/state/lease-view.ts:
    - claim
    - renew
    - expire
    - reclaim
    - journal d'audit
    Tests: timeout, reclaim, renew hors TTL, no double mutation durable.

TASK-106:
  titre: Generaliser la sante agent vers la sante noeud
  assigné: "@dev Amelia"
  prompt: |
    Etendre src/bridge/agent-connection-health.ts pour supporter la projection noeud ou worker
    sans casser les tests existants.
    Ajouter des tests ciblant fraicheur, age de heartbeat et statut stale/offline.
```

### STORY-00-03 — Ownership Git distribuee et Cockpit Live

**@dev + @qa + @ux** | **Points** : 13 | **Sprint** : 1-2

**Dependances** : STORY-00-02 terminee.

**Statut de préparation** : Prête à lancer dès que leases TTL et node registry sont stables.

**Critères d'acceptation story** :

- Une tache mutable expose branche, worktree et owner sans ambiguite.
- Le cockpit repond aux questions operatoires clefs sans transcript brut.
- Une mutation hors ownership actif est refusee et auditée.

```yaml
TASK-107:
  titre: Verrouiller ownership Git dans le runtime source
  assigné: "@dev Amelia"
  prompt: |
    Etendre src/bridge/runtime-source-fs.ts pour porter:
    - une tache -> une branche -> un owner -> un worktree
    - rejet des collisions d'ownership
    - audit des refus et succes
    Tests: collisions, branche absente, worktree absent, reclaim legitime.

TASK-108:
  titre: Construire le cockpit multi-PC
  assigné: "@dev Amelia"
  collaboration: "@ux Sally cadrage UI"
  prompt: |
    Etendre src/state/runtime-dashboard-view.ts et src/state/runtime-dashboard-ui-view.ts,
    puis creer src/state/runtime-cockpit-view.ts pour exposer:
    - header projet/run
    - barre flotte
    - lanes taches avec lease et ownership
    - rail d'attention
    - drawer preuves et timeline
    Tests: focus unique, cards coherentes, parite avec read models sources.

TASK-109:
  titre: Couvrir les scenarios operateur multi-PC
  assigné: "@qa Quinn"
  prompt: |
    Creer les tests d'integration runtime-cockpit-view:
    - perte de noeud
    - expiration de lease
    - collision d'ownership
    - blocage de verification
    Valider que chaque scenario est explicable depuis le cockpit seul.
```

### STORY-00-04 — Observateur spatial et command gateway borne

**@dev + @ux + @qa** | **Points** : 8 | **Sprint** : 2

**Dependances** : STORY-00-03 terminee.

**Statut de préparation** : Prête à lancer après stabilisation du cockpit.

**Critères d'acceptation story** :

- La scene spatiale montre les memes alertes, handoffs et focus que le cockpit.
- Aucune commande critique n'existe seulement dans la scene.
- Le gateway borne toutes les mutations GUI et bloque totalement spectator.

```yaml
TASK-110:
  titre: Creer runtime-observer-view a partir des memes read models
  assigné: "@dev Amelia"
  collaboration: "@ux Sally scenographie utile"
  prompt: |
    Creer src/state/runtime-observer-view.ts:
    - mapping spatial des noeuds, claims, handoffs et blocages
    - war room observateur
    - focus synchronisable avec le cockpit
    Tests: parite cockpit/observer, absence de logique metier parallele.

TASK-111:
  titre: Implementer le command gateway borne
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn authz et audit"
  prompt: |
    Creer src/server/control-plane/command-gateway.ts:
    - liste fermee de commandes GUI
    - authz par role
    - idempotency key obligatoire
    - audit des refus et succes
    - blocage total du spectateur sur les mutations
    Tests: autorisations, refus, spectator, audit trail.

TASK-112:
  titre: Valider le mode spectateur partageable
  assigné: "@qa Quinn"
  prompt: |
    Construire les preuves de partage spectateur:
    - token read-only distinct
    - aucune mutation possible
    - lecture stable des projections cockpit/observer
    - audit des tentatives refusees
```

---

## EPIC-01 — Infrastructure de base et moteur de jeu

**Vision** : Poser les fondations du moteur de jeu. Canvas 2D fonctionnel, serveur WebSocket, ECS minimal.

**Assignation principale** : `@arch` + `@dev`

**Prompt pour l'Architect (Winston) :**

```text
EPIC-01 ARCHITECTURE BRIEF
Tu es Winston, Architect expert en game development et TypeScript.

Ton travail : définir et valider l'architecture ECS (Entity Component System)
pour le moteur de jeu Canvas 2D du Grimoire Game Board.

Livrables attendus:
1. ADR-GAME-001: Canvas 2D vs WebGL (décision + justification)
2. ADR-GAME-002: ECS architecture
3. Schéma d'architecture du moteur (Mermaid)
4. Interface TypeScript publique du World, EntityManager, SystemScheduler
5. Performance budget par système (en ms budget/frame à 60fps)

Contraintes:
- TypeScript strict
- Zéro framework jeu external (Phaser, Pixi.js → custom)
- Target: Chrome/Firefox/Safari modernes
- 20 agents simultanés @ 60fps minimum
```

---

### STORY-01-01 — Setup projet et toolchain

**@dev** | **Points** : 3 | **Sprint** : 1

**Tâches :**

```yaml
TASK-001:
  titre: Initialiser le projet TypeScript/SvelteKit
  assigné: "@dev Amelia"
  prompt: |
    Initialise un projet SvelteKit 2.x avec:
    - TypeScript strict
    - Vite comme bundler
    - Vitest pour les tests
    - Playwright pour e2e
    - Prettier + ESLint
    - Structure de dossiers: src/core/, src/game/, src/bridge/, src/server/, src/ui/
    Crée le README avec les commandes de dev.
  acceptation:
    - npm run dev démarre sans erreur
    - npm test passe (au moins 1 test hello world)
    - Structure dossiers conforme au document technique

TASK-002:
  titre: Configurer le serveur Node.js avec WebSocket
  assigné: "@dev Amelia"
  prompt: |
    Crée le serveur backend avec:
    - Hono pour REST API (lightweight)
    - ws pour WebSocket server
    - Port configurable (défaut 8765)
    - Token auth basique (lecture depuis ~/.grimoire/game.token)
    - Event router avec types TypeScript stricts
    - Enveloppe évènementielle minimale versionnée pour les événements critiques (`eventType`, `eventVersion`, `source`, `actor`, `correlationId`)
    - Rate limiter 100 msg/sec
    Tests: unit sur le router, integration sur auth
  acceptation:
    - Connexion WS authentifiée fonctionne
    - Non-authentifié est rejeté
    - Les événements critiques partagent une enveloppe minimale stable côté WS/API
    - 100 msg/sec sans drop

TASK-003:
  titre: Pipeline CI/CD (GitHub Actions)
  assigné: "@dev Amelia / @qa Quinn"
  prompt: |
    Crée le workflow GitHub Actions:
    - Test unitaires (vitest)
    - Lint TypeScript
    - Build check
    - Test e2e Playwright (headless)
    - Coverage report (>80%)
  acceptation:
    - CI verte sur main
    - Badge coverage dans README
```

---

### STORY-01-02 — ECS Core

**@dev** | **Points** : 8 | **Sprint** : 1-2

**Dépendances** : STORY-01-01 terminée, ADR-GAME-002 validée, interfaces publiques relues par `@arch`.

**Statut de préparation** : Prête à lancer une fois les interfaces `World`, `EntityManager`, `ComponentStorage` et `SystemScheduler` gelées pour le sprint.

**Critères d'acceptation story** :

- Le coeur ECS couvre création, destruction, stockage, requêtes et scheduling sans état incohérent.
- Les budgets système et les cas limites critiques sont couverts par des tests automatisés lisibles.
- Les components de base sont validés, sérialisables et directement consommables par le renderer et les agents.

```yaml
TASK-004:
  titre: Implémenter EntityManager
  assigné: "@dev Amelia"
  prompt: |
    Implémente l'EntityManager ECS:
    - IDs uniques (UUIDv4 ou compteur)
    - create(): EntityId
    - destroy(id: EntityId): void
    - alive(id: EntityId): boolean
    - getAll(): EntityId[]
    Tests: 100% coverage, TDD (écrire les tests d'abord)
  collaboration: "@arch Winston review de l'interface"

TASK-005:
  titre: Implémenter ComponentStorage générique
  assigné: "@dev Amelia"
  prompt: |
    Implémente le ComponentStorage type-safe:
    - add<T>(entity, component: T): void
    - get<T>(entity): T | undefined
    - remove<T>(entity): void
    - query<T>(...types: ComponentType[]): EntityId[]
    - Storage dense (Map<ComponentType, Map<EntityId, T>>)
    Optimisation: itérer en cache-friendly order
    Tests: edge cases (entity détruite, composant dupliqué, query vide)

TASK-006:
  titre: Implémenter SystemScheduler
  assigné: "@dev Amelia"
  prompt: |
    Implémente le SystemScheduler:
    - register(system: System, priority: number): void
    - runAll(dt: number): void
    - enable(systemId): void / disable(systemId): void
    - Profile chaque system (time budget monitoring)
    Interface System: { update(world: World, dt: number): void }
    Tests: ordre d'exécution, disable/enable, performance budget alert

TASK-007:
  titre: Components de base
  assigné: "@dev Amelia"
  prompt: |
    Implémenter tous les components définis dans TECH-grimoire-game.md section 2.2:
    Position, Velocity, AgentState, Sprite, AgentMeta, 
    DialogBubble, PathTarget, AnimationState, Room
    Tous typés strictement avec Zod schemas pour validation runtime
    Tests: création, mutation, sérialisation/désérialisation
```

---

### STORY-01-03 — Game Loop et Renderer

**@dev** | **Points** : 8 | **Sprint** : 2

**Dépendances** : STORY-01-02 terminée, ADR-GAME-001 validée, format de tilemap et de manifest stabilisé.

**Statut de préparation** : Prête à lancer après arbitrage final sur les couches de rendu, la caméra et la cible de performance.

**Critères d'acceptation story** :

- La boucle update/render reste stable avec pause, reprise et delta maîtrisé.
- Un rendu multi-couches jouable fonctionne sur au moins une carte multi-room avec navigation fluide.
- Le loader de tilemap, le pathfinding et la caméra coopèrent sans casser la lisibilité ni la fluidité perçue.

```yaml
TASK-008:
  titre: Game Loop (requestAnimationFrame)
  assigné: "@dev Amelia"
  prompt: |
    Implémenter la game loop:
    - requestAnimationFrame loop
    - Delta time calculé et cappé à 16ms max
    - Séparation update/render
    - FPS counter (visible en debug mode)
    - Pause/Resume API
    Tests: delta time correct, pas de spiral of death

TASK-009:
  titre: Renderer Canvas 2D (layers)
  assigné: "@dev Amelia"
  collaboration: "@ux Sally (retour visuel)"
  prompt: |
    Implémenter le RenderSystem avec layers:
    Layer 0: Floor tiles (avec dirty-rect optimization)
    Layer 1: Walls (cached offscreen canvas)
    Layer 2: Furniture (cached offscreen canvas)
    Layer 3: Agents (dynamic, redrawn chaque frame)
    Layer 4: Particles (pooled, max 200)
    Layer 5: UI Overlay (health bars, bubbles)
    
    Camera: pan (drag) + zoom (scroll wheel, 0.5x à 3x)
    Viewport culling: ne rendre que les éléments visibles
    Éditeur de layout intégré: undo/redo 50 niveaux (Ctrl+Z/Ctrl+Y, Command pattern)
    Grille extensible jusqu'à 64×64 tiles (clic sur la bordure pour agrandir)
    Tests: test de performance (mock 20 agents @ 60fps dans jsdom)

TASK-010:
  titre: Tilemap loader (format Tiled JSON)
  assigné: "@dev Amelia"
  prompt: |
    Implémenter le loader de tilemaps:
    - Format Tiled JSON (.tmj) compatible
    - Layers: floor, walls, decoration, collision
    - Walkability map générée depuis la layer collision
    - Support des rooms multiples (switch de map)
    - Asset packs: scan du dossier assets/furniture/ pour charger les manifest.json
    - Format manifest: { id, name, frames, states: [{ name, sprite }], rotations, anchor }
    - Support de dossiers d'assets externes (Settings > Add Asset Directory)
    Tests: load/parse tilemap, walkability correcte, manifest parsing correct

TASK-011:
  titre: Pathfinding A* (Web Worker)
  assigné: "@dev Amelia"
  prompt: |
    Implémenter l'algorithme A* dans un Web Worker:
    - Grid 2D de tiles (walkable/blocked)
    - Heuristique Manhattan distance
    - Path cache (LRU, 100 paths max)
    - Async: postMessage request → postMessage result
    Tests: pathfinding correct (obstacles, pas de chemin, chemin optimal)
    Performance: path de 200 tiles en moins de 5ms
```

---

## EPIC-02 — Agents et personnages

**Vision** : Chaque agent BMAD devient un personnage animé visible et cliquable.

**Assignation principale** : `@dev` + `@ux` + `@arch`

**Prompt pour le Developer (Amelia) :**

```text
EPIC-02 DEV BRIEF
Tu es Amelia, Senior Developer.

Ton travail : implémenter le système de personnages agents.
Chaque agent BMAD devient un sprite animé avec state machine.

Priorité absolue : les animations DOIVENT être cohérentes avec l'action réelle de l'agent.
Source de vérité : les JSONL transcripts et les WS events de grimoire-kit.

Référence code : pixel-agents (https://github.com/pablodelucca/pixel-agents)
Analyse leur src/agentTracker.ts et leur stateMachine pour t'inspirer.
```

---

### STORY-02-01 — Sprite system et animations

**@dev + @ux** | **Points** : 13 | **Sprint** : 2-3

```yaml
TASK-012:
  titre: Sprite sheet loader et animation player
  assigné: "@dev Amelia"
  prompt: |
    Implémenter AnimationSystem:
    - Charger des sprite sheets (PNG + JSON manifest)
    - Jouer des clips d'animation (définies par frame range)
    - Blit correct (anti-aliasing OFF pour pixel art)
    - Direction-aware (4 dirs: N/S/E/W)
    - Transitions entre clips (immediate ou bridged)
    
TASK-013:
  titre: Créer les animations de base (programmatiques)
  assigné: "@dev Amelia / @ux Sally"
  collaboration: "@ux Sally: validation visuelle"
  prompt: |
    En attendant les assets finaux, créer les animations PROGRAMMATIQUES
    (pas de sprites externes), juste des formes colorées animées:
    - Un rond coloré par rôle (vert=dev, violet=QA, orange=PM, etc.)
    - Oscillation verticale pour idle_breathe
    - Rectangle qui s'étire pour sit_type
    - Point d'interrogation animé pour sit_think
    - Flash rouge pour react_error
    Ces placeholders seront remplacés par les vraies sprites
    
TASK-014:
  titre: Mapping tool→animation depuis JSONL
  assigné: "@dev Amelia"
  prompt: |
    Implémenter le TOOL_TO_ANIMATION mapping défini dans TECH-grimoire-game.md:
    - Sur chaque ToolCallStart event: changer animation de l'agent
    - Sur ToolCallEnd: retour idle ou next action
    - Cas spécial: memory → walk to library room
    - Cas spécial: runSubagent → spawn effect + sub-agent link
    Tests: chaque tool mappe à la bonne animation
```

---

### STORY-02-02 — Agent state machine et bridge

**@dev** | **Points** : 8 | **Sprint** : 3

```yaml
TASK-015:
  titre: Agent state machine (XState)
  assigné: "@dev Amelia"
  prompt: |
    Implémenter la state machine de chaque agent avec XState:
    States: IDLE, WALKING, WORKING, COMMUNICATING, IN_MEETING, PRESENTING, SLEEPING, PANIC, CONFUSED
    WORKING sub-states: TYPING, READING, THINKING, SEARCHING, EXECUTING, WAITING
    Transitions: via WS events du serveur
    Chaque transition déclenche une animation change
    Tests: toutes les transitions valides, rejeter transitions invalides

TASK-016:
  titre: Agent Bridge — JSONL watcher
  assigné: "@dev Amelia"
  prompt: |
    Adapter pour lire les JSONL transcripts de grimoire-kit:
    - Watch les fichiers _grimoire-runtime-output/**/*.jsonl
    - Parser les événements (même format que pixel-agents)
    - Mapper vers AgentState WS events
    - Reconnexion automatique si fichier rotaté
    Tests: parse correct de tous les types d'événements JSONL connus
    Reference: pixel-agents src/agentTracker.ts

TASK-017:
  titre: Panel d'information agent (click → details)
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design du panel"
  prompt: |
    Panel droit qui s'ouvre au clic sur un agent:
    - Nom, rôle, modèle, status
    - Tâche en cours avec lien vers carte Kanban
    - Workflow en cours avec position
    - Tokens restants (barre de progression)
    - Rate limit status
    - Mémoires actives (liste cliquable)
    - Actions: [Chat] [Config] [Pause] [Redirect]
    Animé: slide depuis la droite
    Svelte component + store
```

---

## EPIC-03 — Espaces et rooms

**Vision** : Chaque team a sa pièce, des couloirs les relient, la War Room héberge l'Orchestrateur.

**Assignation principale** : `@arch` + `@dev` + `@ux`

---

### STORY-03-01 — Multi-rooms et navigation

**Points** : 8 | **Sprint** : 3-4

```yaml
TASK-018:
  titre: Room manager et transitions
  assigné: "@dev Amelia"
  prompt: |
    Room system:
    - RoomManager: load/unload rooms
    - Doorways comme triggers de transition
    - Camera transition animée entre rooms (fade + pan)
    - Agents persistent entre les rooms (entité ECS permanente)
    - Mini-map globale montre toutes les rooms
    Tests: navigation correcte, agents bien transférés

TASK-019:
  titre: Créer les 8 pièces de base (tilemaps)
  assigné: "@ux Sally"
  collaboration: "@dev Amelia: implémentation"
  prompt: |
    Créer 8 tilemaps Tiled JSON pour:
    1. Team DEV openspace (bureaux, ecrans, plantes)
    2. Team QA openspace (tableau test, serveur de CI)
    3. Team PM boardroom (grande table, whiteboards)
    4. Salle de réunion (table ronde, écran central)
    5. Challenge Room (amphithéâtre, big screen, urne)
    6. War Room Orchestrateur (multiple screens, console centrale)
    7. Bibliothèque/Memory Room (étagères, orbes)
    8. Agent Factory (forge, établi, terrain test)
    
    Chaque map: 30×20 tiles minimum, avec zones walkable définies
    Style: pixel art cohérent avec DA (tons sombres, lumières chaudes)

TASK-020:
  titre: Décoration et ambiance par room
  assigné: "@ux Sally"
  prompt: |
    Pour chaque room, définir la déco spécifique:
    - Plantes d'intérieur (+/- selon type de room)
    - Posters et tableaux (code snippets, matrices, flow charts)
    - Lumières d'ambiance (lampes de bureau, plafonniers)
    - Objets de la spécialité (rack serveur pour DEV, crash board pour QA)
    - Coffee machine dans le couloir principal
    - Kanban board mural dans chaque openspace
    Objectif: chaque room a une identité immédiatement reconnaissable
```

---

## EPIC-04 — Kanban gamifié

**Vision** : Un Kanban mural in-world que les agents et l'utilisateur peuvent manipuler.

**Assignation principale** : `@dev` + `@pm`

---

### STORY-04-01 — Kanban board in-world

**Points** : 13 | **Sprint** : 4-5

```yaml
TASK-021:
  titre: TaskRepository et TaskService
  assigné: "@dev Amelia"
  collaboration: "@arch Winston: schéma DB"
  prompt: |
    Implémenter la couche data des tâches:
    - SQLite schema (cf. TECH-grimoire-game.md section 5.1)
    - SQLiteTaskRepository + InMemoryTaskRepository (tests)
    - TaskService avec business rules:
      * Une tâche ne peut avoir qu'un agent assigné
      * Transitions de status valides (backlog→todo→in_progress→review→done)
      * P0 tasks ne peuvent être dé-priorisées sans approbation
    Tests: CRUD, transitions, contraintes

TASK-022:
  titre: Rendu Kanban mural sur canvas
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design des cartes"
  prompt: |
    Afficher le Kanban in-world comme un grand whiteboard:
    - 5 colonnes (backlog/todo/in_progress/review/done)
    - Cards avec couleur par type (bug rouge, feature bleu, etc.)
    - Avatar agent assigné sur la carte
    - Drag & drop pour changer de colonne
    - Scroll si trop de cartes dans une colonne
    - Animation: agent qui "prend" une carte quand assigné
    Performance: jusqu'à 100 cartes sans lag

TASK-023:
  titre: Interactions Kanban (CRUD)
  assigné: "@dev Amelia"
  prompt: |
    Interactions utilisateur sur le Kanban:
    - Double-clic carte: modal détails (titre, desc, prompt, assignee, priorité)
    - Clic droit carte vide: créer nouvelle tâche
    - Drag carte entre colonnes
    - Tri manuel par priorité
    - Filtre par agent/type/priorité
    - Raccourcis clavier: N=new, E=edit, D=delete, Enter=validate

TASK-024:
  titre: Sync automatique tâches ↔ activité agent
  assigné: "@dev Amelia"
  prompt: |
    Auto-mise à jour:
    - Quand un agent commence une tâche → carte passe en IN_PROGRESS
    - Quand agent pose status done → carte passe en REVIEW
    - Quand agent reçoit une nouvelle tâche → carte créée automatiquement
    Ces rules viennent des events WS agents
    Tests: chaque règle de sync testée indépendamment
```

---

## EPIC-05 — Communication inter-agents

**Vision** : Les agents se parlent visuellement, un agent communicant navigue entre les rooms.

**Assignation principale** : `@dev` + `@arch`

---

### STORY-05-01 — Système de messages visuels

**Points** : 8 | **Sprint** : 5-6

```yaml
TASK-025:
  titre: Message bus visuel inter-agents
  assigné: "@dev Amelia"
  prompt: |
    Système de visualisation des messages:
    - Type: HANDOFF (parchemin volant), REQUEST (?bulle), BROADCAST (ondes)
    - Animation: objet qui se déplace de A vers B en arc
    - Timeline en bas: historique des messages
    - Clic sur message: détail complet
    Tests: tous les types de messages, cas edge (agent hors écran)

TASK-026:
  titre: Agent communicant inter-rooms
  assigné: "@dev Amelia"
  collaboration: "@arch Winston: pattern navigator"
  prompt: |
    Implémenter le CommunicationAgent:
    - Agent spécial avec capacité walk_between_rooms
    - Quand il doit transmettre un message inter-rooms:
      1. Se lève (animation)
      2. Walk vers la porte
      3. Transition vers room destination
      4. Walk vers l'agent cible
      5. Animation talk
      6. Return to own room
    Tests: navigation complète d'un bout à l'autre, cas de room non disponible

TASK-027:
  titre: Système de réunion inter-teams
  assigné: "@dev Amelia"
  prompt: |
    Déclencher une réunion:
    - Team Lead de room A demande réunion avec room B
    - Tous les agents impliqués marchent vers Meeting Room
    - Écran de réunion s'affiche avec agenda
    - Meeting notes écrites en temps réel (par tech-writer si présent)
    - Fin de réunion: agents retournent à leur room
    Tests: convocation, attendance, retour
```

---

## EPIC-06 — Orchestrateur et War Room

**Vision** : L'Orchestrateur est le dieu du système, visible dans sa War Room.

**Assignation principale** : `@dev` + `@ux` + `@arch`

---

### STORY-06-01 — War Room et capacités spéciales

**Points** : 13 | **Sprint** : 6-7

```yaml
TASK-028:
  titre: War Room - vue globale et contrôles
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design war room"
  prompt: |
    La War Room de l'Orchestrateur:
    - 3 grands écrans: global view | agents actifs | logs
    - Mini-maps de toutes les rooms (real-time)
    - Console centrale avec accès routing
    - Dispatch panel: assigner/rediriger agents
    - Status global: uptime, tasks, errors, performance
    Actions disponibles depuis la War Room:
      * Deploy new agent
      * Pause/resume agent
      * Force handoff
      * Broadcast message
      * Launch challenge
      * Memory inspect (read memory of any agent)

TASK-029:
  titre: Interface dialogue utilisateur ↔ Orchestrateur
  assigné: "@dev Amelia"
  prompt: |
    Interface "4ème mur":
    - Chat direct avec l'Orchestrateur (input box flottant)
    - L'Orchestrateur répond via bulle de dialogue étendue
    - Les demandes utilisateur sont "traduites" en prompt structuré
    - L'Orchestrateur dispatche vers les agents appropriés
    - Confirmation de dispatch visible en temps réel
    - Historique des interactions accessible
    Tests: send message → orchestrateur reçoit → dispatch visible

TASK-030:
  titre: Créateur d'agents depuis War Room
  assigné: "@dev Amelia"
  prompt: |
    Interface de création d'agent:
    - Formulaire RPG: nom, rôle, archetype, background, model, tools
    - Sélection des tools via drag-drop depuis inventaire
    - Preview live du prompt système généré
    - Choix de la room initiale
    - Animation de spawn: forge → création → apparition dans la room
    - Clone d'agent existant avec modifications
    Tests: créer agent minimal, clone, vérification dans la room
```

---

## EPIC-07 — Système de mémoire visualisé

**Vision** : Rendre la mémoire des agents visible et tangible. Les livres, orbes et fichiers dans la bibliothèque reflètent en temps réel ce que les agents savent et ont appris.

**Assignation principale** : `@dev` + `@ux`

**Prompt pour le Developer (Amelia) :**

```text
EPIC-07 MEMORY BRIEF
Tu es Amelia, Senior Developer.

Ton travail : implémenter la visualisation du système de mémoire des agents.
La bibliothèque est une pièce spéciale où la mémoire devient physique.

Référence architecture : claude-mem (https://github.com/thedotmack/claude-mem)
- Lifecycle hooks: SessionStart, PostToolUse, Stop
- DB Schema: sessions, observations, summaries
- Progressive disclosure: search → timeline → get_observations

Objectif UX : quand un agent lit ou écrit en mémoire, l'utilisateur DOIT le voir
se déplacer vers la bibliothèque et interagir avec un livre ou orbe.
```

**Points** : 8 | **Sprint** : 7-8

```yaml
TASK-031:
  titre: Memory visualization — bibliothèque
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design bibliothèque"
  prompt: |
    Visualiser la mémoire des agents:
    - Bibliothèque room: rayons, livres, orbes (pour vectors)
    - Mémoire short-term: fichiers flottants sur le bureau de l'agent
    - Mémoire long-term: livres dans les rayons (titre visible)
    - Lors d'un memory access: agent walk to library, ouvre un livre
    - Lors d'un memory write: livre se range dans le rayon
    - Qdrant/Chroma vectors: orbes lumineux dans une zone dédiée
    - Clic sur livre: contenu de la mémoire affiché (3 couches: index compact → timeline → détail)
    
    Référence architecture: claude-mem (https://github.com/thedotmack/claude-mem)
    - Progressive disclosure: search → timeline → get_observations
    - DB Schema: sessions, observations, summaries (inspire notre ClaudeMemAdapter)
    - Web Viewer localhost:37777 → peut être intégré comme source de données

TASK-032:
  titre: Memory sync depuis _grimoire-runtime/_memory/ et claude-mem
  assigné: "@dev Amelia"
  prompt: |
    Double source de mémoire à synchroniser:
    
    Source 1: File watcher sur _grimoire-runtime/_memory/
    - Détecter les créations/modifications de fichiers mémoire
    - Mapper vers les mémoires agents (agent_id depuis nom fichier)
    - Déclencher l'animation de memory write
    - Indexer les contenus pour search in UI
    
    Source 2: ClaudeMemAdapter (si claude-mem installé)
    - Lire le DB SQLite de claude-mem (localhost:37777 ou fichier direct)
    - Hook PostToolUse → animation memory write (livre qui se range)
    - Hook SessionStart → animation memory read (agent qui ouvre un livre)
    - MCP search → 3 couches progressive disclosure dans le panel Library
    
    Tests: creation fichier → agent animé → livre dans bibliothèque
    Tests: claude-mem DB lu → livres visibles dans bibliothèque
```

---

## EPIC-08 — Workflow visualisation

**Points** : 8 | **Sprint** : 8

```yaml
TASK-033:
  titre: Workflow overlay (click-to-inspect)
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design overlay"
  prompt: |
    Overlay de workflow au clic sur agent:
    - Charger le workflow YAML associé    
    Format workflow YAML attendu (source: _grimoire-runtime/bmm/workflows/):
    ```yaml
    id: string           # identifiant unique du workflow
    name: string         # nom lisible
    steps:
      - id: string       # identifiant de l’étape
        agent: string    # agent assigné (à crôiser avec agent_id DB)
        description: string
        depends_on: [string]  # ids des étapes précédentes
    ```
    Ce format est lu depuis workflow_runs.workflow_id (référence YAML) pour reconstruire le DAG    - Afficher le DAG du workflow (nodes + edges)
    - Mettre en évidence l'étape courante
    - Historique des agents qui ont contribué (avec timestamps)
    - Remonter la chaîne des décisions prises
    - Vue "full workflow" avec tous les agents sur le chemin
    Tests: rendu correct, navigation dans l'historique

TASK-034:
  titre: Workflow path visualization in-world
  assigné: "@dev Amelia"
  prompt: |
    Sur la carte, afficher les chemins de workflow actifs:
    - Lignes colorées entre agents qui collaborent sur un workflow
    - Animation: particules qui se déplacent sur la ligne (direction du flow)
    - Épaisseur de ligne = intensité du flow
    - Toggle on/off depuis HUD
    Tests: rendu correct pour 5 workflows simultanés
```

---

## EPIC-09 — Console de debug gamifiée

**Points** : 5 | **Sprint** : 8-9

```yaml
TASK-035:
  titre: Debug console in-world
  assigné: "@dev Amelia"
  prompt: |
    Console de debug in-world:
    - Objets 3D (terminaux, grands écrans) dans la War Room
    - Filtres: agent, type (tool/message/error/warning), level
    - Highlighting syntaxique pour JSON/code
    - Erreur → animation sur l'agent (point d'exclamation rouge)
    - HUP warning → alert orange sur l'agent concerné
    - Export JSON du log
    Tests: filtering correct, log de 1000 events sans lag

TASK-049:
  titre: Panel de diagnostics connexion JSONL
  assigné: "@dev Amelia"
  prompt: |
    Panneau "Connection Diagnostics" par agent (inspiré du Debug View de pixel-agents):
    - Accessible via icône engrenage dans l'AgentPanel (clic sur un agent)
    - Affiche par agent: statut JSONL (Found / Not found), lignes parsées, timestamp
      de la dernière donnée reçue, chemin absolu du fichier JSONL
    - Indicateur visuel: Live (vert) / Stale >5s (jaune) / Disconnected (rouge)
    - Bouton [Resync] pour forcer un re-scan du fichier JSONL
    - Bouton [Copy path] pour copier le chemin dans le presse-papiers
    - Données exposées depuis AgentConnectionHealth.ts dans bridge/
    Tests: JSONL présent → indicateur Live, JSONL absent → Not found, Resync force reload

TASK-051:
  titre: Variantes de Challenge — Investigation + DX Review + Auto-Challenge
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn: design des prompts; @ux Sally: animations nouvelles variantes"
  prompt: |
    Implémenter les 3 variantes de challenge (cf. WORKFLOW-challenge.md §12):
    
    1. Investigation Challenge
       - Déclencheur: bug P0 signalé ou régression détectée
       - Remplacement de la phase Présentation par une phase Trace de données (30 min)
       - Reviewer unique (Debugger) avec animation loupe + timeline data flow
       - Pas de vote: résultat = root cause identifiée ou escalade
       - Post-mortem auto vers _grimoire-runtime/_memory/failure-museum.md
    
    2. DX Review Challenge
       - Déclencheur: livrable API / CLI / onboarding
       - Reviewer DX supplémentaire avec DX_REVIEW_PROMPT (8 dimensions Addy Osmani)
       - Vote bloqué si score < 60/80
    
    3. Auto-Challenge (mode séquentiel)
       - Déclencheur: sprint final, release, ou demand orchestrateur
       - Pipeline: ACCEPTANCE → ADVERSARIAL → EDGE_CASE → DX (conditionnel) → SECURITY
       - Sélection automatique des reviewers pertinents
    
    Ajouter un sélecteur de type de challenge dans le panneau de convocation (Phase 1)
    Tests: chaque variante déclenchée correctement, pipeline Auto-Challenge complet

TASK-052:
  titre: Retro Room — Bilan de sprint gamifié
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: animations + layout bilan; @tw Paige: format snapshot JSON"
  prompt: |
    Implémenter la Retro Room hebdomadaire (cf. GDD §5.3, DA §4.3, CdC F20):

    1. RetroRoom.ts (game/rooms/)
       - Pièce accessible depuis la minimap (icône 📊)
       - Grand écran mural: tweetable summary (commits, LOC net, test ratio, streak)
       - Tableau de classement par agent (commits, tâches terminées, XP gagné)
       - Spotlight "Ship of the Sprint": tâche la plus impactante, badge 🏆
       - Flamme dorée animée (streak_celebrate) si streak global ≥ 7j consécutifs

    2. RetroMetricsCollector.ts (server/services/)
       - Lit le log git (git log --format, --shortstat) sur les 7 derniers jours
       - Agrège par agent (auteur commit = agent assigné dans la config)
       - Calcule: commits, +LOC/-LOC, test ratio, fix ratio, session count, streak
       - Émet un événement WS RETRO_UPDATE (payload: tweetable + metrics + authors)

    3. LearningsAdapter.ts (bridge/)
       - Lit ~/.gstack/projects/${SLUG}/learnings.jsonl (confidence, insight, files, source)
       - Filtre les 3 learnings les plus récents avec confidence ≥ 7
       - Affichage dans la Library Room: icône livre + clé courte + barre confidence (0-10)

    4. Snapshot JSON (.context/retros/AAAA-MM-JJ-N.json)
       - Sauvegarde auto après chaque session Retro Room
       - Format compatible gstack /retro: champs tweetable, metrics, authors
       - Comparaison semaine N vs N-1 (deltas: test ratio, LOC/sprint, streak)

    5. RetroRoom.svelte (ui/components/)
       - Affichage du tweetable summary + classement agents + spotlight
       - Animations: retro_present (orchestrateur), streak_celebrate, react_success/react_confused

    Tests: RETRO_UPDATE déclenche l'animation, snapshot sauvegardé et lisible,
           classement correct vs git log, LearningsAdapter parse bien le JSONL

TASK-053:
  titre: Worktree Lab + Merge Celebration
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: animations merge + room tinting; @qa Quinn: test worktree lifecycle"
  prompt: |
    Implémenter la gestion visuelle des branches git (cf. GDD §5.4, CdC F22):

    1. WorktreeRoom.ts (game/rooms/)
       - Room temporaire générée pour chaque branche active (git worktree list)
       - Tinting vert pâle (feature) ou rouge pâle (hotfix) selon le préfixe de branche
       - Compteur de commits + delta LOC affiché sur l’entrée
       - Écran mural avec boutons [Merge] [PR] [Discard] [Keep]

    2. GitWorktreeService.ts (server/services/)
       - Poll `git worktree list --porcelain` toutes les 10s
       - Émet WS BRANCH_CREATED / BRANCH_MERGED / BRANCH_DELETED
       - Événement BRANCH_MERGED déclenche animation `merge_celebrate` dans War Room

    3. merge_celebrate animation (DA §5.1)
       - 4 frames, 4fps, non-loopé
       - Agents rassemblés autour de l’écran War Room, confetti, high-five, flamme dorée

    4. sub_agent_spawn animation (DA §5.1)
       - 4 frames déclenchées au Task tool call
       - Mini-sprite enfant à scale 0.7×, cordon électrique persistant parent→enfant

    Tests: BRANCH_CREATED crée la WorktreeRoom, BRANCH_MERGED déclenche merge_celebrate,
           boutons de clôture appelent les bons git commands

TASK-054:
  titre: Plugin Power Cards + Deep Inspection Panel
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design halo + card sprite; @tw Paige: tooltip format"
  prompt: |
    Implémenter les Plugin Power Cards et le panneau Deep Inspection (cf. GDD §5.5, CdC F21/F23):

    1. PluginService.ts (server/services/)
       - CRUD activation des plugins (frontend-design, code-review, security-guidance)
       - Persistance dans la config grimoire (champ `active_plugins: []`)
       - Chaque plugin porte provenance, trust status, policy minimale et classe de risque
       - Refuse toute activation si metadata ou policy minimale manquante
       - Émet WS PLUGIN_ACTIVATED / PLUGIN_DEACTIVATED avec `{ pluginId, agentId, correlationId, trustStatus }`

    2. PluginPowerCard.svelte (ui/components/)
       - Carte physique pixelisable (sprite 16×24px) avec icône + nom court + install count
       - Badge provenance/trust/risk visible avant confirmation
       - Click → confirmation modale → WS PLUGIN_ACTIVATED
       - Agent concerné : halo de couleur (bleu/vert/rouge selon plugin) + icône overlay sur sprite

    3. Deep Inspection Panel (panneau latéral, clic sur sprite)
       - Lu depuis AgentConnectionHealth.ts + JSONL transcript
       - Champs : modèle, branche, system prompt (lecture seule), tokens/contexte, outil actif,
         historique de session (compté: outils, fichiers, tests)
       - Actions : Pause (WS AGENT_PAUSE), Chat (WS USER_MESSAGE_DIRECT), Redirect (nouvelle tâche),
         Restart (WS AGENT_RESTART)

    4. Desks as Directories (glisser agent vers bureau)
       - Drag-and-drop agent sur bureau → `AgentService.setCwd(agentId, path)`
       - Icône 📁 flottante au-dessus du bureau assigné (label = dossier court)
       - `walk_to_desk` se déclenche automatiquement si cwd change

        Tests: activation plugin persiste au rechargement, activation sans metadata refusée,
          Deep Inspection affiche les bons données JSONL, drag-to-desk change bien le cwd et déclenche l’animation
```

### STORY-09-02 — Gouvernance d'exécution et garde-fous

**@dev** | **Points** : 13 | **Sprint** : 9-11

**Dépendances** : TASK-035, TASK-049 et TASK-051 livrées, flux Kanban et branches stabilisés, auth spectateur cadrée.

**Statut de préparation** : À lancer après stabilisation du socle de debug et des événements WebSocket critiques.

**Critères d'acceptation story** :

- Les flux Investigation, Review et Security bloquent explicitement lorsqu'une preuve, une spec ou un garde-fou manque.
- Les surfaces War Room associées sont reliées aux cartes Kanban, aux branches et aux événements serveur.
- Les surfaces de configuration ou d'activation rendent visibles provenance, trust status et policy minimale avant mutation.
- Les transitions critiques conservent une chaîne de vérification et une corrélation consultables après replay.
- Les conflits, findings critiques et gaps de revue remontent comme signaux d'exécution visibles et actionnables.

```yaml

TASK-055:
  titre: Investigation Lab + Verification Gate
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn: Evidence Gate tests; @ux Sally: Investigation Lab mini-board UI"
  prompt: |
    Implémenter l'Investigation Lab (4 phases debug) et la Verification Gate (cf. GDD §3.11, CdC F24/F25):

    1. SystematicDebugService.ts (server/services/)
       - Modèle d'état : ROOT_CAUSE | PATTERN | HYPOTHESIS | IMPLEMENTATION
       - Émet WS DEBUG_PHASE_CHANGED avec phase courante
       - Bloque FIX_PROPOSED tant que ROOT_CAUSE_IDENTIFIED absent (WS warning)
       - Compteur FIX_FAILED : à 3 → émet ARCHITECTURE_REVIEW_REQUIRED + crée TASK Kanban

    2. VerificationGateService.ts (server/services/)
       - Evidence Gate 5 étapes : IDENTIFY → RUN → READ → VERIFY → CLAIM
       - Émet WS VERIFICATION_GATE { result: PASS | FAIL, evidence: string, traceId, actionId, verificationRef }
       - Écrit audit log structuré dans .context/verification-log.jsonl (append)
       - Conserve la chaîne minimale action → contrôles → verdict → evidenceRef pour les transitions critiques

    3. Investigation Lab mini-board (UI — panneau latéral en DEBUGGING state)
       - 4 colonnes visuelles Ph1–Ph4 avec progression
       - Badge phase visible sur sprite agent
       - Badge verification status et traceId visible sur la carte ou le panneau de debug
       - Poster Iron Law affiché dans la War Room

    Tests: FIX_PROPOSED bloqué sans ROOT_CAUSE, FIX_FAILED ×3 → ticket arch, audit log écrit
          correctement, Evidence Gate bloque DONE si VERIFY non passé, traceId et verificationRef persistés au replay

---

TASK-056:
  titre: Parallel Dispatcher — Isolation de contexte et Conflict Detection
  assigné: "@dev Amelia"
  collaboration: "@architect Winston: domain decomposition rules; @qa Quinn: conflict detection tests"
  prompt: |
    Implémenter le Parallel Dispatcher et le Parallel Sprint Panel (cf. GDD §3.12, CdC F26):

    1. ParallelDispatcher.ts (game/agents/)
       - Décompose la requête en domaines indépendants (1 agent / domaine)
       - Génère des prompts auto-suffisants : NO context inheritance depuis l'orchestrateur
       - Badge Context: ✅ si prompt isolé, ❌ si dépendance détectée
       - Tether cords persistent jusqu'à retour de tous les sous-agents
       - Conflict check avant fermeture : diff croisé des branches, WS CONFLICT_DETECTED si besoin

    2. Parallel Sprint Panel (War Room UI)
       - Vue ⚡ Sprint Parallèle : tableau agents actifs + domaines + status
       - Tether cords visuels (ligne colorée unique par agent)
       - Boutons : [🔀 Conflict Check] [📋 Integration Review] [✅ Close All]

    Tests: prompts générés sans contexte hérité, tethers fermés uniquement après retour de tous,
           conflict detection sur fichier modifié par 2 agents simultanément

---

TASK-057:
  titre: Code Review Room + Cycle de revue à deux étapes
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn: tests CodeReviewService; @ux Sally: Code Review Room UI 2-stages"
  prompt: |
    Implémenter la Code Review Room et le cycle de revue à deux étapes (cf. GDD §3.13, CdC F27/F28, WORKFLOW §12.7/§12.8):

    1. CodeReviewService.ts (server/services/)
       - Dispatch spec-reviewer subagent avec contexte isolé (BASE_SHA, HEAD_SHA, DESCRIPTION)
       - Dispatch quality-reviewer subagent après validation spec
       - Gestion sévérité : Critical (bloque WS CARD_BLOCKED) / Important / Minor
       - YAGNI Check : grep codebase pour endpoints non appelés, WS YAGNI_DETECTED
       - Stage 1 obligatoire avant Stage 2 (ordre invariant)

    2. SubagentDevelopment.ts (game/agents/)
       - Fresh subagent spawn par tâche (contexte auto-suffisant, jamais héritage)
       - Gestion des statuts : DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
       - DONE_WITH_CONCERNS : lire les concerns avant de procéder
       - BLOCKED : pas de retry sans changement (méthode ou decomposition)
       - Sélection modèle selon complexité (1-2 fichiers spec claire → rapide, multi-fichiers → standard)

    3. Branch Finisher flow (game/agents/ ou game/challenge/)
       - Vérification tests avant présentation des options
       - 4 options (merge/PR/keep/discard), confirmation textuelle pour discard
       - Nettoyage worktree pour options 1 et 4 seulement
       - Animation branch_finish déclenchée par WS BRANCH_FINISH_OPTIONS

    Tests: Stage 1 bloque Stage 2 si SPEC_GAPS_FOUND, Critical bloque progression carte,
           YAGNI détecté sur endpoint non appelé, discard sans saisie annulé

---

TASK-058:
  titre: Security Audit Room (CSO in-game) + /cso et /autoplan
  assigné: "@dev Amelia"
  collaboration: "@architect Winston: modèle STRIDE; @qa Quinn: exploit scenario validation"
  prompt: |
    Implémenter la Security Audit Room (cf. GDD §3.14, CdC F29/F30) :

    1. SecurityAuditService.ts (server/services/)
       - Audit OWASP Top 10 + OWASP Agentic Skills Top 10 + STRIDE threat model
       - Confidence gate : aucun finding publié sous 8/10
       - Zero-noise : 17 exclusions de faux positifs codées (localhost HTTPS, localStorage non-sensible...)
       - Chaque finding : sévérité (CRITICAL/HIGH/MEDIUM/INFO) + exploit scenario concret
       - Chaque finding surface expose provenance/policy/trust gap si applicable
       - WS SECURITY_FINDING { severity, owasp_category, agentic_skill_category, stride_category, exploit, confidence, surfaceId }
       - Céer carte Kanban [sécu] automatiquement par finding
       - CRITICAL → WS SHIP_BLOCKED (bloque /ship jusqu'à merge de la carte de correction)

    2. Security Audit Room UI
       - Grille OWASP (10 cases ✅/⚠️/❌) + grille Agentic Skills + grille STRIDE (6 cases)
       - Panel détail finding : titre, catégorie, confiance, exploit scenario, lien carte Kanban
       - Animation cso_audit (Security Officer scan + affichage progressif des résultats)
       - Lancer depuis War Room bouton ou commande /cso

    Tests: finding sous seuil 8/10 non publié, CRITICAL bloque /ship,
          exploit scenario présent pour chaque finding publié, surface sans provenance/policy signalée, carte Kanban créée
  ```

---

## EPIC-10 — Interface de configuration gamifiée

**Points** : 13 | **Sprint** : 9-10

Statut runtime local verifie au 2026-04-11 : la tranche bornee rattachee a `GAME-TKT-030` est couverte et validee dans `grimoire-kit/apps/grimoire-game`. `TASK-036` reste donc un support de recadrage S9 pour un reliquat UI, UX ou produit explicite, et non un manque runtime encore ouvert dans le package courant.

```yaml
TASK-036:
  titre: Skill tree pour MCP et skills
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design skill tree"
  prompt: |
    Interface de config style RPG skill tree:
    - Nodes = MCP servers / skills availables
    - Edges = dépendances
    - Nœud activé = lumineux, désactivé = grisé
    - Clic sur nœud: panel config (paramètres, auth, test)
    - Chaque nœud affiche provenance, trust status, niveau de risque et policy minimale
    - Preview d'activation montre le scope de mutation et les prérequis de policy
    - Activation/désactivation avec confirmation
    - Sync avec la config grimoire-kit réelle
    - Refus d'activation si metadata minimale absente
    Tests: affichage correct, activation persiste, reload config, activation non qualifiée refusée

TASK-037:
  titre: Configuration prompts in-line
  assigné: "@dev Amelia"
  prompt: |
    Éditeur de prompt in-game:
    - Clic sur agent → "Edit prompt" → modal éditeur
    - Éditeur avec syntax highlighting (markdown + variables {})
    - Preview du prompt enrichi avec contexte
    - Templates disponibles (bibliothèque de prompts)
    - Save persiste dans la config grimoire
    Tests: edit → save → réchargement vérifié

TASK-038:
  titre: Configuration hooks visuels
  assigné: "@dev Amelia"
  prompt: |
    Visualiser les hooks comme déclencheurs in-world:
    - Chaque hook = un capteur physique dans la room (laser, plaque, bouton)
    - Animation quand un hook se déclenche (flash, animation capteur)
    - Click → voir le code du hook, activer/désactiver
    - Événements hook dans le log
    Tests: activation hook → animation → log entry
```

---

## EPIC-11 — Cadre transverse de tests et qualité

**Assignation principale** : `@qa` + `@tea`

**Nature** : capacité transverse / Definition of Done

**Points** : 13 | **Cadence** : transverse

**Règle de pilotage** : ces items durcissent chaque sprint et ne constituent pas un lot terminal autonome.

```yaml
TASK-039:
  titre: Test architecture et fixtures
  assigné: "@tea Murat"
  prompt: |
    Conception de la stratégie de tests complète:
    1. Fixtures partagées pour les tests (agents mock, tilemaps mock)
    2. Factories pour créer des entités ECS en tests
    3. Mock du serveur WS pour tests UI
    4. Mock du file system pour tests bridge
    5. Performance benchmarks automatisés
    Créer le ATDD-strategy.md dans _grimoire-runtime-output/planning-artifacts/grimoire-game/

TASK-040:
  titre: Tests d'intégration complets
  assigné: "@qa Quinn"
  prompt: |
    Tests d'intégration pour les flux critiques:
    - Flux complet: agent créé → tâche assignée → travaillée → challenge → done
    - Flux communication: message envoyé → visualisé → loggué
    - Flux workflow: workflow lancé → étapes visibles → terminé
    - Migration DB: v1 → v2
    Coverage: 85%+ sur les services

TASK-041:
  titre: Tests e2e Playwright
  assigné: "@qa Quinn"
  prompt: |
    Tests e2e pour les interactions UI:
    - Démarrer le serveur + ouvrir le browser
    - Cliquer sur un agent → panel s'ouvre avec données correctes
    - Créer une tâche Kanban → visible sur le board
    - Lancer une challenge session → étapes se déroulent
    - Configurer un MCP → check que config sauvegardée
    Runs en CI headless
```

---

## EPIC-12 — Intégration grimoire-kit et déploiement

**Points** : 5 | **Sprint** : 10-11

```yaml
TASK-042:
  titre: Intégration grimoire.sh setup
  assigné: "@dev Amelia"
  collaboration: "@arch Winston: validation"
  prompt: |
    Intégrer dans grimoire.sh:
    - Nouveau command: grimoire game start / stop / status
    - Installation automatique lors du setup
    - Lecture config _grimoire-runtime/bmm/config.yaml
    - Import automatique des agents BMAD existants
    - Documentation mise à jour dans grimoire-kit README
    Tests: grimoire.sh setup → board disponible sur localhost

TASK-043:
  titre: Documentation complète
  assigné: "@tw Paige"
  prompt: |
    Rédiger la documentation complète:
    - README avec screenshots
    - Guide d'installation
    - Guide utilisateur (interface, actions disponibles)
    - Guide développeur (architecture, comment ajouter une room)
    - API reference (WS events, REST endpoints)
    - Changelog initial
    Respecter markdown-standards.instructions.md

TASK-044:
  titre: UI Components via gstack design-html + Anthropic Frontend Design
  assigné: "@ux Sally"
  collaboration: "@dev Amelia: intégration Svelte"
  prompt: |
    Générer les composants UI du board en utilisant les outils de design:
    
    Étape 1 (gstack /design-consultation):
    - Définir le design system: Typography, spacing, couleurs (déjà en DA)
    - Proposer 3 directions visuelles pour les panels et modals
    - Générer DESIGN.md
    
    Étape 2 (Anthropic Frontend Design plugin):
    - Partir du DESIGN.md généré
    - Générer des mockups HTML pour: Agent Panel, Kanban Card, Challenge Modal, Memory Browser
    
    Étape 3 (gstack /design-html):
    - Transformer les mockups en composants Svelte production
    - Détection automatique du framework (Svelte)
    - S'assurer que le texte reflow correctement (pas de hauteurs fixées)
    
    Étape 4 (gstack /cso):
    - Audit OWASP Top 10 + OWASP Agentic Skills Top 10 + STRIDE sur tous les composants qui affichent du contenu agent
    - XSS prevention sur le display des bulles de dialogue
    Tests: visuels corrects dans les 3 résolutions cibles

TASK-050:
  titre: Mode spectateur read-only
  assigné: "@dev Amelia"
  collaboration: "@arch Winston: spéc token spectateur"
  prompt: |
    Mode spectateur pour observateurs externes (F19):
    - Génération d'un token spectateur (read-only) depuis Settings > Share
    - URL copiable en 1 clic: http://localhost:8765?mode=spectator&token=<token>
    - Token spectateur: droits lecture seule (agents, tâches, Kanban, timeline)
    - Blocage côté serveur de toutes les mutations pour les tokens spectateurs (403)
    - Les projections read-only réutilisent l'enveloppe critique minimale du runtime (`eventType`, `eventVersion`, `source`, `correlationId`)
    - Bannière "Mode spectateur — vue lecture seule" affichée en bas du canvas
    - CSS pointer-events: none sur tous les éléments actionnables en mode spectateur
    Tests: token spectateur → toute mutation bloquée (403), lecture OK, bannière visible,
           projection read-only stable après reconnexion
```

---

## EPIC-13 — Son, XP et Onboarding

**Vision** : Les features de qualité de vie qui rendent l'expérience complète et polished.

**Assignation principale** : `@dev` + `@ux`

```yaml
TASK-045:
  titre: Système sonore (SFX + musique d'ambiance)
  assigné: "@dev Amelia"
  prompt: |
    Implémenter le système audio complet (cf. GDD section 6 + DA section 7.2):
    - Web Audio API pour SFX (10 événements: spawn, done, error, meeting, challenge, etc.)
    - Musique d'ambiance lo-fi par room (loop, crossfade animé à la transition)
    - Contrôle volume global (slider dans HUD, mémorisé en localStorage)
    - Toggle mute individuel par catégorie (SFX / Musique)
    - Lazy-load des assets audio (pas de blocage au démarrage)
    Tests: chaque événement déclenche son SFX, mute persiste en localStorage

TASK-046:
  titre: Système XP et achievements gamifiés
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design badges achievements"
  prompt: |
    Implémenter le système de progression (cf. GDD section 5.1):
    - XP attribué automatiquement selon les actions agents (table GDD: done=+100, challenge=+250, etc.)
    - Barre d'XP animée sous le nom de l'agent (progression visible)
    - 5 achievements initiaux (First Deploy, On Fire, Team Player, Bug Hunter, Memory Master)
    - Notification d'achievement: badge qui slide depuis top-right (DA spec) → 2s visible
    - Persistance en SQLite (table agent_xp + table achievements_unlocked)
    Tests: chaque action XP testée, achievement unlock correct, badge affiché

TASK-047:
  titre: Tutoriel d'onboarding (premier démarrage)
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design des overlays de tutoriel"
  prompt: |
    Implémenter le tutoriel interactif 5 étapes (cf. GDD section 7.1):
    1. Clic sur un agent → panel d'info s'ouvre
    2. Créer une tâche sur le Kanban (clic droit)
    3. Assigner la tâche à un agent (drag & drop)
    4. Observer l'agent travailler (animation + bubble)
    5. Lancer une mini-challenge session
    - [Skip] disponible à tout moment
    - Overlay avec pointer pixel art vers l'élément ciblé
    - Non-bloquant: l'utilisateur peut interagir librement
    - Flag "tutorial_done" en localStorage (ne se relance pas)
    Tests: 5 étapes enchaînées, skip fonctionnel, pas de relance au 2ème démarrage

TASK-048:
  titre: Observatory Panel — intégration iframe sandbox
  assigné: "@dev Amelia"
  collaboration: "@ux Sally: design du panel"
  prompt: |
    Implémenter le bouton [📡 Obs] du header (cf. GDD 4.1, ADR-GAME-005):
    - Bouton dans le nav header: [📡 Obs] qui toggle un side-panel droit
    - Side-panel contient un <iframe sandbox="allow-scripts allow-same-origin">
      pointant vers le fichier local _grimoire-runtime-output/observatory.html
    - Gestion gracieuse si le fichier n'existe pas (message "Observatory non disponible")
    - Resize handle sur le panel (150px → 600px largeur)
    - Le panel ne bloque pas le canvas (overlay flottant ou resize du layout)
    - ObservatoryPanel.svelte pour l'encapsulation SvelteKit
    Tests: toggle fonctionne, iframe charge si fichier présent, fallback affiché si absent
```

---

## EPIC-14 — Gouvernance transverse et pilotage produit

**Vision** : Convertir les axes transverses `AX-01` à `AX-08` en capacités réellement exécutables, avec preuves, gates et artifacts de décision utilisables dans le board.

**Assignation principale** : `@qa` + `@tea` + `@arch` + `@pm`

### STORY-14-01 — Drift prompts, reprise incident et qualité mémoire

**@qa + @tea** | **Points** : 13 | **Cadence** : transverse

**Dépendances** : `GAME-TKT-001`, `GAME-TKT-003`, `GAME-TKT-010`, vues `audit`, `session`, `verification` stabilisées.

**Statut de préparation** : Prête à lancer.

**Critères d'acceptation story** :

- Une évolution de prompt ou de policy ne passe pas sans mesure de drift.
- Un incident critique dispose d'un runbook, d'un exercice et d'une preuve de recovery.
- Une référence mémoire obsolète est détectée et peut bloquer une transition critique.

```yaml
TASK-113:
  titre: Baseline prompts/policies + suite canari de drift
  assigné: "@qa Quinn"
  collaboration: "@pm John scenarios de reference"
  prompt: |
    Mettre en place la baseline des prompts et policies critiques pour GAME-TKT-021:
    - registre versionne des prompts/policies
    - scenarios canari rejouables
    - rapport de drift de verdict
    - gate de blocage au-dessus du seuil
    Tests: drift detecte, blocage, puis deblocage apres correction.

TASK-114:
  titre: Runbooks incident + exercices de reprise critiques
  assigné: "@tea Murat"
  collaboration: "@qa Quinn preuves de reprise"
  prompt: |
    Couvrir GAME-TKT-022 avec:
    - runbooks WS indisponible, duplicate, out-of-order, replay partiel, adapter indisponible
    - checklist detection -> containment -> recovery -> verification
    - exercices traces et archives
    Tests: chaque scenario produit une preuve de resync coherent.

TASK-115:
  titre: Qualite mémoire/recall + gate obsolescence
  assigné: "@qa Quinn"
  collaboration: "@arch Winston regles de fraicheur"
  prompt: |
    Couvrir GAME-TKT-023 avec:
    - score de recall et indicateurs d'obsolescence
    - marqueurs de fraicheur sur references memoire
    - gate bloquante si seuil depasse
    Tests: reference obsolete detectee, gate bloquee, puis remediation validee.
```

### STORY-14-02 — Qualité de décision collective, FinOps et explicabilité

**@arch + @qa + @pm** | **Points** : 13 | **Cadence** : transverse

**Dépendances** : STORY-14-01 engagée, `verification-view`, `audit-view` et `board-view` utilisables.

**Statut de préparation** : Prête à lancer.

**Critères d'acceptation story** :

- Les livrables critiques passent par une contre-review orthogonale.
- Le coût et la latence par ticket deviennent visibles en review.
- Les décisions critiques laissent des `decision cards` auditables.

```yaml
TASK-116:
  titre: Protocole anti-chambre d'écho et contre-review orthogonale
  assigné: "@arch Winston"
  collaboration: "@qa Quinn validation workflow"
  prompt: |
    Couvrir GAME-TKT-024 avec:
    - protocole de contre-review orthogonale
    - checklist severite / resolution / objections substantielles
    - gate bloquante tant que la contre-review manque
    Tests: lot critique bloque sans contre-review, puis debloque apres completion.

TASK-117:
  titre: FinOps agentique par ticket, rôle et modèle
  assigné: "@pm John"
  collaboration: "@qa Quinn instrumentation"
  prompt: |
    Couvrir GAME-TKT-025 avec:
    - metriques cout, tokens, latence par ticket
    - normalisation par complexite
    - seuils d'alerte et extrait review
    Tests: derive detectee et alerte publiee sur ticket.

TASK-118:
  titre: Decision cards et explicabilité opérationnelle
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn validation audit"
  prompt: |
    Couvrir GAME-TKT-026 avec:
    - schema standard de decision card
    - production sur transitions critiques
    - exposition dans audit-view et vues operationnelles
    - gate si card obligatoire absente
    Tests: card visible, filtrable et gate bloquante en cas d'absence.
```

### STORY-14-03 — Provenance/licences et experimentation produit

**@pm + @tw + @qa** | **Points** : 8 | **Cadence** : transverse

**Dépendances** : STORY-14-02 engagée, registres assets/plugins et planning vivants disponibles.

**Statut de préparation** : Prête à lancer.

**Critères d'acceptation story** :

- Aucun asset ou plugin non conforme ne passe en review.
- Toute expérimentation produit se termine par une décision explicite reliée au backlog.

```yaml
TASK-119:
  titre: Gate conformité licences et provenance assets/plugins
  assigné: "@qa Quinn"
  collaboration: "@tw Paige bundle d'attribution"
  prompt: |
    Couvrir GAME-TKT-027 avec:
    - registre unique de provenance assets/plugins
    - verification source/licence/attribution
    - gate fail-closed sur non-conformite
    Tests: rapport pass/fail et blocage review si element non conforme.

TASK-120:
  titre: Framework d'expérimentation produit
  assigné: "@pm John"
  collaboration: "@tw Paige registre des decisions"
  prompt: |
    Couvrir GAME-TKT-028 avec:
    - template hypothese/metrique/garde-fou/decision
    - registre des experimentations
    - lien experience -> ticket -> decision backlog
    Tests: aucune experimentation ne se cloture sans mesure ni decision explicite.
```

---

## EPIC-15 — Host Bridge externe et surface multi-host

**Vision** : Convertir les tickets `GAME-TKT-047` à `GAME-TKT-051` en stories d’implémentation alignées sur les contrats, la policy et la surface runtime multi-host déjà cadrés.

**Statut local** : Couvre localement sur la tranche runtime host bridge de reference; conserver cet epic comme matrice de preuve et de reliquats, pas comme front runtime encore ouvert.

**Assignation principale** : `@arch` + `@dev` + `@qa`

**Sources opératoires** : [PAQUET-execution-host-bridge-agentique-externe.md](./PAQUET-execution-host-bridge-agentique-externe.md), [CONTRAT-host-bridge-agentique-externe.md](./CONTRAT-host-bridge-agentique-externe.md)

### STORY-15-01 — Host canon et contrats runtime externes

**@arch + @dev** | **Points** : 13 | **Sprint** : 10-11

**Dépendances** : `GAME-TKT-040`, contrats runtime V1 stables, façade cockpit multi-PC engagée.

**Statut de preparation** : Verifiee localement sur la tranche runtime de reference.

**Critères d'acceptation story** :

- Les hotes externes passent par un modèle canonique unique.
- Les actions, reviews et contextes externes deviennent replayables et auditables.

```yaml
TASK-121:
  titre: Host Binding + Capability Manifest canoniques
  assigné: "@arch Winston"
  collaboration: "@dev Amelia schemas runtime"
  prompt: |
    Couvrir GAME-TKT-047 avec:
    - Host Binding
    - Capability Manifest
    - mapping vendeur -> primitive canonique
    - registre des hotes dans les read models runtime
    Tests: manifests valides/invalides et projection du registre des hotes.

TASK-122:
  titre: Invocation Envelope, Context Ledger et Review Artifact
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn tests de contrat"
  prompt: |
    Couvrir GAME-TKT-048 avec:
    - Invocation Envelope
    - Context Ledger
    - Review Artifact
    - propagation additive dans audit-view, session-view et dashboard runtime
    Tests: replay, idempotence et rejection des payloads invalides.

TASK-123:
  titre: Vues runtime pour hotes externes
  assigné: "@dev Amelia"
  prompt: |
    Brancher les nouveaux contrats externes dans les vues runtime cibles:
    - audit-view
    - session-view
    - runtime-dashboard-view
    en gardant Forge comme source de verite.
    Tests: une action, une review ou un import externe se relit sans UI vendeur.
```

### STORY-15-02 — Policy engine externe et reviews comme evidence

**@dev + @qa** | **Points** : 13 | **Sprint** : 11

**Dépendances** : STORY-15-01 terminée, `GAME-TKT-037` et `GAME-TKT-038` stabilisés.

**Statut de preparation** : Verifiee localement sur la tranche runtime de reference.

**Critères d'acceptation story** :

- Aucun connecteur externe ne mute l'état durable hors policy.
- Les reviews externes deviennent des evidence refs cockpit de première classe.

```yaml
TASK-124:
  titre: Policy engine connecteurs externes + permission prompts
  assigné: "@dev Amelia"
  collaboration: "@qa Quinn tests négatifs"
  prompt: |
    Couvrir GAME-TKT-049 avec:
    - scopes fs/network/secrets/exec/config_write/write_budget
    - decisions ALLOW/PROMPT/DENY/DEGRADE
    - allowlists, degrade states et audit trail
    Tests: blocage d'un connecteur non approuve et degradation vers lecture seule.

TASK-125:
  titre: Reviews externes normalisées en evidence pack
  assigné: "@qa Quinn"
  collaboration: "@dev Amelia ingestion runtime"
  prompt: |
    Couvrir GAME-TKT-050 avec:
    - import review/check/comment -> Review Artifact
    - rattachement a traceId, taskId et evidenceRefs
    - exposition cockpit/audit/verification
    Tests: review importee consultable sans UI source et utilisable comme evidence ref.
```

### STORY-15-03 — Surface multi-host générique

**@dev + @qa + @ux** | **Points** : 8 | **Sprint** : 11

**Dépendances** : STORY-15-02 terminée, `GAME-TKT-020`, `GAME-TKT-044` et `GAME-TKT-046` engagés.

**Statut de preparation** : Verifiee localement sur la tranche runtime de reference.

**Critères d'acceptation story** :

- VS Code, web et hôtes externes lisent le même run sans divergence de causalité.
- Un hôte `stale`, `degraded` ou `blocked` remonte clairement dans la surface multi-host.

```yaml
TASK-126:
  titre: Host Bridge générique au-dessus du pont VS Code
  assigné: "@dev Amelia"
  collaboration: "@ux Sally surface multi-host"
  prompt: |
    Couvrir GAME-TKT-051 avec:
    - surface multi-host dans le dashboard runtime
    - bindings, capabilities, routines actives, health et degrade state
    - parite semantique web / VS Code / hotes externes
    Tests: meme run lu depuis plusieurs surfaces sans divergence.

TASK-127:
  titre: Validation d'interopérabilité multi-host
  assigné: "@qa Quinn"
  prompt: |
    Construire les preuves de la tranche multi-host:
    - compatibilite des focus et timelines
    - health snapshots host
    - absence de bypass policy via surface multi-host
    Tests: interop cockpit/host bridge et lecture degradee correcte.
```

---

## Calendrier macro (séquencement relatif)

| Sprint | Lots dominants | Objectif |
| --- | --- | --- |
| S0 | EPIC-00A + architecture + setup | Contrat canonique, flux critique de référence, cockpit minimal, ADRs et environnement initialisés |
| S1 | EPIC-01 front + EPIC-00 ouverture conditionnelle | Setup projet, ECS core, puis ouverture multi-PC seulement si EPIC-00A est prouvé |
| S2 | EPIC-01 + EPIC-02 démarrage + EPIC-00 poursuite | Game loop, renderer, sprites, puis flotte et leases si la gate post-challenge reste verte |
| S3 | EPIC-02 + EPIC-03 démarrage | Agents animés + rooms |
| S4 | EPIC-03 + EPIC-04 démarrage | Multi-rooms + Kanban |
| S5 | EPIC-04 + EPIC-05 | Kanban complet + communication |
| S6 | EPIC-06 | Orchestrateur + War Room |
| S7 | EPIC-07 + EPIC-08 | Mémoire visualisée + workflows |
| S8 | EPIC-09 socle + EPIC-13 front | Debug console, diagnostics connexion, son, XP, onboarding |
| S9 | EPIC-10 + EPIC-09 tranche 1 + TASK-044 | Config gamifiée, UI components, variantes challenge, Investigation Lab |
| S10 | EPIC-12 + EPIC-09 tranche 2 + EPIC-15 démarrage | Intégration, mode spectateur, Parallel Dispatcher, Code Review Room, host canon et contrats externes |
| S11 | EPIC-09 clôture + EPIC-12 release + EPIC-15 finalisation | Retro Room, Worktree Lab, Power Cards, Security Audit Room, host bridge multi-host, release et documentation finale |

**Notes** :

- Sprint S9 detaille : [SPRINT-S09-grimoire-game.md](SPRINT-S09-grimoire-game.md).
- Le cadre qualité de EPIC-11 s'applique à tous les sprints.
- EPIC-00A ouvre le reste du backlog runtime ; aucune surface riche, multi-PC ou multi-host ne contourne cette gate.
- EPIC-14 est transverse et s'exécute en parallèle des lots S9 à S11, au rythme des gates qualité et review.
- EPIC-15 reste bloqué tant que `GAME-TKT-054` puis EPIC-00 ne sont pas stabilisés.
- Le challenge workflow (WORKFLOW-challenge.md) s'applique à chaque sprint en clôture.

---

Fin du document Epics/Stories/Tasks — Version 1.1
