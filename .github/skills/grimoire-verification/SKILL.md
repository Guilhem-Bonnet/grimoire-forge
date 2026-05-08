---
name: grimoire-verification
description: "Vérification obligatoire avant toute claim de complétion. Use when: claiming work is done, about to commit, PR creation, task completion, before marking complete, verification, evidence before claims."
---

# Vérification Avant Complétion

Affirmer qu'un travail est terminé sans vérification est de la malhonnêteté, pas de l'efficacité. Adapté de superpowers.

## Principe fondamental

```
AUCUNE CLAIM DE COMPLÉTION SANS PREUVE DE VÉRIFICATION FRAÎCHE
```

Si la commande de vérification n'a pas été exécutée dans ce message, impossible de prétendre qu'elle passe.

## Quand NE PAS utiliser

- Pour exécuter la batterie complète de checks finaux avant push (tests + lint + harmony + preflight) → `grimoire-pre-push`.
- Pour un audit projet multi-axes (mémoire, antifragile, harmonie, structure) → `grimoire-health-check`.
- Cette skill est ciblée claim-par-claim ; ne pas l'utiliser comme audit large.

## La Fonction Gate

```
AVANT toute claim de statut ou expression de satisfaction :

1. IDENTIFIER : Quelle commande prouve cette claim ?
2. EXÉCUTER : Lancer la commande COMPLÈTE (fraîche)
3. LIRE : Sortie complète, vérifier le code de retour
4. VÉRIFIER : La sortie confirme la claim ?
   - Si NON : Déclarer le statut réel avec preuve
   - Si OUI : Déclarer la claim AVEC preuve
5. ÉTENDRE : Si une vérification adjacente même objectif/L1/L2 est évidente, l'exécuter maintenant (tests pertinents plus larges, lint, docs, contrats, artefacts générés)
6. SEULEMENT ALORS : Faire la claim ou clôturer

Sauter une étape = mentir, pas vérifier
```

## Patterns de vérification

**Tests :**

```
OK  [Lancer pytest] [Voir: 34/34 pass] "Tous les tests passent"
KO  "Devrait passer maintenant" / "Semble correct"
```

**Tests de régression (TDD Red-Green) :**

```
OK  Écrire → Run (pass) → Revert fix → Run (DOIT FAIL) → Restore → Run (pass)
KO  "J'ai écrit un test de régression" (sans vérification red-green)
```

**Build :**

```
OK  [Lancer ruff check] [Voir: 0 errors] "Lint propre"
KO  "Le linter est passé" (le linter ne vérifie pas la compilation)
```

**Exigences :**

```
OK  Relire plan → Créer checklist → Vérifier chaque item → Reporter écarts
KO  "Les tests passent, phase terminée"
```

**Délégation sub-agent :**

```
OK  Sub-agent reporte succès → Vérifier le diff VCS → Vérifier les changements
KO  Faire confiance au rapport du sub-agent sans vérification
```

## Red Flags — STOP

- Utiliser "devrait", "probablement", "semble"
- Exprimer satisfaction avant vérification ("Parfait !", "Terminé !")
- S'apprêter à commit/push/PR sans vérification
- Faire confiance aux rapports d'agents
- Se fier à une vérification partielle
- Clore après un seul check vert alors qu'une vérification adjacente évidente reste à faire
- Penser "juste cette fois"

## Rationalisations

| Excuse | Réalité |
|---|---|
| "Devrait marcher maintenant" | LANCER la vérification |
| "Je suis confiant" | La confiance ≠ une preuve |
| "Juste cette fois" | Pas d'exception |
| "Le linter est passé" | Linter ≠ compilateur |
| "L'agent dit succès" | Vérifier indépendamment |
| "Vérification partielle suffit" | Partiel ne prouve rien |

## Quand appliquer

**TOUJOURS avant :**

- Toute variation de claim de succès/complétion
- Toute expression de satisfaction
- Commit, création de PR, complétion de tâche
- Passage à la tâche suivante
- Retour de contrôle à l'utilisateur
- Délégation à des sub-agents

## Commandes Grimoire

```bash
# Tests
pytest tests/ -v --tb=short

# Lint
ruff check src/

# Type check (si configuré)
mypy src/

# Preflight complet
python3 framework/tools/preflight-check.py --project-root .
```
