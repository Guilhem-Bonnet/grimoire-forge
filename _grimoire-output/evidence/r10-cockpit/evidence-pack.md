# R10 Cockpit and governed observability - Evidence Pack

## Summary

- Task id: `r10-cockpit`
- Profile: `governed`
- Outcome: Forge now has a governed observability contract and a read-only cockpit report.
- Final state: review

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Observability policy | `_grimoire/standard/observability-policy.yaml` | Grimoire Forge | Declares cockpit inputs, outputs, views, redaction and non-authoritative constraints. |
| Runtime rules | `_grimoire/standard/rule-packs.yaml` | Grimoire Forge | Adds read-only cockpit, declared inputs and no-secret-export rules. |
| Pattern catalog | `_grimoire/standard/pattern-catalog.yaml` | Grimoire Forge | Adds governed observability cockpit pattern. |
| Cockpit report | `_grimoire-output/evidence/r10-cockpit/cockpit-report.md` | Grimoire Forge | Provides a reproducible R10 projection from governed sources. |
| Context bundle | `_grimoire-output/context/r10-cockpit/context-bundle.yaml` | Grimoire Forge | Records selected/excluded sources and Memory OS constraints. |
| Decision trace | `_grimoire-output/decisions/r10-cockpit/decision-trace.yaml` | Grimoire Forge | Records why legacy cockpit/runtime outputs are not authoritative. |
| Public docs | `docs/observability-cockpit.md` | Grimoire Forge | Documents R10 cockpit rules for maintainers. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Governed profile verify | `npm run standard:verify -- --profile governed` | pass | Confirms required governed artifacts stay valid. |
| Governed profile audit | `npm run standard:audit -- --profile governed` | pass | Confirms no standard errors or warnings. |
| Docs strict build | `npm run docs:build` | pass | Confirms the cockpit documentation is published in the nav. |
| Diff hygiene | `git diff --check` | pass | Confirms whitespace-safe changes. |

## Controls

| Control family | Applied? | Evidence | Gap |
|---|---:|---|---|
| Observability | yes | `observability-policy.yaml`, `governed-observability-cockpit` | Live dashboard generation remains future work. |
| Security | yes | `observability.no-secret-export` | Automated redaction scan is not yet wired to CI. |
| Runtime | partial | `runtime_journal` declared as advisory input | Event schema normalization remains R10+ Kit work. |
| Governance | yes | Cockpit is explicitly non-authoritative | Score trend persistence is future work. |

## Completion statement

R10 is acceptable for review when Forge can publish a reproducible cockpit report from declared artifacts while preserving standard artifacts, evidence packs and runtime events as the only authoritative inputs.
