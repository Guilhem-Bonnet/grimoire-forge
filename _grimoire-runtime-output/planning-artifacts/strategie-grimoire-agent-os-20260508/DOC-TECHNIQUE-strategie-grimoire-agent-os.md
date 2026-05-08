# Document technique - Stratégie Grimoire Agent OS

## Objet

Ce document décrit la méthode de comparaison et les sources utilisées pour construire la stratégie `Grimoire Agent OS`.

Le paquet part d'une hypothèse : Grimoire doit viser une position différente des frameworks purs. Le projet peut devenir un control plane IDE-native pour agents, à condition de canoniser son runtime et de réduire les ambiguïtés entre méthode, UI, mémoire, hooks et tools.

## Sources locales analysées

### Rapports internes

| Source | Usage |
| --- | --- |
| `audit-agentique-2026-04-10.md` | Diagnostic de positionnement : workbench IDE-native, SDK sérieux, Game UI différenciante, runtime durable incomplet. |
| `benchmark-dimensionnel-agentique-2026-04-10.md` | Comparaison avec OpenAI Agents SDK, LangGraph et Microsoft Agent Framework. |
| `plan-execution-post-audit-agentique-2026-04-10.md` | Lots L1 à L6 : source de vérité, agents, événements, observabilité, MCP, cockpit. |
| `maturation-agentique-20260421/` | Plan V1 à V4 : bus d'événements, Kanban vivant, Office view, rationalisation BM. |
| `repo-analysis/GUIDE-pilotage-agents-orchestration-agentic-V3-maximum.md` | Analyse approfondie des références : hooks Copilot, LangGraph, CrewAI, OpenAI Agents, Haystack, Dify, sécurité. |
| `reference-agentique-pilotage-20260425/` | Cartographie des 33 dossiers Référence-Agentique et typologie de pilotage. |
| `grimoire-game/` planning artifacts | Contrats Host Bridge, guardrails, tests et UX cockpit. |

### Code et configuration Grimoire

| Source | Signal |
| --- | --- |
| `grimoire-kit/version.txt` | Version locale `3.4.2`. |
| `grimoire-kit/src/grimoire/tools/events.py` | Schéma `GrimoireEvent` Python, ledger `activity.jsonl`, quarantine d'erreurs. |
| `grimoire-kit/apps/grimoire-game/src/contracts/hookEvents.ts` | Miroir TypeScript du contrat d'événements. |
| `grimoire-kit/apps/grimoire-game/src/server/hook-events-feed.ts` | Lecteur Node du ledger canonique. |
| `grimoire-kit/apps/grimoire-game/src/server/control-plane/dispatch-gateway.ts` | Pont Mission Board vers événement `task/start`. |
| `grimoire-kit/apps/grimoire-game/src/state/card-activity.ts` | Projection d'activité Mission Board depuis le ledger. |
| `grimoire-kit/apps/grimoire-game/src/state/office-timeline-view.ts` | Scrubber timeline Office. |
| `grimoire-kit/apps/grimoire-game/src/state/stigmergy-signals.ts` | Consumer stigmergy BM-19. |
| `grimoire-kit/docs/memory-os-roadmap.md` | Cible Memory OS et couches ready/partial/planned. |
| `.github/copilot-instructions.md` | SOG, hooks, model routing, UDF, skill routing. |
| `.vscode/mcp.json` et `_grimoire-runtime/_config/mcp-policy.yaml` | Surface MCP réelle et policy locale. |

## Vérifications effectuées

### Comptage actuel

| Mesure | Valeur observée |
| --- | ---: |
| Agents `.github` | 23 |
| Skills `.github` | 43 |
| Instructions `.github` | 8 |
| Prompts user-facing | 6 |
| Scripts hooks | 16 |
| Modules canoniques `src/grimoire/tools` | 17 |
| Tests TypeScript `grimoire-game` | 116 |

### Tests ciblés

Commande exécutée :

```bash
npm --prefix grimoire-kit/apps/grimoire-game run test -- \
  tests/contracts/hook-events.contract.test.ts \
  tests/contracts/hook-events-client.test.ts \
  tests/integration/runtime-dashboard-store.test.ts \
  tests/integration/runtime-dashboard-view.test.ts \
  tests/integration/mission-board-view.test.ts \
  tests/integration/runtime-observability-surface-view.test.ts \
  tests/integration/office-timeline-view.test.ts \
  tests/integration/stigmergy-signals.test.ts
```

Résultat : 6 fichiers de tests exécutés, 33 tests passés.

### Diagnostic CLI

`python -m grimoire doctor .` dans `grimoire-kit` retourne 10 contrôles sur 10 passés.

`grimoire memory status` montre :

- backend `qdrant-server` prêt ;
- 0 entrée mémoire actuelle ;
- mémoire sémantique prête ;
- mémoire courte partielle ;
- connaissance et memory graph partiels ;
- code graph planifié ;
- task memory planifiée ;
- visualisation partielle.

### Policy MCP

Le rapport MCP local classe 5 serveurs :

- `context7` : pass ;
- `github` : pass, mais mutable distant ;
- `grimoire` : pass, mutable local ;
- `playwright` : pass, mutable local ;
- `ollama` : fail, car remote non allowlisté et header secret en clair.

Ce point doit devenir une gate produit, pas seulement un diagnostic.

## Sources web primaires consultées

| Source | Signal stratégique |
| --- | --- |
| [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/) | Le tracing intégré collecte LLM generations, tool calls, handoffs, guardrails et custom events. |
| [OpenAI Agents SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/) | Les guardrails ont des frontières précises ; les tool guardrails ne couvrent pas tous les chemins, notamment certains handoffs et hosted tools. |
| [LangGraph durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution) | Un runtime durable exige checkpointer, thread id, reprise, idempotence et encapsulation des side effects. |
| [LangGraph persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/) | Les checkpoints rendent HITL, memory, time-travel debugging et fault tolerance possibles. |
| [MCP authorization spec](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) | HTTP MCP s'appuie sur authorization/OAuth ; STDIO récupère les credentials via environnement. |
| [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | Les conventions GenAI couvrent events, exceptions, metrics, model spans, agent spans et MCP. |
| [A2A Protocol specification](https://a2a-protocol.org/latest/specification/) | A2A 1.0 définit AgentCard, Task, Message, Part, Artifact, Extension et interop agent-agent. |
| [OWASP Top 10 Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-2026/) | Référence sécurité pour agents autonomes qui planifient, agissent et décident. |
| [OWASP Agentic Skills Top 10](https://genai.owasp.org/resource/agentic-skills-top-10/) | Les skills sont une couche d'exécution à sécuriser : supply chain, privilèges, provenance, registry scanning. |

## Modèle de comparaison

Chaque référence est comparée sur huit axes :

| Axe | Question |
| --- | --- |
| Kernel | Le noyau expose-t-il peu de primitives stables ? |
| Durabilité | Le run peut-il être interrompu, repris et rejoué ? |
| Interop | Les agents, tools et hosts publient-ils des contrats découvrables ? |
| Sécurité | Les actions sont-elles limitées par policy, sandbox, approvals et provenance ? |
| Observabilité | Les traces et métriques décrivent-elles le run complet ? |
| Mémoire | Le contexte est-il promu, typé, invalidable et relié aux tâches ? |
| Opérateur | Un humain peut-il inspecter, challenger, corriger et fermer une mission ? |
| Distribution | Le système est-il installable, testable, extensible et gouverné ? |

## Limite

Cette stratégie n'est pas une implémentation. Elle est un plan d'élévation. Les chiffres et statuts locaux doivent être revérifiés avant chaque paquet d'exécution, car le projet évolue vite.
