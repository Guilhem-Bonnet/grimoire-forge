---
description: 'Bootstrap a new session with full context (session chain, shared context, git status)'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

Bootstrap une nouvelle session BMAD Grimoire :

1. Lis {project-root}/bmad-custom-kit/_bmad/_memory/shared-context.md pour le contexte projet
2. `python3 {project-root}/bmad-custom-kit/framework/tools/session-lifecycle.py --project-root {project-root}/bmad-custom-kit chain --last 3`
3. `cd {project-root}/bmad-custom-kit && git log --oneline -10`
4. `python3 {project-root}/bmad-custom-kit/framework/tools/preflight.py --project-root {project-root}/bmad-custom-kit`

Présente un résumé concis : contexte actuel, dernières sessions, état git, et santé projet. Identifie ce qui reste à faire.
