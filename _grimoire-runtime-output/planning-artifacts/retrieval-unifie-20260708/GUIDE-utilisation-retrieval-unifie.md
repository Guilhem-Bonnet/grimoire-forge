# GUIDE — Utiliser le retrieval unifié de grimoire-kit

## Choisir son backend

| Besoin | Configuration `project-context.yaml` |
| --- | --- |
| Défaut sans service (BM25 local) | `memory.backend: auto` (résout vers `lexical` si FTS5 disponible) |
| Forcer le lexical pur, même avec serveur configuré | `memory.retrieval_mode: lexical` ou `memory.vector_database: false` |
| Stemming FR/EN, gros corpus | `memory.backend: tantivy-local` + `pip install grimoire-kit[search]` |
| Hybride vecteur + BM25 | backend vectoriel (qdrant/weaviate/ollama) — le compagnon lexical est créé automatiquement |

## Exemples

### Lexical par défaut (aucune dépendance)

```yaml
memory:
  backend: auto
```

```python
from grimoire.core.config import GrimoireConfig
from grimoire.memory.manager import MemoryManager

mgr = MemoryManager.from_config(config, project_root=root)
mgr.store("harmonisation des grimoires")
mgr.search("harmonisation")   # BM25, insensible aux accents
```

Le store JSON legacy (`_grimoire/_memory/{prefix}.json`) est migré
automatiquement au premier démarrage (IDs et timestamps préservés).

### Tantivy (stemming français)

```yaml
memory:
  backend: tantivy-local
```

```python
mgr.store("harmonisation des grimoires")
mgr.search("harmonisé")       # matche grâce au stemming fr_stem
```

### Recherche hybride (backend vectoriel + compagnon lexical)

```yaml
memory:
  backend: auto
  qdrant_url: http://localhost:6333
```

```python
results = mgr.hybrid_search("décision architecture qdrant", limit=5)
```

- Chaque écriture (`store`, `remember`, `update`, `upsert`, `delete`) est
  mirrorée dans le compagnon FTS5 — aucun geste supplémentaire.
- Projet existant avec mémoires antérieures au compagnon :

```python
mgr.reindex_lexical_companion()   # backfill complet, retourne le nombre d'entrées
```

- Si le serveur vectoriel tombe, `hybrid_search` continue sur le lexical
  seul (panne enregistrée, pas d'exception).

## Fusion RRF hors manager

```python
from grimoire.memory.retrieval import HybridRetriever

retriever = HybridRetriever([("vector", qdrant_backend), ("lexical", fts_backend)])
results = retriever.search("requête", limit=5)
print(retriever.issues)   # pannes éventuelles par backend
```

## Limites connues

- Le compagnon lexical n'est créé que pour les backends vectoriels avec
  `retrieval_mode: vector` ; `mempalace` n'en bénéficie pas pour l'instant.
- `tantivy-local` filtre `user_id` en post-traitement (sur-échantillonnage) :
  exact mais moins efficace qu'un filtre natif sur de très gros volumes.
- Les scopes `code` et `docs` (indexation codegraph/documentation dans
  tantivy) sont cadrés mais pas encore implémentés — voir le plan.
