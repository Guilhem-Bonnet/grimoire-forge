---
title: Dossier d'execution par agents - Grimoire Agent OS cible
description: Lots de travail adaptes aux agents, avec hooks, guardrails, preuves et gates.
author: Codex
date: 2026-05-08
---

# Dossier d'execution par agents - Grimoire Agent OS cible

## 1. Regle generale

Les agents executent des lots bornes.

Chaque lot doit declarer :

- id ;
- objectif ;
- surface ;
- fichiers ou modules probables ;
- dependances ;
- hooks attendus ;
- guardrails ;
- evidence ;
- gate ;
- mode de promotion.

Aucun lot ne doit supposer une duree. Le routage se fait par readiness, risque, ownership et preuve.

## 2. Lot A - Source de verite et nettoyage

### LOT-A1 - Declarer le paquet cible actif

Objectif :

- enregistrer le cahier des charges cible comme reference de produit cible.

Surface :

- `_grimoire-runtime-output/planning-artifacts/` ;
- registres docs ;
- index planning.

Guardrails :

- ne pas supprimer les anciens rapports ;
- classer au lieu de detruire ;
- conserver provenance.

Evidence :

- index lisible ;
- lien vers plan directeur ;
- registre des documents actifs.

Gate :

- un agent peut trouver le plan actif sans relire toutes les references.

### LOT-A2 - Registre des plans deprecies

Objectif :

- unifier anciens plans, rapports et addenda sous un registre de statut.

Guardrails :

- pas de suppression destructive ;
- mapping ancien vers nouveau ;
- decision explicite pour `active`, `absorbed`, `archive`, `incubator`.

Evidence :

- registre actualise ;
- aucun document actif concurrent.

Gate :

- une nouvelle task reference le plan cible ou le backlog unifie.

## 3. Lot B - Mission Ledger

### LOT-B1 - Schemas ledger

Objectif :

- creer schemas `Mission`, `MissionTask`, `TaskDependency`, `LedgerEvent`, `Incident`.

Surface :

- grimoire-kit schemas ;
- validators ;
- fixtures.

Hooks :

- UserPromptSubmit ;
- PostToolUse ;
- Stop.

Guardrails :

- schema version obligatoire ;
- ids stables ;
- state machine explicite.

Evidence :

- schema validation ;
- fixtures positives et negatives.

Gate :

- task invalide refusee.

### LOT-B2 - Query ready et dependances

Objectif :

- implementer `ready`, `blocked`, `needs_verification`, `incident`.

Guardrails :

- dependance `blocks` interdit execution ;
- claim atomique ;
- aucun close sans verification.

Evidence :

- tests sur graph avec dependances ;
- import/export idempotent.

Gate :

- une task bloquee ne sort jamais dans `ready`.

### LOT-B3 - Adapter Beads

Objectif :

- importer/exporter JSONL compatible Beads sans rendre Beads obligatoire.

Guardrails :

- adapter seulement ;
- preservation provenance ;
- idempotence.

Evidence :

- fixture Beads ;
- mapping report ;
- second import sans doublon.

Gate :

- tasks et dependencies conservees.

## 4. Lot C - Runtime Kernel

### LOT-C1 - Contrats WorkflowInstance et RunEvent

Objectif :

- definir lifecycle runtime canonique.

Surface :

- grimoire-kit runtime ;
- schemas ;
- tests.

Guardrails :

- event pour transition critique ;
- run id obligatoire ;
- task id obligatoire.

Evidence :

- schema tests ;
- event log fixture.

Gate :

- workflow sans task refuse.

### LOT-C2 - Checkpoint et resume

Objectif :

- rendre les workflows reprenables sans doubler les effets.

Guardrails :

- idempotency key ;
- side effects declares ;
- abort reason.

Evidence :

- test resume ;
- test interruption ;
- checkpoint fixture.

Gate :

- replay critique sans divergence.

### LOT-C3 - Tool mediation

Objectif :

- faire passer les tools par policy.

Guardrails :

- mutateur sans verdict bloque ;
- shell critique bloque par defaut ;
- policy reason obligatoire.

Evidence :

- negative tests ;
- trace policy.

Gate :

- aucun tool mutateur ne s'execute sans verdict.

## 5. Lot D - Recipes et workflows

### LOT-D1 - Recipe schema

Objectif :

- formaliser les procedures en recipes versionnees.

Guardrails :

- input schema ;
- output schema ;
- evidence profile ;
- policy profile.

Evidence :

- schema ;
- fixture recipe ;
- validation.

Gate :

- recipe sans output schema refusee.

### LOT-D2 - Conversion Gas City formulas

Objectif :

- convertir formulas en recipes experimentales.

Guardrails :

- pas de commande activee ;
- provenance upstream ;
- status experimental.

Evidence :

- converter report ;
- recipe generated ;
- doctor.

Gate :

- conversion deterministe.

### LOT-D3 - Conversion CrewAI Flows

Objectif :

- convertir Flow et Tasks en recipes ou runner adapter.

Guardrails :

- CrewAI ne remplace pas le kernel ;
- output schema obligatoire ;
- external trace normalisee.

Evidence :

- mapping report ;
- sample flow converted ;
- trace import.

Gate :

- flow execute via adapter sans fermer task seul.

## 6. Lot E - Hook and Guardrail Plane

### LOT-E1 - Hook registry

Objectif :

- declarer hooks disponibles, modes et sorties attendues.

Guardrails :

- mode `shadow` par defaut ;
- digest pour enforced ;
- raison de block obligatoire.

Evidence :

- registry ;
- fixture verdict ;
- smoke hook.

Gate :

- hook inconnu refuse en enforced.

### LOT-E2 - Terminal guard

Objectif :

- controler commandes shell critiques.

Guardrails :

- destructive command block ;
- explicit proof for risky change ;
- no silent allow.

Evidence :

- negative tests ;
- incident on block.

Gate :

- commande destructive bloquee.

### LOT-E3 - Closure guard

Objectif :

- empecher fermeture sans evidence.

Guardrails :

- `EvidencePack` ;
- `VerificationVerdict` ;
- incident check.

Evidence :

- test close refused ;
- test close accepted.

Gate :

- task critique ne ferme pas sans preuve.

## 7. Lot F - Pack Registry

### LOT-F1 - Pack manifest et validator

Objectif :

- definir `pack.yaml` cible.

Guardrails :

- provenance ;
- compatibility ;
- permissions ;
- commands disabled by default.

Evidence :

- schema ;
- fixtures ;
- validator.

Gate :

- pack invalide refuse.

### LOT-F2 - Pack lock

Objectif :

- calculer lock et digest.

Guardrails :

- lock requis pour activation ;
- mismatch bloque.

Evidence :

- lock file ;
- digest verification.

Gate :

- activation refusee si lock manque ou diverge.

### LOT-F3 - Pack doctor

Objectif :

- fournir checks pack-level et global.

Guardrails :

- doctor read-only par defaut ;
- output structure ;
- failure explicable.

Evidence :

- doctor report ;
- fixtures fail and pass.

Gate :

- pack active seulement apres doctor compatible.

## 8. Lot G - Memory OS

### LOT-G0 - Migration target Weaviate Neo4j

Objectif :

- remplacer Qdrant par Weaviate comme store vectoriel cible et Neo4j comme store graphe cible sans perte de donnees.

Surface :

- `grimoire-kit/src/grimoire/core/config.py` ;
- `grimoire-kit/src/grimoire/core/schema.py` ;
- `grimoire-kit/src/grimoire/core/validator.py` ;
- `grimoire-kit/src/grimoire/memory/architecture.py` ;
- `grimoire-kit/src/grimoire/memory/migration.py` ;
- `grimoire-kit/project-context.yaml` ;
- `docker-compose.memory-target.yml`.

Guardrails :

- Qdrant reste source tant que `vector_lossless` n'est pas prouve ;
- les secrets Weaviate et Neo4j passent par variables d'environnement ;
- migration par bundle portable avant cutover ;
- ids source preserves dans Weaviate et Neo4j.

Evidence :

- tests config/schema/validator ;
- `grimoire memory migrate plan` ;
- bundle contenant `manifest.json`, `memories.jsonl`, `weaviate-objects.jsonl`, `neo4j-import.cypher`.

Gate :

- `record_count == vector_count` pour le bundle Qdrant ;
- le backend live ne passe a `weaviate-server` qu'apres parite de recall.

### LOT-G1 - Memory contracts

Objectif :

- definir `MemoryRecord`, `RecallRequest`, `RecallResult`, `PromotionCandidate`.

Guardrails :

- provenance ;
- freshness ;
- contradiction ;
- scope.

Evidence :

- schema ;
- fixtures.

Gate :

- memoire non sourcee refusee en strict.

### LOT-G2 - Recall gouverne

Objectif :

- construire capsule de contexte auditable.

Guardrails :

- max context ;
- source hierarchy ;
- stale warning.

Evidence :

- recall trace ;
- memory refs.

Gate :

- task montre quelles memoires ont ete lues.

### LOT-G3 - Promotion gouvernee

Objectif :

- promouvoir decisions, preuves, incidents et patterns utiles.

Guardrails :

- pas de promotion depuis output non verifie ;
- lien task et evidence.

Evidence :

- promotion event ;
- memory record.

Gate :

- promotion sans provenance refusee.

## 9. Lot H - Code Graph

### LOT-H1 - Index symboles

Objectif :

- indexer fichiers, symboles, imports.

Guardrails :

- incremental ;
- ignore generated ;
- source repo conserve.

Evidence :

- graph snapshot ;
- query symbol.

Gate :

- fichier modifie invalide son fragment.

### LOT-H2 - Impact analysis

Objectif :

- relier code, tests, docs et tasks.

Guardrails :

- confidence score ;
- unknown explicit.

Evidence :

- impact query ;
- tests suggested.

Gate :

- impact result exploitable dans cockpit.

## 10. Lot I - Cockpit

### LOT-I1 - Mission Board projection

Objectif :

- afficher mission, task graph et dependances.

Guardrails :

- projection seulement ;
- mutation via API controlee.

Evidence :

- screenshot or render proof ;
- read model test.

Gate :

- cockpit coherent avec ledger.

### LOT-I2 - Workflow and evidence views

Objectif :

- afficher instance, checkpoints, evidence, verification.

Guardrails :

- evidence digest ;
- no secret display by default.

Evidence :

- view test ;
- redaction proof.

Gate :

- closure expliquee depuis evidence.

### LOT-I3 - Policy and incident views

Objectif :

- rendre refus et blocages lisibles.

Guardrails :

- reason obligatoire ;
- incident status.

Evidence :

- policy projection ;
- incident projection.

Gate :

- operateur sait quoi corriger.

## 11. Lot J - Host Bridge et interop

### LOT-J1 - Capability manifest

Objectif :

- declarer les capacites reelles de chaque host.

Guardrails :

- fallback obligatoire ;
- claims non supportes refuses.

Evidence :

- manifests Codex, Claude, Copilot, CLI.

Gate :

- runtime adapte son controle selon host.

### LOT-J2 - MCP adapter

Objectif :

- exposer tools et resources via MCP avec policy.

Guardrails :

- mutateur soumis a verdict ;
- resources sensibles filtrees.

Evidence :

- MCP smoke ;
- policy trace.

Gate :

- tool MCP critique bloque sans policy.

### LOT-J3 - A2A adapter

Objectif :

- integrer agents externes avec Task, Message, Artifact.

Guardrails :

- external task mapped to ledger ;
- external artifact mapped to evidence ;
- no external closure.

Evidence :

- adapter fixture ;
- trace normalized.

Gate :

- agent externe subordonne au ledger.

## 12. Lot K - Observabilite et evals

### LOT-K1 - Trace Ledger

Objectif :

- stocker traces runtime et policy.

Guardrails :

- redaction ;
- run id ;
- task id ;
- no secrets.

Evidence :

- trace fixture ;
- redaction test.

Gate :

- trace joint task, policy et evidence.

### LOT-K2 - OTel and Langfuse export

Objectif :

- exporter sans rendre backend obligatoire.

Guardrails :

- exporter optionnel ;
- prompts complets non stockes par defaut.

Evidence :

- export sample ;
- sensitive data check.

Gate :

- export valide et redacte.

### LOT-K3 - Eval harness

Objectif :

- mesurer regressions d'agents, workflows, policies et packs.

Guardrails :

- fixtures reproductibles ;
- score explicable.

Evidence :

- eval report ;
- regression sample.

Gate :

- changement critique compare a baseline.

## 13. Lot L - Distribution kit

### LOT-L1 - CLI projet agentique

Objectif :

- creer un projet agentique avec contracts, ledger, packs et doctor.

Guardrails :

- defaults safe ;
- no external service required by default.

Evidence :

- scaffold output ;
- doctor pass.

Gate :

- nouveau projet bootstrappe avec contracts cibles.

### LOT-L2 - SDK public

Objectif :

- exposer APIs ledger, runtime, policy, packs, memory.

Guardrails :

- semver ;
- schema compatibility ;
- typed errors.

Evidence :

- API tests ;
- examples.

Gate :

- example project compile and runs doctor.

### LOT-L3 - Documentation kit

Objectif :

- documenter concepts, contracts, quickstart et migration.

Guardrails :

- docs derivees des schemas ;
- no obsolete roadmap.

Evidence :

- docs build ;
- links check.

Gate :

- builder externe peut creer pack simple.

## 14. Lot M - Fusion projets de reference

### LOT-M1 - Gastownhall complete mapping

Objectif :

- finaliser mapping Mayor, rigs, convoys, formulas, packs, OTel.

Guardrails :

- vocabulaire Grimoire canonique ;
- pas de copie brute.

Evidence :

- mapping matrix ;
- adapters backlog.

Gate :

- chaque primitive utile a destination Grimoire claire.

### LOT-M2 - CrewAI integration profile

Objectif :

- definir ce qui devient recipe, adapter ou reference.

Guardrails :

- CrewAI runner optionnel ;
- output schema obligatoire.

Evidence :

- CrewAI sample import ;
- adapter contract.

Gate :

- CrewAI ne cree pas de source de verite parallele.

### LOT-M3 - Security references

Objectif :

- traduire OWASP Agentic et skills supply chain en gates.

Guardrails :

- red-team cases ;
- negative tests ;
- pack trust tiers.

Evidence :

- threat matrix ;
- refusal tests.

Gate :

- risques majeurs couverts.

## 15. Ordre de readiness

Les lots deviennent executables selon dependances :

1. A avant tous les autres lots documentaires.
2. B avant C, I et J.
3. C avant D, E, K et L.
4. E avant F activation, J mutateurs et K security traces.
5. F avant distribution packs.
6. G et H alimentent routing et cockpit.
7. I depend des projections B, C, E, F, G, K.
8. M reste en adapter ou incubator tant que B, C, E, F ne sont pas stables.

## 16. Contract de sortie agent

Chaque agent doit rendre :

```yaml
agent_output:
  task_id: GAO-example-001
  status: needs_verification
  changed_files:
    - path/to/file
  decisions:
    - id: decision-001
      summary: source of truth remains Mission Ledger
  evidence:
    - kind: test
      uri: evidence://test-output
  incidents:
    - id: inc-example
      status: closed
  follow_up_tasks:
    - title: Add negative policy test
      reason: coverage gap found
  verification_request:
    profile: strict
    requested: true
```

## 17. Regle de promotion

Un lot passe de prototype a cible si :

- contracts publics definis ;
- tests et fixtures presents ;
- evidence pack present ;
- doc liee ;
- cockpit projection possible ;
- guardrails actifs ;
- negative path teste ;
- aucun plan concurrent cree.
