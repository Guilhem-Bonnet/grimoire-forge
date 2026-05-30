# Visual Brief — Mission Board Grimoire

> Projet : **Grimoire**
> Portee : **Mission Board, backlog natif, rooms, cartes, affordances et direction visuelle**
> Sources : [SPEC-mission-board-grimoire.md](./SPEC-mission-board-grimoire.md), [ADR-007-mission-board-control-plane-causal.md](./ADR-007-mission-board-control-plane-causal.md), [grimoire-game-assets/STYLE_GUIDE.md](../../grimoire-game-assets/STYLE_GUIDE.md)

---

## 1. Product Snapshot

- Product name: `Mission Board Grimoire`
- Domain: control plane visuel pour orchestration agentique et verification
- Primary audience: utilisateur expert, operateur, mainteneur, reviewer
- Primary user action: creer, qualifier, router, verifier et clore une task sans perdre la causalite
- Key success signal: une task critique peut etre comprise, pilotee et verifiee sans transcript brut ni etat parallele

## 2. Intent And Experience Goal

- One-line intent: faire ressentir un poste de commandement mystique et technique, ou chaque carte est un dossier causal vivant et chaque room repond a une question operatoire nette
- Desired emotional tone: `lucide`, `rituel`, `tenu`
- Must avoid: `dashboard SaaS`, `theatre visuel`, `magie floue`, `gamification sociale`, `pluie de badges`
- Brand personality: atelier d'operations agentiques, plus bibliotheque technique que cockpit de startup

## 3. Information Architecture Priorities

- Priority block 1: lire le statut canonique d'une mission et de ses tasks
- Priority block 2: comprendre pourquoi une task est ici, ou elle va et ce qui la bloque
- Priority block 3: lancer une commande d'intention bornee sans court-circuiter le runtime
- Secondary content: lineage inter-session, archive, comparisons, telemetry detaillee
- Navigation model: shell stable a rooms specialisees, avec dossier lateral de details et frise causale basse

## 4. Visual Direction

### 4.1 Direction generale

Le board doit ressembler a un systeme d'exploitation agentique installe dans un bureau mystique et technique. Les surfaces principales evocent des dossiers en papier, des plaques techniques, des scelles de verification et des liaisons de dependances visibles uniquement quand elles servent la lecture.

### 4.2 Palette canonique

| Token | Usage dominant |
| --- | --- |
| `Ink` | contours, texte, grilles, panneaux, ombres |
| `Paper` | cartes, dossiers, formulaires, details |
| `Storm` | runtime, workshop, watchtower, etat machine |
| `Verdigris` | handoff, qualification, routage, dependances |
| `Brass` | verdict accepte, readiness, scelles |
| `Ember` | incident, reject, blocage critique |
| `Memory` | lineage, archive, stale, seance |
| `Leaf` | resolution stable et etat sain secondaire |

### 4.3 Typographie et formes

- Titres de room: serif editoriale sobre, avec silhouette de plaque ou d'enseigne
- Metadata, IDs et micro-etats: grotesque ou mono technique compacte
- Cartes: dossiers `Paper` cadres `Ink`, coins nets ou legerement biseautes
- Badges: onglets, cachets et encoches courtes ; pas de pills gonflees ni de capsules generiques

### 4.4 Signatures visuelles

- task en dossier cartonne, pas en carte flottante;
- sceau de verification `Brass` local, jamais carte doree entiere ;
- dependance en tether `Verdigris` directionnel, visible au focus ;
- archive et seance comme paper trail `Memory`, jamais halo mystique ;
- supervision comme instrumentation `Storm`, jamais alarme permanente.

## 5. Motion And Animation

- Role of animation: expliquer les transitions metier, jamais meubler le silence
- Core transitions: intake d'une fiche, stamp de qualification, tether de handoff, dock vers verification, flash serre sur reject
- Hero motions: aucun hero motion permanent ; les seules motions hero sont les transitions qui portent une causalite forte
- Timing and rhythm: mouvements courts, localises, centre sur l'action ; aucun mouvement continu sur toute la surface
- Reduced-motion fallback: remplacement des translations par contours, changements de couleur, opacite et scelles statiques

## 6. Asset Requirements

- Required outputs: plaques de rooms, sigils d'etat, scelles de verification, badges de complexite, tethers de dependance, marqueurs stale, icones de commandes
- Asset families:
  - `room plaques`
  - `task sigils`
  - `verification seals`
  - `dependency loom`
  - `incident markers`
  - `archive tabs`
- 2D sprite and sheet needs: badges, seals, tethers, sigils et micro-FX semantiques
- FX needs: handoff directionnel, stamp de qualification, verdict pass, verdict fail, stale reminder
- Resolution targets: assets lisibles sur cartes compactes et panneaux de room
- Export formats: `png`, `svg` si besoin de netete UI, spritesheet pour FX discretes

## 7. Technical Constraints

- Frontend stack: surfaces board Grimoire et runtime UI existantes
- Runtime constraints: le board ne possede jamais son etat propre de task
- Performance targets: densite d'information elevee avec motion minimale et localisee
- Accessibility constraints: lecture clavier, focus fort, reduced motion, contraste fort sur texte et badges
- Platform targets: desktop prioritaire, lecture correcte sur layouts compacts

## 8. Validation Gates

- UX clarity checks:
  - une carte repond en un coup d'oeil a `quoi`, `ou`, `pourquoi`, `quoi ensuite`
  - une room repond a une question primaire sans bruit lateral
- Visual coherence checks:
  - la palette reste semantique
  - aucun composant ne ressemble a un dashboard SaaS interchangeable
- Accessibility checks:
  - focus visible
  - contrastes lisibles
  - reduced motion complet
- Performance checks:
  - aucune animation globale continue
  - aucune dependance a un canvas suractive pour lire l'etat
- Implementation readiness checks:
  - chaque etat visuel se mappe a un predicate canonique
  - chaque commande UI se mappe a une commande runtime explicite

## 9. Risks And Assumptions

- Open risks:
  - surcharge semantique des cartes
  - confusion entre room narrative et domaine metier reel
  - tentation d'utiliser le drag and drop comme source de mutation canonique
- Assumptions:
  - les rooms principales restent `Intake Desk`, `War Room`, `Workshop`, `Branch Finisher`, `Seance Archive`, `Watchtower`
  - les read models canoniques existeront avant une UI trop riche
- Unknowns needing confirmation:
  - niveau d'exposition du `Mission Bundle`
  - place exacte de la colonne `Verified`
  - profondeur de la vue `Seance` en V1

## 10. Delivery Contract

- Deliverable list:
  - [UX-MAP-mission-board-grimoire.md](./UX-MAP-mission-board-grimoire.md)
  - [MOTION-SPEC-mission-board-grimoire.md](./MOTION-SPEC-mission-board-grimoire.md)
  - `component inventory` future dans le runtime UI
- Priority order:
  1. shell et rooms
  2. carte de task et dossier lateral
  3. etats, scelles et dependances
  4. motion semantique
- Acceptance criteria:
  - aucune room ne vit sans read model correspondant
  - aucune couleur ne sert seulement a decorer
  - aucune interaction n'invente un etat canonique absent du ledger
