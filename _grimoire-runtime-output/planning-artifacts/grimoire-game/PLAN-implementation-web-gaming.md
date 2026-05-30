# Plan d'Implementation Web/Gaming — Grimoire Game

> Projet : **Grimoire Game**
> Statut : **Plan d'execution canonique (sans estimation temporelle)**
> Sources : [CdC](./CdC-grimoire-game.md), [GDD](./GDD-grimoire-game.md), [TECH](./TECH-grimoire-game.md), [EPICS](./EPICS-grimoire-game.md), [PAQUET front prioritaire](./PAQUET-execution-front-prioritaire-post-challenge.md), [PAQUET guardrails](./PAQUET-execution-agentic-guardrails-runtime.md), [CONTRAT guardrails](./CONTRAT-runtime-agentic-guardrails.md), [PAQUET host bridge](./PAQUET-execution-host-bridge-agentique-externe.md), [CONTRAT host bridge](./CONTRAT-host-bridge-agentique-externe.md), [PAQUET multi-PC](./PAQUET-execution-multi-pc-runtime.md), [UX cockpit/observateur](./UX-cockpit-observateur-multi-pc.md)

---

## 1. Objectif de ce plan

Transformer le corpus de specifications en un plan d'implementation unique, ordonne, testable et directement executable pour le projet web/gaming.

Le but produit n'est pas de creer une interface "fun" orientee jeu autonome. Le but est de fournir un
outil visuel, intuitif et operable pour custom/debug/comprendre/modifier/ajuster le systeme d'agents.
La gamification est utilisee comme langage d'interaction et de lisibilite, pas comme finalite.

Ce document devient la reference operationnelle pour:

- prioriser les travaux,
- sequencer les lots techniques,
- valider chaque increment avec preuves,
- eviter les regressions pendant la montee en capacite du jeu.

---

## 2. Principes de pilotage

- **Vertical slices d'abord** : livrer des increments traversant front, moteur, bridge, persistence et tests.
- **Evidence before completion** : aucun lot n'est clos sans tests et preuves de comportement.
- **Etat unique observable** : la source de verite est un store central synchronise avec les evenements WS.
- **Contrat canonique avant surfaces** : le front immediat est `run/host/proof -> flux critique prouve -> cockpit minimal -> extensions`.
- **Aucune logique implicite** : transitions d'etat explicites, erreurs explicites, fallback explicite.
- **Adapter boundary stable** : toute integration agent passe par `AgentAdapter` pour garder le coeur agnostique.
- **Security by default** : auth, autorisations et mode spectateur read-only verifies par defaut.
- **Asset pipeline gouverne** : toute ressource graphique provient de [grimoire-game-assets](../../../grimoire-game-assets/README.md) et de ses manifests.
- **Gamification utilitaire** : chaque mecanique visuelle doit augmenter la comprehension et la capacite
  d'action sur les agents (jamais ajouter du bruit ludique sans valeur operationnelle).

### Priorite normative transverse

| Referentiel | Priorite | Role dans le plan runtime |
| --- | --- | --- |
| OWASP Agentic Skills Top 10 | P0 | Gouverner les surfaces d'execution exposees par skills, plugins, power cards, tools et configurations activables |
| Agentic Integrity Verification Specification (AIVS) | P1 | Transformer verification gate, audit trail et evidence pack en chaine de verification exploitable sur les transitions critiques |
| IEEE P3394 Universal Message Format (UMF) | P2 | Piloter une enveloppe canonique de message pour runtime, replay, spectateur et vues multi-sessions sans figer trop tot tout le produit |

Regle de claim:

- Le plan parle d'alignement et de pilotes bornes, jamais de conformite complete, tant qu'aucun mapping explicite vers preuves et gates n'est ferme.

### Front prioritaire post-challenge

Avant toute ouverture large du backlog, le runtime doit fermer le front suivant dans cet ordre:

1. `GAME-TKT-052` : contrat canonique `run/host/proof` sur panier critique borne ;
2. `GAME-TKT-053` : flux critique mono-host `preview -> validation -> commit borne` prouve ;
3. `GAME-TKT-054` : cockpit minimal expert branche sur cette meme spine.

Regles de sequencing associees:

- `GAME-TKT-040` a `GAME-TKT-046` restent bloques tant que `GAME-TKT-054` n'est pas prouve ;
- `GAME-TKT-050` et `GAME-TKT-051` restent bloques tant que `GAME-TKT-054` n'est pas prouve ;
- `GAME-TKT-012` a `GAME-TKT-036` ne rouvrent pas un second chemin canonique avant cloture de ce front.

---

## 3. Perimetre d'execution

Le plan couvre:

- Moteur 2D canvas et navigation rooms,
- Bridge agentique (events WS + import JSONL),
- Connectivite agentique externe via Host Bridge canonique (Copilot, Claude, hotes MCP-compatibles),
- UI game/HUD/Kanban/inspection,
- Verification gates qualite,
- Persistence locale,
- Integration board dans l'ecosysteme grimoire.

Hors perimetre de ce plan:

- Creation de nouveaux styles DA complets,
- Features experimentales non reliees au CdC,
- Integrations externes non mappees sur `Host Binding`, `Capability Manifest`, `Invocation Envelope`, `Review Artifact` et `Context Ledger`.

---

## 4. Ecarts critiques a fermer en premier

### Ecart A — Prototype runtime trop statique

Symptomes:

- Donnees embarquees dans la page,
- Couplage fort rendu/donnees,
- Faible capacite de reprise d'etat.

Resultat attendu:

- Store de simulation unique,
- Chargement d'etat par API/WS,
- Reconciliation robuste apres reconnexion.

### Ecart B — Couverture partielle des exigences CdC

Symptomes:

- Presence d'une visualisation mais couverture inegale des requirements F03 a F26.

Resultat attendu:

- Traçabilite requirement -> implementation -> test,
- Gate de verification avant passage DONE.

### Ecart C — Observabilite et audit encore incomplets

Symptomes:

- Peu de preuves normalisees sur les transitions critiques.

Resultat attendu:

- Logs d'audit JSONL standards,
- Panneau debug filtrable,
- Historique de verification consultable.

### Ecart D — Fiabilite du flux evenementiel sous-definie

Symptomes:

- Gestion partielle des doublons, out-of-order et replay des evenements,
- Risque d'etats divergents entre client, serveur et bridge.

Resultat attendu:

- Sequence IDs + idempotency keys sur evenements critiques,
- Strategie de replay/resync documentee et testee.

### Ecart E — Securite applicative insuffisamment explicitee

Symptomes:

- Regles d'autorisation encore implicites pour actions sensibles,
- Surface d'attaque non cadrée pour WS/API/Viewer mode.

Resultat attendu:

- Matrice RBAC simple (orchestrateur, agent, spectateur),
- Verification systematique auth/authz + audit trail.

### Ecart F — Mode LIVE et multi-sessions encore partiels

Symptomes:

- Mode LIVE present mais base sur ancrage timeline + auto-refresh global de page,
- Representation multi-sessions surtout par filtres et listes, sans vue parallele unifiee,
- Correlation inter-sessions insuffisante pour debugger des executions simultanees.

Resultat attendu:

- Mode LIVE incremental (sans reload complet) avec latence visuelle faible,
- Vue multi-sessions explicite des executions paralleles et de leurs interactions,
- Correlation robuste session/run/worker/correlation_id sur les evenements et la memoire.

### Ecart G — Gouvernance des surfaces d'execution encore implicite

Symptomes:

- Skills, plugins et power cards prevus sans matrice de risque explicite,
- Activation UI ou runtime encore trop peu liee a provenance, policy et trust status.

Resultat attendu:

- Matrice OWASP Agentic Skills Top 10 -> surfaces runtime -> controles -> gates,
- Activation fail-closed des surfaces d'execution sans metadata ni policy minimales.

### Ecart H — Integrite verifiable et enveloppe canonique de message encore diffuses

Symptomes:

- Les preuves existent mais restent encore trop proches du simple log d'audit,
- Les payloads critiques risquent de diverger entre runtime, replay, spectateur et vues multi-sessions.

Resultat attendu:

- Chaine minimale action -> controles -> verdict -> evidence ref sur les transitions critiques,
- Pilote d'enveloppe canonique partagee entre eventing runtime, replay et lectures read-only.

### Ecart I — Coordination multi-PC et control plane encore implicites

Symptomes:

- La cible produit suppose maintenant plusieurs PCs sur un projet actif commun,
- mais le registre projet, les leases TTL, les heartbeats de noeuds, la discipline d'ownership Git et la frontiere cockpit contre observateur ne sont pas encore un lot explicite.

Resultat attendu:

- un control plane logique unique pour la V1,
- un protocole `node manager` visible par le cockpit,
- des claims de taches recuperables sans double mutation durable,
- une discipline `une tache -> une branche -> un owner -> un worktree`,
- un cockpit live et une office view minimale branches sur les memes projections.

### Ecart J — Connectivite agentique externe encore non contractualisee

Symptomes:

- Les surfaces Copilot, Claude et MCP sont connues au niveau produit, mais pas converties en contrats runtime du plan d'execution.
- Les reviews externes, permission prompts, imports de contexte et etats de connexion restent implicites.
- Le pont VS Code existe comme cible locale, sans modele generique de Host Bridge partageable.

Resultat attendu:

- Un modele canonique `Host Binding` + `Capability Manifest` pour tout hote externe.
- Une enveloppe d'invocation et un ledger de contexte replayables sans dependre de l'UX du vendeur.
- Une policy fail-closed pour les connecteurs externes.
- Une normalisation des reviews et checks externes en evidence pack exploitable.

---

## 5. Backlog priorise (sans calendrier)

### 5.1 Priorite P0 — Fondations indispensables

| ID | Theme | Livrable | Critere de validation |
| --- | --- | --- | --- |
| P0-01 | State Core | Store central `GameState` + schema Zod + hydration | Reconnexion: etat identique apres `STATE_SNAPSHOT` |
| P0-02 | WS Contract | Contrat d'evenements versionne (`ClientEvent`/`ServerEvent`) | Rejet strict des events invalides + tests de contrat |
| P0-03 | ECS Runtime | Entites/composants/systemes isoles et profiles | Ordre deterministe des systemes sur un tick donne |
| P0-04 | Path & Collision | A* + nav-grid + colliders room-aware | Aucun passage au travers des murs/colliders |
| P0-05 | Verification Gate | `VERIFICATION_GATE` bloque DONE sans preuve | Carte reste en REVIEW sans evidence exploitable |
| P0-06 | Asset Integration | Chargement assets depuis export gouverne | Aucune dependance asset hors manifests |
| P0-07 | AgentAdapter Core | Contrat `AgentAdapter` + implementation bridge grimoire | Changer d'adapter ne casse pas le coeur de simulation |
| P0-08 | Event Reliability | Sequence IDs + idempotence + replay snapshot | Aucun etat duplique apres reconnexion/replay |
| P0-09 | Security Baseline | Auth WS/API + RBAC minimal + mode spectateur verrouille | Actions write interdites en lecture seule |
| P0-10 | Agentic Surface Guardrails | Matrice OWASP Agentic Skills + policy minimale sur skills/plugins/power cards | Aucune activation de surface d'execution sans provenance, trust status et controle explicite |
| P0-11 | Control Plane V1 | Registre projet, identifiants canoniques, enveloppe live, projections de flotte | Un run multi-PC se reconstruit sans correlation fragile |
| P0-12 | Node Fleet & Leases | Node managers, heartbeats, leases TTL, claims de taches | Une perte de noeud ne cree pas de double mutation durable |
| P0-13 | Distributed Git Ownership | Ownership runtime aligne sur branche et worktree dedies | Aucun perimetre mutable n'est travaille par deux agents sans ownership explicite |
| P0-14 | External Host Canon | `Host Binding` + `Capability Manifest` + registre des hotes externes | Aucun hote externe n'entre au runtime sans contrat explicite |
| P0-15 | Host Invocation Contract | `Invocation Envelope` + `Context Ledger` + `Review Artifact` additives au protocole `v1` | Une action issue d'un hote reste rejouable et auditable sans ambiguite |
| P0-16 | External Connector Policy | Permission prompts, scopes, allowlists, degrade states et fail-closed | Aucun connecteur externe non approuve ne peut muter l'etat durable |

### 5.2 Priorite P1 — Fonctionnalites coeur produit

| ID | Theme | Livrable | Critere de validation |
| --- | --- | --- | --- |
| P1-01 | Agent Inspection | Panel deep inspection (model, branche, prompt, tokens, outils) | Clic agent -> panneau complet + actions fonctionnelles |
| P1-02 | Kanban In-world | Board par room + drag/drop + sync activite agent | Etat carte coherent avec activite reelle agent |
| P1-03 | Inter-agent Comms | Bulles + liens visuels + meetings inter-teams | Trace complete dans logs de communication |
| P1-04 | Workflow Visual | Chemin workflow + step courant + historique decisions | Navigation du graphe sans perte de contexte |
| P1-05 | Challenge Room | Workflow challenge (presentation/critique/vote/iteration) | Sortie challenge cree actions correctives automatiques |
| P1-06 | Memory/Library | Visualisation memoire active + long terme | Acces memoire trace et anime correctement |
| P1-07 | Live Observatory | Flux live incremental (sans reload global) + fallback replay | Les updates live n'interrompent pas la navigation utilisateur |
| P1-08 | Multi-Session Matrix | Vue parallele par session/run + etat compare | Le parallelisme inter-sessions est lisible en un ecran |
| P1-09 | Session Diff | Diff visuel entre deux sessions (etat, decisions, anomalies) | Les causes de divergence sont identifiables en lecture directe |
| P1-10 | Explainability Panel | Panneau "pourquoi cet etat" avec chaine causale | Chaque transition critique expose sa provenance exploitable |
| P1-11 | Verification Integrity Chain | Chaine de verification orientee AIVS sur les transitions critiques | Une verification reste reconstruisible sans synthese manuelle du reviewer |
| P1-12 | Cockpit Live Multi-PC | Vue experte projet/noeuds/taches/verrous/preuves | L'operateur repond vite a `qui fait quoi, ou, et pourquoi` |
| P1-13 | Office View Minimale | Observateur spatial sur les memes read models que le cockpit | La scene ajoute une comprehension reelle sans divergence |
| P1-14 | Bounded Command Gateway | Budget de mutation GUI borne, authz, audit, spectator partageable | Toute mutation GUI est fail-closed, idempotente et tracee |
| P1-15 | External Reviews as Evidence | Reviews, PR et checks externes normalises dans le cockpit | Une review externe se relit sans repasser par son outil d'origine |
| P1-16 | Generic Host Bridge | Surface multi-host generique au-dessus du pont VS Code | Un meme run reste lisible depuis web, VS Code et un hote externe |

### 5.3 Priorite P2 — Capacites avancees

| ID | Theme | Livrable | Critere de validation |
| --- | --- | --- | --- |
| P2-01 | Worktree Room | Room dynamique par branche + actions merge/pr/discard | Changement branche reflechi visuellement sans ambiguite |
| P2-02 | Power Cards | Cartes plugin activables avec effets et persistence | Etat plugin persiste et visible sur sprite |
| P2-03 | Retro Room | Vue retrospective + snapshot JSON compare | Generation snapshot validee et consultable |
| P2-04 | Spectator Mode | Lecture seule partageable tokenisee | Aucune mutation possible en mode spectateur |
| P2-05 | VS Code Surface | Pont diagnostics/perf vers UI game | Flux d'info lisible sans bruit excessif |
| P2-06 | Canonical Message Envelope Pilot | Pilote UMF borne pour runtime, replay, spectateur et multi-sessions | Les lectures critiques reutilisent une enveloppe commune sans casser les payloads existants |

---

## 6. Ordre d'implementation recommande (vertical slices)

### Slice 0 — Contrats et garde-fous

Contenu:

- Contrat `ClientEvent`/`ServerEvent` versionne,
- `AgentAdapter` stable pour integration grimoire,
- Auth/RBAC de base,
- Matrice OWASP Agentic Skills minimale pour les surfaces d'execution exposees,
- mode canonique des hotes externes et manifests de capabilities,
- enveloppes d'invocation, ledgers de contexte et policy fail-closed pour les connecteurs externes,
- Strategie sequence/idempotence/replay.

Definition of done slice:

- Les contrats rejectent tout payload invalide,
- Un replay d'evenements ne cree pas de duplicat d'etat,
- Aucune activation de surface d'execution ne passe sans provenance, policy et trust status minimaux,
- aucune activation issue d'un hote externe ne contourne `preview -> validation -> commit`,
- Les roles sans permission ne peuvent pas muter l'etat.

### Slice 1 — Boucle jouable minimale et robuste

Contenu:

- `GameState` central,
- map + rooms + navigation fiable,
- affichage agents depuis etat distant,
- fallback de reconnexion,
- protocole de node manager et projection de flotte minimale,
- leases TTL et claims de taches,
- discipline Git distribuee par branche et worktree.

Definition of done slice:

- Le board reste coherent apres deconnexion/reconnexion.
- Les agents se deplacent selon un path valide et observable.
- Les tests de contrat WS passent.
- Une perte de noeud ne laisse ni ownership zombie ni double mutation durable.

### Slice 2 — Travail agent observable de bout en bout

Contenu:

- Mapping tool -> animation,
- panel inspection agent,
- logs filtrables,
- chaine minimale de verification orientee AIVS,
- reviews externes, checks et commentaires normalises en evidence pack,
- verification gate avant DONE,
- `Cockpit Live` multi-PC,
- office view minimale et war room observateur,
- gateway de commande GUI bornee.

Definition of done slice:

- Toute transition critique laisse une preuve consultable.
- Toute verification critique laisse une chaine action -> controles -> verdict -> evidence ref consultable.
- Le passage DONE sans evidence est impossible.
- Une review Copilot, Claude ou PR importee se rattache au meme ledger que le run concerne.
- Le cockpit et l'office view affichent la meme causalite et le meme focus pour un meme run.

### Slice 3 — Collaboration multi-equipes in-world

Contenu:

- Kanban in-world,
- communication inter-agents,
- challenge room et cycle de review.

Definition of done slice:

- Une tache traverse Backlog -> Done avec trace complete.
- Les handoffs inter-teams sont visibles et auditable.

### Slice 4 — Capacites avancees et ecosysteme

Contenu:

- worktree rooms,
- power cards,
- retro room,
- spectator mode,
- host bridge generique et surface multi-host,
- integration ecosysteme grimoire.

Definition of done slice:

- Les fonctions avancees n'impactent pas la stabilite du coeur.
- L'ensemble reste conforme a l'interface `AgentAdapter`.
- Le pont VS Code et les hotes externes partagent les memes contrats et read models.

### Slice 5 — Gouvernance transverse et robustesse decisionnelle

Contenu:

- gouvernance drift prompts/politiques,
- reprise incident,
- qualite memoire/recall,
- anti-chambre d'echo,
- FinOps agentique,
- explicabilite operationnelle,
- conformite licences/provenance,
- experimentation produit.

Tickets associes:

- GAME-TKT-021 a GAME-TKT-028.

Definition of done slice:

- Chaque axe transverse est relie a une verification explicite et a une preuve exploitable.
- Les gates transverses bloquent effectivement les transitions non conformes.
- Les decisions critiques restent auditables et reproductibles.

### Slice 6 — Fermeture des ecarts CdC et finalisation in-world

Contenu:

- Agent Factory complet,
- configuration gamifiee complete,
- systeme sonore,
- progression XP/achievements,
- onboarding first-run,
- Investigation Lab + cycle review,
- Branch Finisher + Security Audit Room,
- fermeture des slots CdC encore manquants.

Tickets associes:

- GAME-TKT-029 a GAME-TKT-036.

Definition of done slice:

- Les ecarts priorises de la matrice sont convertis en comportements verifies in-world.
- Les preuves de verification sont rattachees aux tickets de couverture.
- Les exigences fonctionnelles cibles passent de partiel/non-couvert a couvert.

### Slice 7 — Observabilite LIVE et parallelisme multi-sessions

Contenu:

- live incremental sans reload global,
- vue multi-sessions unifiee (session/run/worker/lane),
- correlation inter-sessions et detection des divergences,
- pilote d'enveloppe canonique de message pour runtime/replay/spectateur,
- panneau explicatif des transitions critiques.

Definition of done slice:

- Le mode LIVE est utilisable en continu sans casser le contexte utilisateur.
- Les sessions paralleles sont comparables et corrigeables depuis une vue unique.
- Les surfaces runtime, replay et lecture seule convergent sur une enveloppe de message bornee et testee.
- Toute divergence critique est rattachee a une chaine causale lisible.

## 6-bis. Artefacts operatoires prioritaires et multi-PC

Le front post-challenge doit maintenant etre lu et execute via un artefact operatoire dedie avant la tranche multi-PC.

- [PAQUET-execution-front-prioritaire-post-challenge.md](./PAQUET-execution-front-prioritaire-post-challenge.md) porte l'ordre d'attaque technique, les landing zones et les preuves attendues pour `GAME-TKT-052` a `GAME-TKT-054`.

La tranche multi-PC V1 doit maintenant etre lue et executee via deux artefacts operatoires dedies.

- [PAQUET-execution-multi-pc-runtime.md](./PAQUET-execution-multi-pc-runtime.md) porte l'ordre d'attaque technique, les work packages, les fichiers pivots et les preuves attendues de `GAME-TKT-040` a `GAME-TKT-046`.
- [UX-cockpit-observateur-multi-pc.md](./UX-cockpit-observateur-multi-pc.md) porte la frontiere cockpit contre observateur, le budget de mutation GUI et la parite de read models.

Regles d'application :

- tout lancement runtime large commence par le paquet prioritaire post-challenge ;
- toute story ou ticket de la tranche multi-PC doit pointer vers ces deux artefacts avant lancement ;
- aucune UI multi-PC ne part en implementation si elle n'identifie pas le read model partage qu'elle consomme ;
- aucune commande GUI ne part en implementation si elle n'apparait pas dans le budget de mutation borne.

---

## 7. Matrice de verification qualite

| Axe | Verification minimum |
| --- | --- |
| Contrats WS | Tests schema + tests d'interoperabilite client/server |
| Simulation | Tests unitaires ECS + tests integration boucle de jeu |
| Navigation | Tests sur obstacles, no-path, replanification |
| UI critique | Tests d'interaction panel agent et kanban |
| Challenge | Tests de workflow review et creation automatique d'actions |
| Persistence | Relecture des snapshots et coherence des etats |
| Securite | Tests auth/authz WS/API + interdictions spectateur |
| Surfaces d'execution | Tests provenance/policy/trust sur skills/plugins/power cards et activations UI |
| Integrite verifiable | Tests de chaine action -> controles -> verdict -> evidence ref sur transitions critiques |
| Enveloppe canonique | Tests d'interoperabilite de l'enveloppe commune entre runtime, replay et spectateur |
| Hotes externes | Tests de `Host Binding`, `Capability Manifest`, permission prompts et degradation fail-closed |
| Reviews externes | Tests d'import `review -> evidence pack -> audit-view` |
| Resilience eventing | Tests out-of-order, duplicate et replay |
| LIVE incremental | Tests flux live sans reload global + coherence timeline |
| Multi-sessions | Tests de correlation session/run/worker + vues paralleles |
| Performance | Budget frame stable avec charge agent representative |
| Non-regression | Suite `quick-check` + tests modifies + lint |

---

## 8. Regles de completion

Un lot est complete uniquement si:

- Le comportement attendu est visible dans l'UI de jeu,
- Les tests associes passent,
- Les contrats de donnees sont valides,
- Les logs d'audit sont presentes,
- La documentation d'usage est mise a jour dans les artefacts de planning/implementation.
- Les permissions et restrictions de role sont verifiees en tests.
- Les scenarios de reconnexion/replay n'introduisent aucun etat incoherent.

Aucune completion declaree sans preuves executables.

---

## 9. Next actions immediates (ordre strict)

1. Geler les identites canoniques et les validateurs Zod du contrat `run/host/proof`.
2. Poser le contrat `AgentAdapter` et l'implementation grimoire de reference sans bypass du flux critique.
3. Mettre en place sequence IDs, idempotence, provenance minimale et replay borne sur le panier critique.
4. Poser auth/RBAC minimal (orchestrateur, agent, spectateur) et refuser toute mutation critique incomplete.
5. Definir la matrice OWASP Agentic Skills minimale pour les surfaces d'execution du panier critique.
6. Poser le modele canonique des hotes externes et leurs capability manifests sans ouvrir encore la surface multi-host.
7. Etendre les contrats runtime avec `Host Binding`, `Invocation Envelope`, `Context Ledger` et `Review Artifact` sur le panier critique seulement.
8. Durcir la policy des connecteurs externes (permission prompts, allowlists, degrade states, fail-closed) sur le panier critique seulement.
9. Introduire `GameState` central + hydration snapshot sur le flux critique de reference.
10. Integrer `VERIFICATION_GATE` et la chaine action -> controles -> verdict -> evidence sur ce flux critique.
11. Prouver le scenario nominal et le scenario miroir refuse de `preview -> validation -> commit borne`.
12. Brancher un cockpit minimal expert sur les read models existants pour inspection, preuve et replay.
13. Ajouter la matrice de tests minimale et l'evidence pack borne par ticket et par run.
14. Seulement ensuite, poser le registre du projet actif et les identifiants canoniques multi-PC.
15. Introduire le protocole `node manager`, les heartbeats et la projection de flotte.
16. Ajouter leases TTL, claims de taches et reprise sur perte de noeud.
17. Verrouiller la discipline `une tache -> une branche -> un owner -> un worktree`.
18. Brancher `Cockpit Live`, office view minimale et budget de mutation GUI borne.
19. Normaliser reviews, PR et checks externes en evidence exploitable.
20. Generaliser la surface VS Code en Host Bridge multi-host sur les memes read models.
21. Isoler `ECS update` et `Render` dans une boucle deterministe.
22. Brancher pathfinding + collision sur nav-grid unifie.
23. Connecter pipeline assets exportes vers le loader tile/sprites.

## 9-bis. Ordre d'execution du backlog restant

Une fois la fondation runtime et la tranche multi-PC engagees, le reste du backlog doit s'executer par vagues coherentes plutot que ticket par ticket en ordre purement numerique.

### Vague P0 — Contrat canonique, preuve et cockpit minimal

Tickets cibles :

- `GAME-TKT-052`
- `GAME-TKT-053`
- `GAME-TKT-054`

Sortie attendue :

- une spine canonique unique `run/host/proof` sur panier critique borne ;
- un flux critique mono-host prouve de bout en bout ;
- un cockpit minimal expert suffisant pour inspecter, expliquer, verifier et rejouer ce flux.

### Vague R1 — Collaboration visible et travail in-world

Tickets cibles :

- `GAME-TKT-012`
- `GAME-TKT-013`
- `GAME-TKT-014`
- `GAME-TKT-015`
- `GAME-TKT-016`

Sortie attendue :

- un board collaboratif lisible de bout en bout ;
- des handoffs et workflows visibles ;
- une challenge room reliee au backlog et aux preuves ;
- une memoire visible et corrélée aux traces runtime.

### Vague R2 — Espaces Git, plugins et lecture partagée

Tickets cibles :

- `GAME-TKT-017`
- `GAME-TKT-018`
- `GAME-TKT-019`
- `GAME-TKT-020`

Sortie attendue :

- rooms de worktree ;
- power cards gouvernees ;
- retro room exploitable ;
- mode spectateur strictement read-only.

### Vague R3 — Gouvernance transverse et robustesse decisionnelle

Tickets cibles :

- `GAME-TKT-021`
- `GAME-TKT-022`
- `GAME-TKT-023`
- `GAME-TKT-024`
- `GAME-TKT-025`
- `GAME-TKT-026`
- `GAME-TKT-027`
- `GAME-TKT-028`

Sortie attendue :

- drift canari ;
- runbooks et exercices ;
- gates memoire, anti-echo, FinOps et explicabilite ;
- registre licences/provenance ;
- cadre d'experimentation produit.

### Vague R4 — Fermeture CdC et finition produit

Tickets cibles :

- `GAME-TKT-029`
- `GAME-TKT-030`
- `GAME-TKT-031`
- `GAME-TKT-032`
- `GAME-TKT-033`
- `GAME-TKT-034`
- `GAME-TKT-035`
- `GAME-TKT-036`

Sortie attendue :

- fermeture des slots CdC encore manquants ;
- configuration gamifiee complete ;
- audio, XP, onboarding ;
- investigation lab, branch finisher et security audit room production-grade.

### Vague R5 — Enveloppe canonique et host bridge multi-host

Tickets cibles :

- `GAME-TKT-039`
- `GAME-TKT-047`
- `GAME-TKT-048`
- `GAME-TKT-049`
- `GAME-TKT-050`
- `GAME-TKT-051`

Sortie attendue :

- pilote UMF borne ;
- host bindings et capability manifests ;
- policy engine externe fail-closed ;
- reviews externes converties en evidence pack ;
- host bridge generique aligne sur le cockpit.

Regle de sequencing :

- `P0` ouvre tout le reste du backlog ;
- une vague n'ouvre la suivante que lorsque ses contracts, read models et preuves minimales sont poses ;
- `R5` ne doit jamais contourner les invariants definis par `P0` a `R4` ;
- les artefacts operatoires dedies restent prioritaires sur les descriptions generales du backlog.

### Note de synchronisation runtime locale (2026-04-11)

- Les tranches runtime bornees rattachees a `GAME-TKT-030`, `GAME-TKT-035` et `GAME-TKT-039` sont deja couvertes et validees dans `grimoire-kit/apps/grimoire-game`.
- `GAME-TKT-038` est egalement prouve localement; il doit etre traite comme dependance satisfaite dans toute lecture operative du plan.
- Les vagues `R4` et `R5` restent valides comme trajectoire macro, mais tout reliquat futur sur ces tickets doit etre redecoupe explicitement comme extension UI, produit, multi-host, documentation ou distribution, et non comme reouverture du coeur runtime local.

---

## 10. Axes complementaires valides

Les axes suivants sont valides et ajoutes au perimetre d'execution comme backlog transverse.

| ID | Axe supplementaire | Livrable | Critere de validation |
| --- | --- | --- | --- |
| AX-01 | Gouvernance drift prompts/politiques | Baseline de prompts + suite canari + regle de promotion | Un drift de verdict au-dessus du seuil bloque le passage en Done |
| AX-02 | Resilience incident et reprise | Runbooks incident + exercices de reprise + preuves de coherence | Les scenarios de rupture critiques se recuperent sans divergence d'etat |
| AX-03 | Qualite memoire et recall | Regles de fraicheur + score recall + controle obsolescence | Les references obsoletes passent sous le seuil defini |
| AX-04 | Qualite de decision collective | Protocole anti-chambre d'echo + contre-reviews obligatoires | Les revues critiques sont tracees avec objections substantielles |
| AX-05 | FinOps agentique | Telemetrie cout/token/latence + politique budget valeur | Le cout par ticket Done reste stable a complexite equivalente |
| AX-06 | Explicabilite operationnelle | Decision cards sur transitions critiques + preuves de contexte | Chaque decision critique est justifiee et consultable en audit |
| AX-07 | Conformite licences et provenance | Registre provenance assets/plugins + gate de conformite | Aucun asset/plugin sans licence/source verifiee ne passe en merge |
| AX-08 | Cadence experimentation produit | Framework d'experimentation (hypothese, mesure, decision) | Chaque test produit se termine par une decision explicite |
| AX-09 | Gouvernance OWASP Agentic Skills | Matrice risques -> controles -> gates sur surfaces d'execution | Toute activation de skill/plugin/power card est gouvernee et tracable |
| AX-10 | Verification integrity | Chaine de verification AIVS-oriented sur transitions critiques | Un reviewer reconstruit verdict et evidence sans enquete manuelle |
| AX-11 | Canonical message envelope | Pilote UMF borne pour runtime/replay/spectateur/multi-session | Les vues critiques convergent sur une enveloppe commune testee |
| AX-12 | Connectivite hotes externes | Host bindings, policy engine, review ingest et surface multi-host | Aucun hote externe n'entre dans le runtime sans contrat, gate et preuve |

---

## 11. Matrice de verification etendue

En complement de la matrice qualite de section 7, ajouter les verifications suivantes.

| Axe transverse | Verification minimum |
| --- | --- |
| Drift prompts/politiques | Suite canari stable + rapport de variation de verdict |
| Reprise incident | Exercices de rupture critiques et preuve de resync coherent |
| Memoire/recall | Rapport precision recall + taux de references obsoletes |
| Decision collective | Presence de contre-review orthogonale sur livrables critiques |
| FinOps agentique | Rapport cout/token/latence par ticket et par role |
| Explicabilite | Decision cards auditable sur transitions critiques |
| Licences/provenance | Rapport de conformite assets/plugins a chaque passage review |
| Experimentation produit | Hypothese explicite, mesure, decision archivee |
| Hotes externes | Registre des hotes, decisions de policy, reviews importees et etats de degradation |

---

## 12. Sequence recommandee du backlog transverse

### Vague 0 — Cadres externes actionnables

1. AX-09 Gouvernance OWASP Agentic Skills
2. AX-10 Verification integrity
3. AX-11 Canonical message envelope
4. AX-12 Connectivite hotes externes

### Vague A — Stabilite decisionnelle et robustesse

1. AX-01 Gouvernance drift prompts/politiques
2. AX-02 Resilience incident et reprise
3. AX-03 Qualite memoire et recall

### Vague B — Qualite de pilotage et maitrise cout

1. AX-04 Qualite de decision collective
2. AX-05 FinOps agentique
3. AX-06 Explicabilite operationnelle

### Vague C — Conformite et apprentissage produit

1. AX-07 Conformite licences et provenance
2. AX-08 Cadence experimentation produit

---

## 13. Next actions transverses (ordre strict)

1. Definir la baseline des prompts critiques et les scenarios canari de reference.
2. Poser la matrice OWASP Agentic Skills minimale pour les surfaces d'execution du board.
3. Definir la chaine minimale de verification orientee AIVS sur les transitions critiques.
4. Borner le pilote d'enveloppe canonique de message pour runtime, replay et spectateur.
5. Poser la regle de blocage si drift de verdict au-dessus du seuil.
6. Ecrire les runbooks incident (WS down, out-of-order, duplicate, replay partiel).
7. Ajouter un exercice de reprise obligatoire dans le cycle review des lots critiques.
8. Definir les indicateurs recall (precision et obsolescence) et leur gate minimum.
9. Introduire la contre-review orthogonale obligatoire sur livrables critiques.
10. Instrumenter cout/token/latence par ticket et publier un rapport de synthese.
11. Ajouter des decision cards sur les transitions critiques du workflow.
12. Construire le registre de provenance assets/plugins et brancher la gate de conformite.
13. Normaliser un template experimentation (hypothese, mesure, decision) dans les artefacts.
14. Geler le vocabulaire `Host Binding` / `Capability Manifest` / `Invocation Envelope` / `Review Artifact` / `Context Ledger`.
15. Poser la policy fail-closed des hotes externes et les permission prompts associes.
16. Normaliser les reviews et checks externes en evidence rattachee aux tickets et au replay.

---

## 14. Synchronisation PLAN <-> TICKETS (etat courant)

| Slice | Tickets | Portee synchronisee |
| --- | --- | --- |
| Slice 0 | GAME-TKT-001 -> GAME-TKT-004, GAME-TKT-037 | Contrats, eventing, auth, RBAC, garde-fous OWASP Agentic Skills |
| Slice 1 | GAME-TKT-005 -> GAME-TKT-007 | Etat central, ECS deterministe, navigation/collision |
| Slice 2 | GAME-TKT-008 -> GAME-TKT-011, GAME-TKT-038 | Verification gate, assets gouvernes, observabilite agent, chaine de verification |
| Slice 3 | GAME-TKT-012 -> GAME-TKT-016 | Collaboration in-world, challenge, memoire |
| Slice 4 | GAME-TKT-017 -> GAME-TKT-020 | Worktrees, plugins, retro, spectateur/VS Code |
| Slice 5 | GAME-TKT-021 -> GAME-TKT-028 | Gouvernance transverse et quality gates avances |
| Slice 6 | GAME-TKT-029 -> GAME-TKT-036 | Fermeture ecarts CdC et finalisation capacites manquantes |
| Slice 7 | GAME-TKT-039 | Enveloppe canonique de message pour runtime, replay, spectateur et multi-sessions |
| Slice 0 (host bridge) | GAME-TKT-047 -> GAME-TKT-049 | Modele canonique des hotes, contrats d'invocation et policy connecteurs externes |
| Slice 2 (host bridge) | GAME-TKT-050 | Reviews externes normalisees en evidence cockpit |
| Slice 4 (host bridge) | GAME-TKT-051 | Host Bridge generique et surface multi-host |

Regles de synchronisation:

- L'ordre canonique d'execution des GAME-TKT reste la source de verite du backlog.
- Tout ajout/split/merge de ticket impose une mise a jour de cette table et de la matrice de tracabilite.
- Les tickets GAME-TKT-029 a GAME-TKT-036 sont integres au plan comme lot de fermeture de couverture.

Reference de verification operationnelle Slice 6:

- [MATRICE-verification-slice6-web-gaming.md](./MATRICE-verification-slice6-web-gaming.md)

Reference de suite de tests Slice 6:

- [SUITE-tests-slice6-web-gaming.md](./SUITE-tests-slice6-web-gaming.md)

---

## 15. Addendum — Positionnement produit et plan LIVE/multi-sessions

### 15.1 Positionnement produit explicite

- L'interface gamifiee sert la comprehension operationnelle des agents.
- Le succes produit est mesure sur l'intuitivite, la capacite de debug et la rapidite d'ajustement.
- Les elements visuels non actionnables sont consideres comme du bruit.

### 15.2 Constat actuel (technique)

- Le mode LIVE existe mais reste principalement un ancrage timeline + auto-refresh de page.
- La lecture multi-sessions existe via filtres/listes, mais la representation du parallelisme reste partielle.
- Le mapping session des traces et des events doit etre unifie pour une correlation robuste.

### 15.3 Contrat de metadata Qdrant pour observabilite

Champs minimaux requis dans les payloads memoire/evenements indexes:

| Champ | Role |
| --- | --- |
| `ui_goal` | Rappeler l'intention produit (outil visuel agentique) |
| `ui_non_goal` | Poser explicitement le non-but (divertissement ludique) |
| `ui_scope` | Capacites cibles: custom/debug/comprendre/modifier/ajuster |
| `session_id` | Regroupement logique de session |
| `parallel_session_group` | Regroupement d'executions paralleles |
| `view_mode` | `historical` ou `live` selon le contexte |
| `is_live` | Flag bool pour les flux en cours |

### 15.4 Backlog complementaire (brainstorm implemente)

| ID | Theme | Livrable | Critere de validation |
| --- | --- | --- | --- |
| OBS-01 | Live Stream | Canal live incremental (SSE/WS) + fallback replay | Aucun reload global necessaire pour suivre l'activite en cours |
| OBS-02 | Session Axis | Index session/run/worker/lane unifie dans les vues | Une execution parallele est lisible sans changer de tab |
| OBS-03 | Correlation Graph | Liens visuels `correlation_id` inter-sessions | Un handoff inter-session est traçable en un clic |
| OBS-04 | Session Diff | Comparateur de sessions (etat, decisions, erreurs) | Les divergences critiques sont detectees et expliquees |
| OBS-05 | Explain State | Panneau de provenance des transitions d'etat | La cause immediate et la chaine causale sont visibles |
| OBS-06 | Attention UX | Mode focus par role (dev/qa/ops) + reduction du bruit | Le taux de navigation inutile baisse sur les scenarios debug |

### 15.5 Next actions specifiques

1. Unifier le schema session des traces et events (`session_id`, `run_id`, `worker_id`).
2. Brancher le selecteur session global sur la timeline principale et le mode office.
3. Introduire un canal LIVE incremental et garder le replay comme filet de securite.
4. Ajouter une vue matrix multi-sessions orientee parallelisme.
5. Ajouter un panneau "pourquoi cet etat" base sur la provenance des evenements.
