---
name: "grimoire-dispatch-engineer"
description: "Génère un prompt de dispatch structuré et validé avant chaque runSubagent. Use when: dispatch to sub-agent, prompt engineering for handoff, multi-agent task, complex delegation, quality-gated dispatch."
catalog-kind: "skill"
created: "2026-05-08"
version: "1.0"
token_budget: 600
zones: {protocol: "≤ 200 tokens", templates: "≤ 250 tokens", validation: "≤ 100 tokens"}
---

# Dispatch Prompt Engineer

## Quand utiliser

Avant chaque `runSubagent`. Automatiquement appliqué par le SOG via le bloc `<dispatch-engineer>` de grimoire-master. Invoquer explicitement via `grimoire-dispatch-engineer` quand :

- La tâche implique plusieurs sub-agents (préparer tous les dispatches d'abord)
- Le dispatch doit être validé ou inspecté avant exécution
- La tâche est critique et la qualité du handoff détermine l'issue

**Ne pas utiliser si** : réponse directe sans sub-agent, tâche conversationnelle, lecture simple sans action.

## Processus

### Étape 1 — Classifier la famille d'agent

| Famille | Agents concernés |
| --- | --- |
| `code` | dev, qa, tea, quick-flow-solo-dev |
| `architecture` | architect |
| `writing` | tech-writer, pm, sm, analyst |
| `ux` | ux-designer, art-director |
| `building` | agent-builder, workflow-builder, module-builder |
| `creativity` | brainstorming-coach, creative-problem-solver, design-thinking-coach, innovation-strategist, storyteller, presentation-master, rodin |

### Étape 2 — Collecter les sources de contexte

Priorité de fill-in :

1. Capsule PCG (`[CONTEXTE ENRICHI]` du Prompt Clarity Gate si présente)
2. Intent analysis du SOG (verbe, cible, objectif extraits lors du routing)
3. Fichiers touchés dans les 5 derniers turns de session
4. `_grimoire-runtime/_memory/shared-context.md`
5. `_grimoire-runtime/core/config.yaml`

### Étape 3 — Remplir le template de la famille

**Template universel — tous agents :**

```
[DISPATCH]
Agent   : {agent_name}
Famille : {family}

## Mission
{verbe d'action} {cible spécifique} — résultat attendu : {outcome précis}

## Contexte
{fichiers/modules concernés, état actuel, conventions actives}

## Contraintes
{non-objectifs, surfaces interdites, rétrocompatibilité}

## Livrable
Format      : {voir table ci-dessous par famille}
Destination : {chemin ou emplacement}

## Preuves attendues
{critères mesurables}

## Condition d'arrêt
{quand escalader au master plutôt que continuer}

## HUP
Incertitude > 30% → remonter au master, ne pas inventer.
[/DISPATCH]
```

**Champs requis et livrables par famille :**

| Famille | Mission — contrainte | Livrable — format attendu | Preuves minimales |
| --- | --- | --- | --- |
| `code` | Verbe + fichier/fonction cible | Code diff ou nouveau fichier | Tests green, lint pass |
| `architecture` | Décision à prendre + périmètre | ADR ou diagramme Mermaid | Critères de bonne décision listés |
| `writing` | Document + audience cible | Fichier .md avec section cible | Critères de review éditorial |
| `ux` | Artefact UX + contexte visuel | Wireframe, spec ou style guide | Critères visuels mesurables |
| `building` | Type d'artefact + template à suivre | Fichier d'artefact (agent/skill/workflow) | Contrat de sortie respecté |
| `creativity` | Objectif d'idéation + contrainte de divergence | Bullet list ou carte d'idées | Diversité des angles couverts |

### Étape 4 — Valider avant dispatch

Critères de blocage (dispatch refusé si un critère échoue) :

- MISSION contient un verbe vague sans cible ("améliore", "fais", "aide") → reformuler
- LIVRABLE dit "écris du code" sans format ni destination → préciser
- PREUVES dit "assure la qualité" sans critère mesurable → spécifier
- Un champ contient `{placeholder}` non remplacé → compléter ou supprimer
- Dispatch > 600 tokens → compresser CONTEXTE (garder delta, pas la base entière)

Si un champ requis ne peut pas être rempli depuis les sources disponibles : noter explicitement `[À PRÉCISER : raison]` — le sub-agent remontera le blocage plutôt que d'inventer.

### Étape 5 — Dispatcher

Passer le prompt généré comme contenu de `runSubagent`. Ne jamais dispatcher le message brut de l'utilisateur.

## Agents impliqués

| Agent | Rôle | Gate de passage |
| --- | --- | --- |
| grimoire-master (SOG) | Invoque le DPE, collecte les sources, valide | Validation étape 4 |
| sub-agent cible | Reçoit le dispatch, exécute | Preuves attendues remplies |

## Assets

- Template universel — inclus dans ce SKILL.md
- Table familles/templates — incluse dans ce SKILL.md
- Validateur — règles listées à l'étape 4

## Contrat de sortie

| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| Dispatch prompt | OUI | Bloc `[DISPATCH]...[/DISPATCH]` | ≤ 600 tokens |
| Famille détectée | OUI | String parmi les 6 familles | — |
| Champs validés | OUI | Confirmation ou liste d'erreurs | — |
| Sources utilisées | SHOULD | Liste ordonnée (PCG > SOG > session > ...) | ≤ 50 tokens |

**Critères de succès** :

- Aucun champ requis vide ou générique dans le dispatch
- Le sub-agent peut exécuter sa mission sans relire la conversation principale
- La condition d'arrêt est explicite — le sub-agent sait quand escalader

## Modules adaptatifs

<!-- WHEN: tâche implique plusieurs sub-agents séquentiels -->

### Module: Multi-dispatch planning

Avant de dispatcher le premier agent, lister tous les dispatches prévus :

```
Dispatch 1 → {agent_1} : {mission_1}
Dispatch 2 → {agent_2} : {mission_2} (dépend de dispatch 1 : {livrable_1})
```

Valider les dépendances de livrable avant de commencer. Arrêter si une dépendance est circulaire.

<!-- /WHEN -->

<!-- WHEN: dispatch vers agent `building` (agent-builder, workflow-builder, module-builder) -->

### Module: Building dispatch

Pour les agents builders, ajouter un champ TEMPLATE obligatoire :

```
## Template
Fichier de référence : {permanent-agent.tpl.md | permanent-skill.tpl.md | ...}
Sections à respecter : Contrat de sortie, Modules adaptatifs, Gestion d'erreur
```

<!-- /WHEN -->

<!-- WHEN: mode expert (user_skill_level=expert) -->

### Module: Expert shortcut

Saute les explications des étapes. Génère directement le bloc `[DISPATCH]` validé et confirme en une ligne.

<!-- /WHEN -->

## Exemples

### DO ✓

**Input** : User dit "améliore le module auth", famille `code` détectée, session contient `src/auth/service.py` récemment touché.

**Output** :

```
[DISPATCH]
Agent   : dev
Famille : code

## Mission
Identifier et corriger les failles de lisibilité dans `src/auth/service.py` —
résultat attendu : fonctions décomposées, noms explicites, complexité cyclomatique <= 10.

## Contexte
Fichier principal : src/auth/service.py (modifié dans les 3 derniers turns)
Stack : Python 3.12, ruff, pytest
Conventions : dataclasses frozen, pathlib, pas de bare except

## Contraintes
Ne pas modifier l'interface publique (AuthService.authenticate, AuthService.refresh)
Ne pas ajouter de dépendances externes

## Livrable
Format      : diff git sur src/auth/service.py (et tests associés si modifiés)
Destination : branche courante

## Preuves attendues
- pytest tests/unit/test_auth.py → vert
- ruff check src/auth/service.py → 0 erreur
- Aucune fonction > 20 lignes

## Condition d'arrêt
Si un changement nécessite de modifier l'interface publique → remonter au master.

## HUP
Incertitude > 30% → remonter au master, ne pas inventer.
[/DISPATCH]
```

### DON'T ✗

**Anti-pattern** : Dispatcher le message brut de l'utilisateur : "améliore le module auth"

**Problème** : Le sub-agent n'a pas de cible, pas de contrainte, pas de critère de succès. Il va produire un résultat arbitraire que le master devra corriger — coût doublé.

## Gestion d'erreur

- **Famille non identifiable** → utiliser `code` par défaut, noter l'incertitude dans CONTEXTE
- **Source de contexte vide** (shared-context.md manquant, pas de PCG capsule) → marquer les champs non remplissables avec `[À PRÉCISER]`, ne pas inventer
- **Dispatch > 600 tokens** → compresser CONTEXTE : garder seulement les fichiers directement touchés + les 2 conventions les plus critiques
- **Validation échoue sur PREUVES** → demander au master une seule question batch pour obtenir le critère manquant
