---
name: grimoire-product-discovery
description: "Recherche, cadrage produit et PRD BMM. Use when: product brief, create PRD, edit PRD, validate PRD, market research, domain research, technical research, generate project context, product discovery, cadrage produit."
created: "2026-04-14"
---

# Grimoire Product Discovery

Cette skill remplace la grappe de wrappers BMM orientes recherche, brief, contexte projet et PRD.

## When to Use

- Quand il faut lancer une recherche marche, domaine ou technique avant de specifier.
- Quand il faut creer, enrichir, corriger ou valider un product brief ou un PRD.
- Quand il faut generer ou mettre a jour le contexte projet a partir d'un cadrage reel.
- Quand le besoin est encore flou et doit passer par un vrai cycle de decouverte produit.

## Pre-requisites

- Charger `_grimoire-runtime/bmm/config.yaml`.
- Lire le contexte produit existant, le PRD courant et les decisions proches si elles existent deja.
- Identifier le livrable attendu avant de commencer : note de recherche, brief, PRD, validation ou contexte projet.

## Process

1. Cadrer la question produit, le scope et l'angle de recherche.
2. Produire la recherche minimale utile : marche, domaine, technique ou combinaison des trois.
3. Transformer la matiere collectee en brief exploitable ou en PRD coherent.
4. Si un PRD existe deja, travailler en mode edition ou validation plutot qu'en recreation aveugle.
5. Finir par un paquet de sortie actionnable : hypothese, decisions, zones ouvertes, prochaines interfaces de handoff.

## Agents Involved

- `analyst` pour la recherche et le cadrage.
- `pm` pour le brief, le PRD et les arbitrages produit.
- `architect` si la faisabilite technique influence le cadrage.
- `tech-writer` si le livrable final doit etre remis en forme ou normalise.

## Assets

- `_grimoire-runtime/bmm/workflows/1-analysis/`
- `_grimoire-runtime/bmm/workflows/2-plan-workflows/create-prd/`
- `_grimoire-runtime/bmm/workflows/generate-project-context/`

## Output Format

- Question de cadrage explicite.
- Synthese de recherche.
- Brief ou PRD mis a jour.
- Liste courte des hypotheses ouvertes et des handoffs recommends.

## Success Criteria

- Le livrable repond a une question produit precise.
- Les hypotheses et contraintes sont explicites.
- Le PRD ou le brief est assez stable pour servir de point d'entree aux phases solutioning et implementation.
- Le contexte projet capture les decisions utiles sans devenir un fourre-tout.