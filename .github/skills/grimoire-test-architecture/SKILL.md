---
name: grimoire-test-architecture
description: "Strategie de test, ATDD et architecture QA/TEA. Use when: test design, test review, ATDD, NFR testing, CI testing, testing framework, teach me testing, test architecture, automation strategy, qa architecture."
created: "2026-04-14"
---

# Grimoire Test Architecture

Cette skill remplace la grappe de wrappers TEA et absorbe le besoin de strategie de tests, d'ATDD et d'architecture QA sans passer par des prompts unitaires disperses.

## When to Use

- Quand il faut concevoir une strategie de test ou un plan d'automatisation.
- Quand il faut cadrer l'ATDD, les NFR, la CI de tests ou le framework de test.
- Quand il faut revoir une suite de tests existante ou enseigner la structure de test attendue.
- Quand la demande depasse une simple ecriture de tests et touche a l'architecture qualite.

## When NOT to Use

- Pour ecrire un test avant le code dans une boucle red-green-refactor → `grimoire-tdd`.
- Pour generer un squelette de tests sur du code existant non teste → `grimoire-test-scaffold`.
- Cette skill est strategique (pyramide, fixtures, gates CI) ; ne pas l'utiliser pour des micro-decisions de test unitaire.

## Pre-requisites

- Charger `_grimoire-runtime/tea/config.yaml`.
- Identifier le niveau de sortie attendu : cadre pedagogique, design de tests, cadre CI/NFR ou plan d'automatisation.
- Distinguer strategie de test et implementation de tests ; pour du TDD pur, preferer `grimoire-tdd`.

## Process

1. Qualifier le risque produit et le niveau de test pertinent.
2. Produire le design de test, le cadre ATDD ou la revue structurelle necessaire.
3. Etablir la couverture NFR et la chaine CI correspondante si le scope le demande.
4. Relier la strategie aux AC, aux contrats et aux surfaces de verification reelles.
5. Finir par un plan d'action clair : quoi automatiser, quoi surveiller, quoi laisser en verification manuelle.

## Agents Involved

- `tea` pour la strategie et la gouvernance qualite.
- `qa` pour l'automatisation exploitable et la revue des suites.
- `dev` si des ajustements de structure sont necessaires pour rendre le code testable.

## Assets

- `_grimoire-runtime/tea/workflows/testarch/`
- `_grimoire-runtime/bmm/workflows/qa-generate-e2e-tests/`

## Output Format

- Risque cible.
- Strategie ou architecture de test.
- Matrice niveaux de test versus objectifs.
- Actions d'automatisation et de CI.

## Success Criteria

- La strategie choisit le bon niveau de test avant de parler outils.
- Les AC, NFR et contrats ont une couverture explicite.
- Le plan de test est actionnable sans multiplier les faux positifs E2E.
- Le resultat peut etre repris par `qa`, `tea` ou `dev` sans ambiguite.