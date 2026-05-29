# Migration Weaviate + Neo4j - Etat du 2026-05-08

## Portee

Migration Memory OS depuis Qdrant vers:

- Weaviate pour le store vectoriel durable.
- Neo4j pour la projection graphe des memoires et tags.

Le cutover applicatif est effectue vers Weaviate. Qdrant reste configure comme source de migration et rollback temporaire.

## Etat realise

- Acces Docker corrige: `guilhem` ajoute au groupe `docker`.
- Stack cible demarree via `docker-compose.memory-target.yml`.
- Weaviate cible joignable sur `http://localhost:8080`, version `1.35.19`.
- Neo4j cible joignable sur `http://localhost:7474` et `neo4j://localhost:7687`, version `5.26.25`.
- Stack Docker cible stabilisee: images pinnees `semitechnologies/weaviate:1.35.19` et `neo4j:5.26.25`, healthchecks actifs.
- Template de stack cible ajoute pour les nouveaux projets `weaviate-server`.
- `grimoire init --backend weaviate-server` genere maintenant la config Weaviate + Neo4j, le compose cible, et active l'agent `vectus`.
- Taches VS Code ajoutees: `grimoire: memory-stack:up`, `grimoire: memory:verify`, `grimoire: memory:status`.
- Qdrant source joignable sur `http://localhost:6333`.
- Collections detectees: `grimoire`, `grimoire-conversations`, `grimoire_kit`.
- Collections Qdrant migrees: `grimoire`, `grimoire-conversations`, `grimoire_kit`.
- Export bundle genere dans `grimoire-kit/_grimoire/_memory/migration/weaviate-neo4j`.
- Bundle lossless: `record_count=68`, `vector_count=68`, `vector_lossless=true`.
- Import Weaviate execute: `68` objets dans la collection `GrimoireKitMemory`.
- Import Neo4j execute: `165` statements Cypher.
- Controle Weaviate: `68` objets.
- Controle Neo4j: `68` noeuds `GrimoireMemory`, `26` relations `TAGGED_WITH`, `68` noeuds `WeaviateObject`, `68` relations `VECTORIZED_AS`.
- Gate `grimoire memory migrate verify`: OK, bundle `68` records, Weaviate `68` objets, Neo4j `68` memoires et `26` relations.
- Cutover `project-context.yaml`: `memory.backend` passe de `qdrant-server` a `weaviate-server`.
- Smoke backend cible: `grimoire memory status` voit `Backend: weaviate-server`, `Entries: 68`.
- Adaptateur runtime Neo4j ajoute: `MemoryManager` synchronise `store`, `store_many`, `update`, `delete`, `facts` et `diary` vers `Neo4jMemoryGraph` quand la couche Neo4j est configuree.
- Producteurs Neo4j ajoutes pour `code_graph` et `task_memory`: `grimoire memory graph sync-code`, `sync-tasks`, `verify`.
- Projection code graph stabilisee: ecriture Neo4j par batch, materialisation des noeuds externes/imports en placeholders, arêtes dedupliquees selon `(source, cible, type)`.
- Gate graph final: `sync-code --paths src,tests` produit `362` fichiers; Neo4j contient `14346` `CodeNode` avec placeholders externes et `45175` `CODE_EDGE` apres resync.
- Projection task memory verifiee: commande `sync-tasks` operationnelle; ledger local vide donc `0` mission, `0` tache, `0` evidence.
- Projection vectorielle code ajoutee: `grimoire memory vector sync-code --paths src,tests` ecrit `362` chunks Weaviate deterministes et les relie aux `CodeNode` via `MEMORY_FOR`.
- Projection vectorielle task ajoutee: `grimoire memory vector sync-tasks` ecrit missions, taches, events, incidents, evidence packs et verdicts quand le ledger contient des donnees; etat local actuel `0`.
- Gate vectoriel ajoute: `grimoire memory vector verify --paths src,tests` verifie `362` projections attendues, `362` presentes, par `content_hash`.
- Gate Memory OS unifie ajoute: `grimoire memory gate` orchestre migration Weaviate/Neo4j, sync optionnel code/task graph, verification vectorielle code/task, puis verification Neo4j.
- References bidirectionnelles ajoutees: Weaviate porte `weaviate_id` et `neo4j_memory_id`; Neo4j materialise `WeaviateObject` et les relations `VECTORIZED_AS` / `VECTOR_FOR`.
- Liens runtime ajoutes: les projections vectorielles portent `projection_group` et sont reliees aux sources graph via `MEMORY_FOR`; la verification migration ignore ces projections pour rester centree sur le bundle Qdrant.
- Promotion task-flow ajoutee: tasks `grimoire: memory:gate-shadow` et `grimoire: memory:gate`; `flow-quick` et `flow-full` executent le gate shadow non bloquant.
- Guardrail hook ajoute: `grimoire-memory-gate` en `PostToolUse`, mode `shadow`, avec verification no-sync/no-migration pour signaler les drifts sans bloquer.
- CI cible ajoutee: workflow `Memory OS Gate` path-limite, demarre `docker-compose.memory-target.yml`, attend Weaviate + Neo4j, synchronise les projections vectorielles, lance `grimoire memory gate --skip-migration`, puis execute `memory migrate verify` si le bundle est present.
- Wrapper Docker local ajoute: `.github/hooks/scripts/grimoire-docker.sh` tente `docker`, puis bascule sur `sg docker -c ...` quand le shell courant n'a pas encore recharge le groupe `docker`.
- Statut Memory OS cible: `semantic_memory=ready`, `semantic_knowledge=partial`, `memory_graph=partial`, `code_graph=partial`, `task_memory=partial`.
- Smoke export cible: `grimoire memory export` retourne les entrees Weaviate courantes.
- Validation projet `grimoire-kit`: `project-context.yaml is valid`.
- Tests cibles apres cutover: suite complete `6399 passed, 2 skipped`.
- Tests Neo4j runtime cibles: `51 passed` sur `test_manager.py`, `test_architecture.py`, `test_neo4j_graph.py`.
- Tests complets `grimoire-kit`: `6399 passed`, `2 skipped` avec extra `dev`.
- `memory status` avec l'extra Qdrant: backend `qdrant-server` sain, collection active `grimoire_kit`, `0` entree.

## Snapshots Qdrant crees

- `grimoire_kit-388483986198339-2026-05-08-12-51-41.snapshot`
  - size: `149504`
  - checksum: `8f488b94c9f1dbde5d288ede670ca1b81a378509bc767e0ced4b4edd331805c5`
- `grimoire-388483986198339-2026-05-08-12-51-50.snapshot`
  - size: `128512`
  - checksum: `5fb16da09efe922c942d170303e6cf9c2d075559a02bd843330cf03c75b53e11`
- `grimoire-conversations-388483986198339-2026-05-08-12-51-50.snapshot`
  - size: `313856`
  - checksum: `d7196ae24dba7310dd6fdf91573fff3c064341973f908a053baaf9a89736d8e6`

## Incident corrige

Docker etait installe et le daemon etait actif, mais l'utilisateur courant n'avait pas acces au socket:

- socket: `/var/run/docker.sock`
- owner: `root:docker`
- fix applique: `sudo -n usermod -aG docker guilhem`
- reprise immediate: commandes Docker executees via `sg docker -c '...'`

Une reconnexion complete de session rendra le groupe `docker` actif sans wrapper `sg docker`.

## Commandes de reprise

```bash
sg docker -c 'docker compose -f docker-compose.memory-target.yml up -d'
```

Puis dans `grimoire-kit`:

```bash
uv run grimoire memory migrate import-weaviate \
  --bundle _grimoire/_memory/migration/weaviate-neo4j \
  --weaviate-url http://localhost:8080

export GRIMOIRE_NEO4J_PASSWORD=grimoire-dev-password
uv run --extra neo4j grimoire memory migrate import-neo4j \
  --bundle _grimoire/_memory/migration/weaviate-neo4j \
  --neo4j-uri neo4j://localhost:7687

GRIMOIRE_NEO4J_PASSWORD=grimoire-dev-password uv run --extra neo4j grimoire memory migrate verify \
  --bundle _grimoire/_memory/migration/weaviate-neo4j
```

## Gates avant cutover

- Weaviate contient `68` objets importes depuis le bundle dans `GrimoireKitMemory` et `362` projections vectorielles code supplementaires: valide.
- Neo4j contient `68` noeuds `GrimoireMemory` importes et les projections runtime supplementaires: valide.
- Neo4j contient les relations `TAGGED_WITH` attendues: `26` relations importees.
- Neo4j contient les references vectorielles attendues: `68` noeuds `WeaviateObject`, `68` relations `VECTORIZED_AS`.
- Neo4j contient les references vectorielles runtime attendues apres projection: `430` noeuds `WeaviateObject`, `430` relations `VECTORIZED_AS`, `362` relations `MEMORY_FOR`.
- Gate ids source bundle -> Weaviate -> Neo4j: valide.
- Gate vectoriel code/task: valide.
- Gate unifie `grimoire memory gate`: valide en mode strict.
- Smoke search/list/export sur Weaviate: valide.
- Cutover applicatif aligne: la collection active Weaviate `GrimoireKitMemory` contient les collections Qdrant exportees.
- `memory.backend` est bascule vers `weaviate-server`.
- Garder Qdrant en rollback temporaire tant que le hook `grimoire-memory-gate` reste en `shadow`.
- Statut Memory OS aligne avec le reel: projection Neo4j runtime signalee `partial`, pas `ready`.

## Suite technique

- Promouvoir `grimoire-memory-gate` de `shadow` vers `canary`, puis `enforced`, apres validation recurrente.
- Ajouter des chunks symbole/test plus fins et alimenter le ledger task avec les vraies missions agents.
- Decider si les collections Qdrant sources doivent rester fusionnees dans `GrimoireKitMemory` ou etre separees par collection Weaviate dediee.
- Apres reconnexion de session, verifier que `docker` fonctionne sans `sg docker -c`.
