---
title: Mission Board Redesign Proof Pack
description: Preuves visuelles et validations de la refonte kanban-first du Mission Board.
---

# Mission Board Redesign Proof Pack

## Portee

Cette preuve couvre la refonte du mode Mission Board du cockpit Grimoire Game pour le scenario `blocked-guardrails`.

La cible etait de remplacer le layout en mosaique decoratif par une surface de pilotage plus fidele au projet de reference:

- rail rooms a gauche pour le contexte
- kanban tactique au centre comme surface dominante
- drawer detaille a droite pilote par la selection
- frise causale en bas

## Validations

Les validations suivantes ont ete executees apres la refonte:

- `grimoire-game: check`
- `grimoire-game: cockpit:verify`
- `vitest run --run tests/integration/mission-board-view.test.ts`
- verification interactive du focus drawer via clic sur une carte du board

## Evidence Files

- [Screenshot final](mission-board-redesign-v2.png)
- [Screenshot premiere passe](mission-board-redesign.png)
- [Snapshot accessibilite final](page-2026-04-17T00-12-37-251Z.yml)
- [Snapshot accessibilite premiere passe](page-2026-04-17T00-10-39-995Z.yml)

## Observations

Le board final montre bien la nouvelle hierarchie attendue:

- les colonnes kanban sont visibles comme centre du pilotage
- les rails Branch Finisher et Watchtower restent secondaires
- le drawer change de focus quand une carte est selectionnee
- la frise causale reste lisible comme support de causalite, sans voler le premier plan
