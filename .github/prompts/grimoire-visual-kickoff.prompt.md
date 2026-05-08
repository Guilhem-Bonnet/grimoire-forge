---
description: 'Kickoff visuel one-prompt. Use when: create full DA, UX/UI package, logo direction, web animation plan, and multi-format visual assets in a governed flow.'
agent: 'grimoire-master'
created: '2026-04-14'
status: 'Experimental'
owner: 'grimoire-master'
capability: 'visual-kickoff'
evidence: '_grimoire-runtime-output/planning-artifacts/plan-flow-agentique-visuel-ultra.md'
---

# Grimoire Visual Kickoff

## Why This Is A Prompt

This artifact is a user-facing kickoff contract for manual execution from one request.
Reusable multi-step operational logic remains in the `grimoire-visual-orchestration` skill.

## Context

This workflow launches a full visual pipeline from one user request and returns a unified visual package.

## Pre-conditions

1. Load `{project-root}/_grimoire-runtime/bmm/config.yaml` and store session variables.
2. Read `{project-root}/grimoire-game-assets/STYLE_GUIDE.md` and `{project-root}/grimoire-game-assets/README.md` when 2D assets are in scope.
3. If markdown files are created or edited, load documentation standards before writing.

## Mandatory Question Batch

Ask one compact batch before generation:

1. What is the first user action the interface must support?
2. Who is the primary audience and domain context?
3. What style mood do you want (3 adjectives), and what must be avoided?
4. What are the 3 priority information blocks on first view?
5. What role should animation play?
6. Which visual outputs are required (logo, UI, icons, assets, FX, storyboards)?
7. Which export formats are required (png, jpg, svg, gif, css, js)?
8. What are the technical constraints (stack, performance, target platforms)?

If the user is non-designer, reformulate questions in plain language and offer options.

## Steps

1. Build `visual-brief.md` from answers.
2. Produce `brand-board.md` with palette, typography, and logo direction.
3. Produce `ux-map.md` with IA, hierarchy, and navigation map.
4. Produce `motion-spec.md` with choreography, timing, and reduced-motion fallback.
5. Produce `assets-manifest.csv` for required visual assets and animation sheets.
6. Produce implementation snippets in `implementation-pack/`.
7. Produce `proof-pack.md` with checks, open risks, and explicit assumptions.
8. Store visual captures in `_grimoire-runtime-output/implementation-artifacts/visual-evidence/` and update `retention-manifest.json` (default TTL 14 days).
9. Enforce visual evidence minimum set: at least 3 captures, including `desktop` and `mobile` viewports, and at least 2 distinct interaction states.
10. Require `ticket_id` for each delivery scope and for every capture entry in `retention-manifest.json`.
11. In `proof-pack.md`, include a mandatory section `## Non-regression visuelle` with explicit pass marks (`PASS` or checked checklist items).

## Agents Involved

- `ux-designer` for IA and interaction structure.
- `art-director` for DA, brand direction, and visual quality.
- `dev` for motion implementation and integration snippets.

## Output Format

1. Visual brief.
2. Brand board.
3. UX map.
4. Motion spec.
5. Assets manifest.
6. Implementation pack.
7. Proof pack.

## Success Criteria

- User receives coherent visual direction from one request.
- Outputs are implementation-ready and governance-aligned.
- Accessibility and performance constraints are explicit.
- Assets and motion are tied to user comprehension goals.

## Acceptance Authority

Final acceptance requires explicit pass marks in `proof-pack.md` for:

1. User approval (business intent).
2. UX approval (`ux-designer`, clarity and interaction model).
3. Art direction approval (`art-director`, style coherence).
4. Technical approval (`dev` + `qa`, accessibility and performance).