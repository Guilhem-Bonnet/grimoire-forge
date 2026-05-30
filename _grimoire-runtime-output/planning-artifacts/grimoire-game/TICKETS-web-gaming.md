# Tickets d'Execution — Grimoire Game Web/Gaming

> Projet : **Grimoire Game**
> Plan source : [PLAN-implementation-web-gaming.md](./PLAN-implementation-web-gaming.md)
> Sprint de reference : [SPRINT-S09-grimoire-game.md](./SPRINT-S09-grimoire-game.md)
> Regle : aucun ticket ne passe en Done sans preuves techniques verifiables

---

## 1. Conventions

Statuts autorises:

- Backlog
- Ready
- In Progress
- Review
- Done

Definition of Ready:

- Scope explicite
- Dependances explicites
- Criteres d'acceptation testables
- Evidence attendue definie

Definition of Done:

- Criteres d'acceptation valides
- Tests associes passes
- Logs/preuves presentes
- Documentation impactee mise a jour

Priorite normative active:

- `GAME-TKT-037` precede toute ouverture large des tickets de configuration ou d'activation de surfaces d'execution.
- `GAME-TKT-038` durcit les transitions critiques avant extension de la Verification Gate a tout le board.
- `GAME-TKT-039` reste un pilote borne et experimental, apres stabilisation des contrats runtime et des lectures read-only.
- `GAME-TKT-047` precede toute ouverture large vers des hotes externes type Copilot, Claude ou MCP-compatible.
- `GAME-TKT-048` stabilise les contrats runtime externes avant toute surface multi-host.
- `GAME-TKT-049` ferme la policy fail-closed des connecteurs externes avant `GAME-TKT-051`.
- `GAME-TKT-052` est couvert localement sur la tranche runtime de reference; le contrat canonique `run/host/proof` ne doit plus etre relu comme chantier local ouvert sans nouveau reliquat explicite.
- `GAME-TKT-053` est prouve localement sur le flux critique mono-host `preview -> validation -> commit borne`; sa chaine replay et preuve est disponible sans redecoupage supplementaire du coeur runtime.
- `GAME-TKT-054` est couvert localement par le cockpit minimal expert branche sur la meme spine runtime et ses read models de preuve/replay.
- `GAME-TKT-040` a `GAME-TKT-046` sont couverts localement sur la tranche control plane multi-PC bornee; tout reliquat doit etre redecoupe explicitement comme deploiement multi-machine, orchestration cross-host ou UX d'exploitation etendue.
- `GAME-TKT-047` a `GAME-TKT-051` sont couverts localement sur la tranche host bridge bornee; tout reliquat doit etre redecoupe explicitement comme integration vendor, interop externe ou surface produit multi-host plus large.
- `GAME-TKT-018` est couvert localement sur une tranche runtime bornee de power cards gouvernees et persistantes; toute extension restante releve d'une surface produit plus riche ou d'un catalogue plugin plus large.
- `GAME-TKT-027` est couvert localement sur une tranche runtime bornee de registre de provenance et gate fail-closed; toute extension restante releve d'un pipeline legal ou asset plus large que le package courant.
- `GAME-TKT-040` a `GAME-TKT-046`, `GAME-TKT-050`, `GAME-TKT-051`, `GAME-TKT-012` a `GAME-TKT-020` et `GAME-TKT-029` a `GAME-TKT-036` restent gelees tant qu'un reliquat multi-PC, multi-host ou produit n'est pas redecoupe explicitement depuis ce front deja prouve.
- Artefacts d'execution associes : [PAQUET runtime](./PAQUET-execution-agentic-guardrails-runtime.md), [CONTRAT runtime](./CONTRAT-runtime-agentic-guardrails.md), [MATRICE runtime](./MATRICE-verification-agentic-guardrails-web-gaming.md), [SUITE runtime](./SUITE-tests-agentic-guardrails-web-gaming.md), [PAQUET host bridge](./PAQUET-execution-host-bridge-agentique-externe.md), [CONTRAT host bridge](./CONTRAT-host-bridge-agentique-externe.md), [MATRICE host bridge](./MATRICE-verification-host-bridge-agentique-externe.md), [SUITE host bridge](./SUITE-tests-host-bridge-agentique-externe.md).
- Artefacts de sequencing prioritaires : [paquet post-challenge programme](../../../docs/exploitation/paquet-execution-prioritaire-post-challenge-agent-os-game-ui.md), [paquet post-challenge runtime](./PAQUET-execution-front-prioritaire-post-challenge.md).
- Artefacts multi-PC associes : [PAQUET multi-PC](./PAQUET-execution-multi-pc-runtime.md), [UX cockpit/observateur](./UX-cockpit-observateur-multi-pc.md).

---

## 2. Front prioritaire post-challenge

Ce front ne cree pas un deuxieme backlog. Il resserre l'ordre d'attaque du board existant.

| Ordre | Ticket | Role | Tickets supports immediats | Gate de sortie |
| --- | --- | --- | --- | --- |
| 1 | `GAME-TKT-052` | Geler le contrat canonique `run/host/proof` | `GAME-TKT-001`, `GAME-TKT-003`, `GAME-TKT-004`, `GAME-TKT-037`, `GAME-TKT-047`, `GAME-TKT-048`, `GAME-TKT-049` | Un run critique mono-host se reconstruit et un refus fail-closed est explicable |
| 2 | `GAME-TKT-053` | Prouver un flux critique mono-host | `GAME-TKT-005`, `GAME-TKT-008`, `GAME-TKT-010`, `GAME-TKT-038`, `GAME-TKT-052` | Le flux `preview -> validation -> commit borne` passe avec replay et preuve relies |
| 3 | `GAME-TKT-054` | Livrer le cockpit minimal expert | `GAME-TKT-011`, `GAME-TKT-014`, `GAME-TKT-053` | Un operateur inspecte, explique et verifie le flux sans transcript brut |

Mise a jour de verification locale au 2026-04-12:

- `GAME-TKT-052` est couvert localement par [verification-gate.contract.test.ts](../../../../grimoire-kit/apps/grimoire-game/tests/contracts/verification-gate.contract.test.ts) et [surface-governance.test.ts](../../../../grimoire-kit/apps/grimoire-game/tests/integration/surface-governance.test.ts).
- `GAME-TKT-053` est prouve localement par [critical-flow-mono-host.test.ts](../../../../grimoire-kit/apps/grimoire-game/tests/integration/critical-flow-mono-host.test.ts).
- `GAME-TKT-054` est couvert localement par [runtime-dashboard-view.test.ts](../../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-dashboard-view.test.ts), [expert-cockpit-view.test.ts](../../../../grimoire-kit/apps/grimoire-game/tests/integration/expert-cockpit-view.test.ts) et [runtime-cockpit-view.test.ts](../../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-cockpit-view.test.ts).

Le front est donc passe localement sur sa tranche runtime de reference; les fronts multi-PC, multi-host, rooms riches, gamification et memory UX large restent en attente d'un reliquat explicite ou d'une nouvelle tranche hors de ce coeur deja prouve.

---

## 2-bis. Etat de reference runtime local

Mise a jour de reference au 2026-04-11:

- `GAME-TKT-030` est couvert et valide sur sa tranche runtime bornee dans `grimoire-kit/apps/grimoire-game`; tout reliquat doit etre redecoupe explicitement comme extension UI ou produit, et non relu comme coeur runtime encore ouvert.
- `GAME-TKT-038` est couvert et valide sur sa tranche runtime bornee; les tickets qui le referencent peuvent le traiter comme dependance satisfaite localement.
- `GAME-TKT-035` est deja couvert sur sa tranche runtime locale par les projections de branch finisher et d'audit securite; aucun increment runtime borne supplementaire n'est ouvert en l'etat.
- `GAME-TKT-039` est deja couvert sur sa tranche runtime locale par le pilote borne d'enveloppe canonique et les projections runtime associees; il reste un marqueur experimental tant qu'aucun delta explicite n'est recadre.
- `GAME-TKT-018` est deja couvert localement sur sa tranche runtime par `power-cards-view`, la persistence `runtime/storage` et les refus d'activation hors trust ou policy.
- `GAME-TKT-027` est deja couvert localement sur sa tranche runtime par `provenance-compliance-view` et le gate fail-closed du branch finisher.
- `GAME-TKT-040` a `GAME-TKT-046` sont deja couverts localement par le control plane, la flotte de noeuds, les leases, le cockpit live, l'observateur et le command gateway bornes.
- `GAME-TKT-047` a `GAME-TKT-051` sont deja couverts localement par les contrats host bridge, la policy externe, l'import review -> evidence et la surface multi-host runtime.
- `GAME-TKT-052` est deja couvert sur sa tranche runtime locale par le contrat canonique `run/host/proof`, les gardes de verification et les refus fail-closed.
- `GAME-TKT-053` est deja prouve localement par le flux critique mono-host et son miroir refuse.
- `GAME-TKT-054` est deja couvert localement par le cockpit minimal expert et ses projections de preuve/replay.
- `GAME-TKT-027` ne revele pas, a date, de tranche runtime locale bornee supplementaire a attaquer sans redecoupage gouvernance ou provenance plus large.

---

## 3. Board des tickets

| Ticket | Priorite | Slice | Titre | Dependances |
| --- | --- | --- | --- | --- |
| GAME-TKT-001 | P0 | Slice 0 | Contrat WS versionne + validation Zod | Aucune |
| GAME-TKT-002 | P0 | Slice 0 | Contrat AgentAdapter + adapter grimoire | GAME-TKT-001 |
| GAME-TKT-003 | P0 | Slice 0 | Sequence IDs + idempotence + replay | GAME-TKT-001 |
| GAME-TKT-004 | P0 | Slice 0 | Auth WS/API + RBAC minimal | GAME-TKT-001 |
| GAME-TKT-037 | P0 | Slice 0 | Garde-fous OWASP Agentic Skills sur surfaces d'execution | GAME-TKT-001, GAME-TKT-004 |
| GAME-TKT-005 | P0 | Slice 1 | Store GameState + hydration snapshot | GAME-TKT-001, GAME-TKT-003 |
| GAME-TKT-006 | P0 | Slice 1 | ECS deterministic + scheduler profile | GAME-TKT-005 |
| GAME-TKT-007 | P0 | Slice 1 | Nav-grid + A* + collision room-aware | GAME-TKT-005, GAME-TKT-006 |
| GAME-TKT-008 | P0 | Slice 2 | Verification Gate bloque Done sans preuve | GAME-TKT-004, GAME-TKT-005 |
| GAME-TKT-009 | P0 | Slice 2 | Asset loader gouverne par manifests | GAME-TKT-005 |
| GAME-TKT-010 | P0 | Slice 2 | Matrice qualite automatisee (contrats, resilience, non-regression) | GAME-TKT-001, GAME-TKT-002, GAME-TKT-003, GAME-TKT-004, GAME-TKT-005, GAME-TKT-006, GAME-TKT-007, GAME-TKT-008, GAME-TKT-009 |
| GAME-TKT-011 | P1 | Slice 2 | Deep Inspection agent (read-only + actions controlees) | GAME-TKT-005, GAME-TKT-004 |
| GAME-TKT-038 | P1 | Slice 2 | Chaine de verification orientee AIVS sur transitions critiques | GAME-TKT-008, GAME-TKT-010 |
| GAME-TKT-012 | P1 | Slice 3 | Kanban in-world synchronise activite agent | GAME-TKT-005, GAME-TKT-008 |
| GAME-TKT-013 | P1 | Slice 3 | Communication inter-agents + traces | GAME-TKT-005 |
| GAME-TKT-014 | P1 | Slice 3 | Visualisation workflow + historique decisions | GAME-TKT-005 |
| GAME-TKT-015 | P1 | Slice 3 | Challenge Room end-to-end | GAME-TKT-008, GAME-TKT-012, GAME-TKT-013 |
| GAME-TKT-016 | P1 | Slice 3 | Library/Memoire active + long terme | GAME-TKT-005, GAME-TKT-013 |
| GAME-TKT-017 | P2 | Slice 4 | Worktree Room dynamique par branche | GAME-TKT-004, GAME-TKT-005 |
| GAME-TKT-018 | P2 | Slice 4 | Power Cards plugins + persistence | GAME-TKT-004, GAME-TKT-005, GAME-TKT-037 |
| GAME-TKT-019 | P2 | Slice 4 | Retro Room + snapshot comparatif | GAME-TKT-010 |
| GAME-TKT-020 | P2 | Slice 4 | Spectator mode read-only + surface VS Code | GAME-TKT-004, GAME-TKT-017 |
| GAME-TKT-021 | P1 | Slice 5 | Gouvernance drift prompts/politiques + suite canari | GAME-TKT-001, GAME-TKT-011 |
| GAME-TKT-022 | P1 | Slice 5 | Runbooks incident + exercices de reprise critiques | GAME-TKT-003, GAME-TKT-005, GAME-TKT-010 |
| GAME-TKT-023 | P1 | Slice 5 | Qualite memoire/recall + gate obsolescence | GAME-TKT-010, GAME-TKT-016 |
| GAME-TKT-024 | P2 | Slice 5 | Protocole anti-chambre d'echo pour review/challenge | GAME-TKT-015 |
| GAME-TKT-025 | P2 | Slice 5 | FinOps agentique (cout/token/latence par ticket) | GAME-TKT-010, GAME-TKT-011 |
| GAME-TKT-026 | P2 | Slice 5 | Explicabilite operationnelle via decision cards | GAME-TKT-011, GAME-TKT-014 |
| GAME-TKT-027 | P1 | Slice 5 | Gate conformite licences et provenance assets/plugins | GAME-TKT-009, GAME-TKT-018 |
| GAME-TKT-028 | P3 | Slice 5 | Framework experimentation produit (hypothese/mesure/decision) | GAME-TKT-011, GAME-TKT-015, GAME-TKT-019 |
| GAME-TKT-029 | P1 | Slice 6 | Agent Factory complet (create/clone/config/deploy) | GAME-TKT-004, GAME-TKT-005, GAME-TKT-011 |
| GAME-TKT-030 | P1 | Slice 6 | Configuration gamifiee complete MCP/skills/prompts/tools/hooks | GAME-TKT-002, GAME-TKT-018, GAME-TKT-020, GAME-TKT-037 |
| GAME-TKT-031 | P2 | Slice 6 | Systeme sonore in-world + controles SFX/musique/volume | GAME-TKT-005, GAME-TKT-015 |
| GAME-TKT-032 | P2 | Slice 6 | Progression XP + achievements + persistence SQLite | GAME-TKT-005, GAME-TKT-019 |
| GAME-TKT-033 | P2 | Slice 6 | Tutoriel onboarding first-run + resume/skip | GAME-TKT-011, GAME-TKT-012 |
| GAME-TKT-034 | P1 | Slice 6 | Investigation Lab 4 phases + cycle review code bloqueur | GAME-TKT-008, GAME-TKT-015, GAME-TKT-024 |
| GAME-TKT-035 | P1 | Slice 6 | Branch Finisher + Security Audit Room in-world | GAME-TKT-004, GAME-TKT-017, GAME-TKT-027, GAME-TKT-037, GAME-TKT-038 |
| GAME-TKT-036 | P1 | Slice 6 | Couverture slots CdC manquants (F01/F02/F03/F19/F21/F22) | GAME-TKT-007, GAME-TKT-011, GAME-TKT-017, GAME-TKT-020 |
| GAME-TKT-039 | P2 | Slice 7 | Pilote UMF borne pour runtime, replay, spectateur et multi-sessions | GAME-TKT-001, GAME-TKT-003, GAME-TKT-020, GAME-TKT-038 |
| GAME-TKT-040 | P0 | Slice 0 | Control plane logique V1 + registre projet + enveloppe canonique de run | GAME-TKT-001, GAME-TKT-003, GAME-TKT-005 |
| GAME-TKT-041 | P0 | Slice 1 | Node manager multi-PC + heartbeat + registre de flotte | GAME-TKT-002, GAME-TKT-005, GAME-TKT-040 |
| GAME-TKT-042 | P0 | Slice 1 | Leases TTL + claims de taches + reprise sur perte de noeud | GAME-TKT-003, GAME-TKT-004, GAME-TKT-040, GAME-TKT-041 |
| GAME-TKT-043 | P0 | Slice 1 | Ownership Git distribuee par tache, branche et worktree | GAME-TKT-004, GAME-TKT-005, GAME-TKT-042 |
| GAME-TKT-044 | P1 | Slice 2 | Cockpit Live + Inspector multi-PC | GAME-TKT-010, GAME-TKT-011, GAME-TKT-041, GAME-TKT-042, GAME-TKT-043 |
| GAME-TKT-045 | P1 | Slice 2 | Office view minimale + War Room observateur sur memes projections | GAME-TKT-044 |
| GAME-TKT-046 | P1 | Slice 2 | Command gateway borne + budget de mutation GUI + mode spectateur partageable | GAME-TKT-004, GAME-TKT-020, GAME-TKT-044, GAME-TKT-045 |
| GAME-TKT-047 | P0 | Slice 0 | Modele canonique des hotes externes + capability manifest | GAME-TKT-001, GAME-TKT-004, GAME-TKT-040 |
| GAME-TKT-048 | P0 | Slice 0 | Contrats runtime Host Binding + Invocation Envelope + Context Ledger + Review Artifact | GAME-TKT-001, GAME-TKT-002, GAME-TKT-003, GAME-TKT-040, GAME-TKT-047 |
| GAME-TKT-049 | P0 | Slice 0 | Policy engine connecteurs externes + permission prompts fail-closed | GAME-TKT-004, GAME-TKT-037, GAME-TKT-047, GAME-TKT-048 |
| GAME-TKT-052 | P0 | Slice 0 | Contrat canonique run/host/proof sur panier critique borne | GAME-TKT-001, GAME-TKT-003, GAME-TKT-004, GAME-TKT-037, GAME-TKT-047, GAME-TKT-048, GAME-TKT-049 |
| GAME-TKT-050 | P1 | Slice 2 | Reviews externes -> Evidence Pack cockpit | GAME-TKT-008, GAME-TKT-010, GAME-TKT-038, GAME-TKT-048, GAME-TKT-049 |
| GAME-TKT-051 | P1 | Slice 4 | Host Bridge generique + surface multi-host | GAME-TKT-020, GAME-TKT-041, GAME-TKT-044, GAME-TKT-046, GAME-TKT-047, GAME-TKT-048, GAME-TKT-049 |
| GAME-TKT-053 | P0 | Slice 1 | Flux critique mono-host preview -> validation -> commit borne prouve | GAME-TKT-005, GAME-TKT-008, GAME-TKT-010, GAME-TKT-038, GAME-TKT-052 |
| GAME-TKT-054 | P1 | Slice 2 | Cockpit minimal expert branche sur preuve et replay | GAME-TKT-011, GAME-TKT-014, GAME-TKT-053 |

---

## 4. Tickets detailes P0/P1 critique

### GAME-TKT-052 - Contrat canonique run/host/proof sur panier critique borne

Priorite: P0

Objectif:

Fermer le contrat canonique minimal qui aligne run, host et preuve avant toute extension de surface.

Scope:

- Geler les identites minimales `runId`, `taskId`, `workerId`, `hostId`, `traceId`, `requestId` et `idempotencyKey`.
- Raccorder provenance, permission et verification minimale aux mutations critiques.
- Borner le panier critique de mutations qui sert de reference au programme.

Criteres d'acceptation:

- Un run critique mono-host se reconstruit sans inference libre.
- Une mutation critique est refusee si provenance, policy ou verification manquent.
- Runtime, audit et verification pointent vers les memes identites canoniques.

Evidence attendue:

- Tests de contrat et de refus explicites.
- Exemple de reconstruction d'un run critique.
- Trace d'audit montrant l'alignement run/host/proof.

---

### GAME-TKT-053 - Flux critique mono-host preview -> validation -> commit borne prouve

Priorite: P0

Objectif:

Prouver un flux critique unique de bout en bout avant d'ouvrir les extensions multi-PC et multi-host.

Scope:

- Selectionner un flux critique unique `preview -> validation -> commit borne`.
- Garantir replay, refus fail-closed et verification exploitable sur ce flux.
- Relier la preuve au ticket, au run et au verdict sans synthese manuelle fragile.

Criteres d'acceptation:

- Le flux critique passe de bout en bout en mono-host et mono-projet.
- Le scenario miroir incomplet ou non autorise est refuse explicitement.
- La chaine action -> decision -> verification -> replay est consultable et coherent.

Evidence attendue:

- Tests d'integration du flux critique.
- Evidence pack borne au flux choisi.
- Extrait de replay et de refus relies au meme run.

---

### GAME-TKT-054 - Cockpit minimal expert branche sur preuve et replay

Priorite: P1

Objectif:

Livrer une seule surface operateur qui permet d'inspecter, expliquer et verifier le flux critique prouve.

Scope:

- Une vue experte unique, sans rooms riches ni logique metier parallele.
- Inspection, decision, preuve et replay dans la meme surface.
- Lecture read-only sur les memes projections que la spine runtime.

Criteres d'acceptation:

- Un operateur comprend pourquoi une action a ete acceptee ou refusee sans transcript brut complet.
- La surface expose inspection, preuve et replay sur le meme run critique.
- Le cockpit n'introduit aucune nouvelle source de verite.

Evidence attendue:

- Tests d'integration des projections cockpit.
- Walkthrough operateur borne sur le flux critique.
- Capture ou journal montrant inspection, preuve et replay alignes.

---

### GAME-TKT-001 — Contrat WS versionne + validation Zod

Priorite: P0

Objectif:

Poser un contrat unique et versionne pour tous les evenements client/serveur.

Scope:

- Definir les schemas Zod pour tous les evenements critiques.
- Valider a l'entree serveur et a la consommation client.
- Introduire une version de contrat dans chaque payload.

Criteres d'acceptation:

- Tout evenement invalide est rejete avec erreur explicite.
- Les evenements valides traversent le pipeline sans cast implicite.
- Les tests de contrat couvrent success et failure cases.

Evidence attendue:

- Rapport de tests de contrat.
- Exemples de payloads valides et invalides.

---

### GAME-TKT-002 — Contrat AgentAdapter + adapter grimoire

Priorite: P0

Objectif:

Rendre le coeur du moteur independant de la source agentique.

Scope:

- Definir l'interface AgentAdapter.
- Implementer AdapterGrimoire comme reference.
- Brancher le moteur uniquement via l'interface.

Criteres d'acceptation:

- Le moteur ne depend d'aucun type interne grimoire hors adapter.
- Un adapter factice de test peut etre injecte sans modification du coeur.

Evidence attendue:

- Tests d'integration avec adapter mock.
- Diagramme des points d'extension adapter.

---

### GAME-TKT-003 — Sequence IDs + idempotence + replay

Priorite: P0

Objectif:

Garantir la coherence d'etat sous deconnexion, duplication ou relecture d'evenements.

Scope:

- Ajouter sequence IDs sur evenements server.
- Ajouter idempotency key sur mutations critiques.
- Implementer resync par snapshot puis replay borne.

Criteres d'acceptation:

- Aucune mutation en double lors d'un replay.
- Les evenements out-of-order sont ignores ou reordonnes selon strategie documentee.
- Reconnexion client restaure un etat coherent.

Evidence attendue:

- Tests de resilience (duplicate/out-of-order/replay).
- Log d'audit montrant sequence et dedup.

---

### GAME-TKT-004 — Auth WS/API + RBAC minimal

Priorite: P0

Objectif:

Fermer la surface d'attaque minimale avant extension fonctionnelle.

Scope:

- Authentification token pour WS/API.
- Roles: orchestrateur, agent, spectateur.
- Matrice de permissions pour operations read/write.

Criteres d'acceptation:

- Un role spectateur ne peut jamais effectuer une mutation.
- Une requete sans token valide est rejetee.
- Les refus d'autorisation sont traces.

Evidence attendue:

- Tests auth/authz.
- Extrait des logs de refus.

---

### GAME-TKT-005 — Store GameState + hydration snapshot

Priorite: P0

Objectif:

Unifier l'etat simulation/UI autour d'une source de verite unique.

Scope:

- Creer GameState type-safe.
- Hydrater a partir de STATE_SNAPSHOT.
- Reconciliation incremental events -> state.

Criteres d'acceptation:

- L'etat rehydrate produit le meme rendu que l'etat serveur.
- Les mutations passent par des reducers explicites.
- Le client recupere sans divergence apres reconnexion.

Evidence attendue:

- Tests reducers + hydration.
- Capture avant/apres reconnexion montrant coherence.

---

### GAME-TKT-006 — ECS deterministic + scheduler profile

Priorite: P0

Objectif:

Garantir des ticks deterministes et observables.

Scope:

- Ordre fixe des systemes.
- Profiling par systeme.
- Guardrail de budget frame.

Criteres d'acceptation:

- A entree egale, sortie egale sur N ticks.
- Un depassement budget est visible et trace.

Evidence attendue:

- Tests determinisme.
- Rapport de profiling par systeme.

---

### GAME-TKT-007 — Nav-grid + A* + collision room-aware

Priorite: P0

Objectif:

Fiabiliser les deplacements et supprimer les traversals invalides.

Scope:

- Generer nav-grid par room.
- Integrer A* + replanification.
- Appliquer colliders et portes.

Criteres d'acceptation:

- Aucun passage au travers de zone bloquee.
- Replanification correcte si obstacle dynamique.
- No-path gere sans blocage global.

Evidence attendue:

- Tests pathfinding obstacles/no-path.
- Scenarios de deplacement multi-room.

---

### GAME-TKT-008 — Verification Gate avant Done

Priorite: P0

Objectif:

Interdire le Done sans preuve technique explicite.

Scope:

- Emettre VERIFICATION_GATE avant transition Done.
- Exiger evidence: tests, exit code, artefact.
- Bloquer transition en cas d'evidence absente.

Criteres d'acceptation:

- Une carte sans preuve reste en Review.
- Les preuves sont historisees dans un log d'audit.
- Le message d'erreur utilisateur est actionnable.

Evidence attendue:

- Tests de workflow Kanban.
- Extraits verification-log valides.

---

### GAME-TKT-009 — Asset loader gouverne par manifests

Priorite: P0

Objectif:

Assurer la tracabilite et la reproductibilite des assets.

Scope:

- Charger exclusivement depuis export gouverne.
- Verifier presence des manifests requis.
- Rejeter assets hors pipeline.

Criteres d'acceptation:

- Aucun asset non indexe n'est charge.
- Erreur explicite si manifest manquant/invalide.

Evidence attendue:

- Tests de chargement assets.
- Journal de rejet pour asset non conforme.

---

### GAME-TKT-010 — Matrice qualite automatisee

Priorite: P0

Objectif:

Verrouiller la qualite minimum sur les axes critiques.

Scope:

- Contrats WS,
- resilience eventing,
- non-regression,
- auth/authz,
- navigation,
- verification gate.

Criteres d'acceptation:

- Pipeline de checks executable en une commande.
- Echec visible par axe de controle.

Evidence attendue:

- Sortie complete du pipeline de checks.
- Mapping test suite -> axe qualite.

---

### GAME-TKT-037 — Garde-fous OWASP Agentic Skills sur surfaces d'execution

Priorite: P0

Axe: AX-09

Objectif:

Gouverner les surfaces d'execution activables du board avant leur exposition large en UI ou runtime.

Scope:

- Dresser l'inventaire des skills, plugins, power cards, tools et actions de configuration activables dans le scope runtime.
- Associer a chaque surface une provenance, un trust status, une policy minimale et une classe de risque.
- Bloquer toute activation UI ou runtime si la metadata minimale ou la policy manque.
- Exposer l'etat de gouvernance dans les vues de configuration et d'audit securite.

Criteres d'acceptation:

- Chaque surface d'execution exposee possede une fiche risque -> controle -> gate explicite.
- Une activation sans provenance, trust status ou policy minimale est rejetee avec diagnostic actionnable.
- La Security Audit Room et la configuration gamifiee reutilisent la meme source de verite.

Evidence attendue:

- Extrait de matrice des surfaces d'execution du scope.
- Tests UI et serveur sur blocage d'activation non qualifiee.
- Journaux d'audit des refus et activations autorisees.

---

### GAME-TKT-011 — Deep Inspection agent

Priorite: P1

Objectif:

Donner une observabilite in-world utile sans compromettre la securite.

Scope:

- Panneau: modele, branche, prompt, tokens, outil actif, historique outils.
- Actions: pause, chat direct, redirect, restart.
- Protection role-based sur actions.

Criteres d'acceptation:

- Le panneau est complet et coherent avec l'etat runtime.
- Les actions non autorisees sont bloquees proprement.
- Les actions autorisees laissent une trace d'audit.

Evidence attendue:

- Tests interaction UI.
- Logs d'action par role.

---

### GAME-TKT-040 — Control plane logique V1 + registre projet + enveloppe canonique de run

Priorite: P0

Objectif:

Poser la base distribuee minimale pour plusieurs PCs sans introduire de quorum lourd ni de seconde source de verite.

Scope:

- Definir le registre du projet actif et les identifiants canoniques `runId`, `taskId`, `traceId`, `workerId`.
- Figer l'enveloppe minimale des evenements live utilises par le cockpit et l'observateur.
- Introduire un control plane logique unique cote runtime web.
- Versionner explicitement les metadonnees de causalite et de fraicheur.

Criteres d'acceptation:

- Un run se reconstruit sans identifiant implicite ni correlation heuristique fragile.
- Le cockpit et l'observateur peuvent lire les memes identifiants et la meme causalite.
- Le registre projet reste la source de verite unique pour le projet actif.

Evidence attendue:

- Tests d'integration sur registre projet et reconstruction de run.
- Exemples de payloads valides avec les identifiants canoniques.
- Note d'alignement entre control plane, read models et enveloppe runtime.

---

### GAME-TKT-041 — Node manager multi-PC + heartbeat + registre de flotte

Priorite: P0

Objectif:

Rendre visible et fiable la presence de plusieurs PCs sans etat fantome ni surcharge d'orchestration.

Scope:

- Declarer le protocole `node manager` pour chaque PC.
- Publier identite, capacites, heartbeat, sante de connexion et etat de travail.
- Exposer une projection de flotte lisible par le cockpit.
- Tracer la fraicheur des donnees pour chaque noeud.

Criteres d'acceptation:

- Deux PCs rejoignent le meme projet et restent visibles sans duplication de noeud.
- Un noeud stale ou offline est detecte explicitement.
- La flotte expose une lecture stable pour le cockpit live.

Evidence attendue:

- Tests d'integration sur heartbeats et transitions online/stale/offline.
- Projection de flotte avec captures ou snapshots de test.
- Journaux d'evenements de presence de noeuds.

---

### GAME-TKT-042 — Leases TTL + claims de taches + reprise sur perte de noeud

Priorite: P0

Objectif:

Eviter qu'une meme tache mutable soit executee deux fois apres sleep, deconnexion ou perte d'un PC.

Scope:

- Introduire un lease store V1 avec TTL et heartbeats.
- Implementer claims de taches et liberation automatique sur expiration.
- Brancher redelivery et reprise sur perte de noeud.
- Tracer tous les changements d'ownership et leurs raisons.

Criteres d'acceptation:

- Une perte de heartbeat libere l'ownership de facon sure.
- Une reprise ne produit pas de double mutation durable.
- Les claims et expirations sont observables dans les vues runtime.

Evidence attendue:

- Tests duplicate, timeout, reclaim et reprise.
- Logs d'audit de claims et expirations.
- Scenario d'integration avec deux noeuds concurrents.

---

### GAME-TKT-043 — Ownership Git distribuee par tache, branche et worktree

Priorite: P0

Objectif:

Faire de Git la verite du code sans laisser deux agents muter le meme perimetre en parallele.

Scope:

- Formaliser la regle `une tache -> une branche -> un owner -> un worktree`.
- Relier ownership runtime et perimetre Git local.
- Exposer branche, worktree et statut dirty dans les vues d'inspection.
- Rejeter toute mutation qui contourne l'ownership actif.

Criteres d'acceptation:

- Aucun perimetre mutable n'est travaille par deux agents sans ownership explicite.
- Une tache expose clairement sa branche et son worktree associes.
- Les cas de conflit d'ownership sont bloques et audites.

Evidence attendue:

- Tests d'integration sur creation de branche/worktree et rejection des collisions.
- Capture ou snapshot d'inspection montrant ownership Git.
- Journal d'audit sur les rejections de mutation hors ownership.

---

### GAME-TKT-047 — Modele canonique des hotes externes + capability manifest

Priorite: P0

Objectif:

Absorber Copilot, Claude et les hotes MCP-compatibles dans un meme modele runtime avant toute integration UI ou bridge specifique.

Scope:

- Definir `Host Binding` et `Capability Manifest` comme source canonique pour tout hote externe.
- Normaliser type d'hote, auth, scopes, health, version, capabilities, routines et surfaces de review.
- Exposer un registre des hotes lisible par le cockpit et l'audit.
- Interdire toute entree runtime d'un hote non qualifie ou non mappe.

Criteres d'acceptation:

- Un meme hote Copilot, Claude ou MCP-compatibile se decrit avec la meme structure de base.
- Aucun nom de feature vendeur n'entre dans le contrat coeur sans mapping explicite.
- Le cockpit et l'audit lisent le meme registre des hotes et le meme statut de confiance.

Evidence attendue:

- Schema de contrat `Host Binding` et `Capability Manifest`.
- Exemples de manifests pour Copilot, Claude et un hote MCP-compatible.
- Snapshot de projection du registre des hotes.

---

### GAME-TKT-048 — Contrats runtime Host Binding + Invocation Envelope + Context Ledger + Review Artifact

Priorite: P0

Objectif:

Etendre le protocole `v1` pour rendre replayables, auditables et bornes les actions, contextes et reviews issus d'un hote externe.

Scope:

- Ajouter les schemas `Host Binding`, `Invocation Envelope`, `Context Ledger` et `Review Artifact`.
- Rattacher correlation, idempotence, provenance, trust, TTL et evidence policy aux evenements externes.
- Propager ces informations dans `audit-view`, `session-view` et les read models runtime.
- Garantir qu'une mutation issue d'un hote externe passe par `preview -> validation -> commit`.

Criteres d'acceptation:

- Une action issue d'un hote externe se rejoue sans ambiguite semantique.
- Un contexte importe ne peut pas ecraser silencieusement la memoire interne.
- Une review externe se relie au meme `traceId` et au meme ticket que le run correspondant.

Evidence attendue:

- Rapports de tests de contrat.
- Exemples de payloads valides et invalides.
- Projection runtime montrant provenance, TTL et trust status.

---

### GAME-TKT-049 — Policy engine connecteurs externes + permission prompts fail-closed

Priorite: P0

Objectif:

Bloquer toute mutation durable ou import non gouverne provenant d'un SDK, plugin ou serveur externe.

Scope:

- Definir les scopes des connecteurs externes (`fs`, `network`, `secrets`, `exec`, `config_write`, `write_budget`).
- Introduire permission prompts, allowlists, degrade states et mode `deny-by-default`.
- Bloquer ou degrader les hotes stale, incompatibles ou hors policy.
- Journaliser les decisions de policy et leurs raisons dans l'audit.

Criteres d'acceptation:

- Un connecteur externe non approuve ne peut pas muter l'etat durable.
- Un hote degrade bascule au minimum en lecture seule.
- Chaque decision `ALLOW`, `PROMPT`, `DENY` ou `DEGRADE` laisse une trace exploitable.

Evidence attendue:

- Matrice scopes -> decisions -> reasons.
- Tests negatifs de blocage et degradation.
- Journaux d'audit des permission prompts et verdicts.

---

## 4. Tickets P1/P2 complementaires (format long)

### GAME-TKT-012 — Kanban in-world synchronise activite agent

Priorite: P1

Exigences ciblees: F04

Objectif:

Faire du Kanban mural la lecture canonique du travail de chaque team, synchronisee avec l'activite agentique et les gates runtime.

Scope:

- Afficher les colonnes `Backlog`, `Todo`, `In Progress`, `Review`, `Done` en room.
- Permettre drag-and-drop, creation et edition de cartes selon les roles autorises.
- Synchroniser les transitions de cartes avec l'activite effective de l'agent et les signaux `VERIFICATION_GATE`.
- Rendre visibles priorite, dependances, type, assignee et causes de blocage.

Criteres d'acceptation:

- Le drag-and-drop fonctionne sans desynchronisation client/serveur.
- Une tache change de colonne quand l'activite agentique correspondante evolue.
- Une carte ne passe pas en `Done` sans preuve validee.

Evidence attendue:

- Tests d'integration sur create, assign, transition et blocage `Review -> Done`.
- Capture du board mural avec cartes, assignees et badges de verification.
- Extrait de log montrant la synchronisation agent -> carte.

### GAME-TKT-013 — Communication inter-agents + traces

Priorite: P1

Exigences ciblees: F05

Objectif:

Rendre les echanges inter-agents visibles, relisibles et auditables a l'echelle d'une room ou entre rooms.

Scope:

- Visualiser les messages, handoffs et broadcasts par bulles, lignes de lien et timeline.
- Supporter les communications intra-room et inter-room via agents communicants.
- Journaliser type, source, destination, correlation et criticite des messages.
- Rendre les handoffs consultables dans les vues de collaboration et d'audit.

Criteres d'acceptation:

- Un message envoye apparait visuellement et dans la timeline associee.
- Un handoff inter-room reste traçable du depart a l'arrivee.
- Les communications critiques restent filtrables par agent, team et trace.

Evidence attendue:

- Tests d'integration sur message local, handoff inter-room et broadcast.
- Capture de timeline de communication avec details d'un message.
- Extrait de journal reliant source, cible et trace.

### GAME-TKT-014 — Visualisation workflow + historique decisions

Priorite: P1

Exigences ciblees: F08

Objectif:

Donner une lecture directe du chemin de workflow, des etapes courantes et de la chaine de decisions associee.

Scope:

- Afficher le DAG ou chemin de workflow actif pour les runs en cours.
- Mettre en evidence l'etape courante, les dependances et les agents contributeurs.
- Relier `WORKFLOW_STEP`, `decision cards` et historique de transitions dans une vue unifiee.
- Rendre cette lecture exploitable en board, challenge et audit.

Criteres d'acceptation:

- Un agent en workflow expose son etape courante sans ambiguite.
- L'historique des decisions est consultable a partir du workflow affiche.
- La causalite workflow contre audit reste stable apres replay.

Evidence attendue:

- Tests d'integration sur rendu du workflow et navigation historique.
- Capture d'une vue workflow avec etape active et trace reliee.
- Extrait d'audit montrant la concordance `WORKFLOW_STEP` -> decision.

### GAME-TKT-015 — Challenge Room end-to-end

Priorite: P1

Exigences ciblees: F10

Objectif:

Fermer le cycle de presentation, critique, vote et iteration dans une salle de challenge lisible et bloquante quand necessaire.

Scope:

- Orchestrer la sequence `presentation -> questions -> critiques -> vote -> iteration`.
- Rendre visibles les prises de parole, objections, verdicts et actions correctives.
- Journaliser la session de challenge avec references de trace et tickets lies.
- Creer automatiquement les taches de suite quand la review le requiert.

Criteres d'acceptation:

- Une session de challenge traverse toutes ses etapes sans rupture de contexte.
- Les critiques et votes sont reliés aux tickets ou traces concernes.
- Une iteration imposee genere automatiquement une action visible dans le backlog.

Evidence attendue:

- Tests d'integration du workflow de challenge complet.
- Capture de la room avec sequence de challenge en cours.
- Extrait de log montrant la creation automatique d'une action corrective.

### GAME-TKT-016 — Library/Memoire active + long terme

Priorite: P1

Exigences ciblees: F06

Objectif:

Rendre la memoire active et long terme des agents visible, consultable et corrélée aux acces runtime.

Scope:

- Visualiser la memoire courte, la memoire long terme et les acces de lecture ou ecriture.
- Mapper les acces memoire a la room bibliotheque et aux objets de scene associes.
- Exposer sources, fraicheur et references memoire cote inspection et audit.
- Relier les acces memoire aux traces et aux actions qui les ont motives.

Criteres d'acceptation:

- Un acces memoire genere un signal visuel et un log consultable.
- Une reference memoire est consultable depuis la fiche agent ou la bibliotheque.
- La coherence memoire contre trace runtime reste stable au replay.

Evidence attendue:

- Tests d'integration sur read, write et synchronisation memoire.
- Capture de la bibliotheque avec objets memoire consultables.
- Extrait de journal reliant acces memoire, agent et trace.

### GAME-TKT-017 — Worktree Room dynamique par branche

Priorite: P2

Exigences ciblees: F21, F22

Objectif:

Representer l'etat Git local de facon spatiale et actionnable, sans casser la discipline de branche ou de worktree.

Scope:

- Creer ou retirer des rooms selon le cycle de vie des branches et worktrees actifs.
- Afficher branche, worktree, statut dirty et options de cloture associees.
- Relier les actions de merge, PR, keep et discard aux bonnes surfaces runtime.
- Rendre les collisions de worktree ou de branche visibles avant mutation.

Criteres d'acceptation:

- Une branche active apparait dans une worktree room coherente avec le runtime.
- Les actions de cloture respectent les gates d'ownership et de verification.
- Un worktree stale ou en conflit remonte comme alerte visible.

Evidence attendue:

- Tests d'integration sur creation, synchro et retrait de worktree room.
- Capture de room montrant branche, worktree et statut dirty.
- Extrait d'audit sur une action de cloture de branche.

### GAME-TKT-018 — Power Cards plugins + persistence

Priorite: P2

Exigences ciblees: F12

Objectif:

Rendre les plugins activables via des cartes visuelles persistantes, tout en gardant la gouvernance OWASP des surfaces d'execution.

Scope:

- Representer chaque plugin comme une `Power Card` avec provenance, trust, risque et policy.
- Permettre activation et desactivation selon le role, avec confirmation explicite.
- Persister l'etat des plugins dans la configuration runtime.
- Refuser toute activation sans metadata minimale ou hors policy.

Criteres d'acceptation:

- L'activation d'une carte modifie la configuration et persiste au rechargement.
- Une carte non qualifiee est bloquee avant mutation effective.
- L'impact du plugin reste visible sur l'agent ou la room cible.

Evidence attendue:

- Tests d'integration sur activation, persistence et refus hors policy.
- Capture des power cards avec badges provenance et trust.
- Extrait d'audit d'une activation acceptee et d'un refus.

### GAME-TKT-019 — Retro Room + snapshot comparatif

Priorite: P2

Exigences ciblees: F10, F26

Objectif:

Donner un espace retrospectif capable de comparer deux etats de run, deux snapshots ou deux iterations d'un meme ticket.

Scope:

- Generer et charger des snapshots comparables du board, des taches et des alertes.
- Afficher un diff lisible sur decisions, blocages, output et progression.
- Relier les ecarts a des traces, tickets et evidence refs.
- Rendre la retro room exploitable en challenge, post-mortem ou revue d'experimentation.

Criteres d'acceptation:

- Deux snapshots peuvent etre compares sans ambiguite semantique.
- Les differences critiques remontent avec un focus resolvable.
- La lecture comparative reste stable en replay ou apres reload.

Evidence attendue:

- Tests d'integration sur generation et comparaison de snapshots.
- Capture d'une retro room avec diff explicite.
- Extrait d'evidence reliant un ecart a une trace ou a un ticket.

### GAME-TKT-020 — Spectator mode read-only + surface VS Code

Priorite: P2

Exigences ciblees: F15, F19

Objectif:

Ouvrir une lecture partageable et strictement read-only du board, compatible avec une surface VS Code et l'enveloppe runtime critique minimale.

Scope:

- Generer des tokens spectateur strictement lecture seule.
- Exposer une surface read-only utilisable depuis le web et VS Code.
- Bloquer toutes les mutations cote serveur et cote UI pour ce mode.
- Garantir une projection read-only stable apres reconnect et replay borne.

Criteres d'acceptation:

- Un token spectateur ne peut produire aucune mutation directe ou indirecte.
- La lecture read-only reste coherente apres reconnexion.
- Les diagnostics VS Code exposes n'ajoutent aucune nouvelle surface d'ecriture.

Evidence attendue:

- Tests d'integration sur token spectateur et refus 403 sur mutation.
- Capture de la banniere et de la surface read-only active.
- Extrait de logs montrant les refus de mutation en mode spectateur.

### GAME-TKT-050 — Reviews externes -> Evidence Pack cockpit

Priorite: P1

Exigences ciblees: AX-12, AX-10

Objectif:

Normaliser les reviews, checks et commentaires externes pour en faire des preuves consultables dans le cockpit sans dependre de l'outil d'origine.

Scope:

- Mapper review, commentaire, status check et verdict externe sur `Review Artifact`.
- Relier chaque artefact de review a `traceId`, `taskId`, `subjectRef` et `evidenceRefs`.
- Exposer ces elements dans `audit-view`, `verification-view` et le cockpit.
- Supporter le replay de la review importee sans perte de semantique.

Criteres d'acceptation:

- Une review externe se relit depuis le cockpit sans parser l'UI source.
- Les findings externes sont relies a la meme causalite que le run concerne.
- Une review importee peut servir d'evidence ref dans une verification critique.

Evidence attendue:

- Tests d'integration sur import `review -> evidence pack -> cockpit`.
- Capture cockpit montrant une review externe resolue dans le meme focus qu'un run.
- Extrait d'audit reliant `Review Artifact`, `traceId` et `taskId`.

### GAME-TKT-051 — Host Bridge generique + surface multi-host

Priorite: P1

Exigences ciblees: AX-12

Objectif:

Generaliser le pont VS Code en `Host Bridge` multi-host capable de presenter Copilot, Claude et hotes MCP-compatibles avec la meme semantique runtime.

Scope:

- Exposer bindings, capabilities, routines actives et health des hotes dans les read models runtime.
- Relier les etats `online`, `stale`, `degraded`, `blocked` au cockpit et a l'audit.
- Garder web, VS Code et hotes externes alignes sur la meme causalite de run.
- Bloquer toute divergence semantique entre la surface multi-host et le cockpit central.

Criteres d'acceptation:

- Un meme run reste lisible depuis plusieurs hotes sans divergence de focus ni de statut.
- Un hote degrade ou bloque remonte explicitement dans la surface multi-host.
- La surface multi-host n'introduit aucune voie de mutation qui contourne la policy externe.

Evidence attendue:

- Tests d'integration sur health, degrade state et lecture multi-host.
- Capture de surface montrant bindings, capabilities et routines actives.
- Extrait d'audit reliant l'etat d'un host a la policy et au run courant.

### GAME-TKT-044 — Cockpit Live + Inspector multi-PC

Priorite: P1

Objectif:

Donner a l'operateur une surface unique pour lire l'etat du projet actif, de la flotte de noeuds, des claims, des ownerships Git et des preuves de verification sans transcript brut.

Scope:

- Etendre `runtime-dashboard-view` et `runtime-dashboard-ui-view` avec la flotte, les leases et l'ownership Git.
- Introduire `runtime-cockpit-view` comme facade operateur compacte.
- Exposer un focus unique `runId`, `traceId`, `taskId`, `nodeId`, `agentId` pour les panneaux live et les drawers de preuve.
- Reutiliser exclusivement les read models canoniques deja presents dans le runtime.

Criteres d'acceptation:

- L'operateur repond vite a `quel projet est actif`, `quels PCs sont vivants`, `qui travaille sur quoi`, `ou sont les verrous` et `quelle preuve explique le blocage`.
- Aucune card cockpit ne depend d'une source de donnees hors read models runtime canoniques.
- Les alertes critiques sont resolvables vers un focus concret ou une preuve concrete.

Evidence attendue:

- Tests d'integration sur `runtime-cockpit-view`.
- Scenario de lecture operateur couvrant flotte, lease, ownership et verification.
- Capture de parite entre dashboard runtime et cockpit.

### GAME-TKT-045 — Office view minimale + War Room observateur sur memes projections

Priorite: P1

Objectif:

Ajouter une scene spatiale utile pour comprendre handoffs, congestions, blocages et contention d'ownership sans creer un second modele metier.

Scope:

- Introduire `runtime-observer-view` a partir des memes read models que le cockpit.
- Mapper noeuds, claims, handoffs, focus et alertes vers des signaux spatiaux explicites.
- Afficher une war room observateur branchee sur la meme attention queue que le cockpit.
- Interdire toute logique de commande critique exclusive a la scene.

Criteres d'acceptation:

- Un meme run affiche les memes taches, les memes alertes et le meme focus dans le cockpit et dans la scene.
- La scene spatiale rend un incident ou un handoff plus comprehensible sans contredire le cockpit.
- Aucune mutation runtime n'est declenchable uniquement depuis l'observateur.

Evidence attendue:

- Tests d'integration sur `runtime-observer-view`.
- Walkthrough d'incident ou de challenge montrant la valeur ajoutee de la scene.
- Verification de parite cockpit contre observateur.

### GAME-TKT-046 — Command gateway borne + budget de mutation GUI + mode spectateur partageable

Priorite: P1

Objectif:

Encadrer strictement les rares mutations GUI autorisees, avec authz, audit, idempotence et blocage total du mode spectateur.

Scope:

- Introduire `command-gateway.ts` comme point d'entree unique des commandes GUI.
- Formaliser un budget de mutation borne par role et par surface.
- Exiger `idempotencyKey`, audit de succes ou refus et rationale de guardrail pour toute commande critique.
- Generer un mode spectateur partageable strictement read-only.

Criteres d'acceptation:

- Toute mutation GUI autorisee est authz, idempotente, auditee et fail-closed.
- Un token spectateur ne peut produire aucune mutation, directe ou indirecte.
- Toute commande refusee expose une raison actionnable et un audit correlable.

Evidence attendue:

- Tests d'integration sur `command-gateway`.
- Logs de refus et de succes pour chaque commande GUI critique.
- Scenario de partage spectateur sans mutation possible.

---

## 4-bis Tickets transverses detailes (format long)

### GAME-TKT-021 — Gouvernance drift prompts/politiques + suite canari

Priorite: P1

Axe: AX-01

Objectif:

Stabiliser les comportements de decision en detectant automatiquement les regressions induites par les evolutions de prompts et de politiques.

Scope:

- Definir une baseline versionnee des prompts et politiques critiques.
- Construire une suite canari de scenarios de reference rejouables.
- Mesurer le drift de verdict entre baseline et version candidate.
- Bloquer la transition Review -> Done si le drift depasse le seuil configure.

Criteres d'acceptation:

- Toute modification de prompt/politique produit une nouvelle version tracee.
- La suite canari publie un rapport de drift scenario par scenario.
- La gate bloque automatiquement au-dessus du seuil et expose un diagnostic actionnable.

Evidence attendue:

- Registre baseline/version des prompts critiques.
- Rapport canari avec drift avant/apres modification.
- Journal de gate (blocage puis validation apres correction).

---

### GAME-TKT-022 — Runbooks incident + exercices de reprise critiques

Priorite: P1

Axe: AX-02

Objectif:

Assurer une reprise fiable et reproductible sur incidents eventing critiques sans divergence d'etat.

Scope:

- Ecrire des runbooks pour WS indisponible, out-of-order, duplicate, replay partiel, adapter indisponible.
- Definir une checklist standard detection -> containment -> recovery -> verification.
- Executer des exercices de reprise traces sur scenarios critiques.
- Rendre la preuve d'exercice obligatoire dans la review des lots critiques.

Criteres d'acceptation:

- Chaque incident critique dispose d'un runbook executable et verifiable.
- Les exercices produisent une preuve de resync coherent client/serveur.
- Un lot critique ne peut pas passer Done sans preuve de reprise conforme.

Evidence attendue:

- Runbooks versionnes et valides.
- Traces d'exercices avec etat avant/apres recovery.
- Artefact review liant lot critique et exercice de reprise.

---

### GAME-TKT-023 — Qualite memoire/recall + gate obsolescence

Priorite: P1

Axe: AX-03

Objectif:

Reduire le rework et les erreurs de contexte en mesurant la qualite de recall et en bloquant les references obsoletes au-dela d'un seuil.

Scope:

- Definir les metriques de recall (precision) et d'obsolescence.
- Ajouter des marqueurs de fraicheur sur les references memoire.
- Detecter les references obsoletes pendant review/challenge.
- Activer une gate bloquante au-dessus du seuil d'obsolescence.

Criteres d'acceptation:

- Un rapport periodique publie precision recall et taux d'obsolescence.
- Les references obsoletes sont detectees avec localisation explicite.
- La gate bloque automatiquement quand le seuil est depasse.

Evidence attendue:

- Rapport recall/obsolescence sur echantillon reel.
- Rapport de detection des references obsoletes.
- Journal de gate (echec et passage apres remediation).

---

### GAME-TKT-024 — Protocole anti-chambre d'echo pour review/challenge

Priorite: P2

Axe: AX-04

Objectif:

Elever la qualite de decision collective en imposant une contre-review orthogonale sur les livrables critiques.

Scope:

- Definir le protocole de contre-review orthogonale (roles, checklist, sortie attendue).
- Imposer une revue critique independante avant cloture des livrables critiques.
- Tracer objections substantielles, severite et resolution.
- Interdire la cloture sans completion du protocole.

Criteres d'acceptation:

- Chaque livrable critique contient une contre-review tracee.
- Les objections substantielles sont classees et resolues explicitement.
- La transition Done est impossible sans protocole complete.

Evidence attendue:

- Trace de review a deux perspectives independantes.
- Registre objections/resolutions.
- Journal workflow montrant l'application de la contrainte.

---

### GAME-TKT-025 — FinOps agentique (cout/token/latence par ticket)

Priorite: P2

Axe: AX-05

Objectif:

Maitriser la derive economique du systeme multi-agents en suivant cout, tokens et latence par ticket.

Scope:

- Instrumenter cout, tokens et latence par ticket, role et modele.
- Normaliser ces metriques par niveau de complexite.
- Definir des seuils d'alerte de derive.
- Integrer ces indicateurs au rituel review/retro.

Criteres d'acceptation:

- Les metriques sont disponibles a la granularite ticket.
- Une alerte se declenche quand la derive depasse le seuil.
- Les lots critiques incluent un extrait FinOps dans leurs preuves.

Evidence attendue:

- Export metriques cout/token/latence par ticket.
- Journal d'alerte de derive.
- Rapport review incluant les indicateurs normalises.

---

### GAME-TKT-026 — Explicabilite operationnelle via decision cards

Priorite: P2

Axe: AX-06

Objectif:

Rendre chaque decision critique explicable et audit-able pour reduire les ambiguities operatoires.

Scope:

- Definir un schema standard de decision card (contexte, options, choix, rationale, impact, evidence).
- Produire une decision card sur les transitions critiques.
- Exposer les cards dans l'audit trail et les vues operationnelles.
- Bloquer les transitions exigees en absence de decision card.

Criteres d'acceptation:

- Toute transition critique couverte possede sa decision card associee.
- Les decision cards sont consultables et filtrables en audit.
- La gate bloque la transition si la card obligatoire est absente.

Evidence attendue:

- Exemples de decision cards complets.
- Sortie de consultation audit avec filtrage.
- Journal de blocage pour card manquante.

---

### GAME-TKT-027 — Gate conformite licences et provenance assets/plugins

Priorite: P1

Axe: AX-07

Objectif:

Empocher les risques legaux et de supply chain en imposant une conformite stricte de provenance/licence avant merge.

Scope:

- Tenir un registre unique de provenance assets/plugins avec statut de conformite.
- Verifier coherence source/licence/obligations d'attribution.
- Appliquer une gate fail-closed sur tout element non conforme.
- Generer un bundle d'attribution quand requis.

Criteres d'acceptation:

- Chaque asset/plugin est lie a une source et une licence verifiees.
- Toute non-conformite bloque review/merge avec raison explicite.
- Les obligations d'attribution sont produites et referencees.

Evidence attendue:

- Extrait du registre de provenance.
- Rapport de conformite pass/fail.
- Journal de gate bloque puis debloque apres correction.

---

### GAME-TKT-028 — Framework experimentation produit (hypothese/mesure/decision)

Priorite: P3

Axe: AX-08

Objectif:

Transformer les choix produit en decisions mesurables via un cadre d'experimentation standardise.

Scope:

- Definir un template obligatoire (hypothese, metrique, garde-fou, decision).
- Centraliser le suivi des experimentations et de leurs resultats.
- Imposer une decision explicite (adopt, iterate, drop) a la cloture.
- Lier chaque experience aux tickets impactes.

Criteres d'acceptation:

- Aucune experimentation ne peut etre cloturee sans mesure et decision explicite.
- L'historique des experimentations est consultable par ticket et par theme.
- Les decisions sont tracees jusqu'aux mises a jour de backlog.

Evidence attendue:

- Exemples d'experimentations remplies selon le template.
- Export du registre des experimentations.
- Trace decisionnelle experience -> ticket.

---

## 4-ter Tickets de couverture CdC detailes (format long)

### GAME-TKT-029 — Agent Factory complet (create/clone/config/deploy)

Priorite: P1

Exigences ciblees: F11

Objectif:

Rendre l'Agent Factory completement operationnel pour creation, clonage, edition et deploiement in-world.

Scope:

- Creer un flux de creation agent (nom, role, modele, prompt, tools, room).
- Ajouter clonage d'agent sans heritage d'XP/historique runtime.
- Ajouter edition post-deploiement avec regles restart explicites.
- Garantir apparition immediate de l'agent dans la room cible.

Criteres d'acceptation:

- La creation d'un agent depuis l'UI produit un agent exploitable en runtime.
- Le clonage conserve config et retire XP/historique de session.
- Les changements necessitant restart sont bloques tant que restart non confirme.

Evidence attendue:

- Tests e2e creation/clonage/edition/deploiement.
- Captures UI des flux create/clone/config.
- Logs d'audit creation et mutation agent.

---

### GAME-TKT-030 — Configuration gamifiee complete MCP/skills/prompts/tools/hooks

Statut de reference au 2026-04-11:

- La tranche runtime locale bornee est couverte et validee dans `grimoire-kit/apps/grimoire-game`.
- Le ticket ne doit plus etre relu comme un manque runtime ouvert dans le package actuel.
- Si un reliquat demeure sur F12, il doit etre redecoupe comme extension UI/produit distincte.

Priorite: P1

Exigences ciblees: F12

Objectif:

Completer la configuration gamifiee pour couvrir l'ensemble MCP, skills, prompts, tools et hooks avec persistance fiable et garde-fous explicites sur les surfaces d'execution.

Scope:

- Exposer edition MCP/skills/prompts/tools/hooks dans l'UI game.
- Afficher provenance, trust status, policy minimale et niveau de risque sur tout noeud activable du scope.
- Valider les schemas de configuration avant sauvegarde.
- Synchroniser les changements avec la configuration grimoire-kit.
- Tracer qui a modifie quoi et quand.

Criteres d'acceptation:

- Tous les blocs de configuration cibles sont editables sans passage terminal.
- Aucune activation UI ne passe sans metadata minimale et sans policy explicite.
- Une configuration invalide est rejectee avec diagnostic actionnable.
- La persistence reste coherente apres restart du board.

Evidence attendue:

- Tests integration UI -> config -> reload.
- Extrait de matrice risque/policy pour le scope de configuration livre.
- Extraits de configuration avant/apres edition.
- Journal d'audit des mutations.

---

### GAME-TKT-038 — Chaine de verification orientee AIVS sur transitions critiques

Statut de reference au 2026-04-11:

- La tranche runtime locale bornee est couverte et validee dans `grimoire-kit/apps/grimoire-game`.
- Les dependances qui pointent vers `GAME-TKT-038` peuvent le considerer comme satisfait localement.

Priorite: P1

Axe: AX-10

Objectif:

Rendre chaque verdict de verification reconstructible a posteriori sans enquete manuelle hors du board.

Scope:

- Enrichir les transitions critiques et les evenements `VERIFICATION_GATE` avec acteur, action, correlation, controles executes, verdict et references de preuve.
- Conserver ces metadonnees au replay et dans les vues review, investigation et explicabilite.
- Bloquer les transitions critiques si la chaine minimale de verification est incomplete.
- Produire un export de preuve structurellement reliable a l'audit trail.

Criteres d'acceptation:

- Un reviewer peut reconstruire action -> controles -> verdict -> evidence ref depuis le board et l'audit log.
- Une transition critique avec chaine incomplete reste bloquee avec raison explicite.
- Le replay conserve les references de verification sans duplication ni perte de causalite.

Evidence attendue:

- Tests de workflow verification gate/replay.
- Extraits d'audit log enrichis.
- Exemple d'export de preuve relie a une transition critique.

---

### GAME-TKT-031 — Systeme sonore in-world + controles SFX/musique/volume

Priorite: P2

Exigences ciblees: F16

Objectif:

Mettre en place un systeme audio exploitable en production avec categories de sons et controles utilisateur.

Scope:

- Brancher les sons par evenement critique (task done, erreur, challenge, message).
- Ajouter ambiance par room et controle volume global.
- Ajouter toggles SFX/musique/ambiance independants.
- Garantir mode silencieux strict en spectateur si configure.

Criteres d'acceptation:

- Les sons cibles se declenchent aux bons evenements sans doublons.
- Les controles audio sont persistants et reappliques au redemarrage.
- Le mode mute total coupe tout flux audio sans fuite.

Evidence attendue:

- Tests d'integration audio events.
- Capture des controles HUD audio.
- Export de configuration audio persistante.

---

### GAME-TKT-032 — Progression XP + achievements + persistence SQLite

Priorite: P2

Exigences ciblees: F17

Objectif:

Activer une progression gamifiee mesurable par agent avec persistance robuste.

Scope:

- Attribuer XP par type d'action agentique.
- Calculer niveau et debloquer achievements.
- Persister XP, niveau, achievements en SQLite.
- Exposer la progression dans HUD et panneaux agent.

Criteres d'acceptation:

- Chaque action eligibile credite l'XP attendue sans doublon.
- Le niveau est recalculable et stable apres restart/reload.
- Les achievements debloques restent consultables dans le temps.

Evidence attendue:

- Tests unitaires sur calcul XP/level.
- Tests integration persistence/restart.
- Extraits DB avant/apres progression.

---

### GAME-TKT-033 — Tutoriel onboarding first-run + resume/skip

Priorite: P2

Exigences ciblees: F18

Objectif:

Fournir un onboarding first-run guide, interruptible et non intrusif pour le cycle de decouverte du board.

Scope:

- Implementer un tutoriel interactif en 5 etapes.
- Ajouter skip global et reprise apres interruption.
- Persister l'etat onboarding_done et onboarding_step.
- Ajouter relance manuelle depuis aide/HUD.

Criteres d'acceptation:

- Le tutoriel se lance automatiquement au premier demarrage uniquement.
- Un skip stoppe definitivement la relance automatique.
- La reprise post-interruption restaure l'etape correcte.

Evidence attendue:

- Tests e2e first-run/skip/resume.
- Captures des etapes onboarding.
- Extrait de persistence localStorage/state store.

---

### GAME-TKT-034 — Investigation Lab 4 phases + cycle review code bloqueur

Priorite: P1

Exigences ciblees: F24, F27

Objectif:

Rendre obligatoire un flux de debug systematique et un cycle de review bloqueur selon severite.

Scope:

- Imposer les 4 phases debug (root cause, pattern, hypothesis, implementation).
- Bloquer FIX_PROPOSED sans ROOT_CAUSE_IDENTIFIED.
- Ajouter cycle review avec severites critical/important/minor.
- Bloquer progression Kanban tant qu'un critical reste non resolu.

Criteres d'acceptation:

- Les transitions de phase sont tracees et non contournables.
- Un critical non resolu empeche passage a l'etape suivante.
- Trois fix_failed consecutifs declenchent escalation architecture.

Evidence attendue:

- Tests workflow debug/review.
- Logs de blocage et deblocage par severite.
- Extrait d'alerte architecture review required.

---

### GAME-TKT-035 — Branch Finisher + Security Audit Room in-world

Statut de reference au 2026-04-11:

- La tranche runtime locale est deja couverte par les projections branch finisher et audit securite actuellement presentes dans le runtime.
- Aucun delta runtime borne supplementaire n'est ouvert en l'etat dans le package courant.
- Un reliquat in-world ou UI riche devrait etre redecoupe explicitement avant toute reouverture.

Priorite: P1

Exigences ciblees: F28, F29

Objectif:

Fermer le cycle de branche avec ceremonies explicites et audit securite in-world bloqueur sur findings critiques.

Scope:

- Implementer les 4 options fin de branche (merge/pr/keep/discard) avec confirmation typed discard.
- Verifier tests avant toute option destructive.
- Ajouter Security Audit Room avec controles OWASP/STRIDE + OWASP Agentic Skills et seuil de confiance.
- Creer automatiquement des cartes Kanban securite a partir des findings.

Criteres d'acceptation:

- Les options de cloture respectent strictement la matrice d'actions prevues.
- Un finding securite critique bloque le ship tant qu'il n'est pas traite.
- Une surface d'execution sans provenance ou policy explicite remonte comme finding bloquant du scope.
- Chaque finding publie comporte scenario d'exploit et severite.

Evidence attendue:

- Scenarios e2e fin de branche (1,2,3,4).
- Rapport d'audit securite avec severites.
- Extrait de matrice surfaces d'execution -> findings securite.
- Tickets securite auto-generes traces dans le board.

---

### GAME-TKT-036 — Couverture slots CdC manquants (F01/F02/F03/F19/F21/F22)

Priorite: P1

Exigences ciblees: F01, F02, F03, F19, F21, F22

Objectif:

Fermer les derniers slots de couverture CdC identifies dans la matrice sur moteur, espaces, agents, spectateur et worktrees.

Scope:

- Ajouter editeur map avec undo/redo, grille extensible et contraintes taille.
- Completer decorations team-aware et controles de visite inter-team.
- Completer surfaces etats agents (barres, liens parent/enfant, details runtime).
- Finaliser mode spectateur tokenise avec partage one-click read-only strict.
- Completer desks-as-directories et icones flottantes associees.
- Completer lifecycle worktree room et actions murales de cloture.

Criteres d'acceptation:

- Chaque slot manquant est relie a un test explicite et un comportement observable.
- Les contraintes read-only spectateur sont verifiees en test negatif.
- Le mapping desk->directory est visible, persistant et non ambigu.

Evidence attendue:

- Matrice de tests slot par slot (F01/F02/F03/F19/F21/F22).
- Captures UI/room montrant les comportements cibles.
- Journaux d'audit des transitions et permissions associees.

---

### GAME-TKT-039 — Pilote UMF borne pour runtime, replay, spectateur et multi-sessions

Statut de reference au 2026-04-11:

- La tranche runtime locale est deja couverte par le pilote borne d'enveloppe canonique et ses projections associees.
- Le ticket reste un marqueur experimental; il ne doit pas etre rouvert sans delta UMF explicite et borne.

Priorite: P2

Axe: AX-11

Objectif:

Valider une enveloppe canonique de message sur un perimetre borne sans destabiliser les contrats runtime existants.

Scope:

- Definir un sous-ensemble d'enveloppe commune pour les evenements critiques du pilote.
- Mapper runtime, replay, spectateur et vues multi-sessions sur cette enveloppe via projections ou adapters explicites.
- Conserver la compatibilite avec les payloads existants pendant le pilote.
- Documenter clairement le caractere experimental, les non-claims et les limites de couverture.

Criteres d'acceptation:

- Au moins deux surfaces critiques lisent la meme enveloppe commune sans divergence semantique visible.
- Les tests de compatibilite et d'interoperabilite du pilote passent.
- Le pilote reste optionnel et n'introduit pas de regression sur les contrats deja stabilises.

Evidence attendue:

- Spec du pilote avec champs communs et mapping des surfaces.
- Exemples de payloads avant/apres projection.
- Tests d'interoperabilite runtime/replay/spectateur.

---

## 4-ter. Paquet Sprint S9 (execution locale)

Ce paquet convertit le brief [SPRINT-S09-grimoire-game.md](./SPRINT-S09-grimoire-game.md) en tickets d'execution locaux. Il ne remplace pas le backlog global. Il borne simplement l'engagement du sprint sous les tickets parents deja portes par le board principal.

Mise a jour de reference au 2026-04-11:

- La tranche runtime locale de `GAME-TKT-030` est deja couverte et validee dans `grimoire-kit/apps/grimoire-game`.
- `GAME-S09-001` et `GAME-S09-002` restent donc des marqueurs de cadrage S9 et non des tickets runtime encore ouverts dans le package courant.
- `GAME-TKT-038` doit etre traite comme dependance satisfaite localement pour tout reliquat S9 futur.

### 4-ter.1 Board S9

| Ticket | Statut initial | Parent backlog | Nature | Dependances |
| --- | --- | --- | --- | --- |
| GAME-S09-001 | Ready | GAME-TKT-030 | Coeur | GAME-TKT-030 |
| GAME-S09-002 | Backlog | GAME-TKT-030 | Coeur | GAME-S09-001 |
| GAME-S09-005 | Backlog | GAME-TKT-037 | Gate coeur | GAME-S09-001, GAME-S09-002, GAME-TKT-037 |
| GAME-S09-003 | Backlog | GAME-TKT-015 | Coeur | GAME-S09-001, GAME-TKT-015 |
| GAME-S09-004 | Backlog | GAME-TKT-034 | Conditionnel | GAME-S09-002, GAME-S09-003, GAME-S09-005, GAME-TKT-034 |

### GAME-S09-001 — Contrats UI S9 + composants Svelte prioritaires

Statut initial: Ready

Parent backlog: GAME-TKT-030

Objectif:

Geler le socle UI du sprint pour eviter tout drift entre design, integration Svelte et surfaces critiques de configuration ou de challenge.

Scope:

- Produire la direction visuelle retenue pour S9 et figer les contrats UI utiles au sprint.
- Livrer les composants Svelte reutilisables necessaires aux panels et modals critiques.
- Valider le reflow, la lisibilite et l'affichage securise du contenu agentique.

Criteres d'acceptation:

- Les composants cibles sont integrables sans divergence de structure entre mockup et implementation.
- Le rendu reste correct sur les resolutions cibles du board.
- Les contrats UI sont suffisamment figes pour lancer les tickets coeur suivants sans reouverture de scope.

Evidence attendue:

- Artefact design retenu et composants cibles identifies.
- Captures ou preuves UI des panels/modals prioritaires.
- Check-list de contrats UI figes pour S9.

### GAME-S09-002 — Skill tree MCP/skills connecte a la config reelle

Statut initial: Backlog

Parent backlog: GAME-TKT-030

Objectif:

Livrer la premiere verticale de configuration gamifiee avec persistence reelle, recharge propre et diagnostic exploitable en cas d'incoherence.

Scope:

- Exposer le skill tree MCP/skills en UI game.
- Synchroniser activation ou desactivation avec la configuration Grimoire reelle.
- Preparer les noeuds du scope S9 a afficher provenance, trust status et policy minimale.
- Verifier la persistence et le rechargement sans divergence visible.

Criteres d'acceptation:

- Une activation ou desactivation modifie la vraie configuration sans edit manuel hors UI.
- Un rechargement restitue le meme etat observable.
- Une configuration invalide est refusee avec diagnostic actionnable.

Evidence attendue:

- Tests integration UI -> config -> reload.
- Extraits de configuration avant/apres mutation.
- Journal d'audit des changements config lies au sprint.

### GAME-S09-005 — Garde-fous OWASP sur les activations du skill tree S9

Statut initial: Backlog

Parent backlog: GAME-TKT-037

Objectif:

Empêcher qu'une surface d'execution livree dans S9 soit activable sans policy, provenance et trust status minimaux.

Scope:

- Afficher sur les noeuds MCP/skills du scope S9 un badge de provenance, un trust status et un niveau de risque.
- Refuser toute activation ou desactivation si la policy minimale attendue est absente.
- Journaliser la raison du refus ou de l'autorisation dans l'audit trail du sprint.

Criteres d'acceptation:

- Un noeud non qualifie ne peut pas etre active depuis l'UI.
- Les badges de governance sont visibles sur les noeuds du scope livre.
- Les refus et autorisations sont auditables sans lecture terminale supplementaire.

Evidence attendue:

- Tests UI sur activation autorisee/refusee.
- Captures du skill tree avec badges de governance.
- Journal d'audit des decisions d'activation du sprint.

### GAME-S09-003 — Selecteur challenge + variantes Investigation, DX Review, Auto-Challenge

Statut initial: Backlog

Parent backlog: GAME-TKT-015

Objectif:

Etendre la Challenge Room avec les trois variantes prevues sans ouvrir prematurement la tranche suivante de gouvernance avancee.

Scope:

- Ajouter le selecteur de type de challenge dans la surface de convocation.
- Supporter les variantes Investigation, DX Review et Auto-Challenge.
- Garder le perimetre strictement borne aux transitions et pipelines prevus par le sprint.

Criteres d'acceptation:

- Chaque variante se declenche selon son type sans ambigute de pipeline.
- La modal de challenge ne regresse pas sur le flux nominal existant.
- Les transitions de variante restent traçables dans les journaux et surfaces associees.

Evidence attendue:

- Tests d'activation des trois variantes.
- Captures UI du selecteur et des etats principaux.
- Traces de pipeline nominales pour Investigation, DX Review et Auto-Challenge.

### GAME-S09-004 — Investigation Lab + Verification Gate tranche S9

Statut initial: Backlog

Parent backlog: GAME-TKT-034

Condition d'ouverture:

Ce ticket n'ouvre que si GAME-S09-002 et GAME-S09-003 sont verts, et si le socle debug ou challenge necessaire ne presente pas de blocage structurel.

Objectif:

Ouvrir la premiere tranche executable de l'Investigation Lab et de la Verification Gate, sans embarquer tout le cycle review avance du backlog global.

Scope:

- Imposer les 4 phases de debug prevues pour le sprint.
- Bloquer FIX_PROPOSED tant que la root cause n'est pas etablie.
- Bloquer DONE tant que la verification n'a pas produit une evidence exploitable.

Criteres d'acceptation:

- Les phases de debug sont visibles, tracees et non contournables.
- FIX_PROPOSED reste bloque sans root cause et DONE reste bloque sans verification.
- L'audit log produit par la gate est lisible et exploitable en review.

Evidence attendue:

- Tests workflow debug et verification gate.
- Extraits du verification log du sprint.
- Preuve de blocage puis de deblocage sur un cas nominal.

### 4-ter.2 Ordre de passage S9

1. GAME-S09-001
2. GAME-S09-002
3. GAME-S09-005
4. GAME-S09-003
5. Revue go/no-go S9
6. GAME-S09-004 uniquement si go/no-go positif

### 4-ter.3 Gates de pilotage S9

- Gate S9-1 : contrats UI figes et composants critiques integrables.
- Gate S9-2 : configuration MCP/skills persistante et rechargee sans drift.
- Gate S9-2b : aucune activation du scope S9 ne passe sans provenance, trust status et policy minimale visibles.
- Gate S9-3 : variantes de challenge declenchees sans regression du flux nominal.
- Gate S9-4 : Investigation Lab et Verification Gate bloquent proprement sans contournement.

### 4-ter.4 Statuts de lancement recommandes

- Reference 2026-04-11: tant qu'aucun reliquat S9 explicite n'est redecoupe, `GAME-S09-001` et `GAME-S09-002` ne doivent pas etre interpretes comme travail runtime restant a ouvrir; la tranche locale correspondante est deja couverte.
- Avant kickoff: `GAME-S09-001` reste `Ready`; `GAME-S09-002`, `GAME-S09-005`, `GAME-S09-003` et `GAME-S09-004` restent `Backlog`.
- Au lancement effectif du sprint: `GAME-S09-001` passe `In Progress`; les autres tickets conservent leur statut initial.
- Quand `Gate S9-1` est vert: `GAME-S09-001` passe `Review`; `GAME-S09-002` passe `Ready`.
- Quand `Gate S9-2` est vert: `GAME-S09-002` passe `Review`; `GAME-S09-005` passe `Ready`.
- Quand `Gate S9-2b` est vert: `GAME-S09-005` passe `Review`; `GAME-S09-003` passe `Ready`.
- Ordre recommande au coeur du sprint: ouvrir `GAME-S09-002` en `In Progress`, puis `GAME-S09-005`, puis `GAME-S09-003` quand le contrat de modal ne bouge plus.
- `GAME-S09-004` reste `Backlog` tant que la revue go/no-go n'est pas positive; il passe `Ready` puis `In Progress` seulement apres ce verdict.

### 4-ter.5 Artefacts de lancement et de decision

- Kickoff court: [KICKOFF-S09-grimoire-game.md](./KICKOFF-S09-grimoire-game.md)
- Gate conditionnelle `GAME-S09-004`: [GO-NO-GO-S09-004-grimoire-game.md](./GO-NO-GO-S09-004-grimoire-game.md)

---

## 5. Ordre de prise recommande

1. GAME-TKT-001
2. GAME-TKT-002
3. GAME-TKT-003
4. GAME-TKT-004
5. GAME-TKT-037
6. GAME-TKT-005
7. GAME-TKT-006
8. GAME-TKT-007
9. GAME-TKT-009
10. GAME-TKT-008
11. GAME-TKT-010
12. GAME-TKT-038
13. GAME-TKT-011
14. GAME-TKT-012
15. GAME-TKT-013
16. GAME-TKT-014
17. GAME-TKT-015
18. GAME-TKT-016
19. GAME-TKT-017
20. GAME-TKT-018
21. GAME-TKT-019
22. GAME-TKT-020
23. GAME-TKT-021
24. GAME-TKT-022
25. GAME-TKT-023
26. GAME-TKT-027
27. GAME-TKT-024
28. GAME-TKT-025
29. GAME-TKT-026
30. GAME-TKT-028
31. GAME-TKT-029
32. GAME-TKT-030
33. GAME-TKT-034
34. GAME-TKT-036
35. GAME-TKT-031
36. GAME-TKT-032
37. GAME-TKT-033
38. GAME-TKT-035
39. GAME-TKT-039
