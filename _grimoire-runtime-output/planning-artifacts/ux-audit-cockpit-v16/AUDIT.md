# AUDIT heuristique — Cockpit v16

Basé sur les captures QHD 2560×1440 de Mission Board
(`evidence/01-mission-board-qhd.png`) et Cockpit par défaut
(`evidence/02-cockpit-default-qhd.png`) + lecture de
`grimoire-kit/apps/grimoire-game/app/styles.css`.

Grille d'analyse : heuristiques de Nielsen, lois UX (Fitts, Hick, Gestalt),
principes information architecture (IA) et density management.

## Synthèse par sévérité

| Sévérité | # | Problème | Heuristique |
|----------|---|----------|-------------|
| **P0 critique** | 1 | Largeur cappée à 1480 px en QHD | Aesthetic & minimalist |
| **P0 critique** | 2 | Pas de foyer visuel, 10 panneaux équipondérés | Aesthetic / Gestalt figure-ground |
| **P0 critique** | 3 | Kanban 5 colonnes à 180 px min, cartes illisibles | Fitts' law / density |
| **P1 majeur**  | 4 | Hero banner occupe la 1re fold sans valeur pilote | Visibility of system status |
| **P1 majeur**  | 5 | Vocabulaire métaphorique hermétique | Match system ↔ real world |
| **P1 majeur**  | 6 | Nav surface = 14 pills sur 2 lignes | Hick's law / Recognition |
| **P2 important** | 7 | OPS Dossier concurrence le kanban comme 3e colonne | Aesthetic / Focus |
| **P2 important** | 8 | Duplication `mission atlas` (rail) ↔ `rooms` (plaques kanban) | Consistency |
| **P2 important** | 9 | Scroll vertical total ≈ 2700 px pour UNE vue | Efficiency of use |
| **P3 mineur**  | 10 | Aucune action keyboard-first, pas de recherche | Accelerators |

---

## P0-1 — Largeur cappée à 1480 px en QHD

### Évidence

[evidence/01-mission-board-qhd.png](evidence/01-mission-board-qhd.png) :
contenu confiné dans une colonne centrale, ~540 px de noir de chaque côté.

`styles.css:118` :

```css
.shell {
  max-width: 1480px;
}
```

### Diagnostic

Sur 2560 px, `1480 / 2560 = 58%` de la largeur est utilisée. Les 42%
restants sont perdus. Sur un écran FHD 1920 c'est encore ~23% perdus.
Conséquence directe : le kanban et tous les rails sont compressés alors
que l'écran offre largement la place.

### Remède

```css
.shell {
  max-width: min(2200px, 100% - 48px);
  padding-inline: clamp(24px, 3vw, 64px);
}
```

Cap à 2200 px pour éviter les lignes trop longues en ultrawide, mais
respirer jusqu'à la limite naturelle de lecture. Alternative : retirer
totalement le cap sur `mission-board` uniquement.

---

## P0-2 — Pas de foyer visuel, 10 panneaux équipondérés

### Évidence

Mission Board en QHD empile, tous au même poids typographique et au
même contraste :

1. Hero banner `Grimoire Agent OS`
2. Bloc secondaire `Guardrails bloquants`
3. Run selector (3 boutons)
4. Surface picker (6 pills primaires + 8 pills secondaires)
5. Lens filter (3 pills)
6. Mission Atlas (rail gauche, 6 plaques)
7. Causal Command Deck (4 stats)
8. War Room Kanban (5 colonnes)
9. OPS Dossier (rail droit, 5 sections)
10. Branch Finisher + Watchtower + Workshop + Intake Desk + Seance Archive (5 cards)
11. Frise Causale (6 event cards)

### Diagnostic

Violation frontale de l'heuristique 8 Nielsen (Aesthetic & minimalist)
et du principe Gestalt figure-ground : aucun élément n'émerge comme
sujet, tout est fond. Le kanban (théoriquement l'outil principal sur
cette surface) est noyé au milieu d'un sandwich.

L'architecture visuelle est « dashboard à tout voir » ; elle devrait
être « outil de travail + périphérie contextuelle ».

### Remède

Hiérarchie en 3 zones :

- **Chrome minimal** (top bar ~56 px) : surface switcher + run + lens + status global.
- **Workspace dominant** (80% viewport) : le kanban pleine largeur.
- **Inspector contextuel** (side panel droit, toggleable) : OPS dossier, preuves, causalité → s'ouvre au clic sur une carte, Cmd-J pour toggle.

Tout ce qui n'est pas kanban ou inspector descend en « périphérie »
collapsible (Frise causale, Intake/Watchtower, Branch Finisher) avec
preview en petit ruban en bas.

---

## P0-3 — Kanban 5 colonnes 180 px min, cartes illisibles

### Évidence

`styles.css:1162` :

```css
grid-template-columns: repeat(5, minmax(180px, 1fr));
```

Sur la largeur actuelle (~900 px après rail + OPS dossier), 5 colonnes
à 180 px = 900 px pile, aucune marge. Les titres (`Prepare branch
finish decision`) se brisent sur 3 lignes, les pills `sans room · non
assigne` débordent.

### Diagnostic

- Fitts : cibles cliquables trop petites et trop rapprochées.
- Density : nombre de colonnes figé à 5 alors que le nombre réel de
  lanes peut varier et la largeur disponible n'est pas exploitée.

### Remède

```css
.mission-board-main {
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}
```

Et si on libère la largeur (P0-1) + on bascule OPS dossier en side panel
(P0-2), on obtient 5 à 7 colonnes à 280-320 px chacune, cartes
respirables.

---

## P1-4 — Hero banner sans valeur pilote

### Évidence

Premier écran après chargement : 280 px de hauteur occupés par le hero
`Grimoire Agent OS / Local shell centered on the runtime surfaces that
matter first…`. Purement narratif, aucune info actionnable.

### Diagnostic

Premier fold est un écran marketing, pas un outil. Un solo dev qui
pilote des agents en live n'a rien à y faire après la 2e fois.

### Remède

- Supprimer le hero sur toutes les surfaces sauf `home`/landing.
- Remplacer par une top bar fine (56 px) :
  `[logo] [surface switcher icônes] [run picker] [lens] — [status badges] [search] [settings]`.
- Status badges = condensé du bloc `Guardrails bloquants` (3 chips : trust, attribution, merge) cliquables pour scroll-to-issue.

---

## P1-5 — Vocabulaire métaphorique hermétique

### Évidence (termes actuels)

`Live runtime atlas`, `Active surface`, `Pressure snapshot`,
`Mission atlas`, `Causal command deck`, `Branch finisher`, `Watchtower`,
`Seance archive`, `Frise causale`, `OPS dossier`.

### Diagnostic

Violation frontale de l'heuristique 2 Nielsen (Match between system and
real world). Chaque terme demande au lecteur de construire un mapping
métaphore → fonction → contenu. C'est gérable quand on a créé le
vocabulaire, épuisant pour un utilisateur qui revient une semaine plus tard.

### Remède

Table de substitution (suggestion, à arbitrer avec toi) :

| Jargon actuel | Remplacement orienté-tâche |
|---------------|----------------------------|
| Live runtime atlas | Runtime |
| Active surface | (masquer, c'est déjà dans le switcher) |
| Pressure snapshot | Blocages |
| Mission atlas | Rooms (ou supprimer, doublon) |
| Causal command deck | Filtres |
| Branch finisher | Finition branche |
| Watchtower | Dérives |
| Seance archive | Historique |
| Frise causale | Preuves récentes |
| OPS dossier | Détail |

Règle : un seul substantif métier, une seule action.

---

## P1-6 — Nav surface : 14 pills sur 2 lignes

### Évidence

`Primary surfaces` : 6 pills. `Secondary atlas` : 8 pills. 14 cibles
en 2 lignes de ~40 px, tout en texte.

### Diagnostic

Hick's law : temps de décision = `log2(n + 1)`. Pour 14 items texte
identiquement stylés, l'œil scanne linéairement à chaque bascule.

### Remède

Switcher icône unique à gauche (~56 px, 14 icônes verticales ou
groupées 6 + 8), tooltip au survol, Cmd-1..9 raccourci clavier.
Secondary atlas regroupé sous un toggle « Atlas » qui déplie un
mini-panel overlay.

---

## P2-7 — OPS Dossier en 3e colonne permanente

### Évidence

Layout Mission Board : `220px minmax(0,1fr) 360px` → rail gauche,
kanban, OPS dossier. La 3e colonne est toujours visible, même sans
carte sélectionnée.

### Diagnostic

Le kanban est le sujet. Un panneau de détail qui occupe 360 px en
permanence concurrence le sujet pour attirer l'attention. Pire : quand
aucune carte n'est sélectionnée, le panneau affiche le 1er item par
défaut, ce qui crée de la confusion (« pourquoi c'est cette carte-là
qui est mise en avant ? »).

### Remède

Side panel inspector :

- Fermé par défaut si aucune carte n'est cliquée.
- S'ouvre à 400-440 px au clic sur une carte (ou Cmd-J).
- Escape ferme.
- Header du panneau = titre de la carte sélectionnée avec `←/→` pour
  naviguer entre cartes sans le fermer.

---

## P2-8 — Duplication Mission Atlas ↔ Rooms kanban

### Évidence

Mission Atlas (rail gauche) liste : `INTAKE DESK 1`, `WAR ROOM 4`,
`WORKSHOP 1`, `BRANCH FINISHER 3`, `SEANCE ARCHIVE 3`, `WATCHTOWER 13`.
Kanban War Room au centre, et juste en dessous, les 5 autres rooms
s'affichent à nouveau en card grid.

Résultat : chaque room apparaît 2 à 3 fois (rail + card détail + parfois
frise causale).

### Diagnostic

Violation heuristique 4 Consistency. L'utilisateur ne sait pas où est
la vérité canonique : la pastille du rail ? la card ? la frise ?

### Remède

Un seul endroit où une room existe. Option retenue :

- Rail gauche = navigation (clique sur la room → scroll ou switch kanban).
- Cards de room en dessous du kanban = **supprimer** (c'est de la
  duplication).
- Frise causale = stricte ligne temporelle d'événements, pas de
  répétition de rooms.

---

## P2-9 — Scroll vertical ≈ 2700 px

### Évidence

Le fullPage screenshot fait 2700 px de haut en 2560 px de large.
Le ratio hauteur/viewport ≈ 3 → 3 scrolls pour tout voir.

### Diagnostic

Le dashboard est infini. Pas de « above the fold » priorisé, chaque
scroll révèle un nouveau bloc. L'œil abandonne.

### Remède

Fold 1 (100 vh, sans scroll) : top bar + kanban pleine largeur + inspector (à droite, closed par défaut).

Le reste devient un **ruban horizontal** en bas de page, collapsible :
`[Preuves récentes] [Historique] [Dérives] [Finition branche]`.
Chaque onglet s'ouvre à 240-320 px de hauteur max sans pousser le kanban.

---

## P3-10 — Pas de raccourcis clavier, pas de recherche

### Évidence

Aucune search bar, aucun `?` d'aide, aucun raccourci affiché.

### Remède (différable)

- Global search `Cmd-K` (jumps entre surface, task, room, agent).
- `?` pour afficher la palette de raccourcis.
- `Cmd-1..9` pour switcher surface.
- `J/K` pour naviguer dans les cartes du kanban.
- `Cmd-J` pour toggle inspector.

---

## Root cause commune

Les 3 P0 ont la même origine : **le cockpit a été conçu comme une mise en scène narrative** (atlas, pressure, frise) **plutôt qu'un outil de travail**. C'est cohérent pour une démo publique mais contre-productif en usage quotidien.

La refonte consiste à **basculer du mode "dashboard show" au mode "workspace"** : un foyer (le kanban), une périphérie contextuelle (inspector), un chrome discret (top bar), et le reste collapsé.

Wireframes concrets dans [WIREFRAMES.md](WIREFRAMES.md).
