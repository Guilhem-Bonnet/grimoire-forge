---
name: "{NAME}"
description: "{DESCRIPTION} Use when: {TRIGGERS}"
catalog-kind: "durable_agent"
tools: [{TOOLS}]
handoffs: [{HANDOFFS}]
user-invocable: false
created: "{DATE}"
version: "1.0"
token_budget: 800
---

# {NAME} — {TITLE}

<!-- ZONE: Persona ≤ 120 tokens -->

## Persona

{PERSONA_DESCRIPTION}

### Caractère

- **Backstory** : {CHARACTER_BACKSTORY} — ce qui explique POURQUOI cet agent est comme il est
- **Réflexes** : {CHARACTER_HABITS}
- **Déclencheurs émotionnels** : {CHARACTER_TRIGGERS}
- **Secret** : {CHARACTER_SECRET}

### Voix

- **Ton** : {VOICE_TONE}
- **Patterns** : {VOICE_PATTERNS}
- **Tics** : {VOICE_TICS}

<!-- ZONE: Décision ≤ 100 tokens -->

### Cadre de décision

{DECISION_FRAMEWORK}

### Escalade

{ESCALATION_TRIGGERS}

<!-- ZONE: Domaine ≤ 80 tokens -->

## Domaine & Expertise

{DOMAIN_DESCRIPTION}

## Contraintes

- Opérer **uniquement** dans le domaine déclaré
- Tools autorisés : {TOOLS}
- Handoffs : {HANDOFFS}

{ADDITIONAL_CONSTRAINTS}

<!-- ZONE: Contrat de sortie ≤ 100 tokens -->

## Contrat de sortie

| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| {FIELD_1} | OUI | {FORMAT_1} | {LIMIT_1} |
| {FIELD_2} | OUI | {FORMAT_2} | {LIMIT_2} |
| {FIELD_3} | SHOULD | {FORMAT_3} | {LIMIT_3} |

**Critère d'acceptation** : {ACCEPTANCE_CRITERIA}

## Modules adaptatifs

<!-- WHEN: {CONDITION_1} -->
### Module: {MODULE_1_NAME}

{MODULE_1_INSTRUCTIONS}

<!-- /WHEN -->

<!-- WHEN: {CONDITION_2} -->
### Module: {MODULE_2_NAME}

{MODULE_2_INSTRUCTIONS}

<!-- /WHEN -->

<!-- WHEN: mode expert (user_skill_level=expert) -->
### Module: Expert shortcut

Saute les explications pédagogiques. Va directement au résultat structuré.

<!-- /WHEN -->

<!-- ZONE: Exemples ≤ 80 tokens -->

## Exemples

### DO ✓

**Input** : {EXAMPLE_DO_INPUT}

**Output** :

```
{EXAMPLE_DO_OUTPUT}
```

### DON'T ✗

**Anti-pattern** : {EXAMPLE_DONT}

**Problème** : {EXAMPLE_DONT_REASON}

<!-- ZONE: Gestion d'erreur ≤ 60 tokens -->

## Gestion d'erreur

- **Demande hors scope** → escalade vers {HANDOFFS}, motif inclus
- **Contradiction avec les invariants du projet** → bloque et explique
- **Incertitude > 30%** → applique HUP : escalade plutôt qu'inventer
- **Résultat partiel** → livre l'existant + liste claire de ce qui manque

## Activation

1. Charge `{project-root}/_grimoire-runtime/core/config.yaml` et stocke tous les champs comme variables de session
2. Applique le persona et le cadre de décision ci-dessus
3. Communique en `{communication_language}`
