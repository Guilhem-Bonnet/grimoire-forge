---
name: repo-analysis
description: 'Analyse approfondie d''un repo avec anti-hallucination, anti-drift et isolation contextuelle. Use when the user says "analyse ce repo", "audit ce codebase", "analyse [repo_name]", or "review ce repo".'
status: Stable
owner: analyst
---

# Workflow — Analyse de Repo

**Objectif :** Analyser un repo en compensant systématiquement les défauts LLM (hallucination, drift, perte de contexte, lecture partielle).

**Garanties de ce workflow :**
- 🔒 **Anti-hallucination** : grounding obligatoire — chaque affirmation sourcée par un fichier réel
- 🔒 **Anti-drift** : objectif ancré dans chaque step + gate adversariale
- 🔒 **Anti-perte de contexte** : isolation contextuelle par repo, résumé canonique
- 🔒 **Anti-truncation** : structure ZONE 1/2/3 + accusé de réception obligatoire

---

## PREREQUISITE

**⛔ Accès au repo requis.** Si le repo n'est pas accessible, abort et expliquer à l'utilisateur comment le rendre accessible.

## CONFIGURATION

Charger `{project-root}/_grimoire-runtime/bmm/config.yaml` et résoudre :
- `user_name`, `output_folder`, `planning_artifacts`
- `communication_language`, `document_output_language`
- `date` comme valeur générée par le système

## DISCOVERY — Capturer les paramètres de l'analyse

Accueillir l'utilisateur et capturer les informations nécessaires :

> "Bonjour {user_name} ! Lançons l'**analyse de repo**.
>
> **Quel repo souhaitez-vous analyser ?**
> (chemin local, URL Git, ou nom si dans le workspace courant)"

### Clarification en 3 questions max

1. **Repo** : "Quel est le chemin ou l'URL du repo ?" (si pas déjà fourni)
2. **Objectif** : "Quel est l'objectif précis de cette analyse ?" — donner des exemples :
   - "Évaluer la qualité pour une reprise de code"
   - "Identifier les risques avant une migration"
   - "Comprendre l'architecture pour y contribuer"
   - "Audit de sécurité"
   - "Autre : [préciser]"
3. **Périmètre** (optionnel) : "Y a-t-il des parties à exclure ou à prioriser ?"

### Paramètres capturés

Après la discovery, déclarer en session :
- `{repo_name}` = nom court du repo
- `{repo_path}` = chemin absolu ou URL
- `{analysis_objective}` = objectif précis capturé
- `{scope_exclusions}` = périmètre exclu (si applicable)

## VÉRIFICATION DE REPRISE (SELF-PILOTING)

**Avant toute chose**, vérifier si une analyse est déjà en cours :

```bash
bash {project-root}/grimoire-kit/framework/tools/repo-analysis-state.sh read \
  --project-root {project-root}
```

- Si `status == "in_progress"` et `repo` est non vide :
  > "Une analyse de `{repo}` est en cours au step {step} (objectif : {objective}). [R] Reprendre à ce step | [N] Nouvelle analyse"
  - [R] → charger directement le step correspondant avec le contexte existant
  - [N] → effacer l'état (`state.sh clear`) et continuer normalement

- Si `status == "not_started"` ou fichier absent → continuer normalement

## ROUTING VERS LES STEPS

Une fois les paramètres capturés :

1. Déclarer : `workflow = "repo-analysis"`
2. Déclarer : `routing_profile = "deep_reasoning"` (CVTL requis — voir model-routing.yaml)
3. Créer le répertoire de sortie : `{planning_artifacts}/repo-analysis/`
4. Charger : `./steps/step-00-context-init.md`

**Ordre des steps (JIT — charger un step à la fois) :**

| Step | Fichier | Défaut compensé | Gate |
|---|---|---|---|
| 00 | `step-00-context-init.md` | Perte de contexte inter-repos | Non |
| 01 | `step-01-grounding.md` | Hallucination | Non |
| 02 | `step-02-structural-analysis.md` | Hallucination, drift | Non |
| 03 | `step-03-semantic-analysis.md` | Drift, lecture partielle | Non |
| 04 | `step-04-cross-validation.md` | Hallucination | ✅ BLOQUANTE |
| 05 | `step-05-adversarial-review.md` | Drift | ✅ BLOQUANTE (min 5 findings) |
| 06 | `step-06-canonical-summary.md` | Perte de contexte | Non |

**Règles d'exécution :**
- Charger chaque step JIT (pas plusieurs en avance)
- Ne pas passer un step si sa gate est bloquante et non résolue
- L'utilisateur peut demander [S] Skip sur les steps non-bloquants uniquement

## TOKEN BUDGET (intégration preflight)

Avant step-01, évaluer le budget token estimé :

- Repo < 100 fichiers → budget normal
- Repo 100-500 fichiers → activer la priorisation par risque dans step-02 et step-03
- Repo > 500 fichiers → activer le mode stratifié : analyser uniquement les fichiers HIGH risk identifiés en step-01

Déclarer `{token_budget_mode}` = `normal | prioritized | stratified`

## MULTI-REPO MODE

Si l'utilisateur veut analyser plusieurs repos en série :

1. Terminer le repo courant jusqu'à step-06
2. step-06 fermera le contexte du repo courant
3. Recharger ce workflow (`workflow-repo-analysis.md`) avec le nouveau `{repo_name}`
4. Le contexte du repo précédent sera isolé dans sa fiche `_memory/repo-contexts/`

⚠️ Ne jamais mélanger les contextes de deux repos dans la même session.

## SORTIE FINALE

Après step-06, le résultat est disponible dans :
`{planning_artifacts}/repo-analysis/{repo_name}-analysis-{date}.md`

Ce fichier est auto-suffisant et peut être partagé sans la conversation.

**✅ YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`**
