---
title: Doc technique - Cahier des charges projet cible Grimoire Agent OS
description: Decisions techniques, sources et preuves attendues pour le cahier des charges cible.
author: Codex
date: 2026-05-08
---

# Doc technique - Cahier des charges projet cible Grimoire Agent OS

## Decision memoire

La combinaison Weaviate + Neo4j est retenue comme cible Memory OS.

Raison :

- Weaviate couvre le store vectoriel, la recherche semantique, la recherche hybride, les objets avec vecteurs custom et les APIs REST GraphQL gRPC ;
- Neo4j couvre le graphe de connaissance, les relations typed, les traversals Cypher, les vector indexes et les usages GraphRAG ;
- Grimoire a besoin des deux plans : similarite semantique pour recall, graphe causal pour tasks, evidence, files, decisions, incidents et packs.

Qdrant reste source de migration tant que la parite n'est pas prouvee.

## Sources primaires consultees

- Weaviate docs, vector database, semantic and hybrid search, RAG and APIs : <https://github.com/weaviate/docs/blob/main/docs/weaviate/index.mdx>
- Weaviate docs, APIs REST GraphQL gRPC : <https://github.com/weaviate/docs/blob/main/docs/weaviate/api/index.mdx>
- Weaviate docs, custom vectors and import patterns : <https://github.com/weaviate/docs/blob/main/_includes/code/quickstart.byov.schema.mdx>
- Neo4j docs, property graph concepts : <https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/>
- Neo4j docs, vector indexes and GraphRAG examples : <https://neo4j.com/docs/neo4j-graphrag-python/current/>
- Qdrant docs, snapshots, points, payloads and vector retrieval : <https://github.com/qdrant/qdrant/blob/master/docs/QUICK_START.md>

## Implementation commencee

Surfaces modifiees :

- config Memory OS reconnait `weaviate-server` ;
- schema JSON reconnait Weaviate, Neo4j et les champs de migration ;
- validator accepte les nouveaux champs ;
- status Memory OS explique Qdrant comme source de migration et Weaviate + Neo4j comme cible ;
- CLI ajoute `grimoire memory migrate plan` et `grimoire memory migrate export-bundle` ;
- bundle de migration preserve ids, payloads, objets Weaviate et projection Cypher Neo4j ;
- compose target local ajoute Weaviate et Neo4j.

## Regle de cutover

Le cutover vers `memory.backend: weaviate-server` est interdit tant que :

- Qdrant exporte un bundle ;
- `record_count == vector_count` ;
- `weaviate-objects.jsonl` contient `source_id` pour chaque objet ;
- `neo4j-import.cypher` contient les nodes et tags de base ;
- la recherche de parite retourne les memes ids source pour un set de requetes de controle ;
- les secrets Weaviate et Neo4j ne sont pas ecrits dans le repo.

## Risques

| Risque | Controle |
| --- | --- |
| Perte de vecteurs pendant migration | export Qdrant avec `with_vectors` et gate `vector_lossless` |
| Re-embedding non controle | vectors custom Weaviate depuis bundle |
| Divergence ids | `source_id` Weaviate et `id` Neo4j |
| Secrets en clair | variables `GRIMOIRE_WEAVIATE_API_KEY`, `GRIMOIRE_NEO4J_PASSWORD`, `GRIMOIRE_NEO4J_AUTH` |
| Graphe trop tot declare ready | status `planned` tant que l'adapter Neo4j n'est pas branche |

