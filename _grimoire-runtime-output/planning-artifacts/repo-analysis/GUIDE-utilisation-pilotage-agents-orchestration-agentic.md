---
title: "Guide d'Utilisation — Guide Pilotage Agentique"
slug: pilotage-agents-orchestration-agentic
type: guide-utilisation
date: 2026-04-26
version: "3.0"
relates_to:
  - GUIDE-pilotage-agents-orchestration-agentic.md
  - GUIDE-pilotage-agents-orchestration-agentic-V2-approfondi.md
  - GUIDE-pilotage-agents-orchestration-agentic-V3-maximum.md
---

# Guide d'Utilisation — Comment exploiter ce document

## Pour quel public ?

Ce guide s'adresse aux personnes qui construisent ou évaluent un système d'orchestration d'agents LLM.

## Quel document lire ?

| Besoin | Document |
|---|---|
| Vue d'ensemble rapide, choisir un framework | **V1** — `GUIDE-pilotage-agents-orchestration-agentic.md` |
| Comprendre l'implémentation interne avec code réel | **V2** — `GUIDE-pilotage-agents-orchestration-agentic-V2-approfondi.md` |
| Repos inédits, sécurité agentique OWASP, approfondissements extrêmes | **V3** — `GUIDE-pilotage-agents-orchestration-agentic-V3-maximum.md` |
| V1 = carte · V2 = terrain · V3 = profondeurs + sécurité |

---

## Navigation V1 — Cartographie générale

### Si tu veux choisir un framework rapidement

→ Section 2 (Cartographie) : vue d'ensemble visuelle  
→ Section 23 (Synthèse par repo) : verdict par framework  
→ Section 24.1 (Recommandations par cas d'usage) : tableau décisionnel

### Si tu veux comprendre un pattern en profondeur (niveau concept)

→ Sections 3 à 13 : un pattern par section  
→ Chaque section : principe, code, forces/faiblesses

### Si tu construis un système de zéro

→ Section 20 (Éléments obligatoires) : les 10 non-négociables  
→ Section 21 (Architecture recommandée) : modèle de référence  
→ Section 22 (Checklist opérationnelle) : 3 checklists pratiques

### Si tu diagnostiques un problème existant

→ Section 19 (Défauts et compensations) : matrice défaut × solution  
→ Section 19.2 (Test des 3 questions) : diagnostic rapide

### Si tu as un problème de sécurité

→ Section 18 (Sécurité) : vecteurs d'attaque + défenses

### Lecture recommandée selon ton niveau (V1)

**Débutant** : Sections 1 → 2 → 23 → 24 → 20  
**Intermédiaire** : Sections 3-13 (patterns) → 14 (mémoire) → 19 (défauts) → 22 (checklist)  
**Expert** : Sections 15-18 (communication, tools, observabilité, sécurité) → 21 (architecture)

---

## Navigation V2 — Analyse code source (2261 lignes)

### Si tu veux comprendre le mécanisme interne d'un framework spécifique

→ Partie I (§1-4) : AutoGen/MAF, CrewAI, OpenAI Agents, LangGraph — frameworks matures  
→ Partie II (§5-7) : LangFlow, Haystack, Dify — pipelines visuels  
→ Partie III (§8-10) : OpenHands, browser-use, BMAD — agents spécialisés  
→ Partie IV (§11-14) : Langfuse, mempalace, kagent, LLMLingua — infrastructure  
→ Partie V (§15-20) : Octogent, switchboard, graphify, autres — petits frameworks  

### Si tu veux les patterns transversaux découverts dans le code

→ Section 21 : patterns transversaux (version-based sync, guardrails parallèles, verbatim storage...)  
→ Section 22 : architectures mémoire analysées au niveau code  
→ Section 25 : stack recommandée avec justifications code

### Si tu cherches un snippet de code spécifique

| Mécanisme | Section V2 |
|---|---|
| Pregel checkpoint format (LangGraph) | §4 |
| RecallFlow ThreadPool (CrewAI) | §2 |
| Guardrails 4 niveaux (OpenAI Agents) | §3 |
| EventStream threading (OpenHands) | §8 |
| Watchdogs passifs (browser-use) | §9 |
| Schema traces tokens/coût (Langfuse) | §11 |
| Verbatim chunking CHUNK_SIZE=800 (mempalace) | §12 |
| CRD controller loop Go (kagent) | §13 |
| Cross-entropy compression (LLMLingua) | §14 |

### Lecture recommandée selon ton niveau (V2)

**Débutant** : §25 (stack recommandée) → §21 (patterns transversaux) → §1 framework de son choix  
**Intermédiaire** : Partie I (§1-4) → §22 (mémoire) → §23 (sécurité)  
**Expert** : Lecture linéaire §1-25, en croisant avec V1

---

## Navigation V3 — Maximum depth (1923 lignes)

### Si tu analyses des repos inédits

→ Partie I — Repos inédits  
→ §1 vscode-copilot-chat : hooks = processus externes, 5-strategy model routing  
→ §2 shannon : Temporal Workflows + 13 agents, git checkpoints, spending cap  
→ §3 skill ecosystems : karpathy-4-principles, claude-skills-66, superpowers 94% reject  
→ §4 openclaw : Plugin SDK + manifest contracts, 55+ plugins  
→ §5 LLMSecurityGuide : OWASP Agentic ASI01-ASI10 avec code offensif + défensif

### Si tu veux aller plus loin que V2 sur les frameworks connus

→ Partie II — Approfondissements  
→ §6 LangGraph : 7 stream modes, 3 channel types avec conflits, interrupt/resume via `pending_writes`  
→ §7 CrewAI : per-guardrail retry (pas global), `drain_writes()` cohérence LanceDB  
→ §8 OpenAI Agents : `asyncio.Queue` streaming + background task, 4-stage tool execution  
→ §9 agent-sandbox : warm pool priority sort, 5 min grace, `Retain/Delete` lifecycle  
→ §10 pixel-agents : dual-mode detection (hooks + 500ms JSONL polling)  
→ §11 OpenMythos : RDT full (LTI stability proof, ACT halting, LoRA depth-wise, MoE aux-loss-free)  
→ §12 Haystack : `ConditionalRouter` Jinja2 + AST literal_eval, YAML SafeLoader avec tuples  
→ §13 Dify : `chunk_size=4000` chars, parallel ThreadPool + fail-fast, score dedup, weighted vs model reranking

### Si tu construis un système sécurisé

→ Partie III §16 : OWASP Agentic Top 10 complet avec code défensif  
→ ASI01 (prompt injection), ASI04 (supply chain), ASI06 (memory tampering), ASI10 (identité) — les 4 critiques  
→ EchoLeak CVE-2025-32711 : premier exploit réel sur système agentique commercial

### Si tu cherches un snippet de code spécifique (V3)

| Mécanisme | Section V3 |
|---|---|
| Hooks = processus externes spawn+stdin/stdout (vscode-copilot-chat) | §1 |
| Temporal Workflows + Claude SDK maxTurns=10000 (shannon) | §2 |
| karpathy 4 principes comportementaux LLM | §3 |
| PRODUCTION_RETRY config Temporal (shannon) | §2 |
| LastValue / Topic / BinaryOperatorAggregate channels (LangGraph) | §6 |
| `drain_writes()` barrier LanceDB (CrewAI) | §7 |
| asyncio.Queue streaming + background task (OpenAI Agents) | §8 |
| SandboxClaim CRD warm pool reconciler (agent-sandbox) | §9 |
| LTI spectral radius proof A_discrete ∈ (0,1) (OpenMythos) | §11 |
| SandboxedEnvironment Jinja2 + AST literal_eval (Haystack) | §12 |
| score-based dedup parallel ThreadPool retrieval (Dify) | §13 |
| MemoryIntegrityValidator ASI06 (LLMSecurityGuide) | §16 |

### Lecture recommandée selon ton niveau (V3)

**Débutant** : §16 (OWASP sécurité) → §3 (skill architectures) → §17 (stack recommandée V3)  
**Intermédiaire** : Partie I repos inédits → §14 (error recovery matrix) → §15 (4 skill models)  
**Expert** : Lecture linéaire V3 entier, en croisant avec V1+V2 pour comparaison d'évolution

---

## Lien avec le workflow Grimoire repo-analysis

Ces documents sont produits par le workflow `repo-analysis`.
Pour produire un document équivalent sur un autre repo ou ensemble de repos :

```
Charger : _grimoire-runtime/bmm/workflows/1-analysis/repo-analysis/workflow-repo-analysis.md
```

Scripts disponibles pour l'automatisation :
- `grimoire-kit/framework/tools/repo-analysis-grounding.sh <repo_path>` — scan automatique de structure
- `grimoire-kit/framework/tools/repo-analysis-state.sh read` — état courant du workflow (self-piloting)
- `grimoire-kit/framework/tools/code-review.py --project-root <path> review --json` — findings automatiques (branché dans step-02)
- `grimoire-kit/framework/tools/swarm-consensus.py vote --topic ... --votes ...` — consensus inter-agents (branché dans step-04)

## Mises à jour

Ces documents sont un snapshot à la date 2026-04-25.
Les frameworks évoluent rapidement (AutoGen → MAF, LangGraph v1.x, browser-use v1.x, etc.).
Relancer une analyse sur les repos mis à jour pour maintenir ces documents à jour.
