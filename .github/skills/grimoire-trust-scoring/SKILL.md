---
name: grimoire-trust-scoring
description: "Scoring de confiance opérationnelle pour sorties agent/sub-agent. Use when: trust score, fiabilité agent, reliability check, confidence gating, should we trust this result, CVTL trigger. Calibrates confidence from evidence and enforces escalation thresholds."
---

# Trust Scoring

Operational trust scoring for agent outputs before final delivery.

## When to Use

- Output has high impact (security, production, migration, architecture)
- A sub-agent result looks plausible but evidence is thin
- Multiple alternatives conflict and a decision must be justified
- User explicitly asks for reliability/trust assessment

## Trust Dimensions

Score each dimension from 0 to 100:

- Evidence quality: concrete file references, command output, reproducible checks
- Consistency: no contradiction with workspace state, instructions, or prior decisions
- Verification depth: tests/lint/validators actually executed when relevant
- Risk coverage: edge cases, rollback, and failure modes considered
- Uncertainty handling: assumptions made explicit, no over-claiming

## Procedure

### Step 1 — Gather Evidence

Collect objective signals:

- Files changed and linked to claims
- Tool outputs used as proof
- Validator/test status and exit codes

### Step 2 — Compute Trust Score

Use weighted scoring:

$$
T = 0.30E + 0.20C + 0.20V + 0.20R + 0.10U
$$

Where:

- $E$ = Evidence quality
- $C$ = Consistency
- $V$ = Verification depth
- $R$ = Risk coverage
- $U$ = Uncertainty handling

### Step 3 — Apply Gates

- `T >= 80`: output can be delivered with standard caveats
- `60 <= T < 80`: deliver with explicit assumptions and one extra verification
- `40 <= T < 60`: trigger CVTL second pass before delivery
- `T < 40`: reject output and re-run with stricter evidence requirements

### Step 4 — Return a Trust Card

Use this format:

```markdown
## Trust Card

- Score: XX/100
- Decision: deliver | deliver-with-guardrails | CVTL-required | reject
- Strongest evidence: ...
- Weakest point: ...
- Required next verification: ...
```

## Notes

- Trust scoring is a gate, not a replacement for technical verification
- Low trust must never be hidden from the user
- Always prefer explicit uncertainty over confident speculation
