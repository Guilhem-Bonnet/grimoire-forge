# R7 Forge kit adoption — Evidence Pack

## Summary

- Task id: `r7-forge-kit-adoption`
- Outcome: la Forge consomme la release canonique 3.34.2 et projette la gouvernance du kit sur Claude Code.
- Final state: validating

## Historique

Le pack d'origine (2026-07-12) était une rétro-qualification : le travail avait été
fait sans preuve, et le contenu n'a jamais été reconstitué. Ce trou de gouvernance
reste acté. L'inventaire ci-dessous couvre le cycle du 2026-08-28, qui reprend la
tâche là où elle avait été laissée.

## Constat d'entrée

| Observation | Commande | Résultat |
|---|---|---|
| Le kit exécuté venait d'un établi, pas d'une release | `pip freeze \| grep grimoire` | editable sur `grimoire-kit@d1789680` |
| L'établi était en retard et non committé | `git rev-list --left-right --count HEAD...origin/main`, `git status --short \| wc -l` | 5 ahead / 43 behind, 111 fichiers non committés |
| Le code exécuté était amputé | `git diff origin/main --stat -- src/` | `cmd_task.py` (418 l.), `missions/board.py` + `gates.py` (456 l.), `standard_checks/` (1995 l.), `mcp/server.py` (91 l.) absents |
| L'hôte exécutant n'était pas gouverné | `grimoire host status --host claude-code` | désynchronisé, 24 fichiers à régénérer |
| La Forge ignorait son propre cockpit | `grimoire cockpit list \| grep -c Grimoire-Forge` | 0 |

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Adoption de la release canonique | `.venv/` | `uv pip install --upgrade grimoire-kit==3.34.2` | 3.32.0 editable remplacé par 3.34.2 depuis PyPI |
| Version effective | session | `grimoire --version` | `grimoire-kit 3.34.2` |
| Capacité regagnée | session | `grimoire task --help` | Mission Ledger disponible : `add`, `claim`, `move`, `board`, `context` |
| Non-régression du standard | `_grimoire/standard/` | `grimoire standard verify` | vert, 21 artefacts, 0 erreur, 0 avertissement |
| Santé projet | session | `grimoire doctor` | 22/22 après correction de `memory.neo4j_uri` |
| Projection de l'hôte | `.claude/` | `grimoire host sync --host claude` | 24 fichiers : 7 sous-agents, 3 skills, 12 commandes, `settings.json` |
| Hôte synchronisé | session | `grimoire host status --host claude-code` | « Claude Code à jour » |
| Le garde refuse réellement | session | payload `PreToolUse` avec `rm -rf` sur `_grimoire/` | refus : « recursive/forced delete », la commande n'a pas été exécutée |
| Le garde laisse passer le légitime | session | payload `PreToolUse` avec `ls` | `permissionDecision: allow`, 95 ms par appel |
| Le gate de sortie mord | session | payload `Stop` | `decision: block` tant que les gates de r7 sont rouges |
| Enrôlement cockpit | registre cockpit | `grimoire cockpit add .` | `grimoire-forge` présent dans `cockpit list` |
| Identité projet alignée | `project-context.yaml` | `grimoire setup` puis section `user:` | `grimoire status` affiche Guilhem / expert |

## Décisions et déviations

| Sujet | Décision | Motif |
|---|---|---|
| Critère « installs canonical Kit via editable path » | Révisé : la Forge installe la release publiée. | L'editable pointait sur une branche de chantier ; l'atelier doit recevoir ce que reçoit un utilisateur. Le mode développement reste accessible par `uv pip install -e grimoire-kit`. |
| Clone `grimoire-kit/` | Non modifié. | Partagé entre sessions, 111 fichiers en vol ; l'arbitrage de ce travail appartient au repo produit. |
| Double pile agentique BMM / kit | Laissée en l'état. | Les 22 wrappers `_grimoire-runtime/` fonctionnent ; fusionner relève d'un chantier d'atelier sans blocage produit derrière. |
| Registre cockpit | 57 entrées d'évals conservées. | `cockpit prune` les déclare vivantes ; les retirer à la main risquerait d'effacer une campagne d'une autre session. |

## Restes connus

| Reste | Nature | Porteur | État |
|---|---|---|---|
| `GRIMOIRE_NEO4J_PASSWORD` | Aucun : la variable était déjà exportée par `~/.zshrc` depuis le 2026-08-27, et le mot de passe est validé contre le conteneur (`cypher-shell` retourne `ok`). L'avertissement venait de `memory.neo4j_uri` vide ; il est tombé avec sa correction. | — | clos |
| `grimoire setup` propage les options vers `copilot-instructions.md` sans écrire la source de vérité, puis annonce « in sync » | Défaut du kit, reproduit sur un projet neuf : `setup --check` contredit le `setup` qui vient de tourner. | repo produit Grimoire-kit | issue #216 |
| Surfaces Copilot non projetées | Tranché : la projection est refusée tant que `host sync` reste tout-ou-rien. Elle apporterait six agents, trois compétences et cinq prompts, mais écraserait `grimoire-session-start.json` et `grimoire-pre-compact.json`, qui passent par `grimoire-hook-gateway.sh` et son registre de promotion. `art-director.agent.md` est préservé sans `--force`, les hooks non. | repo produit Grimoire-kit | issue #218 |
| Artefacts régénérables non ignorés | Index `_grimoire/_memory/*.sqlite3` et context-packs de `repo-contexts/` sortis du suivi git. | — | clos |

## Suites exécutées

| Action | Commande | Résultat |
|---|---|---|
| Publication de la branche | `git push` | `6898cab..a9260c1`, hook `pre-push` vert sans bypass |
| Défaut kit qualifié puis remonté | `gh issue create` | [Grimoire-kit#216](https://github.com/Guilhem-Bonnet/Grimoire-kit/issues/216), reproduction minimale et lecture du code jointes |
| Projet de reproduction retiré du cockpit | `grimoire cockpit remove repro` | registre rendu à son état d'avant le test |
| Asymétrie du sync qualifiée puis remontée | `host sync --host copilot` sur un projet jetable portant un hook maison | le hook est remplacé sans `[!]` ni `--force` ; [Grimoire-kit#218](https://github.com/Guilhem-Bonnet/Grimoire-kit/issues/218) |
