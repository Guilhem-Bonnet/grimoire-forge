---
name: grimoire-pixel-observatory
description: "Développement du Pixel Observatory — game engine, sprites procéduraux, timeline engine. Use when: pixel observatory, game engine, sprite system, office view, agent animation, timeline scrubber, pixel art, gamification, observatory v2."
---

# Pixel Observatory — Skill Grimoire

## Philosophie

Le Pixel Observatory transforme un dashboard analytique en une expérience de jeu vidéo
où les agents sont des personnages pixel art animés dans un bureau virtuel, avec contrôle
temporel (timeline scrubber) et configuration en temps réel.

## Architecture du Game Engine

Tout le code est embarqué dans le HTML généré par `observatory.py` (single-file, zero CDN).
Les sprites sont dessinés procéduralement via Canvas 2D.

### Classes principales

```text
SpriteFactory      → Génération de sprites 16×16 via canvas (cached OffscreenCanvas)
OfficeLayout       → Grille 40×30, zones par équipe, collision map
PathFinder         → A* sur grille avec cache
AgentCharacter     → State machine + animation + position sub-pixel
TimelineEngine     → EventQueue + StateSnapshot + playback controls
Renderer           → requestAnimationFrame loop, camera pan/zoom, layers
InteractionManager → Click/hover/drag/keyboard sur canvas
```

### Conventions sprites

| Taille | Usage |
|---|---|
| 16×16 | Personnages, petits meubles, tiles |
| 32×16 | Desks, grands meubles |
| 32×32 | Whiteboard, décorations |

Tous les sprites sont des tableaux de pixels `[row][col] = colorIndex` :

```javascript
const PALETTE = {
  0: 'transparent',
  1: '#000000',    // outline
  2: skinColor,    // dynamique par agent
  3: shirtColor,   // dynamique par agent
  4: '#4a4a4a',   // pantalon/détails
  5: '#ffffff',    // highlights
};
```

### Animation

- **30 FPS** target (requestAnimationFrame avec delta time)
- Animation frames indexées : `sprites[agentId][state][frameIndex]`
- Frame cycling : `frameIndex = Math.floor(time / frameDuration) % frameCount`
- Interpolation de position pour mouvement fluide

### Timeline Engine

Le timeline est le composant central qui pilote TOUT :

```javascript
class TimelineEngine {
  // Tous les événements triés chronologiquement
  events = [];
  // Index courant dans la file
  currentIndex = 0;
  // Mode : 'playing' | 'paused' | 'seeking' | 'live'
  mode = 'paused';
  // Vitesse de lecture
  speed = 1.0;

  // StateSnapshot : état complet à un instant donné
  // Calculé à partir des événements précédents
  getStateAt(timestamp) → { agents: Map<id, {state, position, lastAction}> }
}
```

### Cross-view sync

Le timeline émet des événements que chaque vue écoute :

```javascript
timeline.on('timeUpdate', (timestamp) => {
  // Chaque vue se met à jour selon le timestamp courant
  officeView.seekTo(timestamp);
  timelineView.highlight(timestamp);
  swimlaneView.moveCursor(timestamp);
  dagView.updateProgress(timestamp);
  networkView.flashEdge(timestamp);
});
```

## Règles de développement

| Règle | Description |
|---|---|
| **Zero dépendances** | Tout en vanilla JS, pas de lib externe |
| **Single-file** | Tout embarqué dans le HTML généré |
| **Procédural** | Sprites canvas, pas de PNG/SVG/base64 |
| **Performance** | 30 FPS avec 20 agents minimum |
| **Pixel-perfect** | `imageSmoothingEnabled = false` |
| **Responsive** | Le canvas s'adapte à la taille de la fenêtre |

## Palette de couleurs agents

Alignée avec le thème existant de l'Observatory :

```javascript
const AGENT_THEME = {
  dev:       { primary: '#3fb950', secondary: '#2ea043', accent: '#56d364' },
  qa:        { primary: '#bc8cff', secondary: '#a371f7', accent: '#d2a8ff' },
  architect: { primary: '#39d2c0', secondary: '#2db7a8', accent: '#56e8d5' },
  pm:        { primary: '#f0883e', secondary: '#d68030', accent: '#f4a261' },
  analyst:   { primary: '#d29922', secondary: '#bf8700', accent: '#e3b341' },
  sm:        { primary: '#f778ba', secondary: '#db61a2', accent: '#ff9bce' },
  techwr:    { primary: '#7ee787', secondary: '#56d364', accent: '#aff5b4' },
  orchestr:  { primary: '#58a6ff', secondary: '#388bfd', accent: '#79c0ff' },
  tea:       { primary: '#f85149', secondary: '#da3633', accent: '#ff7b72' },
};
```

## Checklist qualité

- [ ] Les sprites se génèrent sans erreur console
- [ ] Le game loop tourne à 30+ FPS
- [ ] Le timeline scrubber pilote toutes les vues
- [ ] Le drawer de configuration s'ouvre correctement
- [ ] Le pan/zoom fonctionne au touch et mouse
- [ ] Les animations sont fluides
- [ ] Le mode LIVE met à jour en temps réel
- [ ] Le mode démo fonctionne sans données
