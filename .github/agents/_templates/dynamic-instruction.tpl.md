---
description: "{DESCRIPTION} Applies to: {APPLY_TO_GLOB}"
applyTo: "{APPLY_TO_GLOB}"
catalog-kind: "instruction"
created: "{DATE}"
expires: "{EXPIRES_7DAYS}"
version: "1.0"
token_budget: 200
zones: {critical: "≤ 40 tokens", rules: "≤ 100 tokens", examples: "≤ 40 tokens"}
---

# {NAME}

## Zone Critique

<!-- SEVERITY: MUST -->

- {RULE_CRITICAL_1}
- {RULE_CRITICAL_2}

## Quand appliquer

Fichiers concernés : `{APPLY_TO_GLOB}`

**Ne pas appliquer si** : {ANTI_TRIGGERS}

## Règles

<!-- SEVERITY: MUST -->

{RULES_MUST}

<!-- SEVERITY: SHOULD -->

{RULES_SHOULD}

## Modules adaptatifs

<!-- WHEN: {CONDITION_1} -->

### Module: {MODULE_1_NAME}

{MODULE_1_CONTENT}

<!-- /WHEN -->

## Exemple

### DO ✓

```
{EXAMPLE_DO}
```

### DON'T ✗

**Anti-pattern** : {EXAMPLE_DONT}

## Gestion d'erreur

- **Règle MUST violée** → signale avant de continuer
- **Conflit d'instructions** → applique le `applyTo` le plus spécifique
