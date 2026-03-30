---
name: grimoire-distillator
description: 'Compression lossless de documents optimisée LLM. Produit des distillats hyper-compréssés preservant chaque fait, décision et contrainte. Use when: distill documents, compress docs, create distillate, optimize context, reduce tokens, document compression, context optimization, LLM-optimized docs.'
argument-hint: '[source paths] [--validate distillate-path] [--budget N tokens] [--consumer workflow-name]'
---

# Grimoire Distillator

Compression lossless de documents source en distillats hyper-compressés, optimisés pour consommation LLM.

## Principe

Ceci est une tâche de **compression**, pas de résumé. Les résumés sont lossy. Les distillats sont une compression lossless optimisée pour la consommation LLM : chaque fait, décision, contrainte et relation est préservé, mais tout l'overhead humain (prose, répétitions, formatage décoratif) est éliminé.

## Quand utiliser

- Préparer du contexte pour un workflow downstream (ex: création de PRD, architecture)
- Réduire un corpus de docs trop volumineux pour la fenêtre de contexte
- Créer un snapshot compressé d'artefacts de planification
- Optimiser le ratio signal/bruit d'un ensemble de documents

## Inputs

| Input | Requis | Description |
|---|---|---|
| `source_documents` | Oui | Chemins de fichiers, dossiers, ou globs à distiller |
| `downstream_consumer` | Non | Quel workflow/agent consomme ce distillat (guide le filtrage signal/bruit) |
| `token_budget` | Non | Taille cible approximative. Si dépassée → split sémantique |
| `output_path` | Non | Où sauvegarder. Par défaut : adjacent au document principal avec `-distillate.md` |
| `--validate` | Non | Flag : lancer un test de reconstruction round-trip après production |

## Procédure

### Step 1 — Analyser les sources

1. Lister et lire tous les fichiers source
2. Pour chaque fichier, extraire :
   - Nombre de tokens estimé
   - Structure (headings, sections)
   - Entités nommées (projets, technologies, décisions, contraintes)
   - Densité informationnelle (ratio contenu factuel / prose)
3. Déterminer le routage :
   - **Single mode** : ≤ 3 fichiers ET ≤ 15K tokens estimés → traitement direct
   - **Fan-out mode** : > 3 fichiers OU > 15K tokens → groupement thématique + traitement par groupe

### Step 2 — Compresser

#### Règles de compression

1. **Préserver** : chaque fait, décision, contrainte, relation, dépendance, métrique, date
2. **Éliminer** : prose introductive, transitions, reformulations, exemples redondants, formatage décoratif
3. **Restructurer** : regrouper par thème, pas par document source
4. **Notation dense** :
   - Utiliser `:` et `→` au lieu de phrases complètes
   - Listes avec tirets, pas de paragraphes
   - Abréviations cohérentes (définir en en-tête)
   - Tables pour les données tabulaires
5. **Traçabilité** : chaque section du distillat doit indiquer son/ses document(s) source

#### Mode Single

Traiter tous les fichiers ensemble. Produire un seul distillat.

#### Mode Fan-Out

1. Traiter chaque groupe thématique séparément → distillat intermédiaire par groupe
2. Fusionner les distillats intermédiaires :
   - Dédupliquer cross-groupe
   - Regrouper thématiquement
   - Compression finale
3. Les distillats intermédiaires ne sont pas sauvegardés

### Step 3 — Vérifier et sauvegarder

1. **Check de complétude** : vérifier que chaque heading source a un correspondant dans le distillat
2. **Check de format** : valider que le distillat est markdown valide et lisible
3. **Générer l'en-tête** :
   ```markdown
   <!-- DISTILLATE
   sources: [liste des fichiers source]
   tokens_original: N
   tokens_distilled: N
   ratio: X.Xx
   created: YYYY-MM-DD
   consumer: {downstream_consumer ou "general"}
   -->
   ```
4. Sauvegarder à `output_path` ou `{source-principal}-distillate.md`

### Step 4 — Validation round-trip (si `--validate`)

1. À partir du distillat seul (sans accès aux sources), tenter de reconstruire les points clés de chaque document source
2. Comparer avec les originaux
3. Rapporter :
   - **Préservé** : informations retrouvées fidèlement
   - **Dégradé** : informations présentes mais avec perte de nuance
   - **Manquant** : informations absentes du distillat
4. Si des éléments sont manquants → proposer un patch au distillat

## Format de sortie

Le distillat utilise une notation dense. Exemple :

```markdown
<!-- DISTILLATE
sources: [docs/architecture.md, docs/prd.md]
tokens_original: 8420
tokens_distilled: 2105
ratio: 4.0x
created: 2026-03-23
consumer: architecture-review
-->

# Distillat : Projet Grimoire

## Abréviations
- GK: Grimoire Kit | SOG: Smart Orchestrator Gateway | UDF: Unified Dynamic Factory

## Architecture
- Stack: Python 3.12+ / VS Code Copilot agents / Markdown-as-protocol
- Modules: BMM (method) · BMB (builders) · CIS (creativity) · TEA (testing)
- Dispatch: SOG → sub-agents invisibles → résultat agrégé
- Anti-hallucination: HUP vérifie chaque output sub-agent

## Décisions (ADR)
- ADR-001: Markdown > YAML pour workflows → lisibilité LLM
- ADR-002: Stigmergie > messages directs → coordination émergente
```

## Intégration Grimoire

- Utile avant d'invoquer des workflows lourds (PRD, architecture, brainstorming)
- Les distillats peuvent être chaînés : distiller les outputs de planning → input pour implementation
- Compatible avec le context-summarizer existant (`framework/tools/context-summarizer.py`) mais opère à un niveau de granularité supérieur (documents entiers vs sections)
