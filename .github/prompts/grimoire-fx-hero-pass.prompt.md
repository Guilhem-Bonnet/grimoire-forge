---
description: 'Workflow de passe curatoriale sur les FX hero du Grimoire Game. Use when: finaliser des FX critiques, monter un baseline procedural en rendu final, prioriser 5 a 10 FX hero, produire un brief image-par-image.'
mode: 'prompt'
created: '2026-04-09'
---

# Grimoire FX Hero Pass

## Context

Ce workflow sert a sortir les FX les plus critiques du statut `baseline` pour les faire monter vers un rendu `hero-ready` ou `final`.

## Pre-conditions

1. Charger `{project-root}/_grimoire-runtime/bmm/config.yaml` et stocker les variables de session.
2. Lire `{project-root}/grimoire-game-assets/STYLE_GUIDE.md` puis `{project-root}/grimoire-game-assets/README.md`.
3. Lire `{project-root}/docs/exploitation/proposition-fx-hero-et-agent-da.md` pour reutiliser la priorisation WS6 si elle couvre deja le besoin.
4. Inspecter les FX cibles dans `{project-root}/grimoire-game-assets/10-curated/fx/` et les references utiles dans `00-intake/`.
5. Si un `.md` est cree ou modifie, charger la charte documentation avant ecriture.

## Steps

1. Selectionner jusqu'a 8 FX a plus forte charge semantique et expliquer en une phrase pourquoi ils sont prioritaires.
2. Pour chaque FX, produire un brief court avec : role in-world, room cible, palette canonique, silhouette cle, arc d'animation, anti-goal.
3. Decider la voie de production pour chaque FX : `touch-up`, `rebuild`, ou `reference-curation`.
4. Si le travail touche un generateur, remplacer tout comportement interchangeable par des regles de silhouette et de motion deterministes.
5. Valider explicitement pour chaque FX : lecture a 1x, distinction avec les autres familles, integration room, statut `hero-ready` ou `final`.
6. Finir par un ordre de production compact : lot 1, lot 2, reste.

## Agents Involved

- `art-director` pour l'arbitrage visuel et la qualite finale.
- `ux-designer` pour la lecture immediate des signaux et la comprehension in-world.
- `dev` si un outil, un manifest ou un generateur doit changer.

## Output Format

1. Priorisation.
2. Briefs par FX.
3. Decisions de production.
4. Validation.
5. Statut final par FX.

## Success Criteria

- Les FX critiques ne sont plus interchangeables entre eux.
- La silhouette et le mouvement racontent la fonction avant le detail decoratif.
- Aucun FX hero ne repose sur un anneau generique, un bruit aleatoire ou un simple flash plein ecran.
- Le resultat classe clairement chaque asset en `baseline`, `hero-ready` ou `final`.