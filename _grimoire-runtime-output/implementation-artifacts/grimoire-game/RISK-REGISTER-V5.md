# Risk Register V5 - Agent OS + Game UI

## Objet

Registre des risques actifs pour la V5 resserree, avec strategie de mitigation et statut de suivi.

## Risques actifs

| ID | Risque | Impact | Probabilite | Statut | Mitigation | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| R-V5-01 | Drift entre causalite affichee et causalite canonique runtime | Eleve | Moyen | Ouvert | Prioriser les contrats canoniques et le panel explicable unique | [GO-NO-GO-V5.md](GO-NO-GO-V5.md) |
| R-V5-02 | Live control plane incomplet sur les mutations autorisees | Eleve | Moyen | Ouvert | Conserver un budget write etroit, etendre progressivement le write-path avec tests negatifs (`CONFIG_UPDATE`, `TASK_TRANSITION`, `TASK_ASSIGN`, `AGENT_STATUS_UPDATE`) | [../../../grimoire-kit/apps/grimoire-game/src/bridge/adapter-grimoire.ts](../../../grimoire-kit/apps/grimoire-game/src/bridge/adapter-grimoire.ts), [../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts) |
| R-V5-03 | Surface cockpit finale insuffisante pour remplacer le transcript brut | Eleve | Moyen | Mitige | Capacites cockpit operateur validees sur les surfaces runtime Game UI et Observability, avec generation cockpit et report a partir des memes read models | [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/runtime-surfaces.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/integration/runtime-surfaces.txt), [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/observability-tests.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/observability-tests.txt), [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/cockpit-verify.txt](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430/observability/cockpit-verify.txt), [../../../grimoire-kit/apps/grimoire-game/src/state/runtime-dashboard-view.ts](../../../grimoire-kit/apps/grimoire-game/src/state/runtime-dashboard-view.ts) |
| R-V5-04 | Regression sur idempotence/replay lors des extensions write | Moyen | Moyen | Ouvert | Etendre les tests integration sur reconnect, replay, dedupe des idempotency keys et isolation inter-type des cles partagees | [../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts), [../../../grimoire-kit/apps/grimoire-game/tests/integration/adapter-grimoire.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/adapter-grimoire.test.ts), [../../../grimoire-kit/apps/grimoire-game/tests/integration/idempotency-config.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/idempotency-config.test.ts) |
| R-V5-05 | Couverture insuffisante sur la couche auth/RBAC | Moyen | Moyen | Mitige | Couvrir explicitement les chemins role-based (allow orchestrator, deny agent/spectator sur mutations bornees, reconnect spectator), puis maintenir ces preuves en CI | [../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-token-registry.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-token-registry.test.ts), [../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-rbac.test.ts](../../../grimoire-kit/apps/grimoire-game/tests/integration/auth-rbac.test.ts) |
| R-V5-06 | Qualite release non reproductible sans evidence pack | Eleve | Faible | Mitige | Conserver un run d evidence structure par release candidate | [../../test-artifacts/grimoire-game/v5/RUN-20260414-000430](../../test-artifacts/grimoire-game/v5/RUN-20260414-000430) |

## Risques fermes

| ID | Risque | Statut | Raison de fermeture | Evidence |
| --- | --- | --- | --- | --- |
| R-V5-07 | Absence de verification packaging runtime | Ferme | `npm pack` verifie localement et en CI, artefact produit | [../../../grimoire-kit/apps/grimoire-game/package.json](../../../grimoire-kit/apps/grimoire-game/package.json), [../../../.github/workflows/ci.yml](../../../.github/workflows/ci.yml) |

## Regles de suivi

- Un risque reste ouvert tant qu'une preuve testable n'est pas rattachee a une mitigation.
- Aucun risque ne passe en ferme sur simple argument documentaire.
- Toute mitigation doit pointer vers un fichier, un test, un rapport ou un artefact d evidence.
