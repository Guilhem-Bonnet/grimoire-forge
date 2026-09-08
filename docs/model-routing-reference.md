# Routing des modèles et diagnostics runtime

Référencé depuis `.github/copilot-instructions.md`. Alignement avec les recommandations
VS Code wiki (Getting Started + Performance & Diagnostics).

## Politique de choix de modèle (task-aware)

**Architecture SOG pur + Auto-first** — les agents n'ont pas de `model:` dans leur frontmatter. Le routing est géré entièrement par le SOG, avec fallback dynamique.
Source de vérité complète : `_grimoire-runtime/_config/model-routing.yaml`
Base de décision :
- [Supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models)
- [Model comparison](https://docs.github.com/en/copilot/reference/ai-models/model-comparison)
Commande override session : `/set-model <agent|all|reset> <model-id|auto>` — ex: `/set-model dev gpt-5.3-codex`

| Profil de routing | Primary | Preferred (ordre de fallback) | Agents par défaut |
|---|---|---|---|
| **deep_reasoning** | `auto` | `gpt-5.4`, `gpt-5.3-codex`, `claude-opus-4.6`, `gemini-3.1-pro`, `gemini-2.5-pro` | `grimoire-master`, `rodin`, `architect`, `creative-problem-solver`, `innovation-strategist` |
| **general_code** | `auto` | `gpt-5.3-codex`, `gpt-5-mini`, `claude-sonnet-4.6`, `gemini-2.5-pro` | `dev`, `quick-flow-solo-dev`, `qa`, `tea` |
| **writing_structured** | `auto` | `gpt-5-mini`, `claude-sonnet-4.6`, `gemini-3-flash` | `pm`, `analyst`, `sm`, `tech-writer`, `ux-designer`, `art-director`, `storyteller`, `presentation-master`, `workflow-builder`, `agent-builder`, `module-builder` |
| **fast_iter** | `auto` | `gpt-5.4-mini`, `gpt-5-mini`, `claude-haiku-4.5`, `gemini-3-flash` | `brainstorming-coach`, `design-thinking-coach` |
| **local_coder** | `qwen3-coder` | Ollama `localhost:11434` — 256K ctx, AMD ROCm | usage offline/privé via `/set-model dev qwen3-coder` |

**Overrides task-aware (orchestrateur) :**

| Profil de tâche | Override vers | Raison |
|---|---|---|
| Cross-validation CVTL, second opinion critique, décision nuancée | `deep_reasoning` | Raisonnement indépendant et profondeur argumentative |
| Refactoring complexe, debug multi-fichiers, large codebase, ADR | `deep_reasoning` | Analyse technique profonde + contexte large |
| Contexte long (1000+ lignes, codebase entière) | `deep_reasoning` | Besoin multi-étapes à forte mémoire de contexte |
| Prompt engineering, création workflow/instruction, YAML | `writing_structured` | Sortie structurée, stabilité rédactionnelle |
| Tâches simples, checks d'état, opérations shell | `fast_iter` | Latence/coût optimisés |

Note: la disponibilité des modèles varie selon plan Copilot, client IDE et région; le fallback vers `auto` est obligatoire si un modèle explicite n'est pas disponible.

## Politique de parallélisme

- **Toujours paralléliser** les lectures/recherches indépendantes (read/search/grep/list).
- **Ne pas paralléliser** les commandes terminal mutables dans un shell partagé (ordre strict).
- `runSubagent` est utile pour spécialisation/isolation de contexte; le gain principal n'est pas la vitesse brute.

## Politique diagnostics VS Code (télémétrie opérationnelle)

- Utiliser `code --status` pour snapshot process/perf quand un ralentissement est suspecté.
- Compléter avec Process Explorer (`Help > Open Process Explorer`) et Running Extensions si besoin.
- Archiver les diagnostics dans `_grimoire-runtime-output/test-artifacts/` pour traçabilité.
