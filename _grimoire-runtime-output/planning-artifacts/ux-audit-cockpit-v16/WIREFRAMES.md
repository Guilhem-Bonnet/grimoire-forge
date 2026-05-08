# Wireframes — Cockpit refonte

Deux concepts annotés basés sur [AUDIT.md](AUDIT.md). Toutes les
dimensions sont en pixels à 2560×1440 (QHD). Adaptables à 1920 (FHD) et
1440 (laptop) via breakpoints.

Légende : `[...]` = zone, `|` = bordure, `▼` = collapsible,
`→` = résultat d'interaction.

## Concept A — Focus + Periphery (recommandé)

Refonte **légère** : CSS dominant, un minimum de HTML. Garde
l'architecture actuelle de `main.ts`, ne fait que ré-agencer.

### Fold 1 — au chargement, kanban pleine largeur

```text
2560 px ────────────────────────────────────────────────────────────────
┌──────────────────────────────────────────────────────────────────────┐
│ [G] [▦][◉][◈][◇][☰][⊞]    Run: Guardrails bloquants ▾   Lens: Tout ▾ │  56 px
│  ↑ switcher surface 14    ↑ sélecteur             ↑  [⚠ 3] [🔍] [⚙] │
├──────────────────────────────────────────────────────────────────────┤
│ MISSION BOARD — feature/provenance-clean                             │  40 px
│ 3 missions bloquées · 13 signaux veille · 6 blocages                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INTAKE   QUALIFIED     RUNNING     REVIEW      DONE                 │
│  (0)      (1)           (1)         (1)         (0)                  │
│  ┌─────┐  ┌─────────┐   ┌──────┐    ┌────────┐  ┌────┐               │
│  │     │  │Prepare  │   │      │    │Activate│  │    │               │
│  │     │  │branch   │   │      │    │power   │  │    │               │
│  │ ∅   │  │finish…  │   │ ∅    │    │cards   │  │ ∅  │               │  ~900 px
│  │     │  │[QUAL]   │   │      │    │[REVIEW]│  │    │               │
│  │     │  │non aff. │   │      │    │blocked │  │    │               │
│  │     │  │[3 trace]│   │      │    │[3 tr]  │  │    │               │
│  │     │  └─────────┘   │      │    └────────┘  │    │               │
│  │     │                │      │                │    │               │
│  └─────┘                └──────┘                └────┘               │
│                                                                      │
│  + 5 lanes auto-fit 260-320 px selon largeur dispo                   │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│ ▼ Preuves récentes (6)  ▼ Dérives (13)  ▼ Finition  ▼ Historique     │   collapsed 40 px
└──────────────────────────────────────────────────────────────────────┘
2560 px ────────────────────────────────────────────────────────────────
```

### Fold 1 — état « carte sélectionnée », inspector ouvert

```text
┌──────────────────────────────────────────────────────┬───────────────┐
│ Top bar identique                                    │               │
├──────────────────────────────────────────────────────┤  INSPECTOR    │
│ MISSION BOARD — feature/provenance-clean             │  ← → ✕        │
├──────────────────────────────────────────────────────┤               │
│                                                      │  Prepare      │
│  Kanban 4-5 colonnes auto-fit                        │  branch       │
│  (largeur dispo ≈ 2060 px - 440 px inspector)        │  finish       │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                     │  decision     │
│  │     │ │SELECT│ │     │ │     │                    │  ────────     │
│  │     │ │ ★★★ │ │     │ │     │                    │  Statut       │
│  └─────┘ └─────┘ └─────┘ └─────┘                     │  Qualified    │
│                                                      │  → projection │
│                                                      │               │
│                                                      │  Blocages (2) │
│                                                      │  · Activate   │
│                                                      │  · Audit prov.│
│                                                      │               │
│                                                      │  Prochains    │  440 px
│                                                      │  mouvements   │
│                                                      │  · Intake     │
│                                                      │  · Running    │
│                                                      │  · Review     │
│                                                      │               │
├──────────────────────────────────────────────────────┤               │
│ ▼ Preuves récentes  ▼ Dérives  ▼ Finition  ▼ Histo   │               │
└──────────────────────────────────────────────────────┴───────────────┘
```

### Interactions clés

| Trigger | Résultat |
|---------|----------|
| Clic sur carte kanban | Inspector s'ouvre à 440 px (slide-in 180 ms) |
| `Esc` ou clic hors carte | Inspector se ferme |
| `Cmd-J` | Toggle inspector sur la carte focus courante |
| Clic sur chip `[⚠ 3]` top bar | Scroll smooth sur la première carte bloquante + inspector ouvert |
| Clic sur `▼ Preuves récentes` | Expand ruban 240 px, les autres restent fermés |
| `Cmd-1..9` | Switch surface |
| `J / K` | Navigue dans les cartes du kanban (flèche bordure orange) |
| `Cmd-K` | Palette de recherche globale (surfaces, cartes, rooms) |

### Mapping implémentation

| Élément | Localisation | Changement |
|---------|--------------|------------|
| `.shell` | `styles.css:118` | `max-width: min(2200px, 100% - 48px)` |
| Hero `.live-runtime-atlas` | `main.ts` (renderHero) | Remplacé par `.topbar` fixe 56 px |
| Surface switcher `.primary-surfaces + .secondary-atlas` | `main.ts` (renderSurfaceNav) | Fusion en barre icône unique dans top bar |
| `.run-selector`, `.lens-picker` | `main.ts` | Dropdowns dans top bar |
| `.mission-board-layout` | `styles.css:1015` | Enlever rail gauche (déplacé en nav), garder col kanban + inspector toggle |
| `.mission-board-main` | `styles.css:1162` | `grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))` |
| OPS dossier rail droit | `main.ts` (renderOpsDossier) | Devient `.inspector` positionné fixed, class `is-open` conditionnelle |
| `Workshop / Intake / Branch Finisher / Seance Archive / Watchtower` cards | `main.ts` | Déplacés dans ruban collapsible bas |
| Frise causale | `main.ts` | Même ruban, onglet `Preuves récentes` |

### Bénéfices

- Fold 1 = outil de travail, pas narratif.
- Kanban respire, 5-7 colonnes cartes 260-320 px.
- Ruban bas = accessible sans noyer.
- Inspector = contexte uniquement quand demandé.
- Top bar = navigation permanente discrète.

### Effort estimé

CSS refactor : ~200 lignes modifiées. HTML : ~80 lignes déplacées
(creation topbar, creation ruban bas, wrapping inspector). Pas de
changement de data model, pas de toucher aux vues runtime.

---

## Concept B — Command Center (plus ambitieux)

Refonte **structurelle** : pense le cockpit comme un IDE de pilotage
d'agents, pas comme une SPA de dashboard.

### Layout global

```text
2560 px ────────────────────────────────────────────────────────────────
┌────┬────────────────────────────────────────────────────┬────────────┐
│ N  │ TOP BAR — breadcrumb + action bar                  │ I          │   56 px
│ A  │ feature/provenance-clean · Mission Board · War Room│ N          │
│ V  ├────────────────────────────────────────────────────┤ S          │
│    │                                                    │ P          │
│ 56 │  WORKSPACE (kanban OU game-ui OU obs. OU …)        │ E          │
│ px │                                                    │ C          │
│    │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐         │ T          │
│ ▦  │  │    │ │    │ │    │ │    │ │    │ │    │         │ O          │
│ ◉  │  │    │ │    │ │    │ │    │ │    │ │    │         │ R          │
│ ◈  │  │    │ │    │ │    │ │    │ │    │ │    │         │            │
│ ◇  │  │    │ │    │ │    │ │    │ │    │ │    │         │ toggle     │ ~1280 px
│ ☰  │  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘         │ Cmd-J      │
│ ⊞  │                                                    │            │
│    │                                                    │ 440 px     │
│ ── │                                                    │            │
│    │                                                    │            │
│ ⚙  │                                                    │            │
│ ?  │                                                    │            │
├────┴────────────────────────────────────────────────────┴────────────┤
│ STATUS BAR — [run] · [lens] · [4 hosts] · [6 blocages] · [Cmd-K]    │   32 px
└──────────────────────────────────────────────────────────────────────┘
2560 px ────────────────────────────────────────────────────────────────
```

### Différences avec Concept A

| Aspect | Concept A | Concept B |
|--------|-----------|-----------|
| Surface switcher | Top bar horizontale | Rail vertical gauche fixe 56 px |
| Run / Lens | Top bar dropdowns | Status bar bas |
| Ruban contextuel | En bas, collapsible | Intégré dans Inspector onglets |
| Breadcrumb | Absent | Top bar dédiée (run / surface / room) |
| Search | Cmd-K overlay | Cmd-K dans status bar (bouton visible) |
| Aide | Non présente | Icône `?` rail gauche |

### Ergonomie

- Rail gauche = VS Code-like activity bar, 14 icônes + `⚙` + `?`.
- Top bar = breadcrumb hiérarchique cliquable (retour rapide).
- Inspector = 4 onglets tabs selon contexte : `Détail · Preuves · Causalité · Actions`.
- Status bar = permanent, réassure, signale les blocages en temps réel.
- Workspace = ZONE OUTIL, rien ne la pollue.

### Effort estimé

HTML : nouvelle structure avec 5 zones fixed. CSS : ~400 lignes.
`main.ts` : refactor des render*, ~600 lignes touchées. Tests
`grimoire-game: cockpit:verify` à revoir.

### Bénéfices

- Reconnaissable d'emblée (pattern IDE / Slack / Linear).
- Scale naturellement à toutes les surfaces (pas juste Mission Board).
- Keyboard-first par conception.
- Preserve 100% de la largeur pour le workspace quelle que soit la
  résolution.

---

## Recommandation

**Concept A** en priorité. Il adresse les 3 P0 et 4 des 6 P1/P2 avec un
effort faible, sans risque sur les tests cockpit. Si l'usage valide ce
direction, itérer vers **Concept B** progressivement (rail gauche
d'abord, puis status bar, puis inspector onglets).

Le piège à éviter : commencer par Concept B sans avoir validé que la
disposition « foyer + périphérie » change vraiment ton quotidien. Un
mois de test de Concept A donne la réponse.

## Annexes — wireframes responsive

### FHD 1920×1080

```text
1920 px ──────────────────────────────────────────
┌────┬──────────────────────────────────┬────────┐
│NAV │ Topbar                           │ INSP   │
│ 56 ├──────────────────────────────────┤        │
│    │ Kanban 4 colonnes auto-fit       │ 380 px │
│    │                                  │        │
└────┴──────────────────────────────────┴────────┘
```

### Laptop 1440×900

```text
1440 px ────────────────────────────────
┌────┬────────────────────────┬────────┐
│NAV │ Topbar                 │ INSP   │
│ 56 ├────────────────────────┤ 340 px │
│    │ Kanban 3 colonnes      │        │
│    │ scroll horizontal      │ (ferm  │
│    │                        │ par    │
│    │                        │ défaut)│
└────┴────────────────────────┴────────┘
```

### Mobile / tablette portrait (non prioritaire)

Surface switcher devient `<select>`, inspector devient full-screen
modal, ruban bas devient `<details>` natifs.
