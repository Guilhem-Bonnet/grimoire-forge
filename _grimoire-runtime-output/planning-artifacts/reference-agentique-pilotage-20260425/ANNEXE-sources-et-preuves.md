# Annexe - Sources et preuves locales

Base : `/mnt/Travail/Projets/Dev/Référence-Agentique/`

Cette annexe liste les preuves utilisées pour les rapports. Les références sont locales et doivent être relues dans le workspace si une décision de production en dépend.

## Orchestration, handoffs et graphes

| Dépôt | Référence | Preuve exploitée |
| --- | --- | --- |
| `openai-agents-python` | `README.md:3` | Framework léger pour workflows multi-agents. |
| `openai-agents-python` | `README.md:12-19` | Concepts : agents, tools, guardrails, handoffs, HITL, sessions, tracing. |
| `openai-agents-python` | `README.md:49-51` | Sandbox agent avec filesystem, commandes, patchs et état workspace. |
| `openai-agents-python` | `docs/human_in_the_loop.md:3-7` | HITL avec pause, sérialisation et reprise de `RunState`. |
| `openai-agents-python` | `docs/human_in_the_loop.md:40-50` | Approbations de tools et décisions persistées dans l'état de run. |
| `openai-agents-python` | `docs/models/index.md:243-253` | Mélange de modèles dans un workflow avec prudence sur capacités et prompts. |
| `langgraph` | `README.md:12` | Framework d'orchestration bas niveau pour agents stateful. |
| `langgraph` | `README.md:37-43` | Durable execution, HITL, mémoire, debugging, tracing, métriques. |
| `langgraph` | `libs/checkpoint-conformance/README.md:3-5` | Suite de conformité pour contrats de checkpoint storage. |
| `agent-framework` | `README.md:10` | Framework multi-langage pour construire, orchestrer et déployer des agents. |
| `agent-framework` | `README.md:55-80` | Graph workflows, DevUI, OTel, providers et middleware. |
| `agent-framework` | `python/README.md:198-246` | Collaboration multi-agents : sequential, concurrent, group chat, handoff, magentic. |
| `crewAI` | `README.md:56-60` | Framework indépendant avec Crews et Flows. |
| `crewAI` | `README.md:162-180` | Crews autonomes vs Flows avec contrôle événementiel, état et branches. |
| `crewAI` | `README.md:432` | Processus hiérarchique avec manager pour délégation et validation. |
| `autogen` | `README.md:14-25` | Maintenance mode et recommandation Microsoft Agent Framework pour nouveaux projets. |
| `autogen` | `README.md:101-106` | MCP de confiance seulement et AgentTool pour orchestration de base. |
| `autogen` | `README.md:120-145` | Sous-agents spécialisés exposés comme tools. |
| `autogen` | `README.md:177-194` | Couches Core API, AgentChat, Extensions, Studio, Bench, Magentic-One. |
| `haystack` | `README.md:12-14` | Framework d'orchestration avec pipelines modulaires et workflows agents. |
| `haystack` | `README.md:56-64` | Context engineering, composants, boucles, branches et logique conditionnelle. |
| `haystack` | `haystack/dataclasses/breakpoints.py:15-21` | Snapshots pour inspecter et reprendre l'état de pipeline. |
| `haystack` | `haystack/dataclasses/breakpoints.py:122-171` | `AgentSnapshot` et `PipelineState` sérialisent inputs, visites et outputs. |

## Plateformes, builders et surfaces opérateur

| Dépôt | Référence | Preuve exploitée |
| --- | --- | --- |
| `OpenHands` | `README.md:34-49` | SDK, CLI et GUI locale pour agents de développement. |
| `OpenHands` | `README.md:58-65` | Cloud et Enterprise avec intégrations, multi-user, RBAC et Kubernetes. |
| `OpenHands` | `openhands/app_server/event/README.md:1-21` | Event storage, retrieval, streaming et backends multiples. |
| `OpenHands` | `openhands/app_server/sandbox/README.md:1-21` | Sandboxes Docker, Remote et Local pour exécution sécurisée. |
| `dify` | `README.md:91-114` | Workflow visuel, modèles, prompt IDE, RAG, agents, logs, monitoring, API. |
| `dify` | `README.md:142-150` | Monitoring Grafana et déploiement Kubernetes. |
| `dify` | `api/models/workflow.py:26-35` | Imports human input adapters et pause reasons. |
| `dify` | `api/controllers/console/app/agent.py:31-49` | Endpoint de logs d'exécution agent. |
| `langflow` | `README.md:16-27` | Visual builder, API/MCP, playground, multi-agent, observabilité, sécurité enterprise. |
| `langflow` | `src/lfx/src/lfx/schema/graph.py:8-23` | Tweaks de flow pour personnaliser le comportement dynamique. |
| `langflow` | `src/lfx/src/lfx/schema/workflow.py:15-24` | Statuts de job : queued, in-progress, completed, failed, cancelled, timed out. |
| `langflow` | `src/lfx/src/lfx/schema/workflow.py:50-65` | Exécution background/stream avec contrainte exclusive. |
| `switchboard` | `README.md:3-13` | Kanban VS Code qui déclenche des agents via terminal API sans gateway. |
| `switchboard` | `README.md:41-56` | Rôles : Planner, Team Lead, Lead Coder, Coder, Reviewer, Acceptance Tester, Analyst. |
| `switchboard` | `README.md:92-111` | Routing modes, complexity routing, automation multi-terminaux. |
| `switchboard` | `docs/DELEGATION_WORKFLOWS_README.md:1-15` | Contrat de message de délégation et gate de complétion confirmée par l'utilisateur. |
| `switchboard` | `.github/agents/switchboard.agent.md:1-42` | Tools MCP, inbox/outbox filesystem et triggers de workflow. |
| `pixel-agents` | `README.md:35-45` | Visualisation live d'agents, speech bubbles et subagents. |
| `pixel-agents` | `README.md:105-120` | Observation des transcripts JSONL Claude Code et limites heuristiques. |
| `Design/ui` | `ui/README.md:1-4` | Base shadcn/ui pour construire une bibliothèque de composants customisable. |
| `vscode-copilot-chat` | `README.md` | Référence host IDE Copilot Chat pour agent de code intégré à VS Code. |

## Infrastructure, sandbox et sécurité

| Dépôt | Référence | Preuve exploitée |
| --- | --- | --- |
| `kagent` | `README.md:69-83` | Agents comme CRD Kubernetes, ModelConfig, MCP tools, OTel, déclaratif et testable. |
| `kagent` | `README.md:93-98` | Controller, UI, Engine, CLI. |
| `kagent` | `docs/architecture/README.md:29-74` | Controller, DB, A2A proxy, pods agents, ADK runtime, MCP tool servers. |
| `kagent` | `docs/architecture/README.md:87-100` | Controllers et translator produisent Deployment, Service, Secret, ServiceAccount. |
| `kagent` | `docs/architecture/a2a-subagents.md:1-5` | Subagents A2A comme tools avec HITL propagation, live activity, user ID. |
| `agent-sandbox` | `README.md:20-39` | Sandbox CRD : pod stateful, identité stable, stockage persistant, lifecycle. |
| `agent-sandbox` | `README.md:40-83` | Architecture controller Kubernetes. |
| `agent-sandbox` | `docs/configuration.md:1-34` | Flags de concurrence controller, QPS et burst. |
| `agent-sandbox` | `dev/load-test/README.md:1-38` | Tests de charge et mesure de startup latency. |
| `openclaw` | `README.md:132-162` | DMs untrusted, allowlist, gateway local-first, routage multi-agent, isolation, sandbox. |
| `browser-use` | `README.md:43-91` | Agent navigateur avec Browser et LLM. |
| `browser-use` | `browser_use/agent/service.py:19-80` | Events cloud, event bus, TokenCost, observabilité, telemetry, tools. |
| `browser-use` | `browser_use/browser/watchdogs/security_watchdog.py:1-93` | Watchdog sécurité contre URLs interdites, redirects et nouveaux onglets. |
| `browser-use` | `examples/features/parallel_agents.py:27-47` | Exemple expérimental d'agents parallèles sur une session browser. |
| `LLMSecurityGuide` | `Readme.md:88-119` | Risques critiques et OWASP Agentic Applications avec least agency. |
| `LLMSecurityGuide` | `Readme.md:792-849` | Policy checks, rate limit, sandbox, output validation et Zero Trust AI. |
| `LLMSecurityGuide` | `Readme.md:853-875` | Risques RAG et vector security. |
| `shannon` | `README.md:23-49` | Pentester autonome avec analyse source, exploitation dynamique et PoC. |
| `shannon` | `README.md:134-153` | Worker avec repo cible monté read-only et avertissement d'autorisation explicite. |

## Mémoire, contexte et compression

| Dépôt | Référence | Preuve exploitée |
| --- | --- | --- |
| `CodeGraphContext` | `README.md:89-95` | Index tree-sitter et requêtes MCP de call chain. |
| `CodeGraphContext` | `README.md:125-165` | Indexing, relations, bundles, watch, CLI/MCP, langages et DB backends. |
| `CodeGraphContext` | `docs/BUNDLE_ARCHITECTURE.md:1-42` | Flux de bundle source repo vers export metadata/schema/nodes/edges/stats. |
| `CodeGraphContext` | `docs/BUNDLE_ARCHITECTURE.md:69-78` | Import avec validation metadata/schema/nodes/edges. |
| `CodeGraphContext` | `docs/MCP_TOOLS.md:1-33` | MCP avec outils de contexte, découverte et switching. |
| `CodeGraphContext` | `docs/MCP_TOOLS.md:87-115` | Analyse relations, dead code et complexité. |
| `graphify` | `README.md:55-73` | Clone/merge graphs, shrink guard, passes AST déterministes et agents parallèles. |
| `graphify` | `README.md:88-109` | Support Claude, Codex, OpenCode, Copilot, hooks et config multi-agent. |
| `mempalace` | `README.md:26-40` | Historique verbatim, recherche sémantique, wings/rooms/drawers, local. |
| `mempalace` | `README.md:126-150` | KG temporel, MCP tools, wings/diaries, hooks avant compression contexte. |
| `mempalace` | `mempalace/README.md:7-40` | Modules CLI, normalisation, searcher, couches L0-L3, ChromaDB, SQLite KG. |
| `LLMLingua` | `README.md:34-53` | Prompt compression, LongLLMLingua, LLMLingua-2 et SecurityLingua. |
| `LLMLingua` | `README.md:60-70` | Motivation token limits et coûts. |
| `LLMLingua` | `experiments/llmlingua2/README.md:25-35` | Scripts data collection, training et evaluation. |
| `gas town/beads` | `beads/README.md:15-40` | Mémoire structurée persistante pour agents, graphe de dépendances, IDs anti-conflit. |
| `gas town/beads` | `beads/README.md:42-60` | Commandes ready/create/claim/dep/show et hiérarchie d'IDs. |
| `gas town/beads` | `beads/README.md:88-126` | Dolt embedded/server mode et isolation. |
| `gas town/beads` | `beads/docs/MULTI_REPO_AGENTS.md:9-40` | MCP unique avec routage vers serveurs Dolt par projet et isolation DB. |
| `gas town/beads` | `beads/docs/MULTI_REPO_AGENTS.md:67-140` | Routing maintainer/contributor, inheritance et hydration multi-repo. |

## Méthodes, skills et formation

| Dépôt | Référence | Preuve exploitée |
| --- | --- | --- |
| `BMAD-METHOD` | `README.md:14-23` | Agents/workflows comme collaborateurs experts, adaptation domaine, workflows structurés. |
| `BMAD-METHOD` | `README.md:29-33` | Roadmap cross-platform agent team, sub agents, skills. |
| `BMAD-METHOD` | `README.md:59-69` | Modules BMM, BMB, TEA, BMGD, CIS. |
| `claude-skills` | `README.md:34-72` | 66 skills, activation contextuelle, workflows multi-skill, common-ground context engineering. |
| `superpowers` | `README.md:1-15` | Méthodologie skills pour spec, design, plan et subagent-driven development. |
| `superpowers` | `docs/README.codex.md:35-88` | Codex skills, multi_agent, discovery et structure de skills personnelles. |
| `andrej-karpathy-skills` | `README.md:11-30` | Problèmes LLM : mauvaises hypothèses, sur-complexité, effets de bord ; quatre principes. |
| `andrej-karpathy-skills` | `README.md:34-97` | Think before coding, simplicity first, surgical changes, goal-driven execution. |
| `andrej-karpathy-skills` | `README.md:132-148` | Succès amélioré quand les critères sont explicites. |
| `ai-agents-for-beginners` | `README.md:94-115` | Leçons multi-agent, production, protocoles, contexte, mémoire, browser use. |
| `ai-agents-for-beginners` | `08-multi-agent/README.md:32-78` | Scénarios multi-agent, avantages, building blocks, visibilité. |
| `ai-agents-for-beginners` | `08-multi-agent/README.md:79-100` | Group chat et hand-off patterns. |
| `ai-agents-for-beginners` | `13-agent-memory/README.md:36-129` | Définition, importance, types et gestion de mémoire agent. |

## Références spécialisées et expérimentales

| Dépôt | Référence | Preuve exploitée |
| --- | --- | --- |
| `ruflo` | `README.md:23-40` | Orchestration multi-agent Claude Code, rôles, swarms, mémoire, sécurité, learning loop. |
| `ruflo` | `README.md:56-82` | Routage/swarm layer, topologies, consensus, claims, agents, memory, providers. |
| `ruflo` | `.agents/README.md:1-38` | Configuration `.agents` et skills pour Codex. |
| `Octogent` | `README.md:49-58` | Agent autonome local-first, worker pool, Think-Act-Observe, skills, SQLite. |
| `Octogent` | `README.md:107-132` | Commandes usage, task et worker status. |
| `OpenMythos` | `README.md:180-230` | Hypothèse recurrent-depth transformer, blocs prelude/recurrent/coda, GQA/MLA. |
| `gas town/community` | `community/README.md:1-40` | Hub communautaire pour Gas Town et Beads. |
| `gas town/community` | `community/plans/gastownhall-ecosystem-plan.md:5-55` | Ecosystème géré, contributeurs, transparence, social proof. |
| `gas town/docs` | `docs/README.md:15-25` | Mise en place de skills de documentation pour outils AI. |

## Note de prudence

Plusieurs dépôts contiennent des claims de performance ou d'autonomie. Ces claims ont été utilisés comme indications de design, pas comme résultats validés. Pour une adoption production, il faut créer un benchmark local par workflow cible, avec traces, coûts, preuves et cas de refus.

