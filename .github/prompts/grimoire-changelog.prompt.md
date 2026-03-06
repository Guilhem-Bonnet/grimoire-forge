---
description: 'Generate structured CHANGELOG from git history and session chain context'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

Génère un CHANGELOG structuré pour le projet BMAD Grimoire :

1. `cd {project-root}/bmad-custom-kit && git log --oneline --since="2 weeks ago"`
2. `python3 {project-root}/bmad-custom-kit/framework/tools/session-lifecycle.py --project-root {project-root}/bmad-custom-kit chain --last 10`
3. Lis {project-root}/bmad-custom-kit/CHANGELOG.md pour le format existant
4. Lis {project-root}/bmad-custom-kit/version.txt pour la version courante

Génère un CHANGELOG au format Keep a Changelog avec sections: Added, Changed, Fixed, Security. Inclus les liens de commits.
