# Step 00 — Initialisation du contexte repo

## MANDATORY EXECUTION RULES (READ FIRST):

- 📖 CRITICAL: Lire ce fichier EN ENTIER avant toute action
- 🛑 OBJECTIF DE CE STEP : Créer une fiche contextuelle isolée pour ce repo — aucune analyse de contenu ici
- 🔒 ISOLATION STRICTE : le contexte de ce repo NE DOIT PAS être mélangé avec un repo précédemment analysé
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`

## EXECUTION PROTOCOLS:

- Créer la fiche contexte AVANT toute autre action
- Présenter un résumé des paramètres capturés
- Attendre confirmation [C] avant de passer à step-01
- ⚠️ Si une fiche existe déjà pour ce repo, la lire et demander si c'est une reprise ou une nouvelle analyse

## CONTEXT BOUNDARIES:

- Repo à analyser : `{repo_name}` @ `{repo_path}`
- Objectif global déclaré par l'utilisateur : `{analysis_objective}`
- Ce step ne lit PAS le contenu du repo — uniquement sa métadonnée (chemin, existence, type)

## YOUR TASK:

### 1. Vérifier l'existence de la fiche

Vérifier si `{project-root}/_grimoire-runtime/_memory/repo-contexts/{repo_name}.md` existe.

- **Si elle existe** : lire son contenu et présenter à l'utilisateur :
  > "Une analyse précédente de `{repo_name}` existe (date: {previous_date}). Voulez-vous reprendre cette analyse ou en commencer une nouvelle ? [R] Reprendre | [N] Nouvelle analyse"
  
  - [R] → charger le contexte existant, passer à step-01
  - [N] → archiver l'ancienne fiche sous `{repo_name}-{date}.md.bak`, créer une nouvelle

- **Si elle n'existe pas** : créer la fiche (voir ci-dessous)

### 1b. Initialiser l'état self-piloting

**Avant de créer la fiche**, enregistrer l'état initial :
```bash
bash {project-root}/grimoire-kit/framework/tools/repo-analysis-state.sh write \
  --step 0 --repo "{repo_name}" --status in_progress \
  --objective "{analysis_objective}" \
  --project-root {project-root}
```

### 2. Créer la fiche de contexte repo

Créer `{project-root}/_grimoire-runtime/_memory/repo-contexts/{repo_name}.md` avec le contenu suivant :

```markdown
---
repo: {repo_name}
path: {repo_path}
analysis_objective: {analysis_objective}
started: {date}
status: in_progress
---

# Contexte — {repo_name}

## Objectif de l'analyse

{analysis_objective}

## Structure du repo

> À remplir par step-01 (grounding)

## Patterns identifiés

> À remplir par step-02

## Résultats de l'analyse sémantique

> À remplir par step-03

## Résultats de la validation croisée

> À remplir par step-04

## Points de l'adversarial review

> À remplir par step-05

## Questions ouvertes

- [ ] (remplir au fil des steps)

## Décisions et conclusions

> À remplir par step-06
```

### 2b. Confirmer l'état initial

```bash
bash {project-root}/grimoire-kit/framework/tools/repo-analysis-state.sh write \
  --step 0 --repo "{repo_name}" --status completed \
  --objective "{analysis_objective}" \
  --project-root {project-root}
```

### 3. Présenter le résumé d'initialisation

> "**Contexte repo initialisé ✅**
>
> - Repo : `{repo_name}`
> - Chemin : `{repo_path}`
> - Objectif : {analysis_objective}
> - Fiche créée : `_grimoire-runtime/_memory/repo-contexts/{repo_name}.md`
>
> [C] Continuer vers le grounding (lecture structure réelle)"

## SUCCESS METRICS:

✅ Fiche contextuelle créée et isolée du contexte global
✅ Objectif de l'analyse capturé et stocké
✅ Aucun contenu du repo analysé à ce stade
✅ [C] continue présenté et géré correctement
✅ Reprises correctement détectées et proposées

## FAILURE MODES:

❌ Commencer à analyser le contenu du repo dans ce step
❌ Ne pas créer la fiche de contexte avant de continuer
❌ Laisser un contexte de repo précédent actif (contamination inter-repos)
❌ Oublier de capturer l'objectif global dans la fiche

## NEXT STEP:

Après [C] : charger `{project-root}/_grimoire-runtime/bmm/workflows/1-analysis/repo-analysis/steps/step-01-grounding.md`
