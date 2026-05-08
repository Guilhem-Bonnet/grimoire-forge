---
title: Backlog agentique unifie
description: Backlog unique du nouveau projet Grimoire Agent OS, adapte aux agents, hooks, guardrails et preuves.
author: Codex
date: 2026-05-08
---

# Backlog agentique unifie

## Convention

Prefixe unique : `GAO`.

| Prefixe | Domaine |
| --- | --- |
| `GAO-A` | Source de verite et nettoyage |
| `GAO-B` | Runtime Kernel |
| `GAO-C` | Mission Ledger |
| `GAO-D` | Workflow Instances |
| `GAO-E` | Hooks et guardrails |
| `GAO-F` | Pack Registry et fusion externe |
| `GAO-G` | Memory OS et Code Graph |
| `GAO-H` | Mission Board Cockpit |
| `GAO-I` | Host Bridge et interop |
| `GAO-J` | Observabilite, evals, red team |
| `GAO-K` | Distribution, docs, ecosysteme |

## Vague A - Unifier et rendre executable

| ID | Titre | Surface | Dep | Evidence | Hooks/gates |
| --- | --- | --- | --- | --- | --- |
| `GAO-A001` | Declarer le plan directeur comme source active | Forge | aucune | README + index actualises | `PostToolUse`, doc drift |
| `GAO-A002` | Classer les anciens plans dans le registre | Forge | `GAO-A001` | registre complet | doc drift |
| `GAO-A003` | Migrer les IDs GTA/GM/anciens plans vers GAO | Forge | `GAO-A002` | mapping idempotent | verification docs |
| `GAO-B001` | Spec `RunEvent` canonique | grimoire-kit | aucune | schema + tests parsing | contract gate |
| `GAO-B002` | Spec `Checkpoint` et reprise | grimoire-kit | `GAO-B001` | tests resume/idempotence | strict evidence |
| `GAO-C001` | Spec `MissionTask` et dependances | grimoire-kit | `GAO-A001` | schema + fixtures | ledger gate |
| `GAO-C002` | Import ancien backlog docs vers ledger candidate | Forge + kit | `GAO-C001` | import dry-run | no mutation sans proof |
| `GAO-E001` | Revue des hooks promus et modes `shadow/canary/enforced` | Forge | aucune | rapport hook registry | hook governance audit |
| `GAO-E002` | Policy de blocage `done` sans evidence | Forge + kit | `GAO-C001` | test negatif | verification gate |
| `GAO-H001` | Projection board depuis Mission Ledger minimal | grimoire-game | `GAO-C001` | test view/read model | UI projection gate |

## Vague B - Absorber Gastownhall proprement

| ID | Titre | Surface | Dep | Evidence | Hooks/gates |
| --- | --- | --- | --- | --- | --- |
| `GAO-F001` | Spec `pack.yaml` Grimoire | grimoire-kit | `GAO-A001` | schema + exemples | pack policy |
| `GAO-F002` | Convertisseur `pack.toml` Gas City en `pack.yaml` | grimoire-kit | `GAO-F001` | fixtures gascity-packs | pack activation disabled |
| `GAO-F003` | Doctor checks pack -> doctor global | grimoire-kit | `GAO-F001` | test doctor aggregation | read-only gate |
| `GAO-F004` | Importer projet CrewAI vers pack Grimoire experimental | grimoire-kit | `GAO-F001` | fixtures `agents.yaml`, `tasks.yaml`, `crew.py` | tools deny par defaut |
| `GAO-D001` | Traduction formula/order en recipe/order Grimoire | grimoire-kit | `GAO-B001`, `GAO-F001` | spec + fixture | workflow gate |
| `GAO-D003` | Mapper CrewAI Flow vers Recipe Grimoire | grimoire-kit | `GAO-D001`, `GAO-F004` | graphe `start/listen/router` + state schema | checkpoint gate |
| `GAO-C003` | Import/export Beads JSONL | grimoire-kit | `GAO-C001` | roundtrip fixtures | ledger idempotence |
| `GAO-C004` | Query `ready` avec blockers | grimoire-kit | `GAO-C001` | tests dependencies | no blocked ready |
| `GAO-I001` | Capability Manifest provider | grimoire-kit | `GAO-B001` | schema + examples Codex/Claude/Copilot | host policy |
| `GAO-J001` | Mapping metriques Gas City OTEL vers OTel Grimoire | grimoire-kit | `GAO-B001` | mapping doc + exporter stub | privacy gate |

## Vague C - Durable runtime et memoire

| ID | Titre | Surface | Dep | Evidence | Hooks/gates |
| --- | --- | --- | --- | --- | --- |
| `GAO-B003` | Runtime Kernel v1 pour run/checkpoint/replay | grimoire-kit | `GAO-B001`, `GAO-B002` | tests replay | strict evidence |
| `GAO-D002` | WorkflowInstance store | grimoire-kit | `GAO-B003`, `GAO-D001` | tests resume/abort | no silent stall |
| `GAO-G001` | Collections Memory OS liees tasks/evidence | grimoire-kit | `GAO-C001` | memory status + fixtures | memory provenance |
| `GAO-G002` | Hot memory locale + Redis optionnel | grimoire-kit | `GAO-G001` | fallback local | no Redis source of truth |
| `GAO-G003` | Code graph minimal Python/TS | grimoire-kit | `GAO-G001` | symbols + tests links | code graph gate |
| `GAO-G004` | Mapper CrewAI Knowledge et Memory scopes vers Memory OS | grimoire-kit | `GAO-G001`, `GAO-F004` | source refs + freshness + scope tests | memory provenance |
| `GAO-E003` | `SubagentStop` output evaluator | Forge + kit | `GAO-E001` | score events | canary before enforce |
| `GAO-E004` | `PreCompact` learning candidate gate | Forge + kit | `GAO-G001` | dedupe tests | no auto memory spam |

## Vague D - Cockpit et interop

| ID | Titre | Surface | Dep | Evidence | Hooks/gates |
| --- | --- | --- | --- | --- | --- |
| `GAO-H002` | Vue Workflow Instance et Checkpoints | grimoire-game | `GAO-D002` | UI test | projection only |
| `GAO-H003` | Vue Evidence Pack et Policy Verdict | grimoire-game | `GAO-E002` | UI test | no hidden state |
| `GAO-H004` | Vue Packs, doctor et activation | grimoire-game | `GAO-F003` | UI test | pack policy |
| `GAO-I002` | MCP parity contract | grimoire-kit | `GAO-I001` | contract tests | same business contract |
| `GAO-I003` | A2A AgentCard experimental | grimoire-kit | `GAO-I001` | schema + sample | external policy |
| `GAO-I004` | Adapter CrewAI comme ExternalWorkflowRunner experimental | grimoire-kit | `GAO-D003`, `GAO-I001` | trace CrewAI -> RunEvent | external runner policy |
| `GAO-J002` | Trace/Eval Ledger minimal | grimoire-kit | `GAO-B003` | trace fixtures | privacy gate |
| `GAO-J004` | Adapter patterns CrewAI test/train vers Eval Ledger | grimoire-kit | `GAO-J002`, `GAO-F004` | eval report + learning candidate | no opaque prompt patch |

## Vague E - Distribution et ecosysteme

| ID | Titre | Surface | Dep | Evidence | Hooks/gates |
| --- | --- | --- | --- | --- | --- |
| `GAO-K001` | Guide quickstart Grimoire Agent OS | grimoire-kit docs | `GAO-B003`, `GAO-C001` | docs + command proof | doc drift |
| `GAO-K002` | Guide creation pack gouverne | grimoire-kit docs | `GAO-F001` | docs + sample pack | pack policy |
| `GAO-K003` | Marketplace verifie experimental | grimoire-kit | `GAO-F002`, `GAO-F003` | catalog + lock | security critical |
| `GAO-K004` | Playbook ecosysteme Grimoire-first | Forge | `GAO-K001` | doc playbook | claims proof |
| `GAO-J003` | Red-team harness agentique | grimoire-kit | `GAO-E002`, `GAO-F001` | unsafe pack/tool/memory tests | security critical |
| `GAO-F005` | Importer catalogues de skills vers Pack Registry | grimoire-kit | `GAO-F001` | sample skill catalog + trust verdict | skill supply-chain |
| `GAO-G005` | Construire provider Code Graph unifie | grimoire-kit | `GAO-G003` | graph fixtures CodeGraphContext/Graphify | code graph gate |
| `GAO-G006` | Ajouter compression contexte bornee | grimoire-kit | `GAO-G001` | original ref + compressed ref + quality check | no proof compression |
| `GAO-J005` | Construire red-team harness agentique | grimoire-kit | `GAO-J003` | prompt/tool/memory attack fixtures | security critical |
| `GAO-H005` | Compiler inspiration board/visual builders vers cockpit | grimoire-game | `GAO-H001` | UI decision matrix | projection only |
| `GAO-I005` | Ajouter external runners experimentaux | grimoire-kit | `GAO-I001`, `GAO-B003` | runner adapters in disabled mode | external runner policy |
| `GAO-K005` | Construire documentation enseignement Agent OS | docs | `GAO-K001` | teaching guide indexed | doc drift |

## Taches interdites sans prealable

| Tache | Pourquoi elle est bloquee |
| --- | --- |
| Creer un nouveau board comme source de verite | Le board doit etre projection du ledger. |
| Activer un pack Gas City converti avec commandes mutatrices | Il faut policy, lock et doctor. |
| Ajouter federation/commons dans le noyau | Il faut Pack Registry, Evidence et Trust gates. |
| Ajouter Redis comme prerequis | Redis est hot state optionnel. |
| Ajouter Dolt comme backend obligatoire | Beads inspire le ledger, il ne definit pas le noyau Grimoire. |
| Promouvoir un hook heuristique en enforced | Blocage seulement sur preuve deterministe. |
| Fermer d'anciens plans par suppression brute | Migration et registre d'abord. |
