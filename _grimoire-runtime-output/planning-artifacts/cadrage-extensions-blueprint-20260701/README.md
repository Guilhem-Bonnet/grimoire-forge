---
description: Index du package de cadrage H1 avec schémas anticipés pour H4
author: Guilhem (via Grimoire Forge)
date: 2026-07-01
---

# Package — Cadrage extensions, marketplace et blueprint

Cadrage des chantiers extensions installables, marketplace, setup web et
éditeur de flow agentique de type blueprint pour Grimoire Forge.

## Contenu

| Fichier | Rôle |
| --- | --- |
| [BRIEF-cadrage-extensions-blueprint.md](BRIEF-cadrage-extensions-blueprint.md) | Objectifs, principe d'architecture, trois décisions structurantes, risques |
| [ROADMAP-horizons-extensions-blueprint.md](ROADMAP-horizons-extensions-blueprint.md) | Trajectoire H1 à H4 avec critères de passage |
| [SPEC-manifeste-extension.md](SPEC-manifeste-extension.md) | Contrat `extension.json` |
| [SPEC-export-catalogue.md](SPEC-export-catalogue.md) | Export JSON du catalogue de patterns |
| [SPEC-format-blueprint.md](SPEC-format-blueprint.md) | Format de graphe `.blueprint.json` |
| [schemas/extension.schema.json](schemas/extension.schema.json) | JSON Schema du manifeste d'extension |
| [schemas/catalogue-export.schema.json](schemas/catalogue-export.schema.json) | JSON Schema de l'export catalogue |
| [schemas/blueprint.schema.json](schemas/blueprint.schema.json) | JSON Schema du format blueprint |
| [exemples/crewai.extension.json](exemples/crewai.extension.json) | Manifeste réel de l'extension pilote CrewAI |
| [exemples/onboarding-crew.blueprint.json](exemples/onboarding-crew.blueprint.json) | Blueprint d'exemple avec node d'extension |
| [DOC-TECHNIQUE-cadrage-extensions-blueprint.md](DOC-TECHNIQUE-cadrage-extensions-blueprint.md) | Architecture, contrats, dépendances, validation |
| [GUIDE-utilisation-cadrage-extensions-blueprint.md](GUIDE-utilisation-cadrage-extensions-blueprint.md) | Ordre de lecture et règles d'implémentation |

## Décisions prises

1. Manifeste d'extension en JSON (`extension.json`), validé par JSON Schema.
2. Viewer en Cytoscape.js + elkjs, site vanilla conservé ; réévaluation à l'entrée de l'éditeur H2.
3. CLI `ext` intégré à `grimoire.sh` dans grimoire-kit ; les archetypes existants alimentent le futur wizard.

## Principe non négociable

Le blueprint compile vers les artefacts gouvernés existants ; le runtime
existant exécute. Aucun moteur d'exécution parallèle.

## Avancement H1

Livrés : export catalogue (`scripts/export-catalogue.py` dans le repo de
patterns, JSON validé), CLI `grimoire ext` (grimoire-kit, testé), extension
pilote CrewAI (`grimoire-kit/extensions/crewai/`, cycle complet prouvé).
Voir la documentation technique pour les preuves.

Prochaine étape : page extensions statique du site et blueprint viewer
read-only.
