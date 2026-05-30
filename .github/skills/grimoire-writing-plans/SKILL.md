---
name: grimoire-writing-plans
description: "Écriture de plans d'implémentation bite-sized. Use when: writing plans, implementation plan, plan steps, decompose task, create plan, step-by-step plan, plan for agent, plan for subagent."
---

# Writing Plans — Skill Grimoire

## Philosophie

Un bon plan est la différence entre une implémentation en 10 minutes et un tunnel de 2 heures. Cette skill produit des plans **bite-sized** : chaque étape prend 2-5 minutes, contient du code complet (jamais de placeholders), et est exécutable indépendamment.

**Inspiration** : superpowers (133k★) writing-plans methodology.

## Quand utiliser cette skill

- Avant d'implémenter une feature multi-fichiers
- Pour préparer un plan exécutable par un subagent
- Quand une tâche semble nécessiter plus de 3 éditions de fichiers
- Pour décomposer un refactoring complexe

## Quand NE PAS utiliser

- Pour exécuter un plan déjà écrit step-by-step → `grimoire-executing-plans`.
- Pour explorer plusieurs approches avant de choisir → `grimoire-brainstorming` ou `grimoire-innovate`.
- Pour des tâches ≤ 3 éditions — écrire un plan ajoute plus de friction qu'il n'en économise.

## Process

### Phase 1 — Exploration du contexte

Avant d'écrire une seule ligne de plan :

1. **Explorer le code existant** — lire les fichiers concernés, comprendre la structure
2. **Identifier les dépendances** — quels modules sont impliqués, quels tests existent
3. **Vérifier les conventions** — charger les instructions pertinentes (python-conventions, markdown-standards)
4. **Lister les contraintes** — limites techniques, compatibilité, performances

> Ne jamais écrire un plan sans avoir lu le code. Un plan basé sur des hypothèses est un plan qui échoue.

### Phase 2 — Structure du plan

Le plan est un document Markdown avec ce format :

```markdown
# Plan : [Titre concis]

> Ce plan est destiné à un exécuteur agentic. Chaque étape est autonome
> et contient tout le contexte nécessaire.

## Contexte
[2-3 phrases sur le pourquoi et les contraintes]

## Étapes

### Étape 1 : [Titre descriptif]

**Fichier** : `path/to/file.py`
**Action** : Créer | Modifier | Supprimer

[Description précise de ce qui doit être fait]

```python
# Code COMPLET à écrire/modifier — pas de placeholders, pas de "..."
def actual_function():
    return actual_implementation()
```

**Vérification** : `python -m pytest tests/test_file.py -k test_function`

---

### Étape 2 : [Titre]
[...]
```

### Règles d'or

| Règle | Description |
|---|---|
| **Pas de placeholders** | Jamais de `TODO`, `...`, `pass`, ou `# implement here`. Chaque étape a du code complet |
| **Bite-sized** | 2-5 minutes par étape. Si une étape prend plus, la découper |
| **Code complet** | Inclure les imports, les types, les docstrings si la convention l'exige |
| **Vérification explicite** | Chaque étape a une commande de vérification (test, lint, build) |
| **Ordre d'exécution** | Les étapes sont ordonnées pour que chaque vérification passe immédiatement |
| **Context autonome** | Chaque étape contient le chemin du fichier, l'action, et tout le code |

### Phase 3 — Self-review

Avant de livrer le plan, vérifier :

- [ ] Chaque étape a un titre descriptif et une estimation de temps
- [ ] Aucun placeholder dans le code
- [ ] Les imports sont complets dans chaque étape
- [ ] Les vérifications sont exécutables
- [ ] L'ordre des étapes est correct (pas de dépendance inversée)
- [ ] Le contexte initial est suffisant pour comprendre le pourquoi
- [ ] Les conventions du projet sont respectées (types, style, nommage)

### Phase 4 — Handoff

Le plan terminé peut être :

1. **Exécuté inline** — le même agent suit les étapes une par une
2. **Dispatché à un subagent** — utiliser la skill `grimoire-subagent-dev` pour dispatcher chaque étape
3. **Donné à l'utilisateur** — comme guide d'implémentation manuelle

Pour le dispatch subagent, chaque étape devient un prompt autonome :

```
Implémente l'étape N du plan [PLAN_NAME].

## Contexte
[Le contexte du plan]

## Étape à implémenter
[L'étape complète avec code]

## Vérification
[La commande de vérification]

Exécute la vérification après implémentation et confirme le résultat.
```

## Anti-patterns

| Anti-pattern | Correction |
|---|---|
| "Créer un fichier avec la logique appropriée" | Écrire le code complet |
| Étape de 30 minutes | Découper en 6 étapes de 5 minutes |
| Plan sans exploration préalable | Toujours Phase 1 d'abord |
| Vérification vague ("tester que ça marche") | Commande exacte à exécuter |
| Dépendance circulaire entre étapes | Réordonner pour progression linéaire |
