---
title: Registre de nettoyage des plans deprecies
description: Classement non destructif des anciens plans et regles de migration vers le plan directeur Grimoire Agent OS.
author: Codex
date: 2026-05-08
---

# Registre de nettoyage des plans deprecies

## Statuts

| Statut | Sens | Regle |
| --- | --- | --- |
| `active` | Source de pilotage actuelle | Peut recevoir nouvelles tasks. |
| `source` | Reference analytique utile | Peut etre cite, mais pas piloter directement. |
| `absorbed` | Decisions migrees dans le plan directeur | Ne recoit plus de nouvelles tasks directes. |
| `superseded` | Remplace par un plan plus recent | Lecture historique seulement. |
| `incubator` | Idee ambitieuse non noyau | Peut alimenter un pack experimental. |
| `archive` | Contexte conserve | Pas de pilotage. |

## Regle de migration

Avant de marquer un plan `superseded` :

- extraire les decisions encore utiles ;
- rattacher les taches restantes a un ID `GAO-*` ;
- identifier les docs ou specs encore sources ;
- ajouter une note de migration dans le backlog si necessaire.

## Registre initial

| Artefact | Statut propose | Migration |
| --- | --- | --- |
| `plan-directeur-grimoire-gastown-unifie-20260508/` | `active` | Source unique du nouveau projet. |
| `strategie-grimoire-agent-os-20260508/` | `source` | Ses decisions sont reprises par Tracks B, E, I, J. |
| `DOC-TECHNIQUE-adaptation-gastownhall-grimoire.md` | `absorbed` | Repris dans la matrice Gastownhall complete. |
| `PLAN-adaptation-gastownhall-grimoire.md` | `absorbed` | GTA devient GAO, anciens tickets migrent vers backlog unifie. |
| `FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md` | `absorbed` | Tri absorbed/next/later/reject repris dans matrice fusion. |
| `TICKETS-adaptation-gastownhall-grimoire.md` | `absorbed` | `GTA-TKT-*` devient source de mapping vers `GAO-*`. |
| `PLAN-hooks-vague-suivante-grimoire-kit-2026-04-13.md` | `absorbed` | Repris dans Track E et contrat hooks. |
| `maturation-agentique-20260421/` | `source` | Sert de baseline historique ; ne pilote plus directement. |
| `reference-agentique-pilotage-20260425/` | `source` | Corpus de reference pour decisions externes. |
| `analyse-pilotage-agentique-2026-04-25/` | `source` | Support pedagogique, pas backlog. |
| `repo-analysis/` | `source` | Reference detaillee sur orchestration. |
| `audit-agentique-2026-04-10.md` | `source` | Diagnostic historique. |
| `benchmark-dimensionnel-agentique-2026-04-10.md` | `source` | Comparaison historique. |
| `plan-execution-post-audit-agentique-2026-04-10.md` | `superseded` | Remplace par plan directeur et Tracks A-K. |
| `plan-resserre-post-challenge-agentique-2026-04-11.md` | `source` | Principe contrat -> preuve -> cockpit conserve. |
| `PLAN-A-PLUS-GRIMOIRE-KIT-2026-04-11.md` | `source` | Les items qualite deviennent sous-taches GAO-J/kit quality. |
| `PLAN-multi-llm-multi-source.md` | `absorbed` | Repris dans Track I et Host Bridge. |
| `PRD-grimoire-v4-universal.md` | `incubator` | Vision ambitieuse, mais claims a borner par preuves GAO. |
| `PRD-bmad-kit-v3-platform.md` | `source` | Historique kit, a mapper si taches restantes. |
| `PRD-bmad-intelligence-layer.md` | `source` | Concepts a reprendre seulement via Memory OS et evals. |
| `EPICS-grimoire-v4-universal.md` | `incubator` | Ideas pool, pas execution directe. |
| `BRAINSTORM-GRIMOIRE-V4-UNIVERSAL.md` | `incubator` | Concepts a filtrer par matrice fusion. |
| `BRAINSTORM-META-EVOLUTION-V3.md` | `incubator` | Seulement apres kernel et evidence. |
| `BRAINSTORM-PIXEL-OBSERVATORY-V2.md` | `incubator` | Inspiration UI, pas contrat. |
| `V4-concepts-durcissement/` | `incubator` | Concepts a promouvoir via tests et hooks. |
| `PLAN-implementation-mission-board-grimoire.md` | `absorbed` | Repris dans Track H. |
| `SPEC-mission-board-grimoire.md` | `source` | Spec detaillee du cockpit. |
| `CONTRAT-mission-board-grimoire.md` | `source` | Contrat de board. |
| `MATRICE-verification-mission-board-grimoire.md` | `source` | Verification cockpit. |
| `grimoire-game/CONTRAT-runtime-agentic-guardrails.md` | `source` | Base Track E/H. |
| `grimoire-game/PAQUET-execution-agentic-guardrails-runtime.md` | `absorbed` | Execution deja partiellement materialisee, utiliser comme preuve. |
| `ux-audit-cockpit-v16/` | `source` | Reference UI. |
| `ux-audit-switchboard-v1/` | `source` | Inspiration Mission Board. |
| `ux-audit-pixel-agents-v1/` | `source` | Inspiration UI, pas source metier. |
| `INNOVATION-*` | `incubator` | Ideas pool a filtrer par GAO. |
| `PARTY-BRAINSTORM-V3-PLATFORM.md` | `archive` | Historique ideation. |

## Regles anti-regression documentaire

- Aucun nouveau fichier `PLAN-*` racine ne doit etre cree sans entree dans ce registre.
- Un nouveau PRD doit pointer vers un track `GAO-*`.
- Une task issue d'un ancien plan doit garder `source_ref`.
- Les documents `source` peuvent etre cites, mais une task active doit vivre dans le backlog unifie.
- Les documents `incubator` ne peuvent pas declencher implementation noyau sans passage par matrice fusion.

## Nettoyage physique recommande

Ne pas deplacer les fichiers maintenant.

Ordre recommande :

1. ajouter un index racine qui pointe vers ce paquet ;
2. ajouter des entetes de statut aux artefacts les plus consultes ;
3. migrer les tasks ouvertes vers `BACKLOG-agentique-unifie.md` ou Mission Ledger ;
4. seulement ensuite envisager un dossier `archive/` pour les plans `archive` et `superseded`.

