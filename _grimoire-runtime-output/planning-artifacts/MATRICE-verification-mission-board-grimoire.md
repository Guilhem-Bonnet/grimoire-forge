# Matrice de Verification Detaillee - Mission Board Grimoire

> Projet : **Grimoire**
> Perimetre : contracts, routage, hooks, projections board, verification, supervision, wireframes et discipline de contexte
> Sources : [SPEC](./SPEC-mission-board-grimoire.md), [CONTRAT](./CONTRAT-mission-board-grimoire.md), [PLAN](./PLAN-implementation-mission-board-grimoire.md), [SUITE](./SUITE-tests-mission-board-grimoire.md)

---

## 1. Objectif

Definir les verifications obligatoires, les gates bloquantes et les preuves minimales avant toute transition vers `Done` pour le front `Mission Board`.

## 2. Regles de gate

- Aucun ticket de ce perimetre ne passe `Done` sans preuve exploitable et rattachee a un contrat, une projection ou un scenario e2e.
- Toute verification negative sur un gate bloquant maintient le ticket en `Review` ou `Blocked`.
- Les claims sur la lecture du board, le routage ou la cloture doivent rester rejouables sans inspection manuelle d'une UI seule.
- La discipline memoire, contexte et tokens est un gate produit et non un bonus UX.

## 3. Matrice Ticket -> Verification -> Evidence

| Ticket ou paquet | Verifications obligatoires | Gates bloquantes | Evidence minimale attendue |
| --- | --- | --- | --- |
| `GTA-TKT-001` + `GTA-TASK-039` | `MB-V-001` schema `MissionTask` valide ; `MB-V-002` facettes d'etat coherentes ; `MB-V-003` metadata de provenance presentes | `MB-G-001` task sans `requestId`; `MB-G-002` task sans criteria ; `MB-G-003` facettes incoherentes | schemas, payloads valides/invalides, projection stable |
| `GTA-TKT-003` + `GTA-TASK-044` | `MB-V-004` binding task -> recipe ; `MB-V-005` lien workflow instance ; `MB-V-006` resume/reopen sans duplication | `MB-G-004` run sans `workflowInstanceId`; `MB-G-005` rebind qui ecrase l'historique | examples de run, replay, preuves de rebind |
| `GTA-TKT-008` + `GTA-TASK-042` + `GTA-TASK-046` | `MB-V-007` hooks derives d'evenements canoniques ; `MB-V-008` stale detection ; `MB-V-009` escalation avec `nextAction` | `MB-G-006` hook UI-only ; `MB-G-007` stale silencieux ; `MB-G-008` escalation sans cause | logs d'evenements, projections supervision, tests negatifs |
| `GTA-TKT-009` + `GTA-TASK-043` + `GTA-TASK-048` | `MB-V-010` verification gate bloque `done` ; `MB-V-011` mission guard bloque la cloture parent ; `MB-V-012` reject -> reopen causal | `MB-G-009` `done` sans verdict ; `MB-G-010` mission close avec enfant requis ouvert | traces verification, proof pack, scenario e2e |
| `GTA-TKT-011` + `GTA-TASK-045` + `GTA-TASK-047` | `MB-V-013` colonnes derivees ; `MB-V-014` carte compacte lisible ; `MB-V-015` drawer sans surcharge de contexte | `MB-G-011` colonne stockee comme autorite ; `MB-G-012` transcript brut en carte ; `MB-G-013` drawer auto-deep-fetch | snapshots, predicates de colonnes, captures et payloads |
| `GTA-TKT-012` + package UX | `MB-V-016` rooms et commandes alignes ; `MB-V-017` motion semantique mappee aux events ; `MB-V-018` accessibilite focus et reduced motion | `MB-G-014` room sans read model ; `MB-G-015` motion decoractive ; `MB-G-016` action critique sans alternative clavier | wireframes, motion mapping, evidence visuelle, checklist UX |

## 4. Ordre de verification recommande

1. Contracts et projections
2. Routing et hooks
3. Verification et closure guard
4. Supervision et stale handling
5. Rooms, carte, drawer et motion
6. Scenario e2e final

## 5. Checklist de completion

- [ ] Les schemas canoniques valident les payloads critiques.
- [ ] Les colonnes du board sont derivees et replay-safe.
- [ ] Le routage est explicable et overrideable.
- [ ] Les hooks ne dependent pas de la webview.
- [ ] Aucun `done` sans verification acceptee.
- [ ] Aucune mission ne cloture avec un enfant requis ouvert.
- [ ] Les surfaces respectent la discipline de contexte `L1/L2/L3`.
- [ ] La motion reste semantique et optionnelle.

## 6. Statut d'execution courant

| Bloc | Statut | Commentaire |
| --- | --- | --- |
| Contracts | Specifie | Pret pour implementation runtime |
| Routing | Specifie | Matrice minimale definie |
| Hooks | Specifie | Attend integration evenements runtime |
| Verification | Specifie | Closure guard formalise |
| UX et motion | Specifie | Pret pour integration Game UI |
| E2E | Specifie | Scenario final a brancher sur implementation |
