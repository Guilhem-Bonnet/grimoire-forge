# R9 Hooks, skills and rules taxonomy - Evidence Pack

## Summary

- Task id: `r9-hooks-skills`
- Profile: `governed`
- Outcome: Forge hooks and skills are now classified into promotion lanes with explicit rule and pattern links.
- Final state: review

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Hook/source inventory | `.github/hooks`, `.github/hooks/scripts` | Grimoire Forge | Identified gateway, memory, terminal, doc-drift, subagent and incubator hooks. |
| Skill/source inventory | `.github/skills` | Grimoire Forge | Identified reusable engineering skills, Forge governance skills and visual/game incubator skills. |
| Governed hook taxonomy | `_grimoire/standard/hook-registry.yaml` | Grimoire Forge | Adds managed source lanes: core template candidates, Forge project pack and incubator. |
| Governed rules | `_grimoire/standard/rule-packs.yaml` | Grimoire Forge | Adds hot-memory degradation, gateway, destructive-tool and skill-classification rules. |
| Pattern catalog links | `_grimoire/standard/pattern-catalog.yaml` | Grimoire Forge | Adds Redis soft gate, hook gateway and skill classification patterns. |
| Context bundle | `_grimoire-output/context/r9-hooks-skills/context-bundle.yaml` | Grimoire Forge | Captures selected sources, exclusions, memory constraints and evidence requirements. |
| Decision trace | `_grimoire-output/decisions/r9-hooks-skills/decision-trace.yaml` | Grimoire Forge | Records why assets are classified instead of bulk-promoted into Kit. |

## Classification matrix

| Lane | Hooks | Skills | Promotion rule |
|---|---:|---:|---|
| Core template candidates | memory gate, terminal guard, doc drift, hook gateway | code review, security review, verification, writing plans, test architecture | Candidate for Kit only after generic config and tests exist. |
| Forge project pack | control surface, subagent context/trace, prompt submit, session start | dispatch engineer, memory audit, safety guards, session bootstrap, architecture docs | Stays Forge-governed until another project consumes the contract. |
| Incubator | docker helper, task-flow helper | pixel observatory, 2D asset pipeline, visual orchestration | Kept out of core until runtime contracts and evidence gates are stable. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Forge governed profile | `npm run check:standard` | pass | Uses `scripts/check-standard.sh`, which resolves a `grimoire` CLI that supports `standard`. |
| Forge docs strict build | `npm run docs:build` | pass | MkDocs strict build succeeds after R9 taxonomy changes. |

## Controls

| Control family | Applied? | Evidence | Gap |
|---|---:|---|---|
| Hook governance | yes | `hooks.must-use-gateway`, `hooks.gateway-required` | Gateway behavior remains shell-script based until promoted to Kit templates. |
| Skill governance | yes | `skills.classified-before-use`, `skills.require-classification` | Full skill metadata schema is still future Kit work. |
| Runtime safety | yes | `hooks.no-destructive-bypass`, `tools.terminal-guard` | Tool mediation needs CI/runtime event capture in R10. |
| Memory OS | yes | `memory.hot-degrades-safely`, `memory.hot-soft-gate` | Redis remains optional and non-authoritative. |

## Completion statement

R9 is acceptable for review when the governed profile verifies cleanly, the docs build strictly, and every hook/skill promotion path is classified before any move into Kit core.
