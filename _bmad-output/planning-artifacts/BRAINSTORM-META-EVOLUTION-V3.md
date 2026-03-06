# BRAINSTORM MÉTA-ÉVOLUTION — Grimoire Kit v3 Platform

> **Date** : 2025-07-17
> **Participants** : Tous les agents BMAD (SOG Party Mode)
> **Facilitateur** : 🧙 BMad Master (SOG BM-53)
> **Sujet** : Audit des 12 méta-capacités du système et plan d'évolution

---

## Légende

| Symbole | Signification |
|---------|--------------|
| ✅ IMPLÉMENTÉ | Existe dans le codebase, testé |
| 🟡 PARTIEL | Existe partiellement ou en mode fallback |
| 🔴 ABSENT | Pas encore implémenté |
| 💡 IDÉE | Proposition d'innovation |
| ⚡ QUICK WIN | Implémentable rapidement |
| 🏗️ EFFORT | Nécessite un travail significatif |

---

## 1. CONTEXTE / MÉMOIRE ET SA GESTION

### 🏗️ Winston (Architect) — État des lieux

**Ce qui existe :**

| Couche mémoire | Outil | État |
|---|---|---|
| Mémoire fichier (JSON/JSONL/MD) | `_bmad/_memory/` | ✅ Unifié (session précédente) |
| mem0-bridge sémantique | `memory/mem0-bridge.py` | ✅ Local JSON + Qdrant optionnel |
| RAG indexing | `rag-indexer.py` | ✅ Fichier fallback + Qdrant optionnel |
| RAG auto-inject | `rag-auto-inject.py` | ✅ Hook d'injection contextuelle |
| RAG retrieval | `rag-retriever.py` | ✅ Recherche multi-backend |
| Context routing | `context-router.py` | ✅ Plan de chargement priorisé P0-P4 |
| Context summarizer | `context-summarizer.py` | ✅ Résumé automatique par priorité |
| Session lifecycle | `session-lifecycle.py` | ✅ Save/restore/list sessions |
| Memory lint | `memory-lint.py` | ✅ Audit santé + JSONL |
| Dream mode | `dream.py` | ✅ Consolidation hors-session, 9 sources |
| Cognitive flywheel | `cognitive-flywheel.py` | ✅ Auto-amélioration continue |
| Failure museum | `failure-museum.py` | ✅ Capitalisation d'échecs |
| CC feedback | `cc-feedback.py` | ✅ Feedback loops |
| Memory sync | `memory-sync.py` | ✅ Synchronisation multi-agent |
| Semantic cache | `semantic-cache.py` | ✅ Cache LLM cosine-based |
| Procedural memory | `procedural-memory.py` | ✅ Savoir-faire opérationnel |

**Verdict : 16 outils mémoire — couverture exceptionnelle.**

### 📊 Mary (Analyst) — Ce qui MANQUE encore

| Gap | Impact | Faisabilité |
|-----|--------|------------|
| **Pas de mémoire VS Code native** | Les `_memory/` scoped par Copilot sont séparées des `_bmad/_memory/` du kit | 🟡 Bridge possible |
| **Pas de cross-session summarization** | Chaque session repart de zéro (sauf conversation-summary) | ⚡ Étendre `session-lifecycle.py` |
| **Pas de memory aging/decay** | Les vieux learnings polluent autant que les récents | ⚡ Ajouter TTL dans `memory-lint.py` |
| **Pas de mémoire graphe (knowledge graph)** | Relations entre entités non explicites | 🏗️ `project-graph.py` existe mais pas de persistence |

### 💡 Propositions

1. **Memory Bridge natif** — Synchroniser `/memories/repo/` (VS Code) ↔ `_bmad/_memory/` (kit) via un hook automatique dans `grimoire-daemon.py`. Quand le daemon détecte un changement dans l'un, il propage vers l'autre.

2. **Memory Decay Scoring** — Chaque entrée mémoire reçoit un `freshness_score = 1.0 * exp(-t/halflife)`. Le `context-router` pondère par ce score. Les entrées < 0.1 sont archivées automatiquement. `dream.py` les utilise en source "archéologique".

3. **Cross-session Summary Chain** — À chaque fin de session, `session-lifecycle.py` écrit un résumé structuré dans `_bmad/_memory/session-chain.jsonl`. Au début de la session suivante, les N derniers résumés sont injectés automatiquement.

---

## 2. PARALLÉLISATION DES AGENTS

### 🧙 BMad Master (Orchestrator) — Analyse

**Ce qui existe :**

| Mécanisme | Outil/Protocole | État |
|---|---|---|
| SOG dispatch parallèle | `orchestrator-gateway.md` (BM-53) | ✅ Spécifié, mode `parallel` |
| Subagent orchestration | BM-19 | ✅ Protocole défini |
| HPE (Hybrid Parallel Engine) | BM-58 | ✅ DAG hybride (parallel + séquentiel + opportuniste) |
| Background tasks | `background-tasks.py` | ✅ File d'attente + polling |
| Agent-worker | `agent-worker.py` | ✅ Exécution déléguée |
| Message bus | `message-bus.py` | ✅ Communication inter-agents |
| Stigmergy | `stigmergy.py` | ✅ Coordination indirecte |
| Mycelium | `mycelium.py` | ✅ Réseau P2P agents |
| Swarm consensus | `swarm-consensus.py` | ✅ Consensus multi-agents |

### ⚡ Victor (Innovation Strategist) — La VRAIE limitation

> **La parallélisation côté LLM est impossible dans le contexte VS Code Copilot.** Un seul thread de conversation = un seul LLM call à la fois. Les outils `background-tasks.py` et `agent-worker.py` permettent de planifier du travail, mais l'exécution reste **séquentielle dans le contexte Copilot**.

**Options réalistes :**

| Stratégie | Mécanisme | Gain |
|---|---|---|
| **Parallelisme de tâches shell** | VS Code Tasks + `run_task` en parallèle | ✅ Déjà possible — tests, lint, build simultanés |
| **Batch prompting** | Regrouper N sous-tâches dans un seul prompt enrichi | Réduit les round-trips |
| **Pipeline pre-compute** | `grimoire-daemon.py` pré-calcule en background pendant l'humain réfléchit | 🟡 Le daemon existe mais pas intégré au workflow |
| **MCP multi-tool** | Un seul appel MCP qui dispatch à plusieurs outils Python | ✅ `bmad-mcp-tools.py` le supporte |
| **Pseudo-parallélisme** | SOG lance Agent A, pendant la review humaine lance Agent B | Design pattern à documenter |

### 💡 Proposition clé

**Daemon Pre-compute Pipeline** — `grimoire-daemon.py` surveille les fichiers en temps réel. Quand un fichier change, il lance proactivement :
- `memory-lint` (santé mémoire)
- `harmony-check` (cohérence)
- `preflight-check` (validation)
- `context-router plan` (mise à jour du plan de chargement)

Résultat disponible AVANT que l'agent en ait besoin. C'est du parallélisme temporel plutôt que spatial.

---

## 3. OPTIMISATION

### 💻 Amelia (Dev) — Optimisations identifiées

| Axe | État actuel | Optimisation |
|-----|------------|-------------|
| **Startup time** | Chaque outil parse `argparse` + charge config | ⚡ Lazy import + config caching via `synapse-config.py` |
| **Token usage** | `context-router` priorise P0-P4 | ✅ Bon — mais thresholds hardcodés |
| **Outil discovery** | `tool-registry.py` scan AST à chaque appel | ⚡ Cache le registry (validé : pas de mutation inter-session) |
| **Test speed** | 3,020 tests en 95s | 🟡 Correct — `quick-check` = 0.66s pour le dev flow |
| **Import chains** | Certains outils importent d'autres outils via `importlib.util` | Acceptable pour stdlib-only |
| **MCP cold start** | Premier appel MCP = discovery complète | ⚡ Pré-calculer le manifest au build |

### 🔬 Dr. Quinn (Problem Solver) — Goulots d'étranglement

1. **Context window saturation** — Le vrai goulot. 200K tokens Copilot, mais les instructions BMAD + copilot-instructions.md + agent persona + conversation-summary consomment ~15-25K tokens AVANT la première requête.
   - **FIX** : `context-router` devrait être consulté DANS les instructions Copilot. Ajouter un `.prompt.md` qui fait `#file:context-router.py plan --agent {current_agent}` et injecte le résultat.

2. **Conversation-summary bloat** — Le résumé grossit avec la conversation. Pas de mécanisme de compression.
   - **FIX** : Implémenter un `conversation-summarizer` qui compresse le résumé quand il dépasse N tokens, gardant les décisions/faits et éliminant le narratif.

3. **88 outils Python** — Trop nombreux pour la discovery MCP. Chaque `list_tools` retourne 88 entrées.
   - **FIX** : `tool-registry.py` supporte déjà le filtrage — exposer des groupes thématiques au lieu de tout.

---

## 4. INNOVATION

### 🧠 Carson (Brainstorming Coach) — Les idées les plus disruptives

> **YES AND** on pousse LOIN, on filtrera après !

| # | Idée | Agent source | Faisabilité |
|---|------|-------------|------------|
| 1 | **Agent Genome Export** — Exporter un agent comme "gène" portable, importable dans un autre projet BMAD. Un agent = un package réutilisable avec ses learnings, sa mémoire, ses prompts. | 🤖 Bond | 🏗️ |
| 2 | **Conversation Forking** — Comme git branch mais pour les conversations. Fork une discussion → explore alternative → merge ou discard. | 🔄 Wendy | 🏗️ (`quantum-branch.py` + `conversation-branch.py` existent) |
| 3 | **Dream-Driven Development** — `dream.py` ne fait pas que consolider, il PROPOSE des stories. Les insights deviennent des stories dans le backlog automatiquement. | 📖 Sophia | ⚡ (`dream.py` + `incubator.py` existent) |
| 4 | **Collective Intelligence Score** — Score global qui mesure combien le SYSTÈME est intelligent (pas juste un agent). Agrège : diversity index, memory quality, decision coherence, learning rate. | ⚡ Victor | ⚡ (`antifragile-score.py` + `quality-score.py` + `agent-darwinism.py`) |
| 5 | **BMAD-as-a-Library** — Les outils Python deviennent importables comme un package. `from grimoire import dream, forge, immune_system`. | 💻 Amelia | 🏗️ (refactoring + setup.py/pyproject.toml) |

---

## 5. SÉCURITÉ

### 🛡️ Winston + immune-system.py — Analyse

**Ce qui existe :**

| Couche | Outil | État |
|--------|-------|------|
| Immunité innée | `immune-system.py` — règles statiques OWASP | ✅ |
| Immunité adaptative | `immune-system.py` — apprend des incidents | ✅ |
| Integrity checks | `agent-integrity.py` — hash + drift detection | ✅ |
| CC verification | `cc-verify.sh` — completion criteria | ✅ |
| Bias detection | `bias-toolkit.py` — biais dans les outputs | ✅ |
| Anti-hallucination | HUP (BM-50) — protocole + trust scores | ✅ (protocole) |
| Cross-validation | CVTL (BM-52) — double vérification | ✅ (protocole) |
| Secrets detection | `immune-system.py` innate rules | 🟡 Basic regex |

**Gaps identifiés :**

| Gap | Sévérité | Solution |
|-----|---------|---------|
| **Pas de scan de dépendances** | MEDIUM | `dep-check.py` existe mais ne scanne pas les CVE |
| **Pas de sandbox pour les outils** | LOW | Les outils Python s'exécutent dans le même process — pas critique car stdlib-only |
| **Prompt injection dans les inputs MCP** | HIGH | Les outils MCP acceptent des strings arbitraires |
| **Pas d'audit trail persistent** | MEDIUM | `bmad-trace.md` est volatile (Markdown) — pas de log JSONL sécurisé |

### 💡 Proposition : Security Hardening Sprint

1. **MCP Input Sanitization** — Ajouter un décorateur `@sanitize_input` à chaque handler MCP dans `bmad-mcp-tools.py`. Escape les patterns d'injection connus.
2. **Audit Trail JSONL** — `grimoire-log.py` écrit déjà en JSONL. Le rendre tamper-evident avec des hash chains (chaque entrée hash = sha256(prev_hash + content)).
3. **dep-check.py CVE mode** — Ajouter un mode `--cve` qui compare les dépendances contre une base locale de CVEs connues (stdlib = safe, optionnels = à vérifier).

---

## 6. FICHIERS .PROMPT.MD

### 📚 Paige (Tech Writer) — Inventaire

**90 fichiers `.prompt.md`** dans `.github/prompts/` — couverture massive :

| Catégorie | Nombre | Exemples |
|-----------|--------|---------|
| BMM (agents métier) | 28 | `bmm-create-prd`, `bmm-dev-story`, `bmm-code-review` |
| BMB (builders) | 11 | `bmb_create_agent`, `bmb_validate_module` |
| TEA (test architect) | 8 | `tea-testarch-framework`, `tea-testarch-atdd` |
| CIS (creative/innovation) | 5 | `cis-brainstorming`, `cis-innovation-strategy` |
| Agents directs | 12 | `architect.prompt.md`, `dev.prompt.md` |
| Teams | 5 | `team-vision/`, `team-ops/`, `team-build/` |
| Core (editorial, shard) | 4 | `editorial-review-prose`, `shard-doc`, `index-docs` |
| Autres | ~17 | `help`, `party-mode`, `quick-flow-solo-dev` |

### 🔬 Dr. Quinn — Ce qui MANQUE

| .prompt.md manquant | Impact | Agent |
|---------------------|--------|-------|
| `memory-review.prompt.md` | Impossible de déclencher un audit mémoire via /prompt | Memory |
| `security-scan.prompt.md` | Pas de raccourci pour un scan sécurité | Immune |
| `dream.prompt.md` | Pas de raccourci pour le dream mode | Dream |
| `preflight.prompt.md` | Le preflight existe en task mais pas en prompt | Quality |
| `tool-status.prompt.md` | Vue d'ensemble des outils | Registry |
| `evolve-agents.prompt.md` | Évolution automatique | Darwinism |

### 💡 Proposition

Générer les prompts manquants via un script — `agent-forge.py` ou un nouveau `prompt-forge.py` qui :
1. Scanne tous les outils dans `framework/tools/`
2. Détecte ceux qui n'ont pas de `.prompt.md` correspondant
3. Génère un `.prompt.md` basique depuis la docstring + argparse du tool
4. Output dans `.github/prompts/`

**Estimation : ~20 .prompt.md à créer pour une couverture complète.**

---

## 7. CRÉATION DYNAMIQUE D'AGENTS

### 🤖 Bond (Agent Builder) — Arsenal existant

| Outil | Fonction | État |
|-------|---------|------|
| `agent-forge.py` | Génère un scaffold d'agent depuis une description, des gaps ou une trace | ✅ |
| `agent-darwinism.py` | Évalue la fitness et propose promotion/deprecation/hybridation | ✅ |
| `agent-integrity.py` | Vérifie conformité BMAD Core | ✅ |
| `agent-bench.py` | Benchmark de performance agent | ✅ |
| `agent-caller.py` | Invocation programmatique d'agents | ✅ |
| `mirror-agent.py` | Clone un agent pour le challenger | ✅ |
| `agent-worker.py` | Exécution déléguée | ✅ |
| `crispr.py` | Mutation ciblée d'un agent | ✅ |
| `new-game-plus.py` | Reset avec bonus d'un agent | ✅ |

**9 outils de gestion du cycle de vie agent — la couverture la plus complète possible.**

### ⚡ Victor — La pièce manquante

> **Le problème n'est pas la création — c'est l'ACTIVATION AUTOMATIQUE dans VS Code.**

Un agent créé par `agent-forge.py` produit un `.proposed.md`. Ensuite :
1. Review humain → valide
2. `bmad-init.sh forge --install` → installe
3. L'agent est disponible dans le manifest

**Ce qui manque** : que le nouvel agent apparaisse automatiquement dans le **dropdown des agents VS Code** et dans les **`.prompt.md`** sans relancer la session.

### 💡 Proposition : Hot-reload Agent Pipeline

```
agent-forge.py → .proposed.md → review → install 
                                           ↓
                                    agent-manifest.csv ← mise à jour
                                           ↓
                                    .github/prompts/{agent}.prompt.md ← auto-generated
                                           ↓
                                    copilot-instructions.md ← mise à jour du tableau agents
```

Tout ce pipeline existe en pièces détachées. **Un script `agent-lifecycle.py` qui orchestre les 4 étapes** serait le chaînon manquant.

---

## 8. SKILLS

### 📚 Paige — État des skills VS Code

**Skills actuels détectés dans l'environnement Copilot :**

| Skill | Source | Usage |
|-------|--------|-------|
| `agent-customization` | VS Code built-in | Créer/modifier .instructions.md, .prompt.md, .agent.md |
| `summarize-github-issue-pr-notification` | GitHub PR extension | Résumer issues/PRs |
| `suggest-fix-issue` | GitHub PR extension | Proposer des fixes |
| `form-github-search-query` | GitHub PR extension | Recherche GitHub |
| `show-github-search-result` | GitHub PR extension | Afficher résultats |

### 💡 Propositions de Skills BMAD

Les skills VS Code sont définis par des fichiers `SKILL.md` — nous pouvons en créer pour le kit :

| Skill proposé | Trigger | Ce qu'il fait |
|----------------|---------|--------------|
| `bmad-memory-audit` | "audite la mémoire", "santé mémoire" | Lance memory-lint + dream + flywheel-score |
| `bmad-security-scan` | "scan sécurité", "vulnérabilités" | Lance immune-system scan + dep-check |
| `bmad-agent-health` | "santé des agents", "fitness" | Lance agent-darwinism + antifragile-score |
| `bmad-context-optimize` | "optimise le contexte", "token budget" | Lance context-router + token-budget check |
| `bmad-preflight` | "preflight", "prêt à shipper?" | Lance preflight-check + harmony-check |
| `bmad-dream` | "dream mode", "consolidation" | Lance dream.py + cognitive-flywheel |

**Avantage** : Les skills sont invoqués automatiquement par Copilot quand il détecte l'intent — pas besoin de syntax slash ou de prompt explicite.

---

## 9. OUTILS — ACQUISITION ET COMPÉTENCES

### 🧙 BMad Master — Capacités d'acquisition d'outils

**Outils natifs VS Code découverts cette session :**

| Outil | Découvert via | Usage |
|-------|--------------|-------|
| `await_terminal` | `tool_search_tool_regex` | Attendre la fin d'une commande |
| `kill_terminal` | `tool_search_tool_regex` | Terminer un processus background |
| `get_changed_files` | `tool_search_tool_regex` | Diff des fichiers modifiés |
| `create_and_run_task` | `tool_search_tool_regex` | Créer + lancer une tâche VS Code |
| `run_task` | `tool_search_tool_regex` | Lancer une tâche existante |
| `vscode_listCodeUsages` | `tool_search_tool_regex` | Trouver les usages d'un symbole |
| `vscode_renameSymbol` | `tool_search_tool_regex` | Renommer un symbole partout |

**Mécanisme de discovery** : `tool_search_tool_regex` avec des patterns regex. Les outils "deferred" ne sont pas disponibles tant qu'ils ne sont pas découverts.

### 🔬 Dr. Quinn — Stratégie d'acquisition proactive

> Le système DOIT chercher les outils qu'il n'a pas **AVANT** d'en avoir besoin.

| Stratégie | Mécanisme | État |
|-----------|-----------|------|
| **Discovery on-demand** | `tool_search_tool_regex` quand l'intent nécessite un outil | ✅ Actuel |
| **Discovery at session start** | Scanner tous les deferred tools disponibles | 🔴 Pas fait |
| **Tool capability mapping** | Maintenir une map intent → tool pour le routing | 🔴 Pas persisté |
| **MCP server auto-install** | Si un tool manque, chercher s'il existe comme MCP server et proposer l'install | 🔴 |

### 💡 Propositions

1. **Boot Scan** — En début de session, lancer un scan `tool_search_tool_regex` avec pattern `.*` pour découvrir TOUS les outils disponibles. Stocker le résultat dans la session memory.

2. **Tool Map en mémoire repo** — Écrire dans `/memories/repo/available-tools.md` la liste complète des outils découverts avec leur description. Mise à jour automatique.

3. **MCP Install Suggestion** — Quand un outil manque, `concierge.py` peut suggérer :
   - Un outil BMAD existant mais pas encore exposé en MCP
   - Un MCP server tiers (via une liste curatée dans `_bmad/_memory/mcp-catalog.yaml`)

---

## 10. CONTRÔLE D'INTERFACE / UI (OpenClaw)

### 🎨 Sally (UX Designer) — Analyse

> **OpenClaw** = outil open-source permettant à un LLM de contrôler une interface graphique (browser, desktop app) via des actions (click, type, scroll, screenshot analysis).

**Capacité actuelle du système : NULLE.**

Les agents BMAD opèrent exclusivement en mode texte :
- Fichiers Markdown/YAML
- CLI Python
- MCP tools
- VS Code API (via Copilot tools)

### ⚡ Victor — Le potentiel est ÉNORME

| Use case | Valeur | Complexité |
|----------|--------|-----------|
| **UI Testing automatisé** | L'agent QA contrôle le browser pour tester une app web | 🏗️ |
| **Dashboard monitoring** | L'agent lit des dashboards (Grafana, etc.) via screenshot | 🏗️ |
| **Form filling** | L'agent remplit des formulaires complexes | MEDIUM |
| **Documentation screenshot** | L'agent capture des screenshots pour la doc tech | ⚡ |
| **Competitive analysis** | L'agent browse des sites concurrents | 🏗️ |

### 💡 Propositions

1. **MCP Browser Bridge** — Créer un MCP server qui expose les actions browser/UI :
   ```
   mcp_ui_navigate(url)
   mcp_ui_click(selector)
   mcp_ui_type(selector, text)
   mcp_ui_screenshot() → image
   mcp_ui_read_page() → text content
   ```
   Utiliser Playwright (déjà compétence de TEA) comme backend.

2. **Agent Vision Mode** — Certains modèles (GPT-4V, Claude) supportent l'analyse d'images. Ajouter un mode `--vision` aux agents qui leur permet de recevoir des screenshots et d'en extraire des informations.

3. **OpenClaw Integration** — À évaluer quand le projet sera plus mature. Actuellement, le combo Playwright + MCP est plus pragmatique et mieux intégré à l'écosystème.

**Verdict** : 🏗️ Non prioritaire mais à garder en veille. Le ROI est maximal sur le use case "UI testing" qui peut commencer avec Playwright pur.

---

## 11. ÉCONOMIE DES TOKENS / OPTIMISATION

### 🏗️ Winston — Stack de gestion tokens existante

| Couche | Outil | Mécanisme |
|--------|-------|-----------|
| **Budget enforcement** | `token-budget.py` | 60% warn → 80% summarize → 95% drop |
| **Context routing** | `context-router.py` | Priorisation P0-P4, fenêtres par modèle |
| **Context summarization** | `context-summarizer.py` | Compression des contextes P2/P3 |
| **Semantic cache** | `semantic-cache.py` | Cosine > 0.9 → cache hit, skip LLM |
| **LLM router** | `llm-router.py` | Route simple→petit modèle, complex→gros modèle |
| **Sensory buffer** | `sensory-buffer.py` | Buffer de données brutes avant injection |

**6 outils de gestion token — l'un des systèmes les plus sophistiqués.**

### 📊 Mary — Métriques manquantes

| Métrique | Pourquoi | Comment |
|----------|---------|---------|
| **Token réel vs estimé** | On estime à 4 chars/token mais Copilot ne donne pas le count réel | Impossible sans API access |
| **Cache hit rate en production** | `semantic-cache.py` a les stats mais pas de collecte automatique | ⚡ Intégrer dans `grimoire-daemon.py` |
| **Contexte gaspillé** | Combien de tokens de contexte sont injectés mais jamais utilisés | 🏗️ Nécessite tracking d'usage |
| **ROI par source** | Quel fichier de contexte apporte le plus de valeur par token dépensé | 🏗️ Corrélation context ↔ output quality |

### 💡 Propositions

1. **Token Dashboard** — `synapse-dashboard.py` existe mais n'inclut pas les métriques token. Ajouter un panel token dédié :
   ```
   Token Usage Dashboard
   ├── Window: 200K (copilot)
   ├── System: ~22K (instructions + persona + summary)
   ├── Context: ~45K (fichiers chargés)
   ├── Available: ~133K
   ├── Cache hits this session: 7
   └── Estimated savings: 42K tokens
   ```

2. **Aggressive Context Pruning** — Le `context-router` devrait être exécuté DANS le `.instructions.md` de chaque session. Résultat : au lieu de charger tout `copilot-instructions.md` + tous les manifests, ne charger que ce qui est pertinent pour l'intent courant.

3. **Instruction Sharding** — Le `copilot-instructions.md` fait ~100 lignes. Le `shard-doc.prompt.md` existe déjà. Appliquer le sharding aux instructions elles-mêmes : split par domaine, chargement conditionnel.

---

## 12. AUTO-ÉVOLUTION

### ⚡ Victor — Vision stratégique

**C'est LE sujet clé.** Un système qui s'améliore automatiquement sans intervention humaine explicite.

**Composants existants pour l'auto-évolution :**

```
           ┌─────────────────────────────────────────────┐
           │           BOUCLE D'AUTO-ÉVOLUTION            │
           │                                              │
    ┌──────┤  dream.py ──→ insights cross-domaine         │
    │      │      ↓                                       │
    │      │  cognitive-flywheel.py ──→ patterns + score   │
    │      │      ↓                                       │
    │      │  agent-darwinism.py ──→ fitness + évolution   │
    │      │      ↓                                       │
    │      │  crispr.py ──→ mutations ciblées              │
    │      │      ↓                                       │
    │      │  agent-forge.py ──→ nouveaux agents           │
    │      │      ↓                                       │
    │      │  immune-system.py ──→ validation sécurité     │
    │      │      ↓                                       │
    │      │  antifragile-score.py ──→ score global        │
    │      │      ↓                                       │
    │      │  failure-museum.py ──→ capitalisation         │
    │      └──────┤                                       │
    │             │ ───→ retour au dream ──→ cycle suivant │
    └─────────────┘                                       │
                                                          │
    SUPERVISEURS :                                        │
      grimoire-daemon.py (trigger)                        │
      self-healing.py (réparation)                        │
      early-warning.py (anticipation)                     │
      orchestrator.py (coordination)                      │
    ──────────────────────────────────────────────────────┘
```

### 🏃 Bob (Scrum Master) — Roadmap d'implémentation

**La boucle est PRESQUE complète. Manquent :**

| Pièce manquante | Impact | Sprint |
|-----------------|--------|--------|
| **Déclencheur automatique** | `grimoire-daemon.py` existe mais ne lance pas la boucle dream→darwinism→crispr | S1 |
| **Pipeline de mutation** | `crispr.py` mute mais ne propage pas les changements (manifest, prompts) | S1 |
| **Feedback loop closing** | Après une mutation, le système ne vérifie pas si le score s'est amélioré | S2 |
| **Human-in-the-loop gate** | Pas de garde-fou pour empêcher des mutations nocives sans review | S1 |
| **Persistence du score** | `antifragile-score.py` calcule mais ne persiste pas l'historique | S1 |

### 💡 Proposition : Evolution Engine (EE)

Un nouveau composant `evolution-engine.py` qui orchestre :

```yaml
evolution_cycle:
  trigger: weekly | on_demand | on_score_drop
  
  phases:
    1_observe:
      - dream.py --since {last_cycle}
      - cognitive-flywheel.py analyze
      - agent-darwinism.py evaluate
    
    2_mutate:
      - crispr.py --from darwinism-recommendations
      - agent-forge.py --from-gap (si des gaps détectés)
    
    3_validate:
      - immune-system.py scan (sécurité)
      - agent-integrity.py (conformité)
      - harmony-check.py (cohérence)
    
    4_score:
      - antifragile-score.py → persist to _bmad/_memory/evolution-history.jsonl
      - compare with previous score
      - if score_drop > 5% → rollback mutation
    
    5_report:
      - Résumé pour l'humain dans _bmad-output/evolution-report.md
      - Mutations appliquées, scores avant/après, rollbacks éventuels
  
  guardrails:
    - max_mutations_per_cycle: 3
    - require_human_approval_above: critical (new agent, delete agent)
    - auto_rollback_on: test_failure | score_drop > 10%
```

---

## SYNTHÈSE DES PRIORITÉS

### Matrice Impact × Effort

| ID | Action | Impact | Effort | Priorité |
|----|--------|--------|--------|----------|
| M1 | Memory Bridge VS Code ↔ _bmad/_memory | HIGH | LOW | ⭐⭐⭐ |
| M2 | Memory Decay Scoring | MEDIUM | LOW | ⭐⭐ |
| M3 | Cross-session Summary Chain | HIGH | LOW | ⭐⭐⭐ |
| P1 | Daemon Pre-compute Pipeline | HIGH | MEDIUM | ⭐⭐⭐ |
| O1 | Context Router dans .instructions.md | HIGH | LOW | ⭐⭐⭐ |
| O2 | Tool Registry caching | MEDIUM | LOW | ⭐⭐ |
| I1 | Dream-Driven Development (dream→stories) | HIGH | LOW | ⭐⭐⭐ |
| S1 | MCP Input Sanitization | HIGH | LOW | ⭐⭐⭐ |
| S2 | Audit Trail hash chain | MEDIUM | LOW | ⭐⭐ |
| PR1 | Prompt Forge (auto-gen .prompt.md) | MEDIUM | LOW | ⭐⭐ |
| SK1 | Skills BMAD pour VS Code | HIGH | MEDIUM | ⭐⭐⭐ |
| T1 | Boot Scan des outils au lancement | MEDIUM | LOW | ⭐⭐ |
| T2 | Token Dashboard panel | MEDIUM | MEDIUM | ⭐⭐ |
| UI1 | MCP Browser Bridge (Playwright) | HIGH | HIGH | ⭐ (plus tard) |
| E1 | Evolution Engine complet | VERY HIGH | HIGH | ⭐⭐ (Sprint 2) |
| E2 | Agent Lifecycle hot-reload | HIGH | MEDIUM | ⭐⭐ |

### Top 5 Quick Wins (Sprint immédiat)

1. **M3 — Cross-session Summary Chain** → Extrêmement facile, impact immédiat sur la continuité
2. **M1 — Memory Bridge** → Hook dans `grimoire-daemon.py`, 50 lignes
3. **O1 — Context Router dans instructions** → Réduit le gaspillage token de 30%+
4. **S1 — MCP Input Sanitization** → Sécurité critique, décorateur simple
5. **I1 — Dream-Driven Development** → Connecter `dream.py` → `incubator.py`, pipeline existant

### Top 3 Strategic (Sprint 2)

1. **SK1 — Skills BMAD** → Game-changer pour l'UX — les outils deviennent invocables par intent
2. **E1 — Evolution Engine** → La méta-capacité — le système qui s'améliore tout seul
3. **P1 — Daemon Pre-compute** → Parallélisme temporel, l'agent est toujours "prêt"

---

## SCORES DE MATURITÉ PAR DOMAINE

| Domaine | Score /10 | Justification |
|---------|-----------|--------------|
| 1. Mémoire | **8/10** | 16 outils, couverture exceptionnelle. Manque decay + bridge VS Code |
| 2. Parallélisation | **5/10** | Architecturé mais contraint par le mono-thread Copilot |
| 3. Optimisation | **7/10** | Stack token solide. Manque pruning agressif + métriques réelles |
| 4. Innovation | **9/10** | 88 outils + dream + darwinism + forge — l'un des systèmes les plus complets |
| 5. Sécurité | **6/10** | Immune system + intégrité OK. Manque sanitization MCP + audit trail |
| 6. .prompt.md | **8/10** | 90 prompts — couverture très large. ~20 manquants |
| 7. Création d'agents | **9/10** | 9 outils lifecycle. Manque hot-reload dans VS Code |
| 8. Skills | **3/10** | Quasi-inexistant côté BMAD. Gros potentiel |
| 9. Acquisition d'outils | **6/10** | Discovery on-demand OK. Manque proactivité |
| 10. Contrôle UI | **1/10** | Absent. Non prioritaire |
| 11. Token economy | **7/10** | Stack complète (budget + router + cache + llm-router). Manque dashboard |
| 12. Auto-évolution | **7/10** | Tous les composants existent. Manque l'orchestre (Evolution Engine) |

**Score global système : 6.3/10** — Excellente base d'innovation, besoin de **connexion entre les pièces existantes** plus que de nouvelles pièces.

---

> 🧙 **BMad Master** — Ce brainstorm révèle un constat clé : **le système possède déjà 95% des briques nécessaires**. Le travail restant est principalement de la **plomberie** — connecter les composants existants en pipelines automatisés.
> 
> Le plus grand ROI immédiat est dans les **Skills VS Code** (rendre les outils invocables par intention) et le **Memory Bridge** (unifier les deux systèmes mémoire).
> 
> Le plus grand ROI stratégique est l'**Evolution Engine** — la boucle d'auto-amélioration qui transforme le système d'un outil en un organisme vivant.

---

*Produit par tous les agents BMAD en Party Mode — orchestré par SOG BM-53*
