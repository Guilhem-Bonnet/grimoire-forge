---
description: "Gouvernance des recettes de flow compile. Use when: editing the compiled flow registry, adding chat/report templates, or promoting a dynamic recipe into the durable catalog."
applyTo: "grimoire-kit/framework/registry/compiled-flow-recipes.json"
---

# Compiled Flow Governance

## Scope

- Cette instruction gouverne le registre durable des recettes compilees.
- Les overlays dynamiques suivent les memes regles de fond, mais leur validation passe aussi par `compiled-flow.py validate`.

## Mutation rules

- Modifier une recette `universal` uniquement pour la rendre plus portable, plus fiable, plus observable, plus claire, ou plus decouvrable.
- Si le besoin reste local, temporaire, experimental, ou lie a un incident unique, creer une recette `dynamic` au lieu de toucher le registre durable.
- Une recette `universal` ne doit pas contenir de chemin personnel, de branche temporaire, de ticket local, ni de wording reserve a un seul livrable.

## Template rules

- Garder les templates `chat` et `report` courts, contractuels et reutilisables.
- Ne pas encoder de ton projet-specifique ou de contexte incidentel dans un template partage.
- Preferer les placeholders generiques (`OBJECTIVE`, `COMMAND_LIST`, `SUMMARY`, `DECISION`, `RISKS`, `TARGET`) a des variables ultra-specifiques.

## Promotion rules

- Une recette dynamique n'est promue qu'apres reutilisation repetee et nettoyage de ses details locaux.
- Une promotion doit conserver la separation entre : declenchement, plan d'action, restitution, gouvernance.

## Anti-patterns

- Tordre une recette universelle pour un cas one-off.
- Cacher de la logique metier dans un `hook_context`.
- Ajouter une recette qui duplique une recette existante sans changer le contrat de declenchement ou la gouvernance.