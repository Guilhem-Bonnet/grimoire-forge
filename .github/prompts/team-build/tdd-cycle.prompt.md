---
description: "Cycle TDD guidé — red-green-refactor pour une story ou une fonction"
---

# Skill: TDD Cycle Strict

Implémente `{{story_or_function}}` en suivant rigoureusement le cycle TDD.

## Mode
`[ACT]` — Exécution directe. Pas de confirmation intermédiaire. CC PASS avant fin.

## Contexte
- **Story / Fonction** : `{{story_or_function}}`
- **Fichier story** : `{{story_file_path}}` (si applicable)
- **Stack** : `{{stack}}` (auto-détecter si non précisé)
- **Framework de test** : `{{test_framework}}` (vitest/pytest/go-test/jest/etc.)

## Cycle TDD Obligatoire

### 🔴 RED — Écrire le test d'abord

```
1. COMPRENDRE l'AC à couvrir
2. ÉCRIRE le test le plus simple qui vérifie cet AC
3. VÉRIFIER que le test ÉCHOUE (sinon le test est faux ou la feature existe déjà)
4. Afficher l'output du test en échec
```

### 🟢 GREEN — Faire passer le test

```
1. Écrire le MINIMUM de code pour faire passer le test
2. Pas d'optimisation — juste faire passer
3. VÉRIFIER que le test passe maintenant
4. Afficher l'output du test en succès
```

### 🔵 REFACTOR — Nettoyer sans casser

```
1. Supprimer la duplication
2. Améliorer la lisibilité
3. VÉRIFIER que le test passe toujours après refactor
4. Répéter pour l'AC suivant
```

## Checklist Avant "Terminé"

- [ ] Chaque AC de la story a au moins 1 test
- [ ] Les cas d'erreur et edge cases sont testés
- [ ] Le code compile sans warning
- [ ] CC PASS avec output affiché

```
✅ CC PASS — {{stack}} — {{datetime}}
> {{test_command}} → OK (N tests, 0 failed)
> {{build_command}} → OK
```

## Gestion des Blocages

Si le test est difficile à écrire :
- Décomposer en plus petits tests
- Utiliser un mock/stub si dépendance externe
- Consulter l'ADR si choix architectural nécessaire

Si CC FAIL persistant après 2 tentatives :
- Documenter le blocage
- Créer un ticket dans le sprint backlog
- Ne PAS marquer la story comme terminée
