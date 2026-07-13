# DOC technique — Chaîne de preuve des workflows

Compagnon technique du package `preuve-workflows-20260712`.
Document de référence : `PLAN-preuve-workflows.md`.

## État as-built (2026-07-12)

Les cinq chantiers sont implémentés et verts. Écarts au plan, tous actés dans
les decision traces des cartes kanban `c1` à `c5` :

| Sujet | Plan | As-built |
| --- | --- | --- |
| Journaux C1/C4 | `_grimoire-runtime-output/task-flow/` | `_grimoire-runtime/_memory/` — le memory-guard protège déjà ce préfixe, zéro modification des outils du kit |
| Hook C4 | extension de `grimoire-prompt-submit` | hook dédié `grimoire-engagement` (isole le risque, cycle shadow/canary/promote) |
| Pilote C3 | workflow BMM `4-implementation` | `deliverable-package` (packages planning-artifacts) ; `dev-story` reste le prochain candidat |
| Ordre chronologique C3 | check systématique | opt-in `enforce_order` par workflow — les mtimes sont une preuve faible, la preuve d'ordre forte est portée par le golden run C5 |

**Prérequis découvert et traité** : la couche gateway des hooks était morte —
`hook-safety-gate.py`, `guardrail-policy*` et `grimoire.tools.events` avaient
disparu du checkout kit lors du resync sur `origin/main` (préservés dans le
snapshot `ffcc85f6`). Neuf fichiers restaurés en worktree, non stagés
(discipline de staging chirurgical du kit préservée). Sans cette restauration,
tous les hooks routés par le gateway échouaient silencieusement, et
`grimoire-emit-event.sh` remplissait `events-errors.jsonl` à chaque event.

**Composants livrés** :

| Composant | Chemin |
| --- | --- |
| C1 logique record/check/reconcile | `scripts/board-transitions-log.py` |
| C1 hook + manifest | `.github/hooks/scripts/grimoire-board-transitions.sh`, `.github/hooks/grimoire-board-transitions.json` |
| C1 journal (écrit par hook uniquement) | `_grimoire-runtime/_memory/board-transitions.jsonl` |
| C2 réconciliateur | `scripts/evidence-reconcile.py` |
| C3 manifest + checker | `_grimoire/standard/workflow-state-manifest.yaml`, `scripts/workflow-step-check.py` |
| C4 logique + hook | `scripts/engagement-log.py`, `.github/hooks/scripts/grimoire-engagement.sh` |
| C4 journal | `_grimoire-runtime/_memory/engagement.jsonl` |
| C5 capture/diff | `scripts/golden-run-diff.py` |
| C5 référentiel | `_grimoire-runtime-output/test-artifacts/golden-runs/deliverable-package/golden.json` |
| Pipeline | section `6/6 Preuve` de `scripts/check-quality.sh` |

Les hooks `grimoire-board-transitions` et `grimoire-engagement` sont déclarés
dans `hook-safety-registry.json` en mode `shadow`, digest stampé ; promotion
via `grimoire: hooks-promote` à la main de l'utilisateur.

## Architecture cible

Le plan raccorde deux couches existantes sans en créer de troisième :

| Couche | Sources | Propriété |
| --- | --- | --- |
| Déclarative | `task-board.yaml`, evidence packs, decision traces | Riche, rédigée par l'agent, falsifiable |
| Machine | `task-flow/events.jsonl`, git, mtimes des artefacts | Déterministe, non falsifiable par l'agent |

Les chantiers C1 à C3 construisent les raccords ; C4 et C5 exploitent la
chaîne obtenue.

## Points d'ancrage dans le code existant

### Verify actuel (constat de départ)

- `_verify_task_board` — `grimoire-kit/src/grimoire/core/agentic_standard.py`
  (lignes 1284 et suivantes) : vérifie clés requises, statuts valides,
  refs dans le root. Aucune vérification de contenu ni d'ordre.
- `_verify_evidence_pack` — même fichier (lignes 1217 et suivantes) :
  anti-placeholders uniquement (`pending`, lignes vides, tableau vide).
- `_verify_workflow_state_manifest` — même fichier (lignes 2016 et
  suivantes) : structure du manifest (states, initial_state, transitions),
  pas l'exécution.
- `EvidenceService.verify` — `grimoire-kit/src/grimoire/evidence/service.py` :
  couverture par kinds (`TEST`, `LOG`, `DIFF`, `REPORT`, `DOC`), digest
  non vide (jamais recalculé), acceptance par substring-match.

### Infrastructure hooks réutilisée (C1, C4)

- Gateway : `.github/hooks/scripts/grimoire-hook-gateway.sh` avec registre
  `_grimoire-runtime/_config/hook-safety-registry.json`.
- Cycle de promotion : `shadow` puis `canary` puis `grimoire: hooks-promote`.
- Protection en écriture : mécanique du memory-guard
  (`grimoire-memory-guard.sh`), à étendre au journal des transitions.
- Smoke : `grimoire-hooks-smoke.sh` doit couvrir tout nouveau hook.

## Schémas de données introduits

### `board-transitions.jsonl` (C1)

```json
{"task_id": "c1-board-transitions", "from": "proposed", "to": "ready", "timestamp": "2026-07-15T10:00:00Z", "session": "<session-id>"}
```

Append-only, écrit exclusivement par le hook. La cohérence est vérifiée dans
les deux sens : dernier event contre statut courant du YAML, et légalité de
chaque transition contre `evidence-gates.yaml`.

### Verdicts de réconciliation (C2)

Chaque claim d'un evidence pack reçoit un verdict :

| Verdict | Signification | Effet (profil `governed`) |
| --- | --- | --- |
| `VERIFIED` | Claim corroboré par une source machine | Passe |
| `UNVERIFIABLE` | Aucune source machine ne peut corroborer | Warning |
| `CONTRADICTED` | Une source machine contredit le claim | Échec de gate |

En profil `production`, `UNVERIFIABLE` devient une erreur, aligné sur
`profile_strictness` de `evidence-gates.yaml`.

### Extension `workflow-state-manifest.yaml` (C3)

```yaml
steps:
  - id: step-3
    expected_artifact: "_grimoire-runtime-output/implementation-artifacts/<slug>/step-3-*.md"
```

Le checker valide existence (glob non vide) et ordre chronologique
(timestamp de step N strictement postérieur à step N-1).

### `engagement.jsonl` (C4)

```json
{"artifact": "grimoire-quick-flow", "kind": "workflow", "signal": "sog-dispatch", "timestamp": "2026-07-15T10:00:00Z", "session": "<session-id>"}
```

Le champ `signal` distingue les canaux de détection (dispatch SOG, lecture
fichier, slash command) pour permettre l'élargissement progressif.

## Décisions d'architecture actées

1. **Forge d'abord, upstream ensuite** (C2, C3) : les outils vivent dans la
   Forge tant qu'ils ne sont pas stabilisés, puis remontent dans le Kit via
   la mécanique nested/bridge habituelle. Évite de bloquer sur une release Kit.
2. **Le journal de transitions est écrit par hook, jamais par l'agent** (C1) :
   c'est la propriété qui rend la preuve opposable. Toute solution où l'agent
   écrit lui-même le journal est exclue.
3. **Rétro-validation sans réécriture** (C2) : les packs existants
   (bootstrap, r8, r9, r10) sont requalifiés explicitement si invérifiables,
   jamais réécrits pour passer le check.

## Limites connues

- La preuve couvre l'exécution, pas l'effet. La preuve d'effet relève de la
  campagne d'evals (hors périmètre, voir plan).
- Les mtimes de fichiers sont une source d'ordre faible (copies, checkouts) ;
  le checker C3 privilégie les timestamps internes aux artefacts quand ils
  existent, les mtimes en repli.
- Le hook C1 ne voit que les éditions passant par les outils de l'agent ;
  l'édition manuelle du YAML est rattrapée a posteriori par le check de
  cohérence, pas en temps réel.
