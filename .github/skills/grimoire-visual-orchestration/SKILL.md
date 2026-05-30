---
name: grimoire-visual-orchestration
description: "One-prompt visual ops pipeline. Use when: full visual direction, DA creation, UI/UX package, logo and brand system, web animation choreography, multi-format asset generation."
created: "2026-04-14"
status: "Experimental"
owner: "grimoire-master"
capability: "visual-orchestration"
evidence: "_grimoire-runtime-output/planning-artifacts/plan-flow-agentique-visuel-ultra.md"
---

# Grimoire Visual Orchestration

Unified pipeline to convert one user prompt into a governed visual package:
direction artistique, UX map, brand kit, motion plan, and implementation-ready outputs.

## When to Use

- User asks for complete visual output from one prompt.
- User wants DA + UX/UI + logos + animations + assets in one run.
- User is non-designer and needs guided framing in plain language.
- Team needs repeatable visual quality gates before delivery.

## Mandatory Pre-brief

Before heavy generation, ask one batched clarification round covering:

1. Primary user goal and first action.
2. Audience profile and domain context.
3. Style mood (3 adjectives) and anti-goals.
4. Priority information and navigation behavior.
5. Motion role (guide, explain, reassure, celebrate).
6. Asset scope (logo, icon, character, FX, sprite, background).
7. Output formats (png, jpg, svg, gif, css, js).
8. Technical constraints (stack, performance budget, target devices).

If user is non-designer, reformulate each question with suggested options.

## Process

1. Build a canonical visual brief from the batched answers.
2. Split execution tracks:
   - Brand and logo system
   - UX information architecture and wireflow
   - Motion choreography and interaction mapping
   - 2D assets and animation sheets
   - Front implementation snippets
3. Consolidate all tracks into one visual package.
4. Run visual-first gates.
5. Deliver outputs with explicit status and proof notes.

## Visual-first Gates

- Clarity: first screen conveys where to look and what to do.
- Coherence: palette, type, icon language, and motion are aligned.
- Accessibility: contrast, focus visibility, keyboard paths, reduced motion.
- Performance: no obvious jank and bounded animation complexity.
- Operability: motion supports comprehension, not decoration.
- Governance: sources and claims are traceable.

## Validation Authority

- Primary approver: user (final acceptance).
- Design authority: `ux-designer` + `art-director` (coherence and usability).
- Technical authority: `dev` + `qa` (implementation feasibility, accessibility, performance).

A visual output is accepted only when all four authority angles are explicitly marked as passed in `proof-pack.md`.

## Evidence Retention

- Store screenshots and snapshots under `_grimoire-runtime-output/implementation-artifacts/visual-evidence/`.
- Maintain `retention-manifest.json` with for each capture: ticket_id, objective, source_tool, created_at, ttl_days, expires_at, viewport, state, and file path.
- Default retention is 14 days, unless a stricter project policy applies.
- Minimum capture threshold: 3 captures, including `desktop` and `mobile`, and at least 2 distinct states.
- Keep only captures linked to the current objective/ticket; purge obsolete captures after expiry.

## Output Contract

1. `visual-brief.md`
2. `brand-board.md`
3. `ux-map.md`
4. `motion-spec.md`
5. `assets-manifest.csv`
6. `implementation-pack/`
7. `proof-pack.md`

`proof-pack.md` must include `## Non-regression visuelle` with explicit pass markers (`PASS` or checked list).

## Agents Involved

- `ux-designer` for IA and navigation clarity.
- `art-director` for style coherence and visual signatures.
- `dev` for implementation-ready motion and asset integration.
- `tech-writer` only when documentation artifacts are updated.

## Success Criteria

- One prompt can trigger the full visual package lifecycle.
- User receives a guided flow without design jargon overload.
- Delivery is consistent, testable, and reusable.
- No output is marked final without passing visual-first gates.