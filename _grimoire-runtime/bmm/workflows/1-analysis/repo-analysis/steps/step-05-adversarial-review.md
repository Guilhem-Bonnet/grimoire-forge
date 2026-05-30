# Step 05 — Adversarial Review (gate automatique)

## MANDATORY EXECUTION RULES (READ FIRST):

- 📖 CRITICAL: Lire ce fichier EN ENTIER avant toute action
- 🛑 OBJECTIF : Jouer le rôle d'un critique cynique et chercher ce que les analyses précédentes ont raté
- 🔒 GATE BLOQUANTE : Si 0 finding → HALT et re-analyser (résultat suspect)
- 🔒 L'OBJECTIF INITIAL EST LA BOUSSOLE : tout finding doit être pertinent par rapport à `{analysis_objective}`
- ⚡ Mode : critique destructif mais constructif — le but est de trouver des problèmes, pas de valider
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`

## EXECUTION PROTOCOLS:

- Prendre la posture d'un reviewer adversarial : assumer que des problèmes existent et les trouver
- Trouver au minimum 5 points d'amélioration ou de risque non couverts
- Si 0 finding : HALT — "Ce résultat est suspect, je vais re-analyser avec plus de profondeur"
- Chaque finding DOIT être lié à l'objectif `{analysis_objective}`
- Attendre [C] avant de passer à step-06

## CONTEXT BOUNDARIES:

**ZONE 1 — CRITIQUE** :
```
OBJECTIF : Trouver ce que les analyses de {repo_name} ont raté ou sous-estimé
CONTRAINTE ABSOLUE : Minimum 5 findings. Zero finding = résultat invalide, re-analyser.
FORMAT DE SORTIE : Liste de findings avec sévérité, preuve, et recommandation
RAPPEL OBJECTIF GLOBAL : {analysis_objective} — tout finding hors-scope est ignoré
```

## ACCUSÉ DE RÉCEPTION OBLIGATOIRE:

```
✅ COMPRIS :
- Objectif : trouver les failles des analyses précédentes de {repo_name}
- Contrainte : minimum 5 findings liés à "{analysis_objective}"
- Je vais challenger : [3 affirmations des steps précédents que je vais questionner en premier]
```

## YOUR TASK:

### 1. Relire la fiche contextuelle en mode critique

Charger `{project-root}/_grimoire-runtime/_memory/repo-contexts/{repo_name}.md`.

En lisant chaque section, noter mentalement :
- Ce qui semble trop optimiste
- Ce qui manque
- Ce qui est sous-estimé
- Ce qui est hors du scope de `{analysis_objective}`

### 2. Challenger les conclusions structurelles (step-02)

Pour les 3 affirmations architecturales les plus importantes :

```
CHALLENGE : "{claim_from_step02}"
Question critique : {challenging_question}
Contre-hypothèse : {alternative_interpretation}
Vérification : {file_to_read_for_evidence}
Verdict : TIENT | FRAGILE | FAUX
```

### 3. Chercher les angles morts

Chercher ce qui n'a PAS été analysé mais qui est pertinent pour `{analysis_objective}` :

**Questions adversariales** :
- Le pire scénario de déploiement de ce repo a-t-il été considéré ?
- Les edge cases des domaines métier identifiés ont-ils été couverts ?
- Les dépendances à risque ont-elles été vérifiées pour des CVEs récents ?
- Le test coverage réel (pas apparent) a-t-il été mesuré ?
- Les configurations d'environnement (prod vs dev) ont-elles été comparées ?
- La sécurité des points d'entrée a-t-elle été évaluée ?

### 4. Produire la liste des findings adversariaux

Format pour chaque finding :

```
Finding #{N}
Sévérité : LOW | MEDIUM | HIGH | CRITICAL
Titre : {short_title}
Description : {what_was_missed_or_underestimated}
Source : {file}:{line} (si applicable)
Lien à l'objectif : {how_it_relates_to_analysis_objective}
Recommandation : {concrete_action}
```

**Seuils minimaux** :
- ≥ 1 finding CRITICAL ou HIGH
- ≥ 3 findings MEDIUM
- Total ≥ 5 findings

Si < 5 findings trouvés → HALT et re-analyser avec profondeur accrue.

### 5. Gate de cohérence avec l'objectif

Pour chaque finding, vérifier : est-il pertinent pour `{analysis_objective}` ?

- Oui → conserver
- Non → annoter comme "hors-scope" (informatif uniquement, pas bloquant)

### 6. Mettre à jour la fiche contextuelle

```markdown
## Points de l'adversarial review

**Findings totaux** : {count} ({critical} critiques, {high} hauts, {medium} moyens, {low} bas)
**Angles morts identifiés** : {list}
**Recommandations prioritaires** :
1. {top_recommendation}
2. {second_recommendation}
3. {third_recommendation}
```

### 7. Présenter le rapport adversarial

> "**Adversarial Review terminée ✅**
>
> {N} findings identifiés ({critical} critiques, {high} hauts)
> Angles morts : {list_summary}
>
> **Top 3 recommandations :**
> 1. {rec1}
> 2. {rec2}
> 3. {rec3}
>
> [C] Continuer vers le résumé canonique"

## SUCCESS METRICS:

✅ Minimum 5 findings produits
✅ Minimum 1 finding HIGH ou CRITICAL
✅ Tous les findings liés à `{analysis_objective}`
✅ Angles morts explicitement identifiés
✅ Fiche contextuelle mise à jour
✅ [C] continue présenté

## FAILURE MODES:

❌ Produire 0 finding (résultat impossible — re-analyser)
❌ Approuver les analyses précédentes sans les challenger
❌ Findings non liés à `{analysis_objective}`
❌ Ne pas lire les fichiers lors du challenge des claims

## HALT CONDITION:

Si 0 finding : "Résultat suspect — il est statistiquement impossible qu'une analyse de repo ne révèle aucun point d'amélioration. Je vais re-analyser avec plus de profondeur." → Recommencer step-05 en ciblant les fichiers les plus complexes.

## NEXT STEP:

Après [C] : charger `{project-root}/_grimoire-runtime/bmm/workflows/1-analysis/repo-analysis/steps/step-06-canonical-summary.md`
