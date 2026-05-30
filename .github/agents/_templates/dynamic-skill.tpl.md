---
name: "{SKILL_NAME}"
description: "{DESCRIPTION} Use when: {TRIGGERS}"
created: "{DATE}"
expires: "{EXPIRES_7DAYS}"
version: "1.0"
token_budget: 300
---

# {NAME}

## Quand utiliser

{USAGE_CONTEXT}

**Ne pas utiliser si** : {ANTI_TRIGGERS}

## Processus

{PROCESS_STEPS}

## Contrat de sortie

| Champ | Requis | Format |
| --- | --- | --- |
| {OUTPUT_FIELD_1} | OUI | {FORMAT_1} |
| {OUTPUT_FIELD_2} | SHOULD | {FORMAT_2} |

## Modules adaptatifs

<!-- WHEN: {CONDITION_1} -->

### Module: {MODULE_1_NAME}

{MODULE_1_CONTENT}

<!-- /WHEN -->

## Exemple

**Input** : {EXAMPLE_INPUT}

**Output attendu** : {EXAMPLE_OUTPUT}

## Gestion d'erreur

- **Prérequis manquant** → liste ce qui manque avant d'exécuter
- **Résultat partiel** → livre avec `{"partial": true, "reason": "..."}`
