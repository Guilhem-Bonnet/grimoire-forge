---
name: grimoire-friction-management
description: "Gestion active de la friction conversationnelle via QEC et budget de questions. Use when: too many questions, batching, friction budget, reduce interruptions, smooth execution, autonomous flow. Converts scattered clarifications into minimal high-value question batches."
---

# Friction Management

Reduce conversational friction while preserving correctness.

## When to Use

- User says there are too many questions or interruptions
- Work requires many clarifications across files/domains
- A long implementation risks stalling on micro-decisions
- Session momentum is dropping due to context switching

## Friction Signals

Track these signals continuously:

- Number of clarification prompts per phase
- Repeated asks for information already available in workspace
- Latency caused by avoidable confirmation loops
- User prompts indicating impatience or flow break

## Procedure

### Step 1 — Build a Question Backlog

Before asking anything, collect all pending uncertainties and classify them:

- Blocking: cannot proceed safely without user input
- Non-blocking: can proceed using defaults and report assumptions
- Nice-to-have: defer unless user asks

### Step 2 — Apply a Friction Budget

Use a strict budget per phase:

- Default budget: one batched clarification request
- If budget exceeded: choose safe defaults, continue, and log assumptions
- Escalate only for high-risk blocking decisions

### Step 3 — Batch via QEC

When questions are needed, ask in one compact batch:

- Group by decision area
- Offer recommended default for each item
- Allow quick one-line user response

### Step 4 — Report Assumptions Explicitly

For non-blocking uncertainties, proceed and surface assumptions in output:

```markdown
## Assumptions Applied

- Decision area: ...
- Assumption used: ...
- Why safe: ...
- How to override: ...
```

## Guardrails

- Never trade correctness for silence on high-risk operations
- Never ask one question at a time when batching is possible
- If uncertainty is high and impact is high, escalate immediately

## Outcome Target

- Fewer interruptions
- Faster forward progress
- Clear assumption traceability
