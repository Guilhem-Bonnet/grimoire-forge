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

## Connaissance mutuelle des deux piles

Les 23 agents BMM et les 7 agents du kit vivaient sur deux hôtes sans registre commun.
Rien ne disait qui existe, qui passe la main à qui, ni quels agents faisaient doublon.

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Carte unique des deux piles | `.github/copilot-instructions.md`, entre marqueurs | `scripts/agent-index.py` | 30 agents, 4 ponts, 2 doublons arbitrés, graphe Mermaid des relations |
| Point d'écriture atteignant les deux hôtes | `.github/copilot-instructions.md` | — | chargé nativement par Copilot, importé par `CLAUDE.md` pour Claude Code |
| Ponts déclarés à la main | `_grimoire-runtime/_config/agent-bridges.yaml` | — | les agents du kit étant régénérés, ils ne peuvent rien déclarer : la relation qui traverse la frontière vit là |
| Roster de l'orchestrateur exploité | frontmatter `agents:` de `grimoire-master.agent.md` | `agent-index.py` | 21 agents dispatchables ; seul `bmad-master`, alias de compatibilité, est hors roster |
| Frontmatter du master réparé | `.github/agents/grimoire-master.agent.md` | — | 8 lignes indentées à la tabulation, YAML invalide au sens strict, illisible par tout parseur |
| Garde de cohérence | `.github/hooks/git/pre-commit` | `agent-index.py --check` | bloque un commit qui touche un agent sans régénérer la carte |
| Garde éprouvé sur trois cassures | session | handoff fantôme, pont orphelin, agent renommé | `exit=2` sur chacune, `exit=0` au retour |
| Faux registre supprimé | `_grimoire-runtime-output/.agent-graph.yaml` | — | métriques inventées (« US-042 », trust 87, sprint-5), figé depuis mars 2026, ni lu ni écrit par quoi que ce soit |

## Release 3.36.0 (2026-09-03)

Quatre PR fusionnées sur le produit (#232, #233, #225, #248), release recousue et
publiée (PR #249, tag `v3.36.0`, PyPI et GitHub Release verts), puis consommée ici.

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Release 3.36.0 consommée | `.venv/` | `uv pip install --upgrade grimoire-kit==3.36.0` | `grimoire --version` 3.36.0 ; `doctor` 24/24 ; `host status --host claude-code` à jour ; `standard verify` vert ; `workflows list -k orchestration` : 6 |

## Release 3.37.0 (2026-09-03, soir)

Dix PR fusionnées sur le produit (#250 à #259), release recousue, validée par le
nouveau garde de couverture du changelog, publiée (PR #260, tag `v3.37.0`, PyPI et
GitHub Release verts), puis consommée ici.

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Release consommée | `.venv/` | `uv pip install --upgrade grimoire-kit==3.37.0` | `grimoire --version` 3.37.0 ; `doctor` 24/24 |
| Artefacts obligatoires de la norme générés | `_grimoire-output/evidence/bootstrap/claim-ledger.md`, `_grimoire/standard/runtime-surface-registry.yaml` | `grimoire standard fix --apply` | `verify` passait de FAIL (2 artefacts manquants) à OK |
| Claim ledger rempli | `claim-ledger.md` | main | 8 affirmations du cycle, chacune avec sa preuve ; une contredite (CL-003, #231), une hypothèse (CL-008, usage des agents) |
| Registre des surfaces rempli | `runtime-surface-registry.yaml` | main | 7 surfaces de contrôle, 4 de sortie, 1 dérive (trace Copilot arrêtée le 2026-04-26 sous un hook déclaré enforced), 2 nettoyages |
| Manifeste aligné | `_grimoire/standard/standard-profile.yaml` | main | `required_artifacts` porte les deux nouveaux artefacts |
| Traçabilité vers la norme | session | `grimoire standard traceability --profile governed` | niveau N4, 38 exigences couvertes, 17 trous listés |
| Standard épinglé à jour | session | `grimoire standard upstream` | tête distante identique (53b2c342) |

## Errata (2026-09-03)

| Point | Constat |
|---|---|
| Version du kit | Le venv est passé de 3.34.2 à 3.35.4 le 2026-08-31, hors de ce cycle et sans ligne de preuve. `grimoire --version` et `pip show grimoire-kit` concordent sur 3.35.4 ; les vérifications de ce pack restent valides, la version citée plus haut ne l'est plus. |
| Registre cockpit | Les 57 entrées d'évals « vivantes » du 2026-08-28 pointaient sous `/tmp`, vidé au redémarrage : `cockpit prune -y` en a retiré 71 le 2026-09-03, 6 projets réels conservés. |

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

## Suite — la persona d'entrée n'entrait nulle part

Question posée : pourquoi le concierge ne s'active-t-il pas au lancement de
Claude Code ? Le diagnostic a trouvé mieux qu'une absence de câblage : une
désignation produite, transportée, jamais consommée.

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Accesseur sans appelant | `grimoire.hosts.surface.ProjectSurface.entry_agent` | `grep -rn entry_agent` sur `site-packages`, `src/`, `tests/` | 1 seule occurrence : sa propre définition. Zéro appelant, y compris en test |
| Désignation circulaire | `hosts/emitters/claude_code.py:103`, `copilot.py:66` | lecture du code | `entry_point` ne change qu'une phrase *dans* le fichier de sous-agent — lue seulement si l'on a déjà routé vers lui |
| Aucun hôte n'offre l'autostart | `hosts/capabilities.py` | lecture des 5 profils | pas de champ pour « ouvrir une session dans un agent » ; Claude Code passe par l'outil Agent, Copilot par le dropdown |
| Le hook n'injectait aucune persona | `grimoire-hook --host claude --event SessionStart` sur la Forge | exécution | `additionalContext` ne portait que la directive standard |
| Manque déclaré, plus supposé | `HostProfile.agent_autostart` + `gaps_for` | commit `c3c3f965` | faux sur les 5 hôtes ; substitut nommé hôte par hôte |
| Substitut réel, pas aspirationnel | rendu du plan Codex sur la Forge | `emitter_for(HostId.CODEX).plan(...)` | `AGENTS.md` porte déjà `` `concierge` (entrée) `` — le repli annoncé pour les hôtes sans hook existe |
| Injection prouvée bout-en-bout | racine réelle de la Forge, `PYTHONPATH` sur le worktree | `grimoire-hook --host claude --event SessionStart` | `additionalContext` ouvre sur `[Grimoire — persona d'entrée] … **concierge**` et le chemin `_grimoire/kit/agents/concierge.md` |
| Même injection sur l'autre hôte | idem, `--host copilot` | exécution | identique : la décision est neutre en hôte |
| Directive validée préservée | même sortie | exécution | `[Grimoire Standard — activation]` intacte, en dernier, avec le `task_id` vivant `r7-forge-kit-adoption` |

### Falsification

Le test qui compte est celui qui échoue quand le garde disparaît.

| Sabotage | Commande | Résultat |
|---|---|---|
| API retirée (`src/` remis à `origin/main`) | `git stash push -- src/` puis `pytest tests/unit/test_hosts.py` | `ImportError: cannot import name 'entry_persona_context'` — collecte interrompue |
| Injection neutralisée (`context = directive`) | `pytest -k "persona or directive"` | `1 failed` — `AssertionError: la persona d'entrée n'atteint pas la session` |
| Code restauré | `pytest tests/unit/test_hosts.py` | 58 passed |

### Suites de tests

| Suite | Commande | Résultat |
|---|---|---|
| Ciblée | `pytest tests/unit/test_hosts.py` | 58 passed |
| Unitaire complète | `pytest tests/unit --maxfail=200` | 2932 collectés, 3 échecs |
| Lint | `ruff check src/ tests/unit/test_hosts.py` | All checks passed |
| Format | `ruff format --check src/grimoire/hosts/` | 13 files already formatted |
| Types | `mypy src/grimoire/hosts/{capabilities,decisions}.py` | Success: no issues found |

Les 3 échecs sont antérieurs au changement et tiennent à l'environnement, non au
code : `jsonschema` et le SDK `mcp` sont des extras absents du venv de la Forge.
Vérifié en remettant `src/` et `tests/` à `origin/main` — les mêmes 3 échouent.
La CI, elle, installe les extras ; ces trois-là n'y sont pas rouges.

### Périmètre et livraison

| Point | État |
|---|---|
| Cible | Produit (`grimoire-kit`), pas l'atelier — la doctrine est respectée sans dérogation |
| Isolation d'écriture | Worktree jetable depuis `origin/main` ; `grimoire-kit/` (clone partagé, working tree sale sur un autre chantier) jamais touché |
| Commit | `c3c3f965` sur `feat/entry-persona-autostart`, non poussé |
| Effet dans la Forge | **Pas encore actif** : le venv exécute `grimoire-kit` 3.34.2 depuis PyPI. Une release, ou un basculement d'installation, est nécessaire — décision non prise sans arbitrage |
| Écart de format hérité | `ruff format` a ajouté une ligne vide manquante avant `class ToolFacts` : `decisions.py` n'était pas format-clean sur `origin/main` |

## Vérification de l'errata grimoire-kit 3.34.2

Le rapport venait d'un projet consommateur. Il ne prouvait rien sur le kit tant
qu'on ne l'avait pas rejoué contre la release publiée. Reproduction :
`grimoire init . -y -a platform-engineering,infra-ops,fix-loop -b weaviate-server`
sur un projet Terraform jetable, avec le venv de la Forge en 3.34.2 — la même
version que `origin/main` du dépôt produit.

### Thèse centrale — mesurée

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Le doctor est vert sur un projet criblé | `scratchpad/repro-01` | `grimoire doctor` | `20/20 checks passed` |
| Au même instant | idem | script d'audit de résolution de chemins | 99 références mortes, 44 chemins distincts |
| Aucun check ne lit un chemin livré | `cli/cmd_doctor.py` | lecture | le doctor vérifie l'existence de répertoires, jamais la résolution des chemins cités dans les fichiers qu'il livre |

### Verdicts

| Défaut | Verdict | Localisation dans le source du kit |
|---|---|---|
| BUG-1 — `_grimoire/_config/` mort | confirmé | `core/layout.py:47-58` déclare `_config` comme layout **pré-frontière** ; `grimoire migrate` déplace les vieux projets, mais le contenu livré cite toujours l'ancien chemin. Un projet neuf n'a pas de legacy : les 21 références sont mortes à l'installation. |
| BUG-2 — carte du concierge fantôme | confirmé, cause différente | `archetypes/meta/agents/concierge.md:117-127`. Ce n'est pas une substitution ratée : le fichier ne contient **aucun** placeholder. Rien dans le kit ne sait générer cette carte. |
| BUG-3 — `workflow-graph.yaml` | confirmé, sévérité à revoir | `data/framework/workflows/workflow-graph.tpl.yaml` est un **exemple** (« Usage : copier dans `_grimoire-output/.runs/{run_id}/` »). `_strip_tpl_suffix` (`core/scaffold.py:53-62`) l'installe en `.yaml` et efface le seul signal « gabarit ». Rien ne route depuis lui. Il cite aussi `_grimoire/bmm/…`, inexistant côté kit. |
| BUG-4 — substitution partielle | diagnostic faux, défaut secondaire réel | `_plan_placeholder_rendering` (`core/scaffold.py:654-681`) substitue partout où un placeholder existe. Le défaut réel est au-dessus : `_render_placeholders` (`:41-50`) fait un `str.replace` sur tout le fichier, **y compris le bloc de commentaire qui documente les placeholders** — la légende devient « Stack — Nom de l'agent développement ». |
| BUG-5 — `cc-verify.sh` | confirmé, sous-compté | `data/framework/agent-base.md` lignes **21, 632 et 672** — trois références legacy, pas deux. Seul fichier non migré du kit. |
| BUG-6 — `failure-museum.py` | confirmé, cause différente | Le script **existe** : `data/framework/tools/failure-museum.py`, 16,5 Ko. Il n'est jamais déployé : `_plan_framework` (`core/scaffold.py:790-853`) copie une liste blanche de quatre fichiers ; les 50 outils de `framework/tools/` (~1,3 Mo) ne sortent jamais de la wheel. |
| BUG-7 — hook sur la donnée | confirmé, reproduit 3× | `hosts/decisions.py:127-142` applique `_DESTRUCTIVE_PATTERNS` par `re.search` sur la chaîne `command` entière. Heredoc de doc → `deny`. Message de commit citant la commande → `deny`. `Write` du même contenu → `allow`, car `command` est vide pour un outil d'écriture. |
| BUG-8 — placeholders mémoire | confirmé, deux causes distinctes | (a) `{{project_name}}`/`{{init_date}}` : le rendu ne couvre que `agents/` et `workflows/` (`core/scaffold.py:672`), `_memory/` est hors périmètre ; `init_date` n'est dans aucune table de variables. (b) `$project_name` : `_DECISIONS_LOG` est passé en `content=` **brut** (`core/scaffold.py:905-909`) alors que `_SHARED_CONTEXT_DEFAULT`, huit lignes plus haut, passe par `Template(...).safe_substitute(v)`. |
| BUG-9 — `standard fix --apply` | confirmé | `cli/cmd_standard.py:1166` calcule `actions` avant l'apply ; `:1182-1184` réimprime la liste entière après écriture, sans replanifier. |
| Réfutation du code retour | juste | `standard verify` : 0 erreur / 5 avertissements → `exit 0` ; 1 erreur → `exit 1`. Mesuré sans pipe. |

### Reproductions exécutées

| Action | Commande | Résultat |
|---|---|---|
| Projet témoin | `grimoire init . -y -a platform-engineering,infra-ops,fix-loop -b weaviate-server` | 17 dirs, 51 files, 19 agents |
| Chemins morts | script d'audit sur les `.md`/`.yaml`/`.csv`/`.sh` livrés | 99 références mortes, 44 chemins distincts, dont 21 sur `_grimoire/_config/` |
| Cohérence du roster | croisement des cartes de routage avec `agent-manifest.csv` | 9 agents cités inexistants ; 17 des 19 installés cités nulle part |
| Hook — heredoc de doc | `grimoire-hook --host claude --event PreToolUse` | `permissionDecision: deny` |
| Hook — même contenu via `Write` | idem | `permissionDecision: allow` |
| Hook — message de commit | idem | `permissionDecision: deny` |
| Hook contre l'auditeur | session Claude Code | le hook de la Forge a refusé **deux** de mes propres commandes d'audit, dont celle qui construisait la charge de test du hook |
| `fix --apply` | `grimoire standard fix . --apply` | `[OK] wrote mission-brief.md` puis `! generate_missing_artifact: artifact.missing (mission-brief.md)` |
| Code retour | `grimoire standard verify .` sans pipe | `exit 0` sur 5 avertissements, `exit 1` après suppression de `mission-brief.md` |
| Antériorité | `gh issue list --state open` sur `Grimoire-kit` | aucun des défauts n'est suivi ; 25 issues ouvertes, sans recoupement |

### Défauts que l'errata n'a pas vus

| Défaut | Mesure | Nature |
|---|---|---|
| `mem0-bridge.py` jamais déployé | 14 références, dont `agent-base.md:684` (socle chargé par tout agent) et l'activation de `memory-keeper` | Même classe que BUG-6, sept fois plus de sites d'appel. Le fichier existe (`data/framework/memory/mem0-bridge.py`, 42,8 Ko) et reste dans la wheel. |
| `maintenance.py` cité au mauvais étage | 8 références vers `_grimoire/_memory/maintenance.py` ; le fichier est déployé en `_grimoire/kit/memory/maintenance.py` | Même dérive de frontière que BUG-1 et BUG-5, mais sur la couche mémoire. |
| Artefacts mémoire jamais créés | `dependency-graph.md` 9 réf. — **ligne 33 de huit personas, leur étape d'activation** —, `oss-references.md` 6, `handoff-log.md` 5, `network-topology.md` 2, `knowledge-digest.md`, `agent-changelog.md` | Aucun gabarit dans le kit, aucune création par `init`. Huit agents d'infra commencent leur activation en chargeant un fichier absent. |

### Livrable

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Contre-expertise publiée | `https://claude.ai/code/artifact/0a46db92-020a-4a1e-b4c7-dcbfe017feb1` | session | 9 verdicts, 3 défauts supplémentaires, 1 réfutation confirmée, plan de correction par coût croissant |
| Gates de la tâche | `grimoire standard gate check --task-id r7-forge-kit-adoption --strict` | exécution | `OK evidence gates` |
| Standard du dépôt | `grimoire standard verify .` | exécution | `exit 0`, 0 erreur, 0 avertissement, profil governed |
| Établi rendu à son état | `grimoire cockpit remove repro-01` | exécution | projet de reproduction désenregistré |

### Livraison

| Action | Commande | Résultat |
|---|---|---|
| Branche publiée | `git push -u origin feat/entry-persona-autostart` | nouvelle branche sur `Grimoire-kit` |
| PR ouverte | `gh pr create` | [Grimoire-kit#233](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/233), préfixe `feat(hosts):` pour le release-drafter |
| Build local identifiable | `uv build --wheel` avec `__version__` mis à `3.34.2+entrypersona`, restauré aussitôt | la version installée ne peut pas se confondre avec la 3.34.2 de PyPI ; la branche reste propre |
| Venv de la Forge basculé | `uv pip install …/grimoire_kit-3.34.2+entrypersona-py3-none-any.whl` | `grimoire --version` → `3.34.2+entrypersona` |
| Injection en conditions réelles | `grimoire-hook --host claude --event SessionStart`, **sans `PYTHONPATH`** | le concierge est en tête d'`additionalContext` ; c'est exactement ce que reçoit une session Claude Code |
| Non-régression du standard | `grimoire standard verify .` | 21 artefacts, 0 erreur, 0 avertissement |
| Santé projet | `grimoire doctor` | 22/22 |

Retour en arrière : `uv pip install --reinstall grimoire-kit==3.34.2`. Un
`-U` ne suffit pas — une version locale `3.34.2+entrypersona` est considérée
plus récente que `3.34.2`.

### Effet de bord corrigé

L'arbitrage des doublons disait « le concierge du kit ne s'active pas ici ».
Il était vrai avant ce changement et faux après : les deux personas sont
maintenant chargées ensemble sous Claude Code, le master par l'import de
`CLAUDE.md`, le concierge par le hook.

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Arbitrage remis en accord avec le réel | `_grimoire-runtime/_config/agent-bridges.yaml` | — | les deux personas coexistent sous Claude Code ; le master SOG tranche en cas de désaccord ; sous Copilot rien ne change |
| Carte régénérée | `.github/copilot-instructions.md` | `scripts/agent-index.py` | 30 agents, 4 ponts |
| Garde de cohérence vert | — | `scripts/agent-index.py --check` | `[OK] carte à jour`, `exit=0` |

Les quatre fichiers modifiés dans la Forge ne sont pas committés : la
publication du côté atelier n'a pas été demandée.

## Correction des douze défauts — quatre lots sur le dépôt produit

Le travail est fait dans un worktree jetable créé depuis `origin/main`
(`scratchpad/kit-errata`, branches empilées), jamais dans `grimoire-kit/` :
le clone est partagé entre sessions et son arbre de travail est sale sur un
autre chantier. Un venv dédié installe le worktree en editable, pour valider
dans les conditions de la CI plutôt que contre la release publiée.

### Recensement préalable — « ce qui n'est pas branché ou mal branché »

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Installation maximale | 8 archétypes, `host sync` tous hôtes, `standard init --profile governed`, `hooks install` | session | 212 fichiers, base de comparaison |
| Livré vs atteignable | croisement `framework/` + `archetypes/` contre l'installation | script de recensement | 196 fichiers livrés dans la wheel, 79 atteignent le projet, **117 jamais** (1,76 Mo) |
| Promis mais non livré | croisement des non-déployés avec le contenu qui les nomme | script | 33 fichiers nommés par une persona, un workflow ou une DNA sans jamais être déployés |
| Jamais livré ni nommé | complément du précédent | script | 79 fichiers, 1,28 Mo — hors contrat, laissés dans la wheel |
| Faux positif écarté | 21 gabarits `agentic-standard/templates/` | `standard verify` | déploiement opt-in par pattern, et `verify` signale le manque : conforme à la conception |

### Lots livrés

| Lot | Commit | Défauts fermés | Preuve |
|---|---|---|---|
| 1 — `fix(scaffold)` chemins livrés | `78275154` | BUG-1, BUG-5, BUG-6, N-1, N-2, N-3, N-4, N-5, N-6 | 44 fichiers, 99 → 55 références mortes ; 5658 tests verts |
| 2 — `fix(scaffold)` rendu à l'installation | `e90e2d9a` | BUG-2, BUG-3, BUG-4, BUG-8, BUG-9 | carte générée depuis le roster réel ; 5670 tests verts |
| 3 — `fix(policy)` lire l'argv | `cd6876b7` | BUG-7 | 18 cas dans les deux sens ; 5688 tests verts |
| 4 — `feat(doctor)` deux checks | `df72323f` | récidive | `20/22` sur l'installation d'origine, `22/22` après correction ; 5701 tests verts |

### Défauts trouvés par le recensement, absents de l'errata

| Défaut | Mesure | Lot |
|---|---|---|
| N-4 — `.pre-commit-config.yaml` généré vers `framework/hooks/*.sh` | chemin que seul un clone du kit possède ; les quatre hooks échouaient au premier `pre-commit run` | 1 |
| N-5 — `docs/sdk-guide.md` documente quatre propriétés de `PathResolver` | `grimoire_dir`, `config_dir`, `memory_dir`, `agents_dir` n'existent pas ; seuls `root`, `resolve_path`, `resolve_template` existent | 1 |
| N-6 — `_framework_hooks_dir()` rate l'install editable | résolvait les données du paquet à la main au lieu de passer par `framework_path()` | 1 |

### Verdict final, rejoué sur une installation neuve

| Action | Commande | Résultat |
|---|---|---|
| Seize assertions sur les douze défauts | script de vérdict contre un `init` produit par les quatre lots | **16/16 OK** |
| Les deux checks contre l'installation 3.34.2 d'origine | `grimoire doctor .` | `20/22` — 58 chemins morts et les neuf agents fantômes nommés |
| Les deux checks après correction | `grimoire doctor .` | `22/22`, « tous les chemins du kit cités se résolvent », « carte de routage cohérente » |
| Suite complète | `pytest tests/` | 5701 passés, 9 ignorés, 0 échec |
| Lint | `ruff check src/ tests/` | 4 erreurs, toutes préexistantes sur `origin/main`, aucune dans les fichiers touchés |
| Le défaut se reproduit contre l'auteur | session | le hook `PreToolUse` a refusé **quatre** commandes d'écriture de ce correctif, dont celles écrivant le test qui le prouve |

### Restes assumés

| Reste | Motif |
|---|---|
| `mem0-bridge.py seed` et `export-md` | sans équivalent dans le CLI `grimoire memory` ; documenté comme nécessitant un clone du dépôt du kit |
| 79 fichiers livrés dans la wheel et nommés par personne | hors contrat de livraison ; les déployer ajouterait 1,28 Mo par projet sans site d'appel |
| `grimoire-init.sh` cite l'ancien étage | installeur shell historique, encore référencé par la CI et les gabarits d'issue ; sa dépréciation est un chantier distinct |

### PR ouvertes sur le dépôt produit

| PR | Base | Lot | État |
|---|---|---|---|
| [#234](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/234) | `main` | chemins livrés | mergeable |
| [#235](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/235) | #234 | rendu à l'installation | mergeable |
| [#236](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/236) | #235 | politique de hook | mergeable |
| [#237](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/237) | #236 | checks du doctor | mergeable |

Empilées : chacune se relit seule, et l'ordre de merge est #234 → #235 → #236 → #237.

### Merge — les cinq PR sont sur `main`

| PR | Commit sur `main` | Lot |
|---|---|---|
| [#234](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/234) | `27372b5b` | chemins livrés |
| [#238](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/238) | `6a32c2e1` | archive déterministe (défaut découvert en passant la CI réelle) |
| [#235](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/235) | `6d8adf00` | rendu à l'installation |
| [#236](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/236) | `97384723` | politique de hook |
| [#237](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/237) | `816f6b7c` | checks du doctor |

### Ce que le merge a révélé

| Constat | Preuve | Suite |
|---|---|---|
| `ci-sdk.yml` et `ci-validate.yml` déclarent `pull_request: branches: [main]` | Les PR empilées n'ont vu que 6 checks sur 25 : la vraie suite ne tournait pas | Chaque PR a été rebasée sur `main` avant merge, pour passer la CI réelle |
| `test_publish_is_deterministic` rougit au hasard | `tarfile.open(..., "w:gz")` grave MTIME dans l'en-tête gzip ; corps tar identique, en-têtes différents, mesuré octet par octet | PR #238, deux gardes déterministes |
| Ratchet de taille sur `cli/app.py` | `grew 2798 -> 2819 lines — extract instead of appending` | Rendu des checks déplacé dans `core/integrity.integrity_checks()` ; `app.py` à 2787 lignes |
| `Framework Tools Tests (windows-latest)` rouge sur les cinq PR | 16 tests de `test_init_commands.py` shellant vers `grimoire-init.sh` | Issue [#231](https://github.com/Guilhem-Bonnet/Grimoire-kit/issues/231), préexistante et ouverte ; aucune PR ne touche ce script |

### Vérification finale, contre `main` et non contre une branche

| Action | Commande | Résultat |
|---|---|---|
| Les douze défauts rejoués | verdict sur un `init` produit depuis `origin/main` à `816f6b7c` | **16/16 OK** |
| Doctor sur ce projet | `grimoire doctor .` | `20/20`, les deux nouveaux checks verts |
| Suite complète | `pytest tests/` randomisation activée | 5703 passés, 9 ignorés, 0 échec |

## Release 3.35.0 → 3.35.2, et adoption par la Forge

### Trois gardes de release, découverts en publiant

| Garde | Ce qu'il a refusé | Suite |
|---|---|---|
| `gen-kit-hashes.py --check` | **53 fichiers** introduits par la 3.35.0 avaient une empreinte inconnue : `grimoire migrate` les aurait lus comme des customisations utilisateur et gelés hors de toute mise à jour ultérieure | Catalogue régénéré, 759 empreintes |
| `check-changelog-release.py` | `[Unreleased]` accumulait les entrées de plusieurs PR mergées depuis la 3.34.2 | Basculées dans la section publiée |
| tag ↔ `version.txt` | — | Vérifié avant chaque tag |

### Versions publiées

| Version | Commit | Contenu | PyPI |
|---|---|---|---|
| 3.35.0 | `973a6bb6` | les cinq correctifs de l'errata + le reliquat « à venir » | publiée |
| 3.35.1 | `27d1468a` | régression : les checks comptaient les dépôts imbriqués | publiée |
| 3.35.2 | `bcf79261` | régression : les checks lisaient les archives comme vivantes | publiée |

Les deux régressions ont été trouvées **en mettant la Forge à jour**, pas par un
test : c'est la consommation réelle qui les a exposées, et chacune était le même
mode de panne — du bruit qui rend un check ignorable, ce que le module se donnait
pourtant pour règle d'éviter.

### Adoption par la Forge

| Action | Commande | Résultat |
|---|---|---|
| Venv sur la release | `uv pip install grimoire-kit==3.35.2` | `grimoire-kit 3.35.2` |
| BUG-7 rejoué sur la Forge | trois charges `PreToolUse` de l'errata | `allow`, `allow`, `allow` — la doc passe |
| Le garde bloque toujours | trois charges d'action réelle | `deny`, `deny`, `deny` |
| Étage kit régénéré | `grimoire up` | 40 artefacts mis à jour, 15 fichiers projet préservés |
| Surfaces hôtes reprojetées | `grimoire host sync` | 4 écrits, 20 inchangés |
| Chemins morts de la Forge | `grimoire doctor .` | 395 → 21 |
| Carte de routage | idem | cohérente avec le manifeste |

### Reste — dette de la Forge, pas du kit

Les 21 références restantes viennent des fichiers propres à la Forge : 15 dans
`_grimoire-runtime-output/` (artefacts de planification BMM historiques), 2 dans
`.github/` (surfaces écrites à la main), 2 dans `web/` (données de site
générées), 2 dans `_grimoire/` (`mem0-bridge.py` et un `workflow-graph.yaml`
résiduels d'une installation antérieure, que `up` préserve au lieu de supprimer).
Aucune n'est un défaut du kit ; leur nettoyage vise l'atelier et demande un
accord explicite.

## Solde de la dette — la cause, puis les résidus

### Le décompte qui a changé la réparation

Sur les 21 signalements restants après la 3.35.2, **17 n'auraient pas dû être
émis** :

| Origine | Nombre | Nature |
|---|---|---|
| Audits datés sous `_grimoire-runtime-output/` | 15 | Documents qui **rapportent** les références cassées de leur époque — les corriger falsifierait le compte rendu |
| Journal de site généré | 2 | `"text": "Dossier config manquant : _grimoire/_config"`, alerte de mars 2026 |
| Hook écrit à la main | 1 | `grimoire-kit/_grimoire/…` dont seule la fin était matchée |
| Compétence maison | 1 | Chemin de stockage créé au premier usage |
| **Réels** | **2** | Deux fichiers résiduels d'une installation antérieure |

Corriger les documents historiques aurait été la mauvaise réparation. La cause
était le parcours : trois versions de suite avaient retiré une source de bruit
(dépôts imbriqués, archives, artefacts du projet) sans nommer ce qu'elles
avaient en commun.

### Deux versions de plus, côté kit

| Version | PR | Correction |
|---|---|---|
| 3.35.3 | [#243](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/243) | La vérification lit la surface de livraison, pas tout le projet ; regex ancrée à gauche |
| 3.35.4 | [#244](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/244) | C'est le marqueur `grimoire:managed` qui dit ce que le kit a écrit, plus une liste de répertoires |

Piège rencontré et testé : un premier ancrage rejetant tout slash précédent
éliminait aussi `{project-root}/_grimoire/…`, la forme qu'emploient presque
toutes les personas — 6 détections au lieu de 56. Un test l'exige désormais.

| Cible | chemins morts | fantômes |
|---|---|---|
| Installation 3.34.2 défectueuse | 56 | 9 |
| Installation saine | **0** | **0** |
| Forge, avant solde | 2 | 0 |

Le zéro sur une installation saine est le chiffre qui compte : une vérification
qui parle sur un projet correct apprend à être ignorée.

### Résidus retirés de la Forge

| Fichier | Motif |
|---|---|
| `_grimoire/kit/workflows/workflow-graph.yaml` | Superseded par `examples/workflow-graph.yaml` ; `up` ne supprime pas |
| `_grimoire/kit/workflows/workflow-status.md` | Idem |
| `_grimoire/kit/workflows/github-cc-check.yml.tpl` | Idem, zéro référence |
| `_grimoire/_memory/mem0-bridge.py` | Plus déployé depuis 3.35.0, aucun appelant |
| `_grimoire/_memory/memory_seed.py` | Plus déployé, seulement auto-référencé |

Deux formulations périmées remises à jour : `contradiction-log.md` citait
`mem0-bridge` au lieu du CLI, et `bm-registry.md` déclarait BM-22 « `mem0-bridge.py`
présent ».

| Action | Commande | Résultat |
|---|---|---|
| Venv sur la release | `uv pip install grimoire-kit==3.35.4` | `grimoire-kit 3.35.4` |
| Solde | `git rm` × 5 + 2 corrections de texte | — |
| État final | `grimoire doctor .` | **24/24**, « tous les chemins du kit cités se résolvent », carte cohérente |
| Standard | `grimoire standard verify .` | 0 erreur, 0 avertissement |

## Audit inter-sessions (2026-09-04)

Demande de Guilhem : orchestrer les sessions Claude du projet, auditer, planifier.
Aucune modification de code ; lecture seule sur les deux dépôts.

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Sessions interrogées | `ListAgents` + `SendMessage` | session | 22 visibles, 9 sessions Forge actives ont répondu, 3 sessions PC hors périmètre, 1 cloud sans réponse possible |
| Rapports recoupés | `gh pr view`, `gh issue view`, `git tag`, `pip index versions` | session | 6 rapports sur 9 périmés (PR #164, #226, #230, #232 fusionnées ; 3.33.0 absorbée par 3.34.0) |
| Santé de l'atelier | `grimoire doctor`, `standard verify .`, `gate check --task-id r7-forge-kit-adoption --strict`, `host status` | session | 24/24, 0 erreur 0 avertissement, `OK evidence gates`, Claude Code à jour |
| Protection de `main` du kit | `gh api repos/.../branches/main/protection` | session | 404 « Branch not protected » |
| Dépendance des hooks Forge | `grep` sur `.github/hooks/scripts/` | session | 11 scripts référencent `grimoire-kit/framework/tools/*.py`, untracked dans le clone partagé ; non déployés par 3.37.0 (`_grimoire/kit/tools/` = 5 autres outils) |
| Worktrees du kit | `git worktree list` + `rev-list --left-right` | session | 8 worktrees, 7 sur des branches fusionnées, fermées ou absorbées |
| Livrable | artefact « Audit Grimoire du 4 septembre » | session | état vérifié, constats transverses, plan en trois blocs, cinq décisions attendues |

## Exécution du plan du 2026-09-04 — bloc « cette semaine »

Guilhem a validé les cinq décisions et ajouté deux demandes : la Forge intègre
tout ce que le kit projette, et une revue de direction artistique de
`grimoire serve` / cockpit entre au plan.

### Dépôt produit

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| #245 en conflit avec `main` | `gh pr view 245` | session | `CONFLICTING`, 2 commits / 16 en retard ; conflits sur `CHANGELOG.md` et la table de préfixes de `agentic_standard.py` |
| Rebase dans un worktree jetable | `scratchpad/kit-245`, branche `fix/standard-check-registry-p03-p04` | `git rebase origin/main` | 2 conflits résolus ; 17 checks `claims.*` et `surfaces.*` arrivés avec 3.37.0 déclarés au registre (le test `test_every_emitted_check_is_registered` les nommait) |
| Tests | venv dédié au worktree | `pytest tests/test_agentic_standard.py tests/unit/test_runtime.py tests/unit/test_gascity_converter.py` puis `pytest tests/unit --maxfail=5` | 124 passés, puis suite unitaire verte |
| Types et lint | idem | `mypy --strict registry.py adapter_base.py` ; `ruff check` | 0 erreur mypy ; 2 erreurs ruff préexistantes sur `runtime/recipes.py`, hors périmètre |
| PR de remplacement | [Grimoire-kit#261](https://github.com/Guilhem-Bonnet/Grimoire-kit/pull/261) | `gh pr create` | ouverte ; #245 fermée avec renvoi |
| `main` protégée | `gh api PUT branches/main/protection` | session | 12 contextes requis, `enforce_admins`, push forcé et suppression interdits ; relu par `GET` |
| Stash étranger consommé puis restauré | dépôt `Grimoire-kit` | `git stash pop` par erreur (worktree propre, stash d'une autre session), puis `git fsck --unreachable` et `git stash store 7296e9f7` | `stash@{0}` « WIP on (no branch): 300ecd38 … lot P0.2 » de retour, contenu intact |
| Écriture accidentelle dans le clone partagé | `grimoire-kit/` | cwd du shell resté dans le clone : `grimoire up` et `host sync --host copilot` y ont écrit | 35 fichiers créés supprimés par liste explicite ; `.gitignore` et `copilot-instructions.md` réécrits depuis l'index ; les fichiers de `_grimoire/kit/` régénérés à la 3.37.0 sont laissés (état non suivi, antérieur à l'incident) |

### Atelier

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Gardes des hooks versionnées | `.github/hooks/lib/` (9 fichiers, 320 Ko) | copie depuis les untracked du clone ; `resolve_rules_file` préfère le YAML voisin | 15 scripts, `tasks.json` et les 40 `controlFiles` du registre repointés ; plus aucune référence à `grimoire-kit/framework/tools/` ni à `grimoire-kit/.venv` dans `.github/hooks/scripts/` |
| Même verdict qu'avant | payloads `PreToolUse` | script d'origine (python du clone) et script vendorisé (python de la Forge, 3.14) | `permissionDecision: ask` identiques sur un `rm -rf` de `_grimoire-runtime/_memory` ; `{}` sur `ls` |
| Le gateway refuse de nouveau | `grimoire-hook-gateway.sh` | après `hook-safety-gate.py promote` | même décision `ask` à travers le gateway ; `{}` tant que les hooks étaient `modified` |
| Kit régénéré sur la Forge | `_grimoire/kit/` | `grimoire up` | 18 artefacts mis à jour, 18 fichiers projet préservés |
| Copilot projeté | `.github/` | `grimoire host sync --host copilot` | 22 fichiers : 6 agents du kit, 3 skills, 5 prompts, 7 hooks, README ; `art-director.agent.md` maison préservé |
| Deux hooks maison renommés | `.github/hooks/forge-session-start.json`, `forge-pre-compact.json` | session | la projection écrasait les deux fichiers homonymes ; les hooks du gateway vivent sous `forge-*`, ceux du kit sous `grimoire-*` ; les deux piles tournent sous Copilot |
| Le smoke accepte le binaire du kit | `.github/hooks/lib/hook-safety-gate.py` | `is_kit_host_hook()` | `grimoire-hook --host copilot --event …` reconnu comme passerelle gouvernée ; les 7 manifestes du kit ne sont plus « bypass du gateway » |
| Registre re-promu | `hook-safety-registry.json` | `promote`, puis `set-mode canary grimoire-doc-drift`, `set-mode shadow grimoire-pattern-consumption` | `total=15 enforced=13 canary=1 shadow=1`, smoke `ok` |
| Board soldé | `_grimoire/standard/task-board.yaml` | session | `r7` → `accepted` (gates vertes) ; `r8`, `r9`, `r10`, `c1` à `c5` → `archived` avec motif (gate `missing task_envelope` sur les huit) |
| Carte des agents | `.github/copilot-instructions.md` | `scripts/agent-index.py --check` | à jour, 30 agents, 4 ponts |
| Santé | session | `grimoire doctor`, `standard verify .`, `gate check --task-id r7-forge-kit-adoption --strict` | 24/24 ; 0 erreur 0 avertissement ; `OK evidence gates` |

### Tâche par défaut du kit rendue évaluable

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Le gate de sortie retombait sur `bootstrap` | `grimoire-hook --event Stop` | `active_task_id()` : `GRIMOIRE_TASK_ID`, sinon la tâche `in_progress` unique, sinon `bootstrap` | r7 passée en `accepted` : plus aucune tâche en cours, le hook évaluait `bootstrap`, absente du board (`gate.task_not_on_board`) |
| Entrée au board et compagnons | `task-board.yaml`, `_grimoire-output/context/bootstrap/`, `_grimoire-output/decisions/bootstrap/` | session | `bootstrap` en `accepted` ; context-bundle et decision-trace en rétro-qualification datée du 2026-09-04, sans contenu d'époque inventé |
| Vérification | session | `gate check --task-id bootstrap --strict`, `standard verify .`, hook `Stop` simulé | `OK evidence gates` ; 0 erreur 0 avertissement ; `{}` (clôture autorisée) |
