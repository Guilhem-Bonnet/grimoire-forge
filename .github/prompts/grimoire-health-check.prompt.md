---
description: 'Run full project health check (preflight, harmony, memory-lint, early-warning, quality-score)'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

Run a comprehensive health check on the BMAD Grimoire project using these tools in sequence:

1. `python3 {project-root}/grimoire-kit/framework/tools/preflight.py --project-root {project-root}/grimoire-kit`
2. `python3 {project-root}/grimoire-kit/framework/tools/harmony-check.py --project-root {project-root}/grimoire-kit`
3. `python3 {project-root}/grimoire-kit/framework/tools/memory-lint.py --project-root {project-root}/grimoire-kit scan`
4. `python3 {project-root}/grimoire-kit/framework/tools/early-warning.py --project-root {project-root}/grimoire-kit scan`
5. `python3 {project-root}/grimoire-kit/framework/tools/quality-score.py --project-root {project-root}/grimoire-kit`

Présente un rapport unifié en français avec un score global et les actions prioritaires.
