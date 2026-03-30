---
description: 'Run pre-push validation (tests, lint, harmony check, preflight)'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

Checklist de validation avant push :

1. `cd {project-root}/grimoire-kit && python3 -m pytest tests/ -q --tb=line`
2. `cd {project-root}/grimoire-kit && python3 -m ruff check framework/tools/ tests/`
3. `python3 {project-root}/grimoire-kit/framework/tools/harmony-check.py --project-root {project-root}/grimoire-kit`
4. `python3 {project-root}/grimoire-kit/framework/tools/preflight.py --project-root {project-root}/grimoire-kit`

Résume le résultat : ✅ prêt à push, ou ❌ avec la liste des problèmes à corriger.
