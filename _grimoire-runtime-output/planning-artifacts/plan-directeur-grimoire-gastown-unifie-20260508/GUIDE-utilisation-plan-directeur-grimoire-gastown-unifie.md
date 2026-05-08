---
title: Guide d'utilisation - Plan directeur Grimoire x Gastownhall unifie
description: Mode d'emploi du plan directeur comme source de pilotage unique pour agents, hooks, guardrails et nettoyage documentaire.
author: Codex
date: 2026-05-08
---

# Guide d'utilisation - Plan directeur Grimoire x Gastownhall unifie

## Statut du paquet

Ce paquet est la source de pilotage pour le nouveau projet Grimoire Agent OS.

Il ne supprime pas les anciens plans. Il les classe, les absorbe ou les garde comme references. Une tache nouvelle doit pointer vers ce paquet ou justifier pourquoi elle sort du plan directeur.

## Comment lire les documents

| Besoin | Document a lire |
| --- | --- |
| Comprendre la decision globale | `README.md` puis `DOC-TECHNIQUE-plan-directeur-grimoire-gastown-unifie.md` |
| Executer le nouveau projet | `PLAN-DIRECTEUR-nouveau-projet-grimoire-agent-os.md` |
| Savoir quoi fusionner depuis Gastownhall et les autres projets | `MATRICE-fusion-projets-agentiques.md` |
| Voir la fiche de chaque repo de reference | `ADDENDUM-REFERENCES-AGENTIQUES-comparaison-fusion.md` |
| Comprendre la decision precise sur CrewAI | `ADDENDUM-CREWAI-comparaison-fusion.md` |
| Adapter le travail aux agents, hooks et guardrails | `CONTRAT-hooks-guardrails-agents.md` |
| Creer ou router les prochaines tasks | `BACKLOG-agentique-unifie.md` |
| Nettoyer les anciens plans sans perte | `REGISTRE-nettoyage-plans-deprecies.md` |

## Regle pour les agents

Chaque agent doit traiter une tache comme un contrat executable.

Une tache valide contient :

- un identifiant ;
- une surface cible ;
- un contrat de sortie ;
- un profil de preuve ;
- des dependances ;
- des hooks attendus ;
- des guardrails ;
- une evidence de validation.

Une tache sans preuve attendue est incomplete. Une tache sans surface cible est non routable. Une tache qui modifie un contrat sans migration est bloquee.

## Regle pour Grimoire Forge

Forge reste le chantier vivant.

Forge porte :

- les instructions natives `AGENTS.md`, Copilot, Claude et Codex ;
- les hooks et guardrails host ;
- les rapports de strategie et de decision ;
- la dogfood des workflows ;
- le Mission Board comme cockpit de controle ;
- les evidences de validation.

Forge ne doit pas porter de logique produit qui devrait vivre dans grimoire-kit. Si une primitive devient generique, elle migre vers le kit.

## Regle pour grimoire-kit

grimoire-kit porte le produit distribuable.

grimoire-kit porte :

- SDK Python ;
- CLI ;
- MCP ;
- runtime kernel ;
- pack registry ;
- Memory OS ;
- UI runtime et dashboards ;
- tests et docs utilisateur.

Le kit ne doit pas introduire une architecture abstraite non testee par Forge. Toute primitive structurante doit avoir une preuve de dogfood.

## Regle de promotion

Un element peut passer de `experimental` a `stable` seulement si :

- il a un schema ou contrat versionne ;
- il a un test ou une validation ciblee ;
- il est visible dans le cockpit ou exportable ;
- il a une politique de securite ;
- il ne contourne pas le Mission Ledger ;
- il degrade proprement si le provider externe est absent.

## Regle de nettoyage

Le nettoyage des anciens plans se fait en trois gestes :

1. Classer le plan comme `active`, `source`, `absorbed`, `superseded`, `incubator` ou `archive`.
2. Extraire les decisions utiles vers le plan directeur ou le backlog unifie.
3. Interdire les nouvelles tasks directes contre un plan `superseded` sauf migration explicite.

Il ne faut pas supprimer les anciens artefacts tant que leurs decisions n'ont pas ete migrees ou referencees.

## Regle hooks et guardrails

Les hooks doivent rester courts.

Ils peuvent :

- enrichir le contexte ;
- bloquer une action deterministement dangereuse ;
- emettre un event ;
- ouvrir une task de verification ;
- ajouter un warning ;
- pointer vers une preuve manquante.

Ils ne doivent pas :

- executer un workflow long ;
- faire de la consolidation globale ;
- prendre seuls une decision produit durable ;
- muter le ledger sans contrat ;
- bypasser le registre de securite des hooks.

## Regle de fusion externe

Pour chaque projet externe :

1. nommer la primitive utile ;
2. choisir `core`, `adapter`, `pack`, `incubator`, `reject` ;
3. definir le contrat Grimoire ;
4. ajouter le hook ou gate minimal ;
5. produire une preuve ;
6. seulement ensuite promouvoir.
