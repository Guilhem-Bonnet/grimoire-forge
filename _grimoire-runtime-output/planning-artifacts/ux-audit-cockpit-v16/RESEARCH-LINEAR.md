# Research UX — Linear patterns pour Grimoire Cockpit

> Livrable de recherche chirurgicale pour justifier PR 3 (refonte Mission Board + Shell).
> Référence principale : **Linear** (linear.app). Densité cible : Linear/Height.
> Scope prioritaire : Mission Board, puis propagation au shell global.

---

## 1. Canon Linear — patterns extraits (densité maîtrisée)

### 1.1 Échelle typographique

| Usage | Taille | Weight | Letter-spacing | Exemple |
|---|---|---|---|---|
| H1 page title | 20px | 600 | -0.01em | `Inbox`, `Active issues` |
| H2 section | 16px | 600 | 0 | `Filters`, `Branch finisher` |
| H3 colonne/rail | 13px | 600 | 0 | `In progress`, `Backlog` |
| Body | 13px | 400 | 0 | texte principal |
| Meta / subline | 12px | 400 | 0 | `2h ago`, `ENG-123` |
| Caption / chip | 11px | 500 | 0.02em | `HIGH`, `READY` |
| Mono (IDs, hash, seq) | 12px Geist Mono | 500 | 0 | `RUN-20260414` |

**Piège actuel cockpit** : la `eyebrow` (uppercase 11px) + `h2` 18px + `<p class="muted">` 14px → 3 lignes pour dire une chose. Linear utilise au plus 2 lignes (title + 1 meta ligne discrète).

### 1.2 Échelle d'espacement

`4 / 8 / 12 / 16 / 20 / 24 / 32 / 48`

- Padding carte kanban : `12px 14px`
- Gap entre cartes : `6px`
- Gap entre colonnes : `12px`
- Section gap : `20px` (pas 32-40 comme actuellement)
- Row height kanban : `auto` mais max 4 lignes de contenu (title 2 lignes + meta 1 ligne + chips 1 ligne)

### 1.3 Composants canoniques

| Pattern | Linear | Anti-pattern cockpit actuel |
|---|---|---|
| Filtre | Bouton `[+ Filter]` → popover multi-select | 4-6 pills chip-row pleine largeur |
| Display options | Bouton `[Display ▾]` → popover (group by, order by) | Tout hard-codé, toggles absents |
| Tabs de lens | Segmented control 28px haut, 3-5 items max | 3 `.control-button` avec padding 8×16 |
| Scenario/project picker | Dropdown breadcrumb cliquable | 3 boutons `control-button` côte à côte dans topbar |
| Kanban column header | `Status · 12` compact + menu `⋯` discret | Eyebrow + h3 count + meta line (3 éléments) |
| Card kanban | padding 12/14, 2 lignes title, meta ligne, 1-2 chips max | padding 16+, 3 lignes, chip-row 4+ chips |
| Meta-info | Hover card popover (author, dates, links) | Tout étalé inline dans la carte |
| Détail | Inspector drawer right 480px, Escape ferme | Section inline qui repousse le contenu |
| Section repliable | Caret 10px + title + count, défaut fermé sauf primary | Tout ouvert en permanence |
| Actions contextuelles | Context menu droit-clic + Cmd-K global | Aucun accès rapide |
| Navigation verticale | Rail 240px avec items 28px (icon 14 + label 13) | Rail 64px icon-only (OK) mais pas de 2e niveau |

### 1.4 Color tokens Linear (mappés vers Grimoire Forge)

Linear est dark neutral dominant, accent rare.

```
--surface-0  : #0b0c0e   (page)
--surface-1  : #121418   (elevated panel)
--surface-2  : #1a1d22   (card)
--surface-3  : #232830   (hover / popover)
--line       : rgba(255,255,255,0.08)
--line-strong: rgba(255,255,255,0.14)
--ink        : #f6f7f8   (primary text)
--ink-soft   : #9ba0a8   (secondary)
--ink-muted  : #5b6068   (tertiary, placeholder, caption dim)
--accent     : #ff6b3d   (primary action only : focus ring, primary CTA, 1-2 status)
--warning    : #f59e0b
--critical   : #f87171
--positive   : #4ade80
--hover      : rgba(255,255,255,0.04)
--active     : rgba(255,255,255,0.08)
```

**Règle accent** : l'orange sert uniquement à `:focus-visible`, bouton primary unique par vue, et 1 status `critical` si bloqué. Pas sur les actifs de nav (qui utilisent `--ink` sur `--active` background).

### 1.5 Motion & interaction

- Transition standard : `140ms cubic-bezier(0.4, 0, 0.2, 1)` sur `background-color`, `border-color`, `color`, `transform`
- Popover open : `120ms ease-out` avec `scale(0.98 → 1)` et `opacity(0 → 1)`
- Drawer : `200ms cubic-bezier(0.32, 0.72, 0, 1)` sur `translateX(100% → 0)`
- Modal Cmd-K : `140ms` fade-in + `scale(0.96 → 1)`
- Tous respectent `prefers-reduced-motion: reduce` → `transition-duration: 0ms`

---

## 2. Audit chirurgical — cockpit actuel vs Linear

### 2.1 Topbar (shell global)

**Actuel** :
```
[Rail] │ Breadcrumb │ Run: [scenarioA][scenarioB][scenarioC]  │  Lens: [Tout][Attention][Bloques]  │  [OK/Blocage]
```

**Problèmes** :
- 3 boutons scenario + 3 boutons lens + 1 status = 7 éléments cliquables, tous en boutons padding 6×12 → pollution horizontale.
- Le "Run group" est un switch contextuel (un seul actif), donc **dropdown** > chips.
- Le "Lens group" est aussi un switch (un seul actif), donc **segmented control** > chips.
- Pas de Cmd-K visible, pas de notifications, pas d'accès settings.

**Cible Linear** :
```
[Rail] │ Breadcrumb (scenario dropdown) │          │  [⌕ Search ⌘K]  [▤ Display]  [+ Filter]  [● status]
```

- Scenario devient partie du breadcrumb : `Mission Board › Release ready ▾` (clic ouvre dropdown scenarios)
- Lens devient un segmented control **dans la toolbar mission-board**, pas dans le shell topbar global (car c'est contextuel à la surface)
- Topbar shell global ne contient que : breadcrumb, search trigger Cmd-K, status global, avatar/settings (stub)

### 2.2 Mission Board — command bar (dessus du kanban)

**Actuel (L2053-2086)** :
```html
<section class="mission-board-command-bar">
  eyebrow "Vue d ensemble"
  h2 "Release ready / titre scenario"
  p.muted "subtitle long"
  pill tone-X "summary"
  chip-row : [run RUN-XXX] [branch YYY] [filtre Tout] [sans focus]   <-- CHIPS REDONDANTES
  summary-grid : [Flux 12][Blocages 2][Verif 3][Lineage 8]          <-- 4 métriques toujours visibles
</section>
```

**Problèmes** :
- `eyebrow + h2 + p.muted` = 3 niveaux de titre pour la même idée.
- Les 4 chips (run/branch/filtre/focus) dupliquent ce qui est dans la topbar et le statusbar.
- La summary-grid est utile mais prend 96px+ de haut alors que ce sont des stats dérivables.

**Cible Linear** :
```html
<header class="board-header">
  <div class="board-header__title">
    <h1>Missions</h1>                                               <-- 20px semibold
    <span class="meta">12 active · 2 blocked · Release ready</span> <-- 12px ink-soft
  </div>
  <div class="board-header__actions">
    <button class="btn-ghost">[+] New</button>
    <button class="btn-ghost" data-popover="filter">⊕ Filter</button>
    <button class="btn-ghost" data-popover="display">☰ Display</button>
  </div>
</header>
<nav class="board-segmented" role="tablist">
  <button class="seg is-active">All (12)</button>
  <button class="seg">Attention (3)</button>
  <button class="seg">Blocked (2)</button>
</nav>
```

- Un seul h1, un seul meta-line.
- Les 4 métriques (Flux/Blocages/Verif/Lineage) passent dans **hover card** sur le meta-line ou dans le statusbar mono (déjà présent).

### 2.3 Mission Board — rail gauche Rooms

**Actuel (L2057-2085)** :
Chaque room = une card plaque avec :
- eyebrow "Rooms" + h2 titre + p.muted description
- puis pour chaque room : label, count géant, dominantCommand, summary, chip-row de pills

**Problèmes** :
- La rail est déjà à gauche (navigation), donc afficher 5 cards hautes de 100-120px chacune = 500-600px de rail vertical.
- Les pills (dominantCommand, tags) dans chaque card dupliquent ce qui est dans les cartes kanban et les sections du bas.

**Cible Linear** (style sidebar Linear teams) :
```
ROOMS
  ● War Room         12
  ○ Intake Desk       3
  ○ Workshop          4
  ○ Watchtower        1
  ○ Branch Finisher   2
  ○ Seance Archive    0
```

- Row 28px, icône dot 6px tone-coded, label 13px, count 11px mono align right.
- Click scroll-to-section ou filter (selon appState).
- Détails (command, summary, tags) accessibles via **hover card** sur le row.

### 2.4 Kanban cards

**Actuel (L2042-2052)** :
```html
<button class="mission-task-card tone-X">
  <div class="mission-task-card-top">
    <span class="mission-card-kicker">STATUS</span>
    <span class="mission-room-command">sync state replace underscore</span>
  </div>
  <strong>title</strong>
  <p class="mission-task-subline">room · agent</p>
  <p class="mission-task-detail">detail plus long</p>
  <div class="chip-row">pill pill pill pill</div>
</button>
```

**Problèmes** :
- 4 blocs distincts + chip-row = 6 éléments = carte haute de 140-170px.
- "STATUS" en kicker top + tone déjà color-coded = redondance.
- sync state en haut-droite avec casse `replaceAll('_',' ')` = illisible.

**Cible Linear** :
```html
<article class="kcard" data-task-id="...">
  <span class="kcard__dot" aria-hidden="true"></span>              <-- 6px dot tone
  <div class="kcard__body">
    <h4 class="kcard__title">Title tronqué 2 lignes max</h4>
    <div class="kcard__meta">
      <span class="mono">TASK-42</span>
      <span>·</span>
      <span>Amelia</span>
    </div>
  </div>
  <div class="kcard__chips">                                       <-- 1 chip max visible
    <span class="chip tone-warning">blocked</span>
  </div>
</article>
```

- Haut ≈ 56-72px selon contenu.
- sync state passe en icône discrète `◎` 12px à côté du titre (hover → tooltip "diverged runtime/storage").
- Chips réduites à max 1 en visible, le reste en hover card.

### 2.5 Sections du bas (Workshop / Intake / Watchtower / Branch-Finisher / Seance-Archive)

**Actuel** : 5 sections `.panel.panel-soft` déroulées en permanence, chacune avec section-head + mission-support-stack.

**Problèmes** :
- Duplication quasi-totale avec le rail gauche Rooms.
- Consomme 600-900px de scroll vertical inutile.

**Cible Linear** (progressive disclosure) :
- Toutes ces sections deviennent des **groupes collapsibles** avec default=closed sauf si count > 0 de tasks urgentes.
- Caret `▸` / `▾` 10px, click sur header toggle.
- State persisté dans `appState.collapsedSections: Set<string>`.

Alternative encore plus Linear : supprimer ces sections du scroll principal et les rendre accessibles **uniquement via l'inspector drawer** quand on clique sur une room du rail.

---

## 3. Composants à créer (inventaire PR 3)

### 3.1 `cp-popover` — popover primitif

```
API : data-popover="<id>" sur trigger, role=dialog, focus trap, Escape ferme
Pos : anchored bottom-left par défaut, flip si overflow
Size: min-width 220px, max-width 360px, max-height 60vh scroll
BG  : --surface-3, border 1px line-strong, radius 10px
Shadow: 0 10px 24px rgba(0,0,0,0.4), 0 2px 6px rgba(0,0,0,0.3)
```

Utilisé par : Filter, Display, Scenario picker, Actions contextuelles.

### 3.2 `cp-segmented` — segmented control

```
Haut: 28px, padding 4px
BG : --surface-1, radius 8px, border 1px line
Item: padding 0 12px, font 12px 500, radius 6px
Item active: BG --surface-3, border-color line-strong, color ink
Item hover: BG hover
```

Utilisé par : Lens mission-board (All/Attention/Blocked), futures sous-vues.

### 3.3 `cp-dropdown-trigger` — bouton déroulant breadcrumb-style

```
Format: "label : value ▾" ou "value ▾"
Pad  : 0 8px, haut 24px, radius 4px
BG   : transparent, hover --hover
Caret: 10px chevron, color ink-muted
```

Utilisé par : Scenario picker, groupby/orderby dans Display.

### 3.4 `cp-drawer` — inspector drawer right

```
Width : 480px (QHD), 400px (≤1440), 100% (≤768)
Pos   : fixed right 0, top 56px, bottom 32px (sous topbar, au-dessus statusbar)
BG    : --surface-1, border-left 1px line
Shadow: -10px 0 24px rgba(0,0,0,0.3)
Open  : translateX(100%→0) 200ms cubic-bezier(0.32, 0.72, 0, 1)
Close : inverse + Escape handler + click outside + close btn
Header: 48px avec h3 title + close btn
Body  : overflow-y auto, padding 20px 24px
```

Utilisé par : task detail (mission-board click), proof detail, scenario diff.

### 3.5 `cp-cmd-k` — command palette

```
Overlay: fixed inset 0, BG rgba(0,0,0,0.5) + backdrop-filter blur 8px
Dialog : width 640px, centered top 12vh, radius 12px, BG surface-2
Input  : 48px, padding 0 16px, font 14px, placeholder ink-muted, pas de border
Divider: 1px line sous input
Sections: Actions, Navigate (surfaces), Missions, Scenarios
Row    : 40px, padding 0 16px, font 13px, hover --hover, active --active
         Icon 16px left + label + shortcut kbd 11px mono right
Footer : 32px, divider top, tips en 11px mono (Enter to run · Esc to close)
Shortcut: Cmd/Ctrl+K ouvre
Search : fuzzy sur label + tags, highlight matches en accent
```

### 3.6 `cp-hover-card` — hover card riche

```
Delay  : 500ms open, 100ms close
Trigger: data-hovercard="<templateId>"
Content: template dans DOM caché, cloné dans popover
Size   : max 320px, padding 12/14
```

Utilisé par : cartes kanban (expand meta), rail rooms (détails), chips status (definition).

### 3.7 Notifications / status center

Out of scope PR 3 — reporté PR 4 (mais bouton cloche icon-only dans topbar comme ancre).

---

## 4. Wireframes avant/après (Mission Board, QHD)

### 4.1 Avant (v18 actuel)

```
┌──┬──────────────────────────────────────────────────────────────────────┐
│🎛│ Mission Board / Release ready     Run: [A][B][C]   Lens: [T][A][B]  OK│
├──┼──────────────────────────────────────────────────────────────────────┤
│🗂│  ┌─ rooms plaque ─┐  ┌── VUE D ENSEMBLE ────────────────────────────┐│
│  │  │ Rooms          │  │ eyebrow                                       ││
│🎮│  │ h2 title       │  │ h2 Release ready                              ││
│  │  │ muted           │  │ muted subtitle                                ││
│⚙│  │                 │  │ [chip][chip][chip][chip]  <<< doublons       ││
│  │  │ ┌─War Room──┐  │  │ ┌─12─┬─2─┬─3─┬─8─┐                           ││
│🛡│  │ │ 12 cmd    │  │  │ └────┴───┴───┴───┘                           ││
│  │  │ │ summary   │  │  └───────────────────────────────────────────────┘│
│📊│  │ │ [p][p][p] │  │  ┌── WAR ROOM ──────────────────────────────────┐│
│  │  │ └──────────┘  │  │ eyebrow                                       ││
│⚔│  │ [4 rooms]      │  │ h2 "Quel dossier doit bouger maintenant ?"    ││
│  │  │                │  │ muted                                         ││
│  │  │                │  │ [chip][chip][chip]                            ││
│🗺│  │                │  │ ┌─IN─┬─QL─┬─EX─┬─RV─┬─CL─┐                  ││
│  │  │                │  │ │card│card│card│card│card│                   ││
│  │  │                │  │ │card│card│card│card│    │                   ││
│  │  │                │  │ └────┴────┴────┴────┴────┘                   ││
│  │  │                │  │ ┌─ Branch Finisher ─┬─ Watchtower ─┐         ││
│  │  │                │  │ │ 5 cards            │ 3 cards       │       ││
│  │  │                │  │ └────────────────────┴───────────────┘       ││
│  │  │                │  └───────────────────────────────────────────────┘│
│  │  │                │  ┌─ Workshop ─┬─ Intake ─┬─ Seance Archive ─┐    │
│  │  │                │  │ 4 cards     │ 2 cards   │ 0 cards           │    │
│  │  │                │  └────────────┴───────────┴───────────────────┘    │
│  │  └────────────────┘                                                    │
├──┴──────────────────────────────────────────────────────────────────────┤
│ seq 42 · 8 hosts · 12 signals · 4 proofs · focus ·                       │
└──────────────────────────────────────────────────────────────────────────┘
```

Hauteur scroll totale : ~2400px sur 1440p = 1.7 écrans de scroll juste pour voir tout.

### 4.2 Après (PR 3 cible Linear)

```
┌──┬──────────────────────────────────────────────────────────────────────┐
│🎛│ Mission Board › Release ready ▾         ⌕ Search ⌘K  🔔  ⚙  │●│     │
├──┼──────────────────────────────────────────────────────────────────────┤
│🗂│  ┌── Missions ──────────────────────────────────────────────────────┐│
│  │  │ 12 active · 2 blocked · RUN-20260414                              ││
│🎮│  │                                       [+ New] [⊕ Filter] [☰ Display]││
│  │  └────────────────────────────────────────────────────────────────────┘│
│⚙│  ┌──────────────────────────────────────────────────────────────────┐│
│  │  │ [All 12] [Attention 3] [Blocked 2]   <<< segmented 28px          ││
│🛡│  └────────────────────────────────────────────────────────────────────┘│
│  │                                                                        │
│📊│  ┌─INTAKE 2──┬─QUALIF 3──┬─EXEC 5──┬─REVIEW 2──┬─CLOSE 0──┐           │
│  │  │ ● kcard   │ ● kcard   │ ● kcard │ ● kcard   │            │           │
│⚔│  │ ● kcard   │ ● kcard   │ ● kcard │ ● kcard   │  empty    │           │
│  │  │           │ ● kcard   │ ● kcard │           │            │           │
│  │  │           │           │ ● kcard │           │            │           │
│🗺│  │           │           │ ● kcard │           │            │           │
│  │  └───────────┴───────────┴─────────┴───────────┴────────────┘          │
│  │                                                                        │
│  │  ROOMS                                                                 │
│  │  ● War Room       12                                                   │
│  │  ○ Intake Desk     3                                                   │
│  │  ○ Workshop        4                                                   │
│  │  ○ Watchtower      1                                                   │
│  │  ○ Branch Finisher 2                                                   │
│  │  ○ Seance Archive  0                                                   │
│  │                                                                        │
│  │  ▸ Branch Finisher · 2 queued           <<< collapsed default        │
│  │  ▸ Watchtower · 1 signal                                              │
│  │  ▸ Workshop                                                            │
│  │  ▸ Intake Desk                                                         │
│  │  ▸ Seance Archive                                                      │
├──┴──────────────────────────────────────────────────────────────────────┤
│ seq 42 · 8 hosts · 12 signals · 4 proofs · focus ·                       │
└──────────────────────────────────────────────────────────────────────────┘

[Cmd-J ou click card → drawer right 480px]
┌─────────────────────────────────┐
│ Task TASK-42         ⌘J  ✕      │
├─────────────────────────────────┤
│ Title complet                    │
│ room · agent · sync              │
│                                  │
│ Detail                           │
│ ...                              │
│                                  │
│ Chips : tone-critical, ...       │
│                                  │
│ Proofs                           │
│ - summary.md                     │
│ - decision.json                  │
│                                  │
│ Actions                          │
│ [Focus] [Verify] [Unblock]       │
└─────────────────────────────────┘
```

Hauteur scroll totale : ~1100px sur 1440p = 0.8 écran = tout visible sans scroll sur QHD.

---

## 5. Plan d'implémentation PR 3

### 5.1 Ordre d'exécution

1. **Foundation CSS** : tokens popover/segmented/drawer/cmd-k, transitions, focus rings.
2. **Popover primitif** : DOM + show/hide API + focus trap + Escape.
3. **Segmented control** : refactor Lens group topbar → segmented dans board toolbar.
4. **Scenario dropdown** : refactor Run group topbar → breadcrumb dropdown.
5. **Filter popover** : bouton `[+ Filter]` + popover multi-select (status, tone, focus).
6. **Display popover** : bouton `[☰ Display]` + popover (group by / order by + toggles sections).
7. **Collapsible sections** : `appState.collapsedSections: Set<string>`, caret + click toggle, default closed.
8. **Rail Rooms compacte** : refactor `.mission-board-room-list` en rows 28px + hover card.
9. **Board header** : 1 h1 + 1 meta-line, suppression eyebrow + subtitle + chip-row redondants.
10. **Kanban cards** : dot 6px, 2 lignes title, meta ligne, 1 chip max visible, reste en hover card.
11. **Inspector drawer** : `appState.inspectorOpen: boolean` + `appState.inspectorTaskId`, Cmd-J toggle, Escape close, click card open.
12. **Cmd-K palette** : overlay + fuzzy search + sections Navigate/Actions/Missions/Scenarios.
13. **Metrics displacement** : 4 stats (Flux/Blocs/Verif/Lineage) → hover card sur meta-line + update statusbar mono.
14. **Cleanup CSS** : supprimer les règles orphelines après refactor.

### 5.2 Risques

- **renderMissionBoardMode a 2 branches** (L2055 et L2329) → refactor doit toucher les deux (ou factoriser en helper).
- **bindEvents() ne connaît pas les popovers/drawer/cmd-k** → nouvelle fonction `bindGlobalUI()` au bootstrap.
- **Cmd-K et shortcuts existants** : déjà `Ctrl+1..9` + Escape → Cmd-K doit avoir priorité quand ouvert (Escape ferme palette avant deselect carte).
- **Performance** : `render()` rebuild innerHTML entier ; popover/drawer doivent être **hors** du render loop (fixed DOM ajouté une fois au bootstrap, affiché via `.is-open` class).

### 5.3 Découpage final

Je propose de livrer PR 3 en un **seul commit fonctionnel** mais tester incrementiellement :
- Pass A (steps 1-5) : popover foundation + filter + segmented → test build
- Pass B (steps 6-9) : display + collapsible + rail compacte + header → test build
- Pass C (steps 10-13) : kanban refactor + drawer + Cmd-K + metrics → test build final v19 QHD

Si un step casse, on s'arrête et on diagnostique avant de continuer.

---

## 6. Tokens CSS canoniques (à ajouter dans styles.css)

```css
:root {
  /* Surfaces */
  --surface-0: #0b0c0e;
  --surface-1: #121418;
  --surface-2: #1a1d22;
  --surface-3: #232830;

  /* Lines */
  --line: rgba(255, 255, 255, 0.08);
  --line-strong: rgba(255, 255, 255, 0.14);

  /* Ink */
  --ink: #f6f7f8;
  --ink-soft: #9ba0a8;
  --ink-muted: #5b6068;

  /* Accent reserved */
  --accent: #ff6b3d;
  --accent-soft: rgba(255, 107, 61, 0.14);

  /* Status */
  --warning: #f59e0b;
  --critical: #f87171;
  --positive: #4ade80;

  /* Interactive */
  --hover: rgba(255, 255, 255, 0.04);
  --active: rgba(255, 255, 255, 0.08);
  --focus-ring: 0 0 0 2px var(--surface-0), 0 0 0 4px var(--accent);

  /* Shape */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 10px;
  --radius-xl: 12px;

  /* Shadow */
  --shadow-popover: 0 10px 24px rgba(0, 0, 0, 0.4), 0 2px 6px rgba(0, 0, 0, 0.3);
  --shadow-drawer: -10px 0 24px rgba(0, 0, 0, 0.3);
  --shadow-modal: 0 24px 64px rgba(0, 0, 0, 0.55), 0 8px 16px rgba(0, 0, 0, 0.3);

  /* Motion */
  --ease-linear-ui: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
  --duration-fast: 120ms;
  --duration-std: 140ms;
  --duration-slow: 200ms;

  /* Font */
  --font-ui: 'Geist', system-ui, -apple-system, sans-serif;
  --font-mono: 'Geist Mono', 'SF Mono', Menlo, monospace;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0ms !important;
    animation-duration: 0ms !important;
  }
}
```

---

## 7. Accessibility checklist

- [ ] Tous les boutons ont `aria-label` ou texte visible
- [ ] Popover = `role="dialog"` avec `aria-labelledby` sur titre
- [ ] Segmented = `role="tablist"` avec `role="tab"` + `aria-selected`
- [ ] Drawer = `role="dialog"` + focus trap + restore focus sur close
- [ ] Cmd-K = `role="dialog"` + `role="listbox"` sur résultats
- [ ] Focus visible : `--focus-ring` sur tous les interactifs (pas juste `outline: none`)
- [ ] Kbd shortcuts : `<kbd>` avec `aria-keyshortcuts` sur triggers
- [ ] Contrast : ink sur surface-0 = 18:1 ; ink-soft sur surface-0 = 7:1 ; ink-muted = 4.5:1 min
- [ ] Reduced motion : toutes animations respectent `prefers-reduced-motion`

---

## 8. Sources & inspiration

Patterns observés/documentés (pas de copie, extraction conceptuelle) :
- Linear — kanban, filter popover, display, Cmd-K, inspector, hover cards
- Height 2.0 — segmented, grouping options, board density
- Raycast — command palette layout + shortcuts rendering
- Vercel Dashboard — topbar breadcrumb cliquable, dropdowns compacts
- Stripe Dashboard — filter chips discrets, details drawer right

Next step : passer à l'implémentation en 3 passes A/B/C.
