# R10 Governed cockpit report

## Scope

This cockpit is a read-only projection for Grimoire Forge R10. It summarizes governed sources and runtime event surfaces, but it does not update task state, memory state, gates, scores, risks or waivers.

## Input status

| Input | Status | Source of truth | Notes |
|---|---|---|---|
| Task board | declared | `_grimoire/standard/task-board.yaml` | R7, R8, R9 and R10 tasks expose evidence refs. |
| Memory OS policy | declared | `_grimoire/standard/memory-policy.yaml` | Redis is optional hot memory; Weaviate, Neo4j and SQLite remain durable targets. |
| Compliance score | declared | `_grimoire/standard/compliance-score.yaml` | Adds an `observability_cockpit` dimension. |
| Runtime journal | advisory | `_grimoire-output/events/runtime-journal.jsonl` | Consumed only after redaction and evidence correlation. |
| Evidence packs | declared | `_grimoire-output/evidence/**/evidence-pack.md` | R8/R9/R10 evidence drives review status. |

## Views

| View | Current R10 status | Next hardening step |
|---|---|---|
| Memory OS health | Contract-level view declared | Connect live Redis/Weaviate/Neo4j/SQLite health events in Kit runtime. |
| Task and evidence overlay | Board/evidence references declared | Add machine-readable evidence gap report. |
| Governance status | Score/gate inputs declared | Persist score trend snapshots as runtime events. |

## Guardrails

- Cockpit exports are read-only and reproducible.
- Runtime logs are advisory unless backed by evidence packs.
- Secrets, credentials, personal data and regulated data are forbidden in cockpit exports.
- Legacy visual/cockpit assets remain references until their input contracts are normalized.
