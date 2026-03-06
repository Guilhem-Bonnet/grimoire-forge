---
name: grimoire-session-bootstrap
description: 'Bootstrap a new BMAD Grimoire session with full context. Use when: start session, new session, session bootstrap, load context, resume work, what happened last time, session recap, catch me up, continue where we left off. Loads session chain, checks project health, restores working context.'
---

# Grimoire Session Bootstrap

Initialize a new working session by loading historical context and checking project readiness.

## When to Use

- Starting a new conversation/session on the project
- Resuming after a break
- When the user says "start session", "catch me up", "what happened last time", or "resume"
- At the beginning of any significant work block

## Procedure

### Step 1 — Load Session Chain

Read the session chain to understand recent history:

```bash
cat _bmad/_memory/session-chain.jsonl 2>/dev/null | tail -5
```

If it exists, parse the last 3-5 entries and summarize:
- What was accomplished in recent sessions
- What was planned but not completed
- Key decisions made
- Any blockers or open questions

If it doesn't exist, note that this is the first tracked session.

### Step 2 — Check Shared Context

```bash
cat _bmad/_memory/shared-context.md 2>/dev/null | head -50
```

Load cross-agent shared knowledge to understand current project state.

### Step 3 — Quick Preflight

```bash
python3 framework/tools/preflight-check.py --project-root . 2>&1 | tail -20
```

Ensure the project is in a workable state. Flag any blockers immediately.

### Step 4 — Check Git State

```bash
git status --short
git log --oneline -5
```

Understand:
- Are there uncommitted changes (in-progress work)?
- What were the last commits (recent activity)?
- Is the branch clean or dirty?

### Step 5 — Check Active Planning Artifacts

```bash
ls -la _bmad-output/planning-artifacts/ 2>/dev/null | tail -10
```

Identify active planning documents (PRD, epics, brainstorms) to understand current project phase.

### Step 6 — Present Session Brief

```
## 📋 Session Brief

### Recent History
- Last session: [date] — [summary]
- Previous session: [date] — [summary]
- Unfinished work: [list]

### Project State
- Branch: [branch name]
- Last commit: [message]
- Uncommitted changes: [yes/no — detail]
- Preflight: [pass/issues]

### Active Artifacts
- [list of current planning documents]

### Suggested Next Steps
1. [based on unfinished work from last session]
2. [based on project state]
3. [based on planning artifacts]

Ready to work! What would you like to focus on?
```

## Notes

- This skill is designed to be fast — each step should complete in seconds
- If session-chain doesn't exist, gracefully degrade to git history + file inspection
- The goal is context restoration, not deep analysis
