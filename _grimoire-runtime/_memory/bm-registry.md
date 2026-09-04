# BM-* Registry — Source de vérité numérotation

> **Statut** : canon. Toute création/archivage de concept BM-* passe par ce fichier.
> **Référence réglementaire** : ADR-S08 (pack maturation-agentique-20260421).
> **Dernière revue** : 22 avril 2026.

Ce registre gèle la numérotation des 60 identifiants `BM-*` utilisés dans le
dépôt. Il résout aussi les ambiguïtés historiques (mêmes IDs réutilisés pour
deux concepts différents selon les couches).

## Légende de statut

| Statut | Signification |
|---|---|
| **actif** | Concept fonctionnel, consommé par le runtime. |
| **partiel** | Artefact présent, pas branché dans la chaîne runtime ; durcissement en file. |
| **observable** | Concept exposé comme skill ponctuel, pas critique. |
| **archivé** | Remplacé ou jamais implémenté ; refs à nettoyer au fil des PR. |
| **réservé** | Numéro vide ; libre pour la prochaine création. |

## Canon de numérotation

| ID | Concept canonique | Statut | Lieu / preuve |
|---|---|---|---|
| BM-01 | — | réservé | — |
| BM-02 | workflow-status (human-readable) | actif | workflow-engine |
| BM-03 | Session state persistence | partiel | scripts présents, reprise non effective |
| BM-04 | — | réservé | — |
| BM-05 | Repo Map | actif | workflow `/repo-map` |
| BM-06 | Cross-workspace memory | partiel | `/memories/repo/` sans sync multi-repo |
| BM-07 | Context Router | actif | `src/grimoire/tools/context_router.py` |
| BM-08 | Agent contract tests | partiel | infra tests ok, pas de contrat unifié |
| BM-09 | — | réservé | — |
| BM-10 | — | réservé | — |
| BM-11 | Boomerang task chains (sequential) | actif | team-build |
| BM-12 | — | réservé | — |
| BM-13 | — | réservé | — |
| BM-14 | — | réservé | — |
| BM-15 | Team Grimoire standard | actif | teams documentées |
| BM-16 | Team dispatcher | actif | `apps/grimoire-game/src/server/` |
| BM-17 | Team observability | actif | intégré `mission-board` |
| BM-18 | Team status surface | partiel | Mission Board mock, pas branché sur bus V1 |
| BM-19 | Stigmergy signals | partiel | `stigmergy.py` présent, consumers absents |
| BM-20 | Pheromone board | partiel | `pheromone-board.json` non exploité par surfaces |
| BM-21 | Dream consolidation offline | observable | skill `grimoire-dream` |
| BM-22 | Qdrant structured memory | partiel | CLI `grimoire memory` (le pont `mem0-bridge.py` est retiré depuis 3.35.0), Qdrant off par défaut |
| BM-23 (historique : Semantic routing) | **ambigu** — voir §Ambiguïtés | archivé (sémantique) / actif (extension) | réassigné |
| BM-24 | — | réservé | — |
| BM-25 | Agent memory | actif | `_grimoire-runtime/_memory/` |
| BM-26 | Memory coherence linter | actif | `memory_lint.py` |
| BM-27 | Antifragile scoring | observable | skill `grimoire-antifragile` |
| BM-28 | Handoff log | actif | `_memory/handoff-log.md` |
| BM-29 | Decisions log | actif | `_memory/decisions-log.md` |
| BM-30 | Failure museum | actif | `_memory/failure-museum.md` |
| BM-31 | Contradiction log | partiel | fichier présent, détecteur absent |
| BM-32 | Incubator / R&D engine | observable | skill `grimoire-innovate` |
| BM-33 | — | réservé | — |
| BM-34 | — | réservé | — |
| BM-35 | — | réservé | — |
| BM-36 | — | réservé | — |
| BM-37 | — | réservé | — |
| BM-38 | Shell completions | actif | `grimoire-completion.zsh` |
| BM-39 | — | réservé | — |
| BM-40 | Multi-LLM canary | observable | tasks `multi-llm-canary` |
| BM-41 | Semantic cache LLM | partiel | `semantic-cache.py` hors chaîne LLM |
| BM-42 | LLM Router | actif | `llm_router.py` |
| BM-43 | Token budget | actif | `token_budget.py` |
| BM-44 | Agent lint | actif | `agent_lint.py` |
| BM-45 | Compiled flow | actif | `compiled_flow.py` |
| BM-46 | Agent Darwinism | partiel | script sans évaluation périodique |
| BM-47 | — | réservé | — |
| BM-48 | — | réservé | — |
| BM-49 | — | réservé | — |
| BM-50 | HUP (Hallucination Unblock Protocol) | actif | appliqué par SOG |
| BM-51 | QEC (Question Expansion Cluster) | actif | batching SOG |
| BM-52 | CVTL (Cross-Validation Trigger Layer) | actif | sorties critiques |
| BM-53 | SOG (Smart Orchestrator Gateway) | actif | agent unique user-facing |
| BM-54 | PCE (Party Chat Engine) | actif | skill `grimoire-brainstorming` |
| BM-55 | ALS (Autonomy Level System) | actif | `agent-base.md` |
| BM-56 | Friction budget | observable | skill `grimoire-friction-management` |
| BM-57 | ARG (Agent Relationship Graph) | actif | routing SOG |
| BM-58 | Proactive Initiative Protocol (PIP) | actif | comportement SOG |
| BM-59 (historique : ELSS) | **ambigu** — voir §Ambiguïtés | actif (event log V1) / archivé (ELSS) | réassigné |
| BM-60 | — | réservé | — |

## Ambiguïtés résolues

Le repo a deux identifiants re-attribués à deux concepts différents selon les
couches. Le registre tranche et documente la décision.

### BM-23 — double affectation

- **Référence cartographie** [04-CARTOGRAPHIE-concepts.md](../../_grimoire-runtime-output/planning-artifacts/maturation-agentique-20260421/04-CARTOGRAPHIE-concepts.md) : "Semantic routing à 3 niveaux" — à archiver car remplacé par `llm_router.py`.
- **Référence framework** [grimoire-kit/framework/copilot-extension/README.md](../../grimoire-kit/framework/copilot-extension/README.md) : "Grimoire Copilot Extension `@grimoire` — BM-23".
- **Décision registre** :
  - Le concept "Semantic routing 3-niveaux" est **archivé** (ADR-S09). Aucun code `semantic_routing*.py` n'existe.
  - Le label BM-23 reste **actif** pour la Copilot Extension (usage de fait dans le framework).
  - La mention "Semantic routing" dans `04-CARTOGRAPHIE-concepts.md` est une erreur historique ; le concept n'a jamais été implémenté sous ce numéro.

### BM-59 — double affectation

- **Référence cartographie** : "ELSS (Event-Linked Skill Selection)" — à archiver.
- **Référence framework** (~20 fichiers) : "Event Log & Shared State" — bus d'événements persistant.
- **Décision registre** :
  - Le concept "ELSS" nominal est **archivé** (jamais implémenté comme tel). Le dispatch événement→skill est absorbé par SOG (BM-53).
  - Le label BM-59 est **réaffecté canoniquement** à "Event Log & Shared State", qui correspond au bus V1 (`HookEvent`, `activity.jsonl`, contrat `src/grimoire/tools/events.py`). Les ~20 mentions existantes dans `grimoire-kit/framework/` restent valides.

> **Action de nettoyage non bloquante** : au fil des PR, supprimer les mentions
> de "ELSS" dans les commentaires/docs qui citent encore l'acronyme obsolète.
> Les liens vers `event-log-shared-state.md` restent corrects.

## Concepts à durcir (file V4-concepts-durcissement)

Les 10 concepts partiels suivants sont en file de durcissement. Chaque ID a
une story stub dans [V4-concepts-durcissement/](../../_grimoire-runtime-output/planning-artifacts/V4-concepts-durcissement/).

BM-03, BM-06, BM-08, BM-18, BM-19, BM-20, BM-22, BM-31, BM-41, BM-46

Vague courante prioritaire (ADR-S09 §S4.4) : **BM-19 (stigmergy consumers)**,
**BM-20 (pheromone board UI)**, **BM-31 (contradiction detector)**.

## Concepts archivés (fin de vie)

| ID historique | Concept mort | Remplacé par |
|---|---|---|
| BM-23 "Semantic routing 3-niveaux" | jamais implémenté | `llm_router.py` (BM-42) |
| BM-59 "ELSS nominal" | jamais implémenté | SOG dispatch (BM-53) + bus V1 `HookEvent` |

## Règles de numérotation future

1. **Un numéro = un concept canonique.** Pas de réutilisation.
2. **Avant création**, vérifier les trous `réservé` ci-dessus. Utiliser le plus petit disponible.
3. **Après création**, ajouter la ligne au tableau canon avec statut initial (au moins `partiel`).
4. **Archivage** : laisser le numéro dans le registre avec statut `archivé` et une ligne dans §Concepts archivés. Ne pas réutiliser le numéro.

## Références

- Cartographie d'origine : [04-CARTOGRAPHIE-concepts.md](../../_grimoire-runtime-output/planning-artifacts/maturation-agentique-20260421/04-CARTOGRAPHIE-concepts.md)
- Décision canon : ADR-S08 dans [05-DECISIONS-rationalisation.md](../../_grimoire-runtime-output/planning-artifacts/maturation-agentique-20260421/05-DECISIONS-rationalisation.md)
- Archivages : ADR-S09 dans le même pack
