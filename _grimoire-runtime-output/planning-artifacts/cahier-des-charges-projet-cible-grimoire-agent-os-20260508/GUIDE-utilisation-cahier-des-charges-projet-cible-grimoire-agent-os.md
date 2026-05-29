---
title: Guide d'utilisation - Cahier des charges projet cible Grimoire Agent OS
description: Comment utiliser le cahier des charges cible pour piloter les agents et la migration Memory OS.
author: Codex
date: 2026-05-08
---

# Guide d'utilisation - Cahier des charges projet cible Grimoire Agent OS

## Lire le paquet

Ordre conseille :

1. `README.md` pour la decision cible.
2. `CAHIER-DES-CHARGES-projet-cible-grimoire-agent-os.md` pour le produit cible.
3. `ARCHITECTURE-CIBLE-diagrammes.md` pour les flux et composants.
4. `SCHEMAS-CONTRATS-cibles.md` pour les contracts machine-readable.
5. `EXIGENCES-GATES-ACCEPTATION.md` pour les gates.
6. `DOSSIER-EXECUTION-AGENTS.md` pour lancer les lots agents.
7. `DOC-TECHNIQUE-cahier-des-charges-projet-cible-grimoire-agent-os.md` pour les decisions techniques.

## Utiliser la decision Weaviate Neo4j

La migration se pilote en mode non destructif.

Commandes utiles :

```bash
cd grimoire-kit
grimoire memory migrate plan
grimoire memory migrate export-bundle --bundle _grimoire/_memory/migration/weaviate-neo4j
```

Le bundle produit :

- `manifest.json` ;
- `memories.jsonl` ;
- `weaviate-objects.jsonl` ;
- `neo4j-import.cypher`.

## Gate de migration

Ne pas changer `memory.backend` vers `weaviate-server` tant que :

- `manifest.json` indique `vector_lossless: true` ;
- le nombre de records egale le nombre de vectors ;
- Weaviate contient les objets avec `source_id` ;
- Neo4j contient les nodes `GrimoireMemory` ;
- les checks de parite de recall passent.

## Donner une tache a un agent

Chaque tache doit citer :

- lot du dossier d'execution ;
- fichiers autorises ;
- guardrails ;
- preuve attendue ;
- gate de sortie.

Exemple :

```yaml
task:
  id: GAO-memory-001
  lot: LOT-G0
  objective: export qdrant migration bundle
  files:
    - grimoire-kit/src/grimoire/memory/migration.py
    - grimoire-kit/src/grimoire/cli/cmd_memory.py
  guardrails:
    - no qdrant cutover before vector_lossless
    - no secrets in repo
  evidence:
    - pytest target
    - migration manifest
  gate:
    - record_count equals vector_count for qdrant export
```

