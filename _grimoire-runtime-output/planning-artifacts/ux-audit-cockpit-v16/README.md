# UX Audit — Cockpit v16

Audit heuristique et proposition de refonte du cockpit SPA
(`grimoire-kit/apps/grimoire-game`), vu depuis
`http://127.0.0.1:4174/cockpit/` en résolution QHD 2560×1440.

## Contexte

- **Persona** : toi, solo dev, pilote d'agents Grimoire en live.
- **Surface prioritaire** : Mission Board (Kanban).
- **Écran réel** : QHD 2560×1440.
- **Densité recherchée** : moins d'info par écran, un foyer visuel, focus tâche.
- **Livrable** : audit écrit + wireframes annotés (aucun code applique).

## Corpus

- [AUDIT.md](AUDIT.md) — diagnostic heuristique, 10 problèmes classés par
  priorité avec évidence et diagnostic root-cause.
- [WIREFRAMES.md](WIREFRAMES.md) — deux concepts de refonte annotés (Focus+Periphery, Command Center) avec mapping implémentation.
- `evidence/` — screenshots QHD de Mission Board et Cockpit par défaut.

## TL;DR — 3 verdicts

1. **Le cockpit gaspille 1080 px de large en QHD**
   (`max-width: 1480px` centré sur 2560 px). Sur un kanban, c'est
   le problème dominant : 5 colonnes à 180 px min au lieu de 7 à 280 px.
2. **Tout est au même niveau hiérarchique.** Hero banner,
   run selector, surface picker, lens picker, atlas, kanban, detail dossier,
   frise causale : 7 à 10 blocs équipondérés empilés. Aucun foyer visuel,
   aucun progressive disclosure.
3. **Le vocabulaire est hermétique.** `Live runtime atlas`,
   `causal command deck`, `ops dossier`, `mission atlas`, `frise causale` :
   métaphores internes qui demandent recall plutôt que recognition.

## Top 5 quick wins (si tu veux que je les applique)

| # | Action | Impact | Effort CSS |
|---|--------|--------|------------|
| 1 | Lever le cap `max-width: 1480px` → `min(2200px, 100% - 48px)` | Kanban respire, infos latérales cessent d'empiler | 1 ligne |
| 2 | Kanban `repeat(auto-fit, minmax(280px, 1fr))` au lieu de `5 × 180px` | Cartes lisibles, colonnes adaptatives | 1 ligne |
| 3 | Virer le hero banner de la vue principale (2 tuiles de stats suffisent en top-bar fine) | Récupère la 1re fold entière | 20 lignes |
| 4 | Déplacer `OPS Dossier` en side-panel droite toggleable (Cmd-J) au lieu de 3e colonne permanente | Foyer visuel sur le kanban | 30 lignes |
| 5 | Fusionner `primary surfaces` + `secondary atlas` en une barre unique (switcher icônes) | Hick's law : 14 cibles → 14 icônes, pas 14 pills | 40 lignes |

Détails et wireframes : voir [WIREFRAMES.md](WIREFRAMES.md).

## Décision attendue

Choisir entre :

- **A. Refonte incrémentale** — j'applique les 5 quick wins CSS uniquement. ~1h, pas de toucher à `main.ts`.
- **B. Refonte Concept Focus+Periphery** — CSS + petite couche HTML (top bar, side panel). ~2-3h.
- **C. Refonte Concept Command Center** — CSS + restructuration `main.ts`. ~4-6h, risque tests cockpit.
- **D. Rester sur l'audit, on discute avant de coder.**
