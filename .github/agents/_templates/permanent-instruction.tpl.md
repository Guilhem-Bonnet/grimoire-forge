---
description: "{DESCRIPTION} Applies to: {APPLY_TO_GLOB}"
applyTo: "{APPLY_TO_GLOB}"
catalog-kind: "instruction"
created: "{DATE}"
version: "1.0"
token_budget: 400
zones: {critical: "≤ 60 tokens", rules: "≤ 200 tokens", examples: "≤ 80 tokens"}
---

# {NAME}

## Zone Critique

<!-- SEVERITY: MUST -->

- {RULE_CRITICAL_1}
- {RULE_CRITICAL_2}
- {RULE_CRITICAL_3}

## Quand appliquer

Cette instruction s'applique aux fichiers correspondant au pattern : `{APPLY_TO_GLOB}`

**Ne pas appliquer si** : {ANTI_TRIGGERS}

## Règles

<!-- SEVERITY: MUST -->

### {RULE_GROUP_1}

{RULES_1}

<!-- SEVERITY: SHOULD -->

### {RULE_GROUP_2}

{RULES_2}

<!-- SEVERITY: MAY -->

### {RULE_GROUP_3}

{RULES_3}

## Modules adaptatifs

<!-- WHEN: {CONDITION_1} -->

### Module: {MODULE_1_NAME}

{MODULE_1_CONTENT}

<!-- /WHEN -->

<!-- WHEN: mode expert (user_skill_level=expert) -->

### Module: Expert shortcut

Saute les explications pédagogiques. Applique les règles directement sans commentaire.

<!-- /WHEN -->

## Exemples

### DO ✓

**Contexte** : {EXAMPLE_DO_CONTEXT}

```
{EXAMPLE_DO_CONTENT}
```

### DON'T ✗

**Anti-pattern** : {EXAMPLE_DONT}

**Problème** : {EXAMPLE_DONT_REASON}

## Contrat de sortie

| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| {OUTPUT_FIELD_1} | OUI | {FORMAT_1} | {LIMIT_1} |
| {OUTPUT_FIELD_2} | SHOULD | {FORMAT_2} | {LIMIT_2} |

## Gestion d'erreur

- **Règle MUST violée** → signale l'écart avant de continuer, ne valide pas silencieusement
- **Règle SHOULD ignorée** → commente l'exception si elle est intentionnelle
- **Conflit avec une autre instruction** → applique celle dont le `applyTo` est le plus spécifique
