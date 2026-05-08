---
title: Guide d'utilisation - Adaptation Gastownhall Grimoire
description: Guide operatoire pour lire, activer et executer le package d'adaptation Gastownhall -> Grimoire sans perdre la these Grimoire-first.
author: GitHub Copilot
date: 2026-04-16
---

## Guide d'utilisation — Adaptation Gastownhall Grimoire

## 1. Portee

Ce guide explique comment utiliser le package `adaptation-gastownhall-grimoire` pour lancer une execution reelle sans rediscuter a chaque session la direction, les priorites ou les dependances.

Il ne promet pas que toutes les implementations existent deja. Il documente comment **piloter proprement l'execution**.

## 2. Ordre de lecture recommande

1. lire [PLAN-adaptation-gastownhall-grimoire.md](./PLAN-adaptation-gastownhall-grimoire.md) pour la these directrice ;
2. lire [TICKETS-adaptation-gastownhall-grimoire.md](./TICKETS-adaptation-gastownhall-grimoire.md) pour les dependances et les gates ticket par ticket ;
3. lire [FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md](./FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md) pour l'inventaire et les tasks preparees ;
4. utiliser [DOC-TECHNIQUE-adaptation-gastownhall-grimoire.md](./DOC-TECHNIQUE-adaptation-gastownhall-grimoire.md) si vous devez brancher l'implementation ;
5. relire ce guide avant de lancer une tranche.

## 3. Tranche a lancer en premier

La tranche finale retenue est la suivante :

### T0 — Spine contractuelle

Commencez par :

- `Mission Ledger` ;
- `Workflow Instances` ;
- `Pack Registry` ;
- `Session Lineage`.

Sans cette spine, les surfaces board, la supervision ou le marketplace deviennent du theatre.

### T1 — Memoire, contexte et tokens

Une fois la spine posee, lancez :

- `Seance` read-only ;
- recall borne et progressive disclosure ;
- `Qdrant` optionnel avec fallback local ;
- `Redis` optionnel avec fallback `in-process` ;
- parite de transport MCP puis CLI/API.

### T2 — Verification et supervision

Ensuite seulement :

- taxonomie d'incidents ;
- verification queue ;
- evidence pack aligne ;
- self-heal et escalation.

## 4. Comment choisir entre local, Redis et Qdrant

### Sans service externe

Choisissez :

- `local` ou JSON fallback pour la memoire ;
- `in-process` pour l'etat chaud runtime.

Ce mode est suffisant pour valider le contrat et garder la source de verite dans le repo et le runtime.

### Avec recall semantique utile

Choisissez `Qdrant` seulement si vous avez besoin de :

- recherche semantique filtree ;
- `Memory Context` borne ;
- relecture inter-session compacte ;
- retrieval L1, L2, L3.

### Avec runtime distribue ou chargee

Choisissez `Redis` seulement si vous avez besoin de :

- heartbeats et leases ;
- locks et rate limits ;
- streams ou buffers courts ;
- event bus runtime chaud.

## 5. Regle MCP versus CLI/API

Si MCP est disponible, il peut servir de transport utile.

Si MCP est restreint, interdits ou absent :

- utilisez les memes contrats via CLI ou SDK ;
- gardez les memes identifiants et la meme provenance ;
- ne changez ni la logique metier ni les gates ;
- considerez seulement que le transport change.

Le package devient invalide si le mode MCP et le mode CLI/API racontent deux histoires differentes.

## 6. Comment utiliser les tasks preparees

Les tasks de [FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md](./FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md) servent a ouvrir une implementation tranchee.

Bon usage :

- choisir une tranche ;
- prendre les tasks dans l'ordre de dependance ;
- verifier la gate de chaque task ;
- ne pas ouvrir les tasks marketplace ou federation tant que la spine et la verification ne sont pas stabilisees.

Mauvais usage :

- essayer de lancer tout le backlog en parallele ;
- ouvrir les tasks board avant les contrats et read models ;
- traiter `Redis` ou `Qdrant` comme des prerequisites obligatoires.

## 7. Sortie attendue par tranche

### T0

Vous devez obtenir :

- schemas valides ;
- mapping runtime -> ledger reproductible ;
- lineage lisible ;
- packs resolus avec provenance et policy.

### T1

Vous devez obtenir :

- reponses `Seance` sans transcript brut ;
- `Memory Context` borne et progressive disclosure ;
- etat chaud lisible ;
- fallback local en l'absence de `Redis` ou `Qdrant`.

### T2

Vous devez obtenir :

- refus des completions sans preuve ;
- incidents visibles et classes ;
- playbooks de relance et d'escalation.

## 8. Anti-usages

- lancer marketplace avant la gouvernance des packs ;
- ouvrir commons ou federation comme si c'etait du P0 ;
- confondre etat chaud et source canonique ;
- injecter du transcript brut comme memoire principale ;
- traiter le board comme source de verite au lieu d'une projection.

## 9. References directes

- [PLAN-adaptation-gastownhall-grimoire.md](./PLAN-adaptation-gastownhall-grimoire.md)
- [TICKETS-adaptation-gastownhall-grimoire.md](./TICKETS-adaptation-gastownhall-grimoire.md)
- [FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md](./FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md)
- [SPEC-mission-ledger-grimoire.md](./SPEC-mission-ledger-grimoire.md)
- [SPEC-pack-registry-grimoire.md](./SPEC-pack-registry-grimoire.md)
