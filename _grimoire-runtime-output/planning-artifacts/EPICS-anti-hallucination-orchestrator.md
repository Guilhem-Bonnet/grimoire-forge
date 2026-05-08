# EPICs — Anti-Hallucination, Smart Orchestrator, Enhanced Party Mode & Agent Parallelism

**Projet** : grimoire (BMAD Custom Kit)
**Date** : 2026-03-05
**Auteur** : Party Mode Brainstorm (Carson, Winston, Bond, Wendy, Victor, Dr. Quinn, John)
**Statut** : IMPLÉMENTÉ — 10 EPICs, 10 protocoles framework, fichiers existants intégrés

---

## Vision

Transformer l'interaction multi-agents BMAD en un système **fiable, transparent et contrôlé** où :
- Un **seul orchestrateur** sert d'interface avec l'utilisateur
- Les agents **ne peuvent pas halluciner** sans que le système le détecte
- Toute incertitude **remonte la chaîne** au lieu d'être masquée
- Le Party Mode produit de **vrais débats** avec des perspectives divergentes
- Les agents **travaillent en parallèle** quand c'est possible
- Les agents **communiquent directement** entre eux pour les échanges ciblés
- Les agents **se connaissent** via un graphe relationnel dynamique

---

## EPICs

### EPIC 1 — Smart Orchestrator Gateway (SOG)
> *L'agent unique de communication et d'orchestration*

**Fichier framework** : `framework/orchestrator-gateway.md`

| Item | Détail |
|------|--------|
| **Objectif** | Point d'entrée unique utilisateur ↔ système multi-agents |
| **BM-ID** | BM-53 |
| **Responsabilités** | Analyse d'intention, clarification proactive, prompt enrichissement, routage, agrégation |
| **Pattern** | API Gateway + Context Amplifier |
| **Intégration** | Étend `subagent-orchestration.md` (BM-19) et `boomerang-orchestration.md` (BM-11) |

**Features :**
1. Analyse d'intention avec détection de zones d'ombre
2. Dialogue de clarification proactif AVANT dispatch
3. Création de prompts enrichis contextuellement pour chaque sub-agent
4. Graphe de connaissance conversationnel (session memory graph)
5. Routage intelligent multi-critères
6. Agrégation cohérente des résultats multi-agents
7. Buffer de questions avec lot groupé

---

### EPIC 2 — Honest Uncertainty Protocol (HUP)
> *Le système anti-hallucination par design*

**Fichier framework** : `framework/honest-uncertainty-protocol.md`

| Item | Détail |
|------|--------|
| **Objectif** | Éliminer les hallucinations via méta-cognition artificielle |
| **BM-ID** | BM-50 |
| **Pattern** | Circuit Breaker Cognitif + Pre/Post-flight Checks |
| **Intégration** | S'injecte dans `agent-base.md` comme règle P0 non-négociable |

**Features :**
1. Seuils de confiance 3 niveaux (Vert ≥80% / Jaune 40-80% / Rouge <40%)
2. Pre-flight check obligatoire (infos suffisantes ? hypothèses vérifiées ? output vérifiable ?)
3. Post-flight validation avec self-check (cohérence, faits inventés, confiance)
4. Classification structurée des incertitudes (`knowledge_gap | ambiguity | complexity | missing_data`)
5. Obligation d'effort documenté avant toute escalade
6. Mécanisme anti-évitement (détection de patterns d'esquive sur tâches gourmandes)
7. Intégration BMAD Trace pour auditabilité

---

### EPIC 3 — Question Escalation Chain (QEC)
> *Le système de remontée et agrégation des questions*

**Fichier framework** : `framework/question-escalation-chain.md`

| Item | Détail |
|------|--------|
| **Objectif** | Canaliser toutes les incertitudes vers l'orchestrateur, jamais d'invention |
| **BM-ID** | BM-51 |
| **Pattern** | Message Queue + Batch Processing |
| **Intégration** | Relie HUP (EPIC 2) à SOG (EPIC 1) |

**Features :**
1. File d'attente structurée de questions des sub-agents
2. Agrégation et dé-duplication automatique
3. Tentative de résolution autonome par contexte avant escalade
4. Présentation groupée et structurée à l'utilisateur
5. Priorisation (bloquant / important / nice-to-have)
6. Suivi des réponses et redistribution aux agents concernés
7. Historique des Q&A pour enrichir le contexte futur

---

### EPIC 4 — Cross-Validation & Trust Layer (CVTL)
> *La couche de vérification croisée et de confiance*

**Fichier framework** : `framework/cross-validation-trust.md`

| Item | Détail |
|------|--------|
| **Objectif** | Vérifier les outputs critiques par validation croisée multi-agents |
| **BM-ID** | BM-52 |
| **Pattern** | Peer Review + Trust Score |
| **Intégration** | Étend la stratégie `vote` de `subagent-orchestration.md` |

**Features :**
1. Vérification croisée par un second agent sur outputs critiques
2. Score de confiance composite visible sur chaque livrable
3. Traçabilité des hypothèses vs faits avérés
4. Challenge automatique sur outputs "jaune" (HUP)
5. Rapport d'intégrité par session
6. Pattern Adversarial Review intégré

---

### EPIC 5 — Enhanced Party Mode — Productive Conflict Engine (PCE)
> *Un party mode qui génère de vrais débats et des perspectives divergentes*

**Fichier framework** : Mise à jour de `party-mode/steps/step-02-discussion-orchestration.md`

| Item | Détail |
|------|--------|
| **Objectif** | Transformer le party mode de "consensus facile" en "débat productif" |
| **BM-ID** | BM-54 |
| **Pattern** | Structured Debate + Red Team/Blue Team + Steelman |
| **Intégration** | Étend le party mode existant |

**Features :**
1. Rôles dynamiques : Devil's Advocate assigné automatiquement
2. Mode Red Team / Blue Team pour décisions clés
3. Score de divergence : consensus trop rapide → challenge forcé
4. Steelman obligatoire : reformuler l'argument adverse en version la plus forte
5. Mécanisme de vote structuré pour les décisions
6. Système de réactions inter-agents (contradictions, nuances, builds)
7. Méta-facilitation : détection boucles circulaires + redirection

---

## Dépendances entre EPICs

```
EPIC 2 (HUP) ──────────┐
                        ├──→ EPIC 3 (QEC) ──→ EPIC 1 (SOG)
EPIC 4 (CVTL) ─────────┘                        ↑
                                                  │
EPIC 5 (PCE) ── indépendant ─────────────────────┘ (utilise SOG)
```

**Ordre d'implémentation recommandé :**
1. EPIC 2 (HUP) — fondation, s'injecte dans tous les agents
2. EPIC 3 (QEC) — le canal de remontée
3. EPIC 4 (CVTL) — la vérification croisée
4. EPIC 1 (SOG) — l'orchestrateur qui utilise tout
5. EPIC 5 (PCE) — l'amélioration party mode

---

## Fichiers Framework à Créer/Modifier

| Action | Fichier | EPIC |
|--------|---------|------|
| **CRÉER** | `framework/orchestrator-gateway.md` | 1 |
| **CRÉER** | `framework/honest-uncertainty-protocol.md` | 2 |
| **CRÉER** | `framework/question-escalation-chain.md` | 3 |
| **CRÉER** | `framework/cross-validation-trust.md` | 4 |
| **MODIFIER** | `framework/agent-base.md` — ajout section HUP | 2 |
| **MODIFIER** | `framework/agent-base-compact.md` — ajout HUP compact | 2 |
| **MODIFIER** | `framework/workflows/subagent-orchestration.md` — ajout merge strategy `cross-validate` | 4 |
| **MODIFIER** | `party-mode/steps/step-02-discussion-orchestration.md` — Conflict Engine | 5 |

---

## EPICs 6-10 — Agent Parallelism & Inter-Agent Communication

> Issus du second brainstorm Party Mode — focus sur le travail parallèle, la communication
> directe entre agents, et la connaissance mutuelle.

### EPIC 6 — Agent Mesh Network (AMN)
> *Le réseau maillé pour la communication P2P entre agents*

**Fichier framework** : `framework/agent-mesh-network.md`

| Item | Détail |
|------|--------|
| **BM-ID** | BM-55 |
| **Objectif** | Permettre aux agents de communiquer directement en P2P sans passer systématiquement par le SOG |
| **Pattern** | Service Registry + Peer-to-Peer + Governance |
| **Intégration** | S'appuie sur `message-bus.py`, `agent-worker.py`, ARG (BM-57), ELSS (BM-59) |

**Features :**
1. Service Registry avec découverte dynamique (capabilities, status, workload)
2. Communication P2P directe : ask, inform, request, respond, challenge, offer
3. Gouvernance : décisions finales toujours via SOG, P2P limité à 5 échanges
4. Load balancing weighted-round-robin (availability × expertise × recency × synergy)
5. Protocole d'enregistrement/heartbeat/désenregistrement
6. Observabilité totale via ELSS — SOG peut intervenir à tout moment
7. Discovery de services : trouver l'expert pour un sujet donné

---

### EPIC 7 — Selective Huddle Protocol (SHP)
> *Mini party-mode ciblé pour concertations rapides*

**Fichier framework** : `framework/selective-huddle-protocol.md`

| Item | Détail |
|------|--------|
| **BM-ID** | BM-56 |
| **Objectif** | Micro-sessions de discussion 2-4 agents, time-boxées, avec livrable structuré |
| **Pattern** | Event-Driven Trigger + Scoped Discussion + Structured Deliverable |
| **Intégration** | S'appuie sur AMN (BM-55), ARG (BM-57), PCE (BM-54), ELSS (BM-59) |

**Features :**
1. 3 types de huddle : Quick-Consult (3-5 msg), Debate (5-10 msg), Review (5-8 msg)
2. 6 déclencheurs automatiques (CVTL challenge, HUP JAUNE multi-domaine, contradiction, agent-initiated, emerging ADR, story complexe)
3. Sélection optimisée des participants via ARG (expertise + diversité + synergy)
4. Time-boxing strict avec force-close et synthèse SOG
5. Escalade automatique huddle → party mode si non-convergence
6. Livrables structurés : avis, décision, review_report
7. Commandes utilisateur : `[HUDDLE topic]`, `[HUDDLE topic WITH agents]`

---

### EPIC 8 — Agent Relationship Graph (ARG)
> *Le graphe de connaissance mutuelle et de compétences émergentes*

**Fichier framework** : `framework/agent-relationship-graph.md`

| Item | Détail |
|------|--------|
| **BM-ID** | BM-57 |
| **Objectif** | Graphe dynamique des relations, compétences et performances entre agents |
| **Pattern** | Knowledge Graph + Event Sourcing + Dynamic Enrichment |
| **Intégration** | S'appuie sur `agent-manifest.csv`, `agent-worker.py`, `swarm-consensus.py`, ELSS (BM-59) |

**Features :**
1. Profil dynamique par agent : capabilities statiques + émergentes + métriques
2. Arêtes relationnelles : collaboration, delegation, validation, challenge (avec force)
3. Synergies détectées automatiquement (paires productives)
4. Anti-patterns détectés (agents isolés, tensions récurrentes)
5. Routing optimisé pour SOG : agent_selection = static(30%) + emergent(25%) + trust(25%) + synergy(20%)
6. Bootstrap depuis sources statiques (manifest, KNOWN_AGENTS, AGENT_WEIGHTS)
7. Commandes d'introspection : `[GRAPH-STATUS]`, `[GRAPH-AGENT id]`, `[GRAPH-SUGGEST topic]`

---

### EPIC 9 — Hybrid Parallelism Engine (HPE)
> *Le moteur d'orchestration parallèle adaptative*

**Fichier framework** : `framework/hybrid-parallelism-engine.md`

| Item | Détail |
|------|--------|
| **BM-ID** | BM-58 |
| **Objectif** | Orchestrer des DAG de tâches avec parallélisme adaptatif |
| **Pattern** | DAG Scheduler + Critical Path + Opportunistic Execution |
| **Intégration** | Étend BM-19 et BM-11 · utilise AMN, ARG, ELSS, HUP, QEC, CVTL, SHP |

**Features :**
1. DAG de tâches avec dépendances explicites (`depends_on`)
2. 3 modes d'exécution : parallel (indépendant), sequential (dépendances), opportunistic (early-start)
3. Calcul du chemin critique avec priority boost et agent assignment optimal
4. Gestion d'échecs multi-stratégie : stop-all, continue-others, pause-and-escalate
5. Checkpoints et reprise (`[HPE-RESUME]`)
6. Intégration CVTL (`mode: cross-validate`) et SHP (huddle auto sur critical path JAUNE/ROUGE)
7. Syntaxe `type: hybrid-orchestrate` dans les workflows YAML

---

### EPIC 10 — Event Log & Shared State (ELSS)
> *Le bus d'événements et l'état partagé observable*

**Fichier framework** : `framework/event-log-shared-state.md`

| Item | Détail |
|------|--------|
| **BM-ID** | BM-59 |
| **Objectif** | Bus d'événements persistant et état global reconstruit par event sourcing |
| **Pattern** | Event Sourcing + CQRS + Pub-Sub |
| **Intégration** | S'appuie sur `message-bus.py` et `BMAD_TRACE.md` (BM-28) |

**Features :**
1. Event Log append-only en JSONL (`_bmad-output/.event-log.jsonl`)
2. 10 types d'événements : decision, artifact_created, task_started/completed, uncertainty_raised, etc.
3. Shared State projeté par event sourcing (`_bmad-output/.shared-state.yaml`)
4. Protocole d'émission obligatoire pour chaque agent sur actions significatives
5. Protocole d'observation avec souscription filtrée par type d'événement
6. Garbage collection et archivage (max 10K events, 30 jours)
7. Intégration BMAD Trace bidirectionnelle

---

## Dépendances EPICs 6-10

```
EPIC 10 (ELSS) ─── fondation ──→ tous les EPICs 6-9

EPIC 8  (ARG)  ──→ EPIC 6 (AMN) routing
                   EPIC 7 (SHP) sélection participants
                   EPIC 9 (HPE) assignation agents

EPIC 6  (AMN)  ──→ EPIC 7 (SHP) transport P2P
                   EPIC 9 (HPE) dispatch tâches

EPIC 7  (SHP)  ←── EPIC 4 (CVTL) trigger challenge
                ←── EPIC 5 (PCE) techniques de débat

EPIC 9  (HPE)  ──→ étend EPIC 1 (SOG)
                   utilise EPIC 2 (HUP) + EPIC 3 (QEC) + EPIC 4 (CVTL)
```

**Ordre d'implémentation recommandé :**
1. EPIC 10 (ELSS) — fondation observabilité
2. EPIC 8 (ARG) — graphe de compétences
3. EPIC 6 (AMN) — mesh réseau
4. EPIC 7 (SHP) — huddles sélectifs
5. EPIC 9 (HPE) — orchestration hybride

---

## Fichiers Framework Créés/Modifiés — EPICs 6-10

| Action | Fichier | EPIC |
|--------|---------|------|
| **CRÉER** | `framework/agent-mesh-network.md` | 6 |
| **CRÉER** | `framework/selective-huddle-protocol.md` | 7 |
| **CRÉER** | `framework/agent-relationship-graph.md` | 8 |
| **CRÉER** | `framework/hybrid-parallelism-engine.md` | 9 |
| **CRÉER** | `framework/event-log-shared-state.md` | 10 |
| **MODIFIER** | `framework/agent-base.md` — ajout section AMN (conscience réseau) | 6 |
| **MODIFIER** | `framework/agent-base-compact.md` — ajout règle 8 Mesh | 6 |
| **MODIFIER** | `framework/orchestrator-gateway.md` — ajout AMN/ARG/HPE/SHP/ELSS dans table intégration | 6-10 |
| **MODIFIER** | `framework/workflows/subagent-orchestration.md` — ajout hybrid-orchestrate + mesh dispatch | 6, 9 |
