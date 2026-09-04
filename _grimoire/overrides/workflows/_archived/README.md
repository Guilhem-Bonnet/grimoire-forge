# Archive des workflows legacy `_grimoire/_config/custom/workflows/`

Ces fichiers viennent de l'ancien layout `_bmad/_config/custom/` et ont été déplacés ici le **21 avril 2026** parce que :

- **Zéro consommateur actif** : aucune skill, aucun agent, aucun workflow du runtime ne les référence par chemin.
- **Références internes cassées** : tous les `<a href="../../README.md">` et `<img src="../../docs/assets/icons/*.svg">` pointaient vers le layout `_bmad/` qui n'existe plus.
- **Fonctionnalités superseded** : chaque concept a été réimplémenté sous `.github/skills/` ou `_grimoire-runtime/` :
  - `incident-response.md` → `.github/skills/grimoire-incident-response/SKILL.md`
  - `state-checkpoint.md` → protocoles SOG/AORA dans `_grimoire-runtime/core/agents/grimoire-master.md`
  - `subagent-orchestration.md` → SOG + `runSubagent` natif
  - `boomerang-orchestration.md` → handoffs BMM (`_grimoire-runtime/_config/agent-surface-index.csv`)
  - `repo-map-generator.md` → `grimoire-kit/framework/tools/` (divers analyzers)

Canon : `_grimoire/` est priorité P5 dans `docs/governance/canon-structurel-et-navigation-agentique.md` (« Ne jamais utiliser comme point de depart nominal »).

Le scanner `harmony_check` ignore automatiquement les dossiers préfixés `_archive*`.
