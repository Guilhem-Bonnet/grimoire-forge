# GO/NO-GO V5 - Agent OS + Game UI

## Perimetre

Ce document formalise la decision de go/no-go du livrable V5 pour Agent OS + Game UI.

Il est aligne sur les artefacts suivants:

- [livrable-v5-agent-os-game-ui.md](../../../docs/exploitation/livrable-v5-agent-os-game-ui.md)
- [benchmark-github-agent-os-game-ui.md](../../../docs/exploitation/benchmark-github-agent-os-game-ui.md)
- [plan-maitre-agent-os-game-ui.md](../../../docs/exploitation/plan-maitre-agent-os-game-ui.md)
- [matrice-capabilities-agent-os-game-ui.md](../../../docs/exploitation/matrice-capabilities-agent-os-game-ui.md)

## These de decision

La V5 n'est `GO` que si le produit livre un cockpit operatoire spatial plus utile que la lecture brute des traces pour diagnostiquer, verifier et challenger un run agentique.

## Decision actuelle

- [x] `GO` sur le programme V5 resserre.
- [ ] `GO` sur la release V5.
- [x] `NO-GO` sur une release immediate.

## Gates bloquants

| Gate | Condition de passage | Statut actuel | Verdict |
| --- | --- | --- | --- |
| G-V5-01 Runtime canonique | Contrats, correlations et causalite alignes sans drift doc/code | Socle partiel, encore en consolidation | NO-GO |
| G-V5-02 Backbone live | Replay, reconnect, event store et multi-session fiables | Replay et projections presents, control plane live incomplet | NO-GO |
| G-V5-03 Cockpit utile | Audit, verification, session diff et inspection utilisables par un operateur | Facade runtime unifiee exposee (`board`, `observability`, `session`, `tasks`, `verification`, `sessionDiff`) et validee par tests d'integration cockpit | GO |
| G-V5-04 Mutations fail-closed | Budget write borne, RBAC, audit et mode spectateur prouves | RBAC role-based et mode spectateur prouves avec scenarios etendus (allow orchestrator, deny agent/spectator sur mutations bornees, reconnect spectator), write-path borne etendu a `CONFIG_UPDATE` + `TASK_TRANSITION` + `TASK_ASSIGN` + `AGENT_STATUS_UPDATE`, audit adapter explicite et erreurs fail-closed, budget write encore incomplet | NO-GO |
| G-V5-05 Release engineering | CI Node/TS, coverage, packaging, changelog et notes de release | CI runtime, coverage, packaging npm et artefacts release V5 en place | GO |

## Artefacts de decision V5

- [MATRICE-validation-V5.md](MATRICE-validation-V5.md)
- [RISK-REGISTER-V5.md](RISK-REGISTER-V5.md)
- [RELEASE-NOTES-V5.md](RELEASE-NOTES-V5.md)
- [KNOWN-LIMITATIONS-V5.md](KNOWN-LIMITATIONS-V5.md)

## Delta valide

Execution locale validee sur `grimoire-kit/apps/grimoire-game`:

- `npm run check` : PASS
- `npm run build` : PASS
- `npm test` : PASS (`91` fichiers, `419` tests)
- `npm run test -- <lot contrats runtime>` : PASS (`3` fichiers, `7` tests)
- `npm run test -- <lot runtime surfaces>` : PASS (`4` fichiers, `6` tests)
- `npm run test -- <lot securite auth>` : PASS (`2` fichiers, `27` tests)
- `npm run test -- <lot observability>` : PASS (`3` fichiers, `13` tests)
- `npm run test:coverage` : PASS
- `npm run cockpit:verify` : PASS
- `npm run pack:verify` : PASS
- `npm run pack:artifact` : PASS
- couverture globale runtime: `88.87%` statements, `79.59%` branches, `95.52%` functions, `88.87%` lines.
- evidence pack de ce run: `_grimoire-runtime-output/test-artifacts/grimoire-game/v5/RUN-20260414-000430/`.

## Conditions minimales de GO

1. Le cockpit permet de traiter les scenarios canoniques V5 sans repasser en permanence par le transcript brut.
2. La causalite affichee reste fiable sous replay, reconnect et comparaison de sessions.
3. Les actions write autorisees sont peu nombreuses, auditees et refusent par defaut tout cas ambigu.
4. Le mode spectateur est reel, read-only et prouve par tests.
5. La CI TypeScript et la documentation de release rendent la livraison reproductible.

## Scenarios canoniques a prouver

| Scenario | Question | Preuve attendue |
| --- | --- | --- |
| Diagnostic de divergence | Pourquoi deux sessions ont-elles diverge ? | Session diff + evidence causale |
| Verification avant `DONE` | La tache est-elle prouvable ? | Gate de verification + audit |
| Explication d'une decision | Pourquoi cette transition a-t-elle eu lieu ? | Decision card + support tools |
| Isolement d'un agent fautif | Qui a produit le probleme et avec quoi ? | Inspection + audit + room + trace |
| Cloture d'un challenge | Le verdict est-il justifie et actionnable ? | Sortie challenge + actions correctives |

## Evidence pack attendu

```text
_grimoire-runtime-output/test-artifacts/grimoire-game/v5/
  RUN-YYYYMMDD-HHMMSS/
    summary/
    contracts/
    integration/
    e2e/
    perf/
    security/
    observability/
    release/
    decision/
```

## Risques de faux GO

- confondre des read models prometteurs avec une surface produit effectivement utile ;
- elevier des inferences heuristiques au rang de verite ;
- declarer une V5 sans CI TypeScript et sans packaging ;
- laisser entrer des features decoratives qui masquent l'absence de boucle operatoire ;
- melanger multi-runtime futur et scope Grimoire-first actuel.

## Ruling

Le ruling courant est simple:

- poursuivre la construction du cockpit operatoire resserre ;
- ne pas revendiquer de release V5 tant que les gates G-V5-01 a G-V5-04 ne sont pas toutes vertes ;
- privilegier les coupes de scope nettes a toute acceleration decorative.
