---
name: grimoire-dream
description: 'Run BMAD Grimoire dream consolidation and insight pipeline. Use when: dream mode, consolidate learnings, off-session insights, what did we learn, cross-domain patterns, generate insights, emerging patterns, stigmergy signals, dream journal. Runs dream analysis, deposits stigmergy signals, and optionally seeds incubator with actionable ideas.'
---

# Grimoire Dream

Off-session consolidation pipeline: mine cross-domain insights from memory, deposit signals, seed ideas.

## When to Use

- End of a work session (post-session consolidation)
- After a sprint or milestone
- When the user asks "what did we learn?", "any emerging patterns?", or "dream mode"
- Periodic knowledge distillation (weekly recommended)

## Procedure

### Step 1 — Dream Analysis

Run the full dream consolidation:

```bash
python3 framework/tools/dream.py --project-root .
```

This reads learnings, decisions, trace, failure museum, and shared-context, then produces cross-domain insights that no single agent would have formulated.

Review the output: `_bmad-output/dream-journal.md`

### Step 2 — Validate Insights (no hallucination)

```bash
python3 framework/tools/dream.py --project-root . --validate
```

Ensures generated insights are grounded in actual data, not hallucinated patterns.

### Step 3 — Sense Current Stigmergy Landscape

```bash
python3 framework/tools/stigmergy.py --project-root . landscape
```

See what signals are already active before depositing new ones. Avoid duplicating existing signals.

### Step 4 — Emit Stigmergy Signals

For each significant insight, deposit a pheromone signal:

```bash
python3 framework/tools/stigmergy.py --project-root . emit --type OPPORTUNITY --location "<domain>" --text "<insight summary>" --agent dream
```

Signal types:
- `OPPORTUNITY` (green) — improvement potential discovered
- `ALERT` (red) — risk or debt pattern emerging
- `NEED` (blue) — review or expertise needed

### Step 5 — Seed Incubator (Optional)

For actionable insights that could become features:

```bash
python3 framework/tools/dream.py --project-root . --incubate
```

This bridges validated insights into the incubator as SEED ideas, filtered by confidence threshold.

### Step 6 — Summary

Present a consolidated brief:

```
## 🌙 Dream Consolidation Report

### Insights Generated: N
| # | Insight | Sources | Confidence | Action |
|---|---------|---------|------------|--------|
| 1 | ...     | 2+      | 0.X        | signal/seed/note |

### Stigmergy Signals Deposited: N
- 🟢 OPPORTUNITY: ...
- 🔴 ALERT: ...

### Ideas Seeded in Incubator: N
- SEED: ...

### Key Takeaway
[Most important cross-domain pattern discovered]
```

## Quick Mode

For a rapid dream without full pipeline:

```bash
python3 framework/tools/dream.py --project-root . --quick
```

This runs dream analysis only, skipping stigmergy and incubator steps.

## Notes

- Dream is read-only by default — insights go to `dream-journal.md`, not memory files
- `--incubate` is the bridge to actionable outcomes
- Best run when fresh context is loaded (after session bootstrap)
