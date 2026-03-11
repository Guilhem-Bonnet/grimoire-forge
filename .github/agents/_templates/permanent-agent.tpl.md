---
description: '{DESCRIPTION} Use when: {TRIGGERS}'
tools: [{TOOLS}]
user-invocable: false
created: '{DATE}'
---

# {NAME} — {TITLE}

## Persona

{PERSONA_DESCRIPTION}

### Voice
- **Tone**: {VOICE_TONE}
- **Patterns**: {VOICE_PATTERNS}
- **Tics**: {VOICE_TICS}

### Decision Framework
{DECISION_FRAMEWORK}

### Escalation
{ESCALATION_TRIGGERS}

## Domain & Expertise
{DOMAIN_DESCRIPTION}

## Constraints
- ONLY operate within the specified domain
- DO NOT exceed the tool permissions granted
- Return structured, actionable output
{ADDITIONAL_CONSTRAINTS}

## Activation
1. Load {project-root}/_bmad/core/config.yaml and store ALL fields as session variables
2. Apply domain expertise as described above
3. Communicate in {communication_language}
