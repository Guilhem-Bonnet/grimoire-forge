# Step 06 — Résumé canonique + fermeture du contexte

## MANDATORY EXECUTION RULES (READ FIRST):

- 📖 CRITICAL: Lire ce fichier EN ENTIER avant toute action
- 🛑 OBJECTIF : Produire le résumé canonique de l'analyse et fermer proprement le contexte repo
- 🔒 LE RÉSUMÉ EST L'INPUT DU PROCHAIN REPO : il doit être complet et auto-suffisant
- 🔒 CLORE LE CONTEXTE : après ce step, aucun élément de ce repo ne doit persister en contexte actif
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`

## EXECUTION PROTOCOLS:

- Agréger les résultats des steps 02, 03, 04, 05 depuis la fiche contextuelle
- Produire un résumé canonique auto-suffisant (lisible sans la conversation)
- Fermer le contexte repo (marquer la fiche comme `status: completed`)
- Demander confirmation avant de fermer

## CONTEXT BOUNDARIES:

**ZONE 1 — CRITIQUE** :
```
OBJECTIF : Synthétiser l'analyse de {repo_name} en un résumé canonique exploitable
CONTRAINTE ABSOLUE : Le résumé doit répondre à "{analysis_objective}" — pas une liste exhaustive
FORMAT DE SORTIE : Document Markdown auto-suffisant + fiche contextuelle fermée
```

## YOUR TASK:

### 1. Relire la fiche contextuelle complète

Charger `{project-root}/_grimoire-runtime/_memory/repo-contexts/{repo_name}.md` en entier.

Identifier :
- Les conclusions validées par CVTL (step-04)
- Les findings adversariaux (step-05)
- Les questions ouvertes non résolues
- Les recommandations prioritaires

### 2. Produire le résumé canonique

Créer le fichier de sortie :
`{project-root}/_grimoire-runtime-output/planning-artifacts/repo-analysis/{repo_name}-analysis-{date}.md`

Structure du résumé :

```markdown
---
repo: {repo_name}
analysis_objective: {analysis_objective}
date: {date}
verdict: {overall_verdict}
confidence: {high|medium|low}
---

# Analyse de {repo_name}

## Réponse à l'objectif

> "{analysis_objective}"

{direct_answer_in_2_3_paragraphs}

## Résumé exécutif

| Dimension | Résultat | Confiance |
|---|---|---|
| Architecture | {type} | {high|med|low} |
| Qualité structurelle | {level} | {high|med|low} |
| Qualité sémantique | {level} | {high|med|low} |
| Risques identifiés | {N} ({critical} critiques) | {high|med|low} |
| Dette technique | {level} | {high|med|low} |

## Findings critiques et hauts

{findings_high_and_critical_from_step05}

## Recommandations prioritaires

1. **{rec1}** — {justification} (source: {file})
2. **{rec2}** — {justification} (source: {file})
3. **{rec3}** — {justification} (source: {file})

## Questions ouvertes

{open_questions_not_resolved}

## Sources de vérité (grounding)

Toutes les affirmations de ce rapport sont basées sur une lecture directe des fichiers suivants :
{key_files_read_with_purpose}
```

### 3. Indicateur de confiance global

Calculer la confiance de l'analyse :

**HIGH** : CVTL PASS + ≥ 5 findings adversariaux + 0 hallucination + alignement complet
**MEDIUM** : CVTL PARTIAL + ≥ 3 findings + 0 hallucination critique
**LOW** : CVTL FAIL OU ≥ 1 hallucination critique OU alignement manquant

Annoter le résumé avec la confiance et ses raisons.

### 4. Fermer l'état self-piloting

```bash
bash {project-root}/grimoire-kit/framework/tools/repo-analysis-state.sh write \
  --step 6 --repo "{repo_name}" --status completed \
  --objective "{analysis_objective}" \
  --project-root {project-root}
```

### 5. Fermer le contexte repo

Mettre à jour `_memory/repo-contexts/{repo_name}.md` :

```markdown
---
status: completed
completed: {date}
summary_path: {path_to_canonical_summary}
---
```

Ajouter dans la section "Décisions et conclusions" :
```markdown
## Décisions et conclusions

**Confiance globale** : {level}
**Résumé canonique** : [{repo_name}-analysis-{date}.md]({path})
**Analyse terminée le** : {date}
```

### 6. Confirmation de fermeture

> "**Analyse de `{repo_name}` terminée ✅**
>
> Résumé canonique : `{output_path}`
> Confiance : {level}
> Réponse à l'objectif : {brief_answer}
>
> ⚠️ Le contexte de ce repo est maintenant fermé. Le prochain repo sera analysé avec un contexte vierge.
>
> [N] Analyser un autre repo | [V] Voir le résumé | [Q] Terminer"

## SUCCESS METRICS:

✅ Résumé canonique auto-suffisant produit
✅ Réponse directe à `{analysis_objective}` dans le résumé
✅ Confiance calculée et justifiée
✅ Fiche contextuelle marquée `completed`
✅ Contexte repo fermé pour éviter la contamination

## FAILURE MODES:

❌ Résumé qui ne répond pas à `{analysis_objective}`
❌ Résumé qui nécessite de lire la conversation pour être compris
❌ Fiche contextuelle non fermée (risque de contamination inter-repos)
❌ Confiance non calculée ou non justifiée

## WORKFLOW TERMINÉ

Ce step est le dernier du workflow `repo-analysis`.
Pour analyser un autre repo, recharger `workflow-repo-analysis.md` avec un nouveau `{repo_name}` et un nouveau `{analysis_objective}`.
