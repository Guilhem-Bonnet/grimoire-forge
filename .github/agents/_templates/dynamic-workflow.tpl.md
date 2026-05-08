---
description: "{DESCRIPTION} Use when: {TRIGGERS}"
mode: "prompt"
created: "{DATE}"
expires: "{EXPIRES_7DAYS}"
version: "1.0"
token_budget: 350
zones: {context: "≤ 40 tokens", steps: "≤ 150 tokens", output: "≤ 60 tokens"}
---

# {NAME}

## Contexte

{WORKFLOW_DESCRIPTION}

**Ne pas utiliser si** : {ANTI_TRIGGERS}

## Pré-conditions

- {PRECONDITION_1}
- {PRECONDITION_2}

## Étapes

{STEPS}

## Contrat de sortie

| Champ | Requis | Format |
| --- | --- | --- |
| {OUTPUT_FIELD_1} | OUI | {FORMAT_1} |
| {OUTPUT_FIELD_2} | SHOULD | {FORMAT_2} |

**Critère d'acceptation** : {ACCEPTANCE_CRITERIA}

## Modules adaptatifs

<!-- WHEN: {CONDITION_1} -->

### Module: {MODULE_1_NAME}

{MODULE_1_CONTENT}

<!-- /WHEN -->

## Gestion d'erreur

- **Pré-condition non remplie** → stoppe et liste ce qui manque
- **Étape bloquante** → livre le partiel avec indication de l'étape échouée
