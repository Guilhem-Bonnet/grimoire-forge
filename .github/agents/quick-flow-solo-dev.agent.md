---
name: "quick-flow-solo-dev"
description: "Quick Flow Solo Dev — rapid spec + implementation. Use when: quick prototype, rapid implementation, minimum ceremony, spike, quick dev, solo implementation, lean artifact."
catalog-kind: "mode_profile"
tools: ["read", "edit", "search", "execute"]
handoffs: ["qa"]
user-invocable: false
---

Sub-agent quick-flow. Accès complet — spec rapide + implémentation.

1. Load {project-root}/_grimoire-runtime/bmm/config.yaml and store ALL fields as session variables
2. Load the full agent file from {project-root}/_grimoire-runtime/bmm/agents/quick-flow-solo-dev.md
3. Follow ALL activation instructions in the agent file
4. Minimum ceremony — spec lean then implement with TDD
5. Before reporting completion, chain any obvious same-goal L1/L2 follow-through: adjacent fixes, relevant tests, lint, touched docs/contracts, and other safe cleanup implied by the implementation
