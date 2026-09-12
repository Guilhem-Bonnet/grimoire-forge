# Rejeu réel du dispatch en cascade dans `flow run` — épic #307, lot 3 (#311)

Date : 2026-09-11. Plafond de dépense respecté : 2,5692223 USD réels sur 5,00 USD alloués (aucun appel hors `flow run --executor dispatch`).

## Protocole

- Dépôt jetable initialisé via `grimoire init . -a web-app -b local -y` (kit 3.44.2, celui consommé par la Forge), en dehors de la Forge et du clone `grimoire-kit`, sous le scratchpad.
- Code réel écrit à la main (pas par un modèle) : `src/tasklib/` (`models.py`, `store.py`) + `tests/test_store.py`, 16 tests verts au départ (commit `117befc`, "baseline: tasklib service + tests (16 passing)").
- Registre `_grimoire/standard/llm-provider-registry.yaml` copié depuis `/mnt/Travail/Projets/Dev/Grimoire-Forge/_grimoire/standard/`, un seul changement : ajout de `--output-format json` à l'invocation `anthropic` (le gabarit d'origine n'active pas le JSON, donc `_extract_cost_usd` n'aurait jamais rien lu — sans ce changement, aucun coût n'est mesurable du tout).
- Blueprint réel `tasklib-hardening.blueprint.json`, 5 nodes, chaînés en série, classes dérivées automatiquement par `grimoire.missions.verifiability.classify()` depuis le texte d'`acceptance` (vérifié avant tout appel, coût nul) :
  - `n1-age-method` — V0 (« la suite de tests passe »)
  - `n2-oldest-open` — V0 (« la suite de tests passe », « ruff ne signale aucune erreur de lint »)
  - `n3-refactor-review` — V1 (« revue humaine avant fusion »)
  - `n4-schema-import` — V0 (« les données respectent le schéma pydantic », « la suite de tests passe »)
  - `n5-ambiguous-cleanup` — V2 (« le code est propre et bien structuré », volontairement ambigu)
- Exécution : `GRIMOIRE_NO_COCKPIT=1 grimoire flow run tasklib-hardening.blueprint.json --executor dispatch --timeout 300`, deux fois de suite (run 001 puis, après `git checkout --` des fichiers source pour revenir à la baseline, run 002), pour tester la stabilité.
- Suivi du coût en temps réel par lecture de `_grimoire-runtime-output/ledger/events.jsonl` (événements `task.dispatched`, champ `cost_usd`), reporté après chaque nœud dans `/tmp/.../scratchpad/cost-ledger.txt`.

## Résultat par nœud

| Nœud | Classe | Palier plancher | Run 1 : paliers / verdict / coût | Run 2 : paliers / verdict / coût | Escalade (run1/run2) |
|---|---|---|---|---|---|
| n1-age-method | V0 | cheap | cheap → green — 0,359319 $ | cheap → green — 0,132371 $ | non / non |
| n2-oldest-open | V0 | cheap | cheap(red) → mid(green) — 0,445350 $ | cheap(red) → mid(green) — 0,545254 $ | **oui / oui** |
| n3-refactor-review | V1 | mid | mid → green (à relire) — 0,207293 $ | mid → green (à relire) — 0,207595 $ | non / non |
| n4-schema-import | V0 | cheap | cheap → green — 0,248140 $ | cheap → green — 0,423902 $ | non / non |
| n5-ambiguous-cleanup | V2 | — | refusé avant tout appel — 0 $ | refusé avant tout appel — 0 $ | n/a |

Totaux : run 1 = 1,260101 $ (log CLI : « coût total connu : 1,2601012 — escalades : 1 ») ; run 2 = 1,309121 $ (« coût total connu : 1,3091211 — escalades : 1 »). Grand total mesuré : **2,5692223 $**.

## Comparaison au lot 0 (issue #308, verdict figé : haiku 20/20, 0 % d'escalade, 0,1226 $/tâche complétée ; opus seul 0,5692 $/tâche ; cascade à 21,5 % du coût opus)

- **Nœuds complétés** : 8/8 nœuds délégables (V0+V1) verts sur les deux runs (les 2 occurrences de n5, V2, sont un refus correct avant tout appel, pas un échec).
- **Taux d'escalade** : 25 % des nœuds complétés par run (1 nœud sur 4, `n2-oldest-open`), et 100 % reproductible sur les deux runs — contre 0 % dans le lot 0. La cause observée n'est pas une incapacité de haiku sur le fond (le code produit est correct une fois testé, cf. plus bas) mais un défaut de conformité au format de sortie exigé (`{"pins": {...}}`) sur la première tentative — un mode d'échec que le lot 0, à tâche unique et sans double contrainte (coder + écrire l'enveloppe JSON), ne pouvait pas observer.
- **Coût par nœud complété** : 2,5692223 / 8 = **0,321153 $**, soit 2,62× le chiffre haiku du lot 0 (0,1226 $) et 56,4 % du coût opus seul (0,5692 $) — très au-dessus des 21,5 % mesurés par le lot 0 pour sa propre cascade. Le lot 0 mesurait des tâches isolées avec un `--check` de fond (domaine) ; ici, le gate réel est plus faible (voir ci-dessous) et coûte quand même plus cher, parce que chaque appel est une session agentique complète (lecture de fichiers, édition réelle, exécution d'outils) et non un aller-retour de complétion simple.
- **Incertitudes déclarées** : 1/8 dispatches verts (12,5 %) a rendu un bloc `grimoire-uncertainties` non vide (`n4-schema-import`, run 2 : doute légitime sur la sémantique all-or-nothing de l'import). 0 % des escalades observées sont liées à une incertitude déclarée — le canal d'incertitude (#328) est purement informatif ici, il n'entre pas dans la décision rouge/vert de la cascade.
- **Classe de relisibilité (#327)** : `review_optional` sur les 8 dispatches verts — aucun des fichiers touchés (`models.py`, `store.py`, `importer.py`) ne correspond aux surfaces sensibles par défaut (`*/cli/*`, `*/mcp/*`, `*schema*`, etc. — `importer.py` ne contient pas la sous-chaîne « schema » malgré son rôle). Aucune donnée sur `review_required` : angle mort de ce rejeu (voir « non mesuré » plus bas), pas un défaut du kit.

## Un écart significatif entre la classe V0 et ce que le gate vérifie réellement

Fait vérifié directement, pas déduit : le nœud `n4-schema-import` (V0, acceptance = « la suite de tests passe » + « schéma pydantic ») a été marqué **vert** et a fermé la cascade au palier `cheap`, alors que la vraie suite `pytest` du dépôt **ne s'exécutait même pas** (le nouveau fichier `tests/test_importer.py` importait `pydantic`, jamais installé dans l'environnement de test — `ModuleNotFoundError` bloquant toute la collecte, y compris les 16 tests préexistants). Après installation manuelle de `pydantic`, les 27 tests passent (le code produit est correct) — mais ce n'est pas ce que le gate a vérifié pour rendre son verdict vert et facturer 0,2481 $ / 0,4239 $.

Ce n'est pas un bug caché : `flows/dispatch_executor.py` le documente explicitement (« pour seule vérification, la conformité du fichier que l'ouvrier délégué doit écrire au contrat de sortie du node ») et la PR #336 elle-même le dit (« le check est la validation du fichier de résultat contre les pins du node, la même que `flow resume` »). La classe de vérifiabilité (V0 = « un programme rend seul le verdict : test, lint... ») décrit un vocabulaire d'acceptance, mais **le gate effectif de `flow run --executor dispatch` ne l'exécute jamais** — il vérifie seulement la forme `{"pins": {...}}`. C'est un choix documenté, pas un défaut à corriger par une issue ; mais c'est précisément ce que le lot 0 ne mesurait pas, puisque ses `--check` de tâche isolée pointaient vers de vrais tests.

## Ce qui n'a pas pu être mesuré

- **`review_required`** : aucun fichier touché par ce rejeu ne matche les surfaces sensibles par défaut — la classe de relisibilité #327 n'a donc été observée qu'en `review_optional`.
- **Escalade jusqu'à `strong` (opus)** : aucun nœud n'a épuisé la chaîne complète cheap→mid→strong sur les deux runs ; le comportement au palier `strong` (coût, taux de succès) reste hors de cette mesure.
- **Ajustement du palier de départ par historique (#312/lot 4)** : chaque nœud n'a que 1 à 2 observations dans le ledger de ce dépôt jetable (`start_tier_reason: "moins de 5 observations (1) : palier plancher de la classe"`), donc la règle de relèvement/abaissement du palier de départ ne s'est jamais déclenchée.
- **`grimoire task dispatch` avec un vrai `--check` domaine** (par opposition à `flow run --executor dispatch`) : non rejoué faute de budget restant justifié — l'écart documenté ci-dessus rend cette comparaison probablement plus instructive qu'un second rejeu du même mécanisme.

## Conclusion (trois lignes)

Le routage tient sur un flow réel pour ce qu'il promet explicitement : classification zéro-coût correcte, refus V2 déterministe et gratuit, escalade V0 reproductible à l'identique sur deux rejeux. Il escalade sur la conformité du format de sortie exigé par le moteur de flow, pas sur la difficulté du travail réel — un mode de défaillance invisible au niveau tâche isolée du lot 0. Le lot 0 ne mesurait ni le coût d'une session agentique complète (édition réelle de fichiers, plusieurs outils) ni l'écart entre la classe de vérifiabilité affichée (V0 = « les tests passent ») et le gate structurel réellement exécuté par `flow run --executor dispatch` — écart qui, ici, a laissé fermer un nœud dont la vraie suite de tests ne s'exécutait pas.
