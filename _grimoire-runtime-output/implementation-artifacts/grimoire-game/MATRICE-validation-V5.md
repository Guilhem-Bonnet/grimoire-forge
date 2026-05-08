# Matrice de validation V5 - Agent OS + Game UI

## Objet

Cette matrice consolide le statut des gates V5, les preuves disponibles et le verdict courant.

## Run de reference

- run courant: `RUN-20260414-000430`
- evidence pack: [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430)

## Statut des gates

| Gate | Condition de passage | Statut | Verdict | Evidence principale |
| --- | --- | --- | --- | --- |
| G-V5-01 Runtime canonique | Contrats, correlations et causalite alignees sans drift doc/code | Contrats et projections presentes, alignement canonique encore incomplet | NO-GO | [GO-NO-GO-V5.md](GO-NO-GO-V5.md) |
| G-V5-02 Backbone live | Replay, reconnect, event store et multi-session fiables | Replay/reconnect couverts, control plane live global encore partiel | NO-GO | [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/test.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/test.txt) |
| G-V5-03 Cockpit utile | Audit, verification, session diff et inspection utilisables en exploitation | Capacites cockpit validees en integration sur les surfaces runtime Game UI et Observability, avec generation cockpit et report a partir des memes projections | GO | [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/runtime-surfaces.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/runtime-surfaces.txt), [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/observability-tests.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/observability-tests.txt), [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/cockpit-verify.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/cockpit-verify.txt), [../../../grimoire-kit/apps/grimoire-game/src/state/runtime-dashboard-view.ts](../../../grimoire-kit/apps/grimoire-game/src/state/runtime-dashboard-view.ts) |
| G-V5-04 Mutations fail-closed | Budget write borne, RBAC, audit et mode spectateur prouves | Budget de mutation borne pour `CONFIG_UPDATE`, `TASK_TRANSITION`, `TASK_ASSIGN` et `AGENT_STATUS_UPDATE`, matrice RBAC explicite avec scenarios role-based etendus (allow orchestrator, deny agent/spectator sur mutations bornees, reconnect spectator), audit adapter renforce, write scope encore limite | NO-GO | [../../../grimoire-kit/apps/grimoire-game/tests/integration/adapter-grimoire.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/adapter-grimoire.test.ts), [../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts), [../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-token-registry.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-token-registry.test.ts), [../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-rbac.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-rbac.test.ts) |
| G-V5-05 Release engineering | CI Node/TS, coverage, packaging, changelog et notes de release | CI runtime + coverage + packaging npm verifies et artefacts release V5 poses | GO | [../../../.github/workflows/ci.yml](../../../.github/workflows/ci.yml), [../../../grimoire-kit/apps/grimoire-game/package.json](../../../grimoire-kit/apps/grimoire-game/package.json), [RELEASE-NOTES-V5.md](RELEASE-NOTES-V5.md) |

## Verifications executees

- typecheck: PASS
- build: PASS
- tests: PASS (91 fichiers, 419 tests)
- contrats runtime cibles: PASS (3 fichiers, 7 tests)
- runtime surfaces cibles: PASS (4 fichiers, 6 tests)
- securite auth ciblee: PASS (2 fichiers, 27 tests)
- observability ciblee: PASS (3 fichiers, 13 tests)
- coverage: PASS
- cockpit:verify: PASS
- npm pack dry-run: PASS
- npm pack artifact: PASS

Preuves:

- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/check.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/check.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/build.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/build.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/test.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/test.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/contracts/runtime-contracts.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/contracts/runtime-contracts.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/runtime-surfaces.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/runtime-surfaces.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/security/auth-rbac.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/security/auth-rbac.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/observability-tests.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/observability-tests.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/contracts/test-coverage.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/contracts/test-coverage.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/cockpit-verify.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/cockpit-verify.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/release/pack-verify.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/release/pack-verify.txt)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/release/npm-pack.json](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/release/npm-pack.json)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/summary/execution-summary.md](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/summary/execution-summary.md)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/summary/manifest.json](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/summary/manifest.json)

## Verdict courant

- Programme V5 resserre: GO
- Release V5 complete: NO-GO tant que G-V5-01 a G-V5-04 ne sont pas verts simultanement
