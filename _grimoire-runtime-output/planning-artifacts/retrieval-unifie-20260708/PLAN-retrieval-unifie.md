# Plan final — Retrieval unifié et trajectoire d'architecture grimoire-kit

Statut (2026-07-09) : toutes les phases déclenchées.

| Phase | État | Preuve |
| --- | --- | --- |
| 0 — bras « activé » | Campagne **terminée et jugée** (PR #71) : engagement 40/40, completed 15/40 vs 6/40 baseline, régressions −61,5 %, mais coût +47 % → verdict formel « non démontré » (composante coût) | Rapport `evals/reports/2026-07-09/` (bridge) |
| 1 — retrieval unifié | **Livrée** | PR #68 (rebasée sur main 3.23.0) : backends lexical/tantivy, RRF, CLI `--hybrid`/`reindex-lexical`/`sync-docs`, evals recall@k |
| 2 — résorption bash | Étape 1 **livrée** | PR #69 : inventaire `docs/resorption-bash.md` + `grimoire hooks` + fixes hooks sources |
| 3 — distribution | **Livrée** | PR #70 : uv tool install recommandé ; dualité wheel close depuis ADR-003 |

## Décision de fond : pas de changement de langage

L'évaluation de tantivy (moteur full-text Rust, classe Lucene) a conclu :

- **Port complet Go/Rust : écarté.** Environ 34 000 lignes de source et 62 000
  lignes de tests à porter, écosystème cible Python-first (MCP SDK,
  sentence-transformers, chromadb, ollama), démarrage CLI mesuré à 0,39 s
  (non bloquant pour un outil d'orchestration).
- **Rust là où il compte, via bindings :** le moteur tantivy est consommé au
  travers de `tantivy-py` (wheel binaire) sans posséder de code Rust.
- **Porte de sortie préservée :** l'interface retrieval unifiée constitue la
  couture le long de laquelle un moteur Rust isolé (binaire séparé ou module
  PyO3) pourrait être extrait si le besoin devenait réel (daemon haut débit,
  budget hooks inférieur à 50 ms).

## Phase 0 — Preuve de valeur (gate décisionnel)

Bras « activé » de la campagne d'évaluation web-app-todo — **lancé le
2026-07-09** (40 runs, 8 tâches × 5 reps, mêmes pins que la campagne
2026-07-03). Mécanisme d'activation pré-enregistré : hook SessionStart,
prompt de tâche inchangé (`evals/witnesses/web-app-todo/ACTIVATION.md`,
branche `evals/activated-arm-20260709` du bridge).

Le smoke run (fix-timezone-display) a montré un **engagement complet** du
standard : evidence-pack rempli, `gate check --strict` vert, `verify` sans
erreur — l'inverse du zéro-engagement de la campagne 2026-07-03. Le
jugement (grille JUDGING.md inchangée) et le rapport suivent la fin des
40 runs. Issues possibles :

- Effet démontré : la roadmap continue sur l'architecture actuelle.
- Pas d'effet : le mécanisme d'engagement du standard devient la priorité,
  avant tout investissement d'infrastructure.

## Phase 1 — Service retrieval unifié (IMPLÉMENTÉE)

Livrée sur la branche `feat/lexical-retrieval-fts5-tantivy` :

1. **Backend `lexical`** (SQLite FTS5, BM25, insensible aux diacritiques) —
   honore le contrat déjà déclaré dans le schéma de configuration mais jamais
   implémenté ; migration automatique du store JSON local.
2. **Backend `tantivy-local`** (extra `search`) — BM25 + stemming FR/EN,
   destiné aux corpus volumineux (code, docs).
3. **Fusion RRF** — module `grimoire.memory.retrieval`, `HybridRetriever`
   tolérant aux pannes, `MemoryManager.hybrid_search()` avec index compagnon
   lexical mirroré à chaque écriture.
4. **Résolution `auto`** — le défaut local devient `lexical` quand FTS5 est
   disponible ; `retrieval_mode: lexical` et `vector_database: false` forcent
   le lexical.

Voir `DOC-TECHNIQUE-retrieval-unifie.md` pour les détails d'implémentation et
`GUIDE-utilisation-retrieval-unifie.md` pour l'usage.

### Reste à faire en Phase 1 (chantiers suivants)

- Scopes `code` et `docs` : indexer les projections codegraph et la
  documentation projet dans `tantivy-local` (c'est la niche où tantivy
  surclasse FTS5).
- Evals retrieval : gold set requêtes/mémoires attendues, mesure de recall@k
  avant/après, branché sur le module `evals` existant.
- Surface CLI : exposer `hybrid_search` et `reindex_lexical_companion` dans
  `grimoire memory`.

## Phase 2 — Résorption du bash

- Inventaire des écarts entre `grimoire-init.sh` (environ 3 800 lignes) et
  `cmd_init.py` (la commande Python `grimoire init` existe déjà).
- Port des manques vers Python, réduction du `.sh` à un bootstrap mince
  (installation uv + grimoire-kit, exec `grimoire init`).
- Dépréciation puis suppression après un cycle de release.

## Phase 3 — Distribution

- `uv tool install grimoire-kit` comme voie d'installation officielle.
- Résolution de la dualité wheel restante.
- Si un binaire unique devient nécessaire pour des utilisateurs hors
  écosystème Python : artefact PyApp par release, pas de réécriture.

## Points d'environnement relevés pendant le chantier

- Le gate pre-commit Completion Contract résout `pytest` via le PATH système
  (Python 3.14 sans `typer`) au lieu du venv du projet — baseline locale
  cassée indépendamment du chantier ; 51 échecs de tests locaux identiques
  sur `main` (cwd-dépendants ou dépendances optionnelles absentes du venv).
  À corriger dans un chantier hygiène (candidat Phase 2).
