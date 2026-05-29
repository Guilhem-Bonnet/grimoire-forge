---
title: Status d'implémentation — Grimoire Agent OS
description: Avancement par lot (DOSSIER-EXECUTION-AGENTS.md) au 2026-05-27
author: grimoire-master
date: 2026-05-08
updated: 2026-05-27
---

# Status — Grimoire Agent OS

Légende : Fait · Partiel · Non démarré

## Verdict Cible

La cible finale n'est pas encore atteinte.

Le socle critique est atteint pour la mémoire durable :

- Weaviate est actif comme store vectoriel principal.
- Neo4j est actif comme projection graphe.
- Qdrant reste disponible comme source de migration et rollback.
- Le bundle Qdrant vers Weaviate et Neo4j est vector-lossless.
- Les projections code sont vectorisées dans Weaviate et reliées à Neo4j.
- Les tâches, preuves, verdicts et décisions ont des relations graphe explicites vers le code.
- La gate stricte `grimoire memory gate` est verte.
- Le hook `grimoire-memory-gate` est promu en `enforced`.

La cible reste partielle sur les couches suivantes :

- mémoire courte Redis et promotion court-terme vers durable ;
- extraction plus riche des fichiers/symboles touchés depuis diff, traces et événements runtime ;
- cockpit Memory OS connecté aux vues Weaviate, Neo4j, freshness et task overlays ;
- évaluation de qualité du recall ;
- nettoyage continu des anciens statuts qui sur-déclarent `ready`.

## Snapshot Runtime Vérifié

| Surface | État | Preuve |
| --- | --- | --- |
| Weaviate runtime | Fait | `3700` entrées actives dans `GrimoireKitMemory` |
| Bundle migré | Fait | `68` records, `68` vecteurs, `vector_lossless=true` |
| Neo4j migration | Fait | `68` souvenirs migrés, `26` relations `TAGGED_WITH` |
| Code graph Neo4j | Fait | `14456` `CodeNode`, `45575` `CODE_EDGE` |
| Code vectors Weaviate | Fait | `2746` projections : fichier, symbole, méthode, test, contrat |
| Task memory vectorielle | Fait | `1` mission, `38` tâches, `825` événements, `20` incidents, `1` evidence, `1` verdict, `1` décision, `886` vecteurs |
| Liens vecteur vers graphe | Fait | `3632` relations `MEMORY_FOR` |
| Liens task/evidence/code | Fait | `1` relation `TOUCHES_CODE`, `1` relation `COVERS_CODE`, `2` arêtes décisionnelles |
| Hook Memory OS | Fait | Hook en `enforced`, digest `7770c61dc4e4`, gateway OK |
| Cockpit Memory OS | Partiel | Vues existantes, pas encore cockpit complet connecté au contrat Memory OS |

---

## LOT-A — Source de vérité et documentation

| Sous-lot | Statut | Notes |
|---|---|---|
| A1 — Déclarer le paquet cible actif | ✅ | Cahier des charges présent dans `planning-artifacts/` |
| A2 — Registre des plans dépréciés | ✅ | `deprecated-plans-registry.yaml` — 40+ plans mappés (active/absorbed/archive/incubator) + `plans_registry.py` validator |

---

## LOT-B — Mission Ledger

| Sous-lot | Statut | Fichiers |
|---|---|---|
| B1 — Schemas ledger | ✅ | `missions/schemas.py`, `missions/ledger.py` |
| B2 — Query ready/blocked/needs_verification/incident | ✅ | `missions/ledger.py` |
| B3 — Adapter Beads (import/export JSONL) | ✅ | `missions/beads_adapter.py` — import/export JSONL, idempotent, 14 tests |

---

## LOT-C — Runtime Kernel

| Sous-lot | Statut | Fichiers |
|---|---|---|
| C1 — Contrats WorkflowInstance et RunEvent | ✅ | `runtime/schemas.py` |
| C2 — Checkpoint et resume | ✅ | `runtime/kernel.py` |
| C3 — Tool mediation via policy | ✅ | `policies/engine.py`, `policies/schemas.py` |

---

## LOT-D — Recipes et workflows

| Sous-lot | Statut | Fichiers |
|---|---|---|
| D1 — Recipe schema | ✅ | `runtime/recipes.py` — Recipe, RecipeRegistry |
| D2 — Conversion Gas City formulas → recipes | ✅ | `runtime/gascity_converter.py` — GasCityConverter, tags experimental+gas-city, 18 tests |
| D3 — Conversion CrewAI Flows | ✅ | `runtime/crewai_adapter.py` — CrewAIAdapter, output schema gate, normalize trace, 23 tests |

---

## LOT-E — Hook and Guardrail Plane

| Sous-lot | Statut | Fichiers |
|---|---|---|
| E1 — Hook registry | ✅ | `.github/hooks/`, `hook-safety-registry.json`, `hook-safety-gate.py` |
| E2 — Terminal guard (PreToolUse) | ✅ | `grimoire-terminal-guard.json` + script + `terminal-guard-policy.py` (mode: shadow) |
| E3 — Closure guard (no close sans evidence) | ✅ | `policies/engine.py` — règle `task_close_requires_verification` |

---

## LOT-F — Pack Registry

| Sous-lot | Statut | Fichiers |
|---|---|---|
| F1 — Pack manifest et validator | ✅ | `registry/packs.py` |
| F2 — Pack lock et digest | ✅ | `registry/packs.py` |
| F3 — Pack doctor | ✅ | `registry/packs.py` |

---

## LOT-G — Memory OS

| Sous-lot | Statut | Fichiers |
|---|---|---|
| G0 — Migration Qdrant → Weaviate + Neo4j | ✅ | `migration.py` (822 lignes), `backends/weaviate.py`, CLI `grimoire memory migrate`, `docker-compose.memory-target.yml` |
| G1 — Memory contracts | ✅ | `memory/architecture.py`, `memory/manager.py` |
| G2 — Recall gouverné | ✅ | `memory/manager.py` |
| G3 — Promotion gouvernée | ✅ | `memory/sidecar.py`, `memory/manager.py` |
| G4 — Projection vectorielle code | ✅ | `memory/projections.py`, CLI `grimoire memory vector sync-code`, `verify` |
| G5 — Projection vectorielle task memory | ✅ | CLI `grimoire memory vector sync-tasks`; ledger réel + evidence/verdict/décision |
| G6 — Gate Memory OS stricte | ✅ | `grimoire memory gate`, CI `memory-os-gate.yml`, task-flow |
| G7 — Hook Memory OS promu | ✅ | `grimoire-memory-gate` en `enforced`, digest `7770c61dc4e4` |

---

## LOT-H — Code Graph

| Sous-lot | Statut | Fichiers |
|---|---|---|
| H1 — Index symboles (ast parser) | ✅ | `codegraph/parser.py`, `codegraph/graph.py` |
| H2 — Impact analysis + backends | ✅ | `codegraph/graph.py`, `codegraph/backends/neo4j.py` |

---

## LOT-I — Cockpit

| Sous-lot | Statut | Fichiers |
|---|---|---|
| I1 — Mission Board projection (read model) | ✅ | `missions/projections.py` — CockpitProjectionBuilder |
| I2 — Workflow et evidence views | ✅ | `EvidenceProjection`, `VerdictProjection` dans projections.py + EvidenceService integration |
| I3 — Policy et incident views | ✅ | `IncidentProjection` riche (severity, kind, status, summary) dans CockpitProjection |

---

## LOT-J — Host Bridge et interop

| Sous-lot | Statut | Fichiers |
|---|---|---|
| J1 — Capability manifest | ✅ | `bridges/schemas.py`, `bridges/host.py` |
| J2 — MCP adapter | ✅ | `mcp/server.py`, `mcp/security.py` |
| J3 — A2A adapter | ✅ | `bridges/a2a_adapter.py` — import/export, fast-forward transitions, normalize_trace, 37 tests |

---

## LOT-K — Observabilité et evals

| Sous-lot | Statut | Fichiers |
|---|---|---|
| K1 — Trace Ledger | ✅ | `traces/ledger.py`, `traces/schemas.py` |
| K2 — OTel et export JSONL | ✅ | `traces/ledger.py` — `export_otel_jsonl()` |
| K3 — Eval harness | ✅ | `evals/schemas.py`, `evals/harness.py`, `evals/fixtures.py` — 7 cas pré-câblés, diff baseline |

---

## LOT-L — Distribution kit

| Sous-lot | Statut | Fichiers |
|---|---|---|
| L1 — CLI projet agentique | ✅ | `cli/cmd_init.py`, `grimoire init` |
| L2 — SDK public | ✅ | `grimoire/__init__.py` — 18 symboles publics (ledger, evidence, policy, runtime, traces, packs, memory), 15 tests SDK |
| L3 — Documentation kit | ✅ | MkDocs build sans warnings — liens fixes, `pack-quickstart.md` ajouté, gate builder OK |

---

## LOT-M — Fusion projets de référence

| Sous-lot | Statut | Notes |
|---|---|---|
| M1 — Gastownhall mapping complet | ✅ | `M1-gastownhall-mapping-matrix.md` — 29 primitives, 26/29 ✅ (90 %), backlog adapters documenté |
| M2 — CrewAI integration profile | ✅ | `M2-crewai-integration-profile.md` — contrat adapter, guardrails, sample import |
| M3 — Security references (OWASP Agentic) | ✅ | `policies/security.py` — 10 menaces OWASP, 4 trust tiers, `evaluate_pack_trust()`, 25 tests |

---

## Vue d'ensemble

Le tableau ci-dessous conserve le snapshot de sous-lots déjà livrés. Il ne doit
pas être lu comme une fermeture de la cible finale complète : les items de la
section "Priorités restantes" restent ouverts.

| Lot | ✅ | 🔶 | ❌ |
|---|---|---|---|
| A | 2 | — | — |
| B | 3 | — | — |
| C | 3 | — | — |
| D | 3 | — | — |
| E | 3 | — | — |
| F | 3 | — | — |
| G | 8 | — | — |
| H | 2 | — | — |
| I | 3 | — | — |
| J | 3 | — | — |
| K | 3 | — | — |
| L | 3 | — | — |
| M | 3 | — | — |
| **Total** | **42** | **0** | **0** |

**Socle exécutable atteint pour les lots principaux. Cible finale encore partielle.**

### Livrables de cette session

| Livrable | Impact |
| --- | --- |
| `terminal-guard-policy.py` + hook (E2) | Validation shell avant exécution, mode shadow |
| 8 templates v2 enrichis (B) | Modules adaptatifs, contrat de sortie, exemples, gestion d'erreur |
| `output-contract-standards.instructions.md` (C1) | Contrats de sortie pour 5 types de tâche, `applyTo: "**"` |
| Compression `build_subagent_context` (C2) | 396 bytes → 72 bytes (~100 tokens économisés × N sous-agents) |
| Marqueurs cache `grimoire-master.md` (C3) | `CACHE_BOUNDARY` + `TOKENS:` annotations, ~8 600 tokens mis en cache |
| `EvidenceProjection` + `VerdictProjection` (I2) | Vues evidence + verdict dans CockpitProjection, 10 tests |
| `IncidentProjection` riche (I3) | Severity/kind/status/summary dans cockpit, 4 tests |
| `EvalHarness` + fixtures (K3) | 7 cas pré-câblés policy+lifecycle+intake, diff baseline JSONL, 28 tests |
| G0 déjà complet (vérification) | `migration.py` + `weaviate.py` + CLI + docker-compose — tous les gates OK |
| `beads_adapter.py` (B3) | import/export JSONL idempotent, mapping Beads→MissionTask, 14 tests |
| `plans_registry.py` + `deprecated-plans-registry.yaml` (A2) | 40+ plans mappés, validator, 16 tests |
| `a2a_adapter.py` (J3) | Import A2A task→MissionLedger, fast-forward transitions, guardrail completed→NEEDS_VERIFICATION, 37 tests |
| `grimoire/__init__.py` étendu (L2) | 18 symboles SDK publics, test end-to-end, gate example project ✅, 15 tests |
| `M1-gastownhall-mapping-matrix.md` (M1) | 29 primitives Gastownhall mappées, 26/29 ✅, backlog adapters documenté |
| `gascity_converter.py` (D2) | GasCityConverter, tags experimental+gas-city, déterministe, 18 tests |
| `crewai_adapter.py` (D3) | CrewAIAdapter, output schema gate, normalize trace, 23 tests |
| Docs build propre (L3) | 0 warnings, `pack-quickstart.md` + nav, gate builder externe ✅ |
| `M2-crewai-integration-profile.md` (M2) | Contrat adapter, 4 guardrails, sample import documenté |
| `policies/security.py` (M3) | 10 menaces OWASP, 4 trust tiers, `evaluate_pack_trust()`, 25 tests refus |
| Projections code granulaires (G008) | `2746` entrées Weaviate : fichier, symbole, méthode, test-file, contrat docstring |
| Import task-flow MissionLedger (G009) | `336` événements task-flow importés, puis ledger porté à `38` tâches avec evidence runtime |
| Hook Memory OS enforced (G007) | `grimoire-memory-gate` promu en `enforced`, digest `7770c61dc4e4`, gateway OK |
| Liens task/evidence/code/décision (G010) | `TOUCHES_CODE`, `COVERS_CODE`, `GrimoireDecision`, `HAS_DECISION`, `PRODUCED_DECISION` validés par gate |

---

## Priorités restantes

| Priorité | Statut | Gate d'acceptation |
| --- | --- | --- |
| Construire cockpit Memory OS connecté au contrat runtime | À faire | vue Memory OS lit `memory status`, graph stats et vector neighborhoods |
| Ajouter évaluation de recall Memory OS | À faire | scénarios task similaire, fichier impacté, incident récurrent |
| Ajouter mémoire courte Redis optionnelle | À faire | fallback local, TTL, leases, promotion contrôlée |
| Étendre extraction task-code depuis diff/git/runtime | À faire | relations `TOUCHES_CODE` couvrent fichiers réellement modifiés et symboles impactés |
| Nettoyer les statuts anciens qui sur-déclarent "ready" | En cours | docs alignées avec `grimoire memory status` |
