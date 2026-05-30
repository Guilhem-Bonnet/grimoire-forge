---
description: "Conventions des assets 2D Grimoire. Use when: editing grimoire-game-assets, pixel art, FX, sprites, palettes, manifests, asset generators."
applyTo: "grimoire-game-assets/**"
created: 2026-04-09
---

# Grimoire 2D Assets

Cette instruction transforme la charte visuelle en regles de production concretes pour les assets 2D du projet.

## Scope

This instruction applies to files matching: `grimoire-game-assets/**`

## Rules

- Charger `grimoire-game-assets/STYLE_GUIDE.md` et `grimoire-game-assets/README.md` avant toute modification d'asset, de manifest ou d'outil de generation.
- Considerer `grimoire-game-assets/STYLE_GUIDE.md` comme la source de verite pour la palette, la silhouette, les materiaux et la grammaire FX.
- Ne jamais introduire de palette aleatoire, derivee d'un hash, ou de couleur non rattachee a un token de style nomme.
- Un output procedural est un baseline. Les FX, props hero, silhouettes d'agents et signatures de room doivent recevoir un motif semantique dedie et une revue explicite.
- Toute demande de nouvel asset doit expliciter au minimum : fonction en jeu, room ou contexte, taille cible, nombre de frames, famille de palette, et critere de lecture a l'echelle 1x.
- Toute creation ou modification d'asset publie doit rester coherente avec `manifests/assets-index.csv` : dimensions, frames, chemin, provenance, validation.
- Si un script de generation est modifie, la direction artistique doit etre encodee de maniere deterministe et lisible. Pas de magie pseudo-alatoire cachee.
- Prioriser contours nets, contraste lisible et transparence propre sur la densite de details.
- Si l'asset ressemble encore a un placeholder generique apres revue, il ne doit pas etre presente comme asset final.

## Examples

### Do

- Mapper les FX de reussite vers une palette `Brass` et un burst clairement centre.
- Distinguer `memory_read` et `memory_write` par un mouvement entrant versus sortant.
- Marquer un asset comme baseline procedural si sa valeur est surtout utilitaire.
- Reutiliser les memes tokens de palette entre UI, FX et props d'une meme famille semantique.

### Don't

- Refaire un cercle vide avec des points aleatoires pour trois FX differents.
- Utiliser une palette differente pour deux assets qui representent le meme type d'evenement.
- Valider un FX critique sans trajectoire ni centre d'attention.
- Laisser un asset hero dans le meme niveau de finition qu'un filler procedural.

## Anti-patterns

- Anneau radial generique utilise comme langage FX par defaut.
- Flash uniforme rouge plein cadre pour signifier une erreur.
- Palette arc-en-ciel implicite sans signification produit.
- Dependance a `asset_id` pour inventer automatiquement le rendu final.
- Confusion entre lisibilite systeme et decoration pure.