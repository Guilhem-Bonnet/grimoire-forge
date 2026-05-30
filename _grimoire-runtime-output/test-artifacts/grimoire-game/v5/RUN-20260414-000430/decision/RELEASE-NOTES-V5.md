# Release Notes V5 - Agent OS + Game UI

## Portee de cette note

Cette note couvre le delta release engineering et hardening runtime applique dans la tranche courante de la V5.

## Changements principaux

### Runtime auth et control plane

- `AdapterGrimoire` supporte maintenant un write-path borne pour `CONFIG_UPDATE`.
- `AdapterGrimoire` etend le write-path borne a `TASK_TRANSITION` (transition de statut de tache).
- `AdapterGrimoire` etend le write-path borne a `TASK_ASSIGN` (assignation d une tache a un agent connu).
- `AdapterGrimoire` etend le write-path borne a `AGENT_STATUS_UPDATE` (pause/reprise d'un agent connu dans un graphe borne).
- Les mutations de configuration sont fail-closed hors budget write autorise.
- Les transitions de taches sont fail-closed hors graphe de transitions autorise.
- Les mutations sont idempotentes via `idempotencyKey` cote adapter.
- Les mutations `CONFIG_UPDATE`, `TASK_TRANSITION`, `TASK_ASSIGN` et `AGENT_STATUS_UPDATE` dedupent avec une cle idempotence isolee par type d event.
- Les erreurs runtime emettent des `sequenceId` strictement monotones, y compris sur refus successifs.
- Les refus auth et write sont traces dans un audit log adapter explicite.
- Les echec write runtime remontent en `RUNTIME_WRITE_FAILED` fail-closed.

Fichiers:

- [../../../grimoire-kit/apps/grimoire-game/src/bridge/adapter-grimoire.ts](../../../grimoire-kit/apps/grimoire-game/src/bridge/adapter-grimoire.ts)
- [../../../grimoire-kit/apps/grimoire-game/src/bridge/runtime-source-fs.ts](../../../grimoire-kit/apps/grimoire-game/src/bridge/runtime-source-fs.ts)

### Couverture de tests

- Ajout de tests integration sur:
  - write-path borne et dedupe idempotence de `AdapterGrimoire`;
  - write-path borne et dedupe idempotence de `TASK_TRANSITION`;
  - write-path borne et dedupe idempotence de `TASK_ASSIGN`;
  - write-path borne et dedupe idempotence de `AGENT_STATUS_UPDATE`;
  - isolation explicite inter-type de la cle idempotence partagee (`CONFIG_UPDATE` + `TASK_TRANSITION` sans dedupe croise) dans les deux ordres sur `MockAgentAdapter` et `AdapterGrimoire`;
  - replay reconnect filesystem valide pour des mutations inter-types partageant la meme cle d idempotence (`CONFIG_UPDATE` puis `TASK_TRANSITION`, puis ordre inverse `TASK_TRANSITION` puis `CONFIG_UPDATE`);
  - isolation explicite inter-type de la cle idempotence partagee entre `CONFIG_UPDATE` et `TASK_ASSIGN` dans les deux ordres (Mock, Adapter et replay filesystem);
  - isolation explicite inter-type de la cle idempotence partagee entre `CONFIG_UPDATE` et `AGENT_STATUS_UPDATE` dans les deux ordres (Mock, Adapter et replay filesystem);
  - isolation explicite inter-type de la cle idempotence partagee entre `TASK_TRANSITION` et `AGENT_STATUS_UPDATE` dans les deux ordres (Mock, Adapter et replay filesystem);
  - isolation explicite inter-type de la cle idempotence partagee entre `TASK_TRANSITION` et `TASK_ASSIGN` dans les deux ordres (Mock, Adapter et replay filesystem);
  - replay reconnect filesystem valide pour des mutations inter-types partageant la meme cle d idempotence (`TASK_ASSIGN` puis `AGENT_STATUS_UPDATE`);
  - isolation inter-type validee aussi sur `MockAgentAdapter` pour une cle partagee entre `TASK_ASSIGN` et `AGENT_STATUS_UPDATE`.
  - ordre inverse valide sans dedupe croise (`AGENT_STATUS_UPDATE` puis `TASK_ASSIGN`) sur `MockAgentAdapter`, `AdapterGrimoire` et replay filesystem.
  - refus explicite des cles hors budget write;
  - refus explicite des transitions hors graphe autorise et des entites inconnues (taches ou agents);
  - refus spectateur + audit role-based;
  - sequence monotone sur erreurs `NOT_IMPLEMENTED` consecutives;
  - fail-closed `RUNTIME_WRITE_FAILED` si le runtime source echoue;
  - matrice RBAC explicite (`RECONNECT_HANDSHAKE`, `CONFIG_UPDATE`, `TASK_TRANSITION`, `TASK_ASSIGN`, `AGENT_STATUS_UPDATE`);
  - scenarios role-based auth etendus: allow orchestrator sur mutations bornees, deny agent/spectator sur mutations bornees, reconnect spectator read-only.
  - expiration/revocation de tokens auth;
  - replay apres mutation config, transition task, assignation task et changement de statut agent sur runtime source filesystem.

Fichiers:

- [../../../grimoire-kit/apps/grimoire-game/tests/integration/adapter-grimoire.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/adapter-grimoire.test.ts)
- [../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts)
- [../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-rbac.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-rbac.test.ts)
- [../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-token-registry.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-token-registry.test.ts)

### Packaging runtime et CI

- Contrat de packaging npm explicite:
  - `main`, `types`, `exports`, `files`;
  - scripts `pack:verify`, `pack:artifact`, `release:verify`.
- Pipeline CI Node runtime etendu:
  - verification payload `npm pack --dry-run`;
  - creation d un artefact npm pack versionne;
  - upload des artefacts release.

Fichiers:

- [../../../grimoire-kit/apps/grimoire-game/package.json](../../../grimoire-kit/apps/grimoire-game/package.json)
- [../../../.github/workflows/ci.yml](../../../.github/workflows/ci.yml)

## Validation runtime

Resultats du run de reference:

- check: PASS
- build: PASS
- test: PASS (91 fichiers, 419 tests)
- contrats runtime cibles: PASS (3 fichiers, 7 tests)
- runtime surfaces cibles: PASS (4 fichiers, 6 tests)
- securite auth ciblee: PASS (2 fichiers, 27 tests)
- observability ciblee: PASS (3 fichiers, 13 tests)
- test:coverage: PASS
- cockpit:verify: PASS
- pack:verify: PASS
- pack:artifact: PASS
- couverture globale runtime: `88.87%` statements, `79.59%` branches, `95.52%` functions, `88.87%` lines

Evidence:

- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/summary/execution-summary.md](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/summary/execution-summary.md)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/summary/manifest.json](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/summary/manifest.json)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/release/grimoire-kit-grimoire-game-0.0.0.tgz](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/release/grimoire-kit-grimoire-game-0.0.0.tgz)
- [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/runtime-views-report.html](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/runtime-views-report.html)

## Impact sur les gates V5

- G-V5-05 Release engineering: passe a `GO`.
- G-V5-03 Cockpit utile: passe a `GO`.
- G-V5-01, G-V5-02 et G-V5-04: restent `NO-GO` a ce stade.

## Notes de compatibilite

- Le budget write est volontairement restreint en V5 pour limiter le risque.
- Le write-path global reste en phase de consolidation progressive.
