---
description: "Standards de documentation Markdown du projet. Use when: writing documentation, creating Markdown files, editing docs, README, CHANGELOG, architecture docs, ADR, technical writing."
applyTo: "**/*.md"
---

# Markdown Standards — Grimoire Kit

## CommonMark Strict

- Headers ATX uniquement (`# Title`) — jamais de soulignement `===`
- Un espace après `#` — jamais de `#` en fin de ligne
- Lignes vides avant et après chaque header, liste, et bloc de code
- Pas de HTML inline sauf `<details>` pour les sections pliables

## Code

- Blocs fencés avec langage : ` ```python `, ` ```yaml `, ` ```bash `
- Jamais de blocs indentés (4 espaces)
- Inline code pour les noms de fichiers, variables, commandes : `` `file.py` ``

## Listes

- Marqueur uniforme (`-` préféré) — ne pas mixer `-`, `*`, `+`
- Indentation de 2 espaces pour les sous-listes
- Pas de lignes vides entre les items d'une même liste

## Liens

- Format inline : `[texte](url)` — jamais d'URL nues
- Références internes relatives : `[voir config](../config.yaml)`

## Diagrammes Mermaid

- Syntaxe Mermaid v10+ — type déclaré en première ligne
- Maximum 15 nœuds par diagramme
- Toujours dans un bloc fencé ` ```mermaid `

## Règle critique

**Jamais d'estimation temporelle** dans la documentation — pas de durée de workflow, LOE, ou mesure temporelle sauf demande explicite.
