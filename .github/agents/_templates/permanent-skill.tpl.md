---
name: "{SKILL_NAME}"
description: "{DESCRIPTION} Use when: {TRIGGERS}"
created: "{DATE}"
version: "1.0"
token_budget: 500
deprecated_by: ""
---

# {NAME} — {TITLE}

## Quand utiliser

{USAGE_CONTEXT}

**Ne pas utiliser si** : {ANTI_TRIGGERS}

## Pré-requis

- {PREREQUISITE_1}
- {PREREQUISITE_2}

## Processus

{PROCESS_STEPS}

## Agents impliqués

| Agent | Rôle | Gate de passage |
| --- | --- | --- |
| {AGENT_1} | {ROLE_1} | {GATE_1} |
| {AGENT_2} | {ROLE_2} | {GATE_2} |

## Assets

- {ASSET_1} — {ASSET_1_PURPOSE}
- {ASSET_2} — {ASSET_2_PURPOSE}

## Contrat de sortie

| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| {OUTPUT_FIELD_1} | OUI | {FORMAT_1} | {LIMIT_1} |
| {OUTPUT_FIELD_2} | OUI | {FORMAT_2} | {LIMIT_2} |
| {OUTPUT_FIELD_3} | SHOULD | {FORMAT_3} | {LIMIT_3} |

**Critères de succès** :

- {SUCCESS_CRITERION_1}
- {SUCCESS_CRITERION_2}

## Modules adaptatifs

<!-- WHEN: {CONDITION_1} -->

### Module: {MODULE_1_NAME}

{MODULE_1_INSTRUCTIONS}

<!-- /WHEN -->

<!-- WHEN: mode expert (user_skill_level=expert) -->

### Module: Expert shortcut

Saute les explications pédagogiques. Livre directement le résultat structuré.

<!-- /WHEN -->

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

## Gestion d'erreur

- **Prérequis manquant** → stoppe, liste ce qui manque, n'exécute pas
- **Gate non franchi** → bloque et explique le critère non rempli
- **Résultat partiel** → livre l'existant + liste claire de ce qui manque
