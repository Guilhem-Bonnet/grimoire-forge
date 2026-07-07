# Rework Vitrine/Atelier — note d'intégration

Date : 2026-07-07
Source : `Grimoire(3).zip` (design Claude Design, brief UX de la session
extensions/blueprint). Les deux documents HTML archivés ici sont les
livrables de conception ; le code du rework vit dans le kit public.

## Où c'est intégré

- Repo : `Guilhem-Bonnet/Grimoire-kit`, branche `feat/site-atelier`, PR #64.
- Le zip a remplacé `web/` (commit d'atterrissage `aa607ec7`), puis la couche
  données a été réécrite en anti-corruption layer réelle (`atelier-nav.js`),
  toutes les pages branchées sur `data/*.json` générés et l'API
  `grimoire serve`, le pont Studio v2 ajouté au serveur
  (`_studio_to_v1` dans `forge_server.py`).

## Décisions prises pendant l'intégration

- Les refs de patterns inventées par le design (PRD-01, SEC-02, OPS-01,
  MEM-01, ENG-01, DAT-01…) sont remappées sur le catalogue réel
  (ORC-02, QUA-14, GOV-02, KNO-02, ORC-11 ; DAT-01 supprimée).
- Pins des patterns : heuristique par famille (dupliquée JS/Python,
  documentée comme provisoire) en attendant une curation par pattern
  dans le catalogue — candidate au brainstorm blueprint.
- Le format v2 (état Studio) est la source de vérité persistée dans
  `_grimoire/blueprints/*.blueprint.json` ; le serveur le projette en v1
  pour lint/simulation/compilation.
- `project-selector.html` (démo de composant) supprimée ; le sélecteur
  multi-projets réel attend des endpoints `/api/projects` (non faits).

## Preuve E2E

Parcours vérifié au navigateur sur une installation locale vierge :
serve → hub atelier réel → installation crewai (artefacts écrits) →
création de flow → simulation (verdict API) → compilation
(`.github/prompts/*.blueprint.prompt.md`, sha256 identique entre le
blueprint persisté et l'artefact).
