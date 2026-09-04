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

## Suite r7 — activation automatique de la persona d'entrée

### Objectif

Rendre effective la désignation `entry_point` que le kit produit déjà mais que
personne ne consomme. `collect_agents()` marque `concierge` comme point d'entrée,
`ProjectSurface.entry_agent()` sait le retrouver — et cet accesseur n'a **aucun
appelant** dans `src/` ni dans `tests/`. La désignation ne change qu'une phrase
*à l'intérieur* du fichier de sous-agent, phrase que rien ne lit tant que
quelqu'un n'a pas déjà décidé de router vers lui. Déclaration sans consommation.

Cible : **grimoire-kit** (produit), pas la Forge. La Forge est consommatrice.

### Contrainte d'hôte à contourner

Aucun hôte n'expose de « lancer cet agent au démarrage » : Claude Code n'instancie
un `.claude/agents/*.md` que via l'outil Agent, VS Code Copilot exige une sélection
dans le dropdown. Le substitut disponible sur les deux : l'injection de contexte
`SessionStart` (`additionalContext`). On n'instancie pas le sous-agent — on charge
sa persona dans la boucle principale.

### Périmètre outillé

| Outil | Permission | Portée | Limite de rayon |
|---|---|---|---|
| édition de fichiers | write | worktree jetable `scratchpad/kit-autostart`, branche `feat/entry-persona-autostart` depuis `origin/main` | Aucune écriture dans `grimoire-kit/` (clone partagé entre sessions, working tree sale sur un autre chantier) |
| `pytest` | execute | suite du worktree | Aucun effet sur la Forge |
| `grimoire-hook` | execute | lecture seule, `PYTHONPATH` pointé sur le worktree | Prouve le nouveau code sans toucher au `.venv` de la Forge |
| édition de preuve | write | `_grimoire-output/evidence/r7-forge-kit-adoption/` | — |

### Critères de sortie

1. `HostProfile` nomme la capacité manquante ; les 5 profils la déclarent à `False`.
2. `gaps_for()` rend le manque et son substitut, donc `host status` l'affiche.
3. `decide_activation` injecte la persona d'entrée dans le contexte de session,
   sur tout hôte dont le hook `SessionStart` tourne.
4. Un test échoue si l'accesseur redevient inutilisé.
5. Exécution réelle du hook contre la racine de la Forge : le concierge apparaît
   dans `additionalContext`.

## Suite r7 — vérification de l'errata d'un projet consommateur

### Objectif

Un projet neuf initialisé avec `grimoire-kit` 3.34.2 a produit un errata de neuf
défauts. Établir, pour chacun, s'il est réel, et le localiser dans le **code
source du kit** — pas dans l'installation du projet témoin, qui n'est qu'un
symptôme. Rendre un verdict opposable, pas une paraphrase du rapport.

Cible : **grimoire-kit** (produit). La Forge ne sert ici que d'établi
d'observation : elle héberge le venv 3.34.2 et le projet de reproduction.

### Périmètre outillé

| Outil | Permission | Portée | Limite de rayon |
|---|---|---|---|
| `grimoire init` | write | `scratchpad/repro-01/` uniquement, hors dépôt | Projet jetable ; retiré du cockpit en fin de tâche |
| lecture du paquet installé | read | `.venv/lib64/python3.14/site-packages/grimoire/` | Aucune écriture ; le paquet PyPI fait foi |
| `grimoire-hook`, `grimoire standard` | execute | `scratchpad/repro-01/` | Aucun effet sur la Forge ni sur `grimoire-kit/` |
| scripts d'audit | write | `/tmp/claude-1000/audit_*.py` | Lecture seule sur le projet audité |
| `gh issue list` | read | dépôt `Grimoire-kit` | Aucune écriture ; création d'issue soumise à accord |
| édition de preuve | write | `_grimoire-output/evidence/r7-forge-kit-adoption/` | — |

Aucune écriture dans `grimoire-kit/` : le clone est partagé entre sessions et
son arbre de travail est sale sur un autre chantier.

### Critères de sortie

1. Chaque défaut de l'errata reçoit un verdict — confirmé, confirmé avec cause
   différente, ou infirmé — adossé à une commande rejouable.
2. Chaque défaut confirmé est localisé à la ligne dans le source du kit.
3. La thèse centrale de l'errata (`doctor` vert sur un projet criblé de chemins
   morts) est mesurée, pas reprise sur parole.
4. L'audit systématique que l'errata propose est exécuté : il doit rendre au
   moins ce que l'errata a relevé, sinon la méthode est fausse.
5. Les défauts que l'errata n'a pas vus sont nommés.

## Suite r7 — exécution du plan d'audit du 2026-09-04

### Objectif

Exécuter le bloc « cette semaine » du plan validé par Guilhem le 2026-09-04, plus
ses deux ajouts : la Forge consomme l'intégralité de ce que le kit sait projeter
(hôtes, workflows, standard), et une revue de direction artistique de
`grimoire serve` / cockpit entre au plan.

### Périmètre outillé

| Outil | Permission | Portée | Limite de rayon |
|---|---|---|---|
| `gh` (PR, API branches) | write | dépôt `Grimoire-kit` : merge de #245 ou de son remplaçant, protection de `main`, suppression de branches fusionnées | Aucune suppression de branche non fusionnée ; aucun `--force` sur `main` |
| worktree jetable `scratchpad/kit-245` | write | rebase de la branche de #245 sur `origin/main` | Jamais dans `grimoire-kit/` (clone partagé) |
| édition de fichiers Forge | write | `.github/hooks/lib/` (nouveau), `.github/hooks/scripts/*.sh`, `.vscode/tasks.json`, surfaces `host sync`, `task-board.yaml`, preuve r7 | Les hooks modifiés passent en `modified` au registre jusqu'à `hooks-promote` après smoke vert |
| `grimoire host sync`, `grimoire up`, `grimoire task` | write | Forge uniquement | `--dry-run` relu avant toute écriture ; hooks maison du gateway préservés ou restaurés |
| git Forge | write | commit, branche, PR `work/harmonisation-followup-20260703` → `main` | Pas de push forcé |
| nettoyage du clone et des worktrees | write | après découplage des hooks seulement ; untracked sauvegardés en branche `wip/` avant tout `checkout` | Aucun `stash`, aucun `reset --hard` sur du non sauvegardé |

### Critères de sortie

1. `Grimoire-kit` : #245 (ou son remplaçant rebasé) fusionnée ; trois branches cloud-gov supprimées ; `main` protégée par des checks requis.
2. Forge : aucune référence à `grimoire-kit/` dans `.github/hooks/scripts/` pour les scripts de garde ; `grimoire-hooks-smoke.sh` vert ; un `rm -rf` de test toujours refusé.
3. Forge : les 42 fichiers committés, PR vers `main` fusionnée, board sans tâche `review`, `standard verify` vert.
4. Forge : `host status` à jour sur les deux hôtes, ou refus motivé consigné.
5. Clone `grimoire-kit/` sur `main` propre, worktrees périmés retirés, untracked conservés dans une branche.
