# GO/NO-GO Slice 6 - Grimoire Game

## Perimetre et alignement

Ce document est un artefact de pilotage operationnel pour la decision Go/No-Go de la Slice 6.
Il est aligne sur les sources suivantes:

- [MATRICE-verification-slice6-web-gaming.md](../../planning-artifacts/grimoire-game/MATRICE-verification-slice6-web-gaming.md)
- [SUITE-tests-slice6-web-gaming.md](../../planning-artifacts/grimoire-game/SUITE-tests-slice6-web-gaming.md)
- [test_t029_agent_factory.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t029_agent_factory.py)
- [test_t030_configuration.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t030_configuration.py)
- [test_t031_audio.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t031_audio.py)
- [test_t032_progression.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t032_progression.py)
- [test_t033_onboarding.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t033_onboarding.py)
- [test_t034_investigation.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t034_investigation.py)
- [test_t035_branch_finisher.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t035_branch_finisher.py)
- [test_t036_coverage_slots.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t036_coverage_slots.py)

## 1. Ticket -> Gates bloquants -> Tests obligatoires -> Preuves attendues

| Ticket | Gates bloquants | Tests obligatoires | Preuves attendues |
| --- | --- | --- | --- |
| GAME-TKT-029 | G-029-A creation invalide rejetee; G-029-B mutation sensible sans restart bloquee | S6-T029-E2E-01, S6-T029-E2E-02, S6-T029-NEG-01, S6-T029-IT-01 dans [test_t029_agent_factory.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t029_agent_factory.py) | Rapport e2e creation/clone; captures UI des flux; logs d'audit creation/mutation |
| GAME-TKT-030 | G-030-A config invalide rejetee; G-030-B divergence runtime/stockage bloquante | S6-T030-E2E-01, S6-T030-NEG-01, S6-T030-IT-01, S6-T030-IT-02 dans [test_t030_configuration.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t030_configuration.py) | Rapport e2e UI->config->reload; extraits config avant/apres; journal d'audit des changements |
| GAME-TKT-031 | G-031-A doublons audio non autorises; G-031-B mode mute total incomplet | S6-T031-IT-01, S6-T031-E2E-01, S6-T031-E2E-02, S6-T031-IT-02 dans [test_t031_audio.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t031_audio.py) | Rapport integration audio; captures HUD audio; export config audio persistante |
| GAME-TKT-032 | G-032-A credit XP en double bloque; G-032-B incoherence niveau apres restart bloquante | S6-T032-UT-01, S6-T032-UT-02, S6-T032-NEG-01, S6-T032-IT-01 dans [test_t032_progression.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t032_progression.py) | Rapports unitaires XP/level; preuve anti-double-credit; extraits DB avant/apres restart |
| GAME-TKT-033 | G-033-A relance non voulue apres skip; G-033-B perte d'etat onboarding bloquante | S6-T033-E2E-01, S6-T033-E2E-02, S6-T033-E2E-03, S6-T033-NEG-01 dans [test_t033_onboarding.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t033_onboarding.py) | Rapports e2e first-run/skip/resume; captures tutoriel; extrait persistence onboarding |
| GAME-TKT-034 | G-034-A transition de phase non autorisee; G-034-B critical ouvert interdit progression | S6-T034-E2E-01, S6-T034-NEG-01, S6-T034-E2E-02, S6-T034-IT-01 dans [test_t034_investigation.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t034_investigation.py) | Rapports workflow debug/review; logs de blocage/deblocage; preuve escalade architecture |
| GAME-TKT-035 | G-035-A option destructive sans confirmation typed discard; G-035-B finding securite critical bloque ship | S6-T035-E2E-01, S6-T035-NEG-01, S6-T035-SEC-01, S6-T035-IT-01 dans [test_t035_branch_finisher.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t035_branch_finisher.py) | Scenarios e2e branch finisher; rapport audit securite avec severites; traces tickets securite auto-generes |
| GAME-TKT-036 | G-036-A mutation autorisee en mode spectateur; G-036-B mapping desk->directory ambigu; G-036-C trou de couverture sur slot cible | S6-T036-E2E-01, S6-T036-SEC-01, S6-T036-IT-01, S6-T036-E2E-02 dans [test_t036_coverage_slots.py](../../../grimoire-kit/tests/grimoire_game/slice6/test_t036_coverage_slots.py) | Matrice de tests slot par slot; captures UI/room; journaux d'audit transitions/permissions |

## 2. Checklist operationnelle Ready to Launch (PASS/FAIL)

| Controle | Condition PASS | Condition FAIL | Statut | Reference evidence |
| --- | --- | --- | --- | --- |
| Couverture des tests obligatoires | Tous les tests S6-T029 a S6-T036 sont executes et marques PASS | Au moins un test obligatoire non execute ou FAIL | PASS | `pytest tests/grimoire_game/slice6 -q` -> `32 passed` (voir [execution-summary.md](../../../_bmad-output/test-artifacts/grimoire-game/slice6/RUN-20260409-YOLO/summary/execution-summary.md)) |
| Gates bloquants Slice 6 | Aucun gate G-029 a G-036 n'est ouvert | Un gate bloquant reste ouvert | PASS | Tests NEG/SEC executes et run global PASS (voir [gate-status.md](../../../_bmad-output/test-artifacts/grimoire-game/slice6/RUN-20260409-YOLO/summary/gate-status.md)) |
| Qualite de base | `task bmad: lint` et `task bmad: quick-check` passent | Echec lint ou quick-check | PASS | `ruff check` OK + `quick-check.sh` OK (voir [execution-summary.md](../../../_bmad-output/test-artifacts/grimoire-game/slice6/RUN-20260409-YOLO/summary/execution-summary.md)) |
| Verification globale | `task bmad: test-modified` et `task bmad: test-all` passent | Echec test-modified ou test-all | PASS | `test-modified` OK + `test-all` OK (`[100%]`) (voir [execution-summary.md](../../../_bmad-output/test-artifacts/grimoire-game/slice6/RUN-20260409-YOLO/summary/execution-summary.md)) |
| Tracabilite Ticket -> V/G -> preuve | Chaque ticket a au moins une preuve exploitable reliee aux V-xxx et G-xxx | Tracabilite incomplete ou preuve manquante | PASS | Mapping ticket->tests dans [test-index.md](../../../_bmad-output/test-artifacts/grimoire-game/slice6/RUN-20260409-YOLO/summary/test-index.md) + [MATRICE-verification-slice6-web-gaming.md](../../planning-artifacts/grimoire-game/MATRICE-verification-slice6-web-gaming.md) |
| Validation anti-scaffold | Aucun test de validation finale ne reste en `skipTest` | Presence de `skipTest` sur un test declare obligatoire | PASS | Recherche `skipTest`/`pytest.skip`/`pytest.mark.skip` sans match sur la suite Slice 6 (voir [execution-summary.md](../../../_bmad-output/test-artifacts/grimoire-game/slice6/RUN-20260409-YOLO/summary/execution-summary.md)) |
| Evidence Pack complet | Structure de dossiers conforme et preuves consultables | Dossiers incomplets ou preuves illisibles/non reproduisibles | PASS | Evidence pack consolide dans [RUN-20260409-YOLO](../../../_bmad-output/test-artifacts/grimoire-game/slice6/RUN-20260409-YOLO/summary/execution-summary.md) |

Decision Ready to Launch:

- [ ] PASS
- [ ] FAIL
- [x] GO CONDITIONNEL

## 3. Evidence Pack

Structure recommandee sous `_bmad-output/test-artifacts/grimoire-game/slice6/`:

```text
_bmad-output/test-artifacts/grimoire-game/slice6/
  RUN-YYYYMMDD-HHMMSS/
    summary/
      execution-summary.md
      gate-status.md
      test-index.md
    transversal/
      lint/
      quick-check/
      test-modified/
      test-all/
    GAME-TKT-029/
      reports/
      logs/
      captures/
      state/
    GAME-TKT-030/
      reports/
      logs/
      captures/
      state/
    GAME-TKT-031/
      reports/
      logs/
      captures/
      state/
    GAME-TKT-032/
      reports/
      logs/
      captures/
      state/
    GAME-TKT-033/
      reports/
      logs/
      captures/
      state/
    GAME-TKT-034/
      reports/
      logs/
      captures/
      state/
    GAME-TKT-035/
      reports/
      logs/
      captures/
      state/
    GAME-TKT-036/
      reports/
      logs/
      captures/
      state/
    decision/
      go-no-go-input.md
      exceptions.md
```

Convention minimale conseillee pour les fichiers de preuve:

| Type de preuve | Nommage recommande |
| --- | --- |
| Rapport test | `<test-id>__PASS.md` ou `<test-id>__FAIL.md` |
| Log brut | `<test-id>__runtime.log` |
| Capture | `<test-id>__screen-01.png` |
| Extrait etat/config/DB | `<test-id>__state.json` |
| Evidence transversale | `<commande>__PASS.txt` |

## 4. Decision Log (template)

### 4.1 Entree standard

| Date | Decision | Scope | Gates ouverts | Tests obligatoires executes | Evidence Pack | Decision owner | Validation pair | Actions imposees |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-04-09 | GO CONDITIONNEL | GAME-TKT-029..036 | Aucun gate Slice 6 ouvert sur run automatise | Oui (`32 passed` Slice 6 + gates transverses verts) | RUN-20260409-YOLO | Copilot | Guilhem | Lever gates V5 globaux avant GO release complet |
| YYYY-MM-DD | GO / NO-GO / GO CONDITIONNEL | GAME-TKT-029..036 | A renseigner | A renseigner | A renseigner | A renseigner | A renseigner | A renseigner |
| YYYY-MM-DD | GO / NO-GO / GO CONDITIONNEL | GAME-TKT-029..036 | A renseigner | A renseigner | A renseigner | A renseigner | A renseigner | A renseigner |
| YYYY-MM-DD | GO / NO-GO / GO CONDITIONNEL | GAME-TKT-029..036 | A renseigner | A renseigner | A renseigner | A renseigner | A renseigner | A renseigner |

### 4.2 Justification de decision

- Constat principal: Toutes les verifications Slice 6 executees dans ce run sont vertes.
- Gates critiques concernes: G-029 a G-036 couverts par les tests obligatoires (NEG/SEC inclus).
- Preuves determinantes: `32 passed` sur Slice 6, quick-check et test-all a `100%`, evidence pack RUN-20260409-YOLO.
- Risques residuels acceptes: Warnings environnement preflight (toolchain/devcontainer) sans blocker runtime fonctionnel sur ce run.
- Conditions de levee (si GO CONDITIONNEL): Validation GO release global apres fermeture des gates V5 hors scope Slice 6.
- Prochaine reevaluation: A la prochaine revue GO/NO-GO globale V5.
