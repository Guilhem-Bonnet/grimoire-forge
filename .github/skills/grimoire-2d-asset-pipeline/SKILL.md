---
name: grimoire-2d-asset-pipeline
description: "Direction artistique, production et review des assets 2D du Grimoire Game. Use when: asset 2D, pixel art, sprite, FX, room kit, style guide, palette, visual asset review, art direction, polish visuel."
created: "2026-04-09"
---

# Grimoire 2D Asset Pipeline

Cette skill sert a transformer une demande visuelle vague en un asset 2D gouverne, relisible et integrable dans le board.

## When to Use

- Quand un FX ou un sprite parait generique, hors-style ou faible en lisibilite.
- Quand il faut creer un nouveau room kit, prop, UI element ou effet visuel.
- Quand il faut decider si un asset peut rester procedural ou doit passer en curatorial.
- Quand il faut reviewer une serie d'assets 2D avant publication.

## Pre-requisites

- Lire `grimoire-game-assets/STYLE_GUIDE.md`.
- Lire `grimoire-game-assets/README.md`.
- Lire `grimoire-game-assets/manifests/assets-index.csv` si des assets existants sont modifies ou compares.
- Regarder les references ou precedents visuels pertinents dans `grimoire-game-assets/00-intake/` et `grimoire-game-assets/10-curated/`.

## Process

1. Diagnostiquer le probleme en trois axes maximum : style, lisibilite, semantique.
2. Ecrire un mini brief d'asset avec : role produit, room cible, taille, frames, palette, motif, anti-goal.
3. Choisir le bon mode de production : procedural baseline, passe curatoriale sur sprite pixel, ou curation depuis une reference autorisee.
4. Produire ou modifier l'asset avec palette deterministe, silhouette claire et motion lisible a l'echelle 1x.
5. Rejouer une revue courte : lecture immediate, coherence room, qualite du frame arc, provenance, manifest.
6. Rendre le statut explicite : baseline utilitaire ou asset final.

## Agents Involved

- `ux-designer` pour la lisibilite, la semantique et la hierarchie visuelle.
- `dev` pour les scripts de generation, manifests et integrations runtime.
- `tech-writer` uniquement si la charte, le workflow ou la documentation d'assets changent.

## Assets

- `grimoire-game-assets/STYLE_GUIDE.md`
- `grimoire-game-assets/README.md`
- `grimoire-game-assets/manifests/assets-index.csv`
- `grimoire-game-assets/tools/generate_complete_baseline.py`
- `.github/prompts/grimoire-2d-asset-production.prompt.md`

## Output Format

- Diagnostic court.
- Brief d'asset.
- Decision procedural versus curatorial.
- Changements appliques.
- Validation finale avec statut `baseline` ou `final`.

## Success Criteria

- L'asset est nommable au premier coup d'oeil.
- La palette correspond a une famille semantique stable.
- L'animation raconte une action, pas un simple bruit visuel.
- Le manifest et la provenance sont a jour.
- Le rendu ne depend plus d'une couleur pseudo-aleatoire ou d'un motif interchangeable.