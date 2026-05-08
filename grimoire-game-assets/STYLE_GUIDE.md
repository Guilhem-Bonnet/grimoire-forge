# Guide de style 2D Grimoire Game

## Intention

Le board doit ressembler a un systeme d'exploitation agentique mis en scene dans un bureau mystique et technique.
La priorite est la lecture immediate des roles, des etats et des actions, pas la performance decorative.

## Piliers visuels

- Lisibilite avant spectacle.
- Cohesion de palette avant variete.
- Silhouette nette avant micro-detail.
- Motion semantique avant pluie de particules.
- Procedural pour remplir, curatorial pour signer.

## Palette canonique

| Token | Hex | Usage principal |
| --- | --- | --- |
| Ink | `#2a2323` | Contours, ombres fortes, separation |
| Paper | `#efe6cf` | Pages, highlights chauds, UI claire |
| Brass | `#d2b058` | Reussite, accomplissement, trophies |
| Verdigris | `#86b0a7` | Flux, handoff, broadcast, liaison |
| Memory | `#9f9cdb` | Recall, ecriture memoire, traces mentales |
| Ember | `#d86d5c` | Erreur, danger, refus, incident |
| Leaf | `#a8c06e` | Etats stables, vie, decor vegetal |
| Storm | `#84a0c6` | UI technique, pluie, machines, runtime |

## Regles pixel

- Tailles canoniques : `16x16`, `16x32`, `32x16`, `32x32`, `32x64`.
- Fond transparent strict pour sprites, FX et props.
- Contour principal sombre de 1 px sur les formes lisibles a l'echelle 1x.
- Trois valeurs par materiau maximum : base, ombre, highlight.
- Pas d'anti-alias, pas de blur, pas de glow flou, pas de demi-pixels.
- Un asset doit rester nommable au premier coup d'oeil en vue 1x.

## Grammaire des FX

| Famille | Palette | Motif | Mouvement | A eviter |
| --- | --- | --- | --- | --- |
| Success / XP / Achievement | Brass + Paper | Eclat en etoile, burst concentre, quelques etincelles | Expansion puis extinction nette | Anneaux generiques et confettis sans centre |
| Handoff / Broadcast / Link | Verdigris + Storm | Vague directionnelle, tether, relais entre deux points | Translation gauche-droite ou source-cible | Cercle radial symetrique sans sens |
| Memory read / write | Memory + Paper | Page, glyphe, halo mental, particules entrantes ou sortantes | Convergence ou divergence explicite | Meme animation pour read et write |
| Error / Panic / Reject | Ember + Ink | Eclair brise, croix vive, flash serre | Strobe court, pas de remplissage total | Ecran plein rouge opaque |
| Document / Paper motion | Paper + Storm | Fiche, page, dossier, trait de trajectoire | Glisse, chute, drift | Rectangle nu sans inertie |
| Rain / ambient runtime | Storm + Ink | Streaks, gouttes, fenetre ou grille support | Descente verticale ou diagonale | Bruit blanc anime |

## Procedural versus curatorial

| Categorie | Procedural acceptable | Curatorial requis vite |
| --- | --- | --- |
| Floors | Oui, tant que la palette et le rythme restent coherents | Seulement pour salles iconiques |
| Walls | Oui pour les motifs utilitaires | Oui pour murs-signature et fenetres hero |
| UI micro-icons | Oui si la lecture reste immediate | Oui pour badges et marqueurs critiques |
| Furniture de remplissage | Oui pour volume et cohorte | Oui pour props iconiques de room |
| FX | Non au-dela du baseline | Oui, presque toujours |
| Agent silhouettes | Non | Oui, toujours |
| Room kits signatures | Non | Oui, toujours |

## Revue qualite

Un asset est acceptable seulement si ces points passent ensemble :

1. Lecture semantique claire.
2. Silhouette identifiable.
3. Palette coherente avec les tokens canoniques.
4. Arc d'animation explicite si plusieurs frames.
5. Bonne integration dans la room cible.
6. Provenance et metadata manifest cohérents.

## Rejets immediats

- Palette derivee d'un hash, d'un random ou d'une couleur arbitraire non nommee.
- FX bases sur des anneaux vides ou des points aleatoires sans motif semantique.
- Flash plein ecran opaque a la place d'un impact lisible.
- Asset qui semble venir d'un autre jeu ou d'un autre genre.
- Sprite techniquement propre mais incapable d'indiquer son role dans le board.
