---
description: 'Kickoff or continue Agent OS + Game UI planning from the exploitation corpus'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load {project-root}/_grimoire-runtime/bmm/config.yaml and store ALL fields as session variables
2. Read the operational corpus in this order:
   - {project-root}/docs/exploitation/distillat-source-agent-os-game-ui.md
   - {project-root}/docs/exploitation/matrice-capabilities-agent-os-game-ui.md
   - {project-root}/docs/exploitation/gouvernance-artefacts-agent-os-game-ui.md
   - {project-root}/docs/exploitation/matrice-statuts-artefacts-agent-os-game-ui.md
   - {project-root}/docs/exploitation/matrice-adoption-referentiels-agent-os-game-ui.md
   - {project-root}/docs/exploitation/checklist-design-review-host-bridge-agent-os-game-ui.md
   - {project-root}/docs/exploitation/workflow-kickoff-agent-os-game-ui.md
   - {project-root}/docs/exploitation/plan-maitre-agent-os-game-ui.md
   - {project-root}/docs/exploitation/backlog-brainstorm-agent-os-game-ui.md
3. Determine the working mode from the user request:
   - `kickoff` for a raw need, a new brainstorm batch, or a vague planning request
   - `continuation` when the user says `continu`, `reprend`, `continue`, or asks to push the existing plan further
   - `implementation-prep` when the user wants the next slice, executable tasks, tickets, or a delivery order
4. Apply these decision rules before writing anything:
   - Treat Forge as the source of truth and the Game UI as its operational surface
   - Use the distillate for invariants, hypotheses, and bounded open questions
   - Use the capability matrix to map every idea to an existing asset, a gap, or a parking-lot decision
   - Use the governance document to decide whether the need becomes a document, workflow, skill, instruction, hook, test, CI job, UI surface, or agent
   - Use the status matrix to distinguish supported lifecycle, `Parking lot`, and `Heritage` before naming a status in the output
   - Use the external reference matrix and the Host Bridge checklist before accepting any normative or host-specific claim into the plan
   - Update existing exploitation documents before creating a new artifact
5. Produce an actionable planning package in French:
   - current state already locked by the corpus
   - contradictions or gaps blocking the next wave
   - next 5 to 10 ordered tasks with dependencies and validation gates
   - minimal set of files to update or create
6. If the request requires documentation changes, update only the minimal relevant files under {project-root}/docs/exploitation and keep terminology aligned with the distillate, the matrix, and the master plan
7. If the request is `implementation-prep`, end by naming the smallest executable next slice and the evidence expected before calling it done