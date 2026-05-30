# Step 01 — Grounding obligatoire (anti-hallucination)

## MANDATORY EXECUTION RULES (READ FIRST):

- 📖 CRITICAL: Lire ce fichier EN ENTIER avant toute action
- 🛑 OBJECTIF : Construire la source de vérité locale du repo — ZÉRO affirmation architecturale sans preuve fichier
- 🔒 GROUNDING NON-NÉGOCIABLE : Toute structure, pattern ou convention doit être lue dans un fichier réel. L'inférence sans lecture est interdite.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`

## EXECUTION PROTOCOLS:

- Lire la structure réelle AVANT de faire toute affirmation
- Stocker les résultats dans la fiche repo ET dans la session
- Présenter le résumé du grounding pour validation
- Attendre [C] avant de passer à step-02

## CONTEXT BOUNDARIES:

- Repo : `{repo_name}` @ `{repo_path}`
- Objectif global : `{analysis_objective}` (rappel obligatoire)
- Résultat attendu : source de vérité locale stockée dans `_memory/repo-contexts/{repo_name}.md`

## YOUR TASK:

### ZONE 1 — CRITIQUE (lire et appliquer avant tout)

```
OBJECTIF : Construire la source de vérité locale du repo {repo_name}
CONTRAINTE ABSOLUE : Chaque élément de la source de vérité doit être lu dans un fichier réel — aucune inférence
FORMAT DE SORTIE : Section "Structure du repo" complète dans la fiche contextuelle
```

### 1. Lancer le script de grounding automatique

**Exécuter en premier** :
```bash
bash {project-root}/grimoire-kit/framework/tools/repo-analysis-grounding.sh {repo_path}
```

Ce script retourne un JSON structuré avec :
- `file_tree` — arborescence réelle (≤300 entrées)
- `config_files` — fichiers de config détectés avec leur type
- `entry_points` — points d'entrée détectés
- `test_presence` + `test_framework` — présence et framework de tests
- `ci_config` — fichiers CI/CD
- `estimated_files` — nombre de fichiers total
- `token_budget_mode` — `normal` (<100 fichiers) | `prioritized` (<500) | `stratified` (≥500)

Stocker le résultat JSON dans la variable de session `{grounding_json}`.

Déclarer en session selon le JSON reçu :
- `{file_tree}` = valeur du champ `file_tree`
- `{key_files_list}` = `config_files` + `entry_points` du JSON
- `{patterns_from_grounding}` = types extraits des `config_files`
- `{token_budget_mode}` = valeur du champ `token_budget_mode`

**Écrire l'état self-piloting** :
```bash
bash {project-root}/grimoire-kit/framework/tools/repo-analysis-state.sh write \
  --step 1 --repo "{repo_name}" --status in_progress \
  --objective "{analysis_objective}" \
  --project-root {project-root}
```

### 2. Lire les fichiers clés identifiés par le script

Pour chaque fichier dans `config_files` et `entry_points` du JSON :
- Lire les 60 premières lignes
- Extraire : stack, framework, patterns d'architecture

Lire aussi :
- **README** si présent : en entier
- **Fichiers d'entrée principaux** : 50 premières lignes chacun

### 3. Identifier les fichiers clés

À partir de ce qui a été lu (pas inféré), extraire :

- **Stack technique** : langages, frameworks, outils de build (avec source fichier)
- **Structure d'architecture** : monorepo/microservices/monolithe/lib (avec source fichier)
- **Points d'entrée** : fichiers d'entrée principaux (avec chemin exact)
- **Fichiers à risque** : grande taille, forte complexité apparente (avec chemin exact)
- **Tests** : présence, framework, couverture estimée (avec source fichier)
- **Configuration CI/CD** : pipelines, workflows GitHub Actions, etc. (avec source fichier)

### 3. Stocker dans la fiche contextuelle

Mettre à jour `{project-root}/_grimoire-runtime/_memory/repo-contexts/{repo_name}.md` — section "Structure du repo" :

```markdown
## Structure du repo

**Stack technique** (source: {source_file}):
- Langage principal : {language}
- Framework : {framework}
- Build : {build_tool}

**Architecture** (source: {source_file}):
- Type : {monorepo|microservices|monolithe|lib}
- Points d'entrée : {entry_points}

**Fichiers clés** :
| Fichier | Rôle | Source de vérité |
|---|---|---|
| {path} | {role} | Lu directement |

**Tests** (source: {source_file}):
- Framework : {test_framework}
- Présence : {yes|no|partial}

**CI/CD** (source: {source_file}):
- {ci_cd_details}

**Fichiers à risque identifiés** :
- {path} — {reason}
```

### 4. Écrire l'état final

```bash
bash {project-root}/grimoire-kit/framework/tools/repo-analysis-state.sh write \
  --step 1 --repo "{repo_name}" --status completed \
  --objective "{analysis_objective}" \
  --project-root {project-root}
```

### 5. Présenter le résumé du grounding

> "**Grounding terminé ✅**
>
> Fichiers lus : {N}
> Stack : {stack}
> Architecture : {architecture_type}
> Fichiers clés identifiés : {M}
>
> ⚠️ Toute affirmation dans les steps suivants doit pointer vers un fichier de cette liste.
>
> [C] Continuer vers l'analyse structurelle"

## SUCCESS METRICS:

✅ Tous les éléments structurels prouvés par lecture directe de fichier
✅ Fiche contextuelle mise à jour avec sources de vérité
✅ Variables de session `{file_tree}`, `{key_files_list}`, `{patterns_from_grounding}` déclarées
✅ Aucune inférence sans lecture
✅ [C] continue présenté et géré

## FAILURE MODES:

❌ Faire des affirmations sur l'architecture sans lire de fichier
❌ Utiliser des patterns inférés depuis le nom du repo ou ses dépendances
❌ Ne pas mettre à jour la fiche contextuelle
❌ Oublier de déclarer les variables de session

## NEXT STEP:

Après [C] : charger `{project-root}/_grimoire-runtime/bmm/workflows/1-analysis/repo-analysis/steps/step-02-structural-analysis.md`
