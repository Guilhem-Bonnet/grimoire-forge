# Suite de Tests Executable — Slice 6 (GAME-TKT-029 -> GAME-TKT-036)

> Projet : **Grimoire Game**
> Perimetre : validation executable de la fermeture des ecarts CdC
> Sources : [MATRICE-verification-slice6-web-gaming.md](./MATRICE-verification-slice6-web-gaming.md), [TICKETS-web-gaming.md](./TICKETS-web-gaming.md)

---

## 1. Objectif

Definir une suite de tests actionnable pour GAME-TKT-029 a GAME-TKT-036, avec couverture explicite des verifications V-xxx, des gates G-xxx et des preuves minimales attendues.

---

## 2. Conventions

### 2.1 Format des IDs de test

`S6-T0NN-TYPE-XX`

- `S6` : scope Slice 6
- `T0NN` : ticket cible (ex: `T029`)
- `TYPE` : `UT`, `IT`, `E2E`, `NEG`, `SEC`
- `XX` : index incrementiel

### 2.2 Regles de preuve

- Chaque test produit un resultat binaire `PASS` ou `FAIL`.
- Chaque test conserve un artefact de preuve lisible.
- Les preuves sont stockees sous `/_bmad-output/test-artifacts/grimoire-game/slice6/`.

### 2.3 Commandes de base

- Verification qualite transverse: `task bmad: lint`, puis `task bmad: quick-check`.
- Verification ciblee ticket: `task bmad: test-file` sur le fichier de tests du ticket.
- Verification finale: `task bmad: test-modified`, puis `task bmad: test-all` avant cloture.

---

## 3. Suite ticket par ticket

## 3.1 GAME-TKT-029 — Agent Factory complet

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| S6-T029-E2E-01 | E2E | V-029-01 | Creation agent valide depuis UI avec apparition dans room cible | `pytest tests/grimoire_game/slice6/test_t029_agent_factory.py -k S6_T029_E2E_01` | Rapport e2e + capture UI creation |
| S6-T029-E2E-02 | E2E | V-029-02 | Clonage agent sans heritage XP/historique runtime | `pytest tests/grimoire_game/slice6/test_t029_agent_factory.py -k S6_T029_E2E_02` | Rapport e2e + extrait etat clone |
| S6-T029-NEG-01 | NEG | G-029-A | Tentative creation invalide rejectee avec erreur actionnable | `pytest tests/grimoire_game/slice6/test_t029_agent_factory.py -k S6_T029_NEG_01` | Rapport negatif + extrait erreur |
| S6-T029-IT-01 | IT | G-029-B | Mutation sensible bloquee tant que restart non confirme | `pytest tests/grimoire_game/slice6/test_t029_agent_factory.py -k S6_T029_IT_01` | Logs gate + audit mutation |

## 3.2 GAME-TKT-030 — Configuration gamifiee complete

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| S6-T030-E2E-01 | E2E | V-030-01 | Edition MCP/skills/prompts/tools/hooks via UI | `pytest tests/grimoire_game/slice6/test_t030_configuration.py -k S6_T030_E2E_01` | Rapport e2e + captures UI config |
| S6-T030-NEG-01 | NEG | G-030-A | Configuration invalide rejectee par validation schema | `pytest tests/grimoire_game/slice6/test_t030_configuration.py -k S6_T030_NEG_01` | Rapport negatif + details schema |
| S6-T030-IT-01 | IT | V-030-03 | Coherence config avant/apres restart board | `pytest tests/grimoire_game/slice6/test_t030_configuration.py -k S6_T030_IT_01` | Diff config avant/apres |
| S6-T030-IT-02 | IT | G-030-B | Detection divergence runtime/stockage et blocage | `pytest tests/grimoire_game/slice6/test_t030_configuration.py -k S6_T030_IT_02` | Logs gate + journal audit |
| S6-T030-SEC-01 | SEC | V-030-04, G-030-C | Activation refusee si provenance, trust status ou policy minimale manquent | `pytest tests/grimoire_game/slice6/test_t030_configuration.py -k S6_T030_SEC_01` | Captures badges governance + logs refus activation |

## 3.3 GAME-TKT-031 — Systeme sonore in-world

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| S6-T031-IT-01 | IT | V-031-01 | Declenchement SFX sur evenements cibles sans doublon | `pytest tests/grimoire_game/slice6/test_t031_audio.py -k S6_T031_IT_01` | Rapport integration audio |
| S6-T031-E2E-01 | E2E | V-031-02 | Toggling SFX/musique/ambiance independants | `pytest tests/grimoire_game/slice6/test_t031_audio.py -k S6_T031_E2E_01` | Capture HUD audio + etat toggles |
| S6-T031-E2E-02 | E2E | G-031-B | Mode mute total supprime tout flux audio | `pytest tests/grimoire_game/slice6/test_t031_audio.py -k S6_T031_E2E_02` | Rapport mute + logs runtime |
| S6-T031-IT-02 | IT | V-031-03 | Persistence des reglages audio apres restart | `pytest tests/grimoire_game/slice6/test_t031_audio.py -k S6_T031_IT_02` | Export config audio persistante |

## 3.4 GAME-TKT-032 — Progression XP + achievements

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| S6-T032-UT-01 | UT | V-032-01 | Attribution XP par action eligibile | `pytest tests/grimoire_game/slice6/test_t032_progression.py -k S6_T032_UT_01` | Rapport unitaire attribution |
| S6-T032-UT-02 | UT | V-032-02 | Calcul niveau deterministic a entree identique | `pytest tests/grimoire_game/slice6/test_t032_progression.py -k S6_T032_UT_02` | Rapport unitaire formule level |
| S6-T032-NEG-01 | NEG | G-032-A | Protection contre credit XP en double | `pytest tests/grimoire_game/slice6/test_t032_progression.py -k S6_T032_NEG_01` | Rapport negatif anti-double-credit |
| S6-T032-IT-01 | IT | V-032-03, G-032-B | Persistence XP/achievements et stabilite apres restart | `pytest tests/grimoire_game/slice6/test_t032_progression.py -k S6_T032_IT_01` | Extraits DB avant/apres + logs restart |

## 3.5 GAME-TKT-033 — Tutoriel onboarding first-run

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| S6-T033-E2E-01 | E2E | V-033-01 | Lancement automatique uniquement au premier demarrage | `pytest tests/grimoire_game/slice6/test_t033_onboarding.py -k S6_T033_E2E_01` | Rapport e2e first-run |
| S6-T033-E2E-02 | E2E | V-033-02 | Skip definitif et absence de relance automatique | `pytest tests/grimoire_game/slice6/test_t033_onboarding.py -k S6_T033_E2E_02` | Rapport e2e skip |
| S6-T033-E2E-03 | E2E | V-033-03 | Reprise a la bonne etape apres interruption | `pytest tests/grimoire_game/slice6/test_t033_onboarding.py -k S6_T033_E2E_03` | Rapport e2e resume |
| S6-T033-NEG-01 | NEG | G-033-A, G-033-B | Detection relance non voulue ou perte d'etat onboarding | `pytest tests/grimoire_game/slice6/test_t033_onboarding.py -k S6_T033_NEG_01` | Rapport negatif + extrait persistence |

## 3.6 GAME-TKT-034 — Investigation Lab + cycle review

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| S6-T034-E2E-01 | E2E | V-034-01 | Enchainement strict root-cause -> pattern -> hypothesis -> implementation | `pytest tests/grimoire_game/slice6/test_t034_investigation.py -k S6_T034_E2E_01` | Rapport workflow phases |
| S6-T034-NEG-01 | NEG | G-034-A | Blocage FIX_PROPOSED sans ROOT_CAUSE_IDENTIFIED | `pytest tests/grimoire_game/slice6/test_t034_investigation.py -k S6_T034_NEG_01` | Logs gate phase non autorisee |
| S6-T034-E2E-02 | E2E | V-034-03, G-034-B | Blocage progression si critical review non resolu | `pytest tests/grimoire_game/slice6/test_t034_investigation.py -k S6_T034_E2E_02` | Rapport review + preuve blocage |
| S6-T034-IT-01 | IT | V-034-03 | Escalade architecture apres trois fix_failed | `pytest tests/grimoire_game/slice6/test_t034_investigation.py -k S6_T034_IT_01` | Extrait alerte architecture review required |

## 3.7 GAME-TKT-035 — Branch Finisher + Security Audit Room

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| S6-T035-E2E-01 | E2E | V-035-01 | Options merge/pr/keep/discard conformes a la matrice d'actions | `pytest tests/grimoire_game/slice6/test_t035_branch_finisher.py -k S6_T035_E2E_01` | Rapport e2e branch options |
| S6-T035-NEG-01 | NEG | G-035-A | Rejet option destructive sans confirmation typed discard | `pytest tests/grimoire_game/slice6/test_t035_branch_finisher.py -k S6_T035_NEG_01` | Rapport negatif typed discard |
| S6-T035-SEC-01 | SEC | G-035-B | Blocage ship en presence de finding securite critical | `pytest tests/grimoire_game/slice6/test_t035_branch_finisher.py -k S6_T035_SEC_01` | Rapport audit securite + statut blocage |
| S6-T035-IT-01 | IT | V-035-03 | Generation automatique de tickets securite derives | `pytest tests/grimoire_game/slice6/test_t035_branch_finisher.py -k S6_T035_IT_01` | Trace tickets securite auto-generes |
| S6-T035-SEC-02 | SEC | V-035-04, G-035-C | Surface d'execution sans provenance ou policy remonte comme finding bloquant | `pytest tests/grimoire_game/slice6/test_t035_branch_finisher.py -k S6_T035_SEC_02` | Extrait matrice surfaces -> findings + statut blocage |

## 3.8 GAME-TKT-036 — Couverture slots CdC manquants

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| S6-T036-E2E-01 | E2E | V-036-01 | Editeur map, contraintes de grille et actions undo/redo | `pytest tests/grimoire_game/slice6/test_t036_coverage_slots.py -k S6_T036_E2E_01` | Rapport e2e map editor |
| S6-T036-SEC-01 | SEC | V-036-02, G-036-A | Test negatif read-only spectateur avec refus mutation | `pytest tests/grimoire_game/slice6/test_t036_coverage_slots.py -k S6_T036_SEC_01` | Logs refus mutation |
| S6-T036-IT-01 | IT | V-036-03, G-036-B | Mapping desk->directory persistant et non ambigu | `pytest tests/grimoire_game/slice6/test_t036_coverage_slots.py -k S6_T036_IT_01` | Extrait mapping + rapport coherence |
| S6-T036-E2E-02 | E2E | V-036-04, G-036-C | Lifecycle worktree room complet (creation, transitions, cloture) | `pytest tests/grimoire_game/slice6/test_t036_coverage_slots.py -k S6_T036_E2E_02` | Rapport e2e worktree lifecycle |

---

## 4. Sequence d'execution recommandee

1. Preparer la base qualite (`task bmad: lint`, `task bmad: quick-check`).
2. Executer les suites ticket dans l'ordre: 029, 030, 034, 036, 031, 032, 033, 035.
3. Apres chaque ticket, enregistrer les preuves sous `/_bmad-output/test-artifacts/grimoire-game/slice6/GAME-TKT-0NN/`.
4. Executer `task bmad: test-modified` puis `task bmad: test-all` avant proposition de cloture Slice 6.

---

## 5. Gate final Slice 6

Conditions minimales pour declarer la Slice 6 verifiee:

- Tous les tests listes en section 3 executes.
- Aucun gate bloquant en statut ouvert.
- Toutes les preuves minimales presentes et consultables.
- Coherence maintenue avec [MATRICE-verification-slice6-web-gaming.md](./MATRICE-verification-slice6-web-gaming.md) et [MATRICE-tracabilite-web-gaming.md](./MATRICE-tracabilite-web-gaming.md).

---

## 6. Fichiers de tests Slice 6

Les fichiers de tests associes a cette suite sont:

- `grimoire-kit/tests/grimoire_game/slice6/test_t029_agent_factory.py`
- `grimoire-kit/tests/grimoire_game/slice6/test_t030_configuration.py`
- `grimoire-kit/tests/grimoire_game/slice6/test_t031_audio.py`
- `grimoire-kit/tests/grimoire_game/slice6/test_t032_progression.py`
- `grimoire-kit/tests/grimoire_game/slice6/test_t033_onboarding.py`
- `grimoire-kit/tests/grimoire_game/slice6/test_t034_investigation.py`
- `grimoire-kit/tests/grimoire_game/slice6/test_t035_branch_finisher.py`
- `grimoire-kit/tests/grimoire_game/slice6/test_t036_coverage_slots.py`

Les scenarios sont implementes et ont ete executes sur le run `RUN-20260409-YOLO`.

Resultat de reference du run:

- `pytest tests/grimoire_game/slice6 -q` -> `32 passed`
