---
description: "Structure de prompt anti-truncation pour l'analyse de repos. Use when: building or executing any repo analysis, codebase audit, or multi-repo review prompt."
applyTo: "_grimoire-runtime/bmm/workflows/1-analysis/repo-analysis/**"
---

# Repo Analysis Prompt — Structure Anti-Truncation

## Principe fondamental

Les LLMs ne lisent pas tout le prompt. Les instructions critiques enterrées dans un long prompt sont silencieusement ignorées. Cette instruction impose une structure en entonnoir inversé : **ce qui compte le plus vient en premier**.

## Structure obligatoire des prompts d'analyse de repo

Tout prompt envoyé au LLM pour une analyse de repo DOIT respecter cet ordre :

### ZONE 1 — CRITIQUE (≤ 200 tokens, toujours lue)

```
OBJECTIF : [une phrase, l'objectif précis de cette étape]
CONTRAINTE ABSOLUE : [la règle non-négociable la plus importante]
FORMAT DE SORTIE : [ce qu'on attend exactement en output]
GROUNDING OBLIGATOIRE : Tu dois citer un fichier ou une ligne réelle pour chaque affirmation.
```

### ZONE 2 — CONTEXTE (chargé après ZONE 1)

```
REPO : {repo_name} @ {repo_path}
STRUCTURE RÉELLE :
{file_tree}

FICHIERS CLÉS :
{key_files_list}

CONTEXTE SESSION :
{repo_context_from_memory}
```

### ZONE 3 — ENRICHISSEMENT (optionnel, peut être tronqué)

```
EXEMPLES : [exemples de patterns attendus]
NUANCES : [cas particuliers]
RÉFÉRENCES : [docs, ADRs liés]
```

## Règles d'application

1. **Ne jamais inverser les zones** — ZONE 1 toujours en tête, ZONE 3 toujours en queue.
2. **ZONE 1 tient en 3-4 lignes maximum** — si tu as besoin de plus, c'est que l'objectif n'est pas clair.
3. **Checkpoint d'accusé de réception obligatoire** : chaque step doit démarrer par "Je vais [reformulation de l'objectif en 1 phrase]" — si le LLM ne reformule pas correctement, relancer avec ZONE 1 uniquement.
4. **Rappel d'objectif dans chaque step** : l'objectif initial du workflow DOIT être répété en ZONE 1 de chaque step, pas seulement au premier.
5. **Grounding non-négociable** : aucune affirmation architecturale ou structurelle sans citation de fichier réel. Si le LLM ne cite pas de fichier, l'output est invalide.

## Checkpoint d'accusé de réception

Après le premier message de chaque step, le LLM DOIT produire :

```
✅ COMPRIS :
- Objectif : [reformulation en 1 phrase]
- Contrainte : [la contrainte absolue]
- Je vais commencer par lire : [liste des fichiers à lire avant de faire des affirmations]
```

Si l'accusé de réception est absent ou incorrect, relancer avec :
> "Avant de continuer, reformule en 1 phrase l'objectif de cette étape et liste les fichiers que tu vas lire."

## Détection de lecture partielle

Signes que le LLM n'a pas lu tout le prompt :
- Affirmations sans citation de fichier
- Oubli de la contrainte absolue mentionnée en ZONE 1
- Output qui ne respecte pas le FORMAT DE SORTIE déclaré
- Reformulation incorrecte de l'objectif dans l'accusé de réception

Action corrective : réenvoyer ZONE 1 seule, sans ZONE 2 ni ZONE 3.
