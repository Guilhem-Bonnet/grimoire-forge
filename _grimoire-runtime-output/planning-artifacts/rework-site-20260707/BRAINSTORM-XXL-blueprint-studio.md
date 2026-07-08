# Brainstorm XXL — Blueprint Studio : cases, features, outils

Date : 2026-07-08. Portée : le Studio v2 complet (canvas, palette, équipe,
sous-flows, docs, coût, assist, bibliothèque, simulation, compilation).
Complète le premier brainstorm (BRAINSTORM-blueprint-features.md, verdicts
et priorisation) — celui-ci **élargit** : nouveaux types de cases (nodes),
nouvelles features, nouveaux outils, et la jonction avec les deux chantiers
frais : le **canal beta/Labs** (voie de sortie des nouveautés) et
l'**inventaire des 93 outils dormants** (gisement de capacités prêtes).

Invariant non négociable, répété : le blueprint **se valide, se simule, se
compile — n'exécute jamais**. Chaque nouvelle case doit déclarer *vers quoi
elle compile* ; une case sans sémantique de compilation est un dessin.

---

## 1. Vision — d'un éditeur de flows à un plan de contrôle

Aujourd'hui le Studio est un éditeur : on compose, on compile, on sort des
artefacts. La trajectoire naturelle en fait le **plan de contrôle visuel du
projet agentique** : le blueprint devient la carte vivante où l'on *conçoit*
(composer), *comprend* (le catalogue incarné), *anticipe* (simulation, coût,
risque) et *observe* (replay, drift, signaux) — sans jamais devenir un
moteur. Quatre verbes, une seule surface.

---

## 2. Nouvelles CASES (types de nodes)

Chaque entrée : sémantique → contrats échangés → **compile vers**.

### 2.1 Contrôle de flux (déclaratif, jamais exécutant)

| Case | Sémantique | Compile vers |
|---|---|---|
| **Décision / branche** | Routage déclaratif sur verdict, seuil de coût, ou étiquette (2+ sorties typées) | Règle de policy (GOV-01) dans le mission pack ; les branches deviennent des sections conditionnelles |
| **Boucle bornée** | Itération avec budget max explicite (n tours, plafond tokens) — jamais de boucle libre | Contrainte de workflow + garde de budget ; refus de compiler sans borne |
| **Porte humaine** | Approbation humaine obligatoire avant de continuer | GOV-15 (Human escalation gate) : checkpoint documenté dans le pack |
| **Jonction / fan-in** | Attendre N restitutions avant de poursuivre (quorum simple) | Contrat d'agrégation dans le workflow (handoff-packets multiples) |
| **Consensus critique** | Décision à quorum : 3 votants + avocat du diable | GOV-14 (Decision Council Gate) ; l'outil dormant `adversarial-consensus` fournit la mécanique — candidat beta |

### 2.2 Monde extérieur (entrées/sorties gouvernées)

| Case | Sémantique | Compile vers |
|---|---|---|
| **Déclencheur** (généralisé) | cron, webhook entrant, PR/issue, watch de fichiers | En-tête de workflow (métadonnée de déclenchement) — l'hôte (CI, Copilot) reste l'exécutant |
| **MCP toolbox** | Un serveur MCP comme node : outils exposés = pins de sortie, permissions déclarées | Config MCP du projet + GOV-09 (MCP Trust Gate) obligatoire en amont |
| **Notification sortante** | Publier un résultat (commentaire PR, message) — déclaratif | Étape de workflow avec permission réseau explicite |
| **Ressource / secret** | Déclaration d'environnement requis (API key, service) sans valeur | Section prérequis du pack + check de simulation « ressource présente ? » |

### 2.3 Connaissance & mémoire

| Case | Sémantique | Compile vers |
|---|---|---|
| **Source documentaire** | Corpus indexé (docs externes, repo) avec provenance obligatoire | Config d'indexation ; outils dormants `rag-indexer`/`rag-retriever` — candidat beta ; ancré KNO-06 |
| **Mémoire (lecture)** | Injection de contexte depuis Memory OS (filtre déclaré) | context-pack au démarrage de l'étape ; KNO-02 |
| **Mémoire (écriture)** | Persistance déclarée de décisions/learnings en fin d'étape | memory-record via l'API Memory OS ; jamais d'écriture brute |
| **Signal stigmergique** | Émettre ou écouter un signal du board (NEED, ALERT…) — jonction directe avec la boucle phéromones livrée | Émission déclarée dans le pack ; le hook beta existant fait le reste |

### 2.4 Gouvernance & preuve (compléter la famille)

| Case | Sémantique | Compile vers |
|---|---|---|
| **Garde de budget** | Plafond tokens/coût sur un segment du flow | Enforcement : outil dormant `token-budget` — candidat beta prioritaire |
| **Checkpoint de preuve** | Déclarer l'evidence attendue à ce point (type, format) | QUA-04 : entrée d'evidence-pack exigée par le gate |
| **Sonde d'observation** | Point de télémétrie nommé — apparaît dans replay/observatoire | QUA-08 : convention d'événement dans events.jsonl |
| **Contrat de sortie** | Schéma de sortie attendu (JSON Schema) validé au gate | QUA-14 (Output contract validator) |

### 2.5 Composition

| Case | Sémantique | Compile vers |
|---|---|---|
| **Sous-blueprint référencé** | Pointeur vers un autre `.blueprint.json` du projet (le v1 l'avait, le Studio l'a perdu) | Workflow imbriqué ; le hash de dérive protège la référence |
| **Blueprint du registry** | Référence à un blueprint publié (checksum vérifié) | `ext add-blueprint` + imbrication ; provenance affichée |
| **Variable de blueprint** | Paramètre nommé (modèle par défaut, budget, cible) utilisable dans les fiches | Pack paramétré ; la bibliothèque instancie avec valeurs |

**Règle de curation** : ne pas livrer les 20 cases d'un coup. Chaque case
naît en **canal beta** (palette : section « Labs » avec le badge), et n'entre
dans la palette standard que si utilisée dans de vrais blueprints (le
journal du Studio peut compter les poses par type — même mécanique de
métriques que la stigmergie).

---

## 3. Features de l'éditeur (canvas & UX)

### Navigation & manipulation
- **Palette de commandes** (Ctrl+K) : poser un node, chercher un pattern,
  lancer simulation/compilation — le geste power-user au-dessus de la souris.
- **Minimap** cliquable (les grands flows à 30+ nodes deviennent illisibles).
- **Layout automatique** (elkjs, déjà utilisé par le viewer v1) : bouton
  « réorganiser » global et par sous-flow.
- **Alignement/distribution** de sélection (gauche/centre/espacement égal).
- **Copier/coller inter-blueprints** (presse-papier JSON interne) ; dupliquer
  un sous-flow complet.
- **Recherche sur canvas** : surligner les nodes par nom/famille/contrat.
- **Fit intelligent** : zoom sur sélection / sur sous-flow / sur chemin.

### Le canvas comme document
- **Diff visuel entre versions** : le blueprint est un fichier git — proposer
  la vue « qu'est-ce qui a changé » (nodes ajoutés/retirés/déplacés,
  edges modifiés) entre HEAD et l'état courant, et entre deux commits.
  C'est LA jonction avec « le diff git est la revue » : un reviewer de PR
  devrait pouvoir *voir* le graphe changer, pas lire du JSON.
- **Export images/mermaid** : PNG pour les docs, Mermaid pour les README —
  le blueprint devient citable partout.
- **Mode présentation** : lecture seule plein écran, navigation par étapes
  topologiques — pour expliquer un flow à quelqu'un.
- **Annotations de revue** : commentaires positionnés éphémères (distincts
  des zones), exportables en commentaire de PR.

### Assistance
- **Mode « pourquoi »** : chaque suggestion fantôme et chaque règle R-xx cite
  sa source du catalogue (relation réelle parmi les 141, anti-pattern parmi
  les 52) avec lien vers la fiche — l'assistant devient un professeur, pas
  une opinion (déjà priorisé au brainstorm 1, confirmé ici).
- **Complétion de flow** : « proposer la suite » — depuis le node sélectionné,
  suggérer le sous-graphe canonique du use-case le plus proche (50 réels).
- **Nudges contextuels** : l'outil dormant `nudge-engine` — suggestions au
  bon moment plutôt qu'un panneau statique.

---

## 4. Validation, simulation, anticipation

- **Simulation à données** : injecter un exemple de task-envelope (généré ou
  saisi) et suivre sa transformation contrat par contrat le long du chemin —
  rend la simulation *tangible* au lieu d'un ordre topologique abstrait.
- **Coût réel calibré** : remplacer les hypothèses statiques de bp2-cost par
  la télémétrie du projet (`token-budget` + events.jsonl + ccusage opt-in) ;
  étiqueter honnêtement « hypothèses » tant que non calibré (brainstorm 1).
- **What-if / jumeau numérique** : « si je retire cette porte / change ce
  modèle, qu'est-ce qui change ? » (coût, risque, patterns absents) —
  l'outil dormant `digital-twin` est exactement ça — candidat beta.
- **Verdict de sécurité** : agréger les permissions des extensions et MCP du
  flow → surface d'attaque affichée avant compilation (filesystem, network,
  hooks) ; refus si une case exige une permission non déclarée.
- **Tests de blueprint** : assertions déclaratives versionnées avec le
  blueprint (« tout chemin vers une case déploiement passe par une porte
  QUA », « aucun node EXT sans gate GOV-09 en amont ») — compilées en checks
  CI (`grimoire standard gate check` sait déjà le faire côté standard).
- **Replay temporel** : brancher l'onglet SIMU sur `/api/events` (SSE, déjà
  exposé) pour rejouer une session réelle sur le graphe ; plus loin :
  `time-travel` (checkpoints/bisect) pour comparer deux runs.
- **Drift bidirectionnel** : le hash `compiled` détecte l'artefact modifié à
  la main (livré) ; ajouter l'inverse — blueprint modifié sans recompilation
  = badge « artefacts obsolètes » dans le hub et l'éditeur.

---

## 5. Outils (panneaux & inspecteurs)

- **Inspecteur de chemin** : sélectionner deux nodes → le(s) chemin(s) entre
  eux, contrats traversés, coût cumulé, portes rencontrées.
- **Panneau permissions** : vue agrégée des accès du flow (qui écrit où, qui
  sort sur le réseau) — le pendant Studio du manifeste d'extension.
- **Panneau santé** : linting complet + score de conformité au standard
  (`grimoire standard score` existe) calculé sur le blueprint compilé.
- **Journal du blueprint** : historique des compilations (hash, date, diff
  d'artefacts) — sorti du localStorage, dérivé des sections `compiled`.
- **Gabarits d'équipe** : rôles pré-équipés réutilisables (le testeur haiku,
  l'implémenteur sonnet outillé) — la bibliothèque ne stocke que des flows,
  elle devrait aussi stocker des *agents*.

---

## 6. Import / export / interop

- **Import CrewAI → blueprint** : `crewai_adapter` existe côté runtime ;
  l'inverse du flow actuel — lire un crew YAML/py et proposer le graphe
  équivalent (nodes team + ext). Rend le Studio utile aux équipes qui ont
  déjà des crews.
- **Import LangGraph** : même logique sur les graphes d'état (l'extension
  langgraph est déjà au registry).
- **Rosetta** : l'outil dormant `rosetta` (glossaire cross-domain) pour
  mapper la terminologie CrewAI/LangGraph/AutoGen ↔ patterns du catalogue
  pendant l'import.
- **Profils de compilation** : cible Copilot (`.github/*`) aujourd'hui ;
  demain Claude Code (`.claude/*`), générique (markdown pur). Un sélecteur
  de cible, un seul graphe.
- **Publication registry depuis l'UI** : préparer l'archive + checksum
  (la PR reste manuelle — revue humaine non négociable).

---

## 7. Courbe d'apprentissage

- **Tutoriels par use-case réels** : les 50 use-cases du catalogue comme
  parcours guidés (le squelette seedUseCase existe ; ajouter la narration
  pas-à-pas du tutoriel bp2).
- **Onboarding progressif** : l'outil dormant `crescendo` — déverrouiller
  les familles de patterns au fil de l'usage plutôt que 78 cartes d'un coup ;
  option « tout montrer » pour les experts.
- **Fiches incarnées** : chaque fiche pattern du Studio montre *un exemple
  de blueprint réel* qui l'utilise (les blueprints publiés du registry
  deviennent la matière pédagogique).

---

## 8. Jonction avec le gisement dormant (synthèse)

| Outil dormant | Devient dans le Studio |
|---|---|
| `token-budget` | Case garde de budget + coût calibré |
| `digital-twin` | What-if sur le graphe |
| `adversarial-consensus` | Case consensus critique (GOV-14) |
| `rag-indexer`/`retriever` | Case source documentaire (KNO-06) |
| `project-graph` | Zones réelles du projet (location des signaux et du replay) |
| `time-travel` | Replay comparatif de runs |
| `nudge-engine` | Assistance contextuelle |
| `crescendo` | Onboarding progressif |
| `rosetta` | Mapping terminologique à l'import |
| `failure-museum`/`decision-log` | Alimentation du mode « pourquoi » et du journal |

Chacun suit le pipeline de réveil : SDK → CLI → beta (Labs) → métriques →
palette standard ou déprécation.

---

## 9. Priorisation en trois vagues

### Vague 1 — le socle qui rend tout crédible
1. **Compilation v2 team → vrais artefacts** (chaînon manquant, brainstorm 1).
2. **Curation des pins par pattern dans le catalogue** (supprime l'heuristique).
3. **Case sous-blueprint référencé** (parité v1 perdue) + variable de blueprint.
4. **Diff visuel git** (jonction revue = diff git, valeur immédiate).

### Vague 2 — anticipation (le Studio qui prédit)
5. Coût calibré (`token-budget` réveillé) + garde de budget.
6. Simulation à données + verdict de sécurité (permissions agrégées).
7. Assist « pourquoi » branché sur relations + anti-patterns réels.
8. Replay SSE sur le graphe.

### Vague 3 — l'écosystème (le Studio qui rayonne)
9. Cases contrôle de flux (décision, boucle bornée, porte humaine, consensus).
10. Cases connaissance (RAG, mémoire) + case stigmergie.
11. Import CrewAI/LangGraph + profils de compilation multi-cibles.
12. Onboarding crescendo + tutoriels use-cases + export mermaid/PNG.

Chaque item de vague 2-3 naît **en beta** (Labs), instrumenté, et se promeut
sur métriques — le pipeline construit pour la stigmergie devient la norme
de tout le Studio.
