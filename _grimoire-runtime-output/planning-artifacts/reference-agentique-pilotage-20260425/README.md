# Analyse du corpus Référence-Agentique

Date de production : 2026-04-25

Base analysée : `/mnt/Travail/Projets/Dev/Référence-Agentique/`

Ce paquet rassemble une analyse pédagogique et architecturale de 33 dossiers de référence autour du pilotage d'agents. Le but n'est pas de désigner un seul framework gagnant, mais d'extraire les modèles de pilotage réutilisables, leurs coûts opérationnels, leurs risques, et les conditions minimales pour construire un vrai projet agentique pilotable.

## Livrables

| Fichier | Rôle |
| --- | --- |
| `DOC-TECHNIQUE-reference-agentique-pilotage.md` | Méthode d'analyse, modèle de preuves, limites et carte technique du corpus. |
| `GUIDE-utilisation-reference-agentique-pilotage.md` | Mode d'emploi pour exploiter les rapports et prendre une décision d'architecture. |
| `RAPPORT-01-cartographie-corpus.md` | Cartographie des 33 dossiers, familles fonctionnelles et apports principaux. |
| `RAPPORT-02-modeles-pilotage-agentique.md` | Typologie complète des modèles de pilotage : graphe, handoff, crew, skills, sandbox, Kanban, observabilité, mémoire. |
| `RAPPORT-03-performance-efficacite-observabilite.md` | Analyse performance, efficacité, mesure, traces, coûts, contexte, parallélisme et évaluation. |
| `RAPPORT-04-risques-defauts-antipatterns.md` | Défauts récurrents, risques de sécurité, anti-patterns et contre-mesures. |
| `RAPPORT-05-guide-enseignement-projet-pilotage.md` | Document d'enseignement : comment concevoir un projet réel de pilotage agentique. |
| `ANNEXE-sources-et-preuves.md` | Références de preuves locales avec chemins et lignes. |

## Conclusion courte

Un vrai système de pilotage d'agents ne doit pas être construit comme une grande conversation autonome. Les meilleurs signaux du corpus convergent vers une architecture en couches :

1. Une surface orchestratrice unique qui reçoit l'intention utilisateur.
2. Un plan ou graphe d'exécution durable, inspectable et reprenable.
3. Des agents spécialisés traités comme des travailleurs ou des outils, avec contrats d'entrée/sortie.
4. Une passerelle d'outils qui applique permissions, sandbox, quotas et validations.
5. Une mémoire et un contexte avec provenance, fraîcheur et invalidation.
6. Une observabilité complète : traces, coûts, erreurs, évaluations, décisions humaines.
7. Des preuves de terminaison : artefacts, tests, logs, diff, rapport, ou démonstration contrôlée.

La règle de conception la plus importante est simple : le contrôle doit être déterministe autant que possible, et l'intelligence générative doit être utilisée pour les tâches où elle apporte réellement de la valeur.

## Lecture recommandée

Pour une décision rapide, lire d'abord :

1. `RAPPORT-02-modeles-pilotage-agentique.md`
2. `RAPPORT-05-guide-enseignement-projet-pilotage.md`
3. `RAPPORT-04-risques-defauts-antipatterns.md`

Pour construire un socle Grimoire ou un OS agentique, lire ensuite :

1. `RAPPORT-03-performance-efficacite-observabilite.md`
2. `RAPPORT-01-cartographie-corpus.md`
3. `ANNEXE-sources-et-preuves.md`

## Position d'architecture

Le corpus montre quatre niveaux de maturité :

| Niveau | Description | Risque principal |
| --- | --- | --- |
| Prompt et skills | Instructions, méthodes, agents déclaratifs, discipline de travail. | Aucun état fiable si rien ne l'exécute. |
| Workflow contrôlé | Graphe, pipeline, handoff, manager, run state, reprise. | Complexité de conception et dette de workflow. |
| Plateforme opérable | UI, queue, sandbox, RBAC, traces, déploiement, intégrations. | Coût d'exploitation et surface d'attaque. |
| Système apprenant | Mémoire, graphes, routage, évaluation, optimisation, feedback. | Mémoire toxique, métriques faibles, sur-automatisation. |

Le bon projet commence rarement au niveau le plus haut. Il commence par le plus petit contrôle fiable, puis ajoute spécialisation, parallélisme, mémoire et autonomie seulement quand les preuves de qualité existent.

