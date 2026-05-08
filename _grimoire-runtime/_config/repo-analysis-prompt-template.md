# Template — Prompt d'analyse de repo (anti-truncation)

Ce template applique la structure ZONE 1 / ZONE 2 / ZONE 3 définie dans
`.github/instructions/repo-analysis-prompt.instructions.md`.

Copier-coller et remplir les `{variables}` avant envoi au LLM.

---

## ZONE 1 — CRITIQUE (envoyer EN PREMIER, toujours)

```
OBJECTIF : {objectif_une_phrase}
CONTRAINTE ABSOLUE : Cite un fichier ou une ligne réelle pour CHAQUE affirmation architecturale ou structurelle. Toute affirmation sans source fichier est invalide.
FORMAT DE SORTIE : {format_attendu}
RAPPEL OBJECTIF GLOBAL : {objectif_global_du_workflow}
```

---

## ZONE 2 — CONTEXTE (après ZONE 1)

```
REPO : {repo_name}
CHEMIN : {repo_path}

STRUCTURE RÉELLE (issue du grounding step-01) :
{file_tree}

FICHIERS CLÉS IDENTIFIÉS :
{key_files_list}

PATTERNS DÉTECTÉS :
{patterns_from_grounding}

CONTEXTE SESSION (depuis _memory/repo-contexts/{repo_name}.md) :
- Phase actuelle : {current_phase}
- Questions ouvertes : {open_questions}
- Décisions prises : {decisions_so_far}
```

---

## ZONE 3 — ENRICHISSEMENT (optionnel — peut être omis si le contexte est large)

```
EXEMPLES DE PATTERNS ATTENDUS :
{examples}

NUANCES ET CAS PARTICULIERS :
{nuances}

RÉFÉRENCES :
{references}
```

---

## Accusé de réception attendu du LLM

Le LLM doit répondre par ce bloc AVANT tout contenu :

```
✅ COMPRIS :
- Objectif : [reformulation en 1 phrase]
- Contrainte : [la contrainte absolue]
- Je vais commencer par lire : [liste des fichiers]
```

Si absent ou incorrect → renvoyer ZONE 1 seule.

---

## Variables disponibles dans le workflow repo-analysis

| Variable | Source | Description |
|---|---|---|
| `{repo_name}` | step-00 | Nom du repo analysé |
| `{repo_path}` | step-00 | Chemin absolu |
| `{file_tree}` | step-01 grounding | Arborescence réelle |
| `{key_files_list}` | step-01 grounding | Fichiers clés identifiés |
| `{patterns_from_grounding}` | step-01 grounding | Patterns détectés |
| `{objectif_global_du_workflow}` | step-00 | Objectif déclaré au lancement |
| `{current_phase}` | _memory/repo-contexts/ | Phase courante |
| `{open_questions}` | _memory/repo-contexts/ | Questions ouvertes |
| `{decisions_so_far}` | _memory/repo-contexts/ | Décisions cumulées |
