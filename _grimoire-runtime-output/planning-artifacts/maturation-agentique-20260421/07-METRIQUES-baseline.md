# 07 — Baseline métriques

> Mesures reproductibles, prises le 2026-04-21 depuis `main` branché sur `backup/main-before-origin-sync-20260415`. Cible : rester dans ces bornes pendant la maturation.

## Tableau de bord

| Métrique | Baseline | Cible fin V4 | Seuil d'alerte |
|---|---|---|---|
| Harmony score | 96/100 (A) | ≥ 94 | < 90 → stop |
| Fichiers scannés | 1389 | stable ±5% | — |
| Agents indexés | 84 | stable ±5 | — |
| Workflows indexés | 567 | ≤ 600 | > 700 |
| Tools indexés | 148 | ≤ 160 | > 200 |
| Dissonances total | 46 | ≤ 30 | > 60 |
| Dissonances orphan | 4 | ≤ 2 | > 6 |
| Dissonances size | 32 | ≤ 20 | > 40 |
| Dissonances duplication | 10 | ≤ 5 | > 15 |
| Tests kit (non-e2e) collectés | ≥ 600 | ≥ 650 | régression |
| Tests grimoire-game | 94 | ≥ 120 | régression |
| Ruff status | Clean | Clean | 1+ erreur |
| Framework tools > 800 lignes | 15 | ≤ 10 | > 18 |
| Modules canoniques `src/grimoire/tools/` | 13 | ≥ 18 | — |
| Hooks en `enforced` | 9/9 | 9/9 | régression |
| Scripts hooks | 13 | stable ±2 | — |
| Agents `.github/` | 23 | stable ±3 | — |
| Skills `.github/` | 41 | stable ±3 | — |
| Instructions `.github/` | 7 | stable ±2 | — |
| Prompts user-facing | 6 | stable ±2 | — |
| Artefacts `_dyn-*` vivants | 0 | ≤ 10 | > 30 |
| BM-* référencés | 42 | 32 (après archivages) | — |
| BM-* actifs | 24 | 27 (V4 durcit +3) | < 22 |
| BM-* archivés | 0 | ≥ 2 | — |

## Commandes de vérification

### Harmony

```bash
cd grimoire-kit
.venv/bin/python framework/tools/harmony-check.py --project-root .. score --json
```

### Preflight

```bash
cd grimoire-kit
.venv/bin/python framework/tools/preflight-check.py
```

### Tests Python

```bash
cd grimoire-kit
.venv/bin/python -m pytest --ignore=tests/e2e -q
```

### Tests TypeScript

```bash
cd grimoire-kit/apps/grimoire-game
npm run test
```

### Lint

```bash
cd grimoire-kit
.venv/bin/ruff check
```

### Inventaire hooks + agents + skills

```bash
cd /mnt/Travail/Projets/Dev/Grimoire-Forge
ls .github/hooks/scripts/ | wc -l
find .github/agents -maxdepth 1 -name "*.agent.md" | wc -l
find .github/skills -maxdepth 1 -type d -name "grimoire-*" | wc -l
find .github/prompts -maxdepth 1 -name "*.md" | wc -l
find .github/instructions -maxdepth 1 -name "*.md" | wc -l
find .github -name "_dyn-*" | wc -l
```

### Identifiants BM-*

```bash
cd /mnt/Travail/Projets/Dev/Grimoire-Forge
grep -rohE "BM-[0-9]+" .github _grimoire-runtime grimoire-kit/framework | sort -u | wc -l
```

### Framework tools volumineux

```bash
cd grimoire-kit
for f in framework/tools/*.py; do l=$(wc -l < "$f"); [ "$l" -gt 800 ] && echo "$l $f"; done | sort -rn
```

## KPIs de valeur utilisateur (ajoutés à chaque vague)

Ces métriques n'existent pas encore (V1 les crée), mais seront les plus parlantes :

| Métrique | Introduite par |
|---|---|
| Événements `GrimoireEvent` / heure | V1 |
| Latence hook → surface | V1 |
| Ratio `tool.blocked` / `tool.total` | V1 |
| Cartes Mission Board traitées (non-mock) | V2 |
| Temps moyen carte `queued → done` | V2 |
| Personnages actifs simultanés dans `observatory` | V3 |
| Concepts BM-* archivés | V4 |

## Checkpoint à chaque merge

Un commit qui régresse l'une des métriques hors seuil d'alerte doit déclencher :

1. Revert automatique
2. Note dans `_grimoire-runtime/_memory/failure-museum.md`
3. Analyse via skill `grimoire-systematic-debugging`

## Observabilité de la baseline

Une fois V1 livré, ces mesures seront visibles **dans la surface `observability`** elle-même (sans besoin de ligne de commande). Fin V3, elles sont également scrubbables dans le temps.
