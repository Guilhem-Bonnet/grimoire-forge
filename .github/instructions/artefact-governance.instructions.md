---
description: "Gouvernance des artefacts .github. Use when: creating or editing prompts, skills, agents, instructions, workflow docs, or other Markdown artifacts under .github."
applyTo: ".github/**/*.md"
---

# Artefact Governance

## Scope

- Cette instruction s'applique aux artefacts Markdown sous `.github/`.
- Elle complete [../../docs/exploitation/gouvernance-artefacts-agent-os-game-ui.md](../../docs/exploitation/gouvernance-artefacts-agent-os-game-ui.md) et [../../docs/exploitation/matrice-statuts-artefacts-agent-os-game-ui.md](../../docs/exploitation/matrice-statuts-artefacts-agent-os-game-ui.md).
- Elle ne remplace pas les conventions globales de Markdown ni les instructions de runtime specialisees.

## Statut canonique

- Utiliser uniquement `Incubating`, `Experimental`, `Stable` ou `Deprecated` pour le statut d'un artefact.
- `Parking lot` et `Heritage` restent des marqueurs de backlog ou de lineage ; ne pas les utiliser comme statut d'un fichier `.github`.
- Un artefact `Stable` ne doit pas dependre silencieusement d'un artefact `Incubating` ou `Experimental`.

## Metadonnees minimales pour un nouvel artefact ou une refonte majeure

- Conserver les frontmatters requis par le format existant.
- Quand le format le permet sans casser le consommateur, documenter ou mettre a jour `status`, `owner`, `capability` et `evidence`.
- Si le format est contraint, reporter ces metadonnees dans le document d'exploitation ou le plan qui reference l'artefact.
- Ne pas lancer de migration de masse juste pour normaliser un legacy non touche.

## Choix de l'artefact

- Garder le plus petit artefact suffisant.
- Utiliser un prompt pour une commande user-facing, manuelle, focalisee, avec un contrat de sortie explicite.
- Utiliser un workflow prompt uniquement pour un mission pack prompt-native distinct ; si le besoin est surtout recurrent, multi-etapes ou outille, preferer un skill.
- Utiliser un skill pour une capacite recurrente, multi-etapes, ou qui agrege plusieurs assets, scripts ou ressources.
- Utiliser une instruction pour une contrainte repetee sur une famille de fichiers.
- Utiliser un hook pour une automation deterministe au cycle de vie agent/outils.
- Ne creer un agent que si la frontiere de raisonnement est durable et qu'aucun artefact plus petit ne suffit.

## Gates de review

- Tout nouvel artefact doit pointer vers une capability ou un lot du corpus d'exploitation.
- Le statut initial doit etre explicite dans la review ou la documentation voisine.
- La preuve attendue doit etre nommee : test, commande, checklist, evidence pack ou review.
- Tout nouveau prompt doit justifier pourquoi un skill, une instruction, un agent ou un hook existant ne suffit pas.
- Une instruction doit garder un `applyTo` borne et sans effet de bord gratuit.
- Un artefact `Deprecated` doit pointer vers son remplacant et sa strategie de sortie.

## Anti-patterns

- Introduire une nouvelle surface pour masquer une absence de gouvernance.
- Mettre un artefact `Experimental` sur le chemin principal sans le dire.
- Multiplier les artefacts `.github` qui dupliquent une responsabilite deja couverte.
- Introduire un prompt mince qui ne fait que charger un agent, un workflow runtime ou une task existante.
- Ecrire une instruction plus large que la famille de fichiers qu'elle gouverne.