---
description: "{DESCRIPTION} Use when: {TRIGGERS}"
mode: "prompt"
created: "{DATE}"
version: "1.0"
token_budget: 600
zones: {context: "≤ 60 tokens", steps: "≤ 200 tokens", output: "≤ 80 tokens"}
---

# {NAME} — {TITLE}

## Contexte

{WORKFLOW_DESCRIPTION}

**Problème résolu** : {PROBLEM_SOLVED}

**Ne pas utiliser si** : {ANTI_TRIGGERS}

## Pré-conditions

- {PRECONDITION_1}
- {PRECONDITION_2}

**Rollback** : {ROLLBACK_PROCEDURE}

## Étapes

{STEPS}

## Agents impliqués

| Agent | Rôle | Handoff vers |
| --- | --- | --- |
| {AGENT_1} | {ROLE_1} | {NEXT_1} |
| {AGENT_2} | {ROLE_2} | {NEXT_2} |

## Contrat de sortie

| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| {OUTPUT_FIELD_1} | OUI | {FORMAT_1} | {LIMIT_1} |
| {OUTPUT_FIELD_2} | OUI | {FORMAT_2} | {LIMIT_2} |
| {OUTPUT_FIELD_3} | SHOULD | {FORMAT_3} | {LIMIT_3} |

**Critères de succès** :

- {SUCCESS_CRITERION_1}
- {SUCCESS_CRITERION_2}

**Preuve attendue** : {PROOF_REQUIRED}

## Modules adaptatifs

<!-- WHEN: {CONDITION_1} -->

### Module: {MODULE_1_NAME}

{MODULE_1_INSTRUCTIONS}

<!-- /WHEN -->

<!-- WHEN: output volumineux > 500 tokens -->

### Module: Format condensé

Produis un résumé exécutif de 3 bullets avant le détail complet.

<!-- /WHEN -->

## Exemples

### DO ✓

{EXAMPLE_DO}

### DON'T ✗

{EXAMPLE_DONT}

## Gestion d'erreur

- **Pré-condition non remplie** → stoppe, liste ce qui manque, suggère l'action corrective
- **Étape bloquante** → livre le partiel + indique l'étape échouée + propose un contournement
- **Risque L3+** → pause, présente les options à l'utilisateur avant de continuer
