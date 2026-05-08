# Step 02 — Analyse structurelle

## MANDATORY EXECUTION RULES (READ FIRST):

- 📖 CRITICAL: Lire ce fichier EN ENTIER avant toute action
- 🛑 OBJECTIF : Analyser l'architecture, les dépendances et les patterns structurels du repo
- 🔒 GROUNDING OBLIGATOIRE : Chaque claim architectural DOIT citer un fichier et une ligne. Pas d'inférence.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`

## EXECUTION PROTOCOLS:

- Commencer par l'accusé de réception (voir ci-dessous)
- Lire les fichiers clés identifiés en step-01 avant d'analyser
- Mettre à jour la fiche contextuelle après chaque section
- Attendre [C] avant de passer à step-03

## CONTEXT BOUNDARIES:

**ZONE 1 — CRITIQUE** :
```
OBJECTIF : Analyser l'architecture structurelle de {repo_name}
CONTRAINTE ABSOLUE : Citer fichier + ligne pour chaque affirmation architecturale
FORMAT DE SORTIE : Rapport structurel avec sources de vérité
RAPPEL OBJECTIF GLOBAL : {analysis_objective}
```

Source de vérité disponible depuis step-01 :
- `{file_tree}` — arborescence réelle
- `{key_files_list}` — fichiers clés avec rôles
- `{patterns_from_grounding}` — patterns détectés

## ACCUSÉ DE RÉCEPTION OBLIGATOIRE:

Commencer la réponse par :
```
✅ COMPRIS :
- Objectif : [reformulation en 1 phrase]
- Contrainte : chaque affirmation sera sourcée avec fichier + ligne
- Je vais commencer par lire : [liste des 3-5 premiers fichiers]
```

## YOUR TASK:

### 1. Analyse automatique via code-review.py

**Exécuter en premier** pour obtenir des findings déterministes sans travail LLM :
```bash
python3 {project-root}/grimoire-kit/framework/tools/code-review.py \
  --project-root {repo_path} review --json
```

Le JSON retourné contient :
- `findings` — liste de findings avec `file`, `line`, `severity`, `category`, `message`
- `by_severity` — décompte par sévérité (CRITICAL, HIGH, MEDIUM, LOW)
- `by_category` — décompte par catégorie (SECURITY, TESTS, COMPLEXITY, CONVENTION…)

**Le LLM interprète ce JSON** — il ne scanne pas manuellement les fichiers pour les findings basiques.

Format d'affichage pour chaque finding HIGH/CRITICAL :
```
{severity} [{category}] {file}:{line}
→ {message}
→ Suggestion : {suggestion}
```

### 2. Analyse des dépendances (complément manuel)

Pour les aspects non couverts par code-review.py (architecture, patterns) :
- Lire le fichier de dépendances principal identifié en step-01 (`{key_files_list}`)
- Identifier : versions, dépendances obsolètes (> 2 ans), risques transitifs

Format de sortie pour chaque dépendance notable :
```
{dependency_name} v{version} (source: {file}:{line})
- Usage : {usage}
- Risque : {none|low|medium|high}
```

### 2. Analyse de l'architecture

Lire les fichiers d'architecture identifiés et produire :

**Pattern architectural principal** (source: {file}:{line}) :
- Type : {layered|hexagonal|event-driven|microservices|monolithe|CQRS|autre}
- Justification : {what_in_the_code_proves_it}

**Séparation des responsabilités** :
- Couches identifiées : {layers_list} (source: {file} pour chaque)
- Couplage : {faible|moyen|fort} — preuves : {code_evidence}

**Points d'extension et interfaces** :
- {interface_name} dans {file}:{line} — rôle : {role}

### 3. Analyse des risques structurels

Identifier et signaler :

| Risque | Fichier | Ligne | Sévérité | Justification |
|---|---|---|---|---|
| {risk_type} | {file} | {line} | {low|med|high} | {evidence} |

Types de risques à chercher :
- God objects (classes > 500 lignes avec > 15 méthodes)
- Dépendances circulaires
- Configuration hardcodée (secrets, URLs, ports)
- Absence de gestion d'erreur sur des points critiques
- Dette technique explicite (TODO, FIXME, HACK dans des fichiers critiques)

### 4. Mettre à jour la fiche contextuelle

Mettre à jour `_memory/repo-contexts/{repo_name}.md` — section "Patterns identifiés" :

```markdown
## Patterns identifiés

**Architecture** (source: {file}:{line}) : {type}
**Dépendances** : {count} directes, {risk_count} à risque
**Risques structurels** : {N} identifiés ({high_count} hauts)
**Dette technique** : {level} ({evidence_count} occurrences)
```

### 5. Présenter le résumé structurel

> "**Analyse structurelle terminée ✅**
>
> Architecture : {type} (source: {file})
> Dépendances analysées : {N} ({risks} à risque)
> Risques structurels : {N} ({high_count} hauts)
>
> [C] Continuer vers l'analyse sémantique"

## SUCCESS METRICS:

✅ Toutes les affirmations architecturales sourcées avec fichier + ligne
✅ Risques structurels listés avec preuves
✅ Fiche contextuelle mise à jour
✅ Aucune inférence sans lecture
✅ [C] continue présenté

## FAILURE MODES:

❌ Affirmation architecturale sans source fichier
❌ Évaluer la qualité du code sans lire le code
❌ Inventer des patterns non présents dans les fichiers
❌ Ne pas mettre à jour la fiche contextuelle

## NEXT STEP:

Après [C] : charger `{project-root}/_grimoire-runtime/bmm/workflows/1-analysis/repo-analysis/steps/step-03-semantic-analysis.md`
