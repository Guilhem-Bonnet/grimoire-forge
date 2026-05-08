# Synthese d'execution - RUN-20260414-000430

## Perimetre

Ce run assemble le pack de preuves V5 courant pour `@grimoire-kit/grimoire-game`.

- Racine package: `grimoire-kit/apps/grimoire-game`
- Racine evidence pack: `RUN-20260414-000430`
- Verdict programme: `GO` sur la V5 resserree
- Verdict release: `NO-GO` sur la release V5 immediate

## Commandes executees

| Categorie | Commande | Resultat | Preuve |
| --- | --- | --- | --- |
| Integration | `npm run check` | PASS | `integration/check.txt` |
| Integration | `npm run build` | PASS | `integration/build.txt` |
| Integration | `npm test` | PASS (`91` fichiers, `419` tests) | `integration/test.txt` |
| Contrats | `npm run test -- tests/contracts/vscode-webview-bridge.contract.test.ts tests/contracts/runtime-web-scenarios.contract.test.ts tests/contracts/public-api-exports.contract.test.ts` | PASS (`3` fichiers, `7` tests) | `contracts/runtime-contracts.txt` |
| Integration | `npm run test -- tests/integration/runtime-game-ui-view.test.ts tests/integration/runtime-observability-surface-view.test.ts tests/integration/runtime-dashboard-ui-view.test.ts tests/integration/runtime-cockpit-view.test.ts` | PASS (`4` fichiers, `6` tests) | `integration/runtime-surfaces.txt` |
| Securite | `npm run test -- tests/integration/auth-rbac.test.ts tests/integration/auth-token-registry.test.ts` | PASS (`2` fichiers, `27` tests) | `security/auth-rbac.txt` |
| Observability | `npm run test -- tests/integration/observability-panel-view.test.ts tests/integration/observability-view.test.ts tests/integration/runtime-observability-surface-view.test.ts` | PASS (`3` fichiers, `13` tests) | `observability/observability-tests.txt` |
| Contrats | `npm run test:coverage` | PASS | `contracts/test-coverage.txt` |
| Observability | `npm run cockpit:verify` | PASS | `observability/cockpit-verify.txt` |
| Release | `npm run pack:verify` | PASS | `release/pack-verify.txt` |
| Release | `npm run pack:artifact` | PASS | `release/pack-artifact.txt`, `release/npm-pack.json` |

## Snapshot metriques

- Couverture: `88.87%` statements, `79.59%` branches, `95.52%` functions, `88.87%` lines
- Empreinte disque cockpit-app: `788K`
- Runtime views report: `931569` bytes HTML, `96108` bytes client JS
- Package npm: `394368` bytes packages, `2712292` bytes decompresse

## Artefacts captures

- Assets observability: `observability/runtime-views-report.html`, `observability/runtime-views-report-client.js`
- Build cockpit: `release/cockpit-app/index.html`
- Rapports de couverture: `contracts/coverage/coverage-summary.json`, `contracts/coverage/lcov.info`, `contracts/coverage/lcov-report/`
- Payload npm: `release/grimoire-kit-grimoire-game-0.0.0.tgz`, `release/npm-pack.json`

## Interpretation

Ce pack prouve que le package runtime courant se build, se teste, se package, et regenere les assets web du cockpit et du report.

Il ne change pas le ruling sur la release V5: le pack de preuves est complet pour ce candidat, tandis que la release globale reste bloquee par les gates `G-V5-01`, `G-V5-02` et `G-V5-04`.
