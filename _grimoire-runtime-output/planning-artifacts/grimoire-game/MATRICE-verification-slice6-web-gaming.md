# Matrice de Verification Detaillee — Slice 6 (GAME-TKT-029 -> GAME-TKT-036)

> Projet : **Grimoire Game**
> Perimetre : fermeture des ecarts CdC identifies en priorite haute
> Sources : [TICKETS](./TICKETS-web-gaming.md), [PLAN](./PLAN-implementation-web-gaming.md), [MATRICE](./MATRICE-tracabilite-web-gaming.md)

---

## 1. Objectif

Definir, pour chaque ticket GAME-TKT-029 a GAME-TKT-036, les verifications obligatoires, les gates bloquantes et les preuves minimales avant transition vers Done.

Reference de suite de tests executable:

- [SUITE-tests-slice6-web-gaming.md](./SUITE-tests-slice6-web-gaming.md)

---

## 2. Regles de gate Slice 6

- Aucun ticket Slice 6 ne passe Done sans evidence exploitable rattachee au ticket.
- Toute verification negative sur un gate bloquant maintient le ticket en Review.
- Toute evidence doit etre reproductible (commande, scenario, logs, captures ou extrait de donnees).
- Les preuves doivent etre traceables jusqu'a l'exigence ciblee du CdC.

---

## 3. Matrice Ticket -> Verification -> Evidence

| Ticket | Exigences ciblees | Verifications obligatoires | Gates bloquantes | Evidence minimale attendue |
| --- | --- | --- | --- | --- |
| GAME-TKT-029 | F11 | V-029-01 creation agent via UI; V-029-02 clonage sans heritage XP/historique; V-029-03 edition post-deploiement avec regle restart | G-029-A creation invalide rejectee; G-029-B mutation sensible sans restart bloquee | Rapport tests e2e create/clone/config; captures UI des flux; logs d'audit creation/mutation |
| GAME-TKT-030 | F12 | V-030-01 edition MCP/skills/prompts/tools/hooks; V-030-02 validation schema config; V-030-03 coherence apres restart; V-030-04 badges provenance/trust/policy visibles sur les activations | G-030-A config invalide rejectee; G-030-B divergence config runtime/stockage bloquante; G-030-C activation sans metadata minimale bloquee | Tests integration UI->config->reload; extraits config avant/apres; journal d'audit des changements; extrait matrice risque/policy du scope |
| GAME-TKT-031 | F16 | V-031-01 declenchement SFX sur evenements cibles; V-031-02 toggles audio independants; V-031-03 persistence des reglages audio | G-031-A doublons audio non autorises; G-031-B mode mute total incomplet | Tests integration audio; captures HUD audio; export config audio persistante |
| GAME-TKT-032 | F17 | V-032-01 attribution XP par action eligibile; V-032-02 calcul niveau deterministic; V-032-03 persistence achievements | G-032-A credit XP en double bloque; G-032-B incoherence niveau apres restart bloquante | Tests unitaires XP/level; tests integration persistence/restart; extraits DB avant/apres |
| GAME-TKT-033 | F18 | V-033-01 declenchement first-run uniquement; V-033-02 skip definitif; V-033-03 reprise etape apres interruption | G-033-A relance non voulue apres skip; G-033-B perte d'etat onboarding bloquante | Tests e2e first-run/skip/resume; captures tutoriel; extrait de persistence onboarding |
| GAME-TKT-034 | F24, F27 | V-034-01 enforcement des 4 phases debug; V-034-02 blocage FIX_PROPOSED sans root cause; V-034-03 blocage en presence de critical non resolu | G-034-A transition phase non autorisee; G-034-B critical ouvert interdit progression | Tests workflow debug/review; logs de blocage/deblocage; extrait alerte architecture review required |
| GAME-TKT-035 | F28, F29 | V-035-01 cycle fin de branche options 1/2/3/4; V-035-02 verification tests pre-cloture; V-035-03 audit securite et generation tickets derives; V-035-04 signalement des gaps provenance/policy sur surfaces d'execution | G-035-A option destructive sans confirmation typed discard; G-035-B finding securite critical bloque ship; G-035-C surface d'execution non qualifiee remonte comme finding bloquant du scope | Scenarios e2e branch finisher; rapport audit securite avec severites; traces tickets securite auto-generes; extrait matrice surfaces -> findings |
| GAME-TKT-036 | F01, F02, F03, F19, F21, F22 | V-036-01 couverture editeur map et contraintes; V-036-02 controle read-only spectateur en negatif; V-036-03 mapping desk->directory persistant; V-036-04 lifecycle worktree room complet | G-036-A mutation autorisee en mode spectateur; G-036-B mapping desk->directory ambigu; G-036-C trou de couverture sur un slot cible | Matrice de tests slot par slot; captures UI/room; journaux d'audit transitions/permissions |

---

## 4. Ordre de verification recommande

1. GAME-TKT-029
2. GAME-TKT-030
3. GAME-TKT-034
4. GAME-TKT-036
5. GAME-TKT-031
6. GAME-TKT-032
7. GAME-TKT-033
8. GAME-TKT-035

---

## 5. Checklist de completion Slice 6

- [x] Verification obligatoire executee pour chaque ticket (run `RUN-20260409-YOLO`).
- [x] Gate bloquant valide (aucun gate Slice 6 ouvert sur le run automatise).
- [x] Evidence minimale attachee et consultable (`_bmad-output/test-artifacts/grimoire-game/slice6/RUN-20260409-YOLO/summary/`).
- [x] Coherence maintenue avec la matrice de tracabilite.
- [x] Mise a jour du backlog non requise sur ce run (pas de split/merge de ticket detecte).

---

## 6. Statut d'execution courant (RUN-20260409-YOLO)

| Ticket | Statut | Evidence principale |
| --- | --- | --- |
| GAME-TKT-029 | Verifie (PASS) | `test_t029_agent_factory.py` + evidence pack run |
| GAME-TKT-030 | Verifie (PASS) | `test_t030_configuration.py` + evidence pack run |
| GAME-TKT-031 | Verifie (PASS) | `test_t031_audio.py` + evidence pack run |
| GAME-TKT-032 | Verifie (PASS) | `test_t032_progression.py` + evidence pack run |
| GAME-TKT-033 | Verifie (PASS) | `test_t033_onboarding.py` + evidence pack run |
| GAME-TKT-034 | Verifie (PASS) | `test_t034_investigation.py` + evidence pack run |
| GAME-TKT-035 | Verifie (PASS) | `test_t035_branch_finisher.py` + evidence pack run |
| GAME-TKT-036 | Verifie (PASS) | `test_t036_coverage_slots.py` + evidence pack run |

Conclusion de slice:

- Slice 6: GO CONDITIONNEL.
- Motif: verifications Slice 6 vertes sur ce run; decision GO release globale dependante des gates V5 hors perimetre.
