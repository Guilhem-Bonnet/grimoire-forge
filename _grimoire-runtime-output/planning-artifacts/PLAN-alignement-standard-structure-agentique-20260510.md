# Plan d'alignement avec le standard de structure agentique

## Statut

| Champ | Valeur |
| --- | --- |
| Projet cible | Grimoire Forge |
| Référentiel normatif | processus-developpement-agentique |
| Nature | plan de gaps et d'amélioration documentaire |
| Source de comparaison | standard documentaire + runtime Grimoire Forge |
| Destination | backlog d'évolution Grimoire et amélioration du standard |

## Objectif

Ce plan relie Grimoire Forge au standard de structure agentique. Il sert à identifier :

- les éléments que Grimoire Forge implémente déjà ;
- les gaps que Grimoire Forge doit combler pour être explicitement conforme ;
- les manques du standard révélés par l'existence d'un runtime agentique réel ;
- les références normatives à utiliser pour chaque amélioration.

Le standard reste indépendant de Grimoire Forge. Grimoire Forge sert ici de cas d'implémentation vivant pour éprouver, enrichir et prioriser le référentiel.

## Références normatives

| Référence | Usage pour Grimoire Forge |
| --- | --- |
| [Standard de structure agentique](https://github.com/Guilhem-Bonnet/processus-developpement-agentique) | Référentiel source. |
| [Terminologie agentique](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/terminologie-agentique.md) | Aligner vocabulaire, rôles et langage normatif. |
| [Modèle de référence](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/modele-reference-structure-agentique.md) | Vérifier plans, composants obligatoires et interfaces minimales. |
| [Exigences normatives](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/exigences-normatives-structure-agentique.md) | Construire la matrice de conformité Grimoire. |
| [Patterns de structure agentique](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/patterns-structure-agentique.md) | Mapper les patterns déjà présents et ceux à formaliser. |
| [Profils de capacités](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/profils-capacites-agentiques.md) | Normaliser capacités d'orchestrateur, subagent, outil, mémoire et validation. |
| [Niveaux de conformité](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/niveaux-conformite-agentique.md) | Déclarer le niveau atteint par domaine. |
| [Routage LLM et rétention](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/routage-llm-retention-connaissances.md) | Renforcer routing, fallback, TTL, désindexation et purge. |
| [Orchestration du contexte](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/orchestration-contexte-agentique.md) | Aligner context router, budgets, task envelope et handoff. |
| [Contrats opérationnels](https://github.com/Guilhem-Bonnet/processus-developpement-agentique/blob/main/docs/contrats-operationnels-agentiques.md) | Définir les interfaces inter-agents et outils. |

## Constats principaux

| Domaine | État Grimoire Forge | Lecture standard |
| --- | --- | --- |
| Orchestration | Très avancé avec SOG, grimoire-master, dispatch, agents invisibles. | Conforme au modèle entreprise-agent. |
| Subagents | Agents nombreux, manifestés et spécialisés. | Forte correspondance avec le pattern orchestrateur/subagents. |
| Routage LLM | `model-routing.yaml` existe avec profils et overrides. | Très proche du routage LLM par tâche. |
| MCP | `.mcp.json` et `mcp-policy.yaml` existent. | Bon socle, registre outil à compléter. |
| Hooks | Registre de hooks enforced/canary/shadow. | Plus avancé que le standard conceptuel. |
| Policies | `PolicyEngine` avec allow/warn/block. | Aligne le policy engine normatif. |
| Missions | MissionLedger append-only, états et incidents. | Très bon socle pour mission, Kanban et traçabilité. |
| Preuves | EvidencePack et VerificationVerdict existent. | Plus implémenté que le claim ledger, mais moins lisible comme contrat documentaire. |
| Mémoire | MemoryManager, backends vectoriels, sidecar, Neo4j. | Plus riche techniquement que le standard. |
| Rétention | Présente par endroits, mais dispersée. | Le standard demande une politique centrale. |
| Conformité | Beaucoup de contrôles réels, peu de déclaration normative. | Il manque un mapping vers les exigences AG-*. |
| Acceptation client | Preuves et releases existent, sign-off moins explicite. | Le standard demande un dossier d'acceptation clair. |

## Gaps Grimoire Forge à atteindre

### Gap GF-001 : Registre outil complet

| Élément | Détail |
| --- | --- |
| Problème | Grimoire expose beaucoup d'outils, mais le registre outil canonique reste incomplet. |
| Cible | Compléter `tool-manifest.csv` ou créer un manifeste équivalent avec outil, propriétaire, risque, scopes, preuves et rollback. |
| Référence standard | Profils de capacités, exigences AG-TOL, contrat MCP. |
| Sortie attendue | Registre outil exploitable par SOG, hooks et policy engine. |

### Gap GF-002 : Task envelope canonique

| Élément | Détail |
| --- | --- |
| Problème | Grimoire possède Dispatch Card, mission tasks et workflows, mais pas un contrat unique nommé task envelope. |
| Cible | Définir un schéma `task-envelope` aligné avec mission, rôle, contexte minimal, outils, contraintes, preuves et sortie attendue. |
| Référence standard | Orchestration du contexte, contrats opérationnels, modèle de référence. |
| Sortie attendue | Schéma réutilisable par SOG, workflows et subagents. |

### Gap GF-003 : Handoff packet unifié

| Élément | Détail |
| --- | --- |
| Problème | Les handoffs existent dans agents, pipelines et skills, mais le format reste dispersé. |
| Cible | Formaliser résultat, preuves, hypothèses, risques, changements, mémoire candidate et prochain trigger. |
| Référence standard | Contrats opérationnels, patterns de structure agentique. |
| Sortie attendue | Format commun pour handoff entre subagents, workflows et MissionLedger. |

### Gap GF-004 : Claim ledger lisible

| Élément | Détail |
| --- | --- |
| Problème | EvidencePack prouve des tâches, mais le lien affirmation importante -> preuve n'est pas un objet explicite. |
| Cible | Créer une projection ou un contrat claim ledger au-dessus des evidence packs. |
| Référence standard | Contrats opérationnels, garde-fous, exigences AG-QUA. |
| Sortie attendue | Traçabilité des affirmations critiques vers sources, outils, hypothèses ou preuves. |

### Gap GF-005 : Politique centrale de rétention connaissance

| Élément | Détail |
| --- | --- |
| Problème | La rétention existe pour certains artefacts, mais elle n'est pas centralisée pour mémoire, handoffs, rapports, embeddings et sorties runtime. |
| Cible | Définir une politique `durable / archive / TTL / désindexation / purge` applicable aux surfaces Grimoire. |
| Référence standard | Routage LLM et rétention, gouvernance modèles/connaissances. |
| Sortie attendue | Registre de rétention avec statuts `active`, `archived`, `superseded`, `obsolete`, `sensitive`. |

### Gap GF-006 : Matrice de conformité normative

| Élément | Détail |
| --- | --- |
| Problème | Grimoire satisfait déjà beaucoup d'exigences, mais ne déclare pas sa conformité au standard. |
| Cible | Créer une matrice AG-MIS, AG-ORC, AG-CTX, AG-LLM, AG-TOL, AG-QUA, AG-INC, AG-RET. |
| Référence standard | Exigences normatives, niveaux de conformité. |
| Sortie attendue | Document de conformité montrant exigence, preuve Grimoire, statut et gap. |

### Gap GF-007 : Dossier d'acceptation client

| Élément | Détail |
| --- | --- |
| Problème | Grimoire possède preuves, reports et releases, mais pas un contrat de sign-off client généralisé. |
| Cible | Définir un dossier d'acceptation pour livrable agentique : preuves, limites, risques résiduels, décisions et acceptation. |
| Référence standard | Contrats opérationnels, dossier d'acceptation, exigences AG-QUA. |
| Sortie attendue | Template exploitable par livraison, PR, release ou mission close. |

### Gap GF-008 : Source registry

| Élément | Détail |
| --- | --- |
| Problème | Les sources sont nombreuses : docs, runtime, manifests, memory, output artifacts, site. La source active n'est pas toujours évidente. |
| Cible | Déclarer pour chaque domaine la source de vérité active, l'archive, le statut et la règle de remplacement. |
| Référence standard | Routage LLM et rétention, orchestration du contexte. |
| Sortie attendue | Registre des sources actives pour réduire contradictions et mémoire obsolète. |

## Améliorations à reporter dans le standard

### Standard Gap STD-001 : Profil d'implémentation runtime

Grimoire montre qu'un standard abstrait doit distinguer documentation de référence et runtime exécutable. Ajouter au standard un profil d'implémentation : `documentaire`, `runtime local`, `runtime IDE`, `runtime distribué`, `runtime gouverné`.

### Standard Gap STD-002 : Schémas machine-readable

Le standard décrit les contrats, mais Grimoire prouve l'intérêt de schémas exécutables. Ajouter des schémas pour task envelope, handoff packet, claim ledger, tool registry, source registry et conformité.

### Standard Gap STD-003 : Modes de hook

Grimoire utilise `shadow`, `canary` et `enforced`. Le standard devrait intégrer ces modes comme pattern de promotion de garde-fous.

### Standard Gap STD-004 : Evidence pack comme complément du claim ledger

Le standard insiste sur le claim ledger. Grimoire montre qu'un `EvidencePack` avec digest, couverture et verdict est une primitive plus robuste. Ajouter l'articulation `claim -> evidence item -> evidence pack -> verdict`.

### Standard Gap STD-005 : Mémoire graphe + vectoriel

Le standard parle vector DB et Redis, mais Grimoire montre une architecture mémoire plus complète : vectoriel, graphe, sidecar temporel, journal agent. Ajouter ce pattern comme extension mature.

### Standard Gap STD-006 : Runtime output comme surface gouvernée

Grimoire produit beaucoup d'artefacts runtime. Le standard devrait préciser comment gouverner les surfaces de sortie : planning artifacts, implementation artifacts, test artifacts, traces, telemetry et visual evidence.

## Backlog recommandé

| ID | Sujet | Livrable | Référence standard |
| --- | --- | --- | --- |
| GFB-001 | Tool registry | manifeste outils complet | AG-TOL, profils capacités |
| GFB-002 | Task envelope | schéma canonique + exemple | orchestration contexte |
| GFB-003 | Handoff packet | schéma canonique + intégration workflows | contrats opérationnels |
| GFB-004 | Claim ledger | projection ou template relié aux EvidencePack | AG-QUA, contrats |
| GFB-005 | Rétention connaissance | politique centrale + registre | routage/rétention |
| GFB-006 | Source registry | registre sources actives et superseded | orchestration contexte |
| GFB-007 | Conformité | matrice exigences AG-* -> preuves Grimoire | niveaux conformité |
| GFB-008 | Acceptation | template dossier d'acceptation | contrats opérationnels |
| GFB-009 | Standard feedback | issues ou plan d'amélioration du standard | gaps STD-* |

## Ordre de consolidation

1. Formaliser les contrats qui connectent déjà l'existant : task envelope, handoff packet, tool registry.
2. Ajouter la conformité : matrice AG-* avec preuve et statut.
3. Centraliser la rétention et les sources actives.
4. Relier EvidencePack et claim ledger.
5. Alimenter le standard avec les patterns éprouvés par Grimoire : hook modes, evidence packs, mémoire graphe/vectorielle, runtime output gouverné.

## Définition de Done

Le plan est clos quand :

- chaque gap Grimoire possède un artefact cible nommé ;
- chaque artefact cible référence au moins une exigence ou page du standard ;
- les gaps standard ont une proposition d'évolution ;
- la conformité Grimoire peut être relue sans connaître toute l'implémentation ;
- les nouvelles règles ne dupliquent pas des mécanismes déjà existants dans le runtime.

## Note d'utilisation

Ce document n'est pas un remplacement du standard. Il est le pont entre le standard abstrait et Grimoire Forge comme implémentation concrète. Toute évolution durable doit rester synchronisée dans les deux sens : le standard clarifie les exigences, Grimoire prouve les patterns par l'exécution.
