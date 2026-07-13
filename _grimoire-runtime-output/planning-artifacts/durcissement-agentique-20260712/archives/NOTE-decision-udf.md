---
title: Note de décision — retrait de l'UDF
description: Décision de retrait du mécanisme Unified Dynamic Factory et archivage de son registre
author: Grimoire Master (session Claude)
date: 2026-07-12
---

## Décision

Le mécanisme UDF (Unified Dynamic Factory — création d'artefacts éphémères `_dyn-*` avec triage de durabilité, tracker d'usage et promotion automatique) est retiré du runtime le 2026-07-12, en exécution du lot 1 du plan de durcissement agentique (item 1.2).

## Motif

Zéro usage constaté sur toute la durée de vie du mécanisme :

- `_grimoire-runtime/_memory/udf-usage-tracker.json` : vide (`"artifacts": {}`) ;
- aucun artefact `_dyn-*` jamais créé sous `.github/` ;
- aucune promotion enregistrée.

Le bloc UDF était par ailleurs chargé dans le contexte de chaque session via `copilot-instructions.md` et `grimoire-master.agent.md` — un coût de contexte permanent sans aucun bénéfice mesuré, le mécanisme exact dont la campagne d'evals web-app-todo du 2026-07-03 a démontré l'inefficacité (présence passive sans usage).

## Portée du retrait

- Section UDF de `.github/copilot-instructions.md` remplacée par une section « Création d'artefacts » (créations permanentes uniquement, pipeline skill-forge conservé) ;
- Bloc `<unified-dynamic-factory>` retiré de `.github/agents/grimoire-master.agent.md` et de `_grimoire-runtime/_config/agent-wrapper-spec.json` ;
- `udf-registry.yaml` déplacé de `_grimoire-runtime/_config/` vers ce dossier d'archive ;
- Références `_dyn-*` et registre retirées des skills `grimoire-skill-forge`, `grimoire-skill-analyzer`, `grimoire-builder-factory` ;
- Script `grimoire-cleanup-dynamic-artifacts.sh` et tasks `cleanup-dynamic-artifacts` retirés.

## Ce qui est conservé

Le pipeline de création gouvernée reste inchangé : builders (agent-builder, workflow-builder, tech-writer), gate qualité `grimoire-skill-analyzer` (75/100 minimum), création de hooks toujours en `mode: shadow` via le gateway.

## Réversibilité

Pour ressusciter le mécanisme : restaurer `archives/udf-registry.yaml` vers `_grimoire-runtime/_config/`, puis réintroduire les blocs d'instructions depuis l'historique git (état antérieur au 2026-07-12). Condition posée par le plan : un cas d'usage réel démontré, pas une résurrection spéculative.
