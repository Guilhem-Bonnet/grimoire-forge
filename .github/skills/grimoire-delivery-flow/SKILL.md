---
name: grimoire-delivery-flow
description: "Architecture, UX, stories et execution BMM. Use when: create architecture, create UX design, epics and stories, sprint planning, sprint status, implementation readiness, correct course, create story, dev story, retrospective, quick spec, quick dev, delivery flow, execution pack."
created: "2026-04-14"
---

# Grimoire Delivery Flow

Cette skill remplace la grappe de wrappers BMM orientes solutioning, plan de livraison et execution d'une story.

## When to Use

- Quand il faut passer du cadrage a l'architecture, a l'UX ou aux stories.
- Quand il faut preparer un sprint, verifier la readiness d'implementation ou corriger le cap.
- Quand il faut transformer une story en execution concrete via quick spec, create story ou dev story.
- Quand il faut produire un execution pack coherent au lieu d'enchainer des wrappers BMM disperses.

## Pre-requisites

- Partir d'un brief, d'un PRD ou d'un contexte projet deja assez stable.
- Identifier la phase courante : solutioning, planification, execution ou correction de trajectoire.
- Definir si la sortie attendue est une architecture, un lot de stories, un statut de sprint ou une implementation.

## Process

1. Choisir la bonne phase du flux de livraison plutot qu'un prompt isole.
2. Produire l'artefact de conception requis : architecture, UX, epics ou stories.
3. Passer en readiness puis en execution avec quick spec, create story ou dev story selon le niveau de maturite.
4. Suivre l'avancement avec sprint planning, sprint status, retrospective ou correct course selon le besoin.
5. Fermer la boucle avec un paquet de livraison : artefact produit, etat d'execution, risques restants, relances evidentes.

## Agents Involved

- `architect` pour les choix structurels.
- `ux-designer` pour les artefacts UX/UI.
- `sm` pour le backlog, les stories et le pilotage sprint.
- `dev` pour l'execution.
- `qa` pour la verification immediate au niveau story.

## Assets

- `_grimoire-runtime/bmm/workflows/3-solutioning/`
- `_grimoire-runtime/bmm/workflows/4-implementation/`
- `_grimoire-runtime/bmm/workflows/qa-generate-e2e-tests/`

## Output Format

- Phase du flux choisie.
- Artefact principal produit ou mis a jour.
- Etat d'execution ou de sprint.
- Risques, blocages et relances evidentes.

## Success Criteria

- Le flux ne saute pas de la decouverte au code sans artefact intermediaire utile.
- Chaque handoff correspond a une phase claire.
- Les stories et decisions d'execution sont traçables.
- Le resultat final peut etre repris directement par implementation, QA ou documentation sans reinterpretation lourde.