---
title: M1 — Matrice de mapping Gastownhall → Grimoire Agent OS
description: Correspondance canonique entre primitives Gastownhall et implémentation Grimoire
lot: M1
status: complete
updated: 2026-05-08
---

# M1 — Matrice de mapping Gastownhall → Grimoire

## Vocabulaire de statut

| Symbole | Signification |
|---|---|
| ✅ | Implémenté dans grimoire-kit, tests passants |
| 🔶 | Partiel ou expérimental |
| ❌ | Non démarré / hors scope actuel |

---

## Primitives de contrôle et d'orchestration

| Primitive Gastownhall | Destination Grimoire | Statut | Module Grimoire |
|---|---|---|---|
| **Mayor** (point d'entrée unique) | `grimoire-master` — orchestrateur SOG | ✅ | `_grimoire-runtime/core/agents/grimoire-master.md` |
| **Convoy** (bundle de tâches liées) | `MissionBundle` / `MissionLedger.create_mission()` | ✅ | `grimoire/missions/ledger.py` |
| **Beads** (issues/tasks structurées) | `MissionTask` dans le `MissionLedger` | ✅ | `grimoire/missions/schemas.py`, `beads_adapter.py` |
| **Molecule / Formula** (workflow réutilisable) | `Recipe` (versionnée) + `WorkflowInstance` (exécution) | ✅ | `grimoire/runtime/recipes.py`, `runtime/schemas.py` |
| **Seance** (reprise de session) | `Session Lineage` via `TraceLedger` + `RuntimeKernel.resume()` | ✅ | `grimoire/traces/ledger.py`, `runtime/kernel.py` |
| **Claim** (prise en charge d'une tâche) | `MissionLedger.claim_task()` avec `host_id` | ✅ | `grimoire/missions/ledger.py:claim_task` |
| **Hot State** (leases, heartbeats) | `WorkflowInstance.checkpoint_data` (in-process) | 🔶 | `grimoire/runtime/schemas.py` — Redis optionnel non câblé |

---

## Observabilité et traçabilité

| Primitive Gastownhall | Destination Grimoire | Statut | Module Grimoire |
|---|---|---|---|
| **gascity-otel** (traces OpenTelemetry) | `TraceLedger.export_otel_jsonl()` | ✅ | `grimoire/traces/ledger.py` |
| **Run trace** (événements d'exécution) | `TraceRecord` + `TraceLedger.record()` | ✅ | `grimoire/traces/schemas.py` |
| **Witness / Deacon** (supervision santé) | `IncidentProjection` dans `CockpitProjection` | ✅ | `grimoire/missions/projections.py` |
| **Dogs** (détection de blocage) | `PolicyEngine` + règle `task_close_requires_verification` | ✅ | `grimoire/policies/engine.py` |
| **Refinery** (queue de vérification) | `NEEDS_VERIFICATION` state + `EvidenceService.verify()` | ✅ | `grimoire/evidence/service.py` |

---

## Packs, registry, gouvernance

| Primitive Gastownhall | Destination Grimoire | Statut | Module Grimoire |
|---|---|---|---|
| **Pack / Overrides** (distribution d'agent) | `PackManifest` + `PackRegistry` + Overlays | ✅ | `grimoire/registry/packs.py` |
| **Pack doctor** (validation santé) | `PackRegistry.doctor()` | ✅ | `grimoire/registry/packs.py` |
| **Pack lock / digest** | `PackManifest.lock` + sha256 digest | ✅ | `grimoire/registry/packs.py` |
| **Stamps / Trust Tiers** | `VerdictDecision` + `VerificationVerdict` (attestations) | ✅ | `grimoire/evidence/schemas.py` |
| **Marketplace** | `PackMarketplaceCatalog` (catalogue, non déployé) | 🔶 | `grimoire/registry/packs.py` — schéma OK, déploiement ❌ |
| **Wasteland** (federation) | `Grimoire Commons` — hors scope noyau | ❌ | Reporté |

---

## Interopérabilité et bridges

| Primitive Gastownhall / Externe | Destination Grimoire | Statut | Module Grimoire |
|---|---|---|---|
| **Beads JSONL export** | `BeadsAdapter` (import/export idempotent) | ✅ | `grimoire/missions/beads_adapter.py` |
| **A2A protocol** (Google Agent-to-Agent) | `A2AAdapter` (import task, export status, normalize trace) | ✅ | `grimoire/bridges/a2a_adapter.py` |
| **MCP** (Model Context Protocol) | `MCP server` + `MCPSecurity` | ✅ | `grimoire/mcp/server.py`, `mcp/security.py` |
| **Host bridge** (capability manifest) | `HostBridge.detect()` → `HostCapabilityManifest` | ✅ | `grimoire/bridges/host.py` |

---

## Mémoire et contexte

| Primitive Gastownhall | Destination Grimoire | Statut | Module Grimoire |
|---|---|---|---|
| **Semantic Recall** (recall sémantique) | `MemoryManager` + backends Weaviate/Neo4j/JSON | ✅ | `grimoire/memory/manager.py` |
| **Session lineage** (généalogie session→run) | `TraceLedger` + `WorkflowInstance.run_id` | ✅ | `grimoire/traces/ledger.py` |
| **Progressive disclosure** | `MemoryManager.recall()` gouverné + sidecar | ✅ | `grimoire/memory/sidecar.py` |
| **Qdrant backend** | Migré vers Weaviate + Neo4j (G0) | ✅ | `grimoire/memory/backends/weaviate.py` |

---

## Code graph et analyse statique

| Primitive Gastownhall | Destination Grimoire | Statut | Module Grimoire |
|---|---|---|---|
| **Symbol index** | `CodeGraphParser` (AST) | ✅ | `grimoire/codegraph/parser.py` |
| **Impact analysis** | `CodeGraph.impact_set()` | ✅ | `grimoire/codegraph/graph.py` |
| **Neo4j backend** | `CodeGraphNeo4jBackend` | ✅ | `grimoire/codegraph/backends/neo4j.py` |

---

## Adapters backlog (primitives à câbler)

Les primitives ci-dessous ont un équivalent schéma mais pas encore d'adapter ou de déploiement :

| Backlog item | Priorité | Scope | Prérequis |
|---|---|---|---|
| `Wasteland` / `Grimoire Commons` federation | Basse | Hors noyau | Marketplace stable |
| `Marketplace` déployé sur registry public | Basse | L3 polish | Pack doctor + provenance |
| `Hot State` Redis adapter | Basse | Optionnel | Workflow perf requirements |
| `gascity-otel` receiver (webhook) | Moyenne | Monitoring | TraceLedger OTel export stable |
| `Session Lineage` UI view | Basse | L3 cockpit | CockpitProjection + frontend |

---

## Synthèse

| Catégorie | Total primitives | ✅ | 🔶 | ❌ |
|---|---|---|---|---|
| Orchestration | 7 | 6 | 1 | — |
| Observabilité | 5 | 5 | — | — |
| Packs / Gouvernance | 6 | 4 | 1 | 1 |
| Interop / Bridges | 4 | 4 | — | — |
| Mémoire | 4 | 4 | — | — |
| Code graph | 3 | 3 | — | — |
| **Total** | **29** | **26** | **2** | **1** |

**26/29 primitives utiles Gastownhall ont une destination Grimoire claire et implémentée (90 %).**

Le 1 ❌ (Wasteland/federation) est explicitement reporté hors scope noyau.
Les 2 🔶 (Hot State Redis, Marketplace déploiement) ont leur schéma, pas leur déploiement.

---

## Gate M1 — Validation

- [x] Chaque primitive utile a une destination Grimoire nommée
- [x] Vocabulaire Grimoire canonique utilisé (pas de copie brute Gastownhall)
- [x] Statut d'implémentation traçable par module
- [x] Backlog des adapters restants documenté
