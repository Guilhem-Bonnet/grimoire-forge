---
description: Mini-cadrage — compilation réelle des blueprints vers artefacts gouvernés
author: Guilhem (via Grimoire Forge)
date: 2026-07-03
---

# Mini-cadrage — Compilation des blueprints

Dernier grand chantier du cadrage initial : transformer `compilesTo`
(déclaratif depuis H1) en génération réelle d'artefacts. Ce document pose le
design pour arbitrage avant implémentation.

## Principe (inchangé, non négociable)

La compilation **produit des artefacts gouvernés** que le runtime existant
exécute ; elle ne crée aucun moteur. Tout apply passe par les gates
(`grimoire-skill-analyzer`, hooks shadow, revue humaine du diff).

## Design v1 proposé : le mission pack compilé

Une compilation = **un artefact** : un mission pack `.prompt.md` généré dans
`.github/prompts/{id}.blueprint.prompt.md`, qui rend le flow exécutable par
l'orchestrateur existant.

Contenu généré depuis le blueprint :

| Section du mission pack | Source |
| --- | --- |
| Objectif et flow | `name`, `description`, graphe |
| Plan d'exécution ordonné | `blueprint_simulate` (ordre topologique, déjà livré) |
| Par étape : quoi invoquer | `artifact` = artefact existant référencé ; `extension-node` = agent/workflow de l'extension ; `pattern` = obligations (contrôles du catalogue) à satisfaire par l'exécutant ; `composite` = patterns du use-case |
| Contrats aux frontières | pins/edges (task envelope, handoff packet) |
| Gates de sortie | patterns QUA du flow (evidence pack, verdict) |

La section `compiled` du blueprint (format v1, déjà prévue) trace `at`,
`catalogVersion` et le hash de l'artefact généré — la détection de dérive
existe déjà dans le format.

## Ce que la v1 ne fait pas (v2 possible)

- Pas de génération d'agents `.md` depuis les patterns : exigerait des
  templates par pattern. Piste v2 : les sections « Comment l'implémenter »
  des fiches du catalogue comme source de templates.
- Pas d'apply automatique : `compile` écrit, l'humain (ou le gate) valide le diff.

## Surface technique

- Kit : `blueprint_compile(blueprint) -> {artifact, content, hash}` dans
  `forge_server` + route POST `/api/blueprints/<id>/compile` + CLI éventuel.
- La simulation est le prérequis : un blueprint « bloqué » ne compile pas.
- Éditeur : bouton COMPILER, diff affiché avant écriture.

## À arbitrer (Guilhem)

1. Granularité v1 : un mission pack par blueprint (proposé) ou un artefact par node ?
2. Emplacement et suffixe : `.github/prompts/{id}.blueprint.prompt.md` ?
3. La compilation écrit-elle directement (avec `compiled` tracé) ou produit-elle un diff à appliquer ?
