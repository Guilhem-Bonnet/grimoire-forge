# Plan : Pixel Observatory V2 — Implémentation

> Ce plan est destiné à un exécuteur agentic. Chaque étape est autonome
> et contient tout le contexte nécessaire.

## Contexte

Transformer l'Observatory existant (`grimoire-kit/framework/tools/observatory.py`)
en un tableau de bord agentic gamifié avec vue pixel art, timeline scrubber global,
et panneau de configuration agents. Extension du fichier existant (~1960 lignes).

## Phase 1 : Game Engine Core

### Étape 1.1 : Sprite Factory — Génération procédurale

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS du template)
**Action** : Ajouter le système de sprites dans le JavaScript embarqué

Créer la classe `SpriteFactory` qui génère des personnages pixel art 16×16 via canvas :

- Palette de couleurs par agent (vert pour dev, violet pour qa, etc.)
- Frames d'animation : idle (2), walking (4), typing (3), reading (2), speaking (3)
- Sprites de meubles : desk, chair, computer, whiteboard, plant, coffee machine
- Sprites de sol : floor tiles avec variations, wall tiles
- Tous les sprites mis en cache dans des OffscreenCanvas

**Vérification** : Ouvrir l'observatory, vérifier que les sprites se génèrent sans erreur console

### Étape 1.2 : Office Layout Manager

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Ajouter le système de layout de bureau

Créer la classe `OfficeLayout` :

- Grille 40×30 tiles (640×480 base, scalable)
- Zones définies par rôle d'équipe (vision, architecture, dev, ops, central)
- Placement automatique des meubles et agents selon les données
- Auto-layout : le SOG au centre, les équipes groupées par zone
- Collision map pour le pathfinding

**Vérification** : Le layout se génère sans erreur, les zones sont distinctes

### Étape 1.3 : Pathfinder A\*

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Ajouter le pathfinding pour les déplacements des agents

Implémenter A\* sur la grille :

- Prend en compte les murs et meubles comme obstacles
- Retourne un chemin de tiles
- Smoothing simple pour éviter les mouvements en zigzag
- Cache des chemins fréquents (agent → agent)

**Vérification** : Tester que le pathfinding évite les obstacles

### Étape 1.4 : Agent Controller + State Machine

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Ajouter le contrôleur d'agents

Créer la classe `AgentCharacter` :

- State machine : idle → walking → typing/reading/speaking → idle
- Animation player : cycle frames selon état et vitesse
- Position en sous-pixels (float) pour mouvement fluide
- Bulle de dialogue (speech bubble) avec texte court
- Indicateur de trust score (barre au-dessus de la tête)
- Flash rouge sur erreur, confettis sur célébration
- Sélection (anneau lumineux quand cliqué)

**Vérification** : Les agents s'animent correctement dans les différents états

## Phase 2 : Timeline Engine

### Étape 2.1 : EventQueue + StateSnapshot

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Créer le moteur de timeline

Créer la classe `TimelineEngine` :

- Parse toutes les traces et events en tableau trié chronologiquement
- Pour chaque timestamp, calcule un `StateSnapshot` (position de chaque agent, état, action)
- Interpolation entre snapshots pour mouvement fluide
- API : `play()`, `pause()`, `seek(timestamp)`, `setSpeed(mult)`, `nextEvent()`, `prevEvent()`
- Événements : `onEventReached(callback)`, `onTimeUpdate(callback)`

**Vérification** : La timeline parse correctement les données et produit des snapshots

### Étape 2.2 : Timeline UI Bar

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section HTML/CSS/JS)
**Action** : Ajouter la barre de timeline globale en bas de page

Composant UI :

- Boutons : ⏮ ◀ ⏸/▶ ▶ ⏭
- Barre de progression draggable avec curseur
- Heatmap de densité d'événements sur la barre (gradient de couleur)
- Affichage timestamp courant / total
- Sélecteur de vitesse (0.5x, 1x, 2x, 4x)
- Sélecteur de session
- Badge LIVE (mode temps réel)
- Visible sur TOUTES les vues (position: fixed bottom)

**Vérification** : La barre s'affiche correctement, les contrôles répondent

## Phase 3 : Vue Office intégrée

### Étape 3.1 : Nouvel onglet Office dans le template HTML

**Fichier** : `grimoire-kit/framework/tools/observatory.py`
**Action** : Ajouter le tab "🎮 Office" et la structure HTML

- Insérer le tab en position 0 dans la tab bar
- div `view-office` avec un canvas plein écran
- Canals layers : background (sol, murs), furniture, agents, UI overlay
- Contrôles de camera : pan (drag), zoom (scroll wheel)

**Vérification** : L'onglet Office apparaît et affiche un canvas

### Étape 3.2 : Renderer + Camera

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Créer le moteur de rendu

Créer la classe `Renderer` :

- requestAnimationFrame game loop à 30 FPS
- Système de layers : floor → furniture → agents (sorted by Y) → UI
- Camera avec offset (pan) et scale (zoom, min 0.5, max 3.0)
- Pixel-perfect rendering (imageSmoothingEnabled = false)
- Rendu conditionnel (seulement si tab Office actif)
- Minimap en coin (vue réduite de tout le bureau)

**Vérification** : Le canvas affiche le bureau avec pan/zoom fonctionnel

### Étape 3.3 : Interaction Manager

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Ajouter les interactions souris/clavier sur le canvas

- Click agent → sélection (highlight ring) + ouvre Agent Config Panel
- Hover agent → tooltip avec nom, état, trust
- Hover meuble → tooltip avec fonction
- Double-click agent → centrer la caméra dessus
- Drag canvas → pan
- Scroll → zoom
- Keyboard : Space = play/pause, Left/Right = prev/next event
- Touches 1-9 = sélection rapide d'un agent

**Vérification** : Les interactions fonctionnent sans conflit avec les autres vues

## Phase 4 : Agent Configuration

### Étape 4.1 : Agent Config Drawer

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section HTML/CSS/JS)
**Action** : Créer le panneau de configuration

Panneau latéral droit (drawer) qui s'ouvre sur click d'un agent :

- Header : sprite agrandi (64×64) + nom + persona + role
- Status : état courant animé, dernière action, timestamp
- Trust Score : jauge circulaire SVG + valeur numérique
- Tools : liste des capabilities avec toggles visuels (UI only, pas de persistence backend)
- Historique : 10 dernières traces de cet agent (scrollable)
- Relations : mini-graph des agents connectés (canvas mini)
- Config : sliders pour autonomy level, tool restrictions (UI state only)

**Vérification** : Le drawer s'ouvre/ferme correctement, les données sont populées

### Étape 4.2 : Cross-view synchronisation

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Connecter le timeline à toutes les vues

Quand le scrubber change de position :

- Office : les agents se déplacent et changent d'état selon le timestamp
- Timeline : highlight l'événement courant, auto-scroll
- Swimlane : ligne verticale "now" qui se déplace
- DAG : les barres Gantt se remplissent progressivement
- Network : les liens flash quand une interaction est active
- Log : filtre les entrées jusqu'au timestamp courant
- Metrics : recalcul partiel

**Vérification** : Changer la position du scrubber met à jour toutes les vues visibles

## Phase 5 : Polish et effets

### Étape 5.1 : Effets visuels

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Ajouter les effets de jeu

- Particules : confettis sur task_completed, sparks rouges sur error
- Transitions : fade d'entrée des agents quand ils apparaissent
- Bulles de dialogue : animation d'apparition smooth
- Trail : traînée semi-transparente quand un agent marche
- Halo : glow autour de l'agent actif / sélectionné
- Indicateurs flottants : "+Trust", "Handoff →", "Error!"

### Étape 5.2 : Keyboard shortcuts et polish

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Finitions

- Space : play/pause timeline
- Left/Right : événement précédent/suivant
- F : fullscreen sur la vue Office
- M : toggle minimap
- G : toggle grille visible
- H : aide/raccourcis overlay
- Sounds : Web Audio API pour notifications (click léger, notification, error)
- Mode sombre déjà en place (le thème actuel est dark)

### Étape 5.3 : Mode démo

**Fichier** : `grimoire-kit/framework/tools/observatory.py` (section JS)
**Action** : Ajouter un mode démo quand pas de données

Si aucune trace n'est trouvée, générer une simulation :

- 5 agents fictifs qui interagissent
- Scénario : brainstorm → architecture → implementation → QA → deploy
- Permet de tester et démontrer le système

## Phase 6 : Tests

### Étape 6.1 : Tests unitaires Python

**Fichier** : `grimoire-kit/tests/tools/test_observatory.py`
**Action** : Étendre les tests existants

- Test que les nouvelles sections HTML sont générées
- Test que le tab Office est présent dans le HTML
- Test que la timeline bar est présente
- Test que le JS embarqué est syntaxiquement valide

### Étape 6.2 : Tests visuels Playwright

**Action** : Vérifier via navigateur

- L'onglet Office affiche un canvas non vide
- Les agents sont visibles et animés
- La timeline répond aux interactions
- Le drawer de configuration s'ouvre
- Les contrôles de playback fonctionnent

## Résumé des livrables

| Phase | Livrable | Impact |
|---|---|---|
| 1 | Game engine (sprites, layout, pathfinding, agents) | Fondation technique |
| 2 | Timeline engine + UI bar | Contrôle temporel unique |
| 3 | Vue Office + renderer + interactions | Le WOW factor |
| 4 | Agent config drawer + cross-view sync | Valeur utilitaire |
| 5 | Effets visuels, sons, mode démo | Polish jeu vidéo |
| 6 | Tests Python + Playwright | Qualité |
