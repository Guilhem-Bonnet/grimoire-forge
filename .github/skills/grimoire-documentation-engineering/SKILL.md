---
name: grimoire-documentation-engineering
description: "Documentation, review editoriale et maintenance du corpus. Use when: explain concept, write document, validate document, update standards, mermaid, document project, editorial review, prose review, structure review, index docs, shard doc, documentation engineering."
created: "2026-04-14"
---

# Grimoire Documentation Engineering

Cette skill remplace la grappe de wrappers documentation BMM et les wrappers editoriaux du core en une seule surface de travail documentaire.

## When to Use

- Quand il faut expliquer un concept, rediger un document, valider un document ou mettre a jour des standards.
- Quand il faut produire ou revoir un diagramme Mermaid.
- Quand il faut documenter un projet, relire la prose, revoir la structure, indexer ou sharder un corpus.
- Quand le besoin documentaire doit rester coherent sans accumuler des prompts wrapper pour chaque sous-tache.

## Pre-requisites

- Charger `_grimoire-runtime/_memory/tech-writer-sidecar/documentation-standards.md`.
- Charger les instructions Markdown et toute charte locale applicable.
- Identifier le mode de travail : creation, validation, review editoriale, maintenance de corpus ou restructuration.

## Process

1. Clarifier l'intention documentaire et le type de livrable attendu.
2. Produire, corriger ou valider le contenu avec la charte documentaire active.
3. Appliquer si besoin la revue prose, la revue structure ou la generation Mermaid appropriee.
4. Si le corpus grossit, lancer l'indexation ou le sharding au lieu d'ajouter un nouveau wrapper documentaire.
5. Finir avec une sortie propre : document, rapport de review ou maintenance de corpus avec references valides.

## Agents Involved

- `tech-writer` pour la production et la review editoriale.
- `analyst` ou `architect` si le contenu exige un cadrage metier ou systeme.
- `ux-designer` si la lisibilite ou la structure d'experience documentaire est centrale.

## Assets

- `_grimoire-runtime/bmm/agents/tech-writer/`
- `_grimoire-runtime/core/tasks/editorial-review-prose.xml`
- `_grimoire-runtime/core/tasks/editorial-review-structure.xml`
- `_grimoire-runtime/core/tasks/index-docs.xml`
- `_grimoire-runtime/core/tasks/shard-doc.xml`

## Output Format

- Mode documentaire choisi.
- Livrable ou rapport de review.
- Points de style, structure et references.
- Actions de maintenance de corpus si necessaire.

## Success Criteria

- Le contenu respecte la charte documentaire active.
- La review distingue clairement prose, structure et maintenance de corpus.
- Les documents volumineux sont indexes ou shards plutot que caches derriere des wrappers multiples.
- Le resultat est directement exploitable par le projet sans reprise editoriale lourde.