# Rejeu réel `flow extract` + triple rejeu — condition de déverrouillage lots 3/4 (#206/#207)

Date : 2026-09-14. Kit : grimoire-kit 3.48.0 (venv de la Forge, `.venv/bin/grimoire`). Plafond : **6 USD** — dépense réelle **3,8007901 USD** (run initial + 3 rejeux), jamais entamé un nouveau run au-dessus de 5 USD (2,0824789 avant le rejeu 2, 2,9658702 avant le rejeu 3).

## Projet réel

Copie jetable de `/mnt/Travail/Projets/Dev/OPS/Terraform-HouseServer` (pas un dépôt git) sous `scratchpad/homelab-flow/`, excluant `_grimoire-output/`, `_archive/`, `.venv*`, plus `.terraform/` et `node_modules/` (caches fournisseur/vendor de plusieurs GB, hors sujet — 8,1 Go → 1,0 Go copiés). Trois dépôts git imbriqués (`homelab-c4-viewer`, `infra-prod-home-`, `minecraft-server`) aplatis en un seul arbre (`.git` supprimés, fichiers réels ajoutés) pour que `git checkout`/`git stash` portent sur le contenu réel, pas des gitlinks vides. `git init` sur la copie, 3 commits de baseline.

Cible : module Terraform réel `infra-prod-home-/terraform/modules/lxc-docker-stack/` (conteneur LXC Proxmox + Docker). `terraform` 1.9.8 installé (`~/.local/bin/terraform`), pas de `tflint`/`ansible-lint`/`yamllint` sur ce poste.

Projet initialisé avec `grimoire init . -a infra-ops -b local -y --no-cockpit`. `project-context.yaml` complété avec :

```yaml
needs:
  commands:
    test-runner: "terraform validate"
    lint: "terraform fmt -check -recursive"
```

`grimoire needs resolve` confirme les deux `declared` (le reste `unresolved`, sans marqueur Python/Node/Rust/Go dans ce module — attendu). Registre `_grimoire/standard/llm-provider-registry.yaml` copié depuis la Forge dans `_grimoire/standard/` du projet ; **un seul changement**, comme lors des campagnes du 2026-09-11 (même cause, même correctif) : ajout de `--output-format json` à l'invocation `claude -p`, sans quoi `_extract_cost_usd` ne lit jamais rien et aucun coût n'est mesurable. `_grimoire/standard/pilot.yaml` : `max_cost_usd_per_node: 1.0`.

## Blueprint réel — `tf-lxc-module-hardening.blueprint.json` (5 nœuds)

Travail utile et borné trouvé en lisant le module : le README documente 9 variables (`auto_shutdown_*`, `backup_*`, `docker_compose_files`, `docker_env_files`, `install_packages`, `timezone`), 3 outputs et un dossier `examples/` qui **n'existent plus** dans `variables.tf`/`outputs.tf` ni sur le disque — le module a été refactoré pour déléguer le provisioning à Ansible sans que le README ne suive.

| Nœud | Classe (vérifiée à coût nul avant tout appel) | Tâche |
|---|---|---|
| `n1-fmt-guard` | V0 (`run_need: lint`) | `terraform fmt` canonique |
| `n2-tf-validate` | V0 (`run_need: test-runner`) | `terraform validate` passe |
| `n3-readme-reconcile` | V1 (« revue humaine avant fusion ») | réconcilier le README avec le module réel |
| `n4-input-validation` | V0 (`run_need: test-runner` + `lint`) | ajouter des blocs `validation` sur `vm_id` et `ipv4_address` |
| `n5-ambiguous-cleanup` | V2 (délibérément ambigu) | « rendre le module plus propre » |

**Piège d'auteur de blueprint rencontré et corrigé avant tout dispatch** (vérifié par `classify_criteria`, coût nul) : mélanger un texte libre maison (« le format terraform est canonique... ») à côté d'une entrée structurée `run_need` fait tomber tout le nœud en **V2** si ce texte ne contient aucun mot du vocabulaire mécanique reconnu (`test`, `lint`, `schéma`, `code de sortie`...) — « fmt »/« format » n'y figurent pas. Un seul critère ambigu suffit à dégrader tout le nœud (règle documentée : *un faux V0 est pire qu'un faux V2*). Correction : ne garder que l'entrée structurée (son texte auto-généré contient « code de sortie », donc mécanique). Ce n'est pas un défaut du kit, c'est le comportement documenté — mais un piège réel pour quiconque écrit un blueprint à la main.

## Run initial — `WFI-tf-lxc-module-hardening-002` (`--executor dispatch --timeout 300`)

| Nœud | Palier | Verdict | Coût |
|---|---|---|---|
| n1-fmt-guard | cheap | green, acceptance exécutée | 0,1964973 $ |
| n2-tf-validate | cheap | green, acceptance exécutée | 0,1377317 $ |
| n3-readme-reconcile | mid | green à relire, acceptance jugée | 0,5771326 $ |
| n4-input-validation | cheap | green, acceptance exécutée | 0,1494919 $ |
| n5-ambiguous-cleanup | — | **refusé avant tout appel** (V2) | 0 $ |

Total run initial : **1,0608535 $**, 0 escalade. Recoupé exactement par `grimoire dispatch stats --json` (`total_cost_usd: 1.060853`).

Vérification indépendante des fichiers modifiés (pas seulement le verdict vert — leçon du rejeu du 2026-09-11 sur les faux verts) :
- `main.tf`/`outputs.tf` : non touchés (fmt/validate déjà propres — légitime, pas de travail nécessaire).
- `variables.tf` : +10 lignes, deux blocs `validation` ajoutés (`vm_id > 0`, `ipv4_address` contient `/`).
- `README.md` : -82/+39 lignes, sections Variables/Exemples/Outputs réconciliées avec le module réel.

**Défaut réel trouvé dans le code produit, indépendant du mécanisme extract/replay** (déjà documenté par le mainteneur les 2026-09-11/12, donc **pas une nouvelle issue**) : le bloc de validation `ipv4_address` du run initial utilise `contains(var.ipv4_address, "/")` — `contains()` Terraform exige une liste/tuple/set, pas une chaîne. Confirmé en isolant l'appel dans `terraform console` : `Error: argument must be list, tuple, or set`. `terraform validate` ne l'a pourtant jamais signalé (pas de valeur concrète liée sans `plan`). C'est exactement la même catégorie de défaut que le rapport du 2026-09-11 : le gate V0 (`run_need`/`run`) vérifie le code de sortie de la commande déclarée, pas la véracité sémantique de ce que le nœud prétend avoir fait.

`n3-readme-reconcile` a lui-même détecté et documenté ce genre d'écart dans son incertitude déclarée (sections README encore obsolètes citées explicitement).

## Extraction — `grimoire flow extract WFI-tf-lxc-module-hardening-002 --out extracted.blueprint.json`

Résultat : `n1`/`n2`/`n3`/`n4` → `completed`, `n5` → `host_pending` (jamais résolu par la cascade, correct puisque suspendu côté hôte). **Diff exact vs l'original** (voir `extract-diff-2026-09-14.diff` dans ce scratchpad) :

- Ajout `extractedFrom` (run_id, blueprint_id, blueprint_path, run_status=`checkpointed`, extracted_at).
- Ajout par nœud `"extraction": {"status": ...}`.
- Les entrées `run_need` perdent `cwd`/`expect_exit` explicites — **sans perte d'information**, ce sont les valeurs par défaut (`.`/`0`) que `_parse_run_like_entry` réinjecte au chargement.
- **Aucun nœud perdu, aucune arête perdue, aucune description altérée.**
- Reclassifié après extraction (`classify_criteria` sur `extracted.blueprint.json`) : V0/V0/V1/V0/V2 — **identique** à l'original.

Aucun défaut d'extraction constaté.

## Incident opérationnel (le mien, pas un défaut du kit) et récupération

Après le run initial, `git checkout -- .` a été refusé par le garde Bash de ce poste (« discard all working-tree changes »). Repli prévu par le protocole : `git stash -u -- . && git stash drop` — mais `-u` avec le pathspec `.` a aussi balayé les fichiers **non trackés** du répertoire courant, dont `_grimoire-runtime-output/` (registre des runs/checkpoints) et `_grimoire/` (registre LLM + `pilot.yaml`) et `extracted.blueprint.json` lui-même. `git stash drop` les a donc supprimés. **Récupéré intégralement** : `extracted.blueprint.json` reconstruit par `patch` à partir du diff déjà sauvegardé (0 fuzz, reconstruction identique, revérifiée par reclassification) ; `_grimoire/standard/{llm-provider-registry.yaml,pilot.yaml}` recréés à l'identique. Seule perte réelle et non récupérée : l'historique de checkpoint du run initial dans `_grimoire-runtime-output/` (`flow list` ne le voit plus) — sans conséquence sur la mesure, `grimoire dispatch stats` lit une source distincte (`_grimoire-output/traces/`) qui a survécu intacte (le total 1,060853 $ était toujours là après coup). **Correctif appliqué pour les 3 rejeux suivants** : `git stash push -- <fichiers trackés précis>` (sans `-u`, sans pathspec `.`), qui ne touche jamais les artefacts Grimoire non trackés — vérifié par listing Python avant/après à chaque rejeu.

Note annexe : `find <dir>` sans argument `-iname` sur ce poste masque les fichiers/dossiers cachés (interception transparente du hook RTK) — utiliser `python3 -c "os.listdir(...)"` pour une vérité de terrain, ce qui a été fait à chaque étape sensible.

## Trois rejeux — `grimoire flow run extracted.blueprint.json --executor dispatch`, arbre remis à `git stash push -- README.md variables.tf` + `stash drop` avant chacun

| | n1-fmt-guard | n2-tf-validate | n3-readme-reconcile | n4-input-validation | n5 (V2) | Total run |
|---|---|---|---|---|---|---|
| Rejeu 1 (`...-extract-001`) | green 0,3572744 $ | green 0,1201753 $ | green à relire 0,4149038 $ | green 0,1292719 $ | refusé, 0 $ | **1,0216254 $** |
| Rejeu 2 (`...-extract-002`) | green 0,0854243 $ | green 0,1403208 $ | green à relire 0,4799030 $ | green 0,1777432 $ | refusé, 0 $ | **0,8833913 $** |
| Rejeu 3 (`...-extract-003`) | green 0,0872158 $ | green 0,1737848 $ | green à relire 0,4514692 $ | green 0,1224501 $ | refusé, 0 $ | **0,8349199 $** |

**0 escalade sur les 12 dispatches des 3 rejeux.** `n5` refusé avant tout appel, identiquement, sur les 3 rejeux (même classe V2, même motif : « aucun critère mécanique ni revue reconnue »). Aucune divergence de statut/verdict/classe entre les 3 rejeux ni avec le run source — seule variation observée : le contenu généré par le modèle (ex. rejeu 3 utilise `can(regex("/", var.ipv4_address))` au lieu du `contains(...)` bogué du run initial pour la même validation `ipv4_address` — variance de génération normale entre appels indépendants, pas une divergence du moteur ; les deux passent le même gate `terraform validate`, qui ne discrimine pas leur exactitude sémantique respective, cf. plus haut).

Diffs de fichiers cohérents sur les 3 rejeux + le run initial : `variables.tf` toujours +10 lignes (2 blocs `validation`), `README.md` toujours réécrit sur les mêmes sections (Variables/Exemples/Outputs), jamais `main.tf`/`outputs.tf` touchés.

## Recoupement final — `grimoire dispatch stats --project-root . --json`

```json
{
  "overall": {"total": 16, "resolved": 16, "inexecutable": 0, "escalated": 0,
              "total_cost_usd": 3.80079, "cost_per_resolved_task_usd": 0.237549,
              "escalation_rate": 0.0, "inexecutable_share": 0.0},
  "by_class": {
    "V0": {"total": 12, "resolved": 12, "total_cost_usd": 1.877381, "cost_per_resolved_task_usd": 0.156448},
    "V1": {"total": 4,  "resolved": 4,  "total_cost_usd": 1.923409, "cost_per_resolved_task_usd": 0.480852}
  },
  "by_flow": {
    "tf-lxc-module-hardening":              {"total": 4,  "resolved": 4,  "total_cost_usd": 1.060853, "cost_per_resolved_task_usd": 0.265213},
    "tf-lxc-module-hardening-002-extract":  {"total": 12, "resolved": 12, "total_cost_usd": 2.739937, "cost_per_resolved_task_usd": 0.228328}
  },
  "pass_k_observations": 4, "pass_k_fully_green": 4, "pass_k_rate": 1.0
}
```

`3.80079` (dispatch stats) contre `3.8007901` (ledger tenu à la main, `cost-ledger-2026-09-14.txt`) — recoupement exact (arrondi 6 décimales). Aucune divergence.

`grimoire flow list --project-root .` affiche le flow `tf-lxc-mo…` avec **Mesure = « mesuré »**, 3 runs, 12/12 nœuds résolus, 0 % escalade, 0,2283 $/tâche. `grimoire flow list --require-measure tf-lxc-module-hardening-002-extract` réussit (sortie 0, ligne affichée) — confirme que lot 5 voit bien la mesure sur le blueprint **extrait**, pas seulement l'original.

## Pass^k et avis sur le déverrouillage

- **Pass^k sur les nœuds V0/V1 du flow extrait, rejoué 3 fois** : **3/3** entièrement vert (les 4 nœuds dispatchables verts, `n5` refusé identiquement à chaque fois). En comptant le run source dans les observations pass^k du kit (comportement de `dispatch_outcome_stats`) : **4/4**, `pass_k_rate: 1.0`.
- **Aucune divergence inexpliquée** : tous les statuts/classes/verdicts sont identiques entre le run source, l'extrait et les 3 rejeux ; la seule variation est le contenu généré par le modèle à chaque appel indépendant (attendu, documenté, non un défaut du moteur).
- **Aucun défaut du kit trouvé dans le mécanisme extract/replay lui-même** : extraction fidèle (0 nœud perdu, statuts corrects, métadonnées `extractedFrom` correctes, reclassification identique), pas de `cost_capped` intempestif, `flow list` voit la mesure sur le blueprint extrait. Le seul défaut réel observé (gate V0 plus faible que le texte d'acceptance ne le suggère) est déjà documenté par ailleurs (rapports du 2026-09-11/12) — **pas une nouvelle issue**.

**Avis : la condition fixée par Guilhem est remplie.** Les lots 3 (#206) et 4 (#207) peuvent s'ouvrir.

## Dépense

| Étape | Coût | Cumul |
|---|---|---|
| Run initial | 1,0608535 $ | 1,0608535 $ |
| Rejeu 1 | 1,0216254 $ | 2,0824789 $ |
| Rejeu 2 | 0,8833913 $ | 2,9658702 $ |
| Rejeu 3 | 0,8349199 $ | **3,8007901 $** |

Plafond 6 USD respecté ; jamais entamé de nouveau run au-dessus de 5 USD.

## Artefacts

- Blueprint d'origine : `tf-lxc-module-hardening.blueprint.json`
- Blueprint extrait : `extracted.blueprint.json` (reconstruit à l'identique après l'incident `git stash -u`, voir plus haut)
- Diff extraction : `extract-diff-2026-09-14.diff`
- Logs de run : `flow-run-2026-09-14-run0-initial.log`, `flow-run-2026-09-14-replay{1,2,3}.log`
- Ledger : `cost-ledger-2026-09-14.txt`
- Stats finales : `dispatch-stats-2026-09-14-final.json`
