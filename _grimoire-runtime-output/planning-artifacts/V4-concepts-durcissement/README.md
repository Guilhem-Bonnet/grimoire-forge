# V4 — Concepts durcissement

> File de stories L2 pour durcir les 10 concepts partiels listés dans
> [bm-registry.md](../../../_grimoire-runtime/_memory/bm-registry.md#concepts-à-durcir-file-v4-concepts-durcissement).
> Chaque story est un stub ; elle sera détaillée en PRD/DOC technique
> quand la vague correspondante démarre.

## Priorisation ADR-S09 (vague courante V4.4)

- **S4.4.a** BM-19 Stigmergy consumer — [S4.4.a-BM-19-stigmergy-consumer.md](S4.4.a-BM-19-stigmergy-consumer.md)
- **S4.4.b** BM-20 Pheromone board surface — [S4.4.b-BM-20-pheromone-board-surface.md](S4.4.b-BM-20-pheromone-board-surface.md)
- **S4.4.c** BM-31 Contradiction detector — [S4.4.c-BM-31-contradiction-detector.md](S4.4.c-BM-31-contradiction-detector.md)

## File complète (backlog)

| ID | Concept | Lieu actuel | Manque | Priorité |
|---|---|---|---|---|
| BM-19 | Stigmergy signals | `src/grimoire/tools/stigmergy.py` | consumers réels | P1 |
| BM-20 | Pheromone board | `_grimoire-output/pheromone-board.json` | rendu surface | P1 |
| BM-31 | Contradiction log | `_memory/contradiction-log.md` | détecteur auto | P1 |
| BM-03 | Session state persistence | scripts présents | reprise effective entre sessions | P2 |
| BM-18 | Team status surface | Mission Board mock | câblage bus V1 → cartes | P2 |
| BM-08 | Agent contract tests | infra vitest/pytest | contrat unifié cross-agent | P2 |
| BM-06 | Cross-workspace memory | `/memories/repo/` | sync multi-repo | P3 |
| BM-22 | Qdrant structured memory | `mem0-bridge.py` | Qdrant démarré par défaut | P3 |
| BM-41 | Semantic cache LLM | `semantic-cache.py` | insertion dans chaîne LLM | P3 |
| BM-46 | Agent Darwinism | script présent | évaluation périodique | P3 |

## Critères de sortie de la file

- P1 livrés et visibles dans au moins une surface (test e2e).
- P2 tranchés (livrés ou reclassés archivé).
- P3 décidés : durcis ou archivés selon usage réel observé.

## Convention stub

Chaque story stub contient :

1. **Objectif livrable** — une phrase.
2. **Chemin de preuve** — où l'usager voit l'effet (surface, log, skill).
3. **Dépendances** — BM-* ou vagues prérequis.
4. **Out of scope** — ce qui n'est pas traité.

Les PRD complets ne sont pas produits tant que la story n'est pas en
cours (ADR-S12 : la doc suit l'exécution).
