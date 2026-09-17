# Analyse des tours — bras `kit-gov` (lot F, issue #582)

Analyse en lecture seule, snapshot pris le 2026-09-17 pendant que la campagne
tournait encore (PID dans `_scratch/bench-f/full.pid`). **21 runs `kit-gov`**
disponibles dans `_scratch/bench-f/workspace/state/results.jsonl` au moment de
l'analyse (15 Python : zipper/react/list-ops/proverb/bowling ×3, 6 JavaScript :
list-ops ×3, go-counting ×3 partiel) — les 21 ont été lus et catégorisés en
détail (dépasse le plancher de 8 demandé), aucun résultat n'a été extrapolé
sans preuve sur disque.

Aucun fichier de la campagne en cours n'a été modifié. Aucun identifiant
(`.credentials.json`, `.claude.json`) n'a été ouvert.

## Chiffres généraux (21 runs)

| Bras | n | Tours médians | Coût médian | Temps médian | Succès |
|---|---:|---:|---:|---:|---:|
| `kit-gov` | 21 | **31** | 2,05 $ | 274 s | 21/21 |
| `kit` (rappel) | 60 | 6 | 0,43 $ | 57 s | 54/60 |
| `nu` (rappel) | 60 | 6 | 0,40 $ | 64 s | 55/60 |

Pire run : `javascript__list-ops run1` — 53 tours, 340 s, 3,18 $.

## 1. Décomposition des tours par activité

Comptage par appel d'outil (Bash/Read/Write/Edit) classé sur le contenu réel
de la commande ou du chemin de fichier, dans les 21 transcriptions
`run*.stream.jsonl`. `num_turns` (champ SDK, médiane 31) ≈ nombre d'appels
d'outils + narration ; le tableau ci-dessous compte les **appels d'outils**,
qui en sont l'écrasante majorité.

| Catégorie | Médiane | Max | Pire run (js/list-ops run1) |
|---|---:|---:|---:|
| Orientation gouvernance (lister `_grimoire-output`, lire les gabarits `bootstrap/*.md`, `git status`, nettoyer `__pycache__`) | 8,0 | 12 | 11 |
| **Spéléologie dans le source Grimoire** (`grep`/`sed -n` sur le CLI/lib `grimoire` installé ou sur `_scratch/kit-bench-f/src` pour décoder un gate) | **8,0** | **20** | **18** |
| Écriture `task-envelope.md` | 1,0 | 4 | 1 |
| Écriture `evidence-pack.md` / `acceptance-record.md` / `claim-ledger.md` | 1,0 | 3 | 2 |
| `gate run-tests` | 4,0 | 7 | 4 |
| `gate check --strict` | 3,0 | 6 | 2 |
| `standard verify` | 1,0 | 4 | 4 |
| `context build` + découverte CLI (`--help`) | 3,0 | 4 | 2 |
| **Travail réel sur la tâche** (édition du fichier solution, exécution locale `python3`/`node`/vérifications ad hoc) | **2,0** | 6 | 6 |
| Écriture mémoire Grimoire (`.claude/projects/.../memory/*.md`) | 0,0 | 3 | 2 |

Constats transverses, vérifiés sur les 21 transcriptions :

- **Boucles (même commande Bash répétée ≥2 fois consécutives) : zéro occurrence sur 21 runs.** Un faux positif a été trouvé et écarté (3 appels `Write` consécutifs sur des fichiers différents, confondus par mon premier détecteur avec une répétition).
- **Hook `Stop` bloquant la clôture : zéro occurrence sur 21 runs.** Le hook `Stop` est bien câblé dans le projet (`grimoire-hook --host claude --event Stop`, visible dans `.claude/settings.json` du dépôt de tâche), mais aucun événement `hook_started`/`hook_response` de type `Stop` n'apparaît dans les 21 flux stream-json — seul `SessionStart:startup` y figure (2 événements par run, toujours). Recherche complémentaire de « message de clôture suivi de tours supplémentaires » : les messages texte-seuls trouvés sont de la narration ordinaire entre appels d'outils, pas des tentatives de clôture repoussées. **Le surcoût du bras `kit-gov` n'est donc pas un artefact du hook Stop.**
- Le poste « travail réel » (code + exécution) ne représente que **2 tours sur 31 en médiane (~6-7 %)** ; gouvernance + spéléologie source, à eux seuls, en représentent **16 sur 31 (~52 %)**.

## 2. Pourquoi `test-run.json` manque dans 15/21 runs

Cause confirmée sur le code et sur le disque, pas une command non détectée
par accident : **c'est structurel, pas un raté de l'agent.**

`grimoire.core.standard_checks.acceptance_test_run.record_acceptance_test_run`
(le code exécuté par `grimoire standard gate run-tests`, lu dans
`.venv/lib64/python3.14/site-packages/grimoire/core/standard_checks/acceptance_test_run.py`,
kit 3.55.0) appelle `resolve_need("test-runner", root)`
(`grimoire/core/execution_needs.py`). Cette détection ne connaît que **4
marqueurs** :

```
pyproject.toml → "pytest -q"
package.json   → "npm test"
Cargo.toml     → "cargo test"
go.mod         → "go test ./..."
```

**Si `need.resolved` est faux, la fonction retourne sans exécuter ni écrire
aucun fichier** (`ok=False`, `command=""`) — c'est un retour précoce
explicite, pas une commande qui échoue.

- **Python (15/15 runs, `kit_test_run_evidence=False`)** : les exercices
  Exercism du `polyglot-benchmark` ne livrent ni `pyproject.toml`, ni
  `setup.py`, ni `pytest.ini` — un seul fichier `.py` de stub. Vérifié sur
  disque (`_scratch/bench-f/workspace/tasks/python__zipper/kit-gov/run0/`) :
  aucun marqueur présent. `need.resolved` est **structurellement toujours
  faux** pour ces tâches, quoi que fasse l'agent. Le champ
  `evidence-pack.md` du run confirme que l'agent a bien lancé
  `grimoire standard gate run-tests --task-id python__zipper` (ligne « Gate
  tests Grimoire ») et a reçu *« N/A — aucune commande de test connue dans le
  dépôt »* (WARN, `acceptance.no_test_command_detected`) — l'agent obéit à
  l'ordre, le gate ne peut simplement rien écrire.
- **JavaScript (6/6 runs, `kit_test_run_evidence=True`)** : `package.json`
  est livré par l'exercice avec `"scripts": {"test": "jest ./*"}` → `need`
  résolu, la commande `npm test` est exécutée et **son verdict est écrit dans
  `test-run.json` même quand `ok=false`** (`node_modules` absent, aucun
  fichier `*.spec.js` visible puisque le test est caché — la note mémoire
  `run-tests-gate-unsatisfiable.md` écrite par l'agent lui-même documente un
  échec `exit 127`). Le fichier existe donc, la preuve « le gate a tourné »
  est satisfaite, indépendamment du fait que le test passe.
- **Go/Rust** : marqueurs supportés (`go.mod`, `Cargo.toml`) — l'exercice
  Exercism les livre en général, `test-run.json` serait probablement produit.
  **Java/C++ : aucun marqueur supporté** (`pom.xml`/`build.gradle`,
  `CMakeLists.txt` absents de la liste) — `test-run.json` n'y sera **jamais**
  écrit non plus, même si l'agent fait tout correctement.
- Le harnais cherche au bon endroit (`has_test_run_evidence` :
  `_grimoire-output/evidence/<task>/test-run.json`, glob vérifié) et avec le
  bon id (`_governed_task_id`, remplacement `/`→`__` cohérent entre le
  harnais et Grimoire) — ce n'est **pas** un problème de chemin ou de
  `--task-id` divergent.

## 3. Directive reçue au `SessionStart`

Texte injecté (`additionalContext` du hook `SessionStart:startup`, identique
pour les 21 runs à l'id de tâche près, lu en clair dans
`run0.stream.jsonl` de chaque tâche) :

```
[Grimoire — persona d'entrée] concierge — Concierge — Triage, clarification,
routage intelligent vers l'agent adapté. Frontière d'outils : read, search.
Lis `_grimoire/kit/agents/concierge.md` en entier seulement si la demande est
ambiguë ou s'il faut trier entre plusieurs pistes ; sinon, ce résumé suffit
pour rester dans son rôle.

[Grimoire — rappel de tâche] <task_id> : rien en mémoire — première fois que
ce sujet est travaillé.
[Grimoire Standard — activation]
Ce projet est gouverné par le standard agentique Grimoire. Ces étapes font
partie de la tâche demandée :
1. AVANT toute modification de code : remplis
   `_grimoire-output/evidence/<task_id>/task-envelope.md` — objectif,
   périmètre outillé (tool boundary) concret, critères de sortie.
2. PENDANT le travail : consigne chaque preuve (commande exécutée, test
   vert, diff clé) comme ligne concrète de l'inventaire dans
   `_grimoire-output/evidence/<task_id>/evidence-pack.md`, et remplace le
   résumé placeholder.
3. AVANT de conclure : exécute
   `grimoire standard gate run-tests --task-id <task_id>` puis
   `grimoire standard gate check --task-id <task_id> --strict` puis
   `grimoire standard verify .` et corrige tout échec.
Une clôture sans gates verts est une tâche non terminée.
```

Ordres suivis / ignorés, vérifiés sur les 21 transcriptions :

- **Suivi à la lettre** : remplissage du `task-envelope.md` avant tout code
  (100 % des runs), tenue de l'`evidence-pack.md`, exécution séquentielle des
  3 commandes de gate dans l'ordre prescrit.
- **Suivi en substance, pas à la lettre** : « corrige tout échec » — pour
  `gate run-tests`, correction impossible par construction (§2), donc
  l'agent le réinterprète en « déclare la non-applicabilité et justifie »
  (vu dans `acceptance-record.md` de chaque run python : statut « à
  vérifier », jamais bloquant). Il ne relance jamais `npm install` réseau ni
  ne crée de fichier de test pour forcer le gate au vert — comportement
  correct et documenté par l'agent lui-même dans ses notes mémoire, mais qui
  contredit la lettre de « clôture sans gates verts = tâche non terminée ».
- **Ignoré sans le dire** : la frontière d'outils du persona d'entrée
  (« read, search ») n'est respectée dans aucun des 21 runs — l'agent édite
  le fichier solution, exécute du code, écrit dans `_grimoire-output/` dès
  le premier tour utile. Le persona concierge sert de décor d'ouverture, pas
  de contrainte réelle ; la tâche demandée (implémenter du code) prime
  silencieusement sur le tool boundary annoncé.
- **Angle mort de la directive** : elle mandate `gate run-tests` sans jamais
  vérifier au préalable si `resolve_need("test-runner")` peut aboutir — ni le
  hook `SessionStart` ni le message d'ordre ne savent que, pour ces 15 tâches
  Python, le gate est mathématiquement inatteignable.

## 4. Trois recommandations chiffrées pour le lot G

Toutes les estimations ci-dessous sont des tours **effectivement observés**
dans les 21 runs lus (pas une extrapolation) : médiane et pire cas
(`javascript__list-ops run1`, 53 tours).

### G1 — `gate check --strict` génère lui-même `context-bundle.yaml` (ou dit où le poser) au lieu de renvoyer `FAIL missing context_bundle`

Cause exacte trouvée dans la note mémoire écrite par l'agent lui-même
(`gate-check-exige-context-bundle.md`, run `javascript__go-counting run1`) :
le message d'erreur ne dit pas où poser le fichier, et le chemin attendu
(`context_bundle_ref` du task-board) n'est nulle part dans le message. Sur
21/21 runs, l'agent a dû ouvrir le **code source installé de Grimoire**
(`.venv/.../site-packages/grimoire/{cli,core,missions}/*.py` ou le worktree
`_scratch/kit-bench-f/src`) pour comprendre quoi faire.

- **Tours retirés : médiane 11/run** (spéléologie source 8 + `context
  build`/découverte CLI 3), **jusqu'à 22 sur le pire run** (18 + 4).
- C'est le plus gros levier disponible : à lui seul il explique environ un
  tiers des tours du bras `kit-gov` (16/31 en incluant l'orientation
  gouvernance générale liée au même problème).

### G2 — `task-envelope.md`/`evidence-pack.md` pré-remplis par le hook `SessionStart` (squelette avec task_id, profil, `TASK.md` déjà injectés) plutôt que par l'agent

L'agent recopie systématiquement le gabarit vide de
`_grimoire-output/evidence/bootstrap/*.md` avant de le remplir (observé dans
`other_bash` : `for f in *.md; do cat "$f"; done` sur le dossier bootstrap,
présent dans une majorité des runs) puis réécrit les mêmes champs
mécaniques (task_id, profile, deliverable) qu'un hook connaît déjà.

- **Tours retirés : médiane 3-4/run** (écriture envelope 1 + evidence-pack 1
  + lecture du gabarit bootstrap ~1-2, tous mesurés), **jusqu'à 6-7 sur les
  runs qui relisent le gabarit deux fois** (`python__zipper run2` : 4
  envelope + 1 evidence-pack).

### G3 — la directive ne mandate `gate run-tests` que si `resolve_need("test-runner")` résout effectivement une commande pour ce projet

Sur 15/21 runs (tous les Python), le gate est **structurellement
inatteignable** (§2) : le mandat inconditionnel fait quand même exécuter la
commande, lire le WARN, et documenter la non-applicabilité dans trois
fichiers de preuve différents (evidence-pack, acceptance-record,
claim-ledger).

- **Tours retirés : médiane 4/run sur les 15 runs concernés** (appels
  `gate run-tests` eux-mêmes), **jusqu'à 7 sur le pire cas**
  (`python__react run0`). Effet indirect supplémentaire non chiffré ici :
  moins de lignes à justifier dans les 3 fichiers de preuve.
- Corollaire pour le lot G : ne **pas** prioriser un hook `Stop` non
  bloquant en batch — mesuré à zéro occurrence et zéro tour de coût sur les
  21 runs lus (§1). Ce serait un effort sans retour observable ici.

## Fichiers de référence

- Données : `/mnt/Travail/Projets/Dev/Grimoire-Forge/_scratch/bench-f/workspace/state/results.jsonl`
- Transcriptions analysées : `/mnt/Travail/Projets/Dev/Grimoire-Forge/_scratch/bench-f/workspace/tasks/*/kit-gov/run*.stream.jsonl`
- Dépôts de tâche (preuve du §2) : `/mnt/Travail/Projets/Dev/Grimoire-Forge/_scratch/bench-f/workspace/tasks/python__zipper/kit-gov/run0/`
- Notes mémoire écrites par l'agent lui-même : `/mnt/Travail/Projets/Dev/Grimoire-Forge/_scratch/bench-f/workspace/homes/kit-gov/.claude/projects/*/memory/*.md`
- Code de détection du gate : `.venv/lib64/python3.14/site-packages/grimoire/core/standard_checks/acceptance_test_run.py` et `execution_needs.py` (kit 3.55.0)
- Harnais de banc : `scripts/bench/three_arms.py` (`origin/main` périmé mais suffisant pour la structure, ou worktree `_scratch/kit-bench-f`)
