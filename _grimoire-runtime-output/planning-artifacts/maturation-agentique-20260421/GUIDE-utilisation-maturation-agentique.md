# GUIDE — Utilisation du pack Maturation Agentique

> Comment lire, valider, et déclencher l'exécution de ce pack.

## Public

- **Utilisateur final** (toi) : tu décides, tu valides, tu donnes le go.
- **Orchestrateur Grimoire** : consomme ce pack pour générer les packs d'exécution V1-V4.
- **Futurs contributeurs** : ce pack est la référence source pour toute décision sur la maturation.

## Parcours recommandé

### Étape 1 — Lecture d'entrée (15 min max)

1. [README.md](README.md) — synthèse 30 secondes + mandat + vagues
2. [07-METRIQUES-baseline.md](07-METRIQUES-baseline.md) — pour voir où on part
3. [06-PLAN-execution-phases.md](06-PLAN-execution-phases.md) — pour voir où on va

Cette lecture suffit pour donner le go ou demander des ajustements.

### Étape 2 — Lecture profonde (si tu veux challenger)

1. [01-AUDIT-etat-existant.md](01-AUDIT-etat-existant.md) — vérifier les chiffres
2. [04-CARTOGRAPHIE-concepts.md](04-CARTOGRAPHIE-concepts.md) — valider les tris BM-* actifs/durcir/archiver
3. [03-GAP-ANALYSIS-hooks.md](03-GAP-ANALYSIS-hooks.md) — valider les trous identifiés
4. [02-EXTRACTIONS-refs.md](02-EXTRACTIONS-refs.md) — confirmer le choix des patterns à copier
5. [05-DECISIONS-rationalisation.md](05-DECISIONS-rationalisation.md) — trancher les décisions ouvertes O1-O5

## Actions possibles

### A — Donner le go sur V1

Message type à l'orchestrateur :

> OK, go V1. Décisions ouvertes : O1=WebSocket, O2=TS server, O3=différer en V4, O4=non, O5=polling 2s.

L'orchestrateur produira alors `_grimoire-runtime-output/planning-artifacts/V1-verite-bus-evenements-<date>/` avec les 8 stories S1.1-S1.8 prêtes à exécuter.

### B — Demander un ajustement

Exemples :

- *"Archive aussi BM-41 (semantic cache), on ne l'utilisera jamais"* → mise à jour `04-CARTOGRAPHIE-concepts.md` + ADR-S09 étendu
- *"Je veux V3 avant V2"* → ADR-S11 révisée, nouveau graphe
- *"Canal = SSE pas WS"* → ADR-S02 révisée

### C — Demander une revue adverse

> Lance une revue adverse de ce pack via skill grimoire-code-review et agent rodin.

L'orchestrateur déclenche une contre-analyse structurée avant le go.

### D — Différer

Le pack reste dormant dans `_grimoire-runtime-output/planning-artifacts/`. Tu peux y revenir plus tard. Les métriques baseline sont datées et resteront comparables.

## Comment les vagues s'enchaînent

À chaque go de vague :

1. L'orchestrateur produit un pack planning-artifact d'exécution dédié
2. Ce pack contient les stories L1/L2/L3, les contrats, les tests attendus
3. L'exécution démarre en autonomie L2 sauf demande contraire
4. En fin de vague : DOC-TECHNIQUE + GUIDE + mise à jour des métriques baseline
5. Passage à la vague suivante seulement après gates `07-METRIQUES-baseline.md` verts

## Ce que tu ne verras pas changer

Tant que tu n'as pas donné le go V1 :

- Aucun code source modifié
- Aucun hook redéployé
- Aucun fichier déplacé hors de `_grimoire-runtime-output/planning-artifacts/maturation-agentique-20260421/`
- Aucun site rebuilt

## Ce qui va changer dès V1

- `_grimoire-runtime/_memory/activity.jsonl` devient le ledger canonique
- Les 9 scripts hooks auront une sortie standardisée `GrimoireEvent`
- `observability` affichera des compteurs réels
- Tests e2e Playwright seront étendus

## Comment vérifier la baseline maintenant

Copie-colle dans un terminal depuis la racine du workspace :

```bash
cd grimoire-kit
.venv/bin/python framework/tools/harmony-check.py --project-root .. score --json \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"harmony={d['score']}/100 files={d['total_files']} dissonances={sum(d['category_counts'].values())}\")"
.venv/bin/ruff check 2>&1 | tail -1
```

Résultat attendu à la date du pack :

```text
harmony=96/100 files=1389 dissonances=46
All checks passed!
```

## Conventions respectées

Ce pack respecte :

- **CommonMark strict** : aucune extension Markdown non standard
- **Pas d'estimations temporelles** : "durée" = critère de sortie, pas calendrier
- **File links corrects** : tous relatifs au workspace, pas de backticks autour des chemins
- **Documentation companions** : ce fichier + `DOC-TECHNIQUE-maturation-agentique.md`
- **Charte de structure** : situé sous `_grimoire-runtime-output/planning-artifacts/` conformément à `.github/copilot-instructions.md`

## Questions fréquentes

### Pourquoi pas de dates / estimations ?

Convention repo. Les vagues ferment sur critères de sortie observables, pas sur calendrier. Cela protège la qualité.

### Pourquoi séquentiel et pas parallèle ?

ADR-S11 : V2/V3/V4 consomment le contrat `GameState` produit en V1. Paralléliser créerait trois façons divergentes de consommer un contrat instable.

### Que se passe-t-il si une vague échoue ?

Rollback automatique, entrée dans `_grimoire-runtime/_memory/failure-museum.md`, pack post-mortem produit avant reprise.

### Peut-on sauter V4 ?

Oui, mais au prix d'un codebase qui continue de porter ~10 concepts partiels non branchés et 2 concepts archivables vivants. Le score harmony en souffrira.

### Le site public est-il impacté ?

V1 non (ledger interne). V2 oui (Mission Board devient non-mock, `docs/produit/kanban-live.md` à mettre à jour). V3 oui (nouvelle surface `office-live.md` optionnelle). V4 non (rationalisation interne).

### Les packs précédents restent-ils valides ?

Oui. Ce pack complète `BRAINSTORM-PIXEL-OBSERVATORY-V2.md` et `plan-maitre-agent-os-game-ui.md`, il ne les annule pas.

## Prochaine action suggérée

1. Lis le [README.md](README.md)
2. Parcours `06-PLAN-execution-phases.md`
3. Tranche O1-O5
4. Donne le go V1 ou demande ajustement

Rien d'autre n'est attendu de ta part pour faire avancer la maturation.
