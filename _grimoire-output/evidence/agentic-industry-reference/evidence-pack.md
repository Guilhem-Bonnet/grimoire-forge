# Agentic Evidence Pack

## Summary

- Task id: agentic-industry-reference
- Profile: governed
- Outcome: référence agentique industrielle livrée dans le produit grimoire-kit (PR #315), branchée dans le socle des agents et livrée à chaque projet via le scaffold.
- Final state: validated

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Six rapports de collecte (Anthropic, OpenAI, Google/A2A, protocoles et normes, frameworks, recherche et benchmarks) | sous-agents general-purpose, sources primaires, WebFetch/WebSearch du 2026-09-08 | session Claude Code | 6/6 rendus avec étiquettes de provenance |
| Fichier de référence | `grimoire-kit@9d5ca9f6:framework/agentic-industry-reference.md` | session Claude Code | 762 lignes, 12 sections, registre des sources et protocole de mise à jour |
| Branchement scaffold | `grimoire-kit@9d5ca9f6:src/grimoire/core/scaffold.py` (`_PROTOCOL_DOCS`) | session Claude Code | livré dans `_grimoire/kit/framework/` de chaque projet |
| Pointeurs socle | `framework/agent-base.md` section « Référence industrielle », `framework/agent-base-compact.md` | session Claude Code | déclencheurs de chargement déclarés |
| Test de livraison | `tests/test_scaffold.py::test_plan_includes_framework` | session Claude Code | assertion ajoutée |
| PR produit | https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/315 | gh | ouverte, non mergée |
| Audit d'écart contre la référence | `_grimoire-output/evidence/bootstrap/audit-ecarts-reference-agentique-20260908.md` | cinq sous-agents Sonnet, vérification manuelle des bloquants | 8 bloquants, 15 actions |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Tests ciblés kit | `PYTHONPATH=src .venv/bin/python -m pytest tests/test_scaffold.py tests/test_delivered_paths_resolve.py -q` | pass | 47 passed depuis le worktree jetable sur origin/main 3.40.0 |
| Lint | `.venv/bin/python -m ruff check src/grimoire/core/scaffold.py tests/test_scaffold.py` | pass | All checks passed |
| Gel du framework | `python scripts/check-code-ratchet.py` | pass | code ratchet OK, le gel ne porte que sur .py/.sh |
| Gate Forge | `grimoire standard gate check --task-id bootstrap --strict` | voir addendum du pack bootstrap | |
| Verify Forge | `grimoire standard verify .` | voir addendum du pack bootstrap | |

## Controls

| Control family | Applied? | Evidence | Gap |
|---|---:|---|---|
| Governance | yes | Cible produit conforme à la doctrine Forge/produit ; aucun fichier d'atelier modifié hors preuve. | |
| Quality | yes | pytest, ruff, ratchet ; charte documentaire (CommonMark, icônes SVG, aucune estimation temporelle). | |
| Runtime | n/a | Aucune surface runtime modifiée. | |
| Knowledge | yes | Registre des sources avec niveaux de preuve dans le fichier. | Pages inaccessibles listées en fin de registre. |
| Model/provider | yes | Sous-agents Claude uniquement. | |

## Deviations and accepted risks

| Deviation | Impact | Accepted by | Review trigger |
|---|---|---|---|
| Pages `openai.com/index/*`, whitepapers Kaggle, quelques leaderboards inaccessibles le jour de la veille | Contenu étiqueté `[non vérifié]` ou `[agrégateur]`, non citable comme fait | session (hypothèse autonome) | Prochaine révision trimestrielle (section 12 du fichier) |
| La Forge ne reçoit le fichier qu'après release du kit et `grimoire host sync` | Les agents de la Forge ne le chargent pas encore | session | Merge de la PR #315 puis release |
| Aucune tâche ajoutée au task-board de la Forge | La preuve est rattachée au task-id `bootstrap` comme demandé par le hook | session | Si Guilhem veut une tâche dédiée |

## Completion statement

La tâche est complète : la référence est livrée dans le produit avec sa mécanique de distribution, testée, et la PR est ouverte pour revue.
