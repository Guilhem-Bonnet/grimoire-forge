---
title: Documentation technique - Adaptation Gastownhall Grimoire
description: Vue technique consolidee du package d'adaptation Gastownhall -> Grimoire, de sa spine canonique, de ses backplanes optionnels et de son ordre d'execution.
author: GitHub Copilot
date: 2026-04-16
---

## Documentation technique — Adaptation Gastownhall Grimoire

## 1. Objet

Cette documentation technique consolide le package `adaptation-gastownhall-grimoire` sous un angle implementation-ready.

Elle assemble le plan directeur, les tickets, l'inventaire des features et les decisions de traduction pour repondre a la question suivante : **quelles primitives absorber, dans quel ordre, et sur quelles surfaces canoniques, sans importer les dettes de produit, de backend ou de vocabulaire de Gastownhall**.

## 2. Decision technique directrice

La decision retenue est la suivante :

- la source de verite reste `Mission Ledger` + `Workflow Instances` + `Verification Queue` + `Session Lineage` ;
- `Redis` et `Qdrant` ne sont pas des verites paralleles, mais des backplanes optionnels ;
- la tranche finale priorise `memoire, contexte et tokens` avant les extensions de distribution ou de federation ;
- toute integration doit fonctionner en mode MCP quand le host le permet, puis en mode CLI/API ou fallback local quand MCP est restreint.

## 3. Surfaces canoniques du package

### Artefacts directeurs

- [PLAN-adaptation-gastownhall-grimoire.md](./PLAN-adaptation-gastownhall-grimoire.md)
- [TICKETS-adaptation-gastownhall-grimoire.md](./TICKETS-adaptation-gastownhall-grimoire.md)
- [FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md](./FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md)

### Contrats coeur relies

- [SPEC-mission-ledger-grimoire.md](./SPEC-mission-ledger-grimoire.md)
- [SPEC-pack-registry-grimoire.md](./SPEC-pack-registry-grimoire.md)
- [ADR-006-progressive-disclosure.md](./ADR-006-progressive-disclosure.md)

### References techniques utiles

- [referentiel-bonnes-pratiques-agentiques.md](../../docs/governance/referentiel-bonnes-pratiques-agentiques.md)
- [memory-system.md](../../grimoire-kit/docs/memory-system.md)
- [plugin-development.md](../../grimoire-kit/docs/plugin-development.md)

## 4. Spine cible du package

| Plane | Role | Surface canonique |
| --- | --- | --- |
| `Mission Ledger` | Missions, items, dependances, evidence, verification, escalation | Spec et runtime read models |
| `Workflow Plane` | Recipes, workflow instances, checkpoints, reprise | Contrats runtime et projections |
| `Pack Plane` | Packs, overlays, providers, policies, lock et provenance | `Pack Registry` |
| `Lineage Plane` | Session, run, trace, evidence, decision | `Session Lineage` |
| `Verification Plane` | Queue, verdicts, evidence packs et cloture fail-closed | `Verification Queue` |
| `Hot State Plane` | Leases, heartbeats, locks, rate limits, buffers courts | `in-process` ou `Redis` optionnel |
| `Semantic Recall Plane` | Recall contextuel, progressive disclosure, filtrage semantique | fallback local ou `Qdrant` optionnel |
| `Operator Plane` | Board, Library, Seance, supervision et verification | Projections, jamais source de verite |

## 5. Redis et Qdrant

| Brique | Usage nominal | Acces recommande | Regle dure |
| --- | --- | --- | --- |
| `Redis` | etat chaud runtime, locks, leases, heartbeats, streams et buffers courts | MCP si disponible, sinon `redis-cli` ou SDK via le meme contrat | ne jamais porter seul missions, verdicts ou decisions durables |
| `Qdrant` | memoire semantique, `Memory Context`, `Seance`, retrieval borne et filtres payload | MCP si disponible, sinon `grimoire memory`, client SDK ou REST API | ne jamais stocker seul un fait stable sans pointeur vers une source canonique |

Les deux briques sont utiles seulement si elles restent subordonnees au noyau causal. En cas d'absence, d'indisponibilite ou de policy restrictive, le package doit degrader vers `local`, JSON ou `in-process` sans changer le contrat metier.

## 6. Ordre d'execution final retenu

### Tranche T0 — Spine contractuelle

- `GTA-TKT-001` et `GTA-TKT-002` pour le `Mission Ledger` ;
- `GTA-TKT-003` pour `Workflow Instances` ;
- `GTA-TKT-004` et `GTA-TKT-005` pour `Pack Registry` ;
- `GTA-TKT-006` pour `Session Lineage`.

### Tranche T1 — Memoire, contexte et tokens

- `GTA-TKT-007` pour `Seance` read-only ;
- tasks `GTA-TASK-049` a `GTA-TASK-054` pour `Qdrant`, `Redis`, progressive disclosure, transport MCP/CLI/API et gates de provenance.

### Tranche T2 — Verification et supervision

- `GTA-TKT-008`, `GTA-TKT-009`, `GTA-TKT-010`.

### Tranche T3 — Surfaces operatoires

- `GTA-TKT-011`, `GTA-TKT-012`.

### Tranches suivantes

- `GTA-TKT-013`, `GTA-TKT-014` pour le marketplace verifie ;
- `GTA-TKT-015`, `GTA-TKT-016` en experimental uniquement.

## 7. Gates a respecter

- aucune integration `Redis` ou `Qdrant` ne court-circuite le `Mission Ledger` ;
- aucune reponse de recall n'entre dans un run critique sans provenance, fraicheur et fallback ;
- aucun `done` n'existe sans verification acceptee et evidence rattachee ;
- aucune surface UI n'invente un etat que le runtime n'a pas deja produit ;
- aucun mode MCP ne doit diverger fonctionnellement du mode CLI/API au niveau du contrat metier.

## 8. Non-objectifs

- imposer `Redis` ou `Qdrant` comme prerequis de demarrage ;
- recopier l'ergonomie, le vocabulaire ou les choix de backend de Gastownhall ;
- transformer ce package de planification en promesse que tout le code existe deja ;
- ouvrir marketplace ou federation avant la stabilisation de la spine contractuelle.
