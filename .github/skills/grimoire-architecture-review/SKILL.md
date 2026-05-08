---
name: grimoire-architecture-review
description: "Review d'architecture multi-dimension. Évalue la qualité structurelle, les couplages, la dette technique, et la conformité aux ADR. Use when: architecture review, structure review, coupling analysis, tech debt, dependency check, modularity, evaluate architecture, ADR conformity."
---

# Architecture Review — Skill Grimoire

## Philosophie

Une architecture qui n'est pas régulièrement challengée se dégrade silencieusement. Cette skill applique un audit structuré multi-dimension, inspiré des pratiques de fitness functions et des Architecture Decision Records (ADR).

## Quand utiliser cette skill

- Avant un refactoring majeur
- À chaque milestone (sprint review, release)
- Quand on suspecte de la dette technique
- Pour valider la conformité aux ADR du projet
- Quand un module "sent mauvais" mais on ne sait pas pourquoi

## Process

### Phase 1 — Inventaire structurel

Cartographier l'architecture actuelle :

1. **Modules et packages** — lister tous les packages Python, leurs tailles, et leur responsabilité
2. **Graph de dépendances** — tracer les imports entre modules pour identifier les couplages
3. **Points d'entrée** — CLI, API, hooks, lifecycle — quels sont les entry points ?
4. **Couches** — identifier les couches (core, tools, framework, tests) et vérifier le respect des limites

```
Commandes utiles :
  find src/ -name "*.py" | head -50
  grep -r "^from " src/grimoire/ | sort | uniq -c | sort -rn | head -20
  wc -l src/grimoire/**/*.py | sort -n
```

### Phase 2 — Analyse des ADR

Si des ADR existent (dans `docs/`, `_grimoire-runtime-output/planning-artifacts/`, ou `docs/governance/`) :

1. Lister tous les ADR trouvés
2. Pour chaque ADR, vérifier si la décision est respectée dans le code actuel
3. Identifier les ADR obsolètes ou contradictoires
4. Signaler les décisions implicites (patterns récurrents sans ADR documenté)

Format de finding :

```
ADR-00X : [Titre]
  Statut : ✅ Respecté | ⚠️ Partiellement | ❌ Violé | 🔄 Obsolète
  Preuve : [fichier:ligne ou pattern observé]
  Note : [contexte si nécessaire]
```

### Phase 3 — Métriques de qualité

Évaluer sur 5 dimensions (score /5 chacune) :

| Dimension | Critères | Score |
|---|---|---|
| **Cohésion** | Chaque module a une responsabilité unique et claire | /5 |
| **Couplage** | Les dépendances entre modules sont minimales et explicites | /5 |
| **Testabilité** | Chaque module peut être testé en isolation | /5 |
| **Extensibilité** | On peut ajouter des features sans modifier le core | /5 |
| **Conformité ADR** | Les décisions architecturales documentées sont respectées | /5 |

#### Indicateurs automatisés

```
# Fan-in/Fan-out par module
grep -r "^from grimoire\." src/grimoire/ | awk -F: '{print $1}' | sort | uniq -c | sort -rn

# Taille des modules (LOC)
find src/grimoire -name "*.py" -exec wc -l {} \; | sort -rn | head -20

# Tests par module
for d in src/grimoire/*/; do
  mod=$(basename "$d")
  tests=$(find tests/ -name "test_${mod}*" -o -name "test_*${mod}*" 2>/dev/null | wc -l)
  echo "$mod: $tests test file(s)"
done

# Ratio test/code
code_lines=$(find src/ -name "*.py" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
test_lines=$(find tests/ -name "*.py" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
echo "Ratio: $test_lines / $code_lines"
```

### Phase 4 — Identification de la dette technique

Classifier la dette trouvée :

| Type | Exemples | Urgence |
|---|---|---|
| **Design debt** | Mauvaise abstraction, responsabilité mal placée | Moyenne |
| **Code debt** | Duplication, complexité cyclomatique élevée | Variable |
| **Test debt** | Module sans tests, tests fragiles | Haute |
| **Doc debt** | ADR manquant pour une décision structurelle | Basse |
| **Dependency debt** | Dépendance circulaire, version obsolète | Haute |

### Phase 5 — Rapport de synthèse

```markdown
## Architecture Review — [Projet] — [Date]

### Scores

| Dimension | Score | Tendance |
|---|---|---|
| Cohésion | X/5 | ↗️ / → / ↘️ |
| Couplage | X/5 | ↗️ / → / ↘️ |
| Testabilité | X/5 | ↗️ / → / ↘️ |
| Extensibilité | X/5 | ↗️ / → / ↘️ |
| Conformité ADR | X/5 | ↗️ / → / ↘️ |
| **Total** | **XX/25** | |

### Findings critiques
1. [Finding le plus impactant]
2. [...]

### Dette technique identifiée
| # | Type | Description | Urgence | Effort estimé |
|---|---|---|---|---|

### ADR Status
| ADR | Titre | Statut |
|---|---|---|

### Recommandations
1. [Action prioritaire]
2. [...]
```

### Phase 6 — Learning capture

Si l'architecture review révèle des patterns récurrents, les capturer comme learnings :

```
Skill: grimoire-learnings
Key: arch-review-[pattern]
Insight: [description du pattern]
Confidence: [basé sur le nombre de modules affectés]
```

## Chaîne de skills

```
grimoire-architecture-review → grimoire-writing-plans (si refactoring nécessaire)
                             → grimoire-learnings (patterns découverts)
                             → grimoire-health-check (complémentaire)
```

## Différence avec grimoire-health-check

- **health-check** : diagnostic rapide (preflight, harmony, lint) — état opérationnel
- **architecture-review** : analyse en profondeur — qualité structurelle, dette, conformité ADR
