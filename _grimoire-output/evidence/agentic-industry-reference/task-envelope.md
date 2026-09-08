# Agentic Task Envelope

## Task

- Task id: agentic-industry-reference
- Request: collecter la documentation agentique officielle (labos, protocoles, standards, frameworks, recherche) et l'incorporer dans un fichier de référence que les agents et workflows du kit chargent à la demande.
- Owner agent: session Claude Code (persona d'entrée concierge), six sous-agents de collecte web
- Profile: governed
- Current state: `done`
- Risk level: `low`

## Context orchestration

| Context item | Source | Reason selected | Freshness | Token budget |
|---|---|---|---|---:|
| Doctrine Forge/produit | `.github/copilot-instructions.md` | Fixe la cible : le produit grimoire-kit, jamais l'atelier. | 2026-09-08 | 1500 |
| Socle des agents du kit | `grimoire-kit/framework/agent-base.md` | Point d'ancrage des protocoles chargés à la demande. | origin/main 3.40.0 | 2000 |
| Mécanique de déploiement des protocoles | `grimoire-kit/src/grimoire/core/scaffold.py` (`_PROTOCOL_DOCS`) | Liste explicite des fichiers `framework/*.md` livrés dans `_grimoire/kit/framework/`. | origin/main 3.40.0 | 1000 |
| Garde des références mortes | `grimoire-kit/tests/test_delivered_paths_resolve.py` | Tout protocole cité par le socle doit être livré. | origin/main 3.40.0 | 500 |
| Charte documentaire | `_grimoire-runtime/_memory/tech-writer-sidecar/documentation-standards.md` | CommonMark strict, aucune estimation temporelle. | 2026-09-08 | 800 |

## Knowledge base usage

| Knowledge source | Query or index | Trust level | Used as source of truth? | Notes |
|---|---|---|---|---|
| Docs officielles Anthropic, OpenAI, Google, Microsoft, AWS, LangChain | WebFetch/WebSearch par sous-agent, sources primaires uniquement | authoritative | yes | Chaque affirmation du fichier de référence porte sa source. |
| Specs MCP, A2A, AGENTS.md, Agent Skills, OTel GenAI, OWASP, NIST, ISO, EU AI Act | Sites des specs et organismes | authoritative | yes | Versions et dates relevées. |
| arXiv, leaderboards de benchmarks | Pages publiques | high | partial | Chiffres retenus seulement s'ils sont lus sur la page. |

## Memory usage

| Memory surface | Read/write | Purpose | Integrity check |
|---|---|---|---|
| Mémoire persistante de session (`MEMORY.md`) | read/write | Pièges connus du clone kit partagé ; consigner la livraison. | Recoupée avec `git worktree list` avant écriture. |

## Tool boundary

| Tool | Permission | Scope | Blast-radius limit |
|---|---|---|---|
| Bash (cat, grep, sed, git) | read/execute | Forge et worktree jetable du kit. | Aucune commande destructive ; pas de `git add -A`. |
| WebFetch, WebSearch (sous-agents) | read | Sources primaires publiques. | Lecture seule. |
| Write/Edit | write | `grimoire-kit/framework/agentic-industry-reference.md`, `scaffold.py` (liste `_PROTOCOL_DOCS`), `agent-base.md` (pointeur), preuve Forge. | Fichiers déclarés ici uniquement. |
| gh | write | Ouverture d'une PR sur Grimoire-kit. | Pas de merge, pas de force-push. |

## LLM routing

| Step | Provider | Model or capability | Fallback | Data policy |
|---|---|---|---|---|
| Collecte web parallèle | anthropic | claude-fable-5-1 (sous-agents general-purpose) | aucune | Sources publiques, aucune donnée personnelle. |
| Rédaction et intégration | anthropic | claude-fable-5-1 | aucune | Idem. |

## Evidence gates

| Gate | Required evidence | Status |
|---|---|---|
| Plan accepted or autonomous assumption recorded | Hypothèse autonome : cible = produit (fichier dans `framework/` du kit, livré via `_PROTOCOL_DOCS`), PR ouverte sans merge. | complete |
| Implementation complete | `framework/agentic-industry-reference.md` (762 lignes), entrée `_PROTOCOL_DOCS`, section « Référence industrielle » dans `agent-base.md`, ligne dans `agent-base-compact.md`, assertion dans `test_scaffold.py` ; commit `9d5ca9f6`, PR Grimoire-kit#315. | complete |
| Validation complete | pytest 47 passed, ruff propre, ratchet OK, gate check bootstrap et verify Forge (voir evidence-pack). | complete |
| Deviations documented | Registre des pages inaccessibles en section 11 du fichier ; écarts dans le pack de preuve. | complete |
