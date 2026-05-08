# Go/No-Go Delta

## Run

- Date: 2026-04-09T06:10:27Z
- Run: RUN-20260409-021023

## Delta execute

- Extension du write-path borne V5 avec `TASK_TRANSITION`:
  - nouveau contrat client `TASK_TRANSITION` (taskId, status, idempotencyKey);
  - RBAC explicitement orchestrator-only pour cette mutation;
  - application fail-closed dans `AdapterGrimoire` avec budget de transitions borne;
  - idempotence mutation par type d event (`CONFIG_UPDATE`, `TASK_TRANSITION`) pour eviter les collisions de cle;
  - support runtime source filesystem de la mutation + replay reconnect.
- Extension des tests:
  - contrats events (`TASK_TRANSITION` valide + malformed);
  - RBAC role matrix sur `TASK_TRANSITION`;
  - adapter mock, adapter grimoire, runtime-source-fs pour transition et dedupe.

## Validation

- check: PASS
- build: PASS
- test: PASS (17 suites, 64 tests)
- test:coverage: PASS
- pack:verify: PASS
- pack:artifact: PASS

## Decision

- G-V5-05: GO maintenu.
- G-V5-04: progression concretee (write-path etendu de config vers transitions de taches bornees), mais NO-GO maintenu tant que le budget write n inclut pas encore l ensemble des transitions operatoires cibles.
- G-V5-01 a G-V5-03: NO-GO maintenus.
