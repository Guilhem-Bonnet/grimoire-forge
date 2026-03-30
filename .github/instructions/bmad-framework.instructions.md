---
description: "Conventions du framework BMAD et structure du projet Grimoire. Use when: editing BMAD agents, modifying workflows, working with BMAD config, agent memory, agent manifests, workflow engine, module config, BMAD architecture."
applyTo: "_bmad/**"
---

# BMAD Framework Conventions

## Structure

- `_bmad/core/` — agents et tasks du noyau (bmad-master, help, editorial review)
- `_bmad/bmm/` — module méthode BMAD (agents métier, workflows par phase)
- `_bmad/bmb/` — module builders (agent-builder, module-builder, workflow-builder)
- `_bmad/cis/` — module créativité et innovation
- `_bmad/tea/` — module test architecture
- `_bmad/_config/` — manifests, registries, métriques
- `_bmad/_memory/` — fichiers mémoire protégés (hook PreToolUse)

## Config YAML

Chaque module a un `config.yaml` chargé à l'activation de l'agent :

```yaml
user_name: Guilhem
communication_language: Français
output_folder: "{project-root}/_bmad-output"
```

Les variables `{project-root}`, `{user_name}`, `{communication_language}` sont substituées au runtime.

## Agents (`.agent.md`)

- Frontmatter obligatoire : `description`, `tools`
- Sub-agents : `user-invocable: false`
- Déclarer `handoffs` vers les agents de transition
- Corps : instructions d'activation + contraintes + persona

## Workflows

- YAML workflows → chargés via `_bmad/core/tasks/workflow.xml` (workflow engine)
- MD workflows → exécutés directement (load and follow)
- Exécution step-by-step JIT — jamais charger plusieurs steps d'un coup
- Sauvegarder les outputs après CHAQUE step

## Mémoire

- `_bmad/_memory/` est protégé par le hook `bmad-memory-guard`
- `shared-context.md` — contexte partagé entre sessions
- `udf-usage-tracker.json` — tracking des artefacts dynamiques
- Ne JAMAIS écrire dans `_bmad/_memory/` sans confirmation utilisateur
