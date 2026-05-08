# Grimoire Game Assets Base

## But

Ce dossier est la base unique pour collecter, trier, valider et publier les assets du jeu Grimoire Game.

Regle stricte: ne jamais importer un asset depuis un bac de test runtime (`_grimoire-output/da-tests`).

## Arborescence

- 00-intake/: depot brut des packs sources, sans retouche
- 10-curated/: assets gouvernes, indexes et prets pour integration
- 10-curated/legacy/: imports et exports legacy preserves hors du chemin principal de publication
- manifests/: registre de sources, index des assets, attribution
- tools/: scripts de controle et de publication

## Flux de travail

1. Placer les packs bruts dans 00-intake selon leur origine (pixel-agents, kenney, lpc).
2. Convertir/decouper les assets utiles vers 10-curated par categorie.
3. Renseigner manifests/assets-index.csv pour chaque asset retenu.
4. Verifier la licence dans manifests/sources.yaml et, si necessaire, dans manifests/attribution.md.
5. Marquer `validated=true` dans manifests/assets-index.csv pour les assets approuves.
6. Publier vers le runtime Observatory avec tools/publish_to_observatory.sh.

## Direction artistique

La source de verite visuelle pour les assets 2D vit dans [STYLE_GUIDE.md](STYLE_GUIDE.md).

- Les placeholders proceduraux servent a remplir et tester le board, pas a signer la direction artistique finale.
- Les FX, props iconiques, silhouettes d'agents et signatures de room doivent suivre un motif semantique dedie, pas un simple bruit visuel generique.
- Toute evolution du pipeline de generation doit rester deterministe et rattachee a une palette canonique.

Regle de rangement:

- La racine de `00-intake/` ne contient que des dossiers sources (`pixel-agents/`, `lpc/`, etc.) et leurs fichiers de controle (`.gitkeep`).
- Les fichiers de travail bruts (`.xcf`, captures, exports intermediaires) vivent dans le sous-dossier de leur source, jamais directement a la racine de `00-intake/`.
- Dans un pack source comme `00-intake/pixel-agents/`, utiliser des sous-dossiers explicites: `assets/` pour le dump brut, `fonts/` pour les polices, `references/` pour les captures/previews, `workfiles/` pour les sources de travail modifiables.
- La racine de `10-curated/` ne contient que les categories gouvernees (`characters/`, `floors/`, `furniture/`, `fx/`, `ui/`, `walls/`) et `legacy/`.
- Tout dump source, capture, atlas ou export de travail non indexe sort du chemin principal et va dans `10-curated/legacy/` ou `00-intake/`.

## Convention de nommage

- Fichier image: CATEGORY_SLUG_vNN.png
- Serie seed anonyme: CATEGORY_seed_NN_vNN.png
- Objet seed identifiable: CATEGORY_SLUG_seed_vNN.png
- Manifest local optionnel: CATEGORY_SLUG_vNN.manifest.json
- Slug: minuscules, chiffres, tirets bas seulement

Regle transitoire (assets seeds importes):

- Les imports seeds sont normalises des leur entree dans `10-curated/`.
- Aucun nouveau nom legacy de type `char_0.png`, `floor_0.png` ou `BOOKSHELF.png` n'entre dans le chemin gouverne.
- La publication runtime se base sur l'index (asset_id + relative_path), pas sur le nom du fichier seul.

Exemples:

- characters_dev_idle_v01.png
- furniture_desk_dual_v02.png
- floor_parquet_dark_v01.png
- character_seed_01_v01.png
- furniture_bookshelf_seed_v01.png

## Contraintes de qualite

- Format image: PNG
- Tiles fixes: 16x16, 16x32, 32x32, ou 32x64
- Fond transparent requis pour les sprites et objets
- Aucun nom ambigu ou generique (ex: tile1.png, new.png)
- Toute animation doit documenter son nombre de frames
- Chaque asset publie doit exister dans manifests/assets-index.csv avec `validated=true`

## Validation fail-closed

La publication est strictement bloquante si une regle de gouvernance n'est pas satisfaite.

- `source_id` inexistant dans manifests/sources.yaml
- statut source different de `approved` ou `approved-with-attribution`
- incoherence entre la licence de l'index CSV et la licence declaree dans manifests/sources.yaml
- source `approved-with-attribution` absente du registre manifests/attribution.md
- chemin invalide ou fichier introuvable dans 10-curated

Dans ces cas, la publication s'arrete avec erreur explicite et n'effectue aucune copie partielle.

## Format CSV robuste

Le script utilise un parseur CSV conforme. Les champs texte peuvent contenir des virgules si le champ est quote.

Exemple valide pour `notes`:

```csv
asset_id,category,source_id,license,relative_path,frames,tile_w,tile_h,states,author,notes,validated
example_asset,furniture,local-pixel-agents,internal-procedural,10-curated/furniture/example.png,1,16,16,default,unknown,"Note avec virgule, detail",true
```

## Export vers Observatory

Le script tools/publish_to_observatory.sh publie uniquement les assets declares dans manifests/assets-index.csv avec `validated=true`, sans suppression destructive.

Cible par defaut:

- `_grimoire-output/assets` pour le runtime Observatory actif du depot
- `TARGET_DIR=...` pour surcharger explicitement la destination si necessaire

Variables utiles:

- `DRY_RUN=1` pour verifier sans copier
- `INDEX_FILE`, `SOURCES_FILE`, `ATTRIBUTION_FILE`, `CURATED_DIR`, `TARGET_DIR` pour tests ou environnements specifiques

## Sources autorisees

Voir manifests/sources.yaml pour la source de verite des origins et des licences.
