---
title: Cahier des charges - Projet cible Grimoire Agent OS
description: Index du cahier des charges cible pour Grimoire Forge et grimoire-kit.
author: Codex
date: 2026-05-08
---

# Cahier des charges - Projet cible Grimoire Agent OS

Ce paquet decrit le projet cible ideal pour pousser Grimoire Forge et grimoire-kit au niveau d'un Agent OS operable, gouverne, extensible et mesurable.

Il complete le plan directeur unifie deja present dans :

`_grimoire-runtime-output/planning-artifacts/plan-directeur-grimoire-gastown-unifie-20260508/`

## Documents

| Document | Role |
| --- | --- |
| `CAHIER-DES-CHARGES-projet-cible-grimoire-agent-os.md` | Specification produit et systeme complete |
| `ARCHITECTURE-CIBLE-diagrammes.md` | Architecture cible avec diagrammes Mermaid |
| `SCHEMAS-CONTRATS-cibles.md` | Schemas, contrats, manifests et evenements |
| `EXIGENCES-GATES-ACCEPTATION.md` | Exigences fonctionnelles, non fonctionnelles, securite et gates |
| `DOSSIER-EXECUTION-AGENTS.md` | Lots executables par agents avec hooks, guardrails et preuves |
| `DOC-TECHNIQUE-cahier-des-charges-projet-cible-grimoire-agent-os.md` | Notes techniques, sources et decisions d'implementation |
| `GUIDE-utilisation-cahier-des-charges-projet-cible-grimoire-agent-os.md` | Mode d'emploi pour exploiter le cahier des charges |

## Decision Memory OS target

La cible Memory OS devient :

```text
Qdrant source de migration
-> bundle portable vector-lossless
-> Weaviate comme store vectoriel cible
-> Neo4j comme store graphe cible
```

Qdrant ne doit pas etre coupe tant que le bundle de migration n'a pas preserve les vecteurs, payloads, ids source, projections Neo4j et objets Weaviate.

## Decision structurante

Le projet cible n'est pas un orchestrateur de prompts.

Le projet cible est un systeme de pilotage agentique ou chaque action importante est :

- decrite par une mission et une task ;
- executee par une instance de workflow ;
- controlee par policies et hooks ;
- tracee par events et checkpoints ;
- prouvee par evidence ;
- consultable dans un cockpit ;
- distribuable sous forme de kit, packs et adapters.

## Source de verite

Le pivot canonique est :

```text
Mission -> Task -> WorkflowInstance -> RunEvent -> Checkpoint -> EvidencePack -> VerificationVerdict -> Closure
```

Tout document, UI, hook, pack, provider ou agent interne doit se raccorder a ce pivot.

## Regle d'execution par agents

Chaque lot de travail doit produire :

- un identifiant stable ;
- un scope clair ;
- des fichiers touches ou contrats touches ;
- des guardrails associes ;
- une preuve attendue ;
- un gate de validation ;
- un mode de promotion.

Un agent ne doit pas fermer une tache critique sans evidence et verdict de verification.
