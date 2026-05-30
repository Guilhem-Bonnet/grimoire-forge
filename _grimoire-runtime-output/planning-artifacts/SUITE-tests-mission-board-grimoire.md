# Suite de Tests - Mission Board Grimoire

> Projet : **Grimoire**
> Perimetre : contracts, replay, routage, hooks, verification, supervision, UX causale
> Sources : [MATRICE-verification-mission-board-grimoire.md](./MATRICE-verification-mission-board-grimoire.md), [PLAN-implementation-mission-board-grimoire.md](./PLAN-implementation-mission-board-grimoire.md)

---

## 1. Objectif

Fournir une suite de tests de reference pour verifier le front `Mission Board` de bout en bout, en couvrant les contracts, les projections, les scenarios negatifs et la discipline de contexte.

## 2. Table de suite

| Test ID | Type | Coverage | Description | Commande cible | Evidence attendue |
| --- | --- | --- | --- | --- | --- |
| `MB-T001-CT-01` | CT | `MB-V-001` | Validation du schema `MissionTask` sur payload valide | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/mission-task.contract.test.ts` | payload valide + rapport contrat |
| `MB-T001-CT-02` | CT | `MB-G-001` a `MB-G-003` | Rejets de payloads task invalides | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/mission-task.contract.test.ts -t invalid` | payloads invalides + raisons |
| `MB-T002-CT-01` | CT | `MB-V-004` a `MB-V-006` | Validation du schema `RoutingDecision` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/routing-decision.contract.test.ts` | rapport contrat |
| `MB-T003-CT-01` | CT | `MB-V-007` | Validation du schema `BoardCommandEnvelope` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/board-command.contract.test.ts` | rapport contrat |
| `MB-T004-UT-01` | UT | `MB-V-013` | Projection des colonnes a partir d'etats canoniques | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/board-projection.test.ts` | snapshot des colonnes |
| `MB-T005-UT-01` | UT | `MB-V-008` | Detection de stale et emission d'incident | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/supervision-stale.test.ts` | logs d'incident |
| `MB-T006-UT-01` | UT | `MB-V-010` | Refus de `close_task` sans verification acceptee | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/closure-guard.test.ts -t close_task` | refus explicite |
| `MB-T007-UT-01` | UT | `MB-V-011` | Refus de `close_mission` avec enfant requis ouvert | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/closure-guard.test.ts -t close_mission` | refus explicite |
| `MB-T008-UT-01` | UT | `MB-V-015` | Drawer `L2` sans transcript brut ni deep fetch implicite | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/context-budget.test.ts -t drawer` | payloads drawer compacts |
| `MB-T009-UT-01` | UT | `MB-V-017` | Mapping motion -> evenement canonique | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/motion-mapping.test.ts` | table de mapping verifiee |
| `MB-T010-E2E-01` | E2E | `MB-V-012` + `MB-V-018` | Scenario `create -> qualify -> route -> run -> verify -> close` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/mission-board-e2e.test.ts -t nominal` | evidence pack nominal |
| `MB-T011-E2E-01` | E2E | `MB-G-009` a `MB-G-013` | Scenario negatif `reject -> reopen -> reroute -> verify` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/mission-board-e2e.test.ts -t reject_reopen` | evidence pack negatif |

## 3. Criteres de sortie

- tous les contracts critiques passent ;
- les scenarios negatifs bloquent effectivement la cloture ou la mutation interdite ;
- la projection board reste stable apres replay ;
- la discipline `L1/L2/L3` est observable dans les payloads et captures ;
- les evidence packs permettent la relecture sans UI proprietaire.
