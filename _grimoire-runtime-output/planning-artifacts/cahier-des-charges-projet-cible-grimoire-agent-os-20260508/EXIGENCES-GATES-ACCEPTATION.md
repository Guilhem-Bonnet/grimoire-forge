---
title: Exigences et gates d'acceptation - Grimoire Agent OS
description: Exigences fonctionnelles, non fonctionnelles, securite, observabilite et validation cible.
author: Codex
date: 2026-05-08
---

# Exigences et gates d'acceptation - Grimoire Agent OS

## 1. Methode

Chaque exigence porte :

- un identifiant ;
- une intention ;
- un composant responsable ;
- une preuve attendue ;
- un gate de validation.

Les niveaux de risque sont :

- `light` ;
- `standard` ;
- `strict` ;
- `security_critical` ;
- `release`.

## 2. Exigences fonctionnelles

| ID | Exigence | Responsable | Preuve | Gate |
| --- | --- | --- | --- | --- |
| FR-001 | Creer une mission depuis une demande humaine | Mission Intake | event `mission.created` | mission visible dans ledger |
| FR-002 | Decomposer une mission en tasks atomiques | Mission Intake | events `task.created` | tasks liees a mission |
| FR-003 | Qualifier chaque task par type, risque et surface | Task Router | event `task.qualified` | task non executable sans qualification |
| FR-004 | Calculer les tasks pretes selon dependances | Mission Ledger | query `ready` | task bloquee exclue |
| FR-005 | Claim atomique d'une task par agent ou runner | Mission Ledger | event `task.claimed` | collision refusee |
| FR-006 | Instancier une recipe en workflow | Runtime Kernel | `WorkflowInstance` | instance liee a task |
| FR-007 | Emettre events runtime pour chaque step critique | Runtime Kernel | `RunEvent` | trace complete |
| FR-008 | Creer checkpoints reprenables | Runtime Kernel | `Checkpoint` | resume sans double effet |
| FR-009 | Evaluer policy avant tool mutateur | Policy Engine | `PolicyVerdict` | tool bloque si verdict absent |
| FR-010 | Capturer evidence apres sortie | Evidence Service | `EvidencePack` | evidence liee a task |
| FR-011 | Verifier task avant fermeture | Verification Service | `VerificationVerdict` | close refuse sans verdict |
| FR-012 | Exposer projection cockpit | Cockpit API | read model | etat coherent avec ledger |
| FR-013 | Installer pack en mode desactive par defaut | Pack Registry | manifest + lock | pas de commande mutatrice activee |
| FR-014 | Activer pack par policy | Pack Registry | `PackActivation` | activation refusee si lock manque |
| FR-015 | Importer Beads JSONL | Ledger Adapter | import report | idempotence prouvee |
| FR-016 | Exporter tasks au format JSONL | Ledger Adapter | export report | ids et dependances conserves |
| FR-017 | Convertir Gas City pack.toml | Pack Converter | converted manifest | doctor et schema passent |
| FR-018 | Convertir CrewAI Flow en recipe experimentale | CrewAI Adapter | recipe generated | output schema present |
| FR-019 | Publier host capability manifest | Host Bridge | manifest | runtime adapte fallback |
| FR-020 | Router tool selon capability et policy | Host Bridge | policy trace | mutation bornee |
| FR-021 | Injecter memoire avec provenance | Memory OS | recall result | memoire non sourcee exclue |
| FR-022 | Promouvoir memoire apres verification | Memory OS | memory event | source et task liees |
| FR-023 | Construire Code Graph | Code Graph | graph snapshot | symboles et tests lies |
| FR-024 | Calculer impact fichier | Code Graph | impact result | tests suggerees |
| FR-025 | Exporter traces OTel compatibles | Trace Ledger | export file | secrets redactes |
| FR-026 | Creer incident sur blocage | Runtime Kernel | incident event | blocage visible |
| FR-027 | Refuser fermeture avec incident critique ouvert | Verification | verdict failed | task reste ouverte |
| FR-028 | Supporter cockpit policy view | Cockpit | projection | refus explique |
| FR-029 | Supporter cockpit evidence view | Cockpit | projection | preuve consultable |
| FR-030 | Supporter doctor global | CLI | doctor output | checks contracts passent |
| FR-031 | Supporter `weaviate-server` comme backend memoire | Memory OS | config + backend | status reconnait Weaviate |
| FR-032 | Supporter `neo4j` comme mode graph memory | Memory OS | config + status | graph layers reconnus |
| FR-033 | Exporter bundle Qdrant vers Weaviate Neo4j | CLI Memory | manifest + JSONL + Cypher | bundle vector-lossless |
| FR-034 | Conserver Qdrant jusqu'a parite | Migration | config migration | backend non coupe avant gate |
| FR-035 | Preserver ids source dans Weaviate et Neo4j | Migration | weaviate object + cypher | source_id et node id presents |
| FR-036 | Projeter le code dans Weaviate avec IDs stables | Memory OS | chunks code + `content_hash` | `grimoire memory vector verify` |
| FR-037 | Relier les projections vectorielles au graphe | Memory OS + Neo4j | relations `MEMORY_FOR` | stats Neo4j et graph verify |
| FR-038 | Distinguer migration et projections runtime | Migration | projections exclues des counts bundle | `memory migrate verify` reste centré sur les 68 souvenirs migrés |

## 3. Exigences non fonctionnelles

| ID | Exigence | Mesure | Gate |
| --- | --- | --- | --- |
| NFR-001 | Idempotence des imports | import repete sans doublons | snapshot identique |
| NFR-002 | Replay des runs critiques | replay produit sequence compatible | divergence bloquee |
| NFR-003 | Context efficiency | contexte injecte source et limite | capsule auditable |
| NFR-004 | Observabilite complete | events pour chaque transition critique | trace sans trou |
| NFR-005 | Degradation controlee | fallback si host limite | capability manifest respecte |
| NFR-006 | Extensibilite pack | pack externe sans code core | adapter ou manifest |
| NFR-007 | Compatibilite schema | validators publics | fixture valide |
| NFR-008 | Lisibilite cockpit | projection explique etat | aucun statut opaque |
| NFR-009 | Performance de query ready | query stable sur graph charge | index present |
| NFR-010 | Isolation des stores | ledger, evidence, memory, trace separes | ownership clair |
| NFR-011 | Portabilite locale | mode local sans service cloud obligatoire | doctor local passe |
| NFR-012 | Portabilite equipe | backend partage possible | config documentee |
| NFR-013 | Controle des ressources | runners limites par policy | abus bloque |
| NFR-014 | Robustesse checkpoint | resume apres interruption | side effects non doubles |
| NFR-015 | Maintenabilite docs | doc liee aux contracts | drift detecte |

## 4. Exigences securite

| ID | Exigence | Gate |
| --- | --- | --- |
| SEC-001 | Commandes destructives bloquees par defaut | test negatif |
| SEC-002 | Secrets jamais traces en clair par defaut | redaction test |
| SEC-003 | Pack externe en `experimental` par defaut | activation policy |
| SEC-004 | Commande shell pack desactivee par defaut | manifest validation |
| SEC-005 | MCP tools mutateurs soumis a policy | verdict obligatoire |
| SEC-006 | Memoire non sourcee exclue des runs stricts | recall gate |
| SEC-007 | Prompt externe classe comme non fiable | source hierarchy |
| SEC-008 | Agent externe sans evidence ne ferme rien | adapter gate |
| SEC-009 | Host sans hooks declare fallback | capability gate |
| SEC-010 | Audit trail pour mutation critique | event + policy + evidence |
| SEC-011 | Trust tier pack non social | lock + provenance + checks |
| SEC-012 | Sandbox pour commands experimentees | provider sandbox |
| SEC-013 | Incident cree sur policy block critique | incident event |
| SEC-014 | UI ne contourne pas policy | API mutation test |
| SEC-015 | Refus explique en langage exploitable | verdict reason |
| SEC-016 | Secrets Neo4j et Weaviate par variables d'environnement | config schema |
| SEC-017 | Migration non destructive par bundle portable | manifest |

## 5. Exigences d'observabilite

| ID | Exigence | Event ou sortie |
| --- | --- | --- |
| OBS-001 | Tracer mission creation | `mission.created` |
| OBS-002 | Tracer task lifecycle | `task.*` |
| OBS-003 | Tracer workflow lifecycle | `workflow.*` |
| OBS-004 | Tracer tool request and completion | `tool.requested`, `tool.completed` |
| OBS-005 | Tracer policy | `policy.evaluated` |
| OBS-006 | Tracer checkpoint | `workflow.checkpointed` |
| OBS-007 | Tracer evidence | `evidence.captured` |
| OBS-008 | Tracer verification | `verification.*` |
| OBS-009 | Tracer memory recall | `memory.recalled` |
| OBS-010 | Tracer memory promotion | `memory.promoted` |
| OBS-011 | Tracer pack activation | `pack.activated` |
| OBS-012 | Tracer incident | `incident.created` |
| OBS-013 | Exporter OTel GenAI compatible | export validated |
| OBS-014 | Redacter donnees sensibles | redaction proof |
| OBS-015 | Relier trace a task et evidence | join query |

## 6. Gates par composant

### 6.1 Gate Mission Ledger

Pour accepter le ledger :

- CRUD mission et task ;
- dependances `blocks`, `relates`, `parent_child`, `discovered_from`, `supersedes` ;
- query `ready` ;
- claim atomique ;
- import/export JSONL ;
- state machine ;
- closure refusee sans verification ;
- projection cockpit generable.

### 6.2 Gate Runtime Kernel

Pour accepter le runtime :

- create workflow instance ;
- start ;
- checkpoint ;
- pause ;
- resume ;
- abort ;
- event log ;
- policy mediation ;
- evidence capture ;
- replay test.

### 6.3 Gate Policy Engine

Pour accepter la policy :

- `allow`, `warn`, `block` ;
- modes `shadow`, `canary`, `enforced` ;
- raison explicable ;
- rules versionnees ;
- negative tests ;
- pack activation checks ;
- tool mutation checks.

### 6.4 Gate Pack Registry

Pour accepter le registry :

- manifest schema ;
- lock ;
- doctor ;
- trust tier ;
- compatibility ;
- commands disabled by default ;
- activation policy ;
- quarantine.

### 6.5 Gate Memory OS

Pour accepter la memoire :

- recall avec provenance ;
- freshness ;
- contradiction ;
- promotion gate ;
- memory refs vers tasks ;
- exclusion en strict si provenance manque ;
- projection cockpit.

### 6.6 Gate Code Graph

Pour accepter le graph :

- index symboles ;
- imports ;
- tests lies ;
- docs liees ;
- impact query ;
- ownership ;
- invalidation apres changement.

### 6.7 Gate Cockpit

Pour accepter le cockpit :

- mission board ;
- task graph ;
- workflow instance view ;
- checkpoint view ;
- evidence view ;
- policy view ;
- incident view ;
- pack view ;
- memory view ;
- performance view ;
- aucune source de verite UI parallele.

## 7. Gates transverses

| ID | Gate | Critere |
| --- | --- | --- |
| GATE-001 | No hidden source | toute mutation produit event |
| GATE-002 | Evidence first | toute closure critique a pack preuve |
| GATE-003 | Policy before mutation | aucun mutateur sans verdict |
| GATE-004 | Replay ready | run critique rejouable |
| GATE-005 | Pack safe by default | pack installe sans activation risquee |
| GATE-006 | Memory sourced | contexte critique source |
| GATE-007 | Host honest | capability declaree et respectee |
| GATE-008 | Incident visible | blocage non silencieux |
| GATE-009 | Adapter subordinate | runner externe ne ferme rien seul |
| GATE-010 | Contract tested | schema public a fixture |
| GATE-011 | Vector migration lossless | `record_count == vector_count` |
| GATE-012 | Dual store parity | Qdrant, Weaviate et Neo4j contiennent les ids source |
| GATE-013 | Runtime vector projection parity | projections attendues présentes avec `content_hash` courant |
| GATE-014 | Memory graph link parity | chaque projection vectorielle sourcee a son lien graph attendu |

## 8. Profils de preuve

| Profil | Preuve minimale |
| --- | --- |
| light | source, decision, doc link |
| standard | validation cible ou test comportemental |
| strict | test, schema validation, replay ou checkpoint |
| security_critical | test negatif, audit trail, policy explicite |
| release | doctor, lock, compatibility, changelog, evidence pack |

## 9. Matrice risque vers controle

| Risque | Controle minimal |
| --- | --- |
| read only analysis | source + doc proof |
| doc write | diff + validation markdown |
| code write | tests + evidence |
| runtime contract | schema + replay |
| policy change | negative tests |
| pack activation | lock + doctor + policy |
| memory promotion | provenance + verification |
| external adapter | trace + evidence import |
| security boundary | audit + refusal tests |
| release | full doctor + compatibility |

## 10. Definition of Ready

Une task est prete si :

- elle a un titre clair ;
- elle a une mission ;
- elle a un type ;
- elle a un risk profile ;
- ses dependances bloquantes sont fermees ou absentes ;
- ses inputs sont disponibles ;
- ses acceptance criteria sont explicites ;
- son evidence profile est declare ;
- son owner ou routage est possible.

## 11. Definition of Closed

Une task est fermee si :

- workflow termine ou decision documentee ;
- evidence pack present ;
- acceptance criteria couverts ;
- verification verdict passe ;
- incidents critiques resolus ou acceptes par decision explicite ;
- ledger event `task.closed` emis ;
- projection cockpit actualisee depuis le ledger.

## 12. Anti-patterns bloquants

Un changement doit etre refuse si :

- il ajoute une roadmap parallele ;
- il contourne le ledger ;
- il active une commande pack sans lock ;
- il ferme une task sans evidence ;
- il stocke secret dans trace ;
- il injecte memoire non sourcee en mode strict ;
- il vendorise un projet externe dans le core sans adapter ;
- il transforme un hook en workflow long ;
- il rend un agent interne user-facing sans decision ;
- il fait de la UI une source de verite.

## 13. Checklist d'acceptation globale

- [ ] Mission Ledger source de verite
- [ ] Runtime Kernel avec workflow instances
- [ ] Policy Engine operationnel
- [ ] Evidence Service obligatoire pour closure critique
- [ ] Pack Registry avec lock et doctor
- [ ] Memory OS avec provenance
- [ ] Code Graph exploitable
- [ ] Host Bridge capability-aware
- [ ] Cockpit par projections
- [ ] Trace and Eval Ledger
- [ ] Adapters Beads, Gas City, CrewAI experimentaux
- [ ] Exports MCP, A2A, OTel
- [ ] Doctor global
- [ ] Fixtures schema
- [ ] Gates security
