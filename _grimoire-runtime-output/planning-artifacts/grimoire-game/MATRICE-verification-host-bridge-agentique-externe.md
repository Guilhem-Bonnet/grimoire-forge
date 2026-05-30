# Matrice de Verification Detaillee - Host Bridge agentique externe (GAME-TKT-047 -> GAME-TKT-051)

> Projet : **Grimoire Game**
> Perimetre : hotes externes, policy connecteurs, reviews importees et surface multi-host
> Sources : [TICKETS](./TICKETS-web-gaming.md), [PLAN](./PLAN-implementation-web-gaming.md), [MATRICE](./MATRICE-tracabilite-web-gaming.md), [CONTRAT](./CONTRAT-host-bridge-agentique-externe.md)

---

## 1. Objectif

Definir, pour `GAME-TKT-047` a `GAME-TKT-051`, les verifications obligatoires, les gates bloquantes et les preuves minimales avant transition vers `Done`.

Reference de suite de tests executable:

- [SUITE-tests-host-bridge-agentique-externe.md](./SUITE-tests-host-bridge-agentique-externe.md)

---

## 2. Regles de gate

- Aucun ticket de ce perimetre ne passe `Done` sans preuve exploitable et rattachee a un host, une decision de policy, une review ou une projection concrete.
- Toute verification negative sur un gate bloquant maintient le ticket en `Review`.
- Les preuves doivent rester reproductibles depuis le package runtime TypeScript sans dependre d'une inspection manuelle de l'UI d'un vendeur.
- Les claims sur Copilot, Claude ou MCP restent bornes a ce qui est effectivement teste et mappe vers des primitives canoniques.

---

## 3. Matrice Ticket -> Verification -> Evidence

| Ticket | Verifications obligatoires | Gates bloquantes | Evidence minimale attendue |
| --- | --- | --- | --- |
| `GAME-TKT-047` | `V-047-01` registre des hotes stable; `V-047-02` capability manifest complet; `V-047-03` mapping vendeur -> primitive canonique explicite; `V-047-04` projection lisible du registre des hotes | `G-047-A` hote sans `Host Binding`; `G-047-B` manifest absent; `G-047-C` champ vendeur dans le contrat coeur; `G-047-D` divergence entre registre et projection runtime | Schema et exemples de `Host Binding`; manifestes de capabilities; snapshot du registre des hotes; preuve de projection cockpit |
| `GAME-TKT-048` | `V-048-01` `Invocation Envelope` valide; `V-048-02` `Context Ledger` garde provenance, trust et TTL; `V-048-03` `Review Artifact` relie host, findings et evidence; `V-048-04` replay stable des events `HOST_*` | `G-048-A` mutation sans `preview` ou `validate`; `G-048-B` `idempotencyKey` absent; `G-048-C` import de contexte sans TTL ou trust status; `G-048-D` review importee sans `subjectRef` ni findings | Rapports de contrats; payloads valides/invalides; projections `audit-view` et `session-view`; preuve de replay stable |
| `GAME-TKT-049` | `V-049-01` scopes et allowlists appliques; `V-049-02` permission prompts emis selon policy; `V-049-03` etats `ALLOW` / `PROMPT` / `DENY` / `DEGRADE` audites; `V-049-04` host stale ou incompatible degrade proprement | `G-049-A` connecteur externe non approuve autorise; `G-049-B` host degrade qui reste writable; `G-049-C` decision de policy sans raison explicite; `G-049-D` bypass d'un prompt obligatoire | Matrice scopes -> decisions; journaux de policy; tests negatifs de blocage et degradation; snapshots health |
| `GAME-TKT-050` | `V-050-01` import des reviews externes en `Review Artifact`; `V-050-02` severites et statuts preserves; `V-050-03` evidence refs relies aux tickets et traces; `V-050-04` lecture cockpit sans UI vendeur | `G-050-A` review importee sans lien vers trace ou ticket; `G-050-B` severite perdue au mapping; `G-050-C` commentaires externes illisibles hors source; `G-050-D` absence d'evidence pack reliee | Exemples de review importee; projection audit/verification; evidence pack enrichi; journal de mapping |
| `GAME-TKT-051` | `V-051-01` surface multi-host lisible; `V-051-02` health et capabilities affiches par host; `V-051-03` semantique de run commune entre web, VS Code et hotes externes; `V-051-04` degradation propre visible et non destructive | `G-051-A` divergence de causalite entre surfaces; `G-051-B` host stale non visible; `G-051-C` actions multi-host non corrigeables depuis le cockpit; `G-051-D` surface multi-host dependante d'un vendeur unique | Snapshots `runtime-dashboard-view`; etats de health; captures ou sorties de projections comparees; preuve de degradation sans corruption |

---

## 4. Ordre de verification recommande

1. `GAME-TKT-047`
2. `GAME-TKT-048`
3. `GAME-TKT-049`
4. `GAME-TKT-050`
5. `GAME-TKT-051`

---

## 5. Checklist de completion

- [ ] Registre des hotes du scope prioritaire valide et rattache au runtime.
- [ ] Activations et imports externes bloques sans contrat ni policy.
- [ ] Les reviews externes deviennent des evidence refs consultables.
- [ ] Le replay conserve la causalite host -> invocation -> decision -> preuve.
- [ ] La surface multi-host reste coherente avec le cockpit et l'observateur.
- [ ] Coherence maintenue avec [MATRICE-tracabilite-web-gaming.md](./MATRICE-tracabilite-web-gaming.md).

---

## 6. Statut d'execution courant

| Ticket | Statut | Commentaire |
| --- | --- | --- |
| `GAME-TKT-047` | Planifie | Ticket preparatoire a ouvrir au rythme du front canonique, sans lancer encore de multi-host complet |
| `GAME-TKT-048` | Planifie | Contrats `HOST_*` et projections additives encore a cadrer apres avancee du socle canonique |
| `GAME-TKT-049` | Planifie | Policy engine externe et permission prompts gardes comme suite logique de `047` et `048` |
| `GAME-TKT-050` | Gele | Front review -> evidence reporte; `GAME-TKT-038` y est une dependance deja satisfaite localement, pas un prerequis runtime manquant |
| `GAME-TKT-051` | Gele | Surface multi-host reportee tant que le front prioritaire post-challenge n'est pas clos |

Conclusion du perimetre:

- Le paquet est specifie et sequence, mais pas globalement ouvrable en bloc: `GAME-TKT-047` a `GAME-TKT-049` restent planifiables au fil du front canonique, tandis que `GAME-TKT-050` et `GAME-TKT-051` demeurent geles jusqu'a fermeture du front prioritaire. `GAME-TKT-038` doit y etre traite comme dependance satisfaite localement.
