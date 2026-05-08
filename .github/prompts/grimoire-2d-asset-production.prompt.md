---
description: 'Workflow de direction artistique et production des assets 2D du Grimoire Game. Use when: creer un FX, revoir un sprite, aligner palette et style, produire un room kit, arbitrer procedural versus curatorial.'
mode: 'prompt'
created: '2026-04-09'
---

# Grimoire 2D Asset Production

## Context

Ce workflow transforme une demande visuelle en asset 2D gouverne, lisible et compatible avec la DA du projet.

## Pre-conditions

1. Charger `{project-root}/_grimoire-runtime/bmm/config.yaml` et stocker les variables de session.
2. Lire `{project-root}/grimoire-game-assets/STYLE_GUIDE.md` puis `{project-root}/grimoire-game-assets/README.md`.
3. Lire `{project-root}/grimoire-game-assets/manifests/assets-index.csv` si la demande touche des assets existants ou la gouvernance.
4. Regarder les references utiles dans `00-intake/` et les precedents visuels dans `10-curated/`.
5. Si un `.md` doit etre cree ou modifie, charger la charte documentation avant ecriture.

## Steps

1. Diagnostiquer le probleme visuel en trois points maximum : style, lisibilite, semantique.
2. Produire un brief court avec : objet, usage, room cible, taille, frames, famille de palette, motif, anti-goal.
3. Choisir la voie de production :
   - `procedural-baseline` pour les fillers et supports a faible charge semantique
   - `curated-pass` pour les FX, assets hero, signatures de room et silhouettes critiques
   - `reference-curation` si une source autorisee offre un meilleur point de depart
4. Si un generateur est touche, remplacer tout comportement aleatoire par des regles de style deterministes et lisibles.
5. Si un asset est produit ou modifie, verifier explicitement : lecture a 1x, coherence palette, frame arc, integration room, metadata manifest.
6. Rendre le statut final de chaque asset : `baseline` ou `final`.

## Agents Involved

- `ux-designer` pour la lecture et la semantique.
- `dev` pour scripts, assets et manifests.
- `tech-writer` seulement si la gouvernance ou la charte changent.

## Output Format

1. Diagnostic.
2. Brief d'asset.
3. Decision de production.
4. Fichiers touches.
5. Validation finale.

## Success Criteria

- Le resultat suit la charte DA operatoire.
- Aucun motif FX critique ne reste interchangeable avec un autre.
- La palette est deterministe et rattachee a une famille semantique.
- La gouvernance des assets reste coherente avec l'index et la provenance.