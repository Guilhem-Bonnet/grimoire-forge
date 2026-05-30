---
name: grimoire-learnings
description: "Système d'apprentissage opérationnel cross-session. Use when: log learning, save insight, operational discovery, what did we learn, remember this, cross-session memory, compound learnings."
---

# Operational Learnings

Système d'accumulation de connaissances opérationnelles entre sessions. Inspiré de gstack `/learn` — chaque session peut enregistrer des découvertes qui seront auto-injectées dans les sessions futures.

## Principe

La bonne question : **est-ce que savoir cela économiserait 5+ minutes dans une future session ?** Si oui, le loguer.

## Types de learnings

| Type | Exemples |
|---|---|
| **Opérationnel** | "ruff ignore les fichiers framework/ — utiliser `--extend-select`" |
| **Environnement** | "pytest -x ne s'arrête pas si le test est dans une classe" |
| **Architecture** | "Le MemoryManager ne supporte pas les requêtes parallèles" |
| **Convention** | "Les tools framework/ utilisent des tirets, pas des underscores" |
| **Piège** | "Ne jamais `grep_search` sans `includePattern` — crash extension host" |

## Ne PAS loguer

- Erreurs transitoires (blips réseau, rate limits)
- Évidences (Python utilise des indentations)
- Informations déjà dans la documentation
- Bugs une seule fois non reproductibles

## Comment loguer

**Format structuré :**

```
KEY: identifiant_court_unique
INSIGHT: description concise de la découverte
CONFIDENCE: 0-100 (60 = probable, 80 = confirmé, 95 = certain)
SOURCE: observed | documented | inferred
TAGS: [domaine1, domaine2]
```

**Exemples :**

```
KEY: ruff-framework-exclude
INSIGHT: Les fichiers dans framework/tools/ sont exclus du lint par défaut — utiliser ruff check --extend-select pour les inclure
CONFIDENCE: 95
SOURCE: observed
TAGS: [ruff, lint, framework]
```

```
KEY: pytest-no-xdist
INSIGHT: Ne jamais utiliser pytest-xdist (-n auto) dans ce projet — les tests partagent l'état via des fichiers temporaires
CONFIDENCE: 90
SOURCE: documented
TAGS: [pytest, tests]
```

## Injection automatique

Au démarrage de chaque session, les 3-5 learnings les plus pertinents sont injectés dans le contexte de l'agent :

```markdown
## Operational Learnings (auto-injected)

- **ruff-framework-exclude**: Les fichiers dans framework/tools/ sont exclus du lint par défaut (confidence: 95%)
- **pytest-no-xdist**: Ne jamais utiliser pytest-xdist dans ce projet (confidence: 90%)
```

## Commandes

| Action | Commande |
|---|---|
| Loguer un learning | "retiens que...", "learning: ...", "note opérationnelle: ..." |
| Chercher | "learnings sur pytest", "qu'est-ce qu'on sait sur ruff" |
| Top learnings | "montre les learnings", "operational learnings" |
| Compter | "combien de learnings" |

## Stockage

- **Format** : JSONL dans `_grimoire/_memory/learnings/operational.jsonl`
- **Limite** : 200 entrées max (prune automatique des anciennes low-confidence)
- **Déduplication** : même `key` → mise à jour (pas de doublon)

## Intégration hooks

Le hook `session_start` injecte automatiquement les top learnings via le listener `learning_injector`. Le hook `post_tool_use` capture les échecs pour alimenter les futurs learnings via `failure_capturer`.

## Réflexion de fin de session

Avant de terminer, se poser :

- Des commandes ont échoué de manière inattendue ?
- Un mauvais chemin pris puis corrigé ?
- Une particularité du projet découverte (ordre de build, env vars, timing) ?
- Quelque chose a pris plus longtemps que prévu à cause d'un flag ou config manquant ?

Si oui → loguer le learning.
