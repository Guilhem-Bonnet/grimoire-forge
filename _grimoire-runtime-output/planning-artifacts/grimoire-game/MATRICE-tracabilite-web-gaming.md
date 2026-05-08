# Matrice de Tracabilite — Grimoire Game Web/Gaming

> Projet : **Grimoire Game**
> Sources : [CdC](./CdC-grimoire-game.md), [PLAN](./PLAN-implementation-web-gaming.md), [TICKETS](./TICKETS-web-gaming.md), [CONTRAT](./CONTRAT-runtime-agentic-guardrails.md), [MATRICE guardrails](./MATRICE-verification-agentic-guardrails-web-gaming.md), [CONTRAT host bridge](./CONTRAT-host-bridge-agentique-externe.md), [MATRICE host bridge](./MATRICE-verification-host-bridge-agentique-externe.md)
> Statut : matrice de pilotage (couverture planifiee, preuves a produire a l'execution)

---

## 1. Objectif

Relier chaque exigence du CdC aux tickets d'execution, aux verifications attendues et aux preuves minimales requises avant transition vers Done.

Niveaux de couverture utilises:

- **Couverte** : ticket(s) explicite(s) + verification(s) definie(s)
- **Partielle** : intention couverte mais sous-exigences manquantes ou implicites
- **Non couverte** : aucun ticket explicite dans le backlog actuel

---

## 2. Exigences fonctionnelles (F01 -> F30)

| Exigence | Tickets lies | Verification prevue | Evidence attendue | Couverture |
| --- | --- | --- | --- | --- |
| F01 — Moteur pixel art | GAME-TKT-005, 006, 007, 009, 010, 036 | Tests reducers/hydration, determinisme ECS, pathfinding/collision, budget frame, manifests assets, contraintes editeur map | Rapports tests + profiling + journal loader assets + preuves editeur map | Couverte |
| F02 — Espaces par team | GAME-TKT-007, 013, 017, 036 | Scenarios multi-room, deplacements inter-room, controles d'acces et decor team-aware | Scenarios de navigation + logs d'autorisation + captures rooms team | Couverte |
| F03 — Representation agents | GAME-TKT-006, 011, 013, 018, 036 | Verification etats animation, clic agent -> panneau, liens visuels, interactions role-based, surfaces etats completes | Tests UI + captures etats agent + logs actions | Couverte |
| F04 — Kanban gamifie | GAME-TKT-012, 008, 010 | Drag/drop, synchro activite -> colonne, gate avant Done | Tests workflow Kanban + verification-log | Partielle |
| F05 — Communication inter-agents | GAME-TKT-013, 015 | Visualisation messages/handoffs, reunion inter-teams, tracabilite complete | Journal communications + preuves challenge | Partielle |
| F06 — Connaissances et memoire | GAME-TKT-016, 023 | Lecture/ecriture memoire observable, controle recall/obsolescence | Rapport recall/obsolescence + traces memoire | Partielle |
| F07 — Parallelisme | GAME-TKT-006, 011, 013 | Execution simultanee visible, controle pause/restart, coherence runtime | Logs d'activite parallele + tests stabilite | Partielle |
| F08 — Visualisation workflows | GAME-TKT-014, 026 | Chemin workflow visible, step courant, historique decisions auditable | Historique workflow + decision cards | Couverte |
| F09 — Console debug gamifiee | GAME-TKT-011, 020, 010 | Logs filtrables par agent/evenement, diagnostics visibles, traces outils | Sorties diagnostics + logs filtres | Partielle |
| F10 — Challenge Room | GAME-TKT-015, 024, 028 | Cycle challenge complet, contre-review, cloture par decision explicite | Logs challenge + registre objections + trace decisionnelle | Partielle |
| F11 — Agent Factory | GAME-TKT-029 | Creation/clonage/configuration agent en UI + apparition in-world | Scenarios creation/clonage/deploiement + persistence config | Couverte |
| F12 — Configuration gamifiee | GAME-TKT-018, 027, 030, 037 | Configuration MCP/skills/prompts/tools/hooks via UI + persistence + garde-fous activation | Tests UI config + badges governance + preuves synchro config | Couverte |
| F13 — Orchestrateur special | GAME-TKT-011 (partiel) | Interface dediee, droits exclusifs de gouvernance, monitoring global | Tests RBAC orchestrateur + traces dispatch global | Partielle |
| F14 — Integration grimoire-kit | GAME-TKT-002, 020, 039, 047, 048, 051 | Bridge agnostique, host bindings, diagnostics, reviews externes et projection canonique bornee | Tests integration adapter + projections runtime/replay + snapshots capability manifests + preuves host bridge | Couverte |
| F15 — Integration VS Code (optionnel) | GAME-TKT-020, 039, 051 | Surface telemetry/diagnostics en lecture controlee, bindee comme un host parmi d'autres, et projection stable | Extraits diagnostics affiches + tests read-only + projection commune + etat host bridge | Couverte |
| F16 — Systeme sonore | GAME-TKT-031 | SFX/music par evenement + controles volume/mute | Tests audio + scenarios room-based | Couverte |
| F17 — Progression XP | GAME-TKT-032 | Attribution XP, barre progression, achievements, persistence | Tests progression + preuve persistence | Couverte |
| F18 — Tutoriel onboarding | GAME-TKT-033 | Tutoriel premier demarrage, skip, non-relance | Tests etat first-run + traces completion/skip | Couverte |
| F19 — Mode spectateur | GAME-TKT-020, 004, 036, 039 | Token lecture seule, interdiction mutation, partage controle, projection canonique bornee | Tests auth/authz + logs refus mutation + projection read-only | Couverte |
| F20 — Retro Room | GAME-TKT-019 | Snapshot comparatif, synthese sprint, consultation historique | Exports snapshot + preuve comparaison | Couverte |
| F21 — Desks as Directories + Deep Inspection | GAME-TKT-011, 017, 036 | Deep inspection complet + liens espace de travail/branche + desk-directory mapping | Tests panneau inspection + traces worktree | Couverte |
| F22 — Worktree Room | GAME-TKT-017, 036 | Creation/suppression room par branche + actions de cloture | Scenarios cycle branche + logs transitions | Couverte |
| F23 — Plugin Power Cards | GAME-TKT-018, 027, 037 | Activation visuelle, persistence, provenance et trust status | Tests activation + registre provenance + refus fail-closed | Couverte |
| F24 — Investigation Lab (4 phases) | GAME-TKT-008, 034 | Loi de fer root-cause, blocage Done, alerte escalation | Tests workflow debug + preuves alerting | Couverte |
| F25 — Verification Gate | GAME-TKT-008, 010, 038 | Emission gate obligatoire, blocage sans preuve, audit trail et chaine de verification complete | verification-log + sorties tests associes + evidence refs | Couverte |
| F26 — Dispatch parallele isole | GAME-TKT-006, 013 (partiel) | Parallel sprint, isolation contexte, detection conflits integration | Logs dispatch + rapport conflits/resolution | Partielle |
| F27 — Cycle review code | GAME-TKT-015, 024, 034 | Review automatisee, tri severite, blocage critiques non resolues | Rapport review + preuve resolution findings | Couverte |
| F28 — Branch Finisher | GAME-TKT-017, 035 | Verification tests avant cloture + options merge/pr/keep/discard | Logs cloture branche + preuve confirmations | Couverte |
| F29 — Security Audit Room | GAME-TKT-004, 027, 035, 037, 038 | Couverture OWASP/STRIDE/Agentic Skills + findings exploitables + cartes auto + gaps de policy | Rapport audit securite + tickets derives + matrice surfaces -> findings | Couverte |
| F30 — Design Forge | GAME-TKT-028 (partiel) | Workflow design/decision DX trace jusqu'au backlog | Registre experimentations + decisions produit | Partielle |

---

## 3. Exigences non-fonctionnelles (NFR)

| Exigence NFR | Tickets lies | Verification prevue | Evidence attendue | Couverture |
| --- | --- | --- | --- | --- |
| Performance (4.1) | GAME-TKT-006, 010, 025 | Profiling scheduler, budget frame, suivi latence/token/cout | Rapport profiling + rapport FinOps | Couverte |
| Accessibilite/compatibilite (4.2) | GAME-TKT-020 (partiel) | Verification mode lecture mobile + compatibilite navigateurs | Campagne compatibilite + check UX mobile | Partielle |
| Securite (4.3) | GAME-TKT-004, 020, 027, 037, 038, 047, 048, 049 | Auth WS/API, RBAC, provenance/licences, verification chain, mode read-only strict et policy fail-closed des hotes externes | Tests auth/authz + rapports conformite + logs refus + evidence refs + journaux de policy host bridge | Couverte |
| Maintenabilite (4.4) | GAME-TKT-001, 002, 010, 039 | Contrats explicites, boundary adapter stable, projections additives et non-regression outillee | Tests contrat/integration + quick-check/lint/tests + compatibilite pilote | Couverte |
| Extensibilite (4.5) | GAME-TKT-002, 009, 018, 037, 039, 047, 048, 051 | Extension via adapter boundary, host bridge canonique, pipeline assets/plugins gouvernes et enveloppe pilote bornee | Tests adapter mock + registres assets/plugins + mapping pilote + surfaces multi-host | Couverte |

---

## 4. Axes transverses (AX-01 -> AX-08)

| Axe transverse | Ticket associe | Verification minimum | Evidence attendue | Couverture |
| --- | --- | --- | --- | --- |
| AX-01 — Drift prompts/politiques | GAME-TKT-021 | Suite canari + seuil de drift bloquant | Rapport drift + journal de gate | Couverte |
| AX-02 — Reprise incident | GAME-TKT-022 | Runbooks + exercices de reprise + preuve de resync | Runbooks versionnes + traces recovery | Couverte |
| AX-03 — Memoire/recall | GAME-TKT-023 | Metriques precision/obsolescence + gate | Rapport recall + journal de gate | Couverte |
| AX-04 — Anti-chambre d'echo | GAME-TKT-024 | Contre-review orthogonale obligatoire | Registre objections/resolutions | Couverte |
| AX-05 — FinOps agentique | GAME-TKT-025 | Cout/token/latence par ticket + seuils derive | Export metriques + alertes derive | Couverte |
| AX-06 — Explicabilite | GAME-TKT-026 | Decision cards obligatoires sur transitions critiques | Cards + audit filtrable + journal blocage | Couverte |
| AX-07 — Licences/provenance | GAME-TKT-027 | Gate fail-closed conformite assets/plugins | Registre provenance + rapport pass/fail | Couverte |
| AX-08 — Experimentation produit | GAME-TKT-028 | Template hypothese/mesure/decision obligatoire | Registre experimentations + trace decisionnelle | Couverte |
| AX-09 — Gouvernance OWASP Agentic Skills | GAME-TKT-037 | Registre surfaces + policy minimale + trust status + refus fail-closed | Matrice surfaces -> controles -> gates + audit des activations | Couverte |
| AX-10 — Verification integrity | GAME-TKT-038 | Chaine action -> controles -> verdict -> evidenceRef | verification-view + audit-view + replay stable | Couverte |
| AX-11 — Canonical message envelope | GAME-TKT-039 | Projection pilote runtime/replay/spectateur/multi-session | Mapping avant/apres + tests d'interoperabilite | Couverte |
| AX-12 — Connectivite hotes externes | GAME-TKT-047, 048, 049, 050, 051 | Registre des hotes, policy engine, reviews importees et surface multi-host | Manifests de capabilities + journaux de policy + review artifacts + projections host bridge | Couverte |

---

## 5. Ecarts convertis en tickets (etat courant)

Les ecarts prioritaires ont ete convertis dans le backlog operationnel.

1. **F11** -> GAME-TKT-029 (Agent Factory complet).
2. **F12** -> GAME-TKT-030 (Configuration gamifiee complete).
3. **F16/F17/F18** -> GAME-TKT-031, GAME-TKT-032, GAME-TKT-033.
4. **F24/F27** -> GAME-TKT-034.
5. **F28/F29** -> GAME-TKT-035.
6. **F01/F02/F03/F19/F21/F22 (slots manquants)** -> GAME-TKT-036.
7. **Gouvernance des surfaces d'execution** -> GAME-TKT-037.
8. **Verification d'integrite des transitions critiques** -> GAME-TKT-038.
9. **Enveloppe canonique pilote pour lectures critiques** -> GAME-TKT-039.
10. **Modele canonique des hotes externes** -> GAME-TKT-047.
11. **Contrats runtime des hotes externes** -> GAME-TKT-048.
12. **Policy engine des connecteurs externes** -> GAME-TKT-049.
13. **Reviews externes normalisees en evidence** -> GAME-TKT-050.
14. **Host Bridge generique et surface multi-host** -> GAME-TKT-051.

Points encore partiels a monitorer en priorite suivante: F13, F14, F15, F26, F30.

---

## 6. Verification detaillee Slice 6 (GAME-TKT-029 -> GAME-TKT-036)

La verification operationnelle ticket par ticket est definie dans:

- [MATRICE-verification-slice6-web-gaming.md](./MATRICE-verification-slice6-web-gaming.md)
- [SUITE-tests-slice6-web-gaming.md](./SUITE-tests-slice6-web-gaming.md)

Le perimetre guardrails agentiques est defini dans:

- [MATRICE-verification-agentic-guardrails-web-gaming.md](./MATRICE-verification-agentic-guardrails-web-gaming.md)
- [SUITE-tests-agentic-guardrails-web-gaming.md](./SUITE-tests-agentic-guardrails-web-gaming.md)

Le perimetre Host Bridge agentique externe est defini dans:

- [MATRICE-verification-host-bridge-agentique-externe.md](./MATRICE-verification-host-bridge-agentique-externe.md)
- [SUITE-tests-host-bridge-agentique-externe.md](./SUITE-tests-host-bridge-agentique-externe.md)

Cet artefact complete cette matrice de tracabilite en explicitant, pour GAME-TKT-029 a GAME-TKT-036, les scenarios obligatoires, les gates bloquantes et les preuves minimales avant Done.

---

## 7. Regle d'usage

Cette matrice est une reference de pilotage:

- elle ne remplace pas les preuves d'execution,
- elle impose un lien explicite exigence -> ticket -> verification -> evidence,
- elle doit etre mise a jour a chaque ajout/split/merge de ticket.
