---
name: grimoire-health-check
description: 'Run a full BMAD Grimoire project health check. Use when: project audit, health check, sanity check, validate project, check project health, diagnose issues, preflight, harmony check, quality score, early warning. Combines 5 diagnostic tools into one unified report.'
---

# Grimoire Health Check

Full project health audit combining 5 diagnostic tools into a unified report.

## When to Use

- Before a major feature or sprint
- After significant refactoring
- When something "feels wrong" in the project
- Periodic health reviews
- When the user asks for a "health check", "audit", "diagnostic", or "sanity check"

## Procedure

Run each diagnostic tool from the project root (`bmad-custom-kit/`) and aggregate the results.

### Step 1 — Preflight Check

```bash
python3 framework/tools/preflight-check.py --project-root .
```

Detects environment issues BEFORE they cause failures: missing files, broken references, invalid configs.

### Step 2 — Harmony Check

```bash
python3 framework/tools/harmony-check.py --project-root .
```

Detects architectural dissonances: inconsistent naming, orphan files, structural drift.

### Step 3 — Memory Lint

```bash
python3 framework/tools/memory-lint.py --project-root .
```

Validates memory coherence: contradictions, duplicates, chronological consistency, freshness.

### Step 4 — Early Warning

```bash
python3 framework/tools/early-warning.py --project-root . scan
```

Detects problems BEFORE they become crises: error velocity, entropy, risk concentration, stagnation.

### Step 5 — Quality Score

```bash
python3 framework/tools/quality-score.py --project-root .
```

Evaluates overall quality across multiple dimensions.

### Step 6 — Aggregate Report

Present a unified health dashboard:

```
## 🏥 Grimoire Health Report

| Diagnostic          | Status | Details          |
|---------------------|--------|------------------|
| Preflight           | ✅/⚠️/❌ | N issues found  |
| Harmony             | ✅/⚠️/❌ | N dissonances   |
| Memory Coherence    | ✅/⚠️/❌ | N issues found  |
| Early Warning       | 🟢/🟡/🔴 | Alert level     |
| Quality Score       | XX/100  | Score breakdown |

### Recommendations
- Priority 1: ...
- Priority 2: ...
```

## Interpretation Guide

- **All green**: Project is healthy, proceed confidently
- **Yellow/warnings**: Address before next major change
- **Red/critical**: Stop and fix these before continuing work

## Notes

- All tools are stdlib-only Python, no external dependencies needed
- Each tool supports `--json` flag for machine-readable output
- Run from the `bmad-custom-kit/` directory (where `framework/tools/` lives)
