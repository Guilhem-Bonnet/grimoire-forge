---
description: 'Audit memory system (memory-lint, freshness scoring, session chain, bridge status)'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

Run a deep audit of the BMAD memory system:

1. `python3 {project-root}/grimoire-kit/framework/tools/memory-lint.py --project-root {project-root}/grimoire-kit scan`
2. `python3 {project-root}/grimoire-kit/framework/tools/memory-lint.py --project-root {project-root}/grimoire-kit freshness`
3. `python3 {project-root}/grimoire-kit/framework/tools/session-lifecycle.py --project-root {project-root}/grimoire-kit chain --last 5`
4. `python3 {project-root}/grimoire-kit/framework/tools/grimoire-daemon.py --project-root {project-root}/grimoire-kit status`

Identifie les mémoires stales, les contradictions, et les problèmes de synchronisation. Propose des corrections.
