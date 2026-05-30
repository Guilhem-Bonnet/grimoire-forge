---
description: Index des rapports d'analyse sur les architectures de pilotage d'agents du corpus Reference-Agentique.
date: 2026-04-25
---

# Analyse comparative du pilotage agentique

Ce package consolide l'analyse du corpus local `Reference-Agentique`. Il compare les choix de pilotage, les modeles d'orchestration, la performance, l'efficacite, les defauts, les avantages et les elements reutilisables pour construire un vrai projet de pilotage agentique.

Le resultat n'est pas un classement de popularite. C'est un document d'enseignement et de decision : quoi reprendre, quoi eviter, comment assembler les briques, et quels invariants rendent un systeme agentique operable.

## Livrables

| Fichier | Role |
| --- | --- |
| `01-cartographie-modeles-pilotage.md` | Taxonomie complete des types de pilotage observes, avec forces, limites et cas d'usage. |
| `02-performance-efficacite-observabilite.md` | Analyse performance, cout, efficacite, memoire, contexte, evaluation et observabilite. |
| `03-defauts-risques-garde-fous.md` | Analyse des defauts, risques, vulnerabilites, anti-patterns et garde-fous obligatoires. |
| `04-guide-enseignement-projet-pilotage-agentique.md` | Cours structure pour apprendre a concevoir un vrai control plane agentique. |
| `DOC-TECHNIQUE-analyse-pilotage-agentique.md` | Methodologie, corpus, commandes de releve, hypotheses et limites. |
| `GUIDE-utilisation-analyse-pilotage-agentique.md` | Mode d'emploi pour exploiter les rapports et transformer l'analyse en decisions. |

## Corpus couvert

Le corpus analyse est situe dans `/mnt/Travail/Projets/Dev/Reference-Agentique/`. Les depots Git et dossiers imbriques suivants ont ete pris en compte.

| Famille | Depots representatifs | Signal principal |
| --- | --- | --- |
| Methodes et workflows de delivery | `BMAD-METHOD`, `superpowers`, `gas town/gastown`, `gas town/gascity`, `gas town/beads` | Roles, skills, handoffs, issue ledger, validation, reprise de contexte. |
| Graphes et orchestration stateful | `langgraph`, `agent-framework`, `openai-agents-python`, `crewAI`, `haystack` | Graphes, flows, checkpointing, handoffs, outils, human-in-the-loop. |
| Produits agents complets | `OpenHands`, `openclaw`, `Octogent`, `browser-use`, `shannon` | Runtimes autonomes, interfaces operateur, browser/computer use, sandbox, securite. |
| Plateformes visuelles | `dify`, `langflow`, `switchboard`, `pixel-agents`, `Design/ui` | Canvas, kanban, cockpit, API/MCP, visualisation d'etat. |
| Infra et controle declaratif | `kagent`, `agent-sandbox`, `gas town/gascity-otel`, `gas town/tmux-adapter` | Kubernetes CRD, sandbox lifecycle, WebSocket adapter, OpenTelemetry. |
| Memoire, contexte et graphes | `CodeGraphContext`, `graphify`, `mempalace`, `LLMLingua` | Code graph, graph context, memoire locale, prompt compression. |
| Observabilite et securite | `langfuse`, `LLMSecurityGuide`, `shannon`, `vscode-copilot-chat` | Traces, evals, guardrails, tool confirmations, OWASP agentique. |
| Skills et personnalisation | `claude-skills`, `andrej-karpathy-skills`, `BMAD-METHOD`, `superpowers` | Skills portables, guidelines, declencheurs, conventions de comportement. |

## Synthese courte

Un projet serieux de pilotage agentique ne doit pas choisir entre autonomie et controle. Il doit composer les deux.

Les depots les plus robustes separent clairement quatre surfaces : l'intention, l'etat, l'action et la preuve. Les systemes fragiles les melangent dans un prompt, une session de chat ou une interface visuelle sans ledger verifiable.

Les meilleurs patterns observes sont les suivants.

- Un moteur d'etat explicite, inspire de `langgraph`, `agent-framework` et `openai-agents-python`.
- Une discipline de workflow, inspiree de `BMAD-METHOD`, `superpowers` et `gas town`.
- Une memoire avec provenance, inspiree de `mempalace`, `CodeGraphContext`, `graphify` et `beads`.
- Une observabilite de run, inspiree de `langfuse`, `vscode-copilot-chat`, `kagent` et `gascity-otel`.
- Une isolation d'execution, inspiree de `agent-sandbox`, `openai-agents-python` sandbox agents, `openclaw` et `shannon`.
- Une surface operateur qui reste une projection du ledger, inspiree de `switchboard`, `pixel-agents` et des interfaces VS Code.

## Conclusion de decision

La meilleure architecture n'est pas un swarm autonome massif. C'est un control plane agentique : un systeme ou les agents ne sont que des executants specialises, pilotes par un ledger, des politiques, des etats persistants, des budgets, des validations et des preuves.

Le modele recommande pour un projet comme Grimoire est hybride.

- Workflow explicite pour la discipline de projet.
- Graphe stateful pour la robustesse runtime.
- Skills pour la portabilite des comportements.
- Memoire structuree pour la continuite.
- Sandbox et approvals pour les actions a risque.
- Observabilite et evals pour l'amelioration continue.
- UI operateur comme cockpit, jamais comme source de verite.

## Lecture recommandee

1. Lire `01-cartographie-modeles-pilotage.md` pour comprendre les familles de pilotage.
2. Lire `02-performance-efficacite-observabilite.md` pour choisir les metriques et optimiser cout/qualite.
3. Lire `03-defauts-risques-garde-fous.md` avant toute implementation durable.
4. Utiliser `04-guide-enseignement-projet-pilotage-agentique.md` comme support de formation et de conception.
5. Consulter `DOC-TECHNIQUE-analyse-pilotage-agentique.md` pour reproduire ou auditer l'analyse.
6. Suivre `GUIDE-utilisation-analyse-pilotage-agentique.md` pour transformer les rapports en decisions projet.
