---
name: grimoire-builder-factory
description: "Creation, edition et validation d'artefacts Grimoire via BMB. Use when: create agent, edit agent, validate agent, create module, edit module, validate module, create workflow, edit workflow, validate workflow, builder factory, artifact design."
created: "2026-04-14"
---

# Grimoire Builder Factory

Cette skill remplace la grappe de wrappers BMB et applique la nouvelle politique de choix de primitive avant toute creation d'artefact.

## When to Use

- Quand il faut creer, editer ou valider un agent, un module ou un workflow Grimoire.
- Quand il faut arbitrer entre prompt, skill, instruction, hook et agent avant de builder.
- Quand il faut reprendre un artefact existant sans multiplier les surfaces `.github`.

## When NOT to Use

- Pour creer une **skill** ou un **hook** Grimoire → `grimoire-skill-forge` (gated par `grimoire-skill-analyzer`, score min 75/100, mode `shadow` initial pour les hooks). Ce flow est la seule porte autorisee.
- Pour scaffolder un nouveau projet complet → utiliser le BMM Workflow 1 / module-builder dedie.

## Pre-requisites

- Lire `.github/instructions/artefact-governance.instructions.md`.
- Identifier la primitive minimale suffisante avant de toucher un template.

## Process

1. Classer le besoin : agent, skill, instruction, hook ou workflow prompt user-facing.
2. Rejeter par defaut tout prompt mince ou tout companion prompt automatique.
3. Utiliser les workflows BMB uniquement apres ce tri de primitive.
4. Produire ou modifier l'artefact cible avec metadata, frontmatter et points d'integration coherents.
5. Verifier la non-duplication avec les surfaces deja presentes et documenter la justification si un prompt est quand meme conserve.

## Agents Involved

- `agent-builder` pour les agents.
- `module-builder` pour les modules.
- `workflow-builder` pour les workflow prompts user-facing ou les structures de skill.
- `dev` seulement si un artefact exige des assets codes ou des validateurs techniques.

## Assets

- `_grimoire-runtime/bmb/workflows/agent/`
- `_grimoire-runtime/bmb/workflows/module/`
- `_grimoire-runtime/bmb/workflows/workflow/`
- `.github/instructions/artefact-governance.instructions.md`

## Output Format

- Primitive retenue et rationale courte.
- Artefact cree ou modifie.
- Justification de non-duplication.
- Verification des liens et du frontmatter.

## Success Criteria

- La plus petite primitive suffisante est choisie.
- Aucun prompt compagnon n'est cree par automatisme.
- Aucun artefact ne duplique une skill, un agent, une instruction ou un hook deja adequat.
- Le resultat est pret a etre decouvert sans wrapper superflu.