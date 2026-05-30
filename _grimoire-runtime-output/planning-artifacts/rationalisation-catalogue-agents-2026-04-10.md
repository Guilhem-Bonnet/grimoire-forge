---
title: Rationalisation du catalogue d'agents
description: Audit cible de duplication et proposition de reduction du catalogue actif d'agents Grimoire.
date: 2026-04-10
---

## Rationalisation du catalogue d'agents

## But

Reduire la dette de duplication sans casser les specialites reelles du systeme.

Le principe retenu est simple :

- un **agent durable** porte une responsabilite unique ;
- un **mode** change la cadence ou le niveau de ceremonie ;
- un **workflow** change la structure de travail ;
- un **style** change la forme de sortie, pas la responsabilite.

## Inventaire actuel

| Famille | Inventaire observe | Lecture |
| --- | --- | --- |
| BMM | 9 agents actifs | Socle le plus utile, mais plusieurs profils relevent plus du mode que d'une vraie specialite |
| CIS | 8 agents actifs | Beaucoup de valeur d'animation et de cadrage, mais forte redondance de facilitation |
| TEA | 1 agent actif | Specialite nette et defendable |
| Utilitaire | `Explore` hors runtime Grimoire | Doit rester traite comme utilitaire, pas comme membre du catalogue conceptuel |

Total pratique observe : **18 sous-agents** a traiter comme catalogue actif ou semi-actif.

## Probleme reel

Le probleme n'est pas seulement le score du harmony check. C'est la structure meme du catalogue : trop d'entites portent une difference de ton, de methode ou de ceremonie, alors que le noyau d'un Agent OS devrait privilegier un petit nombre de responsabilites stables.

En l'etat, le risque est double :

- le master route vers des personas au lieu de router vers des responsabilites ;
- le projet parait plus puissant qu'il n'est, parce qu'il multiplie les variantes d'interface de travail.

## Criteres pour garder un agent durable

Un agent reste agent durable seulement s'il remplit au moins les trois conditions suivantes :

- il possede une classe de decisions propre ;
- il produit ou valide des artefacts qu'un autre agent ne devrait pas posseder par defaut ;
- il ne peut pas etre reexprime proprement comme `mode`, `workflow` ou `style`.

## Decision cible par agent

| Agent actuel | Decision cible | Raison |
| --- | --- | --- |
| `architect` | Garder | Porte une responsabilite d'architecture, d'ADR et de frontieres systeme nette |
| `dev` | Garder | Porte l'implementation et le TDD, responsabilite centrale |
| `analyst` | Garder en le resserrant | Doit se limiter a la recherche, au cadrage domaine et aux hypotheses externes |
| `pm` | Garder en le resserrant | Doit se limiter au cadrage produit, priorisation et arbitrages de valeur |
| `qa` | Garder en le resserrant | Doit rester sur la generation et l'execution de couverture rapide |
| `tea` | Garder | Porte une vraie specialite d'architecture de test et de quality gates |
| `ux-designer` | Garder | Porte la conception d'experience, distincte de l'ideation pure |
| `tech-writer` | Garder | Porte la charte documentaire et la qualite editoriale |
| `creative-problem-solver` | Garder | Porte le diagnostic methodique et le root cause solving |
| `innovation-strategist` | Garder | Porte le cadrage strategic et business model |
| `rodin` | Garder | Porte la contradiction intellectuelle et la validation adversariale |
| `art-director` | Garder | Porte une specialite craft reelle pour la direction visuelle |
| `quick-flow-solo-dev` | Demoter en mode | C'est un profil d'execution lean du `dev`, pas une responsabilite distincte |
| `sm` | Demoter en workflow ou mode | Dans ce contexte IDE-first, la ceremonie scrum est une structure, pas un metier distinct |
| `brainstorming-coach` | Demoter en mode | C'est une modalite d'ideation divergente |
| `design-thinking-coach` | Demoter en mode | C'est une modalite de facilitation centree utilisateur |
| `presentation-master` | Demoter en style ou workflow | Releve surtout de la forme de restitution |
| `storyteller` | Demoter en style | Releve surtout de la narration de sortie |

## Catalogue cible

### Agents durables a conserver

- `architect`
- `dev`
- `analyst`
- `pm`
- `qa`
- `tea`
- `ux-designer`
- `tech-writer`
- `creative-problem-solver`
- `innovation-strategist`
- `rodin`
- `art-director`

### Modes, workflows ou styles a extraire du catalogue actif

- `quick-flow-solo-dev` -> mode d'execution rapide du `dev`
- `sm` -> workflow ou mode de decomposition backlog
- `brainstorming-coach` -> mode d'ideation divergente
- `design-thinking-coach` -> mode de facilitation centree utilisateur
- `presentation-master` -> style de communication visuelle
- `storyteller` -> style narratif

## Ce qu'il ne faut pas fusionner

### `qa` et `tea`

Ils se recouvrent rhetoriquement, mais pas fonctionnellement.

- `qa` doit rester l'outil de couverture rapide et de tests concrets.
- `tea` doit rester la couche de strategie, de risque et d'architecture qualite.

### `architect` et `dev`

Les fusionner ferait retomber le projet dans une logique de generaliste omnipotent. Ce serait l'inverse du resserrement voulu.

### `rodin` et `creative-problem-solver`

`rodin` contredit et steelmanne. `creative-problem-solver` diagnostique et structure le probleme. Les deux fonctions sont distinctes.

### `art-director` et `ux-designer`

L'un porte la direction visuelle et le craft, l'autre porte le comportement et l'experience. Les fusionner noierait deux specialites utiles.

## Routage cible simplifie

| Famille | Agents durables | Usage |
| --- | --- | --- |
| Execution | `architect`, `dev`, `qa`, `tea`, `ux-designer`, `tech-writer` | Produire, verifier, documenter |
| Produit | `analyst`, `pm` | Cadrer le probleme et la valeur |
| Critique et strategie | `creative-problem-solver`, `innovation-strategist`, `rodin` | Challenger, arbitrer, redresser |
| Craft specialise | `art-director` | Direction visuelle et coherence de style |

## Sequence de rationalisation

### Etape 1

Geler toute creation de nouvel agent durable tant que la rationalisation n'est pas close.

### Etape 2

Introduire dans le registre une colonne ou un champ equivalent distinguant :

- `durable_agent`
- `mode`
- `workflow_profile`
- `output_style`

### Etape 3

Demoter les six profils identifies sans casser la compatibilite d'usage : alias de routing, wrappers temporaires, documentation de migration.

### Etape 4

Refaire le skill routing du master autour des familles cibles, pas des anciens profils rhetoriques.

### Etape 5

Ajouter une gate simple : aucun agent nouveau ne peut entrer au catalogue durable sans phrase de responsabilite unique et preuve qu'un mode ne suffit pas.

## Gates de validation

- Le catalogue durable passe de 18 profils actifs a **12 agents durables** maximum, hors utilitaires de contexte.
- Chaque agent durable possede une phrase de responsabilite unique.
- Les modes et styles demotes restent utilisables sans rester de premier rang dans le runtime.
- Le master peut expliquer son routage par responsabilite metier, pas par simple proximitie de tonalite.

## Effet attendu

Le gain recherche n'est pas cosmetique. Il est structurel :

- moins de confusion de routage ;
- moins de dette de duplication ;
- un noyau conceptuel plus defendable face a OpenAI Agents SDK, LangGraph et Agent Framework ;
- une meilleure lisibilite du produit pour les contributeurs et pour la documentation publique.
