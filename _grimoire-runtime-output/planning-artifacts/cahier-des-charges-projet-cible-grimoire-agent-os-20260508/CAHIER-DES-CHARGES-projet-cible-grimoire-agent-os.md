---
title: Cahier des charges - Projet cible Grimoire Agent OS
description: Specification detaillee du projet cible pour Grimoire Forge et grimoire-kit.
author: Codex
date: 2026-05-08
---

# Cahier des charges - Projet cible Grimoire Agent OS

## 1. Vision cible

Grimoire Agent OS est une plateforme de pilotage d'agents qui transforme une intention humaine en execution gouvernee, mesurable, explicable et reutilisable.

Le systeme cible doit permettre :

- de recevoir une mission depuis un humain, un IDE, une CLI, un MCP server, un runner externe ou une API ;
- de decomposer la mission en graphe de tasks ;
- d'affecter les tasks a des agents, workflows ou tools selon les capacites disponibles ;
- d'encadrer chaque action par des hooks et guardrails ;
- de tracer les decisions, evenements, checkpoints, outputs et refus ;
- de verifier les resultats avant fermeture ;
- de capitaliser les apprentissages dans une memoire gouvernee ;
- de distribuer les primitives dans grimoire-kit ;
- de prouver le fonctionnement dans Grimoire Forge.

La cible n'est pas seulement d'avoir plusieurs agents. La cible est d'avoir un systeme de controle qui rend les agents utiles, bornes et ameliorables.

## 2. Produits inclus

### 2.1 Grimoire Forge

Grimoire Forge est le chantier de reference et le cockpit produit.

Responsabilites :

- dogfood de toutes les primitives critiques ;
- orchestration user-facing via `grimoire-master` ;
- Mission Board ;
- vues hooks, evidence, policies, memory et packs ;
- integration IDE et workspace ;
- validation des contracts avant generalisation dans le kit ;
- environnement de reference pour les projets complexes.

Forge prouve la valeur et expose le pilotage.

### 2.2 grimoire-kit

grimoire-kit est le produit reutilisable.

Responsabilites :

- SDK ;
- CLI ;
- runtime kernel ;
- schemas ;
- pack registry ;
- adapters MCP, A2A, IDE, runners externes ;
- Memory OS primitives ;
- Weaviate vector store target ;
- Neo4j graph store target ;
- trace and eval ledger ;
- validation tools ;
- templates de projets agentiques.

Le kit ne doit pas contenir de logique specifique a Forge sauf sous forme de fixture, exemple ou pack.

### 2.3 Packs Grimoire

Les packs sont les unites distribuables.

Un pack peut contenir :

- commands ;
- recipes ;
- tools ;
- policies ;
- doctor checks ;
- services ;
- docs ;
- tests ;
- fixtures ;
- providers ;
- adapters ;
- skills.

Un pack ne peut pas activer une commande mutatrice sans manifest valide, lock et policy.

### 2.4 Adapters externes

Les adapters permettent d'integrer des ecosystemes sans les rendre obligatoires.

Sources prioritaires :

- Gastownhall et Gas City ;
- Beads ;
- CrewAI ;
- LangGraph ;
- OpenAI Agents SDK ;
- MCP ;
- A2A ;
- OpenTelemetry GenAI ;
- Langfuse ;
- CodeGraphContext ;
- Graphify ;
- agent-sandbox.

Chaque integration doit etre traduite dans les contrats Grimoire. Aucun format externe ne devient source de verite par defaut.

## 3. Objectifs produit

| ID | Objectif | Resultat attendu |
| --- | --- | --- |
| OBJ-001 | Piloter des agents avec preuve | Chaque task critique a evidence, trace et verdict |
| OBJ-002 | Eviter la fragmentation | Une source de verite pour missions, tasks et workflows |
| OBJ-003 | Industrialiser les workflows | Les procedures deviennent des recipes instanciables |
| OBJ-004 | Distribuer les capacites | Les primitives sortent sous forme de kit et packs |
| OBJ-005 | Gouverner les risques | Policies et hooks bornent les tools, packs et memoires |
| OBJ-006 | Mesurer la performance | Les runs exposent cout, qualite, erreurs et regressions |
| OBJ-007 | Integrer plusieurs hosts | IDE, CLI, MCP, API et runners partagent les memes contrats |
| OBJ-008 | Capitaliser le contexte | La memoire conserve decisions, preuves et patterns utiles |
| OBJ-009 | Rendre le systeme operable | Le cockpit explique et permet le controle humain |
| OBJ-010 | Rester extensible | Les projets externes entrent par packs ou adapters |

## 4. Non-objectifs

Le projet cible ne cherche pas a :

- remplacer tous les frameworks agents existants ;
- vendoriser les repos externes dans le noyau ;
- transformer chaque workflow en agent autonome ;
- lancer des hooks longs et fragiles ;
- stocker des prompts ou secrets dans les traces par defaut ;
- rendre la UI source de verite ;
- fermer les tasks sur declaration sans preuve ;
- multiplier les plans concurrents ;
- cacher les agents internes derriere plusieurs orchestrateurs visibles ;
- confondre demonstration et contrat stable.

## 5. Principes obligatoires

### 5.1 Source de verite unique

Le Mission Ledger est la source de verite pour missions, tasks, dependances, statut, claims, incidents et closure.

La UI, les docs, les hooks et les adapters ne doivent produire que des projections ou des events compatibles avec le ledger.

### 5.2 Execution instanciee

Une procedure reutilisable est une `Recipe`.

Une execution concrete est une `WorkflowInstance`.

Un agent ne doit pas seulement suivre un texte. Il doit travailler dans une instance identifiable, tracable et reprenable.

### 5.3 Evidence avant fermeture

Une task critique ne peut pas passer a l'etat ferme sans `EvidencePack` et `VerificationVerdict`.

### 5.4 Policy avant tool mutateur

Toute action capable de modifier workspace, reseau, secrets, services, packs ou memoire durable doit produire un `PolicyVerdict` avant execution.

### 5.5 Hooks courts et deterministes

Un hook doit orienter, bloquer ou enrichir. Il ne doit pas devenir un workflow long.

La logique durable vit dans le runtime, la CLI, le SDK ou un service versionne.

### 5.6 Packs verrouilles

Un pack actif doit avoir :

- manifest valide ;
- provenance ;
- compatibilite ;
- permissions ;
- lock ;
- doctor checks ;
- policy d'activation.

### 5.7 Memoire gouvernee

La memoire durable doit porter provenance, fraicheur, type, source et lien vers task ou evidence.

Une memoire contradictoire, non sourcee ou obsolete doit produire un avertissement et ne pas entrer dans un run critique sans decision explicite.

### 5.8 Agent interne invisible

`grimoire-master` reste l'orchestrateur user-facing.

Les agents specialises sont des ressources internes. Ils doivent publier leurs sorties via events, evidence et verdicts, pas via une UX concurrente.

## 6. Personas et usages

### 6.1 Operateur humain

Besoins :

- soumettre une mission ;
- comprendre l'etat ;
- voir les blocages ;
- approuver ou refuser des actions risquees ;
- consulter les preuves ;
- relancer ou interrompre une execution.

Interfaces :

- cockpit ;
- CLI ;
- IDE ;
- rapport Markdown ;
- notifications controlees.

### 6.2 Builder de projet agentique

Besoins :

- creer des recipes ;
- publier des packs ;
- definir des policies ;
- brancher des providers ;
- valider un projet avec doctor ;
- tester les guardrails.

Interfaces :

- grimoire-kit ;
- CLI ;
- schemas ;
- templates ;
- pack registry.

### 6.3 Agent executant

Besoins :

- recevoir une capsule de contexte minimale ;
- savoir quelle task executer ;
- connaitre les guardrails ;
- produire evidence ;
- signaler incidents ;
- eviter les collisions avec d'autres agents.

Interfaces :

- task contract ;
- workflow instance ;
- tool policy ;
- output schema ;
- evidence contract.

### 6.4 Mainteneur Grimoire

Besoins :

- faire evoluer les contrats ;
- detecter la derive doc/runtime ;
- maintenir compatibilite ;
- surveiller performance ;
- nettoyer les plans obsoletes ;
- gerer les migrations.

Interfaces :

- tests ;
- validators ;
- dashboards ;
- trace ledger ;
- ADR ;
- release gates.

### 6.5 Auteur de pack

Besoins :

- empaqueter une capacite ;
- declarer permissions ;
- fournir checks et tests ;
- publier avec provenance ;
- gerer compatibilite.

Interfaces :

- `pack.yaml` ;
- `pack.lock.json` ;
- doctor ;
- registry ;
- test harness.

## 7. Perimetre fonctionnel cible

### 7.1 Intake et qualification

Le systeme doit recevoir une demande et la transformer en mission qualifiee.

Capacites :

- detection du type de demande ;
- detection de risque ;
- mapping vers projet, repo, pack ou runtime ;
- creation de mission ;
- creation de tasks ;
- suggestion de workflow ;
- rappel des plans actifs ;
- detection des plans deprecies ;
- creation d'incident si contexte insuffisant bloque l'execution.

Sorties :

- `mission.created` ;
- `task.created` ;
- `task.qualified` ;
- capsule de contexte ;
- policy preview.

### 7.2 Mission Ledger

Le ledger doit stocker :

- missions ;
- tasks ;
- dependances ;
- claims ;
- statuts ;
- comments ;
- decisions ;
- incidents ;
- evidence refs ;
- memory refs ;
- workflow refs ;
- pack refs ;
- verification verdicts.

Il doit supporter :

- import/export JSONL ;
- mapping Beads ;
- queries `ready`, `blocked`, `claimed`, `stale`, `incident`, `needs_verification` ;
- transactions atomiques ;
- idempotence ;
- replay ;
- projection cockpit.

### 7.3 Runtime Kernel

Le runtime kernel doit fournir :

- execution de workflow instance ;
- event log ;
- checkpointing ;
- retries bornes ;
- pause ;
- resume ;
- abort ;
- policy evaluation ;
- tool mediation ;
- evidence collection ;
- trace emission ;
- host capability routing.

Il doit etre utilisable depuis :

- Forge ;
- grimoire-kit CLI ;
- SDK ;
- MCP server ;
- adapters externes.

### 7.4 Workflow Recipes

Une recipe decrit un processus reutilisable.

Elle contient :

- nom ;
- version ;
- input schema ;
- output schema ;
- steps ;
- roles ;
- tools autorises ;
- memory scopes ;
- policy profile ;
- evidence profile ;
- retry profile ;
- verification gates.

Une recipe peut provenir :

- d'un workflow Grimoire natif ;
- d'une formula Gas City convertie ;
- d'un Flow CrewAI converti ;
- d'un template LangGraph inspire ;
- d'un playbook interne.

### 7.5 Hooks and Guardrail Plane

Les hooks doivent couvrir :

- session start ;
- prompt submit ;
- pre tool use ;
- post tool use ;
- subagent start ;
- subagent stop ;
- pre compact ;
- stop.

Les guardrails doivent couvrir :

- tool mutation ;
- filesystem ;
- network ;
- secrets ;
- MCP ;
- pack activation ;
- memory injection ;
- destructive command ;
- source of truth ;
- closure without evidence ;
- stale context ;
- cross-repo collision.

### 7.6 Pack Registry

Le registry doit :

- valider les manifests ;
- calculer lock ;
- verifier provenance ;
- declarer trust tier ;
- exposer compatibility ;
- executer doctor checks ;
- installer en mode desactive par defaut ;
- activer par policy ;
- isoler experimental ;
- permettre rollback logique par version.

### 7.7 Memory OS

La memoire cible comprend :

- memoire de session ;
- memoire de mission ;
- memoire de projet ;
- memoire de code ;
- memoire de decisions ;
- memoire de patterns ;
- memoire d'incidents ;
- memoire de packs.

Collections cible :

- Weaviate `GrimoireKitMemory` pour les objets vectoriels et la recherche semantique ;
- Neo4j `GrimoireMemory`, `GrimoireTask`, `GrimoireEvidence`, `GrimoireFile`, `GrimoireDecision`, `GrimoirePack` pour le graphe causal ;
- exports OTel/Langfuse pour traces et evaluations ;
- ledger canonique pour mission, task, workflow, evidence et closure.

Decision cible :

- Weaviate remplace Qdrant comme backend vectoriel durable cible ;
- Neo4j remplace les graphes sidecar comme backend graphe durable cible ;
- Qdrant reste source de migration jusqu'a preuve de parite ;
- la migration passe par un bundle portable qui preserve vecteurs, payloads, ids source et projection Cypher ;
- aucune coupure Qdrant n'est autorisee avant verification `record_count == vector_count`.

La memoire doit pouvoir expliquer :

- pourquoi un contexte est injecte ;
- quelle source l'a cree ;
- quelle task l'a utilise ;
- quelle preuve le confirme ;
- si une contradiction existe.

### 7.8 Code Graph

Le Code Graph doit fournir :

- symboles ;
- fichiers ;
- fonctions ;
- classes ;
- imports ;
- tests associes ;
- ownership ;
- impact ;
- docs liees ;
- tasks liees ;
- hotspots ;
- zones sans couverture.

Il doit alimenter :

- routing ;
- context recall ;
- impact analysis ;
- verification suggestions ;
- doc drift ;
- cockpit.

### 7.9 Trace and Eval Ledger

Le trace ledger doit suivre :

- run id ;
- agent id ;
- host id ;
- model ;
- tool calls ;
- policy verdicts ;
- token usage si disponible ;
- latency si disponible ;
- errors ;
- retries ;
- evidence ;
- verification results ;
- quality score ;
- cost envelope si disponible.

Il doit pouvoir exporter vers :

- OpenTelemetry GenAI ;
- Langfuse ;
- fichiers JSONL ;
- dashboards locaux.

Les traces ne doivent pas stocker secrets, prompts complets ou outputs sensibles par defaut.

### 7.10 Cockpit Mission Board

Le cockpit cible doit afficher :

- missions ;
- task graph ;
- dependencies ;
- claims ;
- workflow instances ;
- checkpoints ;
- incidents ;
- evidence ;
- verification queue ;
- policies ;
- hook ledger ;
- memory refs ;
- pack status ;
- provider health ;
- performance ;
- regressions.

La UI est une projection. Toute mutation UI doit passer par API, policy et event.

### 7.11 Host Bridge

Le Host Bridge doit normaliser :

- Codex ;
- Claude ;
- GitHub Copilot ;
- CLI ;
- MCP ;
- external runners ;
- API clients.

Chaque host publie :

- capabilities ;
- hooks disponibles ;
- tool policy support ;
- workspace mutation support ;
- MCP support ;
- streaming support ;
- fallback mode.

Le runtime adapte le niveau de controle selon les capacites reelles.

### 7.12 Interop Agent-Agent

L'interop externe doit utiliser A2A ou adapter compatible.

Concepts :

- Agent Card ;
- Task ;
- Message ;
- Artifact ;
- capability ;
- extension ;
- policy ;
- trace ;
- evidence.

Un agent externe ne peut pas contourner le ledger.

## 8. Architecture logique

Le systeme cible est compose de sept plans.

| Plan | Role | Source de verite |
| --- | --- | --- |
| Experience Plane | IDE, CLI, cockpit, reports | Projections |
| Orchestration Plane | mission intake, routing, task graph | Mission Ledger |
| Execution Plane | workflow instances, runners, providers | Runtime Kernel |
| Control Plane | hooks, policies, guardrails | Policy Engine |
| Knowledge Plane | memory, code graph, docs graph | Memory OS |
| Extension Plane | packs, adapters, registry | Pack Registry |
| Observability Plane | traces, evals, performance | Trace and Eval Ledger |

## 9. Composants majeurs

### 9.1 Mission Intake

Responsabilites :

- recevoir demande ;
- extraire intention ;
- detecter scope ;
- associer projet ;
- proposer tasks ;
- produire premier risk profile.

Contrats :

- input request ;
- mission draft ;
- task proposals ;
- policy preview.

### 9.2 Mission Ledger

Responsabilites :

- task graph ;
- state machine ;
- dependencies ;
- events ;
- closure ;
- query ready.

Contrats :

- `Mission` ;
- `MissionTask` ;
- `TaskDependency` ;
- `LedgerEvent` ;
- `Incident`.

### 9.3 Runtime Kernel

Responsabilites :

- workflow lifecycle ;
- checkpoint ;
- replay ;
- tool mediation ;
- event emission ;
- host routing.

Contrats :

- `WorkflowInstance` ;
- `RunEvent` ;
- `Checkpoint` ;
- `ExecutionContext` ;
- `RuntimeError`.

### 9.4 Policy Engine

Responsabilites :

- decide allow, warn, block ;
- compiler policies ;
- verifier permissions ;
- enregistrer verdict ;
- expliquer refus.

Contrats :

- `PolicyRequest` ;
- `PolicyVerdict` ;
- `PolicyRule` ;
- `RiskProfile`.

### 9.5 Evidence Service

Responsabilites :

- collecter preuves ;
- normaliser preuves ;
- lier aux tasks ;
- verifier presence minimale ;
- preparer closure.

Contrats :

- `EvidencePack` ;
- `EvidenceItem` ;
- `VerificationRequest` ;
- `VerificationVerdict`.

### 9.6 Memory OS

Responsabilites :

- recall ;
- promotion ;
- freshness ;
- contradiction ;
- provenance ;
- hot memory ;
- vector memory ;
- graph memory.

Backends cible :

- `weaviate-server` pour la memoire semantique vectorielle ;
- `neo4j` pour knowledge graph, memory graph, code graph et task memory ;
- `qdrant-server` comme source de migration et rollback tant que la parite n'est pas prouvee.

Contrats :

- `MemoryRecord` ;
- `MemoryRef` ;
- `RecallRequest` ;
- `RecallResult` ;
- `PromotionCandidate`.

### 9.7 Code Graph

Responsabilites :

- index code ;
- calcul impact ;
- lier tests ;
- lier docs ;
- supporter retrieval.

Contrats :

- `CodeNode` ;
- `CodeEdge` ;
- `ImpactQuery` ;
- `ImpactResult`.

### 9.8 Pack Registry

Responsabilites :

- validation manifest ;
- lock ;
- activation ;
- doctor ;
- permissions ;
- compatibility.

Contrats :

- `PackManifest` ;
- `PackLock` ;
- `PackActivation` ;
- `PackDoctorResult`.

### 9.9 Host Bridge

Responsabilites :

- capability detection ;
- adapter host ;
- normalize tool events ;
- apply fallback ;
- route providers.

Contrats :

- `HostCapabilityManifest` ;
- `HostSession` ;
- `HostToolEvent` ;
- `HostFallbackPlan`.

### 9.10 Cockpit API

Responsabilites :

- exposer read models ;
- accepter mutations controlees ;
- afficher etat ;
- fournir drilldown evidence ;
- afficher performance.

Contrats :

- `MissionProjection` ;
- `WorkflowProjection` ;
- `PolicyProjection` ;
- `MemoryProjection` ;
- `PackProjection`.

## 10. Etats canoniques

### 10.1 Mission

| Etat | Sens |
| --- | --- |
| `draft` | Mission detectee mais pas qualifiee |
| `open` | Mission active |
| `blocked` | Blocage global |
| `verifying` | Fermeture en verification |
| `closed` | Mission terminee avec preuves |
| `cancelled` | Mission annulee avec raison |

### 10.2 Task

| Etat | Sens |
| --- | --- |
| `proposed` | Task suggeree |
| `ready` | Executable |
| `claimed` | Agent ou runner assigne |
| `running` | Execution active |
| `blocked` | Dependance ou incident |
| `needs_verification` | Sortie produite, verification requise |
| `failed` | Echec prouve |
| `closed` | Terminee avec evidence |
| `cancelled` | Annulee |

### 10.3 Workflow Instance

| Etat | Sens |
| --- | --- |
| `created` | Instance creee |
| `running` | Steps actifs |
| `checkpointed` | Etat durable sauve |
| `paused` | Pause explicite |
| `blocked` | Incident ou policy |
| `aborted` | Interrompu avec raison |
| `completed` | Sortie produite |
| `verified` | Sortie acceptee |

### 10.4 Pack

| Etat | Sens |
| --- | --- |
| `discovered` | Pack detecte |
| `validated` | Manifest valide |
| `locked` | Lock calcule |
| `disabled` | Installe sans activation |
| `active_shadow` | Observe sans effet critique |
| `active_canary` | Effet borne |
| `active_enforced` | Effet complet autorise |
| `quarantined` | Bloque par policy |

## 11. Modes de pilotage agentique

### 11.1 Pilotage manuel assiste

L'humain decide, Grimoire structure et verifie.

Usage :

- analyse ;
- specification ;
- revue ;
- migrations sensibles ;
- arbitrages produit.

Obligatoire :

- task graph ;
- evidence ;
- verification ;
- cockpit lisible.

### 11.2 Pilotage semi-autonome

Grimoire execute les tasks pretes avec validation humaine sur les points risques.

Usage :

- implementation ;
- docs ;
- tests ;
- refactors bornes ;
- packs experimentaux.

Obligatoire :

- policy before tool ;
- checkpoints ;
- incidents explicites ;
- gates de sortie.

### 11.3 Pilotage autonome borne

Grimoire execute des workflows repetables dans un perimetre pre-approuve.

Usage :

- doctor checks ;
- generation de projections ;
- imports ;
- validations ;
- synchronisation ledger.

Obligatoire :

- recipes stables ;
- permissions minimales ;
- replay ;
- logs ;
- refusal path.

### 11.4 Pilotage multi-agent parallele

Plusieurs agents travaillent sur des tasks disjointes.

Usage :

- exploration de repos ;
- implementation par modules ;
- verification parallele ;
- migration de packs.

Obligatoire :

- claims atomiques ;
- ownership de fichiers ;
- contracts de sortie ;
- merge policy ;
- collision detection.

### 11.5 Pilotage externe par adapter

Un runner externe execute mais Grimoire conserve le controle.

Usage :

- CrewAI runner ;
- LangGraph graph ;
- OpenAI Agents SDK ;
- external service ;
- browser automation ;
- sandbox execution.

Obligatoire :

- adapter contract ;
- trace canonicalisee ;
- evidence importee ;
- policy boundary ;
- fallback.

## 12. Performance et efficacite

### 12.1 Mesures principales

| Mesure | Definition | Usage |
| --- | --- | --- |
| Lead to first task | Ecart entre demande et premiere task qualifiee | Mesurer intake |
| Ready throughput | Nombre de tasks pretes executees par cycle de traitement | Mesurer ledger |
| Completion quality | Pourcentage de tasks fermees sans reouverture | Mesurer sortie |
| Evidence completeness | Ratio de preuves attendues presentes | Mesurer rigueur |
| Policy hit rate | Warnings et blocks par famille de risque | Mesurer securite |
| Context efficiency | Taille contexte utile contre contexte injecte | Mesurer memory |
| Replay success | Runs rejouables sans divergence critique | Mesurer kernel |
| Pack activation success | Packs valides actives sans incident | Mesurer registry |
| Human intervention rate | Interventions par risk profile | Mesurer autonomie |
| Regression rate | Echecs detectes apres changement de contract | Mesurer qualite |

### 12.2 Objectif de performance

Le systeme doit optimiser :

- moins de contexte inutile ;
- moins de collisions ;
- moins de rework ;
- plus de fermeture prouvee ;
- meilleure detection de risque ;
- meilleure reuse de recipes ;
- meilleure observabilite des refus.

La performance n'est pas seulement vitesse. Elle inclut exactitude, cout, stabilite, preuve et capacite de reprise.

### 12.3 Points de mesure obligatoires

Le runtime doit emettre des events pour :

- creation mission ;
- qualification task ;
- claim ;
- start workflow ;
- tool requested ;
- policy verdict ;
- tool completed ;
- checkpoint ;
- incident ;
- evidence captured ;
- verification requested ;
- verification passed or failed ;
- closure.

## 13. Securite

### 13.1 Risques principaux

| Risque | Exemple | Controle |
| --- | --- | --- |
| Tool misuse | Commande shell dangereuse | PreToolUse policy |
| Memory poisoning | Memoire non sourcee injectee | provenance + freshness |
| Pack supply chain | Pack externe active commande | manifest + lock + trust tier |
| Prompt injection | Instruction externe contredit runtime | source hierarchy + guardrail |
| Secret leakage | Trace stocke token | redaction by default |
| Cross-agent collision | Deux agents modifient meme module | claim + ownership |
| Silent failure | Workflow bloque sans incident | no hidden stall |
| UI bypass | Mutation depuis cockpit sans event | API policy |
| External runner drift | Runner externe ferme sans preuve | adapter evidence gate |
| Doc/runtime drift | Plan actif diverge du code | validation + doc drift check |

### 13.2 Tiers de confiance

| Tier | Usage |
| --- | --- |
| `core` | Runtime, ledger, policy, schemas |
| `trusted` | Packs maintenus dans organisation |
| `reviewed` | Packs externes verifies |
| `experimental` | Packs en incubation |
| `quarantined` | Packs bloques |

Un tier eleve ne supprime pas les policies. Il reduit seulement la friction quand les preuves sont presentes.

## 14. Distribution

### 14.1 Modes de livraison

Le projet cible doit permettre :

- installation locale ;
- usage repo-native ;
- usage via CLI ;
- usage via MCP ;
- usage SDK ;
- usage service ;
- usage cockpit ;
- usage pack.

### 14.2 Compatibilite

Chaque composant public doit declarer :

- version contract ;
- compatibility range ;
- migration path ;
- deprecation reason ;
- schema version ;
- test fixture.

## 15. Gouvernance documentaire

### 15.1 Documents actifs

Le systeme documentaire doit distinguer :

- cahier des charges cible ;
- plan directeur actif ;
- backlog unifie ;
- registre de plans deprecies ;
- ADR ;
- contracts ;
- guides d'execution ;
- reports historiques.

### 15.2 Regle anti-fragmentation

Un nouveau document ne peut pas introduire une source de verite concurrente.

Il doit declarer :

- son role ;
- son lien vers mission, task, contract ou ADR ;
- son statut ;
- sa relation aux plans precedents.

## 16. Definition de reussite

Le projet cible est atteint quand :

- une mission complexe peut etre intake, decomposed, executee, verifiee et fermee sans source de verite parallele ;
- les agents peuvent travailler en parallele sans collisions non detectees ;
- les hooks bloquent les actions critiques avec explication exploitable ;
- les packs externes peuvent etre importes sans compromettre le noyau ;
- les workflows sont instancies, reprenables et comparables ;
- la memoire injectee est sourcee, fraiche et auditable ;
- le cockpit montre l'etat reel issu du runtime ;
- les traces permettent d'analyser performance, cout, erreurs et regressions ;
- grimoire-kit permet de creer un nouveau projet agentique avec les memes primitives ;
- Forge reste le terrain de preuve et non un fork specifique.

## 17. Trace vers les inspirations externes

| Inspiration | Element retenu | Traduction Grimoire |
| --- | --- | --- |
| Gastownhall | Mayor, rigs, convoys, packs, provider tiers | grimoire-master, Host Bridge, Pack Registry |
| Beads | work graph, ready query, dependencies | Mission Ledger |
| Gas City | formulas, orders, supervisor | Recipes, WorkflowInstance, Runtime Kernel |
| CrewAI | crews, flows, tasks, guardrails | recipe adapter, task output schemas |
| LangGraph | durable execution, checkpoints | workflow lifecycle |
| OpenAI Agents SDK | handoffs, tools, guardrails, tracing | policy and trace patterns |
| MCP | tools and resources protocol | default integration transport |
| A2A | agent-agent interop | external agent adapter |
| OTel GenAI | trace conventions | trace export |
| OWASP Agentic | threat model | guardrails and red-team gates |

## 18. Regles de conception pour implementation

Toute implementation doit respecter :

- schemas avant UI ;
- events avant projections ;
- evidence avant closure ;
- policy avant mutation ;
- locks avant activation ;
- adapters avant vendorisation ;
- dogfood Forge avant generalisation kit ;
- validation avant promotion ;
- incidents visibles ;
- refus explicables.

## 19. Questions d'architecture deja tranchees

| Sujet | Decision cible |
| --- | --- |
| Source de verite | Mission Ledger |
| Runtime | grimoire-kit Runtime Kernel |
| UI | projection cockpit |
| Distribution | packs gouvernes |
| Memoire | Memory OS avec provenance |
| Vector DB cible | Weaviate |
| Graph DB cible | Neo4j |
| Vector DB source | Qdrant jusqu'a migration verifiee |
| Interop | MCP et A2A via adapters |
| Observabilite | Trace and Eval Ledger |
| Securite | policy engine + hooks + evidence |
| Agents visibles | `grimoire-master` seul |
| Fusion externe | adapters, converters, packs |

## 20. Contrat final de produit

Grimoire Agent OS doit etre capable de prendre une organisation de travail agentique complexe et de la rendre :

- comprehensible ;
- verifiable ;
- gouvernee ;
- reusable ;
- mesurable ;
- extensible ;
- distribuable.

La valeur n'est pas dans le nombre d'agents. La valeur est dans la capacite a transformer leur travail en execution fiable, tracable et ameliorable.
