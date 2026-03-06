---
name: grimoire-innovate
description: 'Run the BMAD Grimoire innovation pipeline from idea to prototype. Use when: new idea, innovation, brainstorm to code, incubator, R&D cycle, experiment, explore alternative, what-if scenario, quantum branch, parallel timelines, prototype, seed idea. Combines incubator lifecycle, R&D engine, and quantum branching.'
---

# Grimoire Innovate

Full innovation pipeline: submit ideas, evaluate viability, run R&D cycles, explore in isolated branches.

## When to Use

- New idea that needs structured evaluation
- Running an innovation sprint
- When the user says "what if...", "let's experiment", "new idea", or "R&D"
- Evaluating competing approaches
- Exploring architectural alternatives safely

## Procedure

### Step 1 — Check Incubator Status

```bash
python3 framework/tools/incubator.py --project-root . status
```

See what ideas are already in the pipeline and their lifecycle stages:
- SEED → INCUBATING → VIABLE → HATCHED
- DORMANT (parked), DEAD (abandoned)

### Step 2 — Submit or Wake Idea

**New idea:**

```bash
python3 framework/tools/incubator.py --project-root . submit \
  --title "<idea title>" \
  --description "<detailed description>"
```

**Wake a dormant idea:**

```bash
python3 framework/tools/incubator.py --project-root . wake --id <IDEA-NNN>
```

### Step 3 — Viability Check

```bash
python3 framework/tools/incubator.py --project-root . viable --id <IDEA-NNN>
```

Evaluates:
- Alignment with project objectives
- Technical feasibility (dependencies satisfied?)
- Duplication with existing features
- Sponsor validation (at least one agent approved)

### Step 4 — R&D Cycle (for viable ideas)

**Quick evaluation:**

```bash
python3 framework/tools/r-and-d.py --project-root . cycle --quick
```

Runs harvest + evaluate phases only.

**Full cycle (7 phases):**

```bash
python3 framework/tools/r-and-d.py --project-root . cycle
```

Phases: HARVEST → EVALUATE → CHALLENGE → SIMULATE → IMPLEMENT → SELECT → CONVERGE

**Intensive training (multiple cycles):**

```bash
python3 framework/tools/r-and-d.py --project-root . train --epochs 3
```

Uses reinforcement learning to optimize innovation parameters across cycles.

### Step 5 — Quantum Branch (for exploration)

If the idea needs isolated experimentation:

**Fork a parallel timeline:**

```bash
python3 framework/tools/quantum-branch.py --project-root . fork --name "<experiment-name>"
```

**List active branches:**

```bash
python3 framework/tools/quantum-branch.py --project-root . list
```

**Compare branches:**

```bash
python3 framework/tools/quantum-branch.py --project-root . compare --branches main,<experiment-name>
```

**Merge successful experiment:**

```bash
python3 framework/tools/quantum-branch.py --project-root . merge --source <experiment-name>
```

**Prune failed experiment:**

```bash
python3 framework/tools/quantum-branch.py --project-root . prune --branch <experiment-name>
```

### Step 6 — Innovation Dashboard

```bash
python3 framework/tools/r-and-d.py --project-root . dashboard
```

### Step 7 — Report

```
## 💡 Innovation Pipeline Report

### Incubator Status
| Stage      | Count | Key Ideas              |
|------------|-------|------------------------|
| SEED       | N     | ...                    |
| INCUBATING | N     | ...                    |
| VIABLE     | N     | ...                    |
| DORMANT    | N     | ...                    |
| HATCHED    | N     | (completed)            |

### R&D Cycle Results
- Cycles run: N
- Ideas evaluated: N
- Surviving ideas: N
- Top innovation: <title> (fitness: X)

### Active Experiments (Quantum Branches)
| Branch | Purpose | Age | Status |
|--------|---------|-----|--------|
| ...    | ...     | Nd  | active/ready-to-merge |

### Recommendations
1. [Ideas ready for implementation]
2. [Branches ready to merge]
3. [Dormant ideas worth revisiting]
```

## Quick Mode

Fast idea-to-evaluation without branches:

```bash
python3 framework/tools/incubator.py --project-root . submit --title "<idea>" --description "<desc>"
python3 framework/tools/r-and-d.py --project-root . cycle --quick
```

## Notes

- Quantum branches are filesystem-level snapshots, not git branches
- R&D cycles use reinforcement learning — results improve over multiple runs
- Incubator prune will clean ideas that have been SEED for too long without evaluation
- All tools support `--json` for programmatic output
