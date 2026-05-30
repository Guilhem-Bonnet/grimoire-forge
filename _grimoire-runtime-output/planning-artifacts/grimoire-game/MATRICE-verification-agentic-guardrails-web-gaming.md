# Matrice de Verification Detaillee - Guardrails agentiques (GAME-TKT-037 -> GAME-TKT-039)

> Projet : **Grimoire Game**
> Perimetre : gouvernance des surfaces d'execution, chaine de verification et enveloppe canonique pilote
> Sources : [TICKETS](./TICKETS-web-gaming.md), [PLAN](./PLAN-implementation-web-gaming.md), [MATRICE](./MATRICE-tracabilite-web-gaming.md), [CONTRAT](./CONTRAT-runtime-agentic-guardrails.md)

---

## 1. Objectif

Definir, pour `GAME-TKT-037`, `GAME-TKT-038` et `GAME-TKT-039`, les verifications obligatoires, les gates bloquantes et les preuves minimales avant transition vers `Done`.

Reference de suite de tests executable:

- [SUITE-tests-agentic-guardrails-web-gaming.md](./SUITE-tests-agentic-guardrails-web-gaming.md)

---

## 2. Regles de gate

- Aucun ticket de ce perimetre ne passe `Done` sans preuve exploitable et rattachee a une surface ou une transition concrete.
- Toute verification negative sur un gate bloquant maintient le ticket en `Review`.
- Les preuves doivent rester reproductibles depuis le package runtime TypeScript sans dependre d'une enquete terminale ad hoc.
- Les claims sur OWASP Agentic Skills, verification d'integrite ou enveloppe canonique restent bornes a ce qui est effectivement teste.

---

## 3. Matrice Ticket -> Verification -> Evidence

| Ticket | Verifications obligatoires | Gates bloquantes | Evidence minimale attendue |
| --- | --- | --- | --- |
| `GAME-TKT-037` | `V-037-01` inventaire des surfaces du scope prioritaire; `V-037-02` policy minimale et trust status visibles; `V-037-03` refus fail-closed des activations non qualifiees; `V-037-04` audit trail des decisions d'activation | `G-037-A` activation sans `origin`; `G-037-B` activation sans `requiredPolicy`; `G-037-C` activation avec `trustStatus=blocked`; `G-037-D` divergence entre UI de config et audit trail | Extrait de registre des surfaces; preuves UI de badges governance; logs de refus/autorisation; tests integration auth/policy |
| `GAME-TKT-038` | `V-038-01` metadata critiques presentes sur transitions; `V-038-02` `verification-view` reconstruit verdict et manques; `V-038-03` replay conserve `traceId`/`verificationRef`; `V-038-04` `audit-view` relie action, controles et evidence | `G-038-A` transition critique sans `traceId`; `G-038-B` `verificationRef` absent; `G-038-C` `evidenceRefs` vide; `G-038-D` perte de causalite au replay | Extraits d'events enrichis; rapports `verification-view`; preuves de replay stable; journal de blocage d'une transition incomplete |
| `GAME-TKT-039` | `V-039-01` projection canonique definie sur un panier borne; `V-039-02` compatibilite runtime/replay; `V-039-03` lecture read-only spectateur ou session stable; `V-039-04` consumers existants non regressifs | `G-039-A` enveloppe pilote divergente semantiquement du payload source; `G-039-B` regression sur consommateurs `v1`; `G-039-C` pilote etendu hors panier borne sans decision explicite | Spec de mapping avant/apres; tests d'interoperabilite; captures ou sorties de vues read-only; preuve de compatibilite montante |

---

## 4. Ordre de verification recommande

1. `GAME-TKT-037`
2. `GAME-TKT-038`
3. `GAME-TKT-039`

---

## 5. Checklist de completion

- [x] Registre des surfaces du scope prioritaire valide et rattache au runtime.
- [x] Activations non qualifiees bloquees en UI et en runtime.
- [x] Chaine `action -> controles -> verdict -> evidenceRef` lisible dans les vues runtime.
- [x] Replay stable des metadata de verification.
- [x] Pilote d'enveloppe canonique valide sur le panier borne sans regression.
- [x] Coherence maintenue avec [MATRICE-tracabilite-web-gaming.md](./MATRICE-tracabilite-web-gaming.md).

---

## 6. Statut d'execution courant

| Ticket | Statut | Commentaire |
| --- | --- | --- |
| `GAME-TKT-037` | Verifie (PASS) | Gouvernance des surfaces, refus fail-closed et projections de gouvernance couverts sur la tranche runtime locale |
| `GAME-TKT-038` | Verifie (PASS) | Transitions critiques enrichies, `VERIFICATION_GATE` autoritaire et preuves replayables valides localement |
| `GAME-TKT-039` | Verifie (PASS) | Pilote d'enveloppe canonique read-only couvre runtime, replay et vues de session ou spectateur sur le panier borne |

Conclusion du perimetre:

- Le paquet est `VERIFIE` sur sa tranche runtime locale. Tout prolongement futur doit etre redecoupe explicitement hors de ce coeur deja couvert.
