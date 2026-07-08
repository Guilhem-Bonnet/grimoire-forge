# Inventaire — features innovantes non réellement intégrées

Date : 2026-07-08. Méthode : analyse automatisée des **108 outils** de
`framework/tools/` du kit public, croisée avec leurs surfaces d'intégration
réelles (CLI first-class, SDK `grimoire.tools`, site/serve, `grimoire-init.sh`,
tests, `docs/rnd.md`).

## Le chiffre qui compte

| Statut | Nombre | Signification |
|---|---|---|
| **Intégrés** (CLI, SDK ou site) | **15** | Accessibles à un utilisateur normal |
| **Shell-only** | **93** | Testés, fonctionnels, mais accessibles uniquement par `python framework/tools/x.py` — invisibles pour un utilisateur du paquet |
| Invisibles (aucune surface) | 0 | Tout est au moins couvert par les tests |

Le kit porte donc **~86 % de capacités dormantes** : un investissement
d'ingénierie considérable (des outils de 15 à 97 Ko, tous testés) qui ne
rencontre aucun utilisateur. C'est exactement le problème que le canal
beta/Labs vient de résoudre pour la stigmergie — il faut maintenant l'employer
comme **pipeline de réveil**.

## Les 15 intégrés (référence)

agent-debugger (CLI), agent-forge (SDK), antifragile-score (site),
concierge (CLI), context-guard (SDK), context-router (SDK), dashboard (CLI),
dream (CLI), harmony-check (SDK), memory-lint (SDK+site), nso (CLI),
observatory (site), preflight-check (SDK), **stigmergy (SDK+CLI+hooks+site —
le modèle du pipeline)**, synapse-trace (site).

## Les 93 dormants, par thème

### 1. Écosystème bio-inspiré (le cœur innovant de la marque)
`mycelium` (réseau de nutriments inter-projets), `immune-system`
(anticorps contre les régressions), `self-healing` (auto-réparation de
workflows), `dna-evolve` (évolution des DNA d'archétypes), `agent-darwinism`
(sélection naturelle des agents), `fitness-tracker`, `incubator`
(dormance/incubation d'idées), `sensory-buffer`, `mirror-agent`,
`cognitive-flywheel`, `desire-paths` (chemins de désir des usages),
`dark-matter` (code jamais exercé), `crescendo` (onboarding progressif),
`nudge-engine`, `workflow-adapt` (plasticité synaptique).

### 2. Temporalité & multivers de projet
`time-travel` (checkpoints, replay, bisect), `quantum-branch` (timelines
parallèles), `conversation-branch`, `new-game-plus` (recommencer un projet en
gardant les acquis), `digital-twin` (simulation d'impact).

### 3. Raisonnement & décision
`adversarial-consensus` (quorum + avocat du diable), `swarm-consensus`,
`oracle` (introspection), `reasoning-stream` (HYPOTHESIS/DOUBT/ASSUMPTION),
`bias-toolkit` (catalogue de biais cognitifs), `decision-log` (chaîne
hash-chaînée), `early-warning`.

### 4. Boucle R&D autonome
`r-and-d` + `rnd_core`/`rnd_engine`/`rnd_harvest` (bandit ε-greedy, récolte
d'idées), `failure-museum` (catalogue structuré des échecs).

### 5. Mémoire & connaissance
`semantic-cache` (cache de réponses LLM), `semantic-chain` (chaîne du froid
sémantique), `procedural-memory`, `distill` (director's cut), `memory-sync`
(bidirectionnel Qdrant), `rag-indexer`/`rag-retriever`/`rag-auto-inject`,
`auto-index`, `project-graph`, `conversation-history`, `context-merge`,
`context-summarizer`.

### 6. Orchestration & exécution multi-agents
`orchestrator` (hybride), `agent-caller` (agent-to-agent calling),
`agent-worker`, `hpe-runner`/`hpe-executors`/`hpe-monitor` (parallélisme
hybride), `background-tasks`, `message-bus`, `llm-router`, `token-budget`
(enforcement de budget), `agent-task-system`, `delivery-contracts`
(contrats inter-agents).

### 7. Qualité & outillage dev
`bug-finder` (bugs logiques au-delà du lint), `code-review` (sur git diff),
`quality-score`, `agent-lint`, `agent-test` (tests comportementaux d'agents),
`agent-bench`, `agent-watch` (détection de drift), `gen-tests` (scaffolding
depuis acceptance criteria), `skill-validator`, `schema-validator`,
`dep-check`, `agent-integrity`, `cc-feedback`.

### 8. Synapse (couche intelligence/observabilité avancée)
`synapse-config`, `synapse-dashboard`, `grimoire-mcp-tools` (serveur MCP
Synapse), `grimoire-daemon` (maintenance en arrière-plan).

### 9. Interop & monde extérieur
`rosetta` (glossaire cross-domain), `cross-migrate` (migration
inter-projets), `mcp-proxy`, `mcp-web-search`, `web-browser` (navigation
sandboxée), `vision-judge` (jugement visuel), `image-prompt`,
`doc-fetcher`/`docs-fetcher`, `expert-tool-chain`, `tool-advisor`,
`tool-registry`, `tool-resolver`.

## Anomalies détectées

- **Doublon** : `doc-fetcher.py` et `docs-fetcher.py` coexistent avec la
  même mission (« indexation de documentation externe ») — à fusionner.
- `grimoire-setup`, `session-lifecycle`, `tool-registry`, `agent-integrity`
  ne sont câblés que par `grimoire.sh` (wrapper shell legacy) — surface
  fantôme pour un utilisateur pip.
- La numérotation BM-xx des docstrings témoigne d'un backlog interne jamais
  promu en surface publique.

## Pipeline de réveil proposé (via le canal beta)

Le canal beta + Labs + journalisation viennent d'être créés. Chaque réveil
suit désormais le même chemin que la stigmergie : **SDK propre → CLI
first-class → (si pertinent) hooks non bloquants → vue site → métriques →
promotion ou déprécation**.

### Candidats à réveiller en premier (valeur utilisateur × effort)

| Candidat | Pourquoi lui | Chemin |
|---|---|---|
| **token-budget** | Répond au besoin coût réel (bp2-cost est statique) ; données déjà locales | CLI + endpoint serve + node COÛT du Studio |
| **failure-museum + decision-log** | Piliers de la promesse « rien ne se perd » ; alimentent mémoire et observatoire | CLI + vue observatoire |
| **digital-twin** | Simulation d'impact = extension naturelle de la simulation de blueprints | endpoint serve + panneau Studio |
| **project-graph** | Zones du projet = la `location` de la stigmergie et des blueprints | SDK + data site |
| **agent-watch (drift)** | Complète la boucle gouvernance (drift d'agents comme le doc-drift) | hook shadow + observatoire |
| **crescendo** | Onboarding progressif — rejoint le tutoriel bp2 déjà livré | intégration atelier |
| **bug-finder / code-review** | Valeur immédiate dev ; mais chevauche les outils IDE — à évaluer | CLI seulement |

### À trancher avant tout réveil

1. **Filtrer par la promesse produit** : le kit public promet « OS agentique
   gouverné » — les outils qui renforcent gouvernance/preuve/coordination
   passent d'abord ; les gadgets attendront.
2. **Un réveil = une PR** avec tests + doc + entrée Labs, pas de vague.
3. **Déprécation honnête** : les doublons et les outils sans thèse claire
   (à identifier au cas par cas) méritent l'archivage plutôt que le réveil.
