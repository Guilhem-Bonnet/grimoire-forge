---
name: grimoire-performance-profiling
description: "Profiling et optimisation de performance. Diagnostic systématique des goulots d'étranglement. Use when: slow, performance, bottleneck, optimize, profiling, latency, memory usage, speed up, too slow, benchmark."
---

# Performance Profiling — Skill Grimoire

## Philosophie

L'optimisation prématurée est la racine de tous les maux (Knuth), mais l'ignorance systématique de la performance est la racine de tous les timeouts. Cette skill applique un diagnostic structuré : **mesurer d'abord, optimiser ensuite, vérifier toujours**.

## Quand utiliser cette skill

- Un outil ou test est "trop lent" (subjectif → on va le rendre objectif)
- Après ajout d'une feature, la suite de tests ralentit
- Avant une release, pour valider les performances
- Quand un utilisateur rapporte un problème de latence
- Pour baseline les performances avant un refactoring

## Process

### Phase 1 — Baseline : mesurer l'état actuel

**Règle d'or** : ne jamais optimiser sans baseline. On mesure AVANT de toucher quoi que ce soit.

#### Pour du code Python :

```bash
# Profiling CPU simple
python3 -m cProfile -s cumulative -m pytest tests/test_target.py 2>&1 | head -40

# Profiling avec output fichier (pour analyse détaillée)
python3 -m cProfile -o /tmp/profile.prof -m pytest tests/test_target.py
python3 -c "import pstats; p = pstats.Stats('/tmp/profile.prof'); p.sort_stats('cumulative'); p.print_stats(30)"

# Timing précis d'une fonction
python3 -m timeit -n 100 -r 5 "import module; module.function()"

# Memory profiling (si tracemalloc disponible)
python3 -c "
import tracemalloc
tracemalloc.start()
# ... code à profiler ...
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:10]:
    print(stat)
"
```

#### Pour la suite de tests :

```bash
# Identifier les tests les plus lents
python3 -m pytest tests/ --durations=20 -q 2>&1 | tail -30

# Profiler un test spécifique
python3 -m pytest tests/test_slow.py -v --tb=short --durations=0
```

#### Pour les I/O :

```bash
# Comptage d'appels filesystem
strace -c -e trace=file python3 script.py 2>&1 | tail -20

# Temps par opération I/O
strace -T -e trace=read,write,open,close python3 script.py 2>&1 | head -50
```

### Phase 2 — Identifier le goulot

Classifier le type de bottleneck :

| Type | Symptôme | Diagnostic |
|---|---|---|
| **CPU-bound** | Un seul core à 100%, temps constant | `cProfile` → fonction avec `cumtime` élevé |
| **I/O-bound** | Temps variable, CPU bas | `strace` → nombreux `read`/`write` ou `sleep` |
| **Memory-bound** | Croissance mémoire, swap, OOM | `tracemalloc` → allocations top |
| **Algorithmic** | Temps quadratique ou pire avec la taille | Complexité O(n²) dans les boucles imbriquées |
| **Serialization** | JSON/YAML lent sur gros fichiers | Benchmarker les appels `json.loads`/`yaml.load` |

### Phase 3 — Optimiser (ciblé)

**Principe** : optimiser UNIQUEMENT le goulot identifié en Phase 2. Pas de refactoring gratuit.

#### Stratégies par type :

**CPU-bound** :
- Cache avec `functools.lru_cache` ou dict local
- Algorithme plus efficace (set lookup vs list scan)
- Compilation avec `cython` ou `mypyc` (dernier recours)

**I/O-bound** :
- Batching des écritures (buffer → flush)
- Réduction du nombre de fichiers lus (cache, lazy load)
- JSONL streaming vs full file load

**Memory-bound** :
- `__slots__` sur les dataclasses
- Generators vs listes
- Weak references pour les caches

**Algorithmic** :
- Remplacer O(n²) par O(n log n) ou O(n)
- Index / lookup tables
- Early exit / short-circuit

### Phase 4 — Vérifier l'amélioration

```bash
# Re-exécuter le MÊME profiling que Phase 1
# Comparer les résultats côte à côte

# Format de comparaison :
# Baseline : X.XXs
# After    : Y.YYs
# Speedup  : Z.Zx
```

**Règle** : si le speedup est < 1.2x, l'optimisation ne vaut probablement pas la complexité ajoutée.

### Phase 5 — Rapport

```markdown
## Performance Report — [Contexte]

### Baseline
- Temps total : X.XXs
- Hotspot : `module.function()` (Y% du temps)

### Bottleneck identifié
- Type : [CPU/IO/Memory/Algorithmic]
- Cause : [description]
- Impact : [% du temps total]

### Optimisation appliquée
- Changement : [description]
- Fichier(s) : [paths]

### Résultat
| Métrique | Avant | Après | Ratio |
|---|---|---|---|
| Temps total | X.XXs | Y.YYs | Z.Zx |
| Mémoire peak | X MB | Y MB | Z.Zx |
| Tests passés | N/N | N/N | — |

### Learning capturé
[Si applicable — pattern réutilisable]
```

## Anti-patterns

| Anti-pattern | Correction |
|---|---|
| "J'ai un feeling que c'est lent" | Mesurer avec cProfile/timeit |
| Optimiser sans baseline | Phase 1 obligatoire |
| Optimiser partout | Cibler uniquement le hotspot |
| Micro-optimisation sans impact | Vérifier le speedup > 1.2x |
| Optimisation qui casse les tests | Toujours re-run la suite complète |

## Chaîne de skills

```
grimoire-performance-profiling → grimoire-writing-plans (si refactoring)
                               → grimoire-learnings (patterns découverts)
                               → grimoire-systematic-debugging (si regression)
```
