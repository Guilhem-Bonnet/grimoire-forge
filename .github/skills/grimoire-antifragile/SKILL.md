---
name: grimoire-antifragile
description: 'Assess BMAD Grimoire project resilience and anti-fragility. Use when: antifragile score, resilience check, how robust is the project, system health, failure analysis, early warning, stress test, project resilience, fragility assessment. Combines antifragile scoring, early warning system, and failure museum analysis.'
---

# Grimoire Antifragile Assessment

Deep resilience assessment: is the project learning from its failures, or just surviving them?

## When to Use

- After a difficult sprint or series of failures
- Periodic resilience review (monthly recommended)
- When the user asks "how robust is the project?", "antifragile score", or "failure analysis"
- Before architectural decisions that increase system complexity

## Background

Anti-fragility goes beyond robustness:
- **FRAGILE** (< 30) — System breaks and doesn't learn
- **ROBUST** (30-60) — System survives but doesn't improve
- **ANTIFRAGILE** (60-100) — System improves under stress

## Procedure

### Step 1 — Antifragile Score

```bash
python3 framework/tools/antifragile-score.py --project-root . --detail
```

This produces a composite score (0-100) based on:
- Failure-to-lesson conversion rate
- Decision traceability
- Contradiction resolution velocity
- Learning accumulation rate

### Step 2 — Early Warning Scan

```bash
python3 framework/tools/early-warning.py --project-root . scan
```

Check current alert levels:
- 🟢 NOMINAL — all clear
- 🟡 WATCH — trends to monitor
- 🔴 ALERT — intervention needed

### Step 3 — Entropy Analysis

```bash
python3 framework/tools/early-warning.py --project-root . entropy
```

Measures project complexity/disorder. High entropy = risk of cascading failures.

### Step 4 — Failure Museum Review

```bash
cat _bmad/_memory/failure-museum.md 2>/dev/null | head -100
```

Analyze:
- Are failures being catalogued with root causes?
- Do failures have associated lessons/corrections?
- Are similar failures recurring (patterns)?

### Step 5 — Trend Analysis

```bash
python3 framework/tools/early-warning.py --project-root . trends
```

Look for:
- Improving or degrading trends
- Phase transitions (regime changes)
- Acceleration of issues

### Step 6 — Resilience Report

```
## 🛡️ Antifragile Assessment

### Score: XX/100 — [FRAGILE/ROBUST/ANTIFRAGILE]

### Breakdown
| Dimension                    | Score | Trend |
|------------------------------|-------|-------|
| Failure → Lesson conversion  | X/25  | ↑/↓/→ |
| Decision traceability        | X/25  | ↑/↓/→ |
| Contradiction resolution     | X/25  | ↑/↓/→ |
| Learning accumulation        | X/25  | ↑/↓/→ |

### Early Warning
- Alert level: 🟢/🟡/🔴
- Entropy: X (low/medium/high)
- Key signals: ...

### Failure Patterns
- Total catalogued failures: N
- With lessons: N (X%)
- Recurring patterns: [list]

### Recommendations
1. [Most impactful improvement]
2. [Second priority]
3. [Third priority]

### Path to Antifragile
[Specific actions to move from current level to next level]
```

## Notes

- The antifragile score requires memory files to have content (learnings, decisions, failures)
- A new project will naturally score low — this is expected
- Focus on the TREND, not the absolute score
- All tools support `--json` for programmatic parsing
