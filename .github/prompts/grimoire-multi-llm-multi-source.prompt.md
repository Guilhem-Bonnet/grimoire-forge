---
description: 'Cadrer et operationaliser une strategie multi-LLM et multi-source'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load {project-root}/_grimoire-runtime/bmm/config.yaml and store ALL fields as session variables.
2. Read the canonical sources in this order:
   - {project-root}/docs/exploitation/strategie-exploitation-multi-llm-multi-source.md
   - {project-root}/docs/exploitation/connectivite-agentique-externe-agent-os-game-ui.md
   - {project-root}/docs/exploitation/matrice-capabilities-agent-os-game-ui.md
   - {project-root}/docs/exploitation/benchmark-github-agent-os-game-ui.md
   - {project-root}/_grimoire-runtime/_config/model-routing.yaml
   - {project-root}/grimoire-kit/framework/tools/llm-router.py
3. Interpret the user request using these modes:
   - `brainstorm` when the user wants alternatives, role split, or strategy
   - `playbook` when the user wants a concrete operating model for daily work
   - `execution-prep` when the user wants ordered tasks, config work, prompt work, evals, or proofs
4. Apply these invariants before writing anything:
   - Forge stays the source of truth for runs, memory, policy, and proof
   - Host transcripts are not durable truth
   - Treat any aggregated API as `provider abstraction`, `fallback`, or `eval` unless the user gives a stricter product contract
   - Prefer one mission pack reused across hosts over multiple host-specific briefs
   - Keep the primary strategy as `Copilot shell principal`, `Claude shell critique`, `GPT Codex shell code`, `API agregee fallback et evals` unless the repo context proves otherwise
5. Always produce these elements in French:
   - exactly 3 approaches with trade-offs
   - one firm recommendation grounded in the repo
   - a role matrix for Copilot, Claude, GPT Codex, and the aggregated API
   - a canonical mission pack with objective, scope, sources, constraints, expected output, and expected proof
   - ordered tasks with landing zones and verification gates
6. If the user asks to operationalize the strategy, update only the minimal relevant files under {project-root}/docs/exploitation, {project-root}/_grimoire-runtime-output/planning-artifacts, or {project-root}/.github/prompts.
7. When proposing follow-through work, prioritize in this order:
   - documentation canon
   - reusable prompt or workflow
   - plan artifact
   - config alignment
   - eval harness
8. End by naming the smallest executable next slice and the proof expected before calling it done.