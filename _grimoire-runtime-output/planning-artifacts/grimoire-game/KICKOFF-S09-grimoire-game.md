---
title: Kickoff Sprint S9 - Grimoire Game
description: Checklist de demarrage pour lancer S9 sans relecture exhaustive du corpus.
author: GitHub Copilot
date: 2026-04-09
---

## But

Fournir une checklist de demarrage minimale pour lancer S9 sur l'etat courant du board, avec les bons tickets ouverts, les bonnes gates actives et aucun glissement de scope au kickoff.

## Statut post-challenge

Ce kickoff reste bloque tant que `GAME-TKT-054` n'est pas prouve.

Tant que cette gate n'est pas fermee:

- aucun ticket `GAME-S09-*` ne doit passer `In Progress` hors travail de preparation sur `GAME-S09-001` ;
- `GAME-S09-002`, `GAME-S09-003`, `GAME-S09-004` et `GAME-S09-005` restent non demarrables ;
- la checklist ci-dessous sert surtout de readiness review et non de feu vert immediate.

Mise a jour runtime locale du 2026-04-11 :

- La tranche runtime bornee de `GAME-TKT-030` est deja couverte et validee dans `grimoire-kit/apps/grimoire-game`.
- `GAME-S09-001` et `GAME-S09-002` restent donc, a ce stade, des tickets de readiness ou de recadrage UX plutot que des tickets runtime encore ouverts.
- `GAME-TKT-038` doit etre traite comme dependance satisfaite localement dans toute lecture future du kickoff.

## Sources operatoires

- [SPRINT-S09-grimoire-game.md](SPRINT-S09-grimoire-game.md)
- [HANDOFF-S09-grimoire-game.md](HANDOFF-S09-grimoire-game.md)
- [TICKETS-web-gaming.md](TICKETS-web-gaming.md)
- [GO-NO-GO-S09-004-grimoire-game.md](GO-NO-GO-S09-004-grimoire-game.md)
- [PAQUET-execution-agentic-guardrails-runtime.md](PAQUET-execution-agentic-guardrails-runtime.md)
- [PAQUET-execution-front-prioritaire-post-challenge.md](PAQUET-execution-front-prioritaire-post-challenge.md)

## Checklist de kickoff

### 1. Etat du board

- `GAME-S09-001` est `Ready`.
- `GAME-S09-002`, `GAME-S09-005`, `GAME-S09-003` et `GAME-S09-004` sont `Backlog`.
- `GAME-TKT-052`, `GAME-TKT-053` et `GAME-TKT-054` restent prioritaires et gate le sprint.
- Les parents `GAME-TKT-030`, `GAME-TKT-037`, `GAME-TKT-015` et `GAME-TKT-034` restent la source de verite macro.
- La lecture operative de `GAME-TKT-030` doit integrer le fait que sa tranche runtime locale est deja couverte et ne constitue plus un manque runtime ouvert.

### 2. Scope du sprint

- Le coeur de sprint est borne a `GAME-S09-001`, `GAME-S09-002`, `GAME-S09-005` et `GAME-S09-003`.
- `GAME-S09-004` est explicitement conditionnel.
- Aucun glissement depuis `TASK-037`, `TASK-038`, `TASK-052`, `TASK-053`, `TASK-054`, `TASK-056`, `TASK-057` ou `TASK-058` n'entre dans le kickoff.

### 3. Preconditions techniques

- Le socle debug attendu pour S9 ne presente pas de blocage structurel connu.
- Le cadrage auth spectateur existe au moins au niveau decisionnel ou contractuel.
- Le scope S9 de configuration expose ou prepare provenance, trust status et policy minimale pour les activations.

### 4. Handoffs role par role

- `@ux` prend `GAME-S09-001` pour geler les contrats UI du skill tree et de la modal de challenge.
- `@dev` n'ouvre pas `GAME-S09-002` avant gel des contrats UI.
- `@qa` prepare les preuves de persistence, d'activation autorisee ou refusee et de non-regression challenge.
- `@arch` arbitre les contraintes contractuelles non negociables avant ouverture du conditionnel.

### 5. Sequence de lancement

1. Ne passer `GAME-S09-001` en `In Progress` que si un reliquat S9 explicite est redecoupe; ne pas le rouvrir pour reimplementer la tranche runtime deja couverte de `GAME-TKT-030`.
2. Garder `GAME-S09-002`, `GAME-S09-005`, `GAME-S09-003` et `GAME-S09-004` fermes tant que `GAME-TKT-054` n'est pas prouve.
3. Ne rouvrir `GAME-S09-002` qu'apres `Gate S9-1` et seulement pour un reliquat UI ou produit explicitement recadre.
4. Ouvrir `GAME-S09-005` seulement apres `Gate S9-2`.
5. Ouvrir `GAME-S09-003` seulement apres `Gate S9-2b`.
6. Ouvrir `GAME-S09-004` uniquement apres revue formelle sur [GO-NO-GO-S09-004-grimoire-game.md](GO-NO-GO-S09-004-grimoire-game.md).

## Definition d'un kickoff termine

- `GAME-S09-001` est en cours ou explicitement prepare sans ouverture prematuree du sprint.
- Les roles savent quel ticket ils portent et avec quelle preuve minimale.
- Les gates `S9-1`, `S9-2`, `S9-2b`, `S9-3` et `S9-4` sont comprises et non ambiguës.
- Le sprint est borne sans reinterpretation du scope ni contournement de la gate `GAME-TKT-054`.
