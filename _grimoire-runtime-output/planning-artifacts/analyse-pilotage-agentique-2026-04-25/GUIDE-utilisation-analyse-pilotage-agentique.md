---
description: Guide pratique pour lire, exploiter et transformer le package d'analyse en decisions de conception.
date: 2026-04-25
---

# Guide d'utilisation de l'analyse pilotage agentique

## Pour qui

Ce guide s'adresse a trois publics.

| Profil | Objectif |
| --- | --- |
| Architecte | Choisir une architecture de pilotage agentique robuste. |
| Product owner | Comprendre ce qu'il faut exiger d'un produit agentique. |
| Enseignant ou mentor | Expliquer les types de pilotage, leurs forces et leurs risques. |

## Comment lire le package

Le package contient sept fichiers.

| Fichier | Usage |
| --- | --- |
| `README.md` | Lire la synthese et choisir un parcours de lecture. |
| `01-cartographie-modeles-pilotage.md` | Comprendre les familles de pilotage et leurs compromis. |
| `02-performance-efficacite-observabilite.md` | Construire une strategie de mesure et d'optimisation. |
| `03-defauts-risques-garde-fous.md` | Identifier risques, anti-patterns et protections. |
| `04-guide-enseignement-projet-pilotage-agentique.md` | Enseigner ou transmettre la methode de construction. |
| `DOC-TECHNIQUE-analyse-pilotage-agentique.md` | Verifier la methode, le corpus et les hypotheses. |
| `GUIDE-utilisation-analyse-pilotage-agentique.md` | Utiliser ce package pour produire des decisions. |

## Parcours recommandes

### Parcours decision rapide

1. Lire `README.md`.
2. Lire la matrice de choix dans `01-cartographie-modeles-pilotage.md`.
3. Lire la grille Go/No-Go dans `03-defauts-risques-garde-fous.md`.
4. Selectionner un niveau de maturite dans `04-guide-enseignement-projet-pilotage-agentique.md`.

### Parcours architecture

1. Lire `DOC-TECHNIQUE-analyse-pilotage-agentique.md`.
2. Lire `01-cartographie-modeles-pilotage.md` en entier.
3. Lire `02-performance-efficacite-observabilite.md`.
4. Lire `03-defauts-risques-garde-fous.md`.
5. Transformer les invariants en ADR.

### Parcours enseignement

1. Lire `04-guide-enseignement-projet-pilotage-agentique.md`.
2. Utiliser les exercices comme plan de formation.
3. Utiliser `01-cartographie-modeles-pilotage.md` pour illustrer les types de pilotage.
4. Utiliser `03-defauts-risques-garde-fous.md` pour enseigner les echecs.

### Parcours audit

1. Lire les axes d'evaluation dans `DOC-TECHNIQUE-analyse-pilotage-agentique.md`.
2. Evaluer le systeme cible avec la scorecard de `02-performance-efficacite-observabilite.md`.
3. Appliquer la grille Go/No-Go de `03-defauts-risques-garde-fous.md`.
4. Produire une liste de gaps classes par risque.

## Transformer le package en decisions

### Decision 1 : niveau de maturite vise

Utiliser la grille de maturite du guide d'enseignement.

| Contexte | Niveau recommande |
| --- | --- |
| Prototype personnel | Niveau 1 ou 2. |
| Assistant de developpement interne | Niveau 3. |
| Produit agentique avec utilisateurs | Niveau 4. |
| Environnement sensible ou multi-tenant | Niveau 5. |

### Decision 2 : source de verite

Choisir explicitement le Mission Ledger comme source de verite. Le cockpit, les transcripts et les fichiers Markdown peuvent aider, mais ils ne doivent pas posseder seuls l'etat.

### Decision 3 : runtime principal

Choisir selon le besoin dominant.

| Besoin dominant | Famille pertinente |
| --- | --- |
| Workflows longs et reprise | Graphe d'etat. |
| Collaboration visuelle | Plateforme visuelle + ledger. |
| Agents locaux dans IDE | IDE-native orchestration. |
| Multi-tenant et isolation | Control plane infra. |
| RAG et pipelines | Workflow/pipeline + memoire. |

### Decision 4 : politique de securite

Definir les actions qui demandent confirmation, sandbox ou refus.

Actions a traiter comme sensibles : shell mutating, suppression, reseau externe, navigation authentifiee, ecriture de secrets, execution de code non fiable, modification de policies, modification de memoire durable.

### Decision 5 : mesure de performance

Mesurer le cout par tache verifiee. Eviter les mesures isolees qui ne disent rien sur la qualite finale.

## Checklists pratiques

### Checklist architecture

- Le ledger existe et contient missions, taches, etats, preuves et blocages.
- Les workflows sont versionnes.
- Les agents ont des scopes explicites.
- Les outils ont schemas, policies et logs.
- Les sorties critiques passent par validation.
- Les traces relient intention, action, resultat et preuve.
- La memoire a provenance, scope et invalidation.
- L'UI lit le ledger et n'ecrit que via commandes controlees.

### Checklist securite

- Prompt injection testee sur contenu lu.
- Tool misuse teste sur outils puissants.
- Memory poisoning teste sur memoire persistante.
- Permission escalation bloquee par runtime.
- Sandbox active pour execution non fiable.
- Budget et retries bornes.
- Secrets exclus des prompts et traces.
- Actions irreversibles confirmees.

### Checklist performance

- Les classes de taches sont separees.
- Le succes exige une preuve.
- Les couts sont associes aux missions.
- Les retries ont une limite.
- Le parallelisme est reserve aux taches independantes.
- Le contexte est recupere par besoin, pas injecte en masse.
- La compression est testee contre perte de contraintes.

### Checklist enseignement

- Commencer par un agent outille simple.
- Introduire ensuite workflow et ledger.
- Montrer un echec volontaire et sa trace.
- Ajouter memoire avec provenance.
- Ajouter policy et sandbox.
- Ajouter multi-agent seulement apres stabilisation du ledger.
- Terminer par cockpit et evals.

## Livrables derives possibles

Le package peut etre transforme en :

- ADR d'architecture pour un control plane agentique ;
- cahier des charges produit ;
- grille d'audit interne ;
- support de formation ;
- backlog d'implementation ;
- benchmark comparatif ;
- politique de securite agentique ;
- modele de donnees du Mission Ledger.

## Questions de cadrage a poser avant implementation

1. Quelles actions l'agent a-t-il le droit de faire sans confirmation ?
2. Quelle est la source de verite des taches et etats ?
3. Quelles preuves sont requises pour declarer termine ?
4. Quelle memoire est persistante et comment est-elle invalidee ?
5. Quels outils peuvent avoir des effets de bord ?
6. Comment detecte-t-on un run bloque ?
7. Quels incidents doivent escalader vers un humain ?
8. Quel est le budget par mission et qui peut l'augmenter ?
9. Quelles donnees ne doivent jamais entrer dans un prompt ?
10. Comment rejoue-t-on ou audite-t-on une decision ?

## Mode d'emploi pour un nouveau projet

1. Copier la table des composants du `DOC-TECHNIQUE` dans un document d'architecture.
2. Choisir le niveau de maturite du `04-guide-enseignement`.
3. Selectionner les familles de pilotage pertinentes dans `01-cartographie`.
4. Ajouter les indicateurs de `02-performance` au plan d'observabilite.
5. Transformer la grille Go/No-Go de `03-defauts` en quality gate.
6. Ecrire les premiers schemas `mission`, `task`, `evidence` et `policy_decision`.
7. Construire une implementation minimale autour du ledger avant l'UI.

## Mode d'emploi pour auditer un projet existant

1. Identifier la source de verite actuelle.
2. Reconstituer le chemin intention -> plan -> tool -> preuve -> validation.
3. Lister les outils avec effets de bord.
4. Verifier si les policies sont appliquees par runtime ou seulement par prompt.
5. Examiner la memoire : provenance, obsolescence, scope, effacement.
6. Chercher les cas de silent stall.
7. Evaluer le cout par tache verifiee.
8. Classer les gaps en P0, P1, P2 selon impact et exploitabilite.

## Criteres de bonne exploitation

Le package a ete correctement exploite si une equipe peut produire :

- une decision claire sur le type de pilotage retenu ;
- un schema de ledger ;
- une liste d'outils et policies ;
- une strategie d'observabilite ;
- une strategie de memoire ;
- une grille de securite ;
- une definition de termine avec preuves.

## Conclusion

Utiliser ce package revient a passer d'une question vague, "comment faire des agents", a une question exploitable : "quel systeme de controle permet a ces agents d'agir avec etat, limites, preuve et reprise".
