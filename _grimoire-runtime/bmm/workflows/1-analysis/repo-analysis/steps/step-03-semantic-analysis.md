# Step 03 — Analyse sémantique

## MANDATORY EXECUTION RULES (READ FIRST):

- 📖 CRITICAL: Lire ce fichier EN ENTIER avant toute action
- 🛑 OBJECTIF : Analyser la logique métier, la qualité du code et les risques sémantiques
- 🔒 RAPPEL OBJECTIF GLOBAL : `{analysis_objective}` — ne pas dériver
- 🔒 GROUNDING OBLIGATOIRE : chaque claim sur la logique métier doit citer un fichier et une ligne
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`

## EXECUTION PROTOCOLS:

- Commencer par l'accusé de réception
- Lire les fichiers métier identifiés en step-01 et step-02
- Si le contexte devient trop large : prioriser par risque (high → medium → low)
- Mettre à jour la fiche contextuelle après chaque section
- Attendre [C] avant de passer à step-04

## CONTEXT BOUNDARIES:

**ZONE 1 — CRITIQUE** :
```
OBJECTIF : Analyser la logique métier et la qualité sémantique de {repo_name}
CONTRAINTE ABSOLUE : Ne pas dériver de l'objectif "{analysis_objective}". Chaque affirmation = source fichier + ligne.
FORMAT DE SORTIE : Rapport sémantique avec priorisation par risque
RAPPEL : L'objectif global est "{analysis_objective}", pas une review générique
```

## ACCUSÉ DE RÉCEPTION OBLIGATOIRE:

```
✅ COMPRIS :
- Objectif : [reformulation en 1 phrase]
- Contrainte : rester aligné sur "{analysis_objective}" + sources fichiers
- Je vais commencer par lire : [3-5 fichiers métier prioritaires]
```

## YOUR TASK:

### 1. Analyse de la logique métier

En lisant les fichiers clés (step-01), identifier les domaines métier :

Pour chaque domaine identifié :
```
Domaine : {domain_name} (source: {file}:{line})
- Responsabilité : {description}
- Complexité : {simple|moderate|complex}
- Points d'entrée : {entry_points}
- Points de sortie : {exit_points}
```

### 2. Analyse de la qualité du code

Lire les fichiers à risque identifiés en step-02, puis :

**Lisibilité** :
- Nommage : {clear|mixed|obscure} (exemples dans {file}:{line})
- Complexité cyclomatique apparente : {low|medium|high} (pire cas : {file}:{line})

**Testabilité** :
- Code testé : {yes|partial|no} (source: {test_files})
- Mocking/isolation : {present|absent} (source: {file}:{line})

**Maintenabilité** :
- Duplication détectée : {none|low|high} (exemple : {file}:{line} dupliqué dans {file2}:{line2})
- Complexité des changements apparente : {low|medium|high}

### 3. Identification des anti-patterns

Chercher et signaler avec preuve :

| Anti-pattern | Fichier | Ligne | Impact |
|---|---|---|---|
| {pattern_name} | {file} | {line} | {description} |

Anti-patterns à cibler :
- Logique métier dans les controllers/routes
- Side effects cachés dans des getters/pure functions
- Gestion d'erreur silencieuse (`catch {}`, `except: pass`)
- Validation absente sur des données d'entrée critiques
- Race conditions potentielles dans du code concurrent
- Couplage fort vers des services externes sans abstraction

### 4. Évaluation du drift par rapport à l'objectif

⚠️ Gate anti-drift : vérifier que l'analyse reste alignée sur `{analysis_objective}`.

Répondre explicitement :
> "L'analyse couvre-t-elle bien l'objectif '{analysis_objective}' ? OUI / NON + explication"

Si NON : recentrer sur les fichiers directement liés à l'objectif.

### 5. Mettre à jour la fiche contextuelle

Mettre à jour `_memory/repo-contexts/{repo_name}.md` — section "Résultats de l'analyse sémantique" :

```markdown
## Résultats de l'analyse sémantique

**Domaines métier identifiés** : {count}
**Qualité globale** : {low|medium|high}
**Anti-patterns** : {N} ({critical_count} critiques)
**Alignement objectif** : {aligned|partial|misaligned}
**Questions ouvertes** : {questions_list}
```

### 6. Présenter le résumé sémantique

> "**Analyse sémantique terminée ✅**
>
> Domaines métier : {N}
> Qualité : {level}
> Anti-patterns : {N}
> Alignement objectif : {status}
>
> [C] Continuer vers la cross-validation CVTL"

## SUCCESS METRICS:

✅ Domaines métier identifiés avec sources
✅ Anti-patterns listés avec fichiers et lignes
✅ Gate anti-drift explicitement vérifiée
✅ Fiche contextuelle mise à jour
✅ [C] continue présenté

## FAILURE MODES:

❌ Faire une review générique sans lien avec l'objectif spécifique
❌ Anti-patterns listés sans preuve fichier
❌ Dériver vers des sujets non demandés dans l'objectif
❌ Ne pas mettre à jour les questions ouvertes dans la fiche

## NEXT STEP:

Après [C] : charger `{project-root}/_grimoire-runtime/bmm/workflows/1-analysis/repo-analysis/steps/step-04-cross-validation.md`
