# Rapport 01 - Cartographie du corpus

## Résumé

Le corpus couvre presque toute la chaîne d'un système agentique moderne :

- méthodes de travail et skills ;
- orchestration par graphe, handoff, manager ou workflow visuel ;
- sandbox d'exécution ;
- mémoire et contexte ;
- observabilité et évaluation ;
- sécurité, red-team et garde-fous ;
- surfaces opérateur pour piloter plusieurs agents.

La principale leçon est que les meilleurs projets ne font pas reposer le pilotage sur un "agent maître" omniscient. Ils matérialisent l'état, les permissions, les preuves et les traces en dehors du modèle.

## Carte des 33 dossiers

| Dossier | Famille | Apport pour le pilotage | Réserve principale |
| --- | --- | --- | --- |
| `BMAD-METHOD` | Méthode agentique | Agents spécialisés, workflows structurés, adaptation par domaine. | Très fort côté méthode ; le runtime doit appliquer les contrats. |
| `CodeGraphContext` | Contexte code | Index tree-sitter, graphe de relations, bundles de contexte, MCP. | Dépend de la fraîcheur de l'index et de la qualité des requêtes. |
| `Design/ui` | UI de pilotage | Référence pour construire une bibliothèque de composants propre et extensible. | Pas un framework agentique ; utile surtout pour la surface opérateur. |
| `LLMLingua` | Compression contexte | Réduction de prompt, LongLLMLingua, SecurityLingua. | La compression doit être évaluée sur la perte d'information critique. |
| `LLMSecurityGuide` | Sécurité LLM | Risques agentiques, least agency, sandbox, Zero Trust AI. | Guide large ; les contrôles doivent être implémentés localement. |
| `Octogent` | Agent local autonome | Boucle Think-Act-Observe, pool de workers, persistance SQLite. | Architecture intéressante, mais maturité à vérifier par tests. |
| `OpenHands` | Plateforme agent code | SDK, CLI, GUI locale, cloud, sandbox, event store. | Plateforme large ; coût d'intégration plus élevé qu'un SDK ciblé. |
| `OpenMythos` | Recherche modèle | Recurrent-depth transformer et raisonnement latent. | Pas un système de pilotage ; référence conceptuelle. |
| `agent-framework` | Orchestration enterprise | .NET/Python, graph workflows, middleware, OTel, DevUI, multi-agent. | Ecosystème riche ; nécessite un design de workflow explicite. |
| `agent-sandbox` | Infrastructure sandbox | CRD Kubernetes, pods stateful, template/claim/warmpool, tests de charge. | Nécessite une compétence infra et une politique d'isolation. |
| `ai-agents-for-beginners` | Formation | Leçons multi-agent, production, protocoles, mémoire, observabilité. | Pédagogique ; pas un runtime. |
| `andrej-karpathy-skills` | Discipline coding agent | Penser avant coder, simplicité, changements chirurgicaux, critères de succès. | Dépend de l'obéissance du modèle si non instrumenté. |
| `autogen` | Multi-agent historique | AgentTool, orchestration multi-agent, Core API, Studio. | Le dépôt recommande Microsoft Agent Framework pour les nouveaux projets. |
| `browser-use` | Automation navigateur | Agent navigateur, events, cost tracking, watchdog sécurité, exemples parallèles. | Surface d'attaque élevée ; besoin d'allowlists et d'audit. |
| `claude-skills` | Skills | Activation contextuelle, 66 skills, workflows multi-skill. | Très utile pour expertise ; pas suffisant comme contrôle de run. |
| `crewAI` | Crews et Flows | Crews autonomes, Flows événementiels, manager hiérarchique, telemetry. | Risque de sur-orchestration si les tâches ne sont pas mesurées. |
| `dify` | Plateforme workflow | Builder visuel, RAG, agents, logs, monitoring, déploiement. | Excellent prototypage ; verrouiller les workflows critiques. |
| `gas town/beads` | Graphe de tâches mémoire | Issue graph distribué, Dolt, IDs anti-conflit, claim atomique, multi-repo. | Outil de coordination ; à connecter au runtime d'agent. |
| `gas town/community` | Ecosystème | Communauté et gouvernance autour de Gas Town. | Référence sociale plus que technique. |
| `gas town/docs` | Documentation AI tools | Référence docs et skills d'outillage documentaire. | Starter documentaire ; peu de contrôle agentique. |
| `graphify` | Graphe de connaissance | Extraction AST déterministe, agents parallèles pour docs/images, tags d'incertitude. | Doit être gardé synchronisé avec le code réel. |
| `haystack` | Pipelines IA | Pipelines modulaires, agents, boucles, branches, breakpoints, MCP. | Meilleur pour workflows RAG et pipelines ; design requis pour agents complexes. |
| `kagent` | Kubernetes agents | CRD Agent/ModelConfig/MCP, controller, A2A, OTel, HITL. | Dépend de Kubernetes et d'un modèle d'exploitation clair. |
| `langflow` | Visual builder | Workflows visuels, API/MCP, multi-agent, playground, observabilité. | Comme tout builder visuel, éviter le workflow non versionné. |
| `langfuse` | Observabilité LLM | Tracing, prompt management, evals, datasets, intégrations. | Ne pilote pas seul ; instrumente le pilotage. |
| `langgraph` | Graphe d'état | Agents long-running, durable execution, HITL, mémoire, tracing, déploiement. | Bas niveau ; exige une bonne modélisation d'état. |
| `mempalace` | Mémoire agent | Historique verbatim, recherche sémantique, KG temporel, MCP. | Mémoire puissante mais risque de contamination et de stale context. |
| `openai-agents-python` | SDK agent | Agents, handoffs, tools, guardrails, sessions, tracing, HITL, sandbox. | Excellent socle ; les workflows complexes demandent une couche de plan. |
| `openclaw` | Gateway local-first | Inbox multi-channel, routage multi-agent, isolation workspace/session, sécurité. | Outils host puissants ; isolation non-main obligatoire. |
| `pixel-agents` | Visualisation agent | Visualisation de terminaux Claude Code et subagents par transcript JSONL. | Observation heuristique ; pas un moteur de contrôle. |
| `ruflo` | Orchestration Claude | Rôles, swarms, skills, mémoire, routage, claims de Q-learning/MoE. | Claims ambitieux ; besoin de validation stricte. |
| `shannon` | Pentest agentique | Analyse statique + exploitation dynamique, preuves PoC, worker isolé. | Usage réservé aux environnements autorisés et contrôlés. |
| `superpowers` | Méthodologie skills | Spécification, design, plan, subagent-driven development, déclencheurs skills. | Dépend du host et de la capacité réelle de subagents. |
| `switchboard` | Pilotage opérateur | Kanban VS Code, routage par complexité, batch, rôles, inbox/outbox. | Centralise l'opérateur, mais doit prouver les contrats d'exécution. |
| `vscode-copilot-chat` | Host IDE | Référence host pour agent de code intégré à VS Code. | Gros projet hôte ; peu exploitable comme simple SDK. |

## Familles fonctionnelles

### 1. Méthodes et skills

Les projets `BMAD-METHOD`, `claude-skills`, `superpowers` et `andrej-karpathy-skills` montrent que le pilotage commence souvent par la discipline :

- clarifier l'objectif avant d'agir ;
- expliciter les hypothèses ;
- spécialiser les rôles ;
- contraindre les changements ;
- exiger des critères de réussite.

Ces références sont très utiles pour former les agents, mais elles ne suffisent pas pour un runtime. Une instruction de comportement n'est pas une garantie d'exécution. Elle doit être couplée à un état, des validations et des preuves.

### 2. Graphes, workflows et run state

`langgraph`, `agent-framework`, `haystack`, `dify` et `langflow` convergent vers une idée : le workflow doit être représenté explicitement.

Les bons signaux :

- état durable ;
- branches et conditions ;
- reprise ;
- inspection ;
- checkpoints ;
- breakpoints ;
- visualisation ou API de run ;
- possibilité de servir un workflow comme API ou outil MCP.

Cette famille est la plus solide pour les workflows reproductibles. Elle demande cependant une discipline de modélisation. Un mauvais graphe devient une dette plus lourde qu'un mauvais prompt.

### 3. Handoffs, agents-as-tools et managers

`openai-agents-python`, `agent-framework`, `crewAI`, `autogen` et `kagent` montrent plusieurs façons de déléguer :

- un agent principal appelle un spécialiste comme outil ;
- un handoff transfère le contrôle ;
- un manager coordonne les travailleurs ;
- un agent Kubernetes appelle un sub-agent A2A comme tool ;
- un workflow déclenche plusieurs agents selon l'état.

Le handoff est plus facile à sécuriser qu'un swarm libre, car le contrat d'entrée/sortie peut être borné. Le manager est utile quand il valide les livrables, mais dangereux s'il ne fait que relancer des conversations sans preuve.

### 4. Plateformes et surfaces opérateur

`OpenHands`, `dify`, `langflow`, `switchboard`, `pixel-agents`, `openclaw` et `vscode-copilot-chat` illustrent la nécessité d'une surface de pilotage.

Un opérateur doit voir :

- les tâches en cours ;
- les agents assignés ;
- les outils utilisés ;
- les blocages ;
- les preuves ;
- les décisions humaines attendues ;
- les erreurs et reprises.

Les surfaces visuelles sont utiles quand elles exposent l'état réel. Elles deviennent trompeuses si elles affichent seulement une animation ou un statut deviné.

### 5. Mémoire, contexte et compression

`mempalace`, `CodeGraphContext`, `graphify`, `LLMLingua` et `gas town/beads` traitent le problème le plus sous-estimé : l'agent ne pilote bien que s'il reçoit le bon contexte.

Les meilleures idées :

- graphe de code pour éviter les recherches naïves ;
- bundles de contexte versionnés ;
- mémoire verbatim pour éviter les résumés destructeurs ;
- graphes de tâches avec dépendances ;
- compression de prompt évaluée ;
- tags d'incertitude pour séparer extrait, inféré et ambigu.

La mémoire doit être gouvernée. Sans provenance et invalidation, elle transforme les erreurs anciennes en vérité persistante.

### 6. Sandbox, sécurité et action réelle

`LLMSecurityGuide`, `agent-sandbox`, `OpenHands`, `openclaw`, `browser-use` et `shannon` montrent que l'autonomie agentique est d'abord un problème de sécurité.

Un agent qui peut naviguer, écrire, exécuter ou exploiter doit être limité par :

- sandbox ;
- allowlist ;
- politique de tools ;
- approbation humaine ;
- logs d'audit ;
- validation de sortie ;
- least agency ;
- séparation des sessions et workspaces.

La sécurité n'est pas un module final. Elle fait partie du modèle de pilotage.

### 7. Observabilité et évaluation

`langfuse`, `agent-framework`, `crewAI`, `haystack`, `OpenHands`, `browser-use` et `ai-agents-for-beginners` convergent sur les métriques :

- traces ;
- spans ;
- coûts ;
- erreurs ;
- évaluations offline ;
- évaluations online ;
- feedback humain ;
- datasets ;
- monitoring.

Un système d'agents non instrumenté ne peut pas s'améliorer. Il ne peut que paraître plus intelligent.

## Points forts observés

Les meilleurs éléments du corpus sont :

- `langgraph` pour le contrôle durable et stateful.
- `agent-framework` pour un modèle enterprise multi-langage, middleware, OTel et DevUI.
- `openai-agents-python` pour les primitives pragmatiques : tools, handoffs, guardrails, HITL, sessions, tracing, sandbox.
- `kagent` pour l'exploitation Kubernetes native.
- `langfuse` pour l'observabilité LLM et les évaluations.
- `CodeGraphContext` et `graphify` pour le contexte code structuré.
- `mempalace` et `beads` pour mémoire et coordination persistantes.
- `agent-sandbox`, `OpenHands` et `openclaw` pour l'exécution isolée.
- `BMAD-METHOD`, `superpowers` et `andrej-karpathy-skills` pour les principes de conduite agentique.
- `switchboard` pour le pilotage humain multi-agent depuis l'IDE.

## Défauts structurels récurrents

Le corpus expose aussi des pièges :

- trop de rôles d'agents sans preuve d'efficacité ;
- workflow visuel non versionné ;
- mémoire sans stratégie de retrait ;
- claims de performance sans bench local ;
- permissions de tools trop larges ;
- état de run dispersé entre logs, prompts et fichiers temporaires ;
- parallélisme qui crée des conflits au lieu d'accélérer ;
- UI d'observation confondue avec contrôle réel ;
- absence de contrat de terminaison.

## Lecture pour un projet Grimoire

Pour Grimoire, la cartographie suggère une architecture de pilotage inspirée de plusieurs familles :

- Méthode : `BMAD-METHOD`, `superpowers`, `andrej-karpathy-skills`.
- Orchestration : `langgraph`, `agent-framework`, `openai-agents-python`.
- Mission board : `switchboard`, `beads`, `OpenHands`.
- Contexte : `CodeGraphContext`, `graphify`, `mempalace`, `LLMLingua`.
- Sécurité : `LLMSecurityGuide`, `agent-sandbox`, `openclaw`.
- Observabilité : `langfuse`, OTel, traces de run.

La décision clé est de ne pas copier un framework entier. Il faut extraire les primitives qui durcissent le pilotage : état, preuves, politiques, mémoire, traces et reprise.

