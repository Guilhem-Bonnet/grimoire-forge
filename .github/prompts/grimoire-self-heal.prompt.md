---
description: 'Diagnose and repair workflow failures (self-healing, immune scan, failure museum)'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

Diagnostique et répare les échecs du projet BMAD Grimoire :

1. `python3 {project-root}/bmad-custom-kit/framework/tools/self-healing.py --project-root {project-root}/bmad-custom-kit diagnose`
2. `python3 {project-root}/bmad-custom-kit/framework/tools/immune-system.py --project-root {project-root}/bmad-custom-kit scan`
3. `python3 {project-root}/bmad-custom-kit/framework/tools/failure-museum.py --project-root {project-root}/bmad-custom-kit list --last 5`

Identifie les causes racines, propose des réparations, et documente dans le failure museum si nouveau pattern.
