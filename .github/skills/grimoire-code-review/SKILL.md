---
name: grimoire-code-review
description: 'Review de code multi-couches avec triage structuré. Lance 3 reviewers parallèles (Adversarial, Edge Case Hunter, Acceptance Auditor) puis trie les findings. Use when: code review, review this code, review my changes, review staged, review branch diff, PR review, review avant merge.'
---

# Grimoire Code Review

Review de code adversariale multi-couches avec triage structuré en catégories actionnables.

## Quand utiliser

- Avant un merge/push
- Quand le user dit "review ce code", "review mes changements"
- Review de PR, branch diff, staged changes, ou diff fourni
- En complément ou remplacement de `review-adversarial-general`

## Procédure

### Step 1 — Collecter le contexte

#### 1.1 Détecter l'intention de review

Analyser le message déclencheur pour identifier le mode :

| Phrase détectée | Mode |
|---|---|
| "staged" / "staged changes" | Staged uniquement |
| "uncommitted" / "working tree" / "all changes" | Non-committées (staged + unstaged) |
| "branch diff" / "vs main" / "against main" | Branch diff |
| "commit range" / "last N commits" / "sha..sha" | Range de commits |
| "this diff" / "provided diff" | Diff fourni par l'utilisateur |

Si aucune correspondance claire → **HALT** et demander :

> **Que veux-tu review ?**
> 1. Changements non-committés (staged + unstaged)
> 2. Staged uniquement
> 3. Branch diff vs une branche de base
> 4. Range de commits spécifique
> 5. Diff ou liste de fichiers fournis

#### 1.2 Construire le diff

```bash
# Selon le mode :
git diff                           # uncommitted
git diff --cached                  # staged only
git diff main...HEAD               # branch diff
git diff <sha1>..<sha2>            # commit range
```

Vérifier que le diff n'est pas vide. Si vide → **HALT** "Rien à review."

#### 1.3 Contexte optionnel

Demander : **Y a-t-il une spec ou story qui donne du contexte pour ces changements ?**
- Si oui → `review_mode = "full"`, charger le fichier spec
- Si non → `review_mode = "no-spec"`

Si le diff dépasse ~3000 lignes, proposer de chunker par groupe de fichiers.

#### 1.4 Checkpoint

Présenter un résumé avant de continuer : stats du diff, mode de review, docs de contexte chargés.
**HALT** — attendre confirmation.

### Step 2 — Review parallèle

Lancer les 3 couches de review. Si les subagents ne sont pas disponibles, exécuter séquentiellement.

#### Couche 1 : Blind Hunter (Adversarial)

Invoquer le skill `grimoire-edge-case-hunter` n'est PAS suffisant — utiliser la task adversariale.
**Input** : diff uniquement. Aucun contexte, aucune spec, aucun accès projet.

> Correspond à `_bmad/core/tasks/review-adversarial-general.xml` — review cynique à l'aveugle.

#### Couche 2 : Edge Case Hunter

Invoquer le skill `grimoire-edge-case-hunter`.
**Input** : diff + accès lecture au projet.

#### Couche 3 : Acceptance Auditor (seulement si `review_mode = "full"`)

**Input** : diff + contenu de la spec + docs de contexte chargés.

> Tu es un Acceptance Auditor. Review ce diff par rapport à la spec et aux docs de contexte.
> Vérifier : violations des critères d'acceptation, déviations de l'intention de la spec,
> comportements spécifiés non implémentés, contradictions entre contraintes et code.
> Output : liste Markdown. Chaque finding = titre, quel AC/contrainte est violé, preuve du diff.

#### Gestion des échecs

Si une couche échoue, timeout, ou retourne un résultat vide → noter la couche en échec et continuer avec les findings des autres couches.

### Step 3 — Triage

#### 3.1 Normaliser

Convertir tous les findings en format unifié :

| Champ | Description |
|---|---|
| `id` | Entier séquentiel |
| `source` | `blind`, `edge`, `auditor`, ou fusionné (ex: `blind+edge`) |
| `title` | Résumé une ligne |
| `detail` | Description complète |
| `location` | Fichier et ligne (si disponible) |

#### 3.2 Dédupliquer

Si deux findings décrivent le même problème → fusionner :
- Garder le plus spécifique comme base (préférer le JSON edge-case avec location)
- Ajouter les détails uniques des autres
- Combiner les sources (ex: `blind+edge`)

#### 3.3 Classifier

Chaque finding dans exactement un bucket :

| Bucket | Description |
|---|---|
| **decision_needed** | Choix ambigu nécessitant input humain (seulement si `full` mode) |
| **patch** | Problème fixable sans ambiguïté |
| **defer** | Problème pré-existant, pas causé par le changement actuel |
| **dismiss** | Bruit, faux positif, ou géré ailleurs |

En mode `no-spec` : reclassifier `decision_needed` → `patch` (si fix clair) ou `defer` (sinon).

#### 3.4 Nettoyer

Supprimer tous les `dismiss`. Compter pour le résumé.

Si zéro findings restent ET aucune couche n'a échoué → "✅ Review propre — toutes les couches passées."
Si zéro findings restent MAIS des couches ont échoué → avertir que la review peut être incomplète.

### Step 4 — Présenter et agir

#### 4.1 Résumé

> **Code review terminée.** D `decision-needed`, P `patch`, W `defer`, R rejetés.

#### 4.2 Résoudre les `decision_needed`

Présenter chaque finding avec options. L'utilisateur doit décider.
**HALT** — attendre la décision avant de continuer.

#### 4.3 Traiter les `patch`

Proposer :

> 1. **Appliquer les fixes** — je corrige tout maintenant
> 2. **Fix sélectif** — choisir lesquels corriger
> 3. **Reporter** — noter pour plus tard

**HALT** — attendre le choix.

Si l'utilisateur choisit 1 ou 2, appliquer les corrections, puis re-vérifier chaque fix.

#### 4.4 Findings `defer`

Lister les findings différés avec une description courte. Proposer de les ajouter à un fichier de suivi.

## Notes d'intégration

- Ce skill combine `review-adversarial-general.xml` existant avec l'Edge Case Hunter
- La couche Acceptance Auditor est uniquement active quand une spec est fournie
- Compatible avec l'architecture SOG : l'orchestrateur peut invoquer ce skill directement
