# R8 Redis hot memory — Evidence Pack

## Summary

- Task id: `r8-redis-adapter`
- Profile: `governed`
- Outcome: Redis is now treated as an optional hot-memory layer, not as a durable source of truth.
- Final state: review

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Kit Redis adapter branch | `Grimoire-kit@work/r8-redis-hot-memory-20260529` | Grimoire Kit | Adds `RedisHotMemory`, TTL payloads, leases, namespaced publishing, health status, docs and unit tests. |
| Kit Redis adapter commit | `be1c0971` | Grimoire Kit | Implements optional Redis hot-memory runtime surface. |
| Forge post-merge baseline branch | `Grimoire-Forge@work/r8-memory-runtime-20260529` | Grimoire Forge | Starts from merged R7 `main` and keeps Forge-only checkout self-contained. |
| Memory policy update | `_grimoire/standard/memory-policy.yaml` | Grimoire Forge | Declares Redis optional activation, TTL/lease defaults, install extra and soft-fail behavior. |
| Context/evidence gate update | `_grimoire/standard/context-contract.yaml`, `_grimoire/standard/evidence-gates.yaml` | Grimoire Forge | Requires hot-memory policy evidence and records degradation as non-destructive. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Forge governed profile | `/mnt/Travail/Projets/Dev/Grimoire-kit-agentic-standard-bridge/.venv/bin/grimoire standard verify` | pass | `0 error(s), 0 warning(s)` after Forge-only checkout stabilization. |
| Forge docs strict build | `npm run docs:build` | pass | MkDocs strict build succeeds after nav drift cleanup. |
| Kit Redis unit tests | `.venv/bin/python -m pytest tests/unit -q` | pass | Full unit suite passed after Redis hot-memory additions. |
| Kit targeted lint | `.venv/bin/ruff check ...` | pass | Redis hot-memory modules and tests lint clean. |
| Kit targeted typing | `.venv/bin/mypy --strict ...` | pass | Redis hot-memory modules and tests type-check clean. |
| Kit docs strict build | `.venv/bin/mkdocs build --strict` | pass | Documentation includes Redis hot-memory role and config. |

## Controls

| Control family | Applied? | Evidence | Gap |
|---|---:|---|---|
| Durability | yes | Redis failure mode is soft-fail and non-authoritative | Redis data is intentionally not a durable evidence store. |
| Runtime | partial | Kit exposes Redis adapter and Memory OS status | Forge does not require a live Redis service in CI yet. |
| Governance | yes | Evidence gates require hot-memory policy and degradation record | Release gate remains soft until Redis service policy is finalized. |
| Security | yes | Redis namespace is project-scoped and TTL-bound | Secrets must still be redacted before any hot-memory write. |

## Completion statement

R8 is acceptable for Forge review when the governed standard stays green without Redis, and when enabling Redis only upgrades the hot-memory layer status instead of changing durable truth semantics.
