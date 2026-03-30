---
description: 'Run dream consolidation pipeline (off-session insights, stigmergy signals, incubator seeds)'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

Lance le pipeline de consolidation dream BMAD Grimoire :

1. `python3 {project-root}/grimoire-kit/framework/tools/dream.py --project-root {project-root}/grimoire-kit analyze`
2. `python3 {project-root}/grimoire-kit/framework/tools/dream.py --project-root {project-root}/grimoire-kit analyze --incubate`
3. Lis les signaux stigmergy récents :
   `python3 {project-root}/grimoire-kit/framework/tools/stigmergy.py --project-root {project-root}/grimoire-kit read --type INSIGHT --last 5`

Synthétise les patterns cross-domaine, les idées émergentes, et les seeds incubateur.
