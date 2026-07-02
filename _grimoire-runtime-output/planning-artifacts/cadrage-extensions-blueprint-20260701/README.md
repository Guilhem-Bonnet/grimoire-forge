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

## Avancement

H1 est livré : export catalogue, CLI `grimoire ext`, extension pilote CrewAI,
page extensions et blueprint viewer. Preuves et commits dans la
documentation technique.

H2 est livré côté outillage (2026-07-02, commits kit `2ee2661`, Forge
`b20b458`) : `grimoire serve` (API locale + SSE + statique, 10 tests), page
`/setup/` (wizard archetypes, installation d'extensions, vue « mon setup »,
plan d'init), éditeur blueprint v1 (création, palette patterns + artefacts du
projet, connexions non typées, sauvegarde et validation via l'API). Parcours
complet vérifié navigateur.

Les extensions langfuse (observabilité : hooks + instructions, sans agents)
et langgraph (framework : agent + node pack, sans hooks) sont livrées
(commits kit `ffffa20`, Forge `3819cf7`). Trois extensions réelles valident
le manifeste v1 sans changement structurel : **la précondition d'entrée H3
est satisfaite**.

Reste pour clore H2 : le gate de sortie — l'usage quotidien réel, qui ne se
livre pas, il se constate.

H3 est en production (2026-07-02, validé par Guilhem) : le registry vit dans
son repo dédié
[grimoire-extensions-registry](https://github.com/Guilhem-Bonnet/grimoire-extensions-registry)
— index versionné, 3 extensions publiées, CI de conformité autonome verte
sur GitHub (validation embarquée, sans dépendance au cycle de release du
kit), flux de publication par PR (`scripts/publish-pr.sh`). Côté kit :
`grimoire ext publish` (archives déterministes + sha256) et installation
depuis registry avec intégrité vérifiée (commit `18212ca`, extraction
`e7582c2d`). Côté site : recherche + filtres par famille sur la page
extensions.

Restent pour H3 : stats d'installation (exige une télémétrie d'usage,
décision à prendre) et première extension tierce réelle. H4 (pins typés,
linting normatif, replay) est le prochain grand chantier.
