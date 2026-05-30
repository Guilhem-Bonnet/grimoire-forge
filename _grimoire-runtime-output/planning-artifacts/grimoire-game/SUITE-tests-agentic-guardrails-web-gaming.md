# Suite de Tests Executable - Guardrails agentiques (GAME-TKT-037 -> GAME-TKT-039)

> Projet : **Grimoire Game**
> Perimetre : validation executable des garde-fous sur surfaces d'execution, verification chain et enveloppe canonique pilote
> Sources : [MATRICE-verification-agentic-guardrails-web-gaming.md](./MATRICE-verification-agentic-guardrails-web-gaming.md), [CONTRAT-runtime-agentic-guardrails.md](./CONTRAT-runtime-agentic-guardrails.md)

---

## 1. Objectif

Definir une suite de tests actionnable pour `GAME-TKT-037`, `GAME-TKT-038` et `GAME-TKT-039`, avec couverture explicite des verifications `V-037` a `V-039`, des gates `G-037` a `G-039` et des preuves minimales attendues.

---

## 2. Conventions

### 2.1 Format des IDs de test

`AG-T0NN-TYPE-XX`

- `AG` : scope agentic guardrails
- `T0NN` : ticket cible (`T037`, `T038`, `T039`)
- `TYPE` : `UT`, `IT`, `NEG`, `SEC`, `VIEW`
- `XX` : index incrementiel

### 2.2 Regles de preuve

- Chaque test produit un resultat binaire `PASS` ou `FAIL`.
- Chaque test conserve un artefact de preuve lisible.
- Les preuves sont stockees sous `/_grimoire-runtime-output/test-artifacts/grimoire-game/agentic-guardrails/`.

### 2.3 Commandes de base

- Verification typecheck: `npm --prefix grimoire-kit/apps/grimoire-game run check`
- Verification unitaire ou integration: `npm --prefix grimoire-kit/apps/grimoire-game run test -- <fichier-ou-filtre>`
- Verification couverture: `npm --prefix grimoire-kit/apps/grimoire-game run test:coverage`

---

## 3. Suite ticket par ticket

## 3.1 GAME-TKT-037 - Garde-fous OWASP Agentic Skills

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| `AG-T037-UT-01` | UT | `V-037-01` | Validation du schema `SurfaceExecutionRecord` sur le scope prioritaire | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/surface-governance.contract.test.ts` | Rapport contrat + extrait de surfaces valides |
| `AG-T037-IT-01` | IT | `V-037-03`, `G-037-A`, `G-037-B` | Refus d'activation si `origin` ou `requiredPolicy` manque | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/auth-rbac.test.ts` | Rapport integration + raison de refus explicite |
| `AG-T037-NEG-01` | NEG | `G-037-C` | Blocage d'une surface `trustStatus=blocked` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/surface-governance.test.ts` | Rapport negatif + audit log de blocage |
| `AG-T037-VIEW-01` | VIEW | `V-037-02`, `V-037-04`, `G-037-D` | Alignement entre badges UI, registre et audit trail | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/audit-view.test.ts` | Capture ou sortie de projection + logs d'activation |

## 3.2 GAME-TKT-038 - Chaine de verification orientee AIVS

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| `AG-T038-UT-01` | UT | `V-038-01` | Validation du schema `VerificationGateEvent` et de la metadata critique | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/verification-gate.contract.test.ts` | Rapport contrat + payload valide |
| `AG-T038-VIEW-01` | VIEW | `V-038-02`, `G-038-B`, `G-038-C` | `verification-view` bloque une transition si la chaine est incomplete | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/verification-view.test.ts` | Rapport view + codes de blocage |
| `AG-T038-IT-01` | IT | `V-038-03`, `G-038-D` | Replay filesystem conserve `traceId`, `actionId` et `verificationRef` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/runtime-source-fs.test.ts` | Rapport integration replay + extrait d'event |
| `AG-T038-VIEW-02` | VIEW | `V-038-04`, `G-038-A` | `audit-view` relie refus, controles et evidence refs | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/audit-view.test.ts` | Projection audit + liens de causalite |

## 3.3 GAME-TKT-039 - Pilote UMF borne

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| `AG-T039-UT-01` | UT | `V-039-01` | Validation du schema `CanonicalEnvelopePilot` sur le panier borne | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/canonical-envelope-pilot.contract.test.ts` | Rapport contrat + mapping avant/apres |
| `AG-T039-IT-01` | IT | `V-039-02`, `G-039-A` | Mapping runtime -> replay sans perte semantique sur `TASK_UPDATE` et `WORKFLOW_STEP` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/session-view.test.ts` | Rapport integration + projection comparee |
| `AG-T039-IT-02` | IT | `V-039-03`, `G-039-B` | Projection read-only stable pour spectateur ou session-view | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/runtime-dashboard-view.test.ts` | Sortie read-only + preuve compatibilite |
| `AG-T039-NEG-01` | NEG | `V-039-04`, `G-039-C` | Le pilote n'elargit pas le panier de types sans decision explicite ni regression | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/canonical-envelope-pilot.test.ts` | Rapport negatif + journal de garde-fou |

---

## 4. Sequence d'execution recommandee

1. `npm --prefix grimoire-kit/apps/grimoire-game run check`
2. Ticket `GAME-TKT-037`: `AG-T037-UT-01`, `AG-T037-IT-01`, `AG-T037-NEG-01`, `AG-T037-VIEW-01`
3. Ticket `GAME-TKT-038`: `AG-T038-UT-01`, `AG-T038-VIEW-01`, `AG-T038-IT-01`, `AG-T038-VIEW-02`
4. Ticket `GAME-TKT-039`: `AG-T039-UT-01`, `AG-T039-IT-01`, `AG-T039-IT-02`, `AG-T039-NEG-01`
5. `npm --prefix grimoire-kit/apps/grimoire-game run test:coverage`

---

## 5. Gate final du perimetre

Conditions minimales pour declarer le paquet verifie:

- Tous les tests listes en section 3 executes.
- Aucun gate bloquant `G-037`, `G-038` ou `G-039` en statut ouvert.
- Toutes les preuves minimales presentes et consultables.
- Coherence maintenue avec [MATRICE-verification-agentic-guardrails-web-gaming.md](./MATRICE-verification-agentic-guardrails-web-gaming.md) et [MATRICE-tracabilite-web-gaming.md](./MATRICE-tracabilite-web-gaming.md).

---

## 6. Fichiers de tests cibles

Tests existants a etendre:

- `grimoire-kit/apps/grimoire-game/tests/integration/auth-rbac.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/verification-view.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/audit-view.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/runtime-source-fs.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/session-view.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/runtime-dashboard-view.test.ts`

Tests a ajouter pour fermer le paquet:

- `grimoire-kit/apps/grimoire-game/tests/contracts/surface-governance.contract.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/contracts/verification-gate.contract.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/contracts/canonical-envelope-pilot.contract.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/surface-governance.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/canonical-envelope-pilot.test.ts`
