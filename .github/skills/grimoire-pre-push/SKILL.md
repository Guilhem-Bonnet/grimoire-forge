---
name: grimoire-pre-push
description: 'Pre-push validation checklist for BMAD Grimoire Kit. Use when: before pushing, pre-push check, validate before commit, pre-commit, ready to push, CI check, final validation, run all checks. Runs tests, lint, harmony check, and preflight in sequence.'
---

# Grimoire Pre-Push Validation

Complete validation checklist before pushing code. Catches issues locally before they hit CI.

## When to Use

- Before `git push`
- Before submitting a PR
- After completing a feature or fix
- When the user says "ready to push", "pre-push", "validate everything", or "run all checks"

## Procedure

All commands run from the `grimoire-kit/` directory.

### Step 1 — Test Suite

```bash
python3 -m pytest tests/ -q --tb=short
```

**Expected**: All tests pass. If failures occur, fix them before continuing.

**On failure**: Read the test output, identify the failing test, and fix the issue. Re-run only the failing tests to confirm the fix, then re-run the full suite.

### Step 2 — Ruff Lint (new issues only)

```bash
python3 -m ruff check framework/tools/ tests/ --select E,F,W --no-fix 2>&1 | head -30
```

**Note**: Some pre-existing lint issues (I001, F401, UP017) are known. Focus on NEW issues only — errors in files modified since last commit:

```bash
git diff --name-only HEAD | xargs -I{} python3 -m ruff check {} --select E,F,W --no-fix 2>/dev/null
```

### Step 3 — Harmony Check

```bash
python3 framework/tools/harmony-check.py --project-root .
```

**Expected**: No critical dissonances. Warnings are acceptable.

### Step 4 — Preflight Check

```bash
python3 framework/tools/preflight-check.py --project-root .
```

**Expected**: All preflight checks pass.

### Step 5 — Git Status Review

```bash
git status --short
git diff --stat
```

Verify:
- No unintended files staged
- All intended changes are committed
- No sensitive files (keys, tokens, .env)

### Step 6 — Report

```
## ✅ Pre-Push Validation

| Check          | Status | Detail              |
|----------------|--------|---------------------|
| Tests          | ✅/❌  | NNNN passed, N failed |
| Lint (new)     | ✅/⚠️  | N new issues        |
| Harmony        | ✅/⚠️  | N dissonances       |
| Preflight      | ✅/❌  | N issues            |
| Git status     | ✅/⚠️  | N files changed     |

### Verdict: READY / NOT READY
```

**READY** = all green. Push confidently.
**NOT READY** = fix issues first, then re-run this skill.

## Quick Mode

If the user says "quick check" or time is limited, run only Steps 1 and 2 (tests + lint).
