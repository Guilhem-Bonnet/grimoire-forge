# Rejeu réel du dispatch en cascade avec gate d'acceptance exécutable — épic #307, #433 + #444

Date : 2026-09-12. Plafond respecté : **1,5506053 USD réels sur 5,00 USD alloués** (nouvelle campagne, distincte des 2,5692223 USD du 2026-09-11). Aucun nouveau nœud entamé au-delà de 4,00 USD (jamais approché : le run 1 s'est arrêté à 0,7438220 USD, le run 2 à 0,8067833 USD supplémentaires).

## Kit utilisé

`origin/main` de Grimoire-kit n'est publié qu'en partie (3.45.0 contient #433, pas #444) : worktree jetable `git worktree add .../kit-measure2 origin/main` sur `68d3eff9` (« feat(dispatch): coût par tâche résolue et pass^k... (#442) (#444) »), roue construite dans un venv jetable (`pip install -e <worktree>`, maturin 1.15.0 pour les crates Rust ; `grimoire_dispatch_core`/`grimoire_traces_core` non compilées — chemins optionnels, jamais utilisées par le gate d'acceptance ni par l'agrégation pass^k selon le corps de la PR #444, vérifié par l'exécution ci-dessous qui fonctionne sans elles). Confirmé avant tout appel : `src/grimoire/flows/blueprint_loader.py` porte bien `_ACCEPTANCE_STRUCTURED_KEYS` (#433) et `grimoire dispatch stats` existe (#444).

## Protocole

- Même dépôt jetable que le 2026-09-11 (`scratchpad/flow-dispatch-measure/`), remis à la baseline (`git checkout --` sur les fichiers trackés, suppression des artefacts non trackés du rejeu précédent) avant chaque run — `pytest` repasse à 16 tests verts.
- **Correctif d'environnement (pas du kit)** : `pydantic`, `pytest`, `ruff` installés dans le `.venv-test` du projet *avant* tout dispatch — c'est précisément ce qui manquait le 2026-09-11 et avait laissé `n4` fermer vert sans que la suite ne collecte.
- **Blueprint réécrit** (`tasklib-hardening.blueprint.json`) : chaque nœud V0 (`n1`, `n2`, `n4`) garde son acceptance textuelle d'origine et gagne une entrée structurée `{"run": "pytest -q", "expect_exit": 0}` (+ `{"run": "ruff check src/tasklib/store.py", "expect_exit": 0}` sur `n2`). `n3` (V1, « revue humaine ») et `n5` (V2, ambigu) inchangés. Classification vérifiée à coût nul avant tout appel : V0/V0/V1/V0/V2, identique à avant, `verifiability_warning = None` sur les trois V0 (donc bien fermables par la cascade, pas rétrogradés en V1 par prudence).
- Invocation : `PATH="<projet>/.venv-test/bin:$PATH" GRIMOIRE_NO_COCKPIT=1 grimoire flow run tasklib-hardening.blueprint.json --executor dispatch --timeout 300`, exécutée depuis la racine du kit construit — le `PATH` préfixé fait résoudre `pytest`/`ruff` vers les binaires du projet par le `subprocess.run(shell=True)` de `_run_checks` (confirmé en lisant `missions/dispatch.py`, qui hérite l'environnement de l'appelant).
- Deux runs complets, remise à la baseline entre les deux. Aucun nœud n'est ressorti « inexécutable » : pas de réenchaînement correctif nécessaire.
- Suivi de coût en direct via `_grimoire-output/traces/traces.jsonl` (tags `dispatch.outcome`) et `_grimoire-runtime-output/ledger/events.jsonl` (`task.dispatched`, champ `cost_usd`), reporté après chaque run dans `cost-ledger-2026-09-12.txt`, puis recoupé avec `grimoire dispatch stats --json`.

## Résultat par nœud et par run

| Nœud | Classe | Palier | Run 1 : verdict / acceptance / coût / durée | Run 2 : verdict / acceptance / coût / durée | Escalade (run1/run2) |
|---|---|---|---|---|---|
| n1-age-method | V0 | cheap (haiku) | green / **exécutée** / 0,1469002 $ / 36,2 s | green / **exécutée** / 0,1018815 $ / 47,7 s | non / non |
| n2-oldest-open | V0 | cheap (haiku) | green / **exécutée** / 0,1744607 $ / 74,0 s | green / **exécutée** / 0,1809988 $ / 75,9 s | **non / non** |
| n3-refactor-review | V1 | mid (sonnet) | green (à relire) / jugée / 0,2098088 $ / 33,9 s | green (à relire) / jugée / 0,2266672 $ / 36,8 s | non / non |
| n4-schema-import | V0 | cheap (haiku) | green / **exécutée** / 0,2126523 $ / 108,0 s | green / **exécutée** / 0,2972358 $ / 152,9 s | non / non |
| n5-ambiguous-cleanup | V2 | — | refusé avant tout appel — 0 $ | refusé avant tout appel — 0 $ | n/a |

Totaux : run 1 = 0,7438220 $ (0 escalade) ; run 2 = 0,8067833 $ (0 escalade). **Grand total mesuré : 1,5506053 $.**

`grimoire dispatch stats --project-root <projet> --json` (recoupement) :

```json
{
  "overall": {"total": 8, "resolved": 8, "inexecutable": 0, "escalated": 0,
              "total_cost_usd": 1.550605, "cost_per_resolved_task_usd": 0.1938256625,
              "escalation_rate": 0.0, "inexecutable_share": 0.0},
  "by_class": {
    "V0": {"total": 6, "resolved": 6, "total_cost_usd": 1.114129, "cost_per_resolved_task_usd": 0.18568821666666666, "escalation_rate": 0.0},
    "V1": {"total": 2, "resolved": 2, "total_cost_usd": 0.436476, "cost_per_resolved_task_usd": 0.218238, "escalation_rate": 0.0}
  },
  "by_provider": {"anthropic": {"total": 8, "resolved": 8, "total_cost_usd": 1.550605, "cost_per_resolved_task_usd": 0.1938256625}},
  "pass_k_observations": 4, "pass_k_fully_green": 4, "pass_k_rate": 1.0
}
```

`1.550605` (dispatch stats) contre `1.5506053` (ledger tenu à la main) — recoupement exact (arrondi à 6 décimales). Aucune divergence.

`grimoire standard verify .` / `grimoire standard audit .` : `dispatch.cost_slo` n'émet **aucune ligne** dans les deux (silence = conforme, même convention que tous les autres `_verify_*` du module). Vérifié directement en appelant `_verify_dispatch_cost_slo()` sur ce projet : **0 check ajouté** — confirmé que le contrôle a bien tourné (lu `TraceLedger.dispatch_outcome_stats()`, comparé aux seuils par défaut documentés `max_cost_per_resolved_task_usd=2.0`, `min_pass_k_rate=0.8`, `min_resolved_observations=5`, `min_pass_k_observations=3`) et que les deux métriques (0,1938 $ < 2,0 $ ; pass^k 100 % ≥ 80 %) sont dans l'enveloppe, avec assez de données (8 ≥ 5 résolus, 4 ≥ 3 séries rejouées) pour être jugées plutôt qu'``info``.

## Ce que le faux vert du 2026-09-11 cachait — réponse directe

`n4-schema-import` passe **réellement** au palier `cheap` (haiku), sur les deux runs. Preuve directe extraite de `_grimoire-runtime-output/ledger/events.jsonl` (`task.dispatched`, champ `checks[].output_excerpt`, jamais du texte de prompt) :

```
CHECK: pytest -q ok=True exit=0
EXCERPT: ..............................                                           [100%]
30 passed in 0.08s
```

(31 passed au run 2 — un test de plus écrit par le worker). Vérifié une troisième fois, indépendamment du gate, en relançant `pytest` moi-même après chaque run : 30 puis 31 tests verts, `pydantic` bien importé. Le gate #433 exécute désormais la vraie commande déclarée et non plus seulement l'enveloppe JSON — le point exact que #428/#433 corrige.

## Escalade du nœud n2 — ne s'est pas reproduite

Le 2026-09-11, `n2-oldest-open` escaladait cheap→mid sur les deux runs (100 % reproductible), pour un défaut de conformité au format d'enveloppe JSON, pas une incapacité sur le fond. Aujourd'hui, **0 escalade sur `n2` dans les deux runs** — ni sur aucun autre nœud. Ce n'est pas un changement de comportement du kit (le mécanisme d'escalade n'a pas été touché par #433/#444) : c'est une variance du worker (haiku) sur la conformité de l'enveloppe, cohérente avec l'hypothèse déjà posée le 2026-09-11 (« un mode d'échec que le lot 0 ne pouvait pas observer », pas un défaut de fond). Aucune conclusion de stabilité à tirer d'un échantillon de 2+2 runs sur ce point précis — juste : le défaut d'enveloppe n'est pas systématique.

## pass^k observé

4 séries rejouées (`n1`, `n2`, `n3`, `n4`, chacune via `replay_key=tasklib-hardening:<node>` sur les runs 003/004), **toutes entièrement vertes → pass^k = 100 %** (`pass_k_observations=4`, `pass_k_fully_green=4`). `n5` n'entre jamais dans le calcul (refusé avant tout appel, aucun `dispatch.outcome` écrit — vérifié : 0 événement pour `n5` dans `traces.jsonl`, conforme à la doctrine « pas d'événement pour un refus avant tout appel »).

## Comparaison à trois colonnes

| | Lot 0 (#308, issue figée) | Rejeu 2026-09-11 (#311, faux vert) | Rejeu 2026-09-12 (#433+#444) |
|---|---|---|---|
| Coût / tâche résolue | 0,1226 $ | 0,321153 $ (2,62×) | **0,1938257 $ (1,58×)** |
| % du coût opus seul | 21,5 % | 56,4 % | **34,05 %** (0,19383 / 0,5692) |
| Taux d'escalade | 0 % | 25 % (n2, ×2 reproductible) | **0 %** |
| Acceptance V0 réellement exécutée | n/a (tâche isolée, `--check` réel) | **non** — enveloppe seule, faux vert sur n4 | **oui** — commande réelle, verdict vérifié indépendamment |
| pass^k | non mesuré (outillage absent) | non mesuré (outillage absent) | **100 % (4/4 séries)** |
| Comptabilité continue (`dispatch stats`) | n/a | n/a | **oui, recoupée à l'identique** |

## Ce qui n'a pas pu être mesuré

- **`review_required`** : toujours aucun fichier touché ne matche les surfaces sensibles par défaut — `review_optional` uniquement, comme le 2026-09-11.
- **Escalade jusqu'à `strong` (opus)** : toujours aucun nœud n'a épuisé cheap→mid→strong sur les 4 runs cumulés (2026-09-11 + 2026-09-12).
- **`dispatch.cost_slo` en `WARN`/`FAIL`** : nos chiffres réels sont trop bons pour déclencher le contrôle — son comportement de dépassement (coût > SLO, ou pass^k < seuil, avec/sans `enforce: true`) reste non observé en conditions réelles, seulement vérifié par lecture de code.
- **Acceptance `{"path_exists": ...}` et `{"test": ...}`** : seule la forme `{"run": ...}` a été mesurée en conditions réelles (choix délibéré pour éviter la dépendance à l'interpréteur du kit — voir note kit ci-dessous) ; les deux autres formes restent vérifiées uniquement par lecture de code.

## Défaut de kit trouvé (hors périmètre #433/#444, sans rapport avec l'acceptance)

`run_id`/`WFI-*` tronque silencieusement l'identifiant du blueprint : `runtime/kernel.py:224`, `slug = recipe_id.replace(".", "-")[-16:]` — les **16 derniers caractères seulement**. Pour `tasklib-hardening` (17 caractères), le premier caractère (`t`) disparaît sans avertissement ni troncature visible (pas de `…`, pas de hash) : tous les runs de cette mesure et de celle du 2026-09-11 s'appellent `WFI-asklib-hardening-00N`, jamais `WFI-tasklib-hardening-00N` — vérifié sur les deux campagnes, deux versions du kit (3.44.2 et `68d3eff9`), donc reproductible et indépendant de #433/#444. Risque réel : collision silencieuse entre deux blueprints dont les 16 derniers caractères coïncident, et confusion de lecture (j'ai moi-même dû vérifier que ce n'était pas une faute de frappe dans mon propre blueprint avant de retrouver la ligne en cause). Un problème dédié a été ouvert (voir livrables) — pas de PR, conformément au périmètre de cette mesure.

## Conclusion (trois lignes)

Le gate d'acceptance de #433 ferme désormais un nœud V0 sur un verdict réellement exécuté (`pytest -q`, sortie lue et recoupée trois fois : trace du kit, relance manuelle, `dispatch stats`) — le faux vert du 2026-09-11 sur `n4` ne se reproduit pas, et le coût par tâche résolue retombe de 2,62× à 1,58× le lot 0, avec pass^k à 100 % sur 4 séries mesurées pour la première fois. La comptabilité continue de #444 recoupe le ledger tenu à la main à l'identique et le gate `dispatch.cost_slo` tourne réellement (0 check ajouté, vérifié par appel direct, pas seulement par silence du CLI) sans jamais bloquer par défaut. Rien dans cette mesure ne contredit la doctrine de #433/#444 ; le seul défaut trouvé (troncature silencieuse de `run_id`) est antérieur et sans lien avec l'acceptance structurée.
