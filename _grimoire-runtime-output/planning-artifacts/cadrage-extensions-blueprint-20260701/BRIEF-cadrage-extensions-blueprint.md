---
description: Cadrage H1 avec décisions structurantes prises pour la cible H4
author: Guilhem (via Grimoire Forge)
date: 2026-07-01
---

# Brief de cadrage — Extensions, marketplace et blueprint agentique

## Objectif

Doter Grimoire Forge de trois capacités progressives :

1. Un système d'extensions installables (frameworks agentiques publics comme CrewAI, LangGraph, Langfuse) avec une page web dédiée, puis un marketplace ouvert.
2. Un setup complet de projet pilotable depuis une interface web (site public en lecture, mode local pour l'installation).
3. Un éditeur de flow agentique de type blueprint (modèle Unreal Engine) : nodes typés, connexions contractuelles, debug, observabilité et télémétrie.

Le différenciateur du projet est le catalogue normatif de patterns agentiques
(`Concepts/processus-developpement-agentique`) : 78 patterns socle en 8 familles
(`ORG`, `ORC`, `GOV`, `QUA`, `KNO`, `RUN`, `COG`, `MOD`), 32 contrats formels avec
obligations par champ, relations sémantiques entre patterns, anti-patterns et
matrices de maturité. Aucun éditeur visuel concurrent (Langflow, Dify, n8n,
Flowise) ne s'appuie sur une norme auditée.

## Principe d'architecture non négociable

**Le blueprint compile vers les artefacts gouvernés existants ; il n'exécute rien.**

- L'éditeur génère et modifie les agents `.md`, hooks JSON, workflows YAML et skills que le runtime Grimoire consomme déjà.
- Tout apply passe par les gates existants : `grimoire-skill-analyzer`, registre `hook-safety-registry.json`, hooks en mode `shadow` par défaut.
- Le debug et la télémétrie lisent les flux existants (`_grimoire-runtime-output/hook-runtime/events.jsonl`, `task-flow/events.jsonl`) ; aucun runtime parallèle n'est créé.

Corollaire web : le site public reste statique (catalogue navigable, page
extensions, viewer read-only). Les mutations (installation, édition, apply)
passent par un process local `grimoire serve` qui sert la même UI avec une API
locale. Une seule codebase UI, deux modes.

## Décisions structurantes

### Décision 1 — Format du manifeste d'extension : JSON

Un fichier `extension.json` par extension, validé par JSON Schema
(`schemas/extension.schema.json`).

- Cohérent avec les surfaces gouvernées existantes (`hook-safety-registry.json`, hooks JSON).
- Validation JSON Schema directe en CI du futur registry, sans couche de conversion.
- Diffable et sans les ambiguïtés YAML 1.1/1.2.

Alternative rejetée : YAML (lisibilité légèrement meilleure, mais validation et
outillage plus fragiles pour un format destiné à des contributions tierces).

### Décision 2 — Stack du viewer : Cytoscape.js + elkjs, site vanilla

Le site reste en HTML/CSS/JS vanilla. Le viewer H1 utilise Cytoscape.js (rendu
et interactions de graphe, sans dépendance framework) avec elkjs pour le layout
hiérarchique. Le thème est custom pour coller à la direction artistique
blueprint du site.

- Point de réévaluation : à l'entrée de l'éditeur (H2), si Cytoscape limite l'ergonomie de type Unreal (pins, drag de connexions), bascule possible vers un rendu canvas custom. Le format `.blueprint` étant indépendant du moteur de rendu, la bascule ne casse rien.

Alternative rejetée : introduire React + React Flow (meilleure ergonomie
éditeur, mais rupture de stack avec le site existant et surface de maintenance
front doublée).

### Décision 3 — CLI : sous-commande `ext` dans grimoire-kit

`grimoire.sh` possède déjà une quinzaine de sous-commandes (`setup`, `doctor`,
`standard`, `memory`...), un dossier `adapters/` et un dossier `archetypes/`.

- `grimoire ext add|list|remove|verify` s'insère dans le dispatcher existant.
- Les extensions généralisent le concept d'adapter déjà présent (`adapters/grimoire-mcp/`).
- Les archetypes existants (`agentic-standard`, `game-dev`, `infra-ops`, `web-app`...) deviennent les usecases du futur wizard de setup (H2) sans travail supplémentaire.

Alternative rejetée : CLI séparé (fragmentation de la distribution ; grimoire-kit
est déjà le vecteur d'installation).

## Les trois schémas anticipés

Conçus dès H1 avec l'état final H4 en tête. Ajouter un champ est trivial ;
restructurer un schéma adopté par des extensions tierces est une migration.

| Schéma | Fichier | Consommateurs |
| --- | --- | --- |
| Manifeste d'extension | `schemas/extension.schema.json` | CLI (H1), page web (H1), registry CI (H3), node packs (H4) |
| Export catalogue | `schemas/catalogue-export.schema.json` | Viewer (H1), pins typés et linting (H4) |
| Format blueprint | `schemas/blueprint.schema.json` | Viewer (H1), éditeur (H2), marketplace (H4), replay (H4) |

Spécifications détaillées : [SPEC-manifeste-extension.md](SPEC-manifeste-extension.md),
[SPEC-export-catalogue.md](SPEC-export-catalogue.md),
[SPEC-format-blueprint.md](SPEC-format-blueprint.md).

## Sources de vérité

| Donnée | Source de vérité | Consommation |
| --- | --- | --- |
| Patterns, relations, contrats, anti-patterns | `Concepts/processus-developpement-agentique` | Export JSON build-time, jamais de copie manuelle |
| Inventaire des frameworks candidats | `Concepts/reference-agentique-audit/inventory.json` | Génération de la page extensions |
| Artefacts runtime (agents, hooks, workflows, skills) | Repo cible (`.github/`, `_grimoire-runtime/`) | Compilation blueprint, vue « mon setup » |
| Télémétrie | `_grimoire-runtime-output/*/events.jsonl` | Debug, replay, overlay live |

## Risques et parades

| Risque | Parade |
| --- | --- |
| L'éditeur node devient un moteur d'exécution parallèle | Principe non négociable : compilation vers artefacts, gates existants |
| Divergence catalogue site / catalogue source | Export build-time versionné, le site ne stocke rien |
| Surface de maintenance front | Viewer read-only d'abord ; éditeur seulement après usage réel du viewer |
| Schéma manifeste instable face aux extensions tierces | Champs H3/H4 (`permissions`, `provides.nodes`, `compat`) présents dès la v1 ; gate H3 = schéma stable sur 3-4 extensions réelles |
| Extension tierce malveillante ou envahissante | Permissions déclaratives, hooks en shadow obligatoire, revue CI au registry |

## Critères de sortie H1

- CrewAI installable et fonctionnelle via `grimoire ext add crewai`.
- Page extensions publiée, générée depuis les manifestes.
- Export catalogue JSON généré depuis le repo de patterns et versionné.
- Viewer read-only publié sur le site à côté de la page observabilité.
- Les trois schémas validés par des exemples réels (manifeste CrewAI, blueprint d'exemple).
