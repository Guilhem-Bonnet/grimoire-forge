---
title: Revue du catalogue d'agents 2026-04-14
description: Audit complet du catalogue d'agents, de leur configuration, de leur necessite et de leur alignement avec le scope Grimoire Forge.
date: 2026-04-14
---

## Verdict executif

Le systeme n'est pas sous-dote en agents durables. Il est sur-segmente.

Le vrai probleme n'est pas "quel agent manque ?", mais "quelles entites sont traitees comme agents alors qu'elles ne sont que des modes, des workflows ou des styles ?".

Le catalogue defendable a court terme est :

- `grimoire-master` comme orchestrateur unique et durable
- 12 sous-agents durables alignes sur des frontieres de decision reelles
- 3 builders utilitaires
- 6 profils a demoter hors du premier rang du catalogue durable
- `bmad-master` maintenu comme alias de compatibilite, pas comme source de verite runtime

Aucune creation de nouvel agent durable n'est justifiee a ce stade.

## Perimetre et methode

Cette revue s'appuie sur :

- la configuration runtime : `agent-manifest.csv`, `agent-wrapper-spec.json`, `model-routing.yaml`, `agent-surface-index.csv`
- les wrappers workspace sous `.github/agents/`
- les agents runtime dans `_grimoire-runtime/core/agents/`, `_grimoire-runtime/bmm/agents/`, `_grimoire-runtime/bmb/agents/`, `_grimoire-runtime/cis/agents/`, `_grimoire-runtime/tea/agents/`
- la gouvernance interne : `docs/governance/referentiel-bonnes-pratiques-agentiques.md`, `docs/governance/checklist-operationnelle-audit-agentique.md`, `docs/governance/adr-guardrails-hooks-plan-de-controle.md`
- le scope projet : `project-context.yaml`, `docs/exploitation/plan-maitre-agent-os-game-ui.md`, `docs/vision/objectif-moteur-agentique.md`, `docs/references/agent-frameworks.md`, `README.md`
- les audits precedents, surtout `rationalisation-catalogue-agents-2026-04-10.md`
- des references externes recentes : [Anthropic - Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), [Model Context Protocol](https://modelcontextprotocol.io/introduction) et [GitHub Docs - repository custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)

La conclusion a aussi ete relue via une double lecture croisee interne : une lecture architecture/structure et une lecture gouvernance/builders. Les deux convergent.

## Scope de reference

Le scope reel du projet est celui d'un Agent OS oriente :

- orchestration master-first et SOG
- hooks et guardrails comme plan de controle
- integration host-side avec Copilot, Claude, MCP et outillage VS Code
- preuves d'execution, integrite, trace et surfaces de gouvernance
- Game UI / Cockpit comme surface visible du controle, pas comme nouveau domaine metier autonome

Consequence directe : le catalogue durable doit representer des frontieres de responsabilite stables. Il ne doit pas multiplier des variantes de ton, de cadence ou de ceremonie.

## Constat principal

### 1. L'exposition utilisateur est deja saine

Le modele "un seul agent user-facing" est respecte : `grimoire-master` reste le seul point d'entree utilisateur, les autres wrappers etant des sous-agents internes. C'est coherent avec le scope SOG.

### 2. Le catalogue melange actuellement plusieurs natures d'entites

Avant cette revue, le catalogue traitait a peu pres sur le meme plan :

- des responsabilites durables
- des utilitaires de fabrication d'artefacts
- des modes d'execution
- un profil de workflow
- des styles de restitution
- un alias de compatibilite

Ce melange cree de la dette de routage et de la dette documentaire. Le master risque alors de router vers une "saveur" de travail au lieu de router vers une responsabilite.

### 3. Le systeme manque de classification, pas de personas

La question centrale n'est pas "faut-il plus d'agents ?", mais "comment classifier ce qui existe ?".

Le gap reel etait l'absence d'une classification canonique partagee entre :

- la spec de wrappers
- les wrappers generes
- l'index de surface agentique
- les futures regles de routage et de reporting

### 4. La suppression brute est logique conceptuellement, mais risquee operationnellement

Les six profils a demoter sont encore references dans :

- les manifests et indexes de surface
- le model routing
- l'aide et des workflows
- des artefacts de planning et de communication
- certaines chaines de compatibilite workspace

Une suppression immediate casserait des surfaces secondaires. La bonne sequence est donc : classifier d'abord, migrer ensuite, retirer en dernier.

### 5. Il existe un drift de tooling a corriger plus tard

Un utilitaire Grimoire de listing d'agents ne reconnait pas l'archetype `meta` alors que `project-context.yaml` l'annonce installe. Ce n'est pas un besoin de nouvel agent. C'est un symptome de derive entre configuration projet et outillage d'inspection.

## Taxonomie cible

La taxonomie a inscrire partout est la suivante :

| Kind | Sens | Usage legitime |
| --- | --- | --- |
| `durable_agent` | Frontiere de responsabilite stable | Routage de premier rang |
| `builder_utility` | Utilitaire de fabrication d'artefacts | UDF, maintenance, generation |
| `mode_profile` | Variation de cadence ou de ceremonie | Qualificatif d'execution |
| `workflow_profile` | Variation de structure de travail | Decomposition, delivery flow |
| `output_style` | Variation de forme de restitution | Packaging, narration, presentation |
| `compatibility_alias` | Compatibilite historique | Transition, pas source de verite |

## Catalogue cible

Le catalogue cible defendable est :

- 1 orchestrateur durable : `grimoire-master`
- 12 sous-agents durables
- 3 utilitaires builders
- 3 profils de mode
- 1 profil de workflow
- 2 styles de sortie
- 1 alias de compatibilite

## Matrice de decision par agent

| Entite | Kind cible | Decision | Argument |
| --- | --- | --- | --- |
| `grimoire-master` | `durable_agent` | Garder | Frontiere de responsabilite unique : orchestration, clarification, aggregation, HUP, QEC, CVTL et PCE |
| `analyst` | `durable_agent` | Garder et resserrer | Utile pour recherche, cadrage domaine et hypotheses externes |
| `architect` | `durable_agent` | Garder | Porte l'architecture, les ADR et les frontieres systeme |
| `dev` | `durable_agent` | Garder | Porte l'implementation et l'execution technique |
| `pm` | `durable_agent` | Garder et resserrer | Utile pour priorisation et arbitrage de valeur |
| `qa` | `durable_agent` | Garder et resserrer | Couvre la verification concrete et rapide |
| `tech-writer` | `durable_agent` | Garder | Frontiere editoriale reelle et recurrente |
| `ux-designer` | `durable_agent` | Garder | Porte l'experience, distincte de la simple facilitation |
| `creative-problem-solver` | `durable_agent` | Garder | Diagnostic methodique, root cause solving, debuggage conceptuel |
| `innovation-strategist` | `durable_agent` | Garder | Arbitrage strategique et business model |
| `rodin` | `durable_agent` | Garder | Contradiction intellectuelle, steelmanning, remise en cause de la chambre d'echo |
| `art-director` | `durable_agent` | Garder | Specialite craft reelle pour la direction visuelle |
| `tea` | `durable_agent` | Garder | Architecture de test et quality gates, distincte de `qa` |
| `agent-builder` | `builder_utility` | Garder hors premier rang | Necessaire pour la UDF et la gouvernance d'agents, mais ce n'est pas un agent metier |
| `module-builder` | `builder_utility` | Garder hors premier rang | Meme logique : utilitaire de fabrication, pas responsabilite metier |
| `workflow-builder` | `builder_utility` | Garder hors premier rang | Idem, utile pour la factory et les workflows |
| `quick-flow-solo-dev` | `mode_profile` | Demoter | Variante lean de `dev`, pas frontiere de decision autonome |
| `brainstorming-coach` | `mode_profile` | Demoter | Modalite d'ideation divergente, pas responsabilite durable |
| `design-thinking-coach` | `mode_profile` | Demoter | Modalite de facilitation centree utilisateur, pas agent durable |
| `sm` | `workflow_profile` | Demoter | Dans ce contexte IDE-first, le scrum est une structure de travail plus qu'un metier distinct |
| `presentation-master` | `output_style` | Demoter | Forme de restitution et packaging visuel, pas responsabilite autonome |
| `storyteller` | `output_style` | Demoter | Style narratif, pas frontiere de decision durable |
| `bmad-master` | `compatibility_alias` | Conserver comme alias seulement | Compatibilite workspace, ne doit plus compter dans le catalogue conceptuel |

## Pourquoi ces 6 demotions sont justes

### `quick-flow-solo-dev`

Il n'apporte pas une nouvelle classe de decisions. Il change le niveau de ceremonie, la vitesse et le volume d'artefacts. Cela releve d'un mode de `dev`, pas d'un agent distinct.

### `sm`

Dans un environnement IDE-first pilote par un orchestrateur unique, la decomposition de backlog et la ceremonie scrum doivent etre exprimees comme workflow ou skill de delivery, pas comme un agent durable autonome. La responsabilite est structurante, mais la frontiere metier n'est pas assez forte pour justifier un agent de premier rang.

### `brainstorming-coach` et `design-thinking-coach`

Ces deux profils servent surtout de methodes de facilitation. Ils changent la maniere d'explorer un probleme, pas la nature du probleme. Ils gagnent a devenir des modes ou des workflows applicables aux agents de produit, UX ou innovation.

### `presentation-master` et `storyteller`

Ces profils sont utiles, mais comme styles de restitution. Ils s'appliquent a un resultat produit ailleurs. Les traiter comme agents durables brouille la lisibilite du catalogue.

## Ce qu'il ne faut pas fusionner

### `qa` et `tea`

Leur recouvrement rhetorique existe, mais leurs decisions ne sont pas les memes.

- `qa` couvre le concret, la couverture rapide et l'execution de tests
- `tea` porte la strategie de test, le risque et les quality gates

### `architect` et `dev`

Les fusionner redonnerait un generaliste omnipotent, exactement l'inverse du resserrement recherche.

### `rodin` et `creative-problem-solver`

`rodin` challenge les hypotheses. `creative-problem-solver` structure le diagnostic. Les deux fonctions sont distinctes et utiles.

### `art-director` et `ux-designer`

L'un porte la coherence visuelle et le craft, l'autre le comportement et l'experience. Les fusionner ferait perdre deux specialites utiles, surtout sur le front Game UI / cockpit.

## Analyse des manques par rapport au scope

### Aucun nouvel agent durable n'est requis maintenant

Je ne recommande pas la creation d'un nouvel agent durable sur le scope actuel.

Les besoins qui pourraient donner cette impression sont deja mieux couverts autrement :

| Besoin apparent | Tentation naive | Bonne reponse |
| --- | --- | --- |
| Securite | creer un `security-agent` durable | garder la securite comme skill, workflow, gate et revue transversale |
| Scrum / delivery | garder `sm` comme agent | exprimer cela en workflow ou skill de delivery |
| Ideation | garder plusieurs coachs | garder un mode d'ideation, pas plusieurs agents durables |
| Narration / pitch | garder `storyteller` et `presentation-master` comme agents | les traiter comme styles de sortie invoquables |
| Compatibilite historique | compter `bmad-master` comme agent actif | le traiter comme alias seulement |

### Le vrai manque est ailleurs

Le manque prioritaire est une couche explicite de gouvernance et de routing basee sur la nature de l'entite. Autrement dit :

- le runtime doit savoir qu'un `mode_profile` n'est pas un `durable_agent`
- la documentation doit parler le meme vocabulaire que la spec
- les surfaces d'aide, de listing et de routage doivent cesser de presenter ces profils comme des pairs

## Changement applique dans le depot pendant cette revue

La revue n'est pas restee theorique. Une premiere correction structurelle a ete appliquee.

### 1. Classification canonique ajoutee a la spec de wrappers

`_grimoire-runtime/_config/agent-wrapper-spec.json` contient maintenant un champ canonique `catalogKinds` qui classe chaque entite.

### 2. Propagation automatique dans la generation

`grimoire-kit/framework/tools/agent-lint.py` propage maintenant `catalogKind` :

- dans les wrappers generes
- dans l'index de surface agentique
- dans les artefacts de regeneration associes

### 3. Regeneration et validation complete

Le lint canonique a ete relance avec regeneration des wrappers et de l'index de surface.

Resultat valide :

- 22 agents verifies
- 22 agents propres
- 0 erreur
- 0 warning

## Pourquoi cette correction etait la bonne premiere etape

Parce qu'elle traite la cause racine sans casser le systeme :

- la classification devient machine-readable
- le catalogue peut etre reporte, route et filtre sans suppression immediate
- la migration future peut s'appuyer sur un vocabulaire stable
- les references historiques peuvent etre traitees progressivement

Autrement dit : la rationalisation devient pilotable, pas seulement discutable.

## Recommandations de suite

### Phase 1 - Gouvernance

Faire consommer `catalogKind` par :

- les rapports et surfaces de listing
- les manifests d'aide
- les vues de gouvernance et de doc

### Phase 2 - Routage

Mettre le master et les surfaces de routage en coherence avec cette regle :

- les `durable_agent` sont les seules entites de premier rang
- les `builder_utility` sont selectionnes par besoin UDF
- les `mode_profile`, `workflow_profile` et `output_style` sont invoques comme qualificatifs, pas comme agents pairs

### Phase 3 - Migration sans casse

Retirer progressivement les six profils demotes des surfaces qui les presentent encore comme agents durables, en gardant :

- alias temporaires
- wrappers de compatibilite
- documentation de migration

### Phase 4 - Gate d'entree pour tout nouvel agent

Aucun nouvel agent durable ne doit entrer au catalogue sans satisfaire ces quatre questions :

1. Porte-t-il une frontiere de decision unique et recurrente ?
2. Produit-il ou valide-t-il des artefacts que les autres ne devraient pas absorber par defaut ?
3. Ne peut-il pas etre exprime plus proprement comme mode, workflow, skill ou style ?
4. Le besoin est-il durable sur le scope reel du projet, et pas seulement ponctuel ?

## Decision finale

Le projet doit viser un catalogue conceptuel resserre :

- 1 orchestrateur durable
- 12 sous-agents durables
- 3 utilitaires builders
- 6 entites requalifiees hors du premier rang
- 1 alias de compatibilite non compte comme agent actif

La bonne action n'est donc ni d'ajouter un nouvel agent durable, ni de supprimer brutalement des wrappers encore references. La bonne action est celle qui a ete engagee ici : rendre la classification canonique, puis migrer le reste du systeme vers cette realite.
