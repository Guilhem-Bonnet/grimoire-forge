# Analyse `kit-gov` Go/JavaScript — lot H (issue #582)

> Analyse en lecture seule, aucune modification de dépôt. Source : `_scratch/bench-h2/workspace/state/results.jsonl` (240 lignes)
> et les transcriptions `_scratch/bench-h2/workspace/tasks/<langue>__<tâche>/kit-gov/run{0,1,2}.stream.jsonl` — 15 runs Go
> (5 tâches × 3), 15 runs JavaScript (5 tâches × 3), 5 runs Python (un run par tâche, `run0`) pour comparaison.
> Méthode : chaque run est un fichier JSONL en streaming ; un « tour » = un identifiant de message assistant unique
> (`message.id`), qui regroupe ses blocs `thinking`/`text`/`tool_use` — ce comptage colle à ±1 près au `num_turns` du
> harnais. Chaque tour est classé par priorité sur le texte de ses appels d'outils : `gate_check` (contient
> `gate check`) > `gate_other` (`gate run-tests`/`gate verify`) > `toolchain_search` (recherche de binaire :
> `command -v`, `which`, `find /`, `rpm -q`, listage de répertoires candidats) > `manual_test_run` (exécution directe
> de `go test`/`go build`/`go vet`/`gofmt`/`npm test`/`npx jest`/`cargo test`/`pytest`) > `envelope_io` (lecture ou
> écriture de `task-envelope.md`, `evidence-pack.md`, `acceptance-record.md`, `claim-ledger.md`, par `Write`/`Edit`
> ou par `Bash`/`sed`/heredoc/`python`) > `real_work` (le reste : lecture de l'énoncé, écriture de la solution).
> Scripts d'analyse et JSONL intermédiaires dans le scratchpad de session, non conservés dans le dépôt.

## Résumé exécutif

- **Go** : 100 % des 15 runs échouent le premier `gate check --strict` sur **exactement** le même motif :
  `acceptance.test_run_failed`, `'go test ./...' -> rouge (exit 127)`. Cause prouvée au niveau code (pas une
  hypothèse) : le harnais télécharge un Go portable dans `workspace/tools/go/go/bin`
  (`ensure_go_toolchain`, `scripts/bench/three_arms.py:577`) mais ne le câble **que** dans son propre sous-processus
  de notation (`run_hidden_tests`, ligne 1859) — jamais dans l'environnement du sous-processus qui lance l'agent
  (lignes 699/982/1038/1897 : seul le dossier de `grimoire` est préfixé au `PATH` hérité). Le `PATH` que voit l'agent
  contient même une entrée `/usr/local/go/bin` **qui n'existe pas sur la machine** — un résidu de config qui ne mène
  nulle part. Médiane : 4 tours/run passés à chercher un binaire déjà présent sur disque.
- **JavaScript** : **0 des 15 runs `kit-gov`** n'atteint jamais `OK evidence gates` (recherche exhaustive de la
  chaîne dans les 15 transcriptions — zéro occurrence). Cause : les 5 dépôts de tâche JS ne contiennent **aucun**
  fichier `*.spec.js` (masquage des tests, comportement voulu par `prepare_task_repo(include_tests=False)` — et
  vérifié correct : Python masque ses `_test.py` de la même façon). `npm test` (`jest ./*`) sort donc systématiquement
  en `exit 1` avec « No tests found ». Les dépendances npm, elles, sont bien installées (`test_deps_install_ok=True`
  sur les 15 runs, `jest` s'exécute) — ce n'est pas un problème d'outillage comme pour Go, c'est un plafond
  structurel du gate : rien que l'agent puisse faire légitimement ne le fait passer au vert.
- **Conséquence commune aux deux langues** : le verdict du gate est **déconnecté** du verdict réel de la tâche
  (tests cachés du harnais). Sur Go, 4 runs terminent `reached_ok=False` mais réussissent quand même au sens du
  harnais, et 2 runs terminent `reached_ok=True` mais échouent. Sur JS, les 14 runs réussis (`success=True`) n'ont
  jamais vu le gate passer au vert. Le gate, en l'état, mesure autre chose que ce que mesure le succès réel.
- **Aucun** des quatre artefacts de gouvernance (`task-envelope.md`, `evidence-pack.md`, `acceptance-record.md`,
  `claim-ledger.md`) n'apparaît dans un `[x]` d'échec sur les 30 runs Go+JS analysés — recherche exhaustive de tous
  les appels `gate check` de tous les runs. Le seul check qui échoue jamais, sur les deux langues, est
  `acceptance.test_run_failed`. Les tours `envelope_io` observés (médiane 0 sur Go, 1 sur JS) sont des initiatives
  spontanées de l'agent (il documente sa situation), pas des corrections exigées par le gate.
- Le mécanisme « ne pas relancer les tests si l'empreinte de l'arbre est identique » **existe déjà**
  (`tree_fingerprint.compute_tree_fingerprint`, `gate_test_run._recorded_run_is_fresh_and_green`) mais ne
  court-circuite que les runs **verts et frais** ; un run rouge est toujours ré-exécuté à chaque `gate check --strict`,
  même si rien n'a changé depuis (cas Go PATH et JS sans suite : rouge identique reproduit 2 à 6 fois par run).

## 1. Tours par catégorie (médiane par langue)

| Catégorie | Go (n=15) | JavaScript (n=15) | Python (n=5, comparaison) |
|---|---|---|---|
| **Tours totaux** | 16 | 17 | 7 |
| Recherche/installation toolchain | **4** | 0 | 0 |
| Exécution manuelle des tests projet (`go test/build/vet`, `npm test/jest`, `pytest`) | 2 | 1 | 0 |
| `gate check --strict` (appels) | 3 | 3 | 1 |
| `gate run-tests`/`verify` résiduels | 0 | 0 | 0 |
| Lecture/édition envelope·pack·acceptance·claim-ledger | 0 | 1 | 1 |
| Travail réel (lecture énoncé, écriture solution) | 6 | 8 | 4 |
| Tours texte seul (pas d'appel d'outil) | 2 | 2 | 1 |
| **Gate calls jusqu'au premier OK** | 2 (11/15 l'atteignent) | **jamais (0/15)** | 1 (5/5) |

Lecture : sur Go, la recherche de toolchain (4 tours) pèse presque autant que le travail réel utile pour la
gouvernance du gate (`gate_check` + `toolchain_search` + `manual_test_run` = 9 tours sur 16, **56 %**). Sur JS,
il n'y a pas de recherche de toolchain (node/npm/jest sont sur le `PATH` réel de la machine) mais le gate ne
converge jamais : les 3 appels `gate check --strict` médians sont 3 échecs identiques, pas 3 tentatives qui
progressent.

### Détail par tâche (médiane des 3 runs)

| Tâche | Tours | gate_check | toolchain_search | manual_test_run | envelope_io | real_work | Atteint OK |
|---|---|---|---|---|---|---|---|
| go/bottle-song | 17 | 3 | 4 | 1 | 0 | 3 | 1/3 |
| go/error-handling | 18 | 4 | 3 | 3 | 1 | 5 | 3/3 |
| go/palindrome-products | 15 | 3 | 3 | 2 | 0 | 6 | 3/3 |
| go/pov | 16 | 3 | 4 | 2 | 0 | 6 | 2/3 |
| go/simple-linked-list | 18 | 4 | 4 | 1 | 1 | 7 | 2/3 |
| js/affine-cipher | 21 | 4 | 0 | 1 | 2 | 10 | 0/3 |
| js/go-counting | 12 | 3 | 0 | 1 | 0 | 7 | 0/3 |
| js/list-ops | 15 | 3 | 0 | 1 | 1 | 9 | 0/3 |
| js/queen-attack | 17 | 3 | 0 | 0 | 1 | 8 | 0/3 |
| js/transpose | 17 | 3 | 0 | 1 | 1 | 8 | 0/3 |

## 2. Premier `gate check --strict` — ce qu'il rapporte et ce que l'agent fait après

### Go — identique sur les 15/15 runs

```
FAIL evidence gates for task go__<tâche> (state: in_progress)
  tests exécutés : 'go test ./...' -> rouge (exit 127), enregistré dans .../test-run.json
  [x] acceptance.test_run_failed (.../test-run.json): Le dernier run de test enregistré est rouge
      ('go test ./...', code de sortie 127) sur l'arbre courant : corrigez les tests puis relancez
      `grimoire standard gate run-tests --task-id go__<tâche>` (ou `gate check --strict`, qui le relance).
```

Action suivante systématique (15/15) : une commande `find` / `command -v` / `ls -d` sur des chemins candidats
(`/usr/local/go`, `/usr/lib/golang`, `/opt/go`, `~/go`, `~/sdk`, `find / -maxdepth N -name go`). Exemple
(`go__bottle-song/run0`, tour 5) : `ls -d /usr/lib/golang /usr/local/go /opt/go ~/go ~/sdk/* 2>/dev/null; find /
-maxdepth 5 -name "go" -type f -perm -u+x 2>/dev/null | grep -E "bin/go$" | head`. Le binaire est parfois trouvé
dans `workspace/tools/go/go/bin` (le toolchain du harnais, alors utilisé via un `export PATH=...` manuel — 11/15
runs), parfois dans un cache de module Go d'un tout autre projet (`/home/guilhem/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.23.0.../bin`,
une fuite de l'environnement réel de la machine, pas un artefact du banc), et 4/15 runs n'y arrivent jamais dans le
budget de tours alloué.

**Seul check en échec, sur les 15 runs, sur tous les appels de gate confondus** : `acceptance.test_run_failed`.
Aucune mention de `task-envelope`, `claim-ledger`, `acceptance-record` ou `evidence.pending_gate` en échec.

### JavaScript — identique sur les 15/15 runs

```
FAIL evidence gates for task javascript__<tâche> (state: in_progress)
  tests exécutés : 'npm test' -> rouge (exit 1), enregistré dans .../test-run.json
  [x] acceptance.test_run_failed (.../test-run.json): Le dernier run de test enregistré est rouge
      ('npm test', code de sortie 1) sur l'arbre courant : corrigez les tests puis relancez
      `grimoire standard gate run-tests --task-id javascript__<tâche>` (ou `gate check --strict`, qui le relance).
```

Action suivante typique : `npx jest ./*` en direct, qui répond `No tests found, exiting with code 1` +
`testMatch: **/__tests__/**/*.[jt]s?(x), **/?(*.)+(spec|test).[tj]s?(x) - 0 matches` (`javascript__affine-cipher/run0`,
tour 7). Le diagnostic est net (rouge = pas de suite, pas un bug de code), mais **aucune action légitime ne le
corrige** : la consigne interdit d'écrire soi-même le fichier de test caché, et `--passWithNoTests` triche le
gate sans rien prouver. Citation exacte du dernier tour de `javascript__affine-cipher/run0` :

> « Si tu veux le gate au vert, il faut lever une des deux contraintes : m'autoriser à écrire le fichier de test
> (`affine-cipher.spec.js`, je peux le dériver du harness existant), ou accepter `--passWithNoTests` dans
> `package.json` — ce second choix rendrait le gate vert sans rien prouver, je ne le recommande pas. »

**Seul check en échec, sur les 15 runs, sur tous les appels confondus** : `acceptance.test_run_failed`. Même
constat que Go — aucun échec d'envelope/claim-ledger/acceptance-record. La liste des checks « à rendre
auto-satisfaits pour une tâche V0 » est donc courte et ne concerne **pas** les 4 artefacts cités dans la demande :
c'est `acceptance.test_run_failed` lui-même qu'il faut rendre non bloquant (ou correctement vert) quand la cause
est environnementale (Go) ou structurelle (JS, tests cachés sans suite locale).

## 3. Go — PATH et coût de la recherche de toolchain

- **Commande résolue** : `go test ./...` (enregistrée dans `test-run.json`, confirmée par `resolve_need("test-runner", ...)`).
- **`go` est-il sur le `PATH` de l'agent ?** Non, sur 15/15 runs. Le `PATH` observé (identique sur tous les runs
  échantillonnés) : `.../kit-bench-h/.venv/bin:.../Grimoire-Forge/.venv/bin:/home/guilhem/.local/bin:.../nvm/versions/node/v22.22.2/bin:
  /usr/local/bin:/home/guilhem/bin:/home/guilhem/.dotnet:/home/guilhem/.cargo/bin:/usr/bin:/usr/local/sbin:/usr/sbin:
  /var/lib/snapd/snap/bin:/usr/local/go/bin` — c'est le `PATH` réel de la machine de développement (nvm, cargo,
  dotnet inclus), pas un environnement isolé pour le banc. Vérifié sur l'hôte au moment de l'analyse :
  `/usr/local/go/bin` **n'existe pas** (`ls: cannot access '/usr/local/go/bin': No such file or directory`) — c'est
  une entrée `PATH` morte, pas une piste que l'agent pourrait exploiter.
- **Premier `go test ./...` (via le gate)** : `exit 127`, `go: command not found` (implicite — c'est le code shell
  standard « commande introuvable »).
- **Tours perdus** : médiane 4 tours/run rien que pour la recherche du binaire (`toolchain_search`), plus souvent
  1 à 3 tours de plus pour l'`export PATH=...`/`GOROOT=...` manuel une fois trouvé et pour re-router le
  `gate check` avec ce `PATH`. Sur `go__simple-linked-list/run0` (29 tours, le run le plus long du lot), 10 appels
  `gate check` ont été nécessaires, entrecoupés de recherches de toolchain répétées à chaque nouvelle session de
  sous-shell.
- **Preuve code** (pas une extrapolation) : `ensure_go_toolchain` (`scripts/bench/three_arms.py:577`) télécharge un
  Go portable dans `workspace/tools/go/go/bin` si aucun `go` n'est déjà sur le `PATH` du harnais. Sa seule
  utilisation (`grep -n go_bin`) est `run_hidden_tests(..., go_bin=go_bin)` à la ligne 1859 — la vérification finale
  du harnais, jamais l'environnement de lancement de l'agent. Les 4 points où l'environnement du sous-processus
  agent est construit (lignes ~699, ~982, ~1038, ~1897) ne préfixent au `PATH` hérité que
  `Path(grimoire_bin).parent` (le dossier du binaire `grimoire`) — jamais `workspace/tools/go/go/bin`.

## 4. JavaScript — dépendances, résolution de test, empreinte du gate

- **Commande résolue** : `npm test` → `package.json` déclare `"test": "jest ./*"` (le glob `./*` est développé par
  le shell **avant** d'atteindre `jest`, donc `jest` reçoit tous les fichiers/dossiers de premier niveau du dépôt
  comme motifs — dont aucun ne matche `testMatch` faute de fichier `.spec.js`/`.test.js`).
- **Dépendances du harnais (#603) présentes au premier tour ?** Oui — `test_deps_install_ok=True` sur les 15/15
  runs `kit-gov` JS dans `results.jsonl`, et `npx jest ./*` s'exécute réellement (pas de `command not found`) :
  la sortie est un rapport `jest` complet (« 12 files checked », `testPathIgnorePatterns: /node_modules/ - 12
  matches »), preuve que `node_modules/jest` était bien installé pendant la session. `node_modules/` a depuis été
  supprimé du disque par le nettoyage post-run du harnais (`_BUILD_ARTIFACT_DIRS`), ce qui n'apparaît qu'après coup.
- **Premier `npm test`** : `exit 1`, « No tests found, exiting with code 1 » — confirmé sur les 5/5 tâches JS que
  le dépôt de tâche ne contient **aucun** fichier `*.spec.js` au démarrage (`ls *.spec.js` échoue avec
  `no matches found` dans les 5 premiers tours de chaque tâche). Ce n'est pas « les tests du repo échouent parce
  que la solution n'est pas écrite » (hypothèse de la demande) : il n'y a tout simplement pas de fichier de test à
  faire échouer. C'est un masquage volontaire et cohérent avec Python (`prepare_task_repo(include_tests=False)`,
  qui exclut les fichiers déclarés dans `.meta/config.json["files"]["test"]` — vérifié correct pour les 5 tâches JS
  et les 5 tâches Python échantillonnées).
- **`gate check --strict` relance-t-il les tests à chaque appel ?** Oui, dans ce cas précis, et c'est le
  comportement voulu du code actuel : `gate_test_run.ensure_fresh_test_run` ne saute l'exécution
  (`_recorded_run_is_fresh_and_green`) que si le dernier run enregistré était **vert** ET l'empreinte d'arbre
  identique (`tree_fingerprint.compute_tree_fingerprint`). Un run **rouge** est toujours ré-exécuté, quelle que soit
  l'empreinte — donc chaque `gate check --strict` sur une tâche JS relance `npm test`, qui échoue à l'identique.
  L'agent le constate lui-même dans `javascript__affine-cipher/run0` : « Relancer `gate run-tests` reproduira le
  même résultat à l'identique — je l'ai déjà fait deux fois. »
- **Conséquence sur le succès réel** : `results.jsonl` donne `success=True` sur 14/15 runs `kit-gov` JS (le seul
  échec, `javascript/transpose` run 0, n'est pas lié au gate) — la solution est jugée correcte par la suite cachée
  du harnais alors que le gate visible par l'agent est resté rouge sur les 15/15 runs. Le gate et le jugement de
  succès mesurent deux choses différentes.

## 5. Recommandations chiffrées pour un lot I

### Harnais (`scripts/bench/three_arms.py`)

1. **Injecter `workspace/tools/go/go/bin` dans le `PATH` du sous-processus agent**, aux 4 points où l'environnement
   `kit`/`kit-gov`/`ecc`/`nu` est construit (préfixer comme `Path(grimoire_bin).parent`, avec le résultat
   d'`ensure_go_toolchain`, pas seulement le passer à `run_hidden_tests`). Effet attendu, mesuré sur ce lot :
   suppression des ~4 tours/run de `toolchain_search` (médiane) sur les 15 runs Go, soit environ 25 % des tours
   Go actuels (4/16) — de quoi ramener la médiane Go vers 10-12 tours, sous la cible ≤ 9-13,5 (1,5× nu = 6×1,5=9).
   Coût nul (le téléchargement du toolchain a déjà lieu ; il ne reste qu'à le pointer au bon endroit).
2. **Retirer l'entrée morte `/usr/local/go/bin` du `PATH` hérité pour les runs de banc**, ou au minimum ne pas
   laisser croire à l'agent qu'un Go système existe : elle ne mène nulle part sur cette machine et coûte une
   itération de `find /` supplémentaire à chaque run qui la prend pour une piste sérieuse.
3. **Corriger l'exclusion de `_BUILD_ARTIFACT_DIRS`** si l'objectif est de rejouer fidèlement l'état de fin de
   session pour audit : `node_modules/` disparaît après coup, ce qui a bien failli fausser le diagnostic Q4
   ci-dessus (il faut relire les transcriptions, pas l'état disque final, pour juger de ce que l'agent a vu).

### Produit (comportement du gate, profil V0/starter)

4. **Rendre `acceptance.test_run_failed` non bloquant (ou vert par défaut) quand la cause du rouge est
   `no_test_command`/absence de suite locale sur une tâche à tests cachés**, plutôt que de le laisser échouer à
   l'identique à chaque appel. Sur ce lot, ce changement seul retire l'unique check qui échoue jamais sur Go et
   JS (confirmé exhaustif : 0 échec d'envelope/claim-ledger/acceptance-record sur les 30 runs analysés — **ne pas
   toucher ces 4 artefacts, ils ne sont le problème nulle part dans ce jeu de données**). Dosage V0 concret : pas
   de gate de test bloquant pour une tâche dont le seul `test_files` connu est explicitement masqué par le
   harnais/l'énoncé — remplacer par une preuve déclarative (« tests cachés, jugés par le validateur ») dans
   `acceptance-record.md`, déjà prévu par son gabarit (« AC-001 … reste à la main du validateur, qui seul dispose
   de la suite cachée »).
5. **Ne pas re-déclencher `go test`/`npm test` à `gate check --strict` quand le dernier run est rouge pour la
   même raison structurelle et la même empreinte d'arbre** (`exit 127` faute de toolchain, ou « No tests found »
   faute de suite) : c'est un signal environnemental, pas un signal de code qui aurait pu changer. Le
   fingerprint-skip existant (`gate_test_run._recorded_run_is_fresh_and_green`) ne couvre que le cas vert ; il
   manque le symétrique « rouge identique, ne rejoue pas, redis juste le diagnostic ». Gain mesuré possible : sur
   Go, jusqu'à 10 appels `gate check` observés sur un seul run (`go__simple-linked-list/run0`) ; sur JS, médiane
   de 3 appels `gate check --strict` qui échouent à l'identique sur 15/15 runs, sans jamais converger.
