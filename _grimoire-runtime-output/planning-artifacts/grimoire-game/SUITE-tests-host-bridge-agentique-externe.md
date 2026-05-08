# Suite de Tests Executable - Host Bridge agentique externe (GAME-TKT-047 -> GAME-TKT-051)

> Projet : **Grimoire Game**
> Perimetre : validation executable du Host Bridge, des policies externes, des reviews importees et de la surface multi-host
> Sources : [MATRICE-verification-host-bridge-agentique-externe.md](./MATRICE-verification-host-bridge-agentique-externe.md), [CONTRAT-host-bridge-agentique-externe.md](./CONTRAT-host-bridge-agentique-externe.md)

---

## 1. Objectif

Definir une suite de tests actionnable pour `GAME-TKT-047` a `GAME-TKT-051`, avec couverture explicite des verifications `V-047` a `V-051`, des gates `G-047` a `G-051` et des preuves minimales attendues.

---

## 2. Conventions

### 2.1 Format des IDs de test

`HB-T0NN-TYPE-XX`

- `HB` : scope Host Bridge
- `T0NN` : ticket cible (`T047` a `T051`)
- `TYPE` : `UT`, `IT`, `NEG`, `VIEW`, `SEC`
- `XX` : index incrementiel

### 2.2 Regles de preuve

- Chaque test produit un resultat binaire `PASS` ou `FAIL`.
- Chaque test conserve un artefact de preuve lisible.
- Les preuves sont stockees sous `/_grimoire-runtime-output/test-artifacts/grimoire-game/host-bridge/`.

### 2.3 Commandes de base

- Verification typecheck: `npm --prefix grimoire-kit/apps/grimoire-game run check`
- Verification unitaire ou integration: `npm --prefix grimoire-kit/apps/grimoire-game run test -- <fichier-ou-filtre>`
- Verification couverture: `npm --prefix grimoire-kit/apps/grimoire-game run test:coverage`

---

## 3. Suite ticket par ticket

## 3.1 GAME-TKT-047 - Modele canonique des hotes externes

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| `HB-T047-UT-01` | UT | `V-047-01`, `V-047-02` | Validation des schemas `HostBinding` et `CapabilityManifest` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/host-binding.contract.test.ts` | Rapport contrat + payloads valides |
| `HB-T047-NEG-01` | NEG | `G-047-A`, `G-047-B` | Refus d'un hote sans binding ou sans manifest | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-registry.test.ts` | Rapport negatif + raison explicite |
| `HB-T047-VIEW-01` | VIEW | `V-047-04`, `G-047-D` | Projection lisible du registre des hotes dans le runtime dashboard | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/runtime-dashboard-hosts.test.ts` | Snapshot de projection + coherence cockpit |

## 3.2 GAME-TKT-048 - Contrats runtime des hotes externes

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| `HB-T048-UT-01` | UT | `V-048-01`, `V-048-02`, `V-048-03` | Validation des schemas `InvocationEnvelope`, `ContextLedgerEntry` et `ReviewArtifact` | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/host-invocation.contract.test.ts` | Rapport contrat + payloads valides |
| `HB-T048-IT-01` | IT | `V-048-04`, `G-048-B` | Replay stable des events `HOST_*` avec correlation et idempotence | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-bridge-session.test.ts` | Rapport replay + extrait d'event |
| `HB-T048-NEG-01` | NEG | `G-048-A`, `G-048-C`, `G-048-D` | Blocage d'une mutation directe, d'un contexte sans TTL ou d'une review vide | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-invocation-policy.test.ts` | Rapport negatif + audit trail |

## 3.3 GAME-TKT-049 - Policy engine connecteurs externes

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| `HB-T049-SEC-01` | SEC | `V-049-01`, `V-049-02` | Verification des scopes, allowlists et permission prompts | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-policy-engine.test.ts` | Rapport policy + decisions journalisees |
| `HB-T049-NEG-01` | NEG | `G-049-A`, `G-049-D` | Blocage d'un connecteur non approuve ou d'un prompt obligatoire bypass | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-policy-engine.test.ts` | Rapport negatif + raison explicite |
| `HB-T049-VIEW-01` | VIEW | `V-049-03`, `V-049-04`, `G-049-B`, `G-049-C` | Un host stale ou incompatible degrade en lecture seule et reste visible | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-connection-health.test.ts` | Snapshot health + projection runtime |

## 3.4 GAME-TKT-050 - Reviews externes -> Evidence Pack cockpit

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| `HB-T050-UT-01` | UT | `V-050-01`, `V-050-02` | Validation du schema `ReviewArtifact` et preservation des severites | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/contracts/review-artifact.contract.test.ts` | Rapport contrat + mappings de severite |
| `HB-T050-IT-01` | IT | `V-050-03`, `V-050-04`, `G-050-A`, `G-050-B` | Import d'une review externe jusqu'a l'evidence pack et au cockpit | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-review-evidence.test.ts` | Projection audit/verification + evidence refs |
| `HB-T050-NEG-01` | NEG | `G-050-C`, `G-050-D` | Rejet d'une review sans lien vers trace, ticket ou evidence | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-review-evidence.test.ts` | Rapport negatif + audit log |

## 3.5 GAME-TKT-051 - Host Bridge generique + surface multi-host

| Test ID | Type | Couvre | Scenario | Commande cible | Preuve attendue |
| --- | --- | --- | --- | --- | --- |
| `HB-T051-IT-01` | IT | `V-051-01`, `V-051-02` | `runtime-dashboard-view` expose bindings, capabilities et health par host | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/runtime-dashboard-hosts.test.ts` | Snapshot dashboard multi-host |
| `HB-T051-IT-02` | IT | `V-051-03`, `G-051-A` | Web, VS Code et un hote externe lisent le meme run sans divergence de causalite | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-surface-parity.test.ts` | Projection comparee inter-surfaces |
| `HB-T051-NEG-01` | NEG | `V-051-04`, `G-051-B`, `G-051-C`, `G-051-D` | Une degradation de host reste visible, non destructive et corrigeable depuis le cockpit | `npm --prefix grimoire-kit/apps/grimoire-game run test -- tests/integration/host-surface-parity.test.ts` | Rapport negatif + journal de degradation |

---

## 4. Sequence d'execution recommandee

1. `npm --prefix grimoire-kit/apps/grimoire-game run check`
2. Ticket `GAME-TKT-047`: `HB-T047-UT-01`, `HB-T047-NEG-01`, `HB-T047-VIEW-01`
3. Ticket `GAME-TKT-048`: `HB-T048-UT-01`, `HB-T048-IT-01`, `HB-T048-NEG-01`
4. Ticket `GAME-TKT-049`: `HB-T049-SEC-01`, `HB-T049-NEG-01`, `HB-T049-VIEW-01`
5. Ticket `GAME-TKT-050`: `HB-T050-UT-01`, `HB-T050-IT-01`, `HB-T050-NEG-01`
6. Ticket `GAME-TKT-051`: `HB-T051-IT-01`, `HB-T051-IT-02`, `HB-T051-NEG-01`
7. `npm --prefix grimoire-kit/apps/grimoire-game run test:coverage`

---

## 5. Gate final du perimetre

Conditions minimales pour declarer le paquet verifie:

- Tous les tests listes en section 3 executes.
- Aucun gate bloquant `G-047` a `G-051` en statut ouvert.
- Toutes les preuves minimales presentes et consultables.
- Coherence maintenue avec [MATRICE-verification-host-bridge-agentique-externe.md](./MATRICE-verification-host-bridge-agentique-externe.md) et [MATRICE-tracabilite-web-gaming.md](./MATRICE-tracabilite-web-gaming.md).

---

## 6. Fichiers de tests cibles

Tests existants a etendre:

- `grimoire-kit/apps/grimoire-game/tests/integration/audit-view.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/session-view.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/runtime-dashboard-view.test.ts`

Tests a ajouter pour fermer le paquet:

- `grimoire-kit/apps/grimoire-game/tests/contracts/host-binding.contract.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/contracts/host-invocation.contract.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/contracts/review-artifact.contract.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/host-registry.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/host-bridge-session.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/host-invocation-policy.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/host-policy-engine.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/host-connection-health.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/host-review-evidence.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/runtime-dashboard-hosts.test.ts`
- `grimoire-kit/apps/grimoire-game/tests/integration/host-surface-parity.test.ts`
