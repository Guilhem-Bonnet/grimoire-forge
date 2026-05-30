# Livrable Final — Mission Board Grimoire

> Projet : **Grimoire**
> Statut : **package definitif de conception et delivery**
> Orientation prioritaire : **memoire, contexte et tokens avant luxe de surface**

---

## 1. Objet du package

Ce livrable final ferme le chantier de conception du `Mission Board` Grimoire jusqu'au niveau de delivery documentaire executable. Il couvre :

- la these produit ;
- la spec systeme ;
- la decision architecturale ;
- le contrat runtime ;
- les schemas machine-readables ;
- la direction visuelle et UX ;
- les wireframes ;
- le plan d'implementation ;
- la matrice et la suite de verification.

Ce package est concu pour passer sans reinterpretation majeure vers l'implementation dans `grimoire-kit/apps/grimoire-game` et les surfaces runtime associees.

## 2. Decision structurante

Le `Mission Board` est **une projection causale et une surface de commande bornee**, jamais une source de verite parallele.

Conséquences non negociables :

1. Le board ne sait rien que le control plane ignore.
2. Toute commande est enveloppee, journalisee et rejouable.
3. Toute decision de routage est explicable.
4. Toute cloture est fail-closed.
5. Toute task ouverte doit soit avancer, soit se bloquer explicitement, soit escalader, soit etre annulee avec cause.
6. La projection du board doit rester frugale en contexte.

## 3. Priorite memoire, contexte et tokens

Le cap retenu est explicite : **le `Mission Board` doit consommer peu de contexte par defaut et n'ouvrir la profondeur que sur demande**.

### Regles du package

- `L1`: lecture board compacte, aucun transcript brut ;
- `L2`: drawer decisionnel, resume, rationale, refs ;
- `L3`: deep fetch explicite seulement ;
- aucune duplication longue des traces, preuves ou reviews dans les projections.

## 4. Inventaire des artefacts definitifs

### Socle canonique

- [SPEC-mission-board-grimoire.md](./SPEC-mission-board-grimoire.md)
- [ADR-007-mission-board-control-plane-causal.md](./ADR-007-mission-board-control-plane-causal.md)
- [CONTRAT-mission-board-grimoire.md](./CONTRAT-mission-board-grimoire.md)

### Documentation compagnon obligatoire

- [DOC-TECHNIQUE-mission-board-grimoire.md](./DOC-TECHNIQUE-mission-board-grimoire.md)
- [GUIDE-utilisation-mission-board-grimoire.md](./GUIDE-utilisation-mission-board-grimoire.md)

### Schemas machine-readables

- `contracts/mission-task.schema.json`
- `contracts/routing-decision.schema.json`
- `contracts/board-command-envelope.schema.json`
- `contracts/board-card-projection.schema.json`

### UX et DA

- [VISUAL-BRIEF-mission-board-grimoire.md](./VISUAL-BRIEF-mission-board-grimoire.md)
- [UX-MAP-mission-board-grimoire.md](./UX-MAP-mission-board-grimoire.md)
- [MOTION-SPEC-mission-board-grimoire.md](./MOTION-SPEC-mission-board-grimoire.md)
- [WIREFRAMES-mission-board-grimoire.md](./WIREFRAMES-mission-board-grimoire.md)

### Delivery et verification

- [PLAN-implementation-mission-board-grimoire.md](./PLAN-implementation-mission-board-grimoire.md)
- [MATRICE-verification-mission-board-grimoire.md](./MATRICE-verification-mission-board-grimoire.md)
- [SUITE-tests-mission-board-grimoire.md](./SUITE-tests-mission-board-grimoire.md)

## 5. Ce qui est effectivement verrouille

| Domaine | Etat |
| --- | --- |
| Contrat de task canonique | verrouille |
| Machine d'etat et colonnes derivees | verrouille |
| Contrat de routage et override | verrouille |
| Plane de hooks canoniques | verrouille |
| Closure guard task et mission | verrouille |
| Discipline memoire/contexte/tokens | verrouille |
| Rooms et shell UX | verrouille |
| Carte, drawer et motion semantique | verrouille |
| Plan de delivery et suite de verification | verrouille |

## 6. Ce qui reste volontairement hors package

- implementation code dans `grimoire-kit/apps/grimoire-game` ;
- marketplace ;
- federation ;
- runtime provider externe obligatoire ;
- ergonomies secondaires non adossees aux read models canoniques.

## 7. Definition of Done du package final

- le board est defini comme projection causale ;
- la spec et le contrat sont coherents ;
- les schemas machine-readables existent ;
- le plan d'implementation cible les bonnes landing zones ;
- la verification couvre nominal et negatif ;
- la documentation technique et le guide d'utilisation existent et sont synchronises avec le package ;
- l'UX est suffisamment precise pour passer en implementation ;
- le corpus est indexe dans `docs/exploitation/index.md`.

## 8. Ordre d'execution recommande apres ce livrable

1. Contracts runtime et events.
2. Projections board derives et replay-safe.
3. Routage, hooks et preview decisions.
4. Verification queue et closure guard.
5. Supervision stale/escalation.
6. Rooms, carte, drawer, motion et evidence visuelle.
7. E2E et preuve finale.

## 9. Verdict final

Le `Mission Board` Grimoire est maintenant specifie jusqu'au niveau **definitif de delivery documentaire**. Il peut entrer en implementation sans rouvrir les questions de structure, de causalite, de verification ou de DA.

La seule etape suivante legitime n'est plus un nouveau brainstorm. C'est l'execution tranchee du plan d'implementation.
