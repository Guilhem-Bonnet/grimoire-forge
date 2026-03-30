---
description: 'Check token budget status and auto-prune if needed'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

Vérifie le budget token et optimise si nécessaire :

1. `python3 {project-root}/grimoire-kit/framework/tools/token-budget.py --project-root {project-root}/grimoire-kit check`
2. Si utilisation > 60%, lance un preview de résumé :
   `python3 {project-root}/grimoire-kit/framework/tools/context-summarizer.py --project-root {project-root}/grimoire-kit preview`
3. Si utilisation > 80%, propose l'auto-prune :
   `python3 {project-root}/grimoire-kit/framework/tools/token-budget.py --project-root {project-root}/grimoire-kit enforce --dry-run`

Présente le statut avec barre visuelle, breakdown par priorité, et tendance historique.
