---
name: grimoire-safety-guards
description: "Safety guardrails: careful mode, freeze zones, guard mode. Use when: careful mode, safety mode, restrict edits, freeze directory, guard, protect files, high-risk changes, production changes."
---

# Safety Guards

Mécanismes de protection pour les opérations à haut risque. Adapté de gstack (`/careful`, `/freeze`, `/guard`).

## Modes disponibles

### Careful Mode

Mode de vérification renforcée pour les changements critiques.

**Activation :** quand l'utilisateur demande "mode prudent", "careful", "safety mode"

**Comportement :**

- Chaque changement de fichier est reviewé avant application
- Diff explicite montré à l'utilisateur avant commit
- Vérification doublée : lint + tests après chaque modification
- Pas de modifications groupées — une à la fois
- Confirmation explicite requise pour chaque étape

**Checklist Careful Mode :**

- [ ] Montrer le diff exact avant d'appliquer
- [ ] Lancer `ruff check` après chaque fichier modifié
- [ ] Lancer `pytest` après chaque modification
- [ ] Demander confirmation avant chaque commit
- [ ] Documenter chaque changement et sa raison

### Freeze Zones

Verrouiller les modifications à des répertoires spécifiques.

**Activation :** "freeze src/core", "geler ce dossier", "ne touche pas à X"

**Comportement :**

- Refuser toute modification aux fichiers dans les zones gelées
- Permettre la lecture/analyse des zones gelées
- Lister les zones gelées quand demandé
- Dégeler sur commande explicite

**Zones gelées par défaut (toujours actives) :**

- `_grimoire-runtime/_memory/` — protégé par le hook `grimoire-memory-guard`
- `_grimoire-runtime/_config/` — manifestes et registres

**Format de déclaration :**

```
FROZEN: src/grimoire/core/
FROZEN: tests/integration/
REASON: Stabilisation avant release
```

### Guard Mode

Protection persistante pour les sessions à haut risque.

**Activation :** "guard mode", "mode protection", opérations L3/L4

**Comportement :**

- Toutes les opérations traitées comme L3 minimum (confirmation requise)
- Cross-validation automatique (CVTL) sur chaque output
- Double vérification des commandes destructives
- Résumé de sécurité en fin de session

**Opérations nécessitant Guard :**

| Opération | Risque | Action Guard |
|---|---|---|
| `git push --force` | Destructif | Bloquer, proposer alternative |
| `rm -rf` | Destructif | Bloquer, lister les fichiers d'abord |
| Modification `.env`, secrets | Sécurité | Double confirmation |
| Migration DB | Infrastructure | Plan + rollback avant exécution |
| Modification CI/CD | Shared | Review complète avant apply |

## Commandes

| Commande | Action |
|---|---|
| "mode prudent" / "careful" | Activer Careful Mode |
| "freeze {path}" | Geler un répertoire |
| "unfreeze {path}" | Dégeler un répertoire |
| "guard on" | Activer Guard Mode |
| "guard off" | Désactiver Guard Mode |
| "zones gelées" / "list frozen" | Lister les zones gelées |

## Intégration SOG

L'orchestrateur SOG active automatiquement ces protections selon le contexte :

- **L1/L2** : Mode normal, pas de guard
- **L3** : Careful Mode suggéré si confiance < 90%
- **L4** : Guard Mode automatique, toujours

Le système d'autonomie (ALS) du SOG respecte les zones gelées et les modes actifs.
