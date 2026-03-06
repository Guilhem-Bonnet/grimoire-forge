---
name: grimoire-self-heal
description: 'Diagnose and repair BMAD Grimoire workflow failures. Use when: workflow failed, something broke, error diagnosis, self-healing, auto-repair, rollback, immune scan, what went wrong, fix workflow, debug failure, incident response. Combines self-healing diagnosis, immune system scan, and failure museum documentation.'
---

# Grimoire Self-Heal

Emergency workflow: diagnose a failure, attempt automated repair, and document the incident.

## When to Use

- A workflow or tool has failed
- When the user says "something broke", "what went wrong?", or "fix this"
- After an unexpected error during agent execution
- When a recurring problem needs root cause analysis

## Procedure

### Step 1 — Diagnose the Failure

```bash
python3 framework/tools/self-healing.py --project-root . diagnose --error "<error message or description>"
```

This identifies:
- Root cause category (missing file, config error, dependency issue, etc.)
- Known playbook match (if this failure pattern has been seen before)
- Suggested repair strategy (retry, alternative, rollback)

### Step 2 — Immune System Scan

```bash
python3 framework/tools/immune-system.py --project-root . scan
```

Runs both innate (static rules) and adaptive (learned from failures) checks:
- Pattern violations
- Security issues (OWASP patterns)
- Convention drift
- Historical incident patterns

If targeted to specific file:

```bash
python3 framework/tools/immune-system.py --project-root . scan --target <file-path>
```

### Step 3 — Attempt Healing

```bash
python3 framework/tools/self-healing.py --project-root . heal --error "<error message>"
```

Healing strategies (in order):
1. **Retry** — Transient errors (network, timing)
2. **Alternative** — Find a different path to the same result
3. **Rollback** — Return to last known good state
4. **Escalate** — Human intervention needed (with diagnosis)

### Step 4 — Document in Failure Museum

After resolution (or escalation), catalogue the incident:

```bash
python3 framework/tools/failure-museum.py --project-root . add \
  --title "<brief description>" \
  --category "<category>" \
  --root-cause "<what caused it>" \
  --fix "<what fixed it>" \
  --lesson "<what we learned>"
```

Categories: `config`, `dependency`, `logic`, `integration`, `data`, `performance`, `security`

### Step 5 — Enrich Immune System

If this is a new failure pattern, teach the immune system:

```bash
python3 framework/tools/immune-system.py --project-root . learn \
  --type "<pattern-type>" \
  --desc "<what happened>" \
  --fix "<how to prevent>"
```

### Step 6 — Incident Report

```
## 🩹 Self-Heal Report

### Incident
- Error: <original error>
- Diagnosis: <root cause>
- Severity: 🟢/🟡/🔴

### Resolution
- Strategy: retry / alternative / rollback / escalate
- Status: ✅ healed / ⚠️ partial / ❌ needs human
- Action taken: <what was done>

### Prevention
- Failure museum entry: ✅ created
- Immune system updated: ✅/❌
- Lesson: <key takeaway>

### Existing Playbook Match
- [Yes/No — if yes, which playbook was used]
```

## Quick Mode

For rapid diagnosis without full pipeline:

```bash
python3 framework/tools/self-healing.py --project-root . diagnose --error "<msg>"
```

Just get the diagnosis and recommended strategy, skip immune scan and documentation.

## Playbook Reference

View all known repair strategies:

```bash
python3 framework/tools/self-healing.py --project-root . playbook
```

## Notes

- Self-healing attempts are logged in history for learning
- The immune system gets smarter with each documented incident
- `heal` is safe — it doesn't force destructive operations
- Always document failures even if they were simple to fix (future pattern matching)
