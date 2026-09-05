# Agentic Acceptance Record

Un livrable métier n'est accepté que par celui qui le reçoit. Ce dossier relie
chaque critère d'acceptation à sa preuve et porte la décision du client ou du
validateur : accepter, refuser, demander un ajustement.

- Task id: bootstrap
- Profile: governed
- Deliverable: baseline du standard agentique sur Grimoire-Forge, consommant grimoire-kit 3.38.0 sur les deux hôtes
- Validator: Guilhem (mainteneur), décisions du 2026-09-04

## Critères d'acceptation

| ID | Critère | Preuve | Statut |
|---|---|---|---|
| AC-001 | `grimoire standard verify .` passe sans erreur depuis la racine de la Forge | `grimoire standard verify .` — OK, profil governed, 0 erreur (2026-09-04) | passé |
| AC-002 | Les artefacts du profil governed sont générés, remplis et vérifiés | `grimoire standard fix . --apply` puis `verify` ; 28 artefacts requis présents | passé |
| AC-003 | La Forge consomme la release publiée du kit, pas un établi | `grimoire --version` → grimoire-kit 3.38.0 depuis PyPI ; `pip freeze` sans ligne editable | passé |
| AC-004 | Les surfaces des deux hôtes sont projetées | `grimoire host sync` — 24 fichiers Claude Code inchangés ; Copilot projeté le 2026-09-04 (PR Forge #27) | passé |
| AC-005 | Les gardes des hooks sont versionnées et bloquent réellement | `.github/hooks/lib/`, `grimoire-hooks-smoke.sh` ok, `enforced=13` ; payload PreToolUse destructif → `ask` | passé |

## Vérifications

| Vérification | Résultat | Preuve |
|---|---|---|
| Tests | passé | suite unitaire du kit verte sur chaque PR fusionnée ; CI complète sur chaque PR depuis #268 |
| Build / lint | passé | `make release VERSION=3.38.0` : ruff 0.15.20, mypy, ratchet, wheel installée dans un venv neuf |
| Sécurité | passé avec waivers | audit de dépendances vert ; 3 waivers chromadb reconduits au 2027-02-28 (#272) |
| Design / accessibilité | revue livrée, correction non commencée | `web/DESIGN-REVIEW-2026-09.md` (#263) : 7 décisions en attente |
| Evals IA | non démontré, indicatif | campagne 2026-09-04 (#278) : 0 régression dure sous enforcement, n = 3 répétitions |

## Risques et limites

| Risque ou limite | Impact | Décision |
|---|---|---|
| Deux piles de hooks sous Copilot (kit + atelier) | double contexte de session | accepté, arbitrage écrit dans agent-bridges.yaml |
| `art-director.agent.md` maison à un chemin géré | `host status --host copilot` reste « désynchronisé » | accepté, la version BMM prime |
| Effet de l'enforcement non démontré sur la qualité livrée | claim produit borné à « 0 régression dure » | accepté, consigné au rapport de campagne |

## Décision

| Décision | Validateur | Date | Commentaire |
|---|---|---|---|
| accepté | Guilhem | 2026-09-04 | « je suis ok pour tous les points tu peux les exécuter », puis « ok go tu peux lancer le tout » ; exécution consignée dans evidence/r7-forge-kit-adoption/evidence-pack.md |

Décisions : `accepté`, `refusé`, `ajustement demandé`, `en attente`. Une
décision `accepté` sans validateur ni date n'en est pas une.
