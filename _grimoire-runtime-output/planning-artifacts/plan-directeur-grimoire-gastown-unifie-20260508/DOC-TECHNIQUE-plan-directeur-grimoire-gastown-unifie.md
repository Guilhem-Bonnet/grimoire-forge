---
title: Documentation technique - Plan directeur Grimoire x Gastownhall unifie
description: Analyse technique du nouveau projet Grimoire Agent OS, incluant Grimoire Forge, grimoire-kit, Gastownhall et les projets agentiques a fusionner.
author: Codex
date: 2026-05-08
---

# Documentation technique - Plan directeur Grimoire x Gastownhall unifie

## Reponse courte

Le rapport precedent prenait en compte Gastownhall via les documents d'adaptation deja presents, mais pas encore comme ecosysteme complet. Cette passe corrige ce point.

Gastownhall doit etre lu comme une chaine complete :

```text
Gas Town -> Gas City -> Beads -> Gas City Packs -> Gas City OTEL -> Community and Docs
```

La bonne conclusion n'est pas de recopier Gastownhall. La bonne conclusion est de transformer ses primitives en contrats Grimoire-native, puis de les brancher dans Forge et grimoire-kit avec hooks, guardrails, preuves et cockpit.

## Sources locales analysees

| Source | Signal exploite |
| --- | --- |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/beads/README.md` | Beads comme issue tracker distribue agent-friendly, ids anti-collision, JSON, dependances. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/beads/docs/ARCHITECTURE.md` | Architecture Dolt, modele issues/dependencies/events, audit trail, sync multi-writer. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/beads/docs/MULTI_REPO_AGENTS.md` | Routing multi-repo, isolation par projet, aggregation et provenance. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/gascity/README.md` | Gas City comme orchestration-builder SDK : providers, work routing, formulas, orders, health patrol. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/gascity/docs/getting-started/coming-from-gastown.md` | Traduction roles -> primitives, plugins -> orders, convoys -> bead graph, controller -> infra owner. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/gascity/TRACK3_CONTRACT.md` | Modele command discovery et doctor discovery ferme par defaut. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/gascity-packs/` | Packs reels : commandes, doctor checks, services, formulas, pack.toml. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/gascity-otel/README.md` | Observabilite VictoriaMetrics, VictoriaLogs, Grafana, metriques `gc_*` et `bd_*`. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/gas town/community/plans/gastownhall-ecosystem-plan.md` | Strategie ecosysteme, documentation, Discord, adoption contributeur, transparence produit. |
| `/mnt/Travail/Projets/Dev/Référence-Agentique/crewAI/` | Crews, Flows, task guardrails, checkpointing, memory, knowledge, MCP, tracing, testing/training. |
| `_grimoire-runtime-output/planning-artifacts/DOC-TECHNIQUE-adaptation-gastownhall-grimoire.md` | Ancienne decision : absorber primitives, pas contraintes produit ou backend. |
| `_grimoire-runtime-output/planning-artifacts/PLAN-adaptation-gastownhall-grimoire.md` | Ancienne traduction Mayor, Beads, Convoy, Molecule, Seance, Packs, Marketplace. |
| `_grimoire-runtime-output/planning-artifacts/FEATURES-ET-TASKS-adaptation-gastownhall-grimoire.md` | Backlog GTA et tri absorbed/next/later/experimental/reject. |
| `_grimoire-runtime-output/planning-artifacts/strategie-grimoire-agent-os-20260508/` | Rapport precedent : formule Agent OS, angles morts, references OpenAI, LangGraph, MCP, A2A, OTel, OWASP. |
| `.github/hooks/` et `_grimoire-runtime/_config/hook-safety-registry.json` | Hooks Grimoire deja promus, modes enforced/canary/shadow, digest de validation. |
| `grimoire-kit/docs/memory-os-roadmap.md` | Memory OS : Qdrant, Redis optionnel, code graph, task memory. |
| `grimoire-kit/docs/grimoire-game-runtime-guardrails.md` | Guardrails runtime TypeScript, mutation guardrails, verification chain cible, canonical envelope pilot. |
| `grimoire-kit/framework/registry/compiled-flow-recipes.json` | Recettes compilees, hook governance audit, interdiction de logique metier lourde dans les hooks. |

## Sources web primaires verifiees

| Source | Signal utile |
| --- | --- |
| [Gas City Docs](https://docs.gascityhall.com/) | La documentation publique presente Gas City comme SDK d'orchestration et separe guides actuels, references et engdocs. |
| [Gas City - Coming from Gas Town](https://docs.gascityhall.com/getting-started/coming-from-gastown) | Confirme le pivot : roles et filesystem Gas Town deviennent packs, city config, orders, formulas, controller. |
| [GitHub gastownhall/gastown](https://github.com/gastownhall/gastown) | Gas Town coordonne Claude, Copilot, Codex, Gemini, avec work tracking persistant, Mayor, rigs, hooks, convoys, Beads. |
| [Gas City Hall](https://gascityhall.com/) | Confirme le positionnement ecosysteme : Gas City v1.0, SDK composable, Wasteland, community. |
| [Agent Provider Integration Guide](https://github.com/gastownhall/gastown/blob/main/docs/agent-provider-integration.md) | Confirme les tiers d'integration provider : zero integration, preset, hooks, deep integration. |
| [CrewAI Docs](https://docs.crewai.com/) | Confirme les primitives CrewAI : Crews, Flows, Tasks, Memory, Knowledge, MCP, tracing et checkpointing. |

## Diagnostic Grimoire actuel

Grimoire a deja plusieurs briques qui recoupent Gastownhall :

- un bootstrap multi-host natif : `AGENTS.md`, Copilot, Claude, Codex ;
- un plan de hooks reel : `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, `Stop` ;
- un registre de securite des hooks avec digest, modes et control files ;
- une UI runtime dans `grimoire-kit/apps/grimoire-game` avec ledger hooks, Mission Board, timeline et observabilite ;
- des guardrails runtime TypeScript pour les mutations ;
- un Memory OS deja cadre avec Qdrant, Redis optionnel, code graph et task memory ;
- un SDK Python avec `HookManager`, CLI, MCP, outils runtime et docs ;
- beaucoup de plans historiques, parfois redondants, qui doivent maintenant devenir des sources referencees.

Le risque principal n'est pas le manque d'idees. Le risque principal est la coexistence de trop de roadmaps qui parlent des memes objets avec des noms differents.

## Diagnostic Gastownhall

### Ce qu'il faut absorber

| Primitive | Pourquoi elle compte pour Grimoire |
| --- | --- |
| Beads | Le travail devient graphe durable, interrogeable, partageable et pret pour agents. |
| Dependencies and ready query | Les agents ne choisissent pas au hasard : ils prennent ce qui est debloque. |
| Hash ids et content hashes | Evite collisions et rend l'import multi-agent plus robuste. |
| Multi-repo routing | Utile pour Forge + grimoire-kit + futurs packs externes. |
| City config et packs | Separe definition reutilisable, deploiement local et etat machine. |
| Orders | Remplace les plugins lourds par automation controller-side sans agent si le LLM n'est pas necessaire. |
| Formulas / molecules | Base de recipes instanciees avec suivi et reprise. |
| Supervisor/controller | Les comportements infra appartiennent au runtime, pas a un agent special omniscient. |
| Doctor checks | Chaque pack doit apporter ses checks, mais ils doivent contribuer a un doctor global. |
| Provider tiers | Tous les hosts n'ont pas les memes capacites hooks ; le plan doit gerer fallback et degradation. |
| OTEL metrics | Donne un vocabulaire d'observabilite utile pour agent starts, crashes, calls, tokens, sessions, mail. |

### Ce qu'il faut refuser

| Element source | Raison du refus |
| --- | --- |
| Copier Dolt comme source obligatoire | Grimoire a besoin d'un ledger canonique portable ; Dolt peut devenir adaptateur, pas noyau impose. |
| Copier tmux comme abstraction produit | Utile comme provider, dangereux comme architecture obligatoire. |
| Copier les noms Mayor, Deacon, Dogs, Polecats comme UX principale | Grimoire a deja `grimoire-master` et son vocabulaire. |
| Copier les dossiers Gas Town comme contrat | Les chemins ne doivent pas devenir l'architecture. |
| Copier Wasteland dans le noyau | La federation/trust network est utile, mais doit rester experimentale avant gouvernance complete. |

## These technique

Le nouveau projet doit etre construit autour de deux produits qui se nourrissent mutuellement :

| Surface | Role |
| --- | --- |
| Grimoire Forge | Repo vivant, dogfood, cockpit de planification, runtime d'instructions, politiques, hooks, rapports, preuves. |
| grimoire-kit | SDK, CLI, runtime kernel, pack registry, Memory OS, dashboards, integration distribuable. |

Forge ne doit pas devenir un fork non distribuable du kit. Le kit ne doit pas devenir un SDK abstrait deconnecte du vrai chantier. Forge est la preuve vivante ; grimoire-kit est le produit.

## Formule cible consolidee

```text
Grimoire Agent OS =
  Runtime Kernel
+ Mission Ledger
+ Workflow Instances
+ Pack Registry
+ Hook and Guardrail Plane
+ Memory OS
+ Host Bridge and Provider Plane
+ Trace, Eval and Evidence Ledger
+ Mission Board Cockpit
+ Distribution and Ecosystem Layer
```

## Regle de fusion

Une primitive externe ne rentre pas par copie brute. Elle passe par cette chaine :

```text
Reference externe
-> decision d'absorption
-> contrat Grimoire
-> adaptateur ou pack experimental
-> hook/gate de controle
-> preuve de replay ou de validation
-> promotion stable
```

Toute integration qui contourne `Mission Ledger`, `Workflow Instances`, `Pack Registry`, `Memory OS`, `Policy Verdict` ou `Evidence Pack` doit etre refusee.
