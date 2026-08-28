# Agentic Task Envelope

## Task

- Task id: r7-forge-kit-adoption
- Request: faire consommer à la Forge le grimoire-kit canonique publié, et projeter la gouvernance du kit sur l'hôte qui exécute réellement l'atelier.
- Owner agent: Claude Code (Opus 5) dans VS Code
- Profile: governed
- Current state: `validating`
- Risk level: `medium`

## Context orchestration

| Context item | Source | Reason selected | Freshness | Token budget |
|---|---|---|---|---:|
| Frontière kit/overrides | `_grimoire/kit/`, `_grimoire/overrides/` | Définit ce que le kit régénère et ce que le projet possède ; posée par le commit 1e2866d. | working tree | 2000 |
| Clone produit en chantier | `grimoire-kit/` (branche `docs/cloud-agent-governance-plan`) | Source de l'installation editable à remplacer ; 111 fichiers non committés, 43 commits de retard sur `origin/main`. | working tree | 1500 |
| Écart de code exécuté | `git diff origin/main --stat -- src/` dans le clone | Mesure ce que la Forge n'exécutait pas : `cmd_task.py`, `missions/board.py`, `missions/gates.py`, `standard_checks/`, `mcp/server.py`. | working tree | 2000 |
| Surfaces hôtes | `grimoire host status`, `grimoire host sync --dry-run` | Établit que Claude Code était désynchronisé sur 24 fichiers avant intervention. | exécution de session | 1500 |
| Standard gouverné | `_grimoire/standard/*`, `_grimoire-output/evidence/` | Contrat de preuve opposable du profil governed. | working tree | 3000 |

## Knowledge base usage

| Knowledge source | Query or index | Trust level | Used as source of truth? | Notes |
|---|---|---|---|---|
| grimoire-kit sur PyPI | `pip index versions grimoire-kit` | authoritative | yes | 3.34.2 est la release publiée ; elle fait foi contre l'établi local. |
| grimoire-kit `origin/main` | `git log HEAD..origin/main` | authoritative | yes | 43 commits absents du clone, dont board Mission Ledger, gates opposables, perf hook. |
| Doctrine d'atelier | `.github/copilot-instructions.md` | high | yes | La Forge est un atelier ; elle consomme le produit, elle ne l'héberge pas. |

## Memory usage

| Memory surface | Read/write | Purpose | Integrity check |
|---|---|---|---|
| Mémoire de session Claude Code | read | Rappel de la doctrine atelier/produit et du piège du clone partagé. | Recoupée contre l'état git réel avant toute action. |
| Registre cockpit | read/write | Enrôler la Forge dans son propre cockpit. | `cockpit list` relu après écriture. |

## Tool boundary

| Tool | Permission | Scope | Blast-radius limit |
|---|---|---|---|
| `bash` (lecture, git, grimoire) | read/execute | Diagnostic et commandes `grimoire`. | Aucune commande destructrice ; aucune écriture dans `grimoire-kit/`, clone partagé entre sessions. |
| `uv pip` | write | `.venv/` de la Forge uniquement. | Réversible par `uv pip install -e grimoire-kit`. |
| `grimoire host sync` | write | `.claude/` uniquement, hôte `claude`. | `--dry-run` relu avant écriture ; `settings.local.json` préservé. |
| édition de fichiers | write | `project-context.yaml`, artefacts de preuve de cette tâche. | Sauvegarde préalable de `project-context.yaml` ; pas de commit sans accord. |

## LLM routing

| Step | Provider | Model or capability | Fallback | Data policy |
|---|---|---|---|---|
| Diagnostic, décision et exécution | anthropic | Claude Opus 5 (1M context) via Claude Code | Aucun ; session interactive unique. | Aucun secret, aucune donnée personnelle transmise. |

## Evidence gates

| Gate | Required evidence | Status |
|---|---|---|
| Plan accepté | Guilhem a validé le plan en trois phases puis « ok fais le plan et go fais le tout ensuite ». | complete |
| Version canonique adoptée | `grimoire --version` retourne 3.34.2 depuis PyPI ; l'installation editable sur le clone de chantier est retirée. | complete |
| Non-régression du standard | `grimoire standard verify` reste vert, 0 erreur et 0 avertissement sur 21 artefacts. | complete |
| Surfaces hôtes projetées | `grimoire host status --host claude-code` retourne « à jour » ; 24 fichiers écrits sous `.claude/`. | complete |
| Gouvernance effective, pas déclarative | Le hook `PreToolUse` a refusé une suppression récursive de test ; les hooks `Stop` et `SessionStart` répondent avec une décision structurée. | complete |
| Santé projet | `grimoire doctor` passe 22/22 ; reste un avertissement d'environnement hors dépôt (`GRIMOIRE_NEO4J_PASSWORD`). | complete |
| Déviations documentées | Le critère d'acceptation « editable path » est révisé dans `task-board.yaml` ; motif consigné dans l'evidence pack. | complete |
