---
description: Comment lire et exploiter ce package de cadrage
author: Guilhem (via Grimoire Forge)
date: 2026-07-01
---

# Guide d'utilisation — Cadrage extensions et blueprint

## À quoi sert ce package

Il fixe le cap des chantiers extensions, marketplace, setup web et éditeur
blueprint, et fournit les trois contrats (schémas JSON) que tous les horizons
consomment. Toute implémentation de ces chantiers commence par lire ce package.

## Ordre de lecture

1. [BRIEF-cadrage-extensions-blueprint.md](BRIEF-cadrage-extensions-blueprint.md) — le pourquoi, les décisions prises et leur rationale.
2. [ROADMAP-horizons-extensions-blueprint.md](ROADMAP-horizons-extensions-blueprint.md) — la trajectoire H1 à H4 et les critères de passage.
3. Les trois spécifications, selon le chantier que vous attaquez :
   - [SPEC-manifeste-extension.md](SPEC-manifeste-extension.md) pour le CLI, la page extensions ou le registry.
   - [SPEC-export-catalogue.md](SPEC-export-catalogue.md) pour le script d'export ou le viewer.
   - [SPEC-format-blueprint.md](SPEC-format-blueprint.md) pour le viewer, l'éditeur ou le replay.

## Comment utiliser les schémas

Valider un manifeste ou un blueprint en local :

```bash
python -c "
import json, jsonschema
schema = json.load(open('schemas/extension.schema.json'))
doc = json.load(open('exemples/crewai.extension.json'))
jsonschema.validate(doc, schema)
print('OK')
"
```

Les exemples (`exemples/`) sont la référence de forme : un nouveau manifeste
d'extension part de `crewai.extension.json`, un nouveau flow part de
`onboarding-crew.blueprint.json`.

## Règles à respecter en implémentant

- Ne jamais faire exécuter un flow par l'éditeur : compilation vers artefacts, exécution par le runtime existant.
- Ne jamais copier des données du catalogue à la main : passer par l'export JSON.
- Tout hook fourni par une extension démarre en mode `shadow`.
- Un changement structurel d'un schéma exige un incrément de version majeure et une note de migration dans ce package.

## Quand mettre à jour ce package

- Une décision du brief est remise en cause : documenter la nouvelle décision et son rationale dans le brief.
- Un schéma évolue : mettre à jour le schéma, l'exemple, la spécification et la documentation technique ensemble.
- Un critère de passage d'horizon est atteint : le noter dans la roadmap avec la preuve associée.
