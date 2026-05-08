# Game Design Document — Grimoire Game

> Projet : **Grimoire Game** — Virtual AI Agent Office
> Version : 1.3 — Avril 2026
> Auteurs : BMad Master + UX Designer + Game Design Specialist (multi-agent)
>
> **Changelog v1.3** : Enrichissement des 15 points d'audit — bulles §3.3, Kanban §3.4, communication §3.5,
> challenge §3.6, bibliothèque §3.8, agent factory §3.9, desks §3.10, timeline §4.1, XP §5.1,
> retro room §5.3, sons §6, onboarding §7, tileset animé §2.3 ; teams dynamiques §3.15–§3.19 ;
> Investigation Lab §3.11, Parallel Sprint §3.12, Code Review Room §3.13, Security Audit §3.14,
> Power Cards §5.5, Worktree Lab §5.4.
>
> **Changelog v1.2** : Assets libres Kenney CC0 + LPC référencés, palette conviviale étendue,
> catalogue déco complet (§2.6), colliders et nav-grid (§3.1-bis), protection des passages (§3.1-ter),
> mode décoration utilisateur (§4.4).

---

## 1. Concept du jeu

### 1.1 Pitch

**Grimoire Game** transforme la gestion de vos agents IA en une expérience de jeu de simulation immersive. Imaginez diriger une agence de détectives/hackers dans un monde pixel art des années 90 — chaque agent est un personnage qui vit dans vos locaux, travaille sur ses tâches, communique, dort, mange et parfois se perd dans ses propres pensées.

Genre : **Simulation de bureau / Jeu de gestion en temps réel**

Inspirations vidéo-ludiques :
- **Stardew Valley** — ambiance cosy, pixel art chaleureux, routine satisfaisante
- **The Sims** — visualisation des agents avec besoins/états
- **Dungeon Keeper** — vision God-mode sur vos "sbires"
- **RimWorld** — colonists avec personnalités distinctes, logs d'événements
- **Factorio** — efficacité des systèmes visibles, flow states
- **Habbo Hotel / Gather.town** — openspace virtuel, déplacements fluides
- **Papers Please** — interface de configuration avec formulaires gamifiés

### 1.2 Structure du monde

```
┌─────────────────────────────────────────────────────────────┐
│                    GRIMOIRE HQ                              │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Team DEV    │  │  Team QA     │  │  Team PM     │     │
│  │  (openspace) │  │  (openspace) │  │  (boardroom) │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│        │                  │                  │              │
│  ══════╪══════════════════╪══════════════════╪══════        │
│  COULOIR PRINCIPAL (zone de passage inter-teams)            │
│  ══════╪══════════════════╪══════════════════╪══════        │
│        │                  │                  │              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  SALLE DE    │  │  SALLE DE    │  │  WAR ROOM    │     │
│  │  RÉUNION     │  │  CHALLENGE   │  │ (Orchestr.)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  BIBLIOTHÈQUE│  │  AGENT       │                        │
│  │  (mémoire)   │  │  FACTORY     │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  RETRO ROOM  │  │  CODE REVIEW │  │  SECURITY    │     │
│  │  (bilan)     │  │  ROOM        │  │  AUDIT ROOM  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  Rooms dynamiques (minimap) : Investigation Lab,            │
│  Parallel Sprint Panel, Worktree Lab (par branche git)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Direction Artistique

### 2.1 Style Général

**Style : Pixel Art 16-bit "Cozy Dark Academia"**

- Tiles de 16×16 pixels
- Résolution native : 640×480 upscalée en crisp-edges
- Palette de couleurs : tons sombres chaleureux (bois, lumières chaudes, écrans bleus)
- Atmosphère : bureau de nuit ultra-moderne teinté de magie

### 2.2 Palette principale

```
Backgrounds:
  --floor-wood:    #2D1B0E   (parquet sombre)
  --floor-carpet:  #1A2340   (moquette bleu nuit)
  --wall-dark:     #0F0F1A   (murs sombres)
  --wall-accent:   #1E3A5F   (murs lumineux)

Mobilier:
  --desk-wood:     #4A2E0A   (bois chaud)
  --screen-glow:   #0A84FF   (lueur écrans)
  --plant-green:   #2D6A4F   (plantes déco)
  --lamp-warm:     #FFA040   (lumières chaudes)

Agents:
  --agent-dev:     #3FB950   (vert développeur)
  --agent-qa:      #BC8CFF   (violet QA)
  --agent-pm:      #F0883E   (orange PM)
  --agent-arch:    #39D2C0   (cyan architecte)
  --agent-orch:    #58A6FF   (bleu orchestrateur)
  --agent-writer:  #7EE787   (vert clair tech-writer)
  --agent-analyst: #D29922   (jaune analyste)
  --agent-sm:      #F778BA   (rose SM)
  --agent-ux:      #FF9EE7   (rose clair UX)

UI Elements:
  --bubble-bg:     #161B22   (fond bulles)
  --accent-magic:  #8B5CF6   (mauve magie)
  --gold-xp:       #FFD700   (or XP/achievements)
```

### 2.3 Tileset principal

```
Floor tiles (16x16):
  - parquet_light, parquet_dark, parquet_worn
  - carpet_blue, carpet_red, carpet_green
  - tile_concrete, tile_marble, tile_tech
  - rug_center, rug_border, rug_corner

Wall tiles (16x16):
  - wall_plain, wall_window, wall_door_open, wall_door_closed
  - wall_bookshelf, wall_whiteboard, wall_screen_large
  - wall_poster_code, wall_poster_matrix, wall_window_night

Furniture (16x32 ou 32x32):
  - desk_simple, desk_dual_screen, desk_corner
  - chair_office, chair_meeting, couch_sofa
  - server_rack, printer, coffee_machine
  - whiteboard_kanban, bookshelf_full, plant_small, plant_large
  - meeting_table, presentation_screen
  - monitor_on, monitor_off, monitor_code
  - trophy_shelf, award_plaque, coffee_cup
```

**Tiles animés (spritesheet multi-frames) :**

```
Animated (loop auto, priorité faible) :
  - monitor_blink   (4f — curseur CLI qui clignote)
  - coffee_steam    (6f — vapeur au-dessus du café)
  - plant_sway      (8f — plante qui ondule)
  - server_led      (4f — LED serveur rack)
  - door_open_anim  (3f — ouverture/fermeture porte)
  - window_rain     (12f — pluie sur vitre, déclenché si météo API = rainy)
  - fan_spin        (8f — ventilateur plafond)
```

**Tiles interactifs (déclencheurs in-world) :**

| Tile | Interaction | Effet |
|---|---|---|
| `coffee_machine` | Clic → | +`coffee_cup` item (buff +10% focus 5min), délai 30s avant rechargement |
| `printer` | Clic → | SFX impression + animation `document_flying` (item document créé) |
| `server_rack` | Clic → | Overlay console `console_popup` (logs système en lecture seule) |
| `whiteboard_kanban` | Clic → | Ouvre le board Kanban de la room en mode plein écran |

**Variantes contextuelles :**

```
Day/Night (basculement auto selon heure système, TZ locale) :
  - wall_window    → wall_window_day (lumière) / wall_window_night (obscurité + reflet)
  - parquet_light  → parquet_warm (journée) / parquet_cool (nuit)

État d'usure (rooms non visitées) :
  - parquet_light  → parquet_worn    (room sans activité > 3 sprints)
  - desk_simple    → desk_empty      (bureau non assigné > 7 jours)
  - plant_large    → plant_wilted    (room non visitée > 5 jours)
```

### 2.3-bis Assets libres réutilisables (zéro travail de création)

Le projet dispose déjà d'assets procéduraux issus du module **pixel-agent** et peut
importer directement trois packs **CC0** de Kenney.nl ainsi qu'un pack LPC pour enrichir
la décoration sans effort supplémentaire.

**Assets pixel-agent déjà disponibles** (`_bmad-output/assets/`) :

| Fichier | Contenu | Réutilisation immédiate |
|---|---|---|
| `characters/char_0..5.png` | Spritesheet 6 rôles × 3 états × 3 directions | ✅ Personnages agents |
| `floors/floor_0..8.png` | 9 textures de sol (parquet, moquette, dalle) | ✅ Tiling fond |
| `walls/wall_0.png` | Bitmask walls 4×4 (64×128 px) | ✅ Murs / fenêtres |
| Canvas procéduraux | `makeDeskSprite`, `makePlant`, `makeWhiteboard`, `makeDeskChair` | ✅ Mobilier de base |

**Kenney.nl — CC0 (domaine public, aucune attribution requise)** :

| Pack | Tiles | Contenu exploitable |
|---|---|---|
| [Top-down Shooter](https://kenney.nl/assets/top-down-shooter) | 16×16 | Mobilier de bureau, caisses, comptoirs, sols, murs — 580 fichiers |
| [Tiny Town](https://kenney.nl/assets/tiny-town) | 16×16 | Tables, chaises, étagères, tapis, plantes, objets intérieurs |
| [Tiny Dungeon](https://kenney.nl/assets/tiny-dungeon) | 16×16 | Décoration alternative (coffres, torches, bannières — ambiance "dark academia") |

**Stratégie d'import Kenney** : extraire uniquement les tiles intérieurs du spritesheet,
les coloriser via `multiply` composite (même technique que `makeFloorTile`) pour les
adapter à la palette "cozy dark academia" sans retouche manuelle.

**OpenGameArt LPC — CC-BY-SA 3.0** (attribution + share-alike) :

| Pack | Contenu exploitable |
|---|---|
| [[LPC] House interior and decorations](https://opengameart.org/content/lpc-house-interior-and-decorations) | Cadres photos, tapis, rideaux, objets de bureau, lampes |
| [[LPC] Misc tile atlas](https://opengameart.org/content/lpc-misc-tile-atlas-interior-exterior-trees-bridges-furniture) | Pont mobilier complet (étagères, lits, tables, déco) |

> **Note licence** : les assets LPC sont CC-BY-SA 3.0 — le jeu embarquant ces assets
> doit mentionner les auteurs et rester open-source ou garder ces assets séparés.
> Kenney CC0 est sans contrainte.

### 2.3-ter Palette conviviale étendue

La direction "cozy dark academia" est renforcée par une palette de teintes chaudes
et des tons lumineux doux pour les objets de décoration :

```
Décoration conviviale:
  --deco-lamp-warm:    #FFB347   (guirlandes LED chaudes)
  --deco-lamp-cool:    #A8D8EA   (néon bleu-blanc écran)
  --deco-rug-burgundy: #7B2D3F   (tapis bordeaux)
  --deco-rug-teal:     #1B5E6E   (tapis sarcelle)
  --deco-rug-amber:    #C67B3A   (tapis ocre)
  --deco-plant-moss:   #4A7C59   (mousse/fougère)
  --deco-plant-bloom:  #D4607A   (fleur rose)
  --deco-frame-gold:   #C9A84C   (cadre photo doré)
  --deco-frame-dark:   #2C2C3A   (cadre photo sombre)
  --deco-mug-red:      #C0392B   (mug rouge)
  --deco-mug-cyan:     #1ABC9C   (mug cyan "debug")
  --deco-neon-purple:  #9B59B6   (enseigne néon violet)
  --deco-neon-green:   #27AE60   (enseigne néon vert)
  --deco-banner-team:  per-team  (couleur de team)
  --deco-window-dawn:  #FF8C69   (fenêtre au coucher)
  --deco-winter-snow:  #DCE6F0   (fenêtre enneigée — saisonnier)

Ambiance saisonnière (activable manuellement ou automatique par date réelle):
  Printemps : fleurs sur les fenêtres, plantes fleuries
  Été       : lumière vive, store à moitié baissé
  Automne   : feuilles mortes dans les coins, lumières orange
  Hiver     : neige aux fenêtres, guirlandes de Noël, lumière froide
```

### 2.3-quad Catalogue des objets décoratifs conviviaux

Ces objets enrichissent l'atmosphère des pièces. Tous sont placés par le moteur ou par
l'utilisateur (voir §4.4 Mode Décoration).

**Catégorie : Lumières & Ambiance**

```
Objets                 Taille   Collider  Source
guirlande_led          64x4     Aucun     Procédural (points lumineux animés)
lampe_bureau           16x24    Solid 8x8 Kenney Top-down Shooter
lampe_sol              16x28    Solid 8x8 Kenney Top-down Shooter
neon_sign_[color]      32x16    Aucun     Procédural (canvas text glow)
chandelier             32x32    Aucun     Procédural
fenetre_rideau         16x32    Aucun     LPC House Interior
```

**Catégorie : Plantes & Nature**

```
Objets                 Taille   Collider  Source
plant_small            16x20    Solid 12x8  Pixel-agent: makePlant()
plant_large            16x32    Solid 12x10 Pixel-agent: LARGE_PLANT.png
cactus                 16x20    Solid 10x8  Pixel-agent: CACTUS.png
fougere_suspendue      16x20    Aucun     Procédural (suspendu au plafond)
vase_fleurs            16x16    Solid 10x6  Procédural
terrarium              16x16    Solid     Procédural
```

**Catégorie : Confort & Détente**

```
Objets                 Taille   Collider  Source
sofa                   32x20    Solid 32x10 Pixel-agent: SOFA.png
bean_bag_[color]       16x14    Solid 14x8  Procédural
coffee_table           24x16    Solid     Pixel-agent: COFFEE_TABLE.png
tapis_[pattern]        32x24    Aucun     Kenney Tiny Town (colorisé)
coussin_[color]        10x10    Aucun     Procédural
pouf                   14x12    Solid 12x6  Procédural
```

**Catégorie : Personnalisation d'équipe**

```
Objets                 Taille   Collider  Source
banniere_equipe        16x40    Aucun     Procédural (couleur de team)
fanion_bureau          8x12     Aucun     Procédural
trophee               16x20    Solid 6x4   Pixel-agent: trophy_shelf (extrait)
tableau_liege          32x24    Wall-mount  Procédural (post-its aléatoires)
cadre_photo            12x14    Wall-mount  Procédural / LPC House
plaque_team            24x8     Wall-mount  Procédural (nom de team gravé)
```

**Catégorie : Nourriture & Boissons**

```
Objets                 Taille   Collider  Source
mug_[color]            8x10     Aucun     Pixel-agent: COFFEE.png (colorisé)
pizza_box              16x14    Solid 14x4  Procédural (item comique)
vending_machine        16x32    Solid     Procédural
fontaine_eau           16x28    Solid 8x10  Procédural
bol_snacks             10x8     Aucun     Procédural
```

**Catégorie : Tech & Gaming (clins d'oeil)**

```
Objets                 Taille   Collider  Source
retro_console          24x16    Solid 24x6  Procédural (Game Boy géante)
figurine_[role]        8x12     Aucun     Procédural (mini-version agent)
poster_[theme]         24x32    Wall-mount  Procédural (pixel art)
server_rack_mini       16x32    Solid     Procédural
rubber_duck            8x8      Aucun     Procédural (canard débogueur 🐥)
```

### 2.4 Personnages (sprite sheets)

Chaque personnage a 4 directions × 3 frames d'animation pour le déplacement, + des animations spéciales :

```
Direction sprites (4 dir × 3 frames chacune):
  - walk_north[0..2], walk_south[0..2], walk_east[0..2], walk_west[0..2]

État animations (face caméra ou top-down):
  - idle_breathe        (loop subtile 4f)
  - sit_type_fast       (frappe rapide 4f)
  - sit_type_slow       (frappe lente 4f)
  - sit_read            (lecture, yeux qui bougent 2f)
  - sit_think           (main sur menton, bulle ... 3f)
  - sit_code            (code intense, scroll 4f)
  - stand_talk          (gestes avec les mains 4f)
  - stand_present       (pointer vers écran 4f)
  - walk_papers         (agent avec documents 3f/dir)
  - walk_coffee         (agent avec café 3f/dir)
  - react_success       (celebration, saut 4f)
  - react_error         (erreur, se gratte tête 3f)
  - react_panic         (urgence, agitation 4f)
  - react_confused      (haussement épaules, head tilt 3f)
  - search_web          (typing + magnifier 4f)
  - meeting_listen      (nod, écoute active 2f)
  - sleep_desk          (bref si inactif 3f)
  - magic_cast          (pour l'orchestrateur 4f)
  - hand_raise          (lever la main pour prendre la parole, 2f — challenge)
  - react_respond       (présentateur qui répond à une critique, geste explicatif, 2f)
  - vote_approve        (thumb up pixel art animé, 2f)
  - vote_changes        (main à l'horizontale « avec réserves », 2f)
  - vote_reject         (thumb down pixel art animé, 2f)
```

### 2.5 Éléments UI gamifiés

**Health bars stylées RPG :**
```
[████████░░] 80% — Context   (160k / 200k tokens — source: CONTEXT_UPDATE event)
[████░░░░░░] 40% — Rate limit (40% — source: CONTEXT_UPDATE.rateLimitPct)
[██████████] 100% — Memory
```
*(Si `CONTEXT_UPDATE` n'est pas reçu, les barres Context et Rate limit affichent `N/A` plutôt qu'une valeur erronée — cf. TECH §11.4)*

Affichage supplémentaire dans le panel agent (clic sur personnage) :
```
┌── STATS RPG ────────────────────┐
│ Focus    [███████░░░]  70    │
│ Speed    [████████░░]  80    │
│ Precision[█████████░]  90    │
└──────────────────────────┘
```
*(Stats issues de `agents.stats` JSON — remises à zéro par agent, modifiables ou bonus via achievements)*

**Valeurs par défaut selon le rôle** (champ `stats` JSON initial) :

| Rôle | Focus | Speed | Precision |
|---|---|---|---|
| dev | 80 | 75 | 85 |
| qa | 75 | 60 | 92 |
| architect | 90 | 65 | 88 |
| pm | 70 | 80 | 75 |
| tech-writer | 72 | 70 | 90 |
| analyst | 85 | 68 | 82 |
| sm | 70 | 85 | 78 |
| ux | 75 | 72 | 80 |
| orchestrator | 95 | 90 | 90 |

**Bulles de dialogue :**
```
.bubble {
  style: "pixel border 1px dither";
  tail: "pointing to character";
  max-chars: 80;
  fade-time: 3000ms;
  colors: by-agent-class;
}
```

**Status badges flottants :**
- 🔵 Thinking (animation pulse)
- ⚙️ Tool call (rotation)
- 📝 Writing (animation écriture)
- 🔍 Searching (animation loupe)
- 💬 Talking (animation vagues sonores)
- ⏳ Waiting (animation sablier)
- ✅ Done (flash vert)
- ⚠️ Warning (clignotement jaune)
- 🚨 Error (pulse rouge)
- 💤 Sleeping (ZZZ lent, pulse 0.5fps)
- ❗ Panic (rouge, shake 2f)
- 😕 Confused (haussement épaules 2f, boucle lente)

**Paramètres d’affichage des labels d’agents :**

- **Always-show overlay** : option activable (Settings → Always-show labels) pour maintenir tous les labels d’agents visibles en permanence.
  - Agents non-focusés : opacité réduite à 40 %
  - Agent focusé (dernier cliqué) : opacité 100 %
- **Multi-root workspace** : si VS Code a plusieurs dossiers ouverts, un picker DOIT apparaitre au Premier spawn (« + Agent ») pour choisir le répertoire de rattachement.

**Panel de performance in-world (Perf/Canary Overlay) :**

```
📊 Performance — Sprint #N
LCP: 1.2s  ▼  CLS: 0.01  INP: 95ms  Ressources: 24 (890 KB)
[Status: ✅ Dans les seuils]  [Comparer baseline]
```

- Affiché dans la War Room sur un écran dédié (activable via bouton `[📊 Perf]` en header)
- Source : `RetroMetricsCollector.ts` (lit les résultats de benchmarks + tests Playwright)
- Seuils d'alerte : LCP > 2.5s → ⚠️ jaune ; LCP > 4s → 🚨 rouge ; CLS > 0.1 → ⚠️
- Animation War Room : écran clignote en jaune si régression détectée vs baseline précédente
- Baseline sauvegardée après chaque sprint validé (`.context/perf-baselines/sprint-<N>.json`)

---

## 3. Mécaniques de jeu principales

### 3.1 Système de déplacement

Les agents se déplacent selon les règles suivantes :

1. **Déplacement autonome** : En allant chercher un collègue ou une ressource, l'agent emprunte le chemin le plus court (A* pathfinding).
2. **Déplacement narratif** : Certains déplacements sont motivés (aller dans la salle de réunion, apporter un rapport, chercher un café).
3. **Vitesse** : Chaque agent a une vitesse de déplacement (tiles/sec), modifiable.
4. **Collision avoidance** : Les agents s'évitent (simple repulsion quand proximité < 2 tiles).

### 3.1-bis Système de colliders

Chaque entité du monde porte une **bounding box** qui définit son comportement physique.
Le système est basé sur une **grille de navigation** (nav-grid) de tiles 16×16.

**Types de colliders :**

```
Type            Description                       Exemples d'objets
────────────────────────────────────────────────────────────────────
SOLID           Impassable — bloque agents+déco   Murs, desks, server_rack
PASSABLE        Aucune restriction de passage      Tapis, guirlandes, affiches
WALL_MOUNT      Collé au mur, zéro footprint sol   Cadres, bannieres, néons
SOFT            Passable mais freine (×0.6)        Plantes, coussins, poufs
AGENT_TOKEN     Zone réservée autour d'un agent    Voir §3.1-ter Agent Token Zone
DOOR            Ouvre/ferme — passable si ouvert   Portes, arches
```

**Bounding boxes des agents :**

Chaque agent a un **corps** (12×10 px sur la grille) centré sur sa position tile.
Le corps suit la position interpolée (sub-pixel smooth movement).

```
Footprint agent : 12×10 (3/4 de tile)
Bounding box visuel : 16×32 (sprite complet)
Zone d'interaction : cercle R=24px (clic, bulle de dialogue)
```

**Navigation mesh (nav-grid) :**

La grille de navigation est recalculée à chaque modification de la disposition
(placement/retrait d'un objet, ouverture de porte). Elle est stockée en mémoire
dense (`Uint8Array`, 1 byte par tile) :

```
0x00 = libre (walkable)
0x01 = mur fixe (SOLID permanent)
0x02 = meuble utilisateur (SOLID, déplaçable)
0x03 = meuble déco (PASSABLE ou SOFT)
0x04 = zone réservée agent (AGENT_TOKEN)
0x05 = porte fermée
0x06 = zone de passage protégé (voir §3.1-ter)
```

**Détection de collision :**

Avant chaque déplacement A*, le pathfinder consulte la nav-grid. Si une tile est
`0x06` (passage protégé), aucun objet ne peut y être placé mais les agents passent
librement. Si une tile est `0x02` (meuble utilisateur), le pathfinder la contourne.

**Animations de collision douce :**

Quand deux agents se retrouvent trop proches (< 12px), un **push gentle** les écarte
progressivement (+ 1 px/frame en direction opposée) sans téléportation brusque.
Si trois agents ou plus se bloquent mutuellement, le `CollisionResolver.ts` détecte
le deadlock et téléporte le moins prioritaire vers la tile libre la plus proche.

**Colliders et décoration :**

Chaque objet décoratif déposé par l'utilisateur enregistre ses colliders dans la
nav-grid via `NavGridService.registerObject(obj)`. Cette méthode :
1. Calcule les tiles occupées (footprint × rotation).
2. Vérifie l'absence de conflit (§3.1-ter).
3. Met à jour la nav-grid et invalide le cache A*.
4. Émet un événement `NAV_GRID_UPDATED` pour recompiler les paths en cours.

### 3.1-ter Protection des passages et accès aux agents

**Objectif** : empêcher l'utilisateur de placer des objets qui bloqueraient les couloirs
ou rendraient un agent inaccessible, sans pour autant contraindre la créativité.

**Stratégie retenue : Zones protégées dynamiques + feedback immédiat**

Cette approche est préférable à un lock total car elle conserve la liberté décorative
tout en prévenant les seuls cas réellement problématiques.

**Zone 1 — Couloir principal (protection absolue)**

```
┌─────────────────────────────────────────────────────────────────┐
│  Les tiles du COULOIR PRINCIPAL sont marquées 0x06 en nav-grid  │
│  et portent le flag CORRIDOR_LOCKED = true.                     │
│                                                                  │
│  Règle : aucun objet SOLID ne peut être déposé sur ces tiles.   │
│  Les objets PASSABLE (tapis, affiches) sont autorisés.          │
│                                                                  │
│  Visualisation : léger overlay animé « grille bleue pulsante »  │
│  visible uniquement pendant le Mode Décoration actif.           │
└─────────────────────────────────────────────────────────────────┘
```

**Zone 2 — Accès desk (Agent Token Zone)**

Chaque bureau actif génère automatiquement une **Agent Token Zone** de 3×3 tiles
devant lui (côté entrée). Cette zone est marquée `0x04` dans la nav-grid.

```
Représentation :
  [  MURS  ]
  [  DESK ⬛ ]   ← bureau
  [ ⬛⬛⬛   ]   ← agent token zone (3×1 tiles devant)
  [         ]   ← libre

Règle : aucun objet SOLID dans l'agent token zone.
But  : l'agent peut toujours atteindre son bureau ← garantie de pathfinding.
```

L'agent token zone se déplace si le bureau est déplacé. Elle disparaît si le bureau
est supprimé. Elle n'est visible que pendant le Mode Décoration.

**Zone 3 — Doorways (seuils de portes)**

Chaque porte/arche génère un **doorway clearance** de 2 tiles avant et 2 tiles après.
Ces tiles sont marquées `0x06` et refusent tout objet SOLID.

```
  [...  2t libre  ] [PORTE] [  2t libre  ...]
                    ↑ doorway clearance = 4 tiles min libres
```

**Validation en temps réel (pendant le drag-and-drop) :**

```
Phase 1 — Ghost preview :
  L'objet suit le curseur avec une transparence de 60% (mode fantôme).
  La preview montre les tiles qu'il occuperait.

Phase 2 — Validation :
  VERT   → tiles libres, placement autorisé, colliders OK
  ORANGE → zone SOFT ou near-corridor : avertissement "peut ralentir les agents"
  ROUGE  → zone protégée (0x04, 0x05, 0x06) : placement bloqué

Phase 3 — Feedback si blocage détecté :
  Une bulle d'aide apparaît :
  "Ce meuble bloquerait l'accès de [Agent]. Placez-le ailleurs."
  L'objet rebondit visuellement vers la position d'origine.
```

**Détection de blocage complet (vérification post-placement) :**

Après chaque placement d'un objet SOLID, le système vérifie que chaque agent
a au moins **un chemin valide** depuis sa position actuelle jusqu'à chacune des
sorties de pièce. Cette vérification utilise un BFS simplifié (O(n) sur la
grille locale) et se déclenche en arrière-plan dans un Worker. Si un chemin est rompu :

```
⚠️ Alerte : "[Objet] empêche [Agent] d'accéder à la sortie nord.
   L'objet a été retiré automatiquement."
   [Voir où le placer]  [Annuler]
```

Par défaut, l'objet est retiré automatiquement. Un setting avancé
(`advanced.allow_full_block`) permet de désactiver ce garde-fou.

**Tableau récapitulatif des zones et règles :**

| Zone | Flag nav-grid | SOLID interdit | PASSABLE autorisé | Visible en déco |
|---|---|---|---|---|
| Couloir principal | `0x06` | ✅ | ✅ | Overlay bleu pulsant |
| Agent Token Zone | `0x04` | ✅ | ✅ | Overlay vert pulsant |
| Doorway clearance | `0x06` | ✅ | ✅ | Overlay bleu pulsant |
| Murs | `0x01` | ✅ | ❌ | Non (mur opaque) |
| Zone libre | `0x00` | ❌ | ✅ | Non (invisible) |

**Vitesse par archetype (valeurs par défaut) :**

| Archetype | Tiles/sec | Raison narrative |
|---|---|---|
| dev | 2.5 | Concentré, marche lentement |
| qa | 3.0 | Méthodique mais vif |
| pm | 3.5 | Toujours pressé, réunion en retard |
| architect | 2.0 | Réfléchit en marchant |
| orchestrator | 4.0 | Se déplace rarement mais vite |
| sm | 3.2 | Multi-tasking, transitions rapides |
| ux | 2.8 | Observe, ralentit souvent |
| analyst | 2.3 | Absorbé dans ses données |
| tech-writer | 2.6 | Régulier, posé |

**Gestion des échecs A\* (pathfinding failure) :**

- Chemin bloqué par un autre agent → attente 500ms → retry. Après 3 retries consécutifs → contournement par la case adjacente libre la plus proche.
- Chemin bloqué par un obstacle permanent (mur, meuble) → recalcul avec heatmap élargie. Si impossible → agent reste sur place, badge `⚠️ Bloqué` 2s, puis retour à IDLE.
- Si la destination (ex: bureau cible) est occupée par un autre agent → l'agent attend debout à 1 tile de distance, animation `meeting_listen` (attente active), jusqu'à libération ou timeout 60s → abandon + notification War Room.

**File de déplacement (queue) :**

Quand plusieurs agents convergent vers la même destination simultanément (ex: Challenge convocation) :
- File FIFO par proximité — l'agent le plus proche de la destination entre en premier.
- Les autres s'arrêtent à 2 tiles de distance, animation `meeting_listen`, entrent quand la place se libère (sliding queue).
- Visualisation : les agents font une file physiquement visible dans le couloir ou à l'entrée d'une room.

### 3.2 Machine à états des agents

```
IDLE ──────────────────────────────> WORKING
  │                                     │
  ├── Reçoit tâche ──────────────────────┤
  │                                     │
  ├── Timeout (≥5min) → SLEEPING       │
  │     └── réveil au prochain event   │
  │                                     │
  ├── Message entrant → COMMUNICATING   │
  │          └── retour → WORKING       │
  │                                     │
  ├── Error → PANIC (3s) → WORKING      │
  │                                     │
  └── Tool call → TOOL_USE → WORKING    │
                                        │
WORKING states:
  - TYPING       (code, docs, config)
  - READING      (fichier, web, mémoire)
  - THINKING     (réflexion/planning)
  - SEARCHING    (web search, grep)
  - EXECUTING    (run command, test)
  - WAITING      (attente réponse)

SLEEPING state:
  - Animation: sleep_desk (tête sur le bureau)
  - Déclencheur: inactivité ≥ 5 minutes
  - Réveil: au prochain WS event entrant

CONFUSED state:
  - Animation: react_confused (haussement épaules, head tilt 3f)
  - Déclencheur: prompt incomplet, dépendance manquante, clarification attendue
  - Sortie: WS event CLARIFICATION_RECEIVED → WORKING, ou timeout 30s → IDLE

DEBUGGING state (4 sous-phases):
  - Ph1: ROOT_CAUSE — badge 🔄 Ph1, animation sit_think (boucle)
  - Ph2: PATTERN — badge 🔍 Ph2, animation sit_read (comparaison)
  - Ph3: HYPOTHESIS — badge 🧪 Ph3, animation sit_think (hypothèse)
  - Ph4: IMPLEMENTATION — badge 🛠️ Ph4, animation sit_type (correctif)
  - Loi de Fer: FIX_PROPOSED sans ROOT_CAUSE_IDENTIFIED → avertissement ⚠️ sur l’écran War Room
  - Après 3× FIX_FAILED: alerte « Architecture Review Required » + notification Orchestrateur

BACKGROUND_QUEUE state:
  - Animation: subtle pulse 0.3fps (halo bleu), sprite à opacité 70 %
  - Déclencheur: agent en queue (background agent attend la complétion d’une opération)
  - Survie garantie jusqu’à fin de l’opération (événement QUEUE_COMPLETE)
  - NE doit PAS être reclaimé comme siège par un autre agent pendant cet état
  
COMMUNICATING states:
  - TALKING_LOCAL   (même pièce)
  - WALKING_TO      (en route vers autre agent)
  - IN_MEETING      (salle de réunion)
  - PRESENTING      (salle de challenge)
```

### 3.3 Système de bulles de dialogue

Les bulles affichent en temps réel :
- Les **dernières lignes générées** par l'agent (tronquées à 80 chars)
- Le **nom du tool en cours** (`🔧 read_file: config.yaml`)
- Les **messages inter-agents** (avec flèche directionnelle)
- L'**état émotionnel** (emoji représentant le mood)

Format :
```
┌─────────────────────┐
│ 💭 Analyzing deps…  │
│ 🔧 run_in_terminal  │
└──────┐              │
       │ (agent pic)  │
```

**Gestion des chevauchements (multi-agent simultané) :**

Quand plusieurs agents sont actifs dans la même room, les bulles risquent de se superposer. Règles de priorisation :

| Priorité | Condition | Comportement |
|---|---|---|
| 1 (max) | Agent focusé (dernier cliqué) | Bulle toujours au premier plan, opacité 100% |
| 2 | Agent en DEBUGGING ou ERROR | Bulle au premier plan (urgence), fond rouge |
| 3 | Agent en COMMUNICATING | Bulle visible, opacité 85% |
| 4 | Agents WORKING normaux | Décalage spatial automatique (offset aléatoire ±8px), opacité 60% |
| 5 (min) | Agent SLEEPING | Bulle masquée (ZZZ seulement) |

- Si 5+ bulles simultanément → mode **compact** : les bulles non-prioritaires réduites à une seule ligne + icône de type.
- Survol d'une bulle compacte → expansion complète.

**Expand on click :**

Clic sur une bulle tronquée → popup étendu latéral : texte complet non tronqué, scrollable, max 500 chars. Fermeture : clic ailleurs ou touche `Esc`.

**Mode replay (Timeline scrub) :**

En mode replay (scrub de la Timeline Bar), les bulles sont restituées depuis les snapshots :
- Texte exact de la bulle au moment T, couleur et badge d'état d'origine.
- Indicateur `[⏮ Replay]` en coin supérieur-droit de la bulle pour la distinguer du live.
- Les bulles de replay ne font pas de son (muet en mode replay sauf si l'utilisateur réactive).

### 3.4 Kanban mural in-world

Chaque team possède un grand tableau blanc pixelisé sur lequel sont affichées les cartes Kanban.

**Interaction :**
- Double-clic sur une carte → ouvre le détail
- Glisser-déposer une carte entre colonnes
- Clic droit sur tableau → créer une nouvelle tâche
- Les agents assignés « marchent » vers leur carte quand ils la prennent

**Colonnes et couleurs :**
```
| 📋 BACKLOG | ✅ TODO | ⚡ IN PROGRESS | 🔍 REVIEW | ✨ DONE |
  (gris)      (bleu)    (jaune pulsé)     (violet)    (vert)
```

**Cards Kanban comportent :**
- Titre + icône de type (bug 🐛, feature ✨, infra 🏗️, doc 📚, research 🔬, test 🧪, refactor ♻️, security 🔒, design 🎨)
- Avatar de l'agent assigné
- Barre de progression estimate
- Tags de priorité (🔴 P0, 🟠 P1, 🟡 P2, 🟢 P3)
- Prompt pré-construit (visible en clic)
- **Date d'échéance** (optionnelle — icône 📅, rouge si dépassée)
- **Sous-tâches** : clic droit → `[+ Sous-tâche]` — liste déroulante sous le titre de la carte avec cases à cocher. Barre de progression liée au ratio sous-tâches complétées.

**Gestion du débordement (overflow) :**

- Board limité à **50 cartes visibles** par colonne. Au-delà : scroll vertical sur la colonne (molette + grab).
- Indicateur `[+N masquées]` en bas de colonne si > 50 cartes.
- Mode **compact view** (icône ⊡ en header du board) : cartes réduites à 1 ligne (titre + icône + avatar), permettant de voir 3× plus de cartes.
- Zone `✨ DONE` : archivage automatique après 7 jours. Les cartes archivées disparaissent du board mais restent dans `.context/kanban-archive/`.

**Audit trail :**

Chaque déplacement de carte est logué automatiquement :
```json
{ "card": "INT-042", "from": "IN PROGRESS", "to": "REVIEW",
  "by": "Amelia", "ts": "2026-04-05T14:32:00Z" }
```

Accessible via clic droit sur une carte → `[📋 Historique]` : liste chronologique de tous les mouvements, assignations et commentaires. Exportable en CSV.

### 3.5 Système de communication visuelle

```
Types de messages visualisés:

1. HANDOFF (transfert de tâche)
   Agent A ──[doc icon]──> Agent B
   Animation: parchemin qui vole de A vers B

2. REQUEST (demande d'info)
   Agent A ~~[?bubble]~~> Agent B
   Animation: bulle vide qui file vers B, puis bulle réponse

3. BROADCAST (orchestrateur → tous)
   Orchestr. ──[megaphone]──> all agents
   Animation: ondes concentriques depuis War Room

4. ESCALATION (problème → orchestrateur)
   Agent A ──[!icon]──> Orchestr.
   Animation: courbe vers War Room, flash rouge sur Orchestr.

5. SUBAGENT_SPAWN (agent parent → sous-agent)
   Parent ──[⚡ chain]──> SubAgent
   Animation: lien persistant (cordon électrique pixelisé) entre parent et enfant,
   visible tant que le sous-agent est ACTIF. Icône 🔗 en haut-gauche du sprite enfant.

6. CROSS_TEAM_COLLAB (collaboration informelle inter-teams)
   Agent A ──[💬 walk]──> Couloir ──[💬 walk]──> Agent B
   Animation: les deux agents marchent jusqu'au couloir, se font face, bulles flottantes.
   Durée : 5–30s selon longueur du message. Retour automatique walk_back.
   Si Agent B est BUSY : message ASYNC_NOTE déposé (icône post-it ⬛ sur bureau de B).
```

**Règles de simultanéité et throttle visuel :**

Quand de nombreux messages sont émis simultanément (ex: BROADCAST vers 8 agents en même temps), le rendu serait illisible sans throttle :

| Nb messages simultanés | Stratégie de rendu |
|---|---|
| 1–3 | Toutes les animations jouées en temps réel |
| 4–6 | Animations regroupées : parchemins partent en léger décalé (100ms entre chaque) |
| 7–15 | Mode **burst** : une seule onde concentrique depuis l'émetteur, bulles de réception individuelles (pas d'animation de vol) |
| 16+ | Mode **summary** : icône de broadcast avec compteur `📡 ×N`, pas d'animation individuelle |

Le seuil de throttle est configurable dans les Settings (`display.message_throttle`, défaut : 6).

**File de messages (queue) :**

Si un agent reçoit plusieurs messages en moins de 500ms (ex: cascade d'escalations), ils s'accumulent dans une file visible :
```
📨 Quinn — 3 messages en attente [▼ voir]
```
L'agent traite les messages dans l'ordre FIFO. La file est visible en survolant le badge `📨`.

### 3.6 Salle de challenge — GameFlow

La salle de challenge est une pièce centrale spéciale. Son déroulement est gamifié :

**Phase 1 : Convocation (30s)**
```
Orchestrateur convoque tous les agents
Animation: lumières de la salle qui s'allument, agents qui marchent vers la salle
Kanban board: "In Challenge" affiché
```

**Phase 2 : Présentation (durée variable)**
```
Agent présentateur face à l'écran de présentation
Autres agents: position "audience" (rangées)
Les slides/résultats s'affichent sur l'écran
Animation présentateur: pointer, expliquer, démontrer
```

**Phase 3 : Questions/Critiques**
```
Un agent lève la main (animation) → prend la parole
Bulle de dialogue étendue (max 200 chars)
Types de questions possibles:
  - TECHNICAL_QUESTION (🔧)
  - EDGE_CASE (🕳️)
  - MISSING_FEATURE (📋)
  - SECURITY_CONCERN (🔒)
  - PERFORMANCE_ISSUE (⚡)
  - ALTERNATIVE_APPROACH (💡)
```

**Phase 4 : Vote**
```
Chaque agent vote: ✅ APPROVE / ⚠️ REQUEST CHANGES / ❌ REJECT
Vote affiché comme urne sur l'écran central
Animation: thumb_up / thumb_sideways / thumb_down animé
```

**Phase 5 : Résultat + Itération**
```
APPROVE: confetti animation, carte Kanban → DONE, XP distribué
REQUEST CHANGES: nouvelles cartes créées automatiquement, retour en sprint
REJECT: RCA post-mortem documenté, sprint restart
```

**Règles d'invitation :**

| Mode | Déclencheur | Participants |
|---|---|---|
| AUTO | Sprint complet → toutes les cartes REVIEW | Tous les agents actifs |
| MANUAL | Orchestrateur → bouton [Challenge] HUD | Agents sélectionnés manuellement |
| TASK | Carte Kanban → menu contextuel « Challenge this task » | Owner + agents liés à la tâche |
| PEER | Agent convoque un agent collègue | 2 agents min. + Orchestrateur |

Un agent **absent** (hors ligne, rate-limité ou en pause) reçoit une notification différée :
- Si retour dans les 5 min → intègre la session en cours (phase Critiques ou Vote)
- Sinon → vote `ABSTAIN` automatique (ne bloque pas le résultat, compté dans les stats)

**File de parole (Phase 3) :**
```
[🎤 Prend la parole]
  → Animation hand_raise de l'agent demandeur
  → Icône de main en file sur le HUD latéral
  → 60s de temps de parole max (timer visible)
  → Si timeout → [⏭ SKIP] disponible pour l'Orchestrateur
  → Après parole → prochain en file automatiquement
  → FIFO strict ; ties brisés par ordre alphabétique agent-ID
```

**Annulation de challenge :**

Si l'Orchestrateur clique [✖ Cancel] pendant la phase 1 ou 2 :
```
╔═══════════════════════════════╗
║  ⚠️ Annuler ce challenge ?     ║
║  Les cartes restent en REVIEW. ║
║  [Confirmer]    [Reprendre]    ║
╚═══════════════════════════════╝
```
- Annulé → animation `walk_back` pour tous les agents, room se vide
- Log : `{ type: CHALLENGE_CANCELLED, phase: 1|2, reason: "orchestrator", ts: … }`

### 3.7 War Room — Salle de contrôle de l'Orchestrateur

La War Room est la pièce privée de l'Orchestrateur. C'est un centre de commandement qui comprend :

**Équipements :**
- 3 grands écrans : Vue globale | Agents actifs | Logs système
- Tableau de toutes les rooms (mini-maps)
- Console dédiée avec accès root
- Bibliothèque d'agents disponibles (clonage)
- Interface de création d'agents (formulaire RPG)
- Hotline utilisateur (chat direct)

**Capacités spéciales de l'Orchestrateur depuis la War Room :**
- Déployer un nouvel agent dans une room
- Supprimer/suspendre un agent
- Créer un workflow dynamiquement
- Consulter la mémoire de n'importe quel agent
- Forcer un handoff entre agents
- Observer le web (search) et charger de nouvelles références
- Prompt engineer : réécrire un prompt depuis l'UI
- Override de toute règle système (admin mode)

**Console dédiée (accès root) — Commandes disponibles :**

```
> help                          — Liste toutes les commandes
> agent list                    — Liste agents actifs + état
> agent pause <id>              — Suspend un agent
> agent resume <id>             — Reprend un agent suspendu
> agent restart <id>            — Restart complet (nouveau contexte)
> agent redirect <id> <task>    — Redirige vers une nouvelle tâche
> task create <titre>           — Crée une tâche dans le Kanban
> task move <id> <colonne>      — Déplace une carte manuellement
> workflow run <name>           — Lance un workflow sur l'agent actif
> memory read <agent_id>        — Affiche la mémoire court-terme
> memory clear <agent_id>       — Vide la mémoire court-terme
> broadcast <message>           — Envoie un message à tous les agents
> status                        — Snapshot état global du HQ
> admin unlock                  — Active le mode admin (voir ci-dessous)
```

La console accepte l'autocomplétion (Tab) et conserve un historique des 100 dernières commandes (flèche haut).

**Mode admin override :**

Activé via `> admin unlock` suivi d'une confirmation `CONFIRM` tapée en dur. Autorise :
- Modifier le prompt système d'un agent en cours de session
- Forcer le changement d'état (ex: SLEEPING → WORKING)
- Effacer l'historique d'un agent
- Réinitialiser le score Trust d'une team

Toute action admin est loguée dans `.context/admin-log.jsonl` avec timestamp + action. Pas de mode admin silencieux : un badge `[🔓 ADMIN]` rouge s'affiche dans le header pendant toute la durée du mode.

**Orchestrateur déconnecté / planté :**

- Si le WS de l'Orchestrateur tombe, le HQ entre en **mode dégradé autonome** :
  - Les agents poursuivent leurs tâches en cours normalement (pas de nouveau dispatch).
  - La War Room affiche `[⚠️ Orchestrateur hors ligne — Mode autonome actif]` en rouge pulsant.
  - Le bouton `[💬 Hotline]` reste disponible pour l'utilisateur humain (chat direct avec l'agent le plus disponible).
- Reconnexion : l'Orchestrateur reprend depuis le dernier snapshot (`.context/orchestrator-state.json`), rejoue les événements manquants depuis la queue WS bufferisée.
- Si le crash dure > 10min : alerte persistante + suggestion `[🔄 Restart Orchestrateur]`.

**Hotline utilisateur :**

Bouton `[💬 Hotline]` en bas de la War Room. Ouvre un chat direct avec l'agent disponible le mieux placé pour répondre (sélection automatique par archetype selon le sujet détecté). Si l'Orchestrateur est en ligne, il intercepte le message en premier.

### 3.8 Bibliothèque / Memory Room

Une pièce dédiée à la visualisation des mémoires :

**Structure visuelle de la room :**

```
┌──────────────────────────────────────────────────────────┐
│  📚 BIBLIOTHÈQUE — Memory Room                           │
│                                                          │
│  [Rayons court-terme — 3 étagères, max 9 fiches/étagère] │
│  ████████████████████████████████████   (bois clair)    │
│                                                          │
│  [Archives long-terme — 4 étagères murales hautes]       │
│  ░░░░ Qdrant vectors = livres lumineux ░░░░              │
│  (couleur par type : rouge=code, bleu=doc, vert=test)    │
│                                                          │
│  [Bureau consultation — 1 place]  [Incubateur — 3 pots]  │
│       🪑 (agent si recall actif)      🌱🌿🌳             │
└──────────────────────────────────────────────────────────┘
```

**Zones :**

1. **Rayons mémoire court-terme** : Fiches flottantes représentant les sessions actives. Max 27 fiches visibles (3 étagères × 9). Au-delà, les fiches se superposent avec une opacité réduite (scroll possible en cliquant sur l'étagère).
2. **Archives long-terme** : Livres = vecteurs Qdrant. Couleur : rouge pour le code, bleu pour la documentation, vert pour les tests, jaune pour les notes. Cliquer sur un livre affiche son contenu (extrait JSON/markdown dans une popup).
3. **Bureau de consultation** : Un seul agent peut s'y asseoir. Occupé → badge `🔒 Busy` sur le bureau. Les autres agents attendent à l'entrée.
4. **Incubateur d'idées** : 3 pots de plantes. Stade de croissance visible (🌱 → 🌿 → 🌳) — chaque idée en incubation progresse automatiquement selon le temps écoulé.

**Système de decay / expiration de mémoire :**

| Type | Durée de rétention | Comportement à expiration |
|---|---|---|
| Fiche court-terme (session) | Fin de session (≈ 8h) | Disparaît automatiquement, animation `book_fade` |
| Note opérationnelle | 7 jours | Livre qui jaunit progressivement, puis tombe de l'étagère |
| Vecteur Qdrant (long-terme) | Permanent (sauf éviction manuelle) | Ne disparaît jamais seul — suppression manuelle uniquement |
| Idée incubateur | 14 jours max | Si non récoltée → plante qui se fane et meurt (animation 3f) |

Indicateur de freshness : couleur du livre — vert vif (récent) → jaune (>3j) → orange (>5j) → rouge (expire dans 24h).

**Incubateur — Cycle de vie des idées :**

- **Germination** (🌱) : idée créée (source : agent, incubator task, ou note manuelle). Titre affiché en bulle flottante.
- **Croissance** (🌿) : idée enrichie par au moins un feedback d'agent (commentaire auto ou interaction). Tige visible.
- **Maturité** (🌳) : idée mature après 3+ jours et 2+ feedbacks. Peut être `[🔨 Convertir en tâche]` ou `[📚 Archiver]`.
- **Dépérissement** : si non touchée 14j → animation de fanaison, puis disparition. Log `IDEA_EXPIRED` dans `.context/incubator-log.jsonl`.

**Triggers de visite physique vs recall silencieux :**

| Déclencheur | Type de recall | Animation |
|---|---|---|
| Agent cherche un fichier récemment édité | Silencieux (pas de déplacement) | Badge `📚` 1s sur le sprite |
| Agent a besoin d'une mémoire long-terme (Qdrant) | Visite physique si disponible | `walk_papers` → entre dans la room → `sit_read` → retour |
| Recall pendant une tâche urgente (état DEBUGGING) | Toujours silencieux | Badge `🔍 Recall` 1s |
| L'utilisateur clique sur `[📚 Consulter mémoire]` dans le panel agent | Visite forcée | Agent marche jusqu'à la Bibliothèque |

**Recherche dans la mémoire (interface utilisateur) :**

Clic sur la Bibliothèque → panel latéral `[🔎 Recherche mémoire]` :
```
[Rechercher...                    ] [🔍]
Filtres : [Court-terme ▼] [📅 Aujourd'hui ▼] [Agent: tous ▼]
────────────────────────────────────────────────────
  📄 config.yaml — Amelia — il y a 12min
  📘 auth-design.md — Winston — il y a 2h
  🔴 UserService.ts — Quinn — il y a 1j
```

**Animations de mémoire :**
- Agent → bibliothèque : `walk_papers` → `sit_read` → retourne avec item
- Nouvelle mémoire sauvegardée : livre qui se range dans l'étagère
- Mémoire utilisée : livre qui s'illumine, l'agent l'ouvre et le feuillette
- Vecteurs Qdrant : représentés comme des orbes lumineux dans un espace 3D stylisé
- Livre qui jaunit : animation progressive 1 frame/heure visible (LOD désactivé si zoom < 1×)

### 3.9 Agent Factory — Créer un Agent

L'Agent Factory est représentée comme un **atelier de fabrication** avec :

**Éléments visuels :**
- Forge (pour "forger" le persona)
- Établi (pour configurer les tools)
- Bibliothèque des templates (archetypes RPG : Warrior, Mage, Rogue, Healer...)
- Machine à cloner (animation spectaculaire)
- Terrain d'entraînement (preview de l'agent avant déploiement)

**Processus de création :**
1. Choisir un archetype (ou template existant)
2. Configurer le nom, la description, le background en prose
3. Sélectionner les tools disponibles (drag-drop depuis l'inventaire)
4. Choisir le modèle LLM (menu déroulant stylé)
5. Écrire/choisir le prompt système
6. Assigner la room de naissance
7. **DEPLOY** → animation de "spawn" de l'agent dans sa room

**Terrain d'entraînement — Preview avant déploiement :**

Avant de cliquer sur DEPLOY, l'agent peut être testé dans un sandbox isolé :
- Mini-canvas à droite du formulaire : l'agent reçoit un prompt de test et répond en direct.
- Son état (IDLE, TYPING…) est visible en temps réel.
- Si le prompt système est vide → avertissement `[⚠️ Pas de prompt système — l'agent sera générique]` (non bloquant).

**Clonage d'agent :**

La machine à cloner permet de dupliquer un agent existant :
- Clic droit sur un sprite → `[🔁 Cloner]` → choisir un nouveau nom → DEPLOY.
- La copie hérite du prompt, des tools, du modèle LLM et du routing archetype.
- Elle **ne hérite pas** de l'XP, du niveau, ni de l'historique de session (repart à zéro).
- Cas d'usage : déployer 3 agents DEV identiques pour un sprint parallèle.

**Édition post-déploiement :**

Un agent déployé peut être édité sans le relancer :
- Clic droit → `[⚙️ Configurer]` → formulaire identique à la création, pré-rempli.
- Modifications applicables sans redémarrage : nom, description, tools, team.
- Modifications nécessitant un restart (`[🔄 Appliquer + Restart]`) : prompt système, modèle LLM.

**Suppression / retrait du HQ :**

- `[🗑️ Supprimer]` → dialog de confirmation si l'agent a une tâche active (voir §3.19 R03).
- `[📦 Archiver]` → agent retiré du canvas mais sa config est conservée dans `.context/agents/archived/`. Peut être restauré via `[📂 Restaurer]` dans l'Agent Factory.
- Différence clé : **Supprimer** efface tout. **Archiver** conserve la config mais pas la session.

### 3.10 Desks as Directories — Assignation et Deep Inspection

**Desks as directories :**

- Chaque bureau (`desk_simple`, `desk_dual_screen`, `desk_corner`) peut être assigné à un répertoire de travail : glisser un agent sur le bureau le sédentarise dans ce répertoire.
- Une icône de dossier flotte au-dessus du bureau (`📁 src/server`, couleur distinctive) tant qu’il est assigné.
- Quand le `cwd` de l’agent change, une animation `walk_to_desk` l’envoie automatiquement vers le bureau correspondant.

**Conflits et réservation :**

| Situation | Comportement |
|---|---|
| 2 agents glissés sur le même bureau | Flash rouge 🔴 + bulle « Déjà occupé » — 2e agent reste en suspension |
| Bureau marqué `reserved` | Icône 🔒 sur le bureau ; seul le propriétaire assigné peut s'y asseoir |
| Agent hors connexion > 10 min | Bureau grisé, icône ❓ ; autre agent peut prendre temporairement (`temp_assign`) |
| `temp_assign` + propriétaire de retour | Propriétaire prioritaire : pop-up « Reprendre votre bureau ? » |

**Désassignation :**
```
Drag agent OFF bureau → Drop dans la zone "limbo" (coin de room)
→ Dialog : "Désassigner src/server ?" [Oui] [Non]
   → Oui : icône 📁 disparaît, bureau passe en état libre
   → L'agent reprend l'animation idle_standing en milieu de room
```

Si un agent est désassigné de force (par l'Orchestrateur depuis la War Room) :
- Notification bulle : « Votre bureau a été libéré par l'Orchestrateur. »
- Log : `{ type: DESK_DEASSIGNED, agentId, by: "orchestrator", ts: … }`

**Deep Inspection Panel :**

```
[──────── AGENT: Amelia (DEV) ────────]
 Modèle  : claude-opus-4
 Branche : feat/retro-room
 Tokens  : 42k / 200k   ████░░░░░░
 Outil   : edit_file → src/game/RetroRoom.ts
 Session : 14 outils · 6 fichiers · 2 tests
 [⏸ Pause]  [💬 Chat]  [↩ Redirect]  [🔄 Restart]
```

- Accessible via **clic sur un sprite** → panneau latéral.
- Sources : `AgentConnectionHealth.ts` + transcript JSONL (lu en temps réel).
- Actions disponibles : interrompre, envoyer un message direct, rediriger vers une nouvelle tâche, relancer.

### 3.11 Investigation Lab — Debug à 4 phases

**Objectif** : rendre le débogage systématique visible et jouable.

L'écran du bureau de l'agent passe en mode « Investigation » et affiche un mini-board à 4 colonnes :

```
┌─────────────────────────────────────────────────────┐
│  🔍 Investigation Lab — Amelia (DEV)                │
│  Bug: TypeError: Cannot read properties of undefined │
├──────────┬──────────┬──────────┬────────────────────┤
│ 🔄 ROOT  │ 🔍 PAT.  │ 🧪 HYP.  │  🛠️ IMPL.          │
│  [■■■░]  │  [░░░░]  │  [░░░░]  │  [░░░░]            │
│  In prog │  Pending │  Pending │  Pending           │
└──────────┴──────────┴──────────┴────────────────────┘
  Phase 1/4 — Root Cause Investigation
```

**Red Flags (affichés en War Room sur écran dédié) :**

- `FIX_PROPOSED` émis sans `ROOT_CAUSE_IDENTIFIED` → message d'alerte rouge : ⚠️ *« Root cause not investigated »*
- 3× `FIX_FAILED` consécutifs → alerte orange : *« Architecture Review Required »* + ticket TASK auto-généré
- Temps passé en Ph1 > 20 min → suggestion *« Use root-cause-tracing technique »*

**Iron Law affiché in-world :**

Un poster au mur de la War Room porte l'inscription :
> **⚔️ NO FIX WITHOUT ROOT CAUSE**
> *Evidence before assertions always.*

**Escalade architecture :**

Si `FIX_FAILED` atteint 3×, le `SystematicDebugService.ts` émet un événement WS `ARCHITECTURE_REVIEW_REQUIRED` ; l'Orchestrateur reçoit une notification et crée une carte TASK dans le Kanban avec le label `[🏛️ Arch Review]`.

### 3.12 Parallel Sprint Panel — Dispatch isolé et War Room

**Objectif** : visualiser le dispatch parallèle avec isolation de contexte.

Vue spéciale accessible via bouton `[⚡ Sprint Parallèle]` dans la War Room :

```
┌──────────────────────────────────────────────────────┐
│  ⚡ Parallel Sprint — Orchestrateur dispatche         │
│  Agents actifs : 3 / Domaines isolés : 3              │
├───────────────┬───────────────┬──────────────────────┤
│  Amelia (DEV) │  Quinn (QA)   │  Tea (ARCH)          │
│  feat/auth    │  tests/auth   │  review/api          │
│  🔵 Coding    │  🔍 Testing   │  📐 Reviewing        │
│  Context: ✅  │  Context: ✅  │  Context: ✅         │
│  ──❮tether❯── │  ──❮tether❯── │  ──❮tether❯──       │
│         [Orchestrateur — Monitoring]                  │
└───────────────┴───────────────┴──────────────────────┘
  [🔀 Conflict Check]  [📋 Integration Review]  [✅ Close All]
```

**Principe d'isolation de contexte (visualisé) :**

- Chaque agent reçoit un prompt auto-suffisant — **jamais d'héritage du contexte orchestrateur**.
- Badge `Context: ✅` visible sur chaque agent : vert = prompt isolé reçu, rouge = dépendance détectée.
- Les **tether cords** (lignes colorées) persistent depuis le dispatch jusqu'au retour de tous les agents.

**Conflict Check automatique :**

Avant de fermer les tethers, le `ParallelDispatcher.ts` lance un diff croisé entre les branches. Si un conflit est détecté, l'interface l'affiche :

```
⚠️ Conflit détecté : src/auth/index.ts (Amelia ↔ Quinn)
[Voir diff]  [Assigner arbitre]  [Ignorer]
```

### 3.13 Code Review Room — Révision à deux étapes

**Objectif** : rendre le cycle de revue de code visible et obligatoire.

Chaque tâche terminée déclenche deux sous-agents reviewers avant que la carte Kanban avance :

```
┌─────────────────────────────────────────────────────┐
│  🔍 Code Review Room — Task: AuthService.ts         │
│  Reviewer 1 (Spec) : En cours...                    │
├─────────────┬───────────┬───────────┬───────────────┤
│ Stage 1     │ Spec      │ Quality   │ VERDICT       │
│ (spec)      │ ✅ Conforme│  [░░░░]   │  En attente   │
│ Stage 2     │           │           │               │
│ (quality)   │           │  Pending  │               │
└─────────────┴───────────┴───────────┴───────────────┘
  Findings : 🔴 Critical: 0 · 🟡 Important: 1 · ⚪ Minor: 2
```

**Règles de progression :**

- Stage 1 (Spec Compliance) OBLIGATOIRE avant Stage 2 — l'ordre est invariant.
- `Critical` finding → bloque la progression de la carte, sprite agent passe en état `REVIEWING_BLOCKED` (badge 🔴).
- `Important` finding → l'implémenteur doit corriger + relancer le stage 2 ; carte reste en `IN_REVIEW`.
- `Minor` finding → noté dans le log, n'interrompt pas la progression.

**YAGNI Check automatique :**

Si le reviewer détecte un endpoint/code non appelé dans le codebase, il émet un badge orange `YAGNI` visible sur la carte :

```
⚠️ YAGNI détecté : sendMetrics() n'est jamais appelée. Supprimer ?
[Oui — Supprimer]  [Non — Conserver]
```

**Principe d'intégrité technique :**

Le reviewer ne fait jamais d'accord performatif (« You're absolutely right! » est interdit en dur). Il vérifie, renvoie un pushback technique si nécessaire, et engage un Technical Reasoning quand il remet en cause un choix.

### 3.14 Security Audit Room — CSO in-game

**Objectif** : intégrer la sécurité comme mécanique de jeu visible, pas comme effet secondaire.

Salle dédiée dans le HQ (icône 🔒, couleur rouge sombre). Déclenchable via :
- Bouton `[🔒 Audit sécu]` dans la War Room
- Commande gstack `/cso`
- Automatiquement avant chaque `/ship`

```
┌─────────────────────────────────────────────────────┐
│  🔒 Security Audit — Chief Security Officer         │
│  OWASP Top 10 · STRIDE · Confidence ≥ 8/10          │
├───────────────────────────┬────────────────────────┤
│ OWASP Coverage            │ STRIDE Threats         │
│ A01 Accès : ✅             │ Spoofing     : ✅      │
│ A02 Crypto : ⚠️            │ Tampering    : ✅      │
│ A03 Injection : ✅         │ Repudiation  : ❌      │
│ A04 Insecure Design : ✅   │ Info Disclos.: ⚠️      │
│ ...                       │ DoS          : ✅      │
│                           │ Elevation    : ✅      │
└───────────────────────────┴────────────────────────┘
  Findings : 🔴 CRITICAL: 0 · HIGH: 1 · MEDIUM: 2 · ℹ️ INFO: 3
```

**Zero-noise filter :**

17 catégories de faux positifs sont exclues par défaut (ex : HTTPS uniquement local, localStorage pour données non-sensibles). Aucun finding n'est publié sous le seuil de confiance 8/10.

**Exploit scenario requis :**

Chaque finding inclut un paragraphe *« Comment un attaquant pourrait exploiter ceci »* — visible dans le panneau de détail.

**Intégration Kanban :**

Chaque finding crée automatiquement une carte `[🔒 Sécu]` dans la colonne Backlog, avec priorité selon sévérité. CRITICAL bloque le `/ship` jusqu'au merge de la carte de correction.

---

### 3.15 Teams dynamiques — Création à la volée

**Objectif** : ne pas contraindre l'utilisateur aux 3 teams prédéfinies (DEV / QA / PM). Le HQ s'adapte à n'importe quelle composition d'équipe réelle.

**Formulaire de création (War Room → bouton `[+ Team]`) :**

```
┌─────────────────────────────────┐
│  Nouvelle Team                  │
│  Nom     : [DESIGN            ] │
│  Couleur : [ 🎨 Magenta ▼    ] │
│  Type    : [ Openspace ▼     ] │
│  Icône   : [ 🎨 ▼            ] │
│  Agents  : [ Sélectionner... ] │
│  [Créer]  [Annuler]            │
└─────────────────────────────────┘
```

**Types de rooms disponibles** :

| Type | Disposition | Usage typique |
|---|---|---|
| Openspace | Grid de bureaux libre | DEV, QA, DESIGN, RESEARCH |
| Boardroom | Table centrale + écran | PM, ARCH, stratégie |
| Lab | Établis + équipements | DATA, SECURITY, INFRA |
| Studio | Grands écrans + tablettes | DESIGN, UX, CONTENT |

**Contraintes de layout** :

- Maximum **8 teams** simultanément dans le HQ (limite d'affichage canvas).
- Au-delà, les rooms excédentaires sont compressées dans une zone `[+N autres]` en minimap.
- Une room vide reste dans le HQ avec effet visuel : poussière qui tombe, lumières éteintes, plante fanée.

**Actions de gestion (clic droit sur la room title dans la minimap) :**

- Renommer · Recolorer · Changer de type · Dissoudre (agents renvoyés dans le couloir)
- Fusionner deux teams (drag-and-drop d'une room sur une autre → confirmation)

**Agents "sans team"** : placés dans le **Couloir Principal** comme freelances flottants. Icône `🚶 Freelance` au-dessus de leur sprite. Peuvent être recrutés en glissant-déposant sur n'importe quelle room.

---

### 3.16 Team Routing Rules — Assignation automatique par archetype

**Objectif** : éviter la configuration manuelle pour chaque agent — le système propose un placement par défaut intelligent basé sur l'archetype BMAD.

**Table de routing par défaut :**

| Archetype BMAD | Team par défaut | Override possible |
|---|---|---|
| `dev` | Team DEV (ou première team Openspace) | ✅ |
| `qa` | Team QA (ou première team Lab) | ✅ |
| `pm` | Team PM (ou première team Boardroom) | ✅ |
| `architect` | Team PM ou Team DEV (configurable) | ✅ |
| `ux-designer` | Team DESIGN (créée auto si absente) | ✅ |
| `analyst` | Team PM | ✅ |
| `tech-writer` | Team PM ou Team DEV | ✅ |
| `sm` | Team PM (flotte entre toutes) | ✅ |
| `orchestrator` | War Room (exclusif) | ❌ |
| Custom (aucun archetype BMAD) | Couloir Principal (freelance) | ✅ |

**Règles de résolution en cas d'ambiguïté :**

1. Si la team par défaut n'existe pas → créer automatiquement avec un avertissement `[⚠️ Team auto-créée : DEV]` en War Room.
2. Si l'agent a **deux archetypes** (ex: dev + qa) → team principale selon le premier archetype listé, badge secondaire `[+QA]` visible sur le sprite.
3. Override manuel : drag agent → room → confirmation → `routing_override: true` mémorisé par agent.

**Routing rule editor** (War Room → onglet `Routing`) :

```
[Archetype: dev       ] → [Team: DEV      ▼]  [✏️ Modifier]
[Archetype: qa        ] → [Team: QA       ▼]  [✏️ Modifier]
[Archetype: ux-designer]→ [Team: DESIGN   ▼]  [✏️ Modifier]
[Archetype: graphiste ] → [Team: DESIGN   ▼]  [✏️ Modifier]  ← custom archetype
```

Tous les archetypes custom (non-BMAD) apparaissent dans cette table et peuvent être routés vers n'importe quelle team.

---

### 3.17 Cross-Team Workflows — Flux inter-équipes visualisé

**Objectif** : rendre visible le voyage d'une tâche de DEV → QA → PM (ou tout autre pipeline inter-teams).

**Animation inter-rooms :**

Quand une tâche passe d'un agent (Team A) à un agent (Team B), l'animation de HANDOFF emprunte le **Couloir Principal** :

```
[Team DEV] ──[parchemin traverse couloir]──> [Team QA]
              Agent Amelia                    Agent Quinn
              (sort de l'openspace,           (reçoit au seuil
               marche jusqu'au couloir)        de sa room)
```

- L'agent émetteur joue `walk_to_hallway` → `handoff_throw`
- Le parchemin traverse physiquement le couloir avec une courbe pixelisée
- L'agent receveur joue `walk_to_hallway` → `handoff_catch` → `walk_back`
- Si le receveur est `SLEEPING` ou `BUSY` → le parchemin reste **en attente dans le couloir** (icône ⏳ au sol)

**Pipeline visualizer (War Room) :**

Bouton `[🔀 Pipelines]` ouvre une vue de flux inter-teams :

```
┌─────────────────────────────────────────────────────────────┐
│  Cross-Team Pipeline — feat/auth                            │
│                                                             │
│  [Team DEV]──────▶[Team QA]──────▶[Team PM]               │
│   Amelia ✅        Quinn ⏳          Bob ○                  │
│   INT-042 DONE     INT-042 IN TEST   INT-042 PENDING        │
│                                                             │
│  Temps total : 2h14m  │  Goulot : Team QA (+45min)         │
│  [Voir détail]  [Accélérer QA]  [Notifier PM]              │
└─────────────────────────────────────────────────────────────┘
```

**Review Gate inter-team :**

Si une tâche arrive dans une team et qu'aucun agent n'est disponible, elle entre en **Transit Hold** :
- Icône de parchemin suspendu dans le couloir
- Compteur de temps d'attente visible
- Après seuil configurable (défaut : 15min) → escalade automatique vers War Room

**Mémorisation du pipeline :**

Chaque tâche conserve un `pipeline_trace` :
```json
{
  "task_id": "INT-042",
  "hops": [
    {"team": "DEV", "agent": "Amelia", "duration_s": 3240, "status": "DONE"},
    {"team": "QA",  "agent": "Quinn",  "duration_s": 2700, "status": "IN_TEST"},
    {"team": "PM",  "agent": "Bob",    "duration_s": null,  "status": "PENDING"}
  ]
}
```

Utilisable pour l'export de logs et l'analyse de bottlenecks dans la Retro Room.

---

### 3.18 Team Stats Panel — Métriques par équipe

**Accès** : dropdown `[Team▼]` dans le header → sélectionner une team → icône 📊 → panel latéral filtré.

```
┌──────────────────────────────────────────────┐
│  📊 Stats — Team DEV                         │
│  Agents actifs : 3/4  │  Streak : 7j 🔥     │
├──────────────────────────────────────────────┤
│  Tâches (24h)         │     12 terminées     │
│  Tâches en cours      │      4               │
│  Bugs injectés/repo   │      2               │
│  Avg time/task        │      7m48s           │
│  Trust Score          │     91/100           │
│  XP collectif         │   3 840 XP           │
├──────────────────────────────────────────────┤
│  Top performer : Amelia — 6 tâches           │
│  Agent slow    : Winston — 1 tâche (bloqué)  │
├──────────────────────────────────────────────┤
│  Cross-team flux sortant  : DEV → QA : 14   │
│  Cross-team flux entrant  : PM → DEV :  3   │
│  Goulot actif             : QA (+23min avg)  │
└──────────────────────────────────────────────┘
```

**Comparaison inter-teams** (War Room uniquement) :

Bouton `[⚖️ Compare Teams]` affiche un tableau comparatif de toutes les teams actives :

```
| Team    | Agents | Tasks/24h | Bugs/inj | Trust | Goulot? |
| DEV     |  3/4   |    12     |    2     |  91   |   Non   |
| QA      |  2/2   |     8     |    0     |  95   | ⚠️ Oui  |
| DESIGN  |  1/1   |     3     |    0     |  88   |   Non   |
```

Badge `⚠️ Goulot` automatique si une team a un `avg_wait_incoming > 20min` sur les 2 dernières heures.

**Persistance** : snapshots JSON dans `.context/team-stats/YYYY-MM-DD-{team}.json`, même format que les retros.

---

### 3.19 Team System — Risques et gardes-fous

Cette section documente les edge cases identifiés du système de teams et la stratégie de mitigation pour chacun. Principe directeur : **aucune action destructive ne doit pouvoir se produire silencieusement**.

---

#### R01 — Race condition : agent spawné avant que sa team existe

**Problème** : un agent est instancié (ex: au démarrage du HQ) avant que le routing ait chargé les teams depuis la config. L'agent n'a nulle part où aller.

**Garde-fou** :
- Le `TeamRoutingService.ts` est **bloquant au boot** : aucun agent ne spawne avant que le registre de teams soit prêt (`teams_ready` event WS).
- Si le fichier de config est corrompu ou absent → toutes les teams sont recréées depuis les defaults (DEV/QA/PM) et une alerte `[⚠️ Config teams réinitialisée]` s'affiche en War Room.
- Queue de spawn : les agents en attente s'accumulent dans une file `PENDING_ASSIGNMENT` (visible en War Room) et sont placés dès que la team cible est disponible.

---

#### R02 — Deux agents avec le même archetype, une seule team cible disponible

**Problème** : DEV1 et DEV2 ont tous deux `archetype: dev`, la team DEV n'a qu'un bureau libre. Le second agent est routé en freelance sans notification.

**Garde-fou** :
- Rooms à **capacité extensible** : les bureaux (`desk_simple`) sont ajoutés automatiquement si une room est pleine, dans la limite de 8 bureaux par room (contrainte visuelle canvas).
- Au-delà de 8 → proposition automatique : `[⚠️ Team DEV pleine. Créer une Team DEV-2 ?]` avec bouton `[Oui]` / `[Assigner en freelance]`.
- Aucun agent ne va silencieusement en freelance : tout routing fallback génère une notification War Room horodatée.

---

#### R03 — Dissolution d'une room avec agents actifs

**Problème** : l'utilisateur clique sur "Dissoudre" alors que 3 agents sont en plein `WORKING`. Leurs tâches sont en cours. Résultat potentiel : tâches corrompues, états incohérents.

**Garde-fou** — protocole obligatoire en 3 étapes :

```
┌──────────────────────────────────────────────────────────┐
│  ⚠️ Dissoudre "Team QA" ?                                │
│                                                          │
│  2 agents actifs détectés :                              │
│    • Quinn (QA)   — tâche INT-042 en cours [45%]         │
│    • Murat (TEA)  — tâche INT-038 en cours [80%]         │
│                                                          │
│  Que faire des tâches en cours ?                         │
│  ○ Suspendre et migrer vers [Couloir ▼]                  │
│  ○ Attendre la fin (estimé : ~12min)                     │
│  ○ Forcer l'arrêt (perte de progression) ← déconseillé  │
│                                                          │
│  Que faire des agents ?                                  │
│  ○ Déplacer vers [Team DEV ▼]                            │
│  ○ Placer en Freelance (Couloir)                         │
│                                                          │
│  [Confirmer]  [Annuler]                                  │
└──────────────────────────────────────────────────────────┘
```

- Option "Forcer l'arrêt" est désactivée par défaut (unlock via setting `advanced.allow_force_dissolve`).
- Après dissolution : snapshot de l'état de chaque tâche sauvegardé dans `.context/team-dissolve/{team}-{timestamp}.json`.

---

#### R04 — Merge de deux teams : conflits de Kanban

**Problème** : Team DEV (12 cartes) + Team DEV-2 (7 cartes) fusionnent. Colonnes dupliquées ? Ordre d'affichage ? Cartes assignées à des agents de l'autre board ?

**Garde-fou** :
- Fusion = **union de toutes les cartes** dans un board unique, triées par date de création.
- Colonnes identiques → fusionnées. Colonnes spécifiques à une team → conservées avec tag `[Ex-DEV-2]`.
- Cartes avec agent assigné : l'assignation est conservée. L'agent reste dans la nouvelle team fusionnée.
- Aperçu du board résultant proposé **avant** confirmation :

```
[Prévisualisation — Board fusionné : 19 cartes]
  BACKLOG: 8 cartes  ·  TODO: 3  ·  IN PROGRESS: 4  ·  REVIEW: 2  ·  DONE: 2
  [Voir toutes]  [Confirmer la fusion]  [Annuler]
```

---

#### R05 — Cross-team HANDOFF vers un agent rate-limited ou SLEEPING

**Problème** : le parchemin est lancé vers Quinn (Team QA) mais Quinn est bloqué en rate-limit. Le parchemin reste en attente indéfiniment dans le couloir.

**Garde-fou** :
- Timeout configurable (défaut : **15 min**) sur tout parchemin en Transit Hold.
- À l'expiration : escalade automatique → War Room reçoit `HANDOFF_TIMEOUT` + options :

```
⏰ Parchemin INT-042 en attente depuis 15min (cible : Quinn / QA)
[Rediriger vers Murat]  [Attendre encore 15min]  [Reprendre par DEV]
```

- L'Orchestrateur peut **pré-router** : si l'agent cible est détecté `SLEEPING` ou `RATE_LIMITED` avant l'envoi, le `CrossTeamHandoffService.ts` propose automatiquement un agent alternatif dans la même team.
- Parchemin toujours visible dans le couloir (icône ⏳ + compteur temps d'attente) — jamais silencieux.

---

#### R06 — Limite de 8 teams dépassée

**Problème** : l'utilisateur tente de créer une 9ème team. Le layout canvas est prévu pour 8 maximum.

**Garde-fou** :
- Bouton `[+ Team]` devient grisé dès la 8ème team avec tooltip `Limite atteinte (8/8)`.
- Alternative proposée : `[Fusionner deux teams existantes]` ou `[Archiver une team inactive]`.
- **Archive** : une team archivée disparaît du canvas mais ses données (agents, tâches, stats) sont conservées dans `.context/teams/archived/`. Recall possible via `[📦 Restaurer]` en War Room.

---

#### R07 — Agent hybride / archetype ambigu

**Problème** : un agent déclaré `archetype: dev+qa` (ou sans archetype) génère un badge secondaire `[+QA]` peu visible. L'utilisateur ne sait pas qui gère réellement le QA.

**Garde-fou** :
- Badge secondaire affiché **en couleur contrastante** sur le sprite (pas en overlay grisé).
- Deep Inspection Panel expose clairement :
  ```
  Archetype principal : dev  →  Team : DEV
  Archetype secondaire: qa   →  (override: aucun)
  Capacité QA : ✅ disponible si Team QA déléguée
  ```
- En War Room → vue `[Capacités]` : tableau croisé agents × archetypes pour identifier les "ressources cachées" d'une team.
- Notification si une team n'a aucun agent avec la capacité requise pour une tâche entrante : `[⚠️ Aucun agent QA dans Team DESIGN — tâche de test non couverte]`.

---

#### R08 — Agent freelance oublié dans le couloir

**Problème** : un agent est laissé en freelance indéfiniment. Pas de tâche, XP à 0, visuellement isolé. Risque de "ressource gaspillée".

**Garde-fou** :
- Après **30 min** sans tâche → badge orange `🚶 Idle` clignotant sur le sprite freelance.
- Après **2h** → notification War Room : `[ℹ️ Amelia est sans team depuis 2h — Assigner ?]`.
- Après **24h** → l'agent passe en état `DORMANT` (sprite assis au sol dans le couloir, lumière réduite) et apparaît dans la liste `Ressources non utilisées` du dashboard.
- Raccourci War Room : bouton `[🚶 Freelances (N)]` — liste tous les agents sans team, avec action d'assignation rapide.

---

#### R09 — Communication cross-team non-tâche (agents qui "discutent" sans transfert)

**Problème** : deux agents de teams différentes collaborant sur un sujet commun n'ont pas de mécanique de communication directe (hors HANDOFF de tâche).

**Solution** :
- Nouveau type de message : `CROSS_TEAM_COLLAB`
  - Agent A quitte sa room, marche jusqu'au couloir (`walk_to_hallway`).
  - Si Agent B est disponible : Agent B marche aussi jusqu'au couloir (`walk_to_hallway`).
  - Les deux agents se font face dans le couloir, bulles de dialogue flottantes.
  - Durée visuelle : 5–30s. Retour automatique (`walk_back`) après échange.
  - Log dans les deux historiques agents.
- Si Agent B est BUSY → message `ASYNC_NOTE` déposé (icône post-it ⬛ sur le bureau de B).

---

#### R10 — Inégalité perçue entre teams (classement War Room)

**Problème** : le tableau comparatif inter-teams (§3.18) peut créer une dynamique de "team star vs. team lente" décourageante si l'utilisateur l'utilise comme classement.

**Garde-fou de design** :
- Le tableau comparatif affiche **contexte et charge**, pas seulement le volume :
  - Colonne `Complexité avg` (tâches simples vs. complexes) pour relativiser les chiffres.
  - Colonne `Charge entrante` (flux reçus de l'externe) — une team QA lente l'est peut-être parce qu'elle reçoit trop.
- Pas de "classement" avec rang numéroté — seulement des indicateurs factuels.
- Badge `⚠️ Goulot` pointe vers la **cause** (flux entrant élevé, manque d'effectifs) pas vers la "faute" de la team.
- Suggestion automatique si déséquilibre détecté : `[ℹ️ Team QA débordée — Ajouter un agent QA ou réduire le flux entrant DEV]`.

---

#### Tableau de synthèse

| # | Risque | Gravité | Stratégie | Service concerné |
|---|---|---|---|---|
| R01 | Spawn avant team prête | 🔴 Critique | Queue PENDING_ASSIGNMENT + boot bloquant | `TeamRoutingService.ts` |
| R02 | Room pleine → freelance silencieux | 🟡 Élevé | Extension auto + notification obligatoire | `TeamCapacityService.ts` |
| R03 | Dissolution avec agents actifs | 🔴 Critique | Dialog 3-étapes + snapshot avant action | `TeamLifecycleService.ts` |
| R04 | Merge Kanban conflicting | 🟡 Élevé | Preview + union ordonnée | `KanbanMergeService.ts` |
| R05 | HANDOFF vers agent indisponible | 🟡 Élevé | Timeout 15min + escalade + pré-routing | `CrossTeamHandoffService.ts` |
| R06 | Limite 8 teams dépassée | 🟢 Moyen | Guard hard + archive | `TeamLayoutService.ts` |
| R07 | Agent hybride invisible | 🟢 Moyen | Badge contrastant + vue Capacités War Room | `AgentCapabilityService.ts` |
| R08 | Freelance oublié | 🟢 Moyen | Idle timer 30min → 2h → 24h + alerte | `FreelanceMonitorService.ts` |
| R09 | Pas de communication cross-team non-tâche | 🟢 Moyen | `CROSS_TEAM_COLLAB` + async note | `CrossTeamCollab.ts` |
| R10 | Inégalité perçue par classement | 🔵 Design | Contexte + charge + pas de rang | UX/Dashboard |

---

## 4. UX / Interactions utilisateur

### 4.1 Navigation principale

```
LAYOUT GÉNÉRAL:
┌──────────────────────────────────────────────────────────┐
│  [🔭 Grimoire HQ]  [Team▼] [⚙️] [📊] [🎨 Déco] [🎮] [📡 Obs]  │ ← Header
├─────────────────────────────────────────────┤
│                                             │
│              CANVAS 2D PRINCIPAL            │ ← Terrain de jeu
│          (scrollable, zoomable)             │
│                                             │
├───────────────┬─────────────────────────────┤
│  MINI-MAP     │  STATUS BAR                 │ ← HUD
│  [.......]    │  Agents: 8 | Tasks: 12/3    │
└───────────────┴─────────────────────────────┘
┌─────────────────────────────────────────────┐
│  ████████████████████████████ TIMELINE BAR  │ ← Playback
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐ [mode spectateur uniquement]
│  ★ Mode spectateur — vue lecture seule  ✕   │ ← Bannière (si token spectateur)
└─────────────────────────────────────────────┘
```

**Mécanique TIMELINE BAR :**

La TIMELINE BAR est une barre de lecture chronologique en bas du canvas.

- **Mode par défaut — Live-follow** : la tête de lecture est toujours au présent (⊢ fin du buffer). Le curseur se déplace automatiquement en temps réel.
- **Pause/Scrub** : clic sur la barre ou touche `Space` gele la tête de lecture. L'utilisateur glisse le curseur vers la gauche pour revenir dans l'historique des événements (buffer max 2h local, persisté en SQLite via `workflow_runs.history`).
- **Replay** : les agents sont restitués dans leur état passé (lecture des snapshots depuis la DB). Les événements futurs sont gelés.
- **Retour au live** : bouton `[▶ Live]` qui repositionne le curseur au présent et reprend le flux WS.
- **Plage sélectionnée** : shift+clic pour sélectionner un intervalle — utilisable pour exporter les logs de la période.

Visuel : fond gris foncé, barres colorées par room, tête de lecture rouge, marqueurs d'événements (spawn, challenge, erreur) visibles comme points.

**Navigation clavier :**

| Touche | Action |
|---|---|
| `←` / `→` | Sauter au marqueur précédent / suivant |
| `Ctrl+←` / `Ctrl+→` | Reculer / avancer de 5 minutes |
| `Space` | Play / Pause replay |
| `Home` / `End` | Début / fin du buffer |
| `Échap` | Quitter le mode replay (retour au temps réel) |

**Annotations :**

Clic sur la timeline (hors replay) → champ inline :
```
[📝 Note] Sprint planning repoussé → impact sur §4 ___
```
- Sauvegardé dans `.context/timeline-annotations.json` (`{ ts, text, author }`)
- Affiché comme drapeau jaune 🚩 sur la timeline ; survol = tooltip du texte
- Exportable avec le reste des logs via la Plage sélectionnée (§4.1)

**Buffer plein (session > 2h) :**
```
Timeline buffer = 2h glissantes (rolling window)
Si session > 2h :
  - Entrées > 2h archivées dans .context/timeline-archive/{yyyymmdd}.json
  - Alerte à T=1h50 : "⚠️ Buffer proche de sa limite (10 min). Archivage auto dans 10 min."
  - Replay d'un événement archivé : bannière "📂 Archive — données chargées depuis disque"
```

### 4.2 Panel d'information contextuel

Clic gauche sur un agent → Panel droit glisse :
```
┌────────────────────┐
│ 🟢 Amelia DEV      │
│ "Senior Developer" │
├────────────────────┤
│ État: 💻 Coding    │
│ Tâche: INT-042     │
│ Workflow: TDD ●──○ │
│ Tokens: 78%        │
│ Rate: OK           │
├────────────────────┤
│ Mémoire active: 3  │
│ [config.yaml]      │
│ [user_story.md]    │
│ [test_plan.md]     │
├────────────────────┤
│ [Chat] [Config]    │
│ [Pause] [Redirect] │
└────────────────────┘
```

### 4.3 Workflow visualizer (click-to-inspect)

Au clic sur un agent en cours de workflow, la vue bascule vers un overlay de workflow :

```
WORKFLOW: TDD Red-Green-Refactor
══════════════════════════════════════
[Amelia] ──▶ [Write test] ──▶ [Fail] ──▶ [Implement] ──▶ [Pass] ──▶ [Refactor]
                               ▲ YOU ARE HERE
══════════════════════════════════════
Historique:
  14:32 - Quinn (QA) → Amelia: "Test specs ready"
  14:35 - Amelia: Starting RED phase
  14:37 - Amelia: Test runner failed (expected)
══════════════════════════════════════
[Remonter la chaîne] [Voir tous les contributeurs]
```

### 4.4 Mode Décoration — Personnalisation des pièces

Le Mode Décoration permet à l'utilisateur de personnaliser librement chaque pièce du HQ.
Il est accessible depuis le header (bouton `[🎨 Déco]`) ou depuis le menu contextuel
d'une room (clic droit → `Décorer cette pièce`).

**Activation :**

```
┌──────────────────────────────────────────────────────────────────┐
│  🎨 Mode Décoration — Team DEV                       [✕ Quitter] │
├───────────────────────────────────────────────────────────────────┤
│  Les agents continuent à travailler. Les zones protégées         │
│  sont visibles en surbrillance. Drag & drop pour placer.         │
└───────────────────────────────────────────────────────────────────┘
```

Les agents continuent leurs animations et tâches en arrière-plan pendant le mode déco.
Les zones protégées (couloir, agent token zones, doorways) s'affichent en surbrillance
colorée (§3.1-ter).

**Panneau de catalogue (sidebar gauche) :**

```
┌────────────────────────────────┐
│  🎨 Catalogue de décoration    │
├────────────────────────────────┤
│  🔍 [Rechercher...           ] │
├────────────────────────────────┤
│  Filtres :                     │
│  [Lumières] [Plantes] [Confort]│
│  [Perso.team] [Food] [Tech]    │
├────────────────────────────────┤
│  ┌──────┐  ┌──────┐  ┌──────┐ │
│  │ 🪴   │  │ 🛋️   │  │ 🖼️   │ │
│  │Plante│  │ Sofa │  │Cadre │ │
│  └──────┘  └──────┘  └──────┘ │
│  ┌──────┐  ┌──────┐  ┌──────┐ │
│  │ 💡   │  │ 🦆   │  │ 🪑   │ │
│  │Lampe │  │Rubber│  │Pouf  │ │
│  └──────┘  └──────┘  └──────┘ │
├────────────────────────────────┤
│  Items placés : 7 / ∞          │
└────────────────────────────────┘
```

**Flow de placement :**

```
1. Clic sur un item du catalogue
   → apparaît en mode "ghost" (50% opacité) sous le curseur

2. Déplacement sur le canvas
   → visualisation en temps réel des colliders affectés
   → code couleur VERT / ORANGE / ROUGE (§3.1-ter)

3. Clic gauche → confirmer le placement (snap automatique sur la grille 16×16)
   Clic droit  → rotation de l'objet (90° par clic)
   Echap       → annuler

4. Post-placement : vérification BFS en arrière-plan
   → si blocage → retrait automatique + alerte (§3.1-ter)
```

**Interaction sur les objets placés :**

```
Survol        → highlight de l'objet + tooltip (nom + collider type)
Clic gauche   → sélection (poignées de déplacement apparaissent)
Clic droit    → menu contextuel :
                  [↻ Pivoter]
                  [🎨 Changer couleur]
                  [📋 Dupliquer]
                  [🗑️ Supprimer]
Double-clic   → ouvre le panneau de propriétés (couleur, label, animation)
Drag          → déplace l'objet (même validation que le placement initial)
```

**Personnalisation couleur :**

```
┌─── Couleur : plante ──────────────────────┐
│  Pot       [🟫 Terracotta ▼]              │
│  Feuilles  [🟢 Vert standard ▼]           │
│  Fleur     [🌸 Rose doux ▼] (si applicable)│
│  [Appliquer à tous les objets similaires] │
└───────────────────────────────────────────┘
```

Les couleurs sont choisies parmi la palette étendue (§2.5-bis).
Une option `[Couleur de l'équipe]` applique automatiquement la teinte de la team active.

**Modes de placement avancés :**

```
Mode SYMÉTRIQUE   : place en miroir (parfait pour deux plantes de chaque côté d'une porte)
Mode RÉPÉTITION   : répète l'objet en ligne ou en grille avec espacement configurable
Mode ALÉATOIRE    : scatter esthétique (répartit n exemplaires au hasard dans la zone libre)
Mode THÈME        : applique un preset décoratif complet en un clic (voir §4.4-bis)
```

**Presets thématiques (§4.4-bis) :**

```
┌────────────────────────────────────────┐
│  🏷️ Thèmes de room disponibles          │
├────────────────────────────────────────┤
│  🌿 Jungle Office     — plantes partout │
│  ☕  Café cozy         — bois, lampes, mugs│
│  🔬  Lab sombre       — neons, tech      │
│  🎮  Gaming Corner    — consoles retro  │
│  📚  Bibliothèque     — étagères, globe  │
│  🏆  Wall of Fame     — trophées, cadres │
│  🌸  Sakura           — fleurs, pastel  │
│  ⚡  War Room Elite   — metal, écrans    │
└────────────────────────────────────────┘
```

Un thème décore automatiquement la room en plaçant les objets sur les tiles disponibles
(en respectant les zones protégées). Les objets existants sont conservés si compatibles,
déplacés si conflit. Un aperçu fantôme est montré avant confirmation.

**Persistance :**

Toutes les décorations sont sauvegardées dans `.context/room-decorations/{room-id}.json` :

```json
{
  "room_id": "team-dev",
  "theme": "cafe-cozy",
  "objects": [
    { "type": "plant_small", "tile": [5, 3], "rotation": 0, "color_override": null },
    { "type": "mug_red", "tile": [8, 12], "rotation": 0, "color_override": "#D32F2F" },
    { "type": "guirlande_led", "tile": [0, 0], "rotation": 0, "tile_end": [0, 24] }
  ],
  "updated_at": "2026-04-05T10:00:00Z"
}
```

Le fichier est rechargé à chaque démarrage du HQ. Les décorations survivent aux redémarrages
et aux mises à jour des agents.

**Bouton Reset et Undo :**

```
[↩ Annuler] — annule le dernier placement/déplacement (stack undo 20 actions)
[🔄 Reset]  — retire tous les objets déco de la room (confirmation requise)
```

### 4.5 Configuration gamifiée des MCP/Skills

La configuration est présentée comme un **Skill Tree RPG** :

```
         [🌐 Web Search]
              │
         [🔎 DeepWiki]
              │
    ┌─────────┴───────────┐
[🗄️ SQLite]           [📁 Filesystem]
                           │
                    [✏️ File Editor]
                           │
                    [🏗️ Project Context]
```

Chaque nœud du skill tree s'allume quand le MCP/skill est activé. On peut cliquer sur chaque nœud pour configurer ses paramètres (popup modal RPG).

---

## 5. Système de progression et métriques

### 5.1 XP et achievements gamifiés

Les agents gagnent de l'XP visible (barre d'XP sous leur nom) :

| Action | XP |
|---|---|
| Tâche terminée | +100 |
| Challenge passé | +250 |
| Bug zero test | +50 |
| Handoff réussi | +30 |
| Documentation créée | +75 |
| Web research | +20 |
| Security finding détecté | +80 |
| Idea incubateur convertie en tâche | +60 |
| Sprint streak +1 jour | +40 |
| Code review sans Critical finding | +45 |

**Pénalités XP :**

| Événement | XP |
|---|---|
| Challenge REJECT (auteur de la tâche) | -50 |
| 3× FIX_FAILED consécutifs | -30 |
| Tâche expirée (deadline dépassée) | -20 |

**Système de niveaux (Level Up) :**

| Niveau | XP requis | Déblocages |
|---|---|---|
| Lv.1 (Junior) | 0 | Démarrage |
| Lv.2 (Mid) | 500 | Accès challenge presenter |
| Lv.3 (Senior) | 1 500 | Accès vote en challenge |
| Lv.4 (Lead) | 4 000 | Badge Lead visible sur sprite, bonus +10% XP |
| Lv.5 (Principal) | 10 000 | Halo doré permanent, peut mentorer (boost XP voisins +5%) |

Animation `level_up` : flash blanc + particules colorées sur le sprite, popup `[🎉 Amelia passe Lv.3 !]` en War Room, fanfare courte.

**Persistance :**

- XP et niveaux persistés dans `agents.stats.xp` et `agents.stats.level` (SQLite).
- **Entre sessions** : l'XP est cumulatif et ne se remet jamais à zéro — il représente l'historique complet de l'agent.
- **En cas de Restart agent** (réinitialisation du contexte) : l'XP et le niveau sont conservés, seule la session en cours est réinitialisée.

**Utilité concrète de l'XP :**

- Débloque des niveaux et leurs avantages (voir tableau ci-dessus).
- Contribue au **Team Trust Score** : moyenne pondérée des XP de la team, visible dans le dashboard.
- Débloque des Power Card slots supplémentaires : Lv.3+ = 2 Power Cards actives en simultané (défaut : 1).
- Les achievements sont affichés dans le Deep Inspection Panel de l'agent et dans la Retro Room.

**Achievements débloquables :**

| Achievement | Condition | Récompense |
|---|---|---|
| 🏆 "First Deploy" | Premier agent déployé | +100 XP bonus |
| 🔥 "On Fire" | 5 tâches consécutives sans erreur | Badge flamme permanent |
| 🤝 "Team Player" | 10 handoffs réussis | +30 XP/handoff bonus |
| 🐛 "Bug Hunter" | 20 bugs identifiés en challenge | Badge loupe |
| 🧠 "Memory Master" | 100 items en mémoire long-terme | +1 slot mémoire court-terme actif (max passe de 27 à 30 fiches) |
| 🔒 "Guardian" | 5 security findings détectés | Badge bouclier |
| ⚡ "Speed Demon" | 10 tâches en < 5min chacune | Animation sprint sur sprite |
| 🌱 "Gardener" | 3 idées incubateur converties | Plante déco sur bureau |
| 🏛️ "Architect" | 0 Architecture Review Required sur 30j | Couronne architecte |

Les achievements sont **par agent** (non partagés entre agents) et **permanents** (jamais retirés).

### 5.2 Dashboard métriques global

Accessible depuis l'icône 📊 en header :

```
🏢 GRIMOIRE HQ — Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━
Agents actifs   : 8/12
Tâches en cours : 15
Tâches done (24h): 42
Taux de succès  : 94.3%
Temps moyen/task: 8m32s
Trust Score     : 88/100
━━━━━━━━━━━━━━━━━━━━━━━━━━
Top performer: Amelia (DEV) — 14 tasks
Alert: Quinn bloqué depuis 23min
Next challenge: dans 2h
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5.3 Retro Room — Bilan de sprint gamifié

La Retro Room est une pièce dédiée accessible depuis la minimap (icône 📋). Elle s'anime lors
 de l'ouverture manuelle ou automatique en fin de sprint.

**Tweetable summary (ligne d'accroche en tête de room) :**

```
Sprint #N : 47 commits (8 agents), +3.2k LOC, 38% tests, 12 tâches — Streak: 14j 🔥
```

**Éléments visuels :**

```
[Grand écran mural]    ← tweetable summary + métriques générales
[Classement par agent]
  Amelia (DEV): 14 tâches · +1 800 LOC · Focus: api/   ← 🏆 Ship of Sprint
  Quinn  (QA):   8 tâches · +420 LOC  · Focus: tests/
  Winston (ARCH):3 tâches · +280 LOC  · Focus: docs/
[Flamme dorée flottante si streak global ≥ 7j consécutifs]
[Spotlight "🏆 Ship of Sprint" : tâche la plus impactante]
```

**Animations dédiées :**

- `retro_present` quand l'orchestrateur ouvre la session
- `streak_celebrate` pour chaque agent ayant contribué ≥ 5 jours consécutifs
- `react_success` + confetti si test ratio > 80 %
- `react_confused` si fix ratio > 50 % (alerte : trop de bugs cette semaine)

**Persistance :** JSON snapshot dans `.context/retros/AAAA-MM-JJ-N.json` (sources :
`RetroMetricsCollector.ts`). Format compatible avec gstack `/retro` (champ `tweetable`, `metrics`,
`authors`).

**Déclenchement :**

| Mode | Condition |
|---|---|
| AUTO | Toutes les cartes sprint passées DONE **ou** date de fin sprint atteinte |
| MID-SPRINT | Orchestrateur → [Retro rapide] depuis HUD (format court, 3 items max) |
| MANUAL | Orchestrateur → icône 📋 minimap → [Ouvrir Retro] |
| PLANIFIÉ | Cron configurable dans `.context/sprint.json` (`retro_day`, `retro_time`) |

**Format Start / Stop / Continue :**

Chaque agent doit contribuer avant de pouvoir quitter la salle :
```
╔══════════════════════════════════════════════╗
║  📋 Retro — Amelia (DEV)                     ║
║  ┌─ Start ──┐  ┌─ Stop ──┐  ┌─ Continue ─┐  ║
║  │ ________ │  │ _______ │  │ _________  │  ║
║  └──────────┘  └─────────┘  └────────────┘  ║
║  [Valider]                                   ║
╚══════════════════════════════════════════════╝
```
- Saisie libre (~80 chars) ; gstack valide la présence de chaque colonne avant clôture
- Votes : chaque agent peut 👍 (+1 poids) les items des autres avant la clôture
- Items ≥ 3 votes → **action item automatique**

**Action items → Kanban :**
```
Item voté ≥ 3 fois → Dialog "Créer une carte Kanban ?" [Oui] [Non]
  → Oui : carte créée dans TODO avec tag [retro], assignée à l'auteur de l'item
  → Texte de la carte = texte Start/Stop/Continue verbatim
  → Traçabilité : champ retro_ref: AAAA-MM-JJ-N sur la carte
```

### 5.4 Worktree Lab — Branches git comme rooms temporaires

Chaque branche git active génère une **Worktree Room** temporaire accessible depuis la minimap (icône 🌿).

```
[MINIMAP]
  🏢 Main Office       (branche : main)
  🌿 feat/retro-room   (Amelia · 3 commits)
  🌿 fix/ws-reconnect  (Quinn  · en cours)
```

- Room tintée en **vert pâle** (feature branch) ou **rouge pâle** (hotfix).
- **Compteur de commits** + delta LOC affiché sur l’entrée de la room.
- **Écran mural de clôture** avec boutons in-world :

```
[⬆️ Merge]  [🔀 Pull Request]  [🗑️ Discard]  [⏸ Keep]
```

- Animation `merge_celebrate` si merge validé — confetti + flamme collective dans la War Room.
- `GitWorktreeService.ts` gère la création et suppression des Worktree Rooms (via `git worktree add/remove`).

### 5.5 Plugin Power Cards — Augmentations activables

La **Bibliothèque** (§3.8) hébergera un **Skills Shelf** d’augmentations : les plugins Anthropic officiels se présentent comme des **cartes physiques** posées sur une étagère.

```
[🎨 frontend-design]  [🔍 code-review]  [🔒 security-guidance]
  Carte bleue          Carte verte       Carte rouge
  455k installs        212k installs     107k installs
```

**Interactions :**

- Clic sur carte → pop-up de confirmation → activation sur l’agent sélectionné.
- Agent activé : halo de couleur distinctif (bleu / vert / rouge) + icône du plugin en overlay sprite.
- Cas d’usage typiques :
  - `frontend-design` → Sally (UX) avant un livrable UI
  - `code-review` → Quinn (QA) avant chaque push de PR
  - `security-guidance` → activée automatiquement pendant les challenges SECURITY
---

## 6. Sons et feedback audio

| Événement | Son |
|---|---|
| Agent spawn | chime magique court |
| Task completed | ding satisfaisant |
| Error | buzzer discret |
| Meeting starts | cloche réunion |
| Challenge begins | fanfare courte |
| Challenge validate | applaudissements |
| New message | notification discrète |
| Agent walks | pas (pixel sfx) |
| Memory access | papier qui tourne |
| Workflow transition | click mécanique |

*(Tous les sons sont désactivables individuellement)*

**Audio positionnel :**

Chaque son est émis depuis la position de la room ou de l'agent source. Le volume décroît selon la distance par rapport au centre de la vue (fade linéaire, plage 0–400 px).

- Agent dans une room hors vue → son à 10% (présence sonore atténuée)
- Agent directement sous le curseur → son à 100% + relief stéréo léger
- Zoom < 0,75× → audio positionnel désactivé (LOD audio)

**Ambiance par room :**

| Room | Son ambiant |
|---|---|
| DEV | clavier mécanique (loop lent ~40 BPM) |
| QA | souris rapide + ding discret toutes les 10s |
| Bibliothèque | silence + souffle léger d'air conditionné |
| War Room | hum serveur grave + bip radar toutes les 5s |
| Challenge Room | silence tendu (+ musique si challenge actif) |
| Retro Room | ambiance café : murmures, crayon sur tableau |

**Musique thématique :**

| État du jeu | Thème musical |
|---|---|
| Idle (aucun agent actif) | Lo-fi ambiant, 70 BPM |
| Sprint en cours | Lo-fi focus, 90 BPM (progressive) |
| Challenge en cours | Tension électronique, 110 BPM |
| Sprint terminé (succès) | Jingle court + retour lo-fi |
| Erreur critique / REJECT | Stinger discordant (2s) |
| Retro ouverte | Jazz café, 85 BPM |

**Catégories de mute (Settings > Sons) :**
```
☑ Interface  (clics, notifications, transitions)
☑ Ambiance   (sons de rooms, air conditionné)
☑ Musique    (thèmes, jingles)
☑ SFX agents (pas, animations, XP dings)
  [Volume général : ████░░ 70%]
```

**Contrôles caméra :**

| Action | Contrôle |
|---|---|
| Pan (déplacer la vue) | Clic-droit maintenu + glisser |
| Zoom avant/arrière | Molette souris (0,5× à 3×) |
| Zoom clavier | `+` / `-` |
| Recentrer sur un agent | Double-clic sur l’agent |
| Vue globale (dézoom max) | Touche `H` (Home) |
| Follow mode | Clic sur agent, puis touche `F` |

Le facteur de zoom courant est persisté en `localStorage`. En-deà de 0,75×, les animations de détail sont désactivées (LOD).

## 7. Onboarding

### 7.1 Premier démarrage

```
[Écran d'accueil]
"Bienvenue dans Grimoire HQ."
"Vos agents vous attendent."

[Tutoriel interactif - 5 étapes]
1. "Voici votre bureau — le cœur de Grimoire HQ." *(pointeur lumineux sur la salle DEV, agent sélectionné automatiquement)*
2. "Créez votre première tâche sur le Kanban." *(pointeur sur le board Kanban, bouton [+ Tâche] highlight pulsant)*
3. "Assignez-la à un agent par glisser-déposer." *(flèche animée carte → agent)*
4. "Observez : l’agent se met au travail, l’animation change." *(caméra suit auto l’agent, bulle « En cours » apparait)*
5. "Quand la tâche est en Review, lancez une Challenge Session depuis le HUD." *(highlight bouton [Challenge] dans le HUD)*

*(Indicateur de progression en haut : « 1 / 5 »). Un flag `onboarding_done` est posé en `localStorage` après l’étape 5 pour ne plus afficher le tutoriel.*
```

**Reprise si interruption :**

Si l'utilisateur ferme la fenêtre pendant le tutoriel, l'état est persisté :
```json
{ "onboarding_step": 3, "onboarding_done": false }
```
- Au prochain démarrage : bannière « Reprendre là où vous en étiez ? [Reprendre] [Recommencer] [Ignorer] »
- Si [Ignorer] → `onboarding_done: true` posé immédiatement, tutoriel masqué
- [Recommencer] efface `onboarding_step` → repart à 0

**Re-lancement manuel :**
- Menu `Aide > Revoir le tutoriel` → reset `onboarding_done` + `onboarding_step: 0`
- Raccourci : `Ctrl+Shift+?` depuis n'importe quelle vue

**Modules contextuels (premier usage par room) :**

| Déclencheur | Module affiché |
|---|---|
| Premier accès Bibliothèque | « 💡 La Bibliothèque stocke la mémoire de vos agents. Cliquez sur une zone pour explorer. » |
| Première ouverture Agent Factory | « 🏭 Créez un nouvel agent ou clonez-en un existant. Les XP ne sont pas hérités lors du clonage. » |
| Premier challenge lancé | « ⚔️ En Challenge : présentez, questionnez, votez. Les cartes rejetées reviennent en sprint. » |
| Première Retro Room | « 📊 La Retro analyse votre sprint. Chaque agent doit contribuer Start/Stop/Continue avant de partir. » |
| Premier accès Worktree Lab | « 🌿 Chaque branche git est une room temporaire. Mergez ou discardez depuis l'écran mural. » |

Chaque module s'affiche **une seule fois** ; flag individuel en `localStorage` (`tutorial_{roomType}_seen`).

---

---

## 8. Architecture technique des nouvelles fonctionnalités

### 8.1 Services liés aux colliders et à la navigation

```
NavGridService.ts
  - registerObject(obj)      → place SOLID/PASSABLE sur la nav-grid
  - unregisterObject(id)     → libère les tiles, invalide A* cache
  - isWalkable(tile)         → consulte le byte nav-grid
  - isCorridor(tile)         → flag 0x06 (pas de SOLID autorisé)
  - isAgentToken(tile)       → flag 0x04 (zone réservée bureau)
  - recomputeAfterChange()   → BFS depuis chaque agent, vérifie les accès sorties

ColliderRegistry.ts
  - COLLIDER_DB              → dictionnaire type → { w, h, offsetX, offsetY }
  - getFootprint(type, rot)  → retourne les tiles occupées selon la rotation
  - checkConflict(tiles)     → consulte nav-grid, retourne VALID|BLOCKED|SOFT_WARN

DecorPlacementService.ts
  - startGhostMode(type)     → initie le mode fantôme (curseur attaché)
  - validatePosition(tile)   → retourne VALID|BLOCKED|SOFT_WARN + message
  - confirmPlace(tile, rot)  → place l'objet + appelle NavGridService.registerObject
  - undo()                   → dépile la stack undo (max 20)
  - persistRoom(roomId)      → sérialise en .context/room-decorations/{id}.json
```

### 8.2 Cycle de validation anti-blocage

```
Événement : confirmPlace(tile)
│
├─ 1. NavGridService.registerObject(obj)       → met à jour nav-grid
│
├─ 2. CollisionBFSWorker.postMessage(navGrid)  → BFS en web worker (non-bloquant)
│     │
│     └─ onmessage { ok, blocked_agents }:
│           ok=true  → rien à faire
│           ok=false → NavGridService.unregisterObject(obj.id)
│                      + notification ⚠️ (§3.1-ter)
│
└─ 3. Renderer.invalidateCache()              → redessine la room
```

### 8.3 Format de persistence des décorations

Le fichier `.context/room-decorations/{room-id}.json` est validé au chargement
par `DecorationSchema` (Zod). Les champs inconnus sont ignorés (forward-compat).
Si le fichier est corrompu, la room démarre sans décorations + alerte war room.

### 8.4 Performance

- La nav-grid est un `Uint8Array` de `(width × height)` bytes → lecture O(1)
- Le BFS post-placement tourne dans un **Web Worker** → jamais de jank UI
- Les colliders du catalogue sont pré-calculés à l'init (pas de calcul à chaque drag)
- Les sprites décoratifs sont mis en cache dans `_spriteCache` (même pool que pixel-agent)
- La validation fantôme ne lance **pas** de BFS complet — elle consulte seulement
  `ColliderRegistry.checkConflict` (O(footprint tiles), ~4-16 tiles max)

---

*Fin du Game Design Document — Version 1.2*
