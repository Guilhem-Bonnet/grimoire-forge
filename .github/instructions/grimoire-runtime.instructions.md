---
description: "Conventions du framework Grimoire et structure du projet Grimoire. Use when: editing Grimoire agents, modifying workflows, working with Grimoire config, agent memory, agent manifests, workflow engine, module config, Grimoire architecture."
applyTo: "_grimoire-runtime/**"
---

# Grimoire Framework Conventions

## Structure

- `_grimoire-runtime/core/` — agents et tasks du noyau (grimoire-master, help, editorial review)
- `_grimoire-runtime/bmm/` — module méthode Grimoire (agents métier, workflows par phase)
- `_grimoire-runtime/bmb/` — module builders (agent-builder, module-builder, workflow-builder)
- `_grimoire-runtime/cis/` — module créativité et innovation
- `_grimoire-runtime/tea/` — module test architecture
- `_grimoire-runtime/_config/` — manifests, registries, métriques
- `_grimoire-runtime/_memory/` — fichiers mémoire protégés (hook PreToolUse)

## Config YAML

Chaque module a un `config.yaml` chargé à l'activation de l'agent :

```yaml
user_name: Guilhem
communication_language: Français
output_folder: "{project-root}/_grimoire-runtime-output"
```

Les variables `{project-root}`, `{user_name}`, `{communication_language}` sont substituées au runtime.

## Agents (`.agent.md`)

- Frontmatter obligatoire : `description`, `tools`
- Sub-agents : `user-invocable: false`
- Déclarer `handoffs` vers les agents de transition
- Corps : instructions d'activation + contraintes + persona

## Workflows

- YAML workflows → chargés via `_grimoire-runtime/core/tasks/workflow.xml` (workflow engine)
- MD workflows → exécutés directement (load and follow)
- Exécution step-by-step JIT — jamais charger plusieurs steps d'un coup
- Sauvegarder les outputs après CHAQUE step

## Mémoire

- `_grimoire-runtime/_memory/` est protégé par le hook `grimoire-memory-guard`
- `shared-context.md` — contexte partagé entre sessions
- `udf-usage-tracker.json` — tracking des artefacts dynamiques
- Ne JAMAIS écrire dans `_grimoire-runtime/_memory/` sans confirmation utilisateur
