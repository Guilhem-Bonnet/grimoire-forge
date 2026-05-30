# Revue critique - Angles morts et corrections du plan

## Verdict de revue

Le plan est viable, mais il ne doit pas être interprété comme une liste de features. C'est un programme de durcissement du noyau.

Le risque principal reste le même que dans les anciens rapports : Grimoire peut devenir trop riche avant d'être assez canonique. La correction est de faire passer chaque idée par le Runtime Kernel.

## Ce que les rapports anciens avaient raison de dire

### La vision est en avance sur l'exécution

C'est encore vrai, mais moins qu'avant. Plusieurs pièces prévues sont maintenant présentes :

- `GrimoireEvent` ;
- ledger hook ;
- observability projections ;
- Mission Board activity ;
- Office timeline ;
- stigmergy consumer ;
- tests ciblés.

La dette restante est donc plus précise : le projet a des événements, mais pas encore un run durable complet.

### Trop d'agents n'est pas un OS

Toujours vrai. Le nombre d'agents `.github` reste stable à 23, mais les skills montent à 43. La croissance future doit passer par capabilities et packs, pas par profils ad hoc.

### L'observabilité doit devenir un produit

Toujours vrai. Les vues et tests existent, mais il manque la chaîne :

```text
run -> event -> span -> eval -> evidence -> cockpit
```

### MCP doit passer de capacité à control plane

Toujours vrai. Le rapport policy local montre un échec concret sur `ollama`. Ce n'est pas un détail : c'est exactement le genre de signal que le cockpit doit exposer et bloquer.

## Ce que les anciens plans ne couvraient pas assez

### 1. A2A est devenu plus stratégique

Les anciens plans parlaient surtout MCP et Host Bridge. A2A ajoute une couche différente :

- MCP : agent vers tools et ressources ;
- A2A : agent vers agents avec AgentCard, tasks, messages, artifacts.

Grimoire doit être A2A-ready, mais sans exposer son état interne. La bonne approche est un adapter contrôlé, pas une refonte du kernel autour d'A2A.

### 2. Les skills sont une surface de sécurité

Les rapports parlaient beaucoup agents et tools. Les sources OWASP récentes montrent que les skills sont une couche d'exécution à part entière.

Correction :

- manifest de skill ;
- permissions ;
- provenance ;
- checksum ;
- scanner ;
- tests ;
- gate de promotion.

### 3. Les guardrails agent-level ne suffisent pas

OpenAI documente des frontières précises : les input/output guardrails ne couvrent pas tout, et les tool guardrails ont eux-mêmes des limites.

Correction :

- policy au niveau tool ;
- policy au niveau handoff ;
- policy au niveau host bridge ;
- policy au niveau skill ;
- verdict dans chaque `RunEvent`.

### 4. Le schema drift Python/TypeScript va devenir dangereux

`hookEvents.ts` dit explicitement qu'il faut garder le miroir TS synchronisé avec `events.py`. Cette synchronisation manuelle est acceptable pour V1, mais pas pour un kernel.

Correction :

- JSON Schema source de vérité ;
- génération Python et TypeScript ;
- tests de round-trip ;
- versioning explicite.

### 5. Le dispatch gateway est encore trop permissif

`dispatch-gateway.ts` documente un comportement fail-open si l'emitter échoue. Pour une UI de contrôle, ce comportement peut être acceptable dans une projection, mais pas dans le control plane.

Correction :

- fail-open seulement pour preview ou démo ;
- fail-closed pour tout dispatch réel ;
- afficher la raison dans le cockpit ;
- créer un event `task/block` si l'émission échoue.

### 6. Le ledger n'est pas encore un checkpoint

Un ledger append-only dit ce qui s'est passé. Un checkpoint permet de reprendre.

Correction :

- séparer `EventStore` et `CheckpointStore` ;
- stocker side effects ;
- ajouter idempotency key ;
- rejouer les projections sans rejouer les actions externes.

### 7. Le Memory OS est prêt en infrastructure mais vide en valeur

`grimoire memory status` montre Qdrant prêt, mais aucune entrée. Une mémoire prête mais non alimentée ne crée pas encore de valeur agentique.

Correction :

- promotion depuis events ;
- promotion depuis decisions ;
- promotion depuis evidence packs ;
- task memory ;
- code graph ;
- recall eval.

### 8. Le code graph reste un trou compétitif

CodeGraphContext et Graphify montrent qu'un agent de code moderne doit comprendre symboles, fichiers, tests, dépendances et ownership.

Correction :

- indexer `src/grimoire`, `apps/grimoire-game`, `.github`, `_grimoire-runtime` ;
- lier symboles aux tasks et tests ;
- exposer une recherche hybride graph + vector.

### 9. Le model routing doit devenir capability-based

Le routing actuel documente des modèles et profils. La disponibilité réelle des modèles change selon host, plan, région et date.

Correction :

- résoudre les modèles par capacités ;
- stocker des model cards locales ;
- tracer le modèle effectivement utilisé ;
- fallback vers `auto` seulement avec raison enregistrée ;
- éviter les noms hardcodés comme source de vérité durable.

### 10. Le sandboxing reste insuffisamment produit

Les guardrails limitent des actions, mais un Agent OS doit aussi isoler l'exécution.

Correction :

- sandbox leases ;
- workspace scope ;
- network scope ;
- process scope ;
- cleanup ;
- audit ;
- integration Playwright/browser explicite.

## Concepts ambitieux à ajouter

### Flight Recorder

Un enregistreur de mission qui capture :

- run state ;
- events ;
- checkpoints ;
- prompts ;
- tools ;
- approvals ;
- evidence ;
- memory reads ;
- policy verdicts.

Objectif : debug, audit, replay, comparaison de versions.

### Capability Internet

Une registry où chaque agent, skill, workflow, host et tool publie une carte.

Objectif : SOG ne route plus par intuition textuelle, mais par capacités déclarées et testées.

### Policy Compiler

Un compilateur de policy qui transforme YAML en :

- validators Python ;
- guards TypeScript ;
- hook configs ;
- MCP policy ;
- cockpit explanation.

Objectif : une policy, plusieurs projections.

### Evidence-First Done

La transition `done` n'est plus un statut manuel. Elle est calculée par un profile de preuve.

Objectif : aucune mission critique ne se ferme sans preuves liées.

### Memory Freshness Radar

Un radar de fraîcheur mémoire :

- mémoire récente ;
- mémoire stale ;
- mémoire contradictoire ;
- mémoire sans source ;
- mémoire fréquemment utile.

Objectif : éviter que Memory OS devienne une vérité fossilisée.

### Agent Red Team Harness

Un harness de tests adversariaux :

- prompt injection ;
- tool poisoning ;
- malicious skill ;
- over-privileged skill ;
- MCP hostile ;
- memory poisoning ;
- exfiltration via logs.

Objectif : aligner Grimoire sur OWASP Agentic et OWASP Agentic Skills.

## Corrections prioritaires au plan

| Risque | Correction à intégrer |
| --- | --- |
| Runtime Kernel trop ambitieux | Commencer par schéma et reconstruction de run, puis checkpoints. |
| A2A exposé trop tôt | Publier AgentCard interne d'abord, gateway externe après policy. |
| OTel ajouté comme dépendance lourde | Exporter local JSONL compatible d'abord, exporter externe optionnel ensuite. |
| Memory OS alimente trop de bruit | Promouvoir seulement décisions, preuves, incidents et patterns répétés. |
| Cockpit avance sans kernel | Toute nouvelle view doit déclarer son contrat source. |
| Skills supply chain oubliée | Ajouter scanner et manifest avant registry remote. |
| MCP `ollama` ignoré | Corriger immédiatement la policy ou le config, puis afficher le statut dans cockpit. |

## Go / No-Go

### Go

Lancer la Vague A si :

- les tests ciblés runtime restent verts ;
- le schéma actuel est gelé comme entrée de migration ;
- le périmètre est limité au kernel et aux contrats ;
- aucune nouvelle room UI n'est ajoutée.

### No-Go

Reporter si :

- la vague mélange kernel, UI, A2A et Memory OS dans un seul changement ;
- le plan commence par pack registry ou self-improvement ;
- les policies restent diagnostics non bloquants ;
- les preuves de fin ne sont pas définies avant l'implémentation.

## Conclusion de revue

Le plan le plus fort est aussi le plus strict : Grimoire doit devenir un noyau de contrôle avant de redevenir un laboratoire d'idées.

La bonne séquence est :

```text
kernel -> reprise -> policy -> evidence -> memory -> cockpit -> interop -> packs -> learning
```

Tout autre ordre augmente le risque de refaire le même cycle : beaucoup d'artefacts, beaucoup de promesses, et pas assez de vérité runtime.

