---
name: grimoire-executing-plans
description: "Exécution méthodique de plans d'implémentation. Use when: execute plan, run plan, follow plan, implement from plan, step by step execution, plan runner, plan executor."
---

# Executing Plans — Skill Grimoire

## Philosophie

Un plan bien écrit ne vaut rien sans exécution disciplinée. Cette skill transforme un plan bite-sized (produit par `grimoire-writing-plans`) en code vérifié, étape par étape, sans dérive ni raccourci.

**Règle fondamentale** : chaque étape est exécutée puis **vérifiée** avant de passer à la suivante. Un échec de vérification bloque l'avancement.

**Bâton autonome** : si l'utilisateur demande explicitement d'exécuter le plan, l'agent enchaîne les étapes sans demander de confirmation intermédiaire. Il ne remonte que les vrais bloqueurs ou les décisions produit/architecture nécessaires.

## Quand utiliser cette skill

- Après qu'un plan a été produit par `grimoire-writing-plans`
- Quand un plan d'implémentation est fourni par l'utilisateur
- Pour exécuter un plan complexe nécessitant rigueur et vérification

## Process

### Phase 1 — Préparation

1. **Charger le plan complet** — lire le document de plan de bout en bout
2. **Inventaire rapide** — lister les fichiers qui seront touchés
3. **Vérifier le point zéro** — s'assurer que les tests existants passent avant toute modification
4. **Identifier les risques** — noter les étapes à haut risque (suppression, migration, refactoring lourd)

```
POINT ZÉRO : Exécuter la suite de tests pertinente
Si tests en échec → STOP. Corriger d'abord. Ne jamais commencer un plan sur une base instable.
```

### Phase 2 — Exécution séquentielle

Pour **chaque étape** du plan :

#### 2a — Lire l'étape

- Lire la description, le fichier cible, l'action attendue
- Identifier le code exact à écrire ou modifier
- Repérer la commande de vérification

#### 2b — Implémenter

- Appliquer les modifications exactement comme décrit dans le plan
- Ne pas improviser ni "améliorer" — suivre le plan tel quel
- Si le plan contient une erreur évidente (import manquant, typo), la corriger et le **noter**

#### 2c — Vérifier

- Exécuter la commande de vérification de l'étape
- Si **PASS** → loguer le résultat et passer à l'étape suivante
- Si **FAIL** → entrer en mode diagnostic (Phase 3)

#### 2d — Loguer

Format de log par étape :

```
✅ Étape N : [titre] — PASS
   Fichier: path/to/file.py
   Vérification: [commande exécutée]
```

ou en cas de correction :

```
⚠️ Étape N : [titre] — PASS avec correction
   Fichier: path/to/file.py
   Correction: [description de la déviation du plan]
   Vérification: [commande exécutée]
```

### Phase 3 — Diagnostic d'échec

Quand une vérification échoue :

1. **Lire l'erreur complète** — ne pas deviner, lire le traceback/output
2. **Classifier** — erreur du plan vs erreur d'implémentation vs erreur préexistante
3. **Appliquer le fix minimal** — corriger uniquement ce qui est nécessaire pour verdir
4. **Re-vérifier** — relancer la commande de vérification
5. **Si 3 tentatives échouent** → invoquer `grimoire-systematic-debugging` et **noter l'échec**

### Phase 4 — Clôture

Une fois toutes les étapes exécutées :

1. **Test suite complète** — relancer tous les tests associés au plan
2. **Lint check** — exécuter ruff sur les fichiers modifiés
3. **Same-goal endgame sweep** — exécuter immédiatement les suites logiques L1/L2 révélées par le plan : docs touchées, contrats impactés, artefacts générés, petits fix adjacents, tests manquants mais évidents
4. **Rapport de synthèse** :

```
## Rapport d'exécution — [Nom du plan]

| Étape | Statut | Notes |
|---|---|---|
| 1. [titre] | ✅ | — |
| 2. [titre] | ⚠️ | Import manquant corrigé |
| 3. [titre] | ✅ | — |

**Tests** : N/N passés
**Lint** : clean
**Déviations du plan** : 1 (étape 2 — correction mineure)
```

5. **Learning capture** — si des corrections ont été nécessaires, enregistrer un learning via `grimoire-learnings`

## Règles de discipline

| Règle | Description |
|---|---|
| **Pas de freestyle** | Implémenter exactement ce que dit le plan. Les améliorations viennent après |
| **Vérification obligatoire** | Jamais de "ça devrait marcher". Exécuter la commande |
| **Progression linéaire** | Pas de saut d'étape, même si ça semble trivial |
| **Transparence** | Toute déviation est documentée dans le rapport |
| **Fail fast** | Si le point zéro échoue, ne pas commencer |
| **Pas de clôture prématurée** | Si le plan révèle une suite logique même objectif/L1/L2, l'exécuter avant le rapport final |
| **Pas de checkpoint artificiel** | Si l'utilisateur a demandé l'exécution, ne pas demander "je continue ?" entre les étapes |

## Chaîne de skills

```
grimoire-writing-plans → grimoire-executing-plans → grimoire-verification
                                    ↓ (si échec)
                         grimoire-systematic-debugging
                                    ↓ (si learning)
                            grimoire-learnings
```

## Mode subagent

Quand le plan est exécuté via `grimoire-subagent-dev` :

- Chaque étape est dispatchée individuellement à un subagent dev
- Le subagent reçoit : contexte du plan + étape complète + commande de vérification
- Le rapport de chaque subagent est agrégé par l'orchestrateur dans le rapport final
- L'orchestrateur vérifie la cohérence entre les étapes (pas de conflit d'édition)
