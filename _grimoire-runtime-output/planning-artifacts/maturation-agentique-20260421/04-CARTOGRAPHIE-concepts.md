# 04 — Cartographie des concepts BM-*

> 42 identifiants `BM-*` référencés dans `.github/`, `_grimoire-runtime/` et `grimoire-kit/framework/`. Tri par statut opérationnel.

## Méthodologie

Pour chaque concept :

- **Fonctionnel** : le code correspondant existe dans `src/grimoire/tools/` ou `framework/tools/`, est testé, et utilisé dans le runtime (hook, workflow, ou skill).
- **Partiel** : doc + script présent, mais pas branché dans la chaîne runtime (aucun consommateur réel).
- **Théorique** : uniquement référencé en prose, aucun artefact exécutable correspondant.

## Classement complet

### Fonctionnels (24 concepts, à garder et maintenir)

| ID | Concept | Preuve d'activité |
|---|---|---|
| BM-02 | workflow-status (human-readable) | Référencé dans workflow-engine |
| BM-05 | Repo Map | Utilisé par workflow `/repo-map` |
| BM-07 | Context Router | `src/grimoire/tools/context_router.py` actif |
| BM-11 | Boomerang task chains (sequential) | Pattern utilisé par team-build |
| BM-15 | Team Grimoire standard | Teams documentées + active |
| BM-16 | Team dispatcher | `apps/grimoire-game/src/server/` |
| BM-17 | Team observability | Intégré `mission-board` mock |
| BM-25 | Agent memory | `_grimoire-runtime/_memory/` actif |
| BM-26 | Memory coherence linter | `src/grimoire/tools/memory_lint.py` |
| BM-28 | Handoff log | `_grimoire-runtime/_memory/handoff-log.md` |
| BM-29 | Decisions log | `_grimoire-runtime/_memory/decisions-log.md` |
| BM-30 | Failure museum | `_grimoire-runtime/_memory/failure-museum.md` |
| BM-38 | Shell completions | `grimoire-completion.zsh` actif |
| BM-42 | LLM Router | `src/grimoire/tools/llm_router.py` canonique |
| BM-43 | Token budget | `src/grimoire/tools/token_budget.py` canonique |
| BM-44 | Agent lint | `src/grimoire/tools/agent_lint.py` canonique |
| BM-45 | Compiled flow | `src/grimoire/tools/compiled_flow.py` canonique |
| BM-50 | HUP (Hallucination Unblock Protocol) | Appliqué par SOG |
| BM-51 | QEC (Question Expansion Cluster) | Batching actif |
| BM-52 | CVTL (Cross-Validation Trigger Layer) | Déclenché sur sorties critiques |
| BM-53 | SOG (Smart Orchestrator Gateway) | Runtime complet, agent unique |
| BM-54 | PCE (Party Chat Engine) | Skill `grimoire-brainstorming` |
| BM-55 | ALS (Autonomy Level System) | Documenté dans `agent-base.md` |
| BM-57 | ARG (Agent Relationship Graph) | Utilisé par routing SOG |

### Partiels (10 concepts, à durcir ou brancher)

| ID | Concept | Où ça coince |
|---|---|---|
| BM-03 | Session state persistence | Scripts existent, pas de reprise réelle entre sessions |
| BM-06 | Cross-workspace memory | `/memories/repo/` utilisé, pas de sync multi-repo |
| BM-08 | Agent contract tests | Infrastructure test présente, pas de contrat unifié (à reprendre D3 hooks) |
| BM-18 | Team status surface | Visible dans Mission Board mock, pas branché sur vrai bus |
| BM-19 | Stigmergy signals | `src/grimoire/tools/stigmergy.py` canonique, mais consumers absents |
| BM-20 | Pheromone board | `_grimoire-output/pheromone-board.json` existe, pas exploité par surfaces |
| BM-22 | Qdrant structured memory | `mem0-bridge.py` présent, Qdrant non démarré par défaut |
| BM-31 | Contradiction log | Fichier existe, pas de détecteur automatique |
| BM-41 | Semantic cache LLM | `semantic-cache.py` existe, pas dans chain LLM |
| BM-46 | Agent Darwinism | Script existe, pas d'évaluation périodique actuelle |

### Théoriques (8 concepts, décision à prendre)

| ID | Concept | Recommandation |
|---|---|---|
| BM-21 | Dream consolidation offline | Garder : skill `grimoire-dream` actif même si usage ponctuel |
| BM-23 | Semantic routing à 3 niveaux | Archiver : remplacé par `llm_router.py` V1 |
| BM-27 | Antifragile scoring | Garder : skill `grimoire-antifragile` utile |
| BM-32 | Incubator / R&D engine | Garder : skill `grimoire-innovate` en backlog |
| BM-40 | Multi-LLM canary | Garder : tasks `multi-llm-canary` actives |
| BM-56 | Friction budget | Garder : skill `grimoire-friction-management` documenté |
| BM-58 | Proactive Initiative Protocol (PIP) | Garder : comportement SOG |
| BM-59 | ELSS (Event-Linked Skill Selection) | Archiver : non implémenté, SOG dispatche autrement |

## Matrice de décision synthétique

| Action | Nombre | Liste |
|---|---|---|
| **Garder actif** | 24 | BM-02, 05, 07, 11, 15, 16, 17, 25, 26, 28, 29, 30, 38, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 57 |
| **Durcir (brancher la chaîne réelle)** | 10 | BM-03, 06, 08, 18, 19, 20, 22, 31, 41, 46 |
| **Garder mais observer seulement** | 6 | BM-21, 27, 32, 40, 56, 58 |
| **Archiver (documenter la fin de vie)** | 2 | BM-23, 59 |

## Trous de numérotation

Identifiants **non trouvés** en référence dans le code : BM-01, BM-04, BM-09, BM-10, BM-12, BM-13, BM-14, BM-24, BM-33, BM-34, BM-35, BM-36, BM-37, BM-39, BM-47, BM-48, BM-49.

**Interprétation** : soit ces IDs ont été redistribués, soit ils correspondent à des concepts abandonnés sans trace. Décision en V4 : produire `_grimoire-runtime/_memory/bm-registry.md` comme source de vérité unique pour figer la numérotation et documenter les archivages.

## Pont avec les GM-*

Les identifiants GM-* viennent du benchmark Game UI ([docs/exploitation/benchmark-github-agent-os-game-ui.md](../../../docs/exploitation/benchmark-github-agent-os-game-ui.md)). Ils couvrent un axe différent (surfaces visuelles) et doivent rester séparés.

Cross-ref partielle pertinente pour ce pack :

| GM-* | BM-* associé | Statut pack |
|---|---|---|
| GM-15 (Office view) | — | V3 |
| GM-16 (Event→sprite mapping) | BM-19 (stigmergy) | V3 |
| GM-17 (Sub-agent visualization) | BM-57 (ARG) | V3 |
| GM-27 (Timeline scrubber) | BM-21 (dream) | V3 (optionnel) |

## Action immédiate recommandée (V4)

1. Produire `_grimoire-runtime/_memory/bm-registry.md` (source de vérité numérotation)
2. Pour chaque concept "durcir" : ouvrir une story L2 dans le prochain pack V4
3. Pour chaque concept "archiver" : ajouter une note `# ARCHIVED BM-23 — <date> — <motif>` en tête du fichier concerné puis supprimer les références mortes
4. Mettre à jour [.github/copilot-instructions.md](../../../.github/copilot-instructions.md) pour ne citer que les 24 actifs + 10 durcis
