---
name: grimoire-intent-routing
description: "Routage d'intention avec scoring de confiance pour sélectionner skill/agent/profil. Use when: intent classification, routing decision, dispatch strategy, choose best skill, ambiguous request, confidence-based routing. Produces deterministic routing decisions with explicit confidence and fallback path."
---

# Intent Routing

Classify user intent and route execution with confidence-aware decisions.

## When to Use

- Request is ambiguous or spans multiple domains
- Several skills could match and prioritization is required
- Need deterministic routing justification for auditability
- User asks which path/agent/skill is most appropriate

## Intent Model

Classify intent into one primary class and optional secondary classes:

- Implement
- Debug
- Review
- Plan
- Validate
- Explore
- Operate

## Procedure

### Step 1 — Extract Signals

Use only observable inputs:

- Explicit verbs in user prompt
- Referenced files/symbols
- Error outputs and failing checks
- Session context and current phase

### Step 2 — Score Candidate Routes

For each candidate route, assign:

- Relevance score (0-100)
- Risk alignment score (0-100)
- Evidence completeness score (0-100)

Compute route confidence:

$$
R = 0.5Relevance + 0.3RiskAlignment + 0.2Evidence
$$

### Step 3 — Select Strategy

- `R >= 75`: direct route to best skill/path
- `50 <= R < 75`: route with explicit fallback and one guard check
- `R < 50`: ask one batched clarification or split into phased execution

### Step 4 — Emit Routing Card

```markdown
## Routing Card

- Primary intent: ...
- Candidate routes: A (XX), B (YY), C (ZZ)
- Selected route: ...
- Confidence: XX/100
- Fallback route: ...
- Reasoning basis: observed signals only
```

## Guardrails

- No hidden routing decisions on low confidence
- Avoid route flapping: keep route stable until a new strong signal appears
- If request becomes safety-critical, force verification path before execution
