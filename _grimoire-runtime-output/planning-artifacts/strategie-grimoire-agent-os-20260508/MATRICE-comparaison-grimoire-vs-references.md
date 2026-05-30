# Matrice - Grimoire versus références IA

## Synthèse

Grimoire a progressé depuis les anciens rapports. Les tranches `GrimoireEvent`, Mission Board, observability, Office timeline et stigmergy ne sont plus seulement des plans. Elles ont des modules et des tests ciblés.

L'écart majeur se déplace donc :

- avant : "les surfaces sont-elles branchées ?"
- maintenant : "le runtime est-il durable, interopérable, sécurisé et productisable ?"

## Position actuelle de Grimoire

| Axe | Statut actuel | Lecture |
| --- | --- | --- |
| IDE-native | Fort | Grimoire est meilleur que la plupart des frameworks purs sur l'intégration aux agents IDE, hooks, skills et surfaces opérateur. |
| Runtime visible | Fort mais fragmenté | `grimoire-game` donne une vraie surface, mais elle doit rester projection du kernel. |
| Event ledger | Partiel avancé | `GrimoireEvent` existe, mais il est encore hook-centric et doit évoluer vers un run ledger complet. |
| Durable execution | Faible à partiel | Pas encore d'équivalent LangGraph : checkpoints, resume, side effects idempotents et thread/run state. |
| MCP | Bon socle | Serveur Grimoire et policy existent ; `ollama` montre que la fail-closed policy doit devenir opérationnelle. |
| A2A | Manquant | Aucun AgentCard public ou registry A2A-ready n'est visible comme contrat produit. |
| Observabilité | Partielle avancée | Tests et vues existent ; OTel GenAI, span model et export eval restent à faire. |
| Mémoire | Partielle | Qdrant est prêt, mais 0 entrée observée ; code graph et task memory restent planifiés. |
| Sécurité | Bon instinct, trous restants | Hooks, guardrails et registry existent ; skills supply chain et MCP secrets doivent monter d'un cran. |
| Distribution | Correcte côté SDK | `grimoire-kit` est packagé, mais l'ABI produit Agent OS doit être plus nette. |

## Comparaison par référence

| Référence | Ce qu'elle fait mieux | Ce que Grimoire fait mieux | Décision |
| --- | --- | --- | --- |
| OpenAI Agents SDK | Petit noyau, agents/tools/handoffs/guardrails/sessions/tracing. | Méthode projet, IDE-native, cockpit, gouvernance documentaire. | Absorber la sobriété des primitives et les limites explicites de guardrails. |
| LangGraph | Durable execution, checkpointers, interrupt/resume, time travel, HITL. | UI opérateur plus originale, culture de preuve projet. | Construire un Runtime Kernel inspiré, sans importer LangGraph comme dépendance centrale. |
| Microsoft Agent Framework | Enterprise workflows, interop, graph orchestration, providers. | Produit plus singulier, plus proche du workspace agentique réel. | Absorber le modèle workflow + provider + A2A/MCP, refuser la dépendance vendor. |
| Langfuse | Observabilité, datasets, evals, prompt management. | Cockpit local et contextualisé au projet. | Exporter vers une forme compatible, garder Grimoire comme source de vérité locale. |
| Dify et Langflow | Builder visuel, prototypage, API/MCP. | Runtime IDE-native et contrôles plus proches du code. | Import/export flow utile, pas comme kernel. |
| Kagent | Agents déclaratifs Kubernetes, CRD, OTel, MCP. | Meilleur fit local IDE et projet solo/équipe. | Créer plus tard un adapter infra, pas bloquant pour le kernel local. |
| Agent Sandbox et OpenHands | Exécution isolée, worker/sandbox, event store. | Gouvernance plus fine des artefacts et Mission Board. | Ajouter sandbox leases pour les actions risquées. |
| CodeGraphContext et Graphify | Code graph, AST, bundles, tags extrait/inféré. | Déjà un contexte projet riche et des skills. | Priorité haute : Code Graph Grimoire relié à Memory OS. |
| MemPalace et Beads | Mémoire longue, graph de tâches, dépendances, claims atomiques. | Cockpit et runtime visualisable. | Relier task memory, preuves, décisions et graphe typed memory. |
| Switchboard | Kanban déclencheur et rôle opérateur simple. | Contrats, guardrails, mission ledger plus ambitieux. | Garder drag-to-dispatch, mais le brancher sur Runtime Kernel. |
| Pixel Agents | Observation vivante des agents, timeline et spatialisation. | Capacité à relier visualisation à preuves et policies. | Garder Office view comme projection, pas comme moteur. |
| OWASP Agentic/Skills | Taxonomie des risques agentiques et skills. | Hooks et registries déjà présents. | Ajouter skill provenance, signing, scanner et policy AST10. |
| A2A | Agent discovery, AgentCard, tasks, artifacts, interop. | SOG et registry interne déjà riches. | Exposer une compatibilité A2A par adapter contrôlé. |
| MCP | Standard tool/resource interface. | Policy locale et serveur Grimoire déjà réels. | Durcir auth, secrets, loopback, fail-closed et audit. |
| OpenTelemetry GenAI | Vocabulaire commun pour spans, metrics, events. | Vue opérateur locale riche. | Mapper `GrimoireEvent` vers OTel GenAI sans perdre les champs métier. |

## Ce que Grimoire doit revendiquer

Grimoire ne doit pas se vendre comme :

- un simple SDK agents ;
- un clone de LangGraph ;
- un builder visuel low-code ;
- un catalogue de personas ;
- une UI de monitoring.

La bonne revendication :

**Grimoire est un Agent OS IDE-native : un runtime local qui transforme les agents, hooks, tools, mémoires et preuves en missions pilotables depuis un cockpit.**

## Ce que Grimoire doit arrêter de faire

- Ajouter des agents quand un mode ou une skill suffit.
- Ajouter des rooms UI sans nouveau signal kernel.
- Conserver des concepts BM théoriques sans statut.
- Laisser `framework/tools` grossir hors du SDK canonique.
- Garder des policies MCP diagnostiques mais non bloquantes.
- Faire dépendre la preuve d'un transcript brut.

## Ce que Grimoire doit faire maintenant

- Passer de `HookEvent` à `RunEvent`.
- Ajouter `RunState` et `Checkpoint`.
- Définir `Capability Manifest` pour agents, skills, tools, hosts.
- Publier un `AgentCard` Grimoire compatible A2A.
- Ajouter un exporter OTel GenAI.
- Brancher Memory OS sur events, tasks, code graph et preuves.
- Durcir MCP et skills supply chain.
- Faire du Mission Board la surface de vérité opérateur.

