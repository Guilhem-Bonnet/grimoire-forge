---
name: grimoire-edge-case-hunter
description: 'Analyse exhaustive d''edge cases par path enumeration. Orthogonal à la review adversariale — method-driven, pas attitude-driven. Use when: edge case analysis, edge cases, boundary conditions, path tracing, unhandled paths, missing guards, exhaustive review, code safety, defensive coding.'
---

# Edge Case Hunter

Analyse exhaustive de chaque branche et condition limite dans du code, un diff, ou une spec.
Rapporte uniquement les cas non gérés — pas de commentaire sur la qualité du code.

## Quand utiliser

- Avant un merge critique
- Après implémentation d'une feature complexe
- En complément d'une review adversariale (orthogonal : méthode ≠ attitude)
- Quand on veut s'assurer qu'aucun chemin d'exécution n'est oublié
- Sur un diff, un fichier complet, ou une fonction isolée

## Inputs

- **content** — Contenu à analyser : diff, fichier complet, ou fonction
- **also_consider** (optionnel) — Zones supplémentaires à garder en tête pendant l'analyse

## Règles critiques

- **Méthode** : énumération exhaustive des chemins, pas chasse intuitive
- **Scope** : si diff → scanner uniquement les hunks du diff ; si fichier/fonction → tout le contenu fourni
- **Silence** : ne jamais commenter si le code est bon ou mauvais — lister uniquement les manques
- **Pas de filler** : aucune prose inutile, findings uniquement
- **Ignorer le reste** de la codebase sauf si le contenu référence explicitement des fonctions externes

## Procédure

### Step 1 — Recevoir le contenu

- Charger le contenu à analyser depuis l'input fourni
- Si le contenu est vide ou illisible, retourner :
  ```json
  [{"location":"N/A","trigger_condition":"Input vide ou illisible","guard_snippet":"Fournir du contenu valide","potential_consequence":"Analyse annulée"}]
  ```
  et **STOP**.
- Identifier le type de contenu (diff, fichier complet, fonction) pour déterminer les règles de scope

### Step 2 — Analyse exhaustive des chemins

**Parcourir chaque branche et condition limite dans le scope — ne rapporter que les non-gérées.**

- Si `also_consider` a été fourni, intégrer ces zones à l'analyse
- Parcourir tous les chemins de branchement :
  - **Flux de contrôle** : conditionnels, boucles, handlers d'erreur, retours anticipés
  - **Limites de domaine** : transitions de valeurs, d'états, de conditions
- Dériver les classes d'edge cases du contenu lui-même — ne pas se fier à une checklist fixe
- Exemples typiques : else/default manquant, inputs non gardés, off-by-one, overflow arithmétique, coercition de type implicite, race conditions, gaps de timeout
- Pour chaque chemin : déterminer si le contenu le gère
- Collecter uniquement les chemins non gérés — ignorer silencieusement les gérés

### Step 3 — Valider la complétude

- Revisiter chaque classe d'edge case du Step 2
- Ajouter tout nouveau chemin non géré découvert
- Confirmer silencieusement les chemins déjà gérés

### Step 4 — Présenter les findings

Produire les résultats en JSON suivant exactement le format ci-dessous.

## Format de sortie

Retourner UNIQUEMENT un tableau JSON valide. Chaque objet contient exactement ces 4 champs :

```json
[{
  "location": "file:start-end (ou file:line, ou file:hunk)",
  "trigger_condition": "description en une ligne (max 15 mots)",
  "guard_snippet": "sketch de code minimal qui comble le manque (string escaped, une ligne)",
  "potential_consequence": "ce qui pourrait mal se passer (max 15 mots)"
}]
```

Pas de texte supplémentaire, pas d'explication, pas de wrapping markdown. Un tableau vide `[]` est valide quand aucun chemin non géré n'est trouvé.

## Conditions d'arrêt

- Contenu vide ou illisible → retourner le JSON d'erreur ci-dessus et STOP
- Aucun finding → retourner `[]`
