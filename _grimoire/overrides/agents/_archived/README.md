# Archive legacy custom agents

Moved here **21 avril 2026** comme suite à la review E2E.

Ces 8 agents héritent de l'ancien layout `_bmad/_config/custom/agents/` et ne sont référencés par aucun workflow, skill ou manifest actif dans :

- `_grimoire-runtime/_config/`
- `_grimoire-runtime/bmm/`, `_grimoire-runtime/cis/`, `_grimoire-runtime/tea/`
- `.github/skills/`, `.github/agents/`, `.github/prompts/`

**Correspondances modernes :**

| Fichier archivé | Remplaçant actuel |
|---|---|
| `art-director.md` | `.github/agents/art-director.agent.md` + `_grimoire-runtime/cis/agents/art-director.md` |
| `project-navigator.md` | `.github/skills/grimoire-project-explore/` |
| `memory-keeper.md` | `_grimoire-runtime/_memory/` + `/memories/` (VS Code) |
| `agent-optimizer.md` | `agent-builder` (`.github/agents/`) + `grimoire-kit/framework/tools/agent-lint.py` |
| `creative-toolsmith.md` | `workflow-builder` + `tool-advisor.py` |
| `concierge.md` | `grimoire-master` orchestrator SOG |
| `vectus.md` | `.github/skills/grimoire-intent-routing/` |
| `custom-agent.tpl.md` | `grimoire-kit/archetypes/*/agents/` + `agent-builder` |

Canon : `_grimoire/` est P5 archéologie uniquement (`docs/governance/canon-structurel-et-navigation-agentique.md`).

Le scanner `harmony_check` exclut automatiquement les dossiers préfixés `_archive*`.
