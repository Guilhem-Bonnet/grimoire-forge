---
date: 2026-04-10
status: PROPOSED
owners:
  - Guilhem
  - Grimoire Master
---

# EPICS - Gouvernance structurelle et memoire agentique

## Objectif

Rendre la topologie du depot explicite, stable et exploitable par defaut pour les agents. Le programme doit imposer une hierarchie canonique de recherche, une gouvernance memoire nette, un minimum d'artefacts agentiques bien choisis et des garde-fous anti-drift, tout en reportant dans `grimoire-kit/` toute logique durable une fois la solution planifiee et validee.

## Decisions structurantes

- La racine reste un cockpit de documentation, d'orchestration et de glue locale.
- `_grimoire-runtime/` reste la source de verite du runtime Grimoire.
- `grimoire-kit/` est la landing zone obligatoire pour toute logique durable, tout validateur, tout indexeur et tout outillage reutilisable.
- `.github/agents/_archived/` sort du chemin de recherche nominal.
- Aucun nouvel agent de gouvernance n'est cree tant qu'un skill, une instruction ou un validateur suffit.

## Vue de livraison

| Phase | Focus | Sortie attendue | Gate de sortie |
| --- | --- | --- | --- |
| Phase 0 | Canon du depot | Charte des surfaces, navigation canonique, trigger de report vers le kit | Une seule doctrine explicite |
| Phase 1 | Navigation et memoire | Matrice de lookup, gouvernance memoire, index actifs versus archives | Un agent sait ou chercher sans heuristique fragile |
| Phase 2 | Artefacts agentiques | Skill cible, manifests enrichis, instructions durcies | Le comportement de recherche devient systemique |
| Phase 3 | Anti-drift | Checks de chemins, lint memoire, validateurs de manifests | Les ecarts deviennent detectables et visibles |
| Phase 4 | Migration et fermeture | Repointage progressif, reduction des wrappers gras, report vers le kit | Plus de logique durable laissee a la racine |

## Quick wins de la premiere vague

- Publier la charte canonique des surfaces et du lookup.
- Publier la gouvernance memoire agentique.
- Rendre explicite que les archives ne sont pas une surface de recherche normale.
- Ajouter un warning de preflight si une logique durable est ajoutee hors de `grimoire-kit/`.
- Produire un index actif versus archive pour les artefacts agentiques.

## Definition of Done globale

- Une doctrine unique couvre racine, runtime, outputs et kit.
- La hierarchie canonique de recherche est visible dans la doc et branchee dans les artefacts agentiques.
- La gouvernance memoire assigne une source canonique, un proprietaire et une regle d'obsolescence a chaque couche.
- Les archives sont exclues du chemin nominal.
- Les checks detectent les ecarts de landing zone, de memoire et de structure.
- Une story ne se ferme pas si sa logique durable n'a pas sa cible dans `grimoire-kit/`.

## Dependances avec Grimoire Kit

- `preflight-check.py` doit porter les regles de landing zone et de drift structurel.
- `memory-lint.py` doit porter les regles de contradictions, pointeurs manquants et couches memoire.
- Les validateurs de skills et manifests doivent etre renforces dans le kit, puis invoques depuis la racine.
- Les scans, indexeurs et policies reutilisables vivent dans `grimoire-kit/framework/tools/`.

## Phase 0 - Canon du depot

### EP01 - Canon des surfaces

**But** : figer les frontieres officielles du depot et les droits d'ecriture associes.

**Criteres de sortie** : chaque surface du depot a un role canonique, un droit d'ecriture et un statut de recherche clair.

#### Stories initiales EP01

| ID | Story | Sortie attendue |
| --- | --- | --- |
| GS-EP01-S01 | Rendre explicite le role de la racine, du runtime, des outputs et du kit | Charte des surfaces publiee |
| GS-EP01-S02 | Sortir les archives du chemin nominal | Regle officielle pour `.github/agents/_archived/` |
| GS-EP01-S03 | Fixer le trigger de report vers le kit | Regle opposable pour la landing zone durable |

### EP02 - Navigation canonique

**But** : rendre deterministe le premier chemin de recherche selon le besoin traite.

**Criteres de sortie** : un agent peut suivre une matrice de lookup courte, sans exploration opportuniste par defaut.

**Dependances** : EP01.

#### Stories initiales EP02

| ID | Story | Sortie attendue |
| --- | --- | --- |
| GS-EP02-S01 | Definir l'ordre de lecture par type de besoin | Matrice de lookup publiee |
| GS-EP02-S02 | Rendre le canon visible depuis les points d'entree du depot | README et hub documentaire raccordes |
| GS-EP02-S03 | Definir le fallback autorise | Regle unique de repli documentee |

## Phase 1 - Navigation et memoire

### EP03 - Gouvernance memoire par couche

**But** : distinguer rappel operationnel, memoire systeme, historique et source de verite.

**Criteres de sortie** : chaque type de fait a une source canonique, une memoire de soutien et une regle d'obsolescence.

**Dependances** : EP01 et EP02.

#### Stories initiales EP03

| ID | Story | Sortie attendue |
| --- | --- | --- |
| GS-EP03-S01 | Definir la source canonique par type de fait | Matrice source de verite publiee |
| GS-EP03-S02 | Definir qui ecrit ou et quand purger | Matrice ecriture, lecture, purge publiee |
| GS-EP03-S03 | Raccorder la memoire repo aux nouvelles sources canoniques | Notes repo repointees vers les bons fichiers |

## Phase 2 - Artefacts agentiques minimum

### EP04 - Skill et manifests de navigation

**But** : encoder le canon dans le dispositif agentique avec le plus petit artefact suffisant.

**Criteres de sortie** : le bootstrap et les artefacts de routage savent exposer la navigation canonique sans creer un nouvel agent specialise.

**Dependances** : EP02 et EP03.

#### Stories initiales EP04

| ID | Story | Sortie attendue |
| --- | --- | --- |
| GS-EP04-S01 | Creer un skill cible de navigation structurelle et landing zones | Skill valide et documente |
| GS-EP04-S02 | Enrichir les manifests avec statut, surface et priorite de lookup | Metadonnees disponibles pour le runtime |
| GS-EP04-S03 | Durcir les instructions existantes plutot que multiplier les artefacts | Instructions ciblees alignees sur le canon |

## Phase 3 - Anti-drift

### EP05 - Garde-fous structurels et memoire

**But** : rendre visibles et actionnables les ecarts a la doctrine.

**Criteres de sortie** : les checks signalent les mauvaises landing zones, les doublons memoire et les references obsoletes.

**Dependances** : EP03 et EP04.

#### Stories initiales EP05

| ID | Story | Sortie attendue |
| --- | --- | --- |
| GS-EP05-S01 | Ajouter le controle de landing zone au preflight | Warning ou echec cible sur logique durable hors kit |
| GS-EP05-S02 | Etendre memory-lint aux pointeurs et contradictions | Rapport memoire plus discriminant |
| GS-EP05-S03 | Valider les manifests et indexes actifs versus archives | Index et validateurs coherents |

## Phase 4 - Migration et fermeture

### EP06 - Report progressif vers Grimoire Kit

**But** : fermer les ambiguities sans big bang et sortir la logique durable de la racine.

**Criteres de sortie** : les wrappers racine restent minces et appellent une logique du kit deja stabilisee.

**Dependances** : EP05.

#### Stories initiales EP06

| ID | Story | Sortie attendue |
| --- | --- | --- |
| GS-EP06-S01 | Identifier les wrappers gras ou controles locaux a extraire | Liste de migration priorisee |
| GS-EP06-S02 | Deplacer les validateurs et indexeurs reutilisables vers le kit | Outils durables poses dans `grimoire-kit/framework/tools/` |
| GS-EP06-S03 | Repointage progressif de la documentation et des hooks | Plus de verite concurrente entre racine et kit |
