# Tickets d'Execution — Adaptation Gastownhall -> Grimoire

> Projet : **Grimoire**
> Plan source : [PLAN-adaptation-gastownhall-grimoire.md](./PLAN-adaptation-gastownhall-grimoire.md)
> Specs source : [SPEC-mission-ledger-grimoire.md](./SPEC-mission-ledger-grimoire.md), [SPEC-pack-registry-grimoire.md](./SPEC-pack-registry-grimoire.md)
> Regle : aucun ticket ne passe en Done sans contrat valide, preuves verifiables et mapping explicite vers les `GM-*` du plan maitre

---

## 1. Conventions

Statuts autorises :

- Backlog
- Ready
- In Progress
- Review
- Done

Definition of Ready :

- scope explicite ;
- dependances explicites ;
- mapping `GTA-*` et `GM-*` explicite ;
- criteres d'acceptation testables ;
- evidence attendue definie.

Definition of Done :

- criteres d'acceptation valides ;
- preuves de contrat, replay ou validation presentes ;
- documentation impactee mise a jour ;
- gates transverses references dans le plan source closes ou explicitement non applicables.

Regles de pilotage :

- `GTA-TKT-001` a `GTA-TKT-007` ouvrent la slice minimale recommandee du plan directeur.
- Aucun ticket de distribution ou federation ne s'ouvre avant stabilisation de `Mission Ledger`, `Pack Registry` et `Session Lineage`.
- Aucun ticket d'UI ne passe devant les tickets de contrat et de verification qui le supportent.

---

## 2. Mapping des workstreams vers le plan maitre

| Workstream | Intention | GM principaux a renforcer |
| --- | --- | --- |
| GTA-01 | `Mission Ledger` | GM-06, GM-08, GM-09, GM-10a, GM-33, GM-35, GM-35a, GM-39 |
| GTA-02 | `Workflow Instances` | GM-05, GM-08, GM-09, GM-24, GM-38, GM-39 |
| GTA-03 | `Pack Registry` | GM-03, GM-03a, GM-04, GM-27, GM-33a, GM-43, GM-44 |
| GTA-04 | `Session Lineage` | GM-08, GM-09, GM-37, GM-38, GM-39, GM-40, GM-40a |
| GTA-05 | `Supervision Chain` | GM-23, GM-24, GM-26, GM-32, GM-33, GM-36 |
| GTA-06 | `Verification Queue` | GM-23, GM-26, GM-35, GM-35a, GM-36 |
| GTA-07 | `Operator Surfaces` | GM-16, GM-17, GM-22, GM-25, GM-26, GM-38, GM-39, GM-40 |
| GTA-08 | `Verified Marketplace` | GM-03, GM-04, GM-27, GM-33a, GM-43, GM-44 |
| GTA-09 | `Grimoire Commons` | GM-41, GM-42, GM-43a, GM-44 |

---

## 3. Board des tickets

| Ticket | Priorite | Slice | Workstream | Titre | Dependances |
| --- | --- | --- | --- | --- | --- |
| GTA-TKT-001 | P0 | Slice A0 | GTA-01 | Schema canonique du Mission Ledger | Aucune |
| GTA-TKT-002 | P0 | Slice A0 | GTA-01 | Mapping runtime -> Mission Ledger -> read models | GTA-TKT-001 |
| GTA-TKT-003 | P0 | Slice A0 | GTA-02 | Workflow Instances + checkpoints + reprise | GTA-TKT-001 |
| GTA-TKT-004 | P0 | Slice A0 | GTA-03 | Manifest `Pack Registry` + validateur de schema | Aucune |
| GTA-TKT-005 | P0 | Slice A0 | GTA-03 | Resolution des packs, overlays et policies | GTA-TKT-004 |
| GTA-TKT-006 | P0 | Slice A0 | GTA-04 | Session Lineage canonique | GTA-TKT-001 |
| GTA-TKT-007 | P0 | Slice A0 | GTA-04 | Surface `Seance` read-only sur sessions closes | GTA-TKT-006 |
| GTA-TKT-008 | P1 | Slice A1 | GTA-05 | Taxonomie d'incidents + file de supervision | GTA-TKT-001, GTA-TKT-006 |
| GTA-TKT-009 | P1 | Slice A1 | GTA-06 | Verification Queue coeur + verrous de transition | GTA-TKT-001, GTA-TKT-002 |
| GTA-TKT-010 | P1 | Slice A1 | GTA-06 | Alignement Evidence Pack + attestations + verdicts | GTA-TKT-009 |
| GTA-TKT-011 | P1 | Slice A2 | GTA-07 | Read models board pour missions, lineage et verification | GTA-TKT-002, GTA-TKT-006, GTA-TKT-009 |
| GTA-TKT-012 | P1 | Slice A2 | GTA-07 | Surfaces board de supervision, Library et Branch Finisher | GTA-TKT-008, GTA-TKT-009, GTA-TKT-011 |
| GTA-TKT-013 | P2 | Slice A3 | GTA-08 | Contrat du Verified Marketplace | GTA-TKT-004, GTA-TKT-005 |
| GTA-TKT-014 | P2 | Slice A3 | GTA-08 | Gates de publication, install et compatibilite des packs | GTA-TKT-013 |
| GTA-TKT-015 | PX | Slice A4 | GTA-09 | Schema experimental Grimoire Commons | GTA-TKT-001, GTA-TKT-010 |
| GTA-TKT-016 | PX | Slice A4 | GTA-09 | Provider local et vues read-only des commons | GTA-TKT-015, GTA-TKT-011 |

---

## 4. Tickets detailles P0 et P1 critiques

### GTA-TKT-001 — Schema canonique du Mission Ledger

Priorite : P0

Objectif :

Definir une unite machine-readable commune pour mission, item de travail, dependance, evidence, verification, escalation et attestation.

Mapping :

- Workstream : GTA-01
- GM : GM-06, GM-08, GM-09, GM-10a, GM-33, GM-35, GM-35a, GM-39

Scope :

- schema des objets coeur du ledger ;
- contraintes minimales d'identite, de provenance, de correlation et d'idempotence ;
- modele de statuts mission/item ;
- format d'export et de stockage initial.

Criteres d'acceptation :

- chaque objet critique possede un schema valide et versionne ;
- les references `traceId`, `actor`, `source`, `requestId` et `idempotencyKey` sont explicites sur les mutations critiques ;
- le modele couvre les besoins de `task-view`, `verification-view` et `runtime-dashboard-view` sans duplicer leur logique metier.

Evidence attendue :

- schema documente ;
- exemples valides et invalides ;
- tests de validation et de serialisation.

---

### GTA-TKT-002 — Mapping runtime -> Mission Ledger -> read models

Priorite : P0

Objectif :

Brancher les evenements runtime existants au ledger et en deriver des read models stables.

Mapping :

- Workstream : GTA-01
- GM : GM-08, GM-09, GM-35, GM-39

Scope :

- mapping `TASK_UPDATE`, `TASK_TRANSITION`, `WORKFLOW_STEP`, `TOOL_CALL`, `VERIFICATION_GATE`, `RUNTIME_ERROR`, `AGENT_STATUS_UPDATE` ;
- projection vers missions, items, verification queue et supervision ;
- gestion des doublons et de l'ordre.

Criteres d'acceptation :

- le meme flux d'evenements reconstruit le meme etat ledger ;
- un event replaye ne duplique pas les artefacts du ledger ;
- les vues runtime derivees peuvent lire le ledger sans contourner les contrats existants.

Evidence attendue :

- matrice de mapping evenement -> mutation ledger ;
- tests replay, duplicate et out-of-order ;
- preuve de projection board cohérente.

---

### GTA-TKT-003 — Workflow Instances + checkpoints + reprise

Priorite : P0

Objectif :

Introduire une representation instanciee des workflows et de leurs checkpoints pour rendre l'execution reprenable et comparable.

Mapping :

- Workstream : GTA-02
- GM : GM-05, GM-08, GM-09, GM-24, GM-38, GM-39

Scope :

- modele `recipe` versus `workflow instance` ;
- etats `planned`, `running`, `paused`, `blocked`, `completed`, `failed` ;
- checkpoints, retries et resume context ;
- lien vers mission, task, evidence et lineage.

Criteres d'acceptation :

- un workflow peut etre interrompt puis repris sans duplication d'effets ;
- les checkpoints sont lisibles et comparables entre runs ;
- l'instance expose un historique causal exploitable par le board.

Evidence attendue :

- spec de l'instance ;
- exemples de reprise ;
- tests de resume, abort et divergence.

---

### GTA-TKT-004 — Manifest `Pack Registry` + validateur de schema

Priorite : P0

Objectif :

Definir le contrat minimal des packs Grimoire et le validateur associe.

Mapping :

- Workstream : GTA-03
- GM : GM-03, GM-03a, GM-04, GM-27, GM-33a, GM-43

Scope :

- manifest `pack.yaml` ;
- metadata `name`, `version`, `status`, `owner`, `compatibility`, `source` ;
- composants declares et surfaces cibles ;
- regles de validation minimales.

Criteres d'acceptation :

- un pack invalide est refuse avec erreur exploitable ;
- un pack valide peut etre materialise sans ambiguite sur ses surfaces ;
- le schema est assez strict pour bloquer les activations implicites.

Evidence attendue :

- spec du manifest ;
- exemples de packs valides et invalides ;
- sorties du validateur.

---

### GTA-TKT-005 — Resolution des packs, overlays et policies

Priorite : P0

Objectif :

Formaliser l'ordre de composition des packs, overlays et overrides, avec policies et provenance explicites.

Mapping :

- Workstream : GTA-03
- GM : GM-03, GM-03a, GM-27, GM-33a, GM-44

Scope :

- ordre de resolution `includes -> pack local -> overlays -> overrides operateur` ;
- detection de cycles ;
- merge additif des providers et precedence du consommateur ;
- hash de contenu et materialisation d'un lock file.

Criteres d'acceptation :

- deux resolutions identiques donnent le meme resultat materialise ;
- un cycle d'include est detecte et bloque ;
- les policies resolues sont lisibles et auditables.

Evidence attendue :

- table des priorites de merge ;
- exemples de resolution ;
- tests de collision, override et cycle.

---

### GTA-TKT-006 — Session Lineage canonique

Priorite : P0

Objectif :

Unifier la genealogie `session -> run -> trace -> evidence -> decision`.

Mapping :

- Workstream : GTA-04
- GM : GM-08, GM-09, GM-37, GM-38, GM-39, GM-40, GM-40a

Scope :

- modele des identifiants et references ;
- relation predecesseur/successeur ;
- index read-only ;
- liens avec la memoire et les verdicts.

Criteres d'acceptation :

- une decision critique est reliée a une session et a un run de maniere stable ;
- le lineage supporte replay et lectures differees ;
- la stale memory peut pointer un lineage ou une absence de lineage.

Evidence attendue :

- schema du lineage ;
- exemples de chaines relues ;
- tests de reconstruction et de collisions d'identifiants.

---

### GTA-TKT-007 — Surface `Seance` read-only sur sessions closes

Priorite : P0

Objectif :

Exposer une primitive de questionnement et de reprise de sessions precedentes sans transcript brut obligatoire.

Mapping :

- Workstream : GTA-04
- GM : GM-25, GM-38, GM-39, GM-40

Scope :

- recherche de sessions predecessrices ;
- reponse read-only a une question operateur ;
- filtrage par mission, run, agent, tag ou evidence ;
- progressive disclosure.

Criteres d'acceptation :

- la surface ne permet aucune mutation ;
- les reponses se basent sur le lineage, le ledger et les projections, pas sur une synthese libre opaque ;
- une session close peut etre interrogee par mission et par trace.

Evidence attendue :

- spec de requete ;
- scenarios de lecture ;
- tests read-only et cas de session manquante.

---

### GTA-TKT-008 — Taxonomie d'incidents + file de supervision

Priorite : P1

Objectif :

Transformer les checks existants en une file coherente de supervision et d'escalation.

Mapping :

- Workstream : GTA-05
- GM : GM-23, GM-24, GM-26, GM-32, GM-33, GM-36

Scope :

- typologie des incidents ;
- severites et politiques de relance ;
- file des incidents et diagnostics lies ;
- raccord health-check, self-heal, preflight, memory-lint, quick-check.

Criteres d'acceptation :

- un incident critique remonte avec contexte, severite et action suivante ;
- la supervision sait distinguer alerte, blocage, escalade et bruit ;
- les checks existants se projettent dans une vue unifiee.

Evidence attendue :

- taxonomie d'incidents ;
- scenarios de stuck/stall/reject ;
- preuves de projection vers la file.

---

### GTA-TKT-009 — Verification Queue coeur + verrous de transition

Priorite : P1

Objectif :

Faire passer les claims de completion par une file de verification explicite avec verrous et verdicts.

Mapping :

- Workstream : GTA-06
- GM : GM-23, GM-26, GM-35, GM-35a, GM-36

Scope :

- file de verification ;
- statuts `queued`, `verifying`, `accepted`, `rejected`, `needs_work` ;
- verrous de transition `review -> done` ;
- lien vers evidence et attestation.

Criteres d'acceptation :

- aucun `done` ne contourne la verification queue ;
- un rejet garde la chaine causale et la preuve associee ;
- les verrous sont lisibles et auditables depuis le board.

Evidence attendue :

- spec de la queue ;
- tests de rejection/acceptation ;
- exemples de verdicts et de verrous.

---

### GTA-TKT-010 — Alignement Evidence Pack + attestations + verdicts

Priorite : P1

Objectif :

Unifier evidence pack, verdict de verification et attestation operatoire.

Mapping :

- Workstream : GTA-06
- GM : GM-35, GM-35a, GM-36, GM-43a

Scope :

- format d'evidence pack enrichi ;
- lien `action -> controle -> verdict -> evidenceRef` ;
- modele d'attestation minimal ;
- export lisible par les surfaces board et docs d'evidence.

Criteres d'acceptation :

- un verdict de verification pointe toujours vers une evidence exploitable ;
- l'attestation reste une preuve operatoire et non un signal social flou ;
- l'evidence pack devient recherchable par mission, item et verification.

Evidence attendue :

- structure de l'evidence pack ;
- exemples de verdicts lies ;
- tests d'export et de lecture.

---

## 5. Tickets suivants a ouvrir apres la slice minimale

### GTA-TKT-011 — Read models board pour missions, lineage et verification

- Priorite : P1
- Workstream : GTA-07
- Dependances : GTA-TKT-002, GTA-TKT-006, GTA-TKT-009
- GM : GM-16, GM-17, GM-38, GM-39

### GTA-TKT-012 — Surfaces board de supervision, Library et Branch Finisher

- Priorite : P1
- Workstream : GTA-07
- Dependances : GTA-TKT-008, GTA-TKT-009, GTA-TKT-011
- GM : GM-22, GM-25, GM-26, GM-40

### GTA-TKT-013 — Contrat du Verified Marketplace

- Priorite : P2
- Workstream : GTA-08
- Dependances : GTA-TKT-004, GTA-TKT-005
- GM : GM-03, GM-04, GM-43, GM-44

### GTA-TKT-014 — Gates de publication, install et compatibilite des packs

- Priorite : P2
- Workstream : GTA-08
- Dependances : GTA-TKT-013
- GM : GM-27, GM-33a, GM-43, GM-44

### GTA-TKT-015 — Schema experimental Grimoire Commons

- Priorite : PX
- Workstream : GTA-09
- Dependances : GTA-TKT-001, GTA-TKT-010
- GM : GM-41, GM-43a, GM-44

### GTA-TKT-016 — Provider local et vues read-only des commons

- Priorite : PX
- Workstream : GTA-09
- Dependances : GTA-TKT-015, GTA-TKT-011
- GM : GM-41, GM-42, GM-43a

---

## 6. Regle d'usage

Ce paquet de tickets sert a convertir le plan directeur en ordre d'execution :

- il impose un lien `ticket -> workstream -> GM -> evidence` ;
- il borne la slice minimale recommandee ;
- il interdit l'ouverture prematuree de marketplace ou federation ;
- il doit etre mis a jour si les schemas ou les gates structurants changent.
