# PARTY BRAINSTORM — Grimoire Kit v3 Platform
## Session du 2026-03-05 — Mémoire active de recherche

> Ce document est la mémoire active de la session de brainstorming party-mode.
> Les décisions fermes sont marquées **[DÉCIDÉ]** et seront migrées vers la mémoire long terme.
> Le reste est exploratoire.

---

## STATUS: LIVRÉ — Résultats consolidés

---

# PARTIE 1 — TODO LIST CONSOLIDÉE

## 1.1 Bugs critiques à corriger

| # | Bug | Fichier | Sévérité |
|---|-----|---------|----------|
| B1 | `open()` sans `encoding="utf-8"` (3 occurrences) | `framework/memory/maintenance.py` L82, L87, L162 | 🔴 High |
| B2 | 82 `except...pass` silencieux dans les outils | `framework/tools/*.py` (réparti) | 🟡 Medium |

## 1.2 Améliorations techniques validées par l'équipe

| # | Amélioration | Owner | Priorité |
|---|-------------|-------|----------|
| T1 | CLI unifiée `grimoire <cmd>` wrapper | Dev (Amelia) | P0 |
| T2 | Découper `r-and-d.py` (2523 lignes) | Architecte (Winston) | P1 |
| T3 | Registre de dépendances inter-outils (valider au boot) | Architecte | P1 |
| T4 | Logging structuré dans les except...pass | Dev | P2 |
| T5 | Test intégration NSO chaîne complète | QA (Quinn) | P1 |
| T6 | Smoke test `bmad-init.sh --auto` en CI | QA | P1 |
| T7 | `grimoire doctor` — diagnostic en 1 commande | Dev | P2 |
| T8 | Progressive onboarding guide (J1/S1/M1) | Tech Writer (Paige) | P2 |

---

# PARTIE 2 — CHALLENGE DES SKILLS, PROMPTS ET WORKFLOWS

## 2.1 Challenge des Prompts d'agents

### 🏗️ Winston (Architecte) vs 📊 Mary (Analyste) — Débat : "Nos prompts agents sont-ils trop longs ?"

**Winston :** *"Les personas agents dans l'agent-manifest.csv sont courtes et percutantes — 2-3 lignes pour communicationStyle, principles. C'est ce qu'il faut. MAIS l'agent-base.md fait 100+ lignes de protocole. Chaque agent le charge. Ça consomme du budget context pour CHAQUE session. Le Context Router devrait injecter seulement les sections pertinentes d'agent-base.md selon la tâche."*

**Mary :** *"D'accord sur le diagnostic. Mais le VRAI problème c'est que les principes des agents sont trop génériques. 'Load resources at runtime' pour bmad-master — c'est une règle d'implémentation, pas un principe business. Les personas devraient avoir des principes ACTIONNABLES liés à leur domaine, pas des règles techniques."*

**Résolution :** Les prompts devraient être en 2 couches :
1. **Core protocol** (CC, Plan/Act, Grice) — injecté toujours, mais compacté à ~30 lignes
2. **Domain principles** — spécifiques à chaque agent, actionnables

> **[DÉCIDÉ]** Refactorer agent-base.md en version condensée + version complète (chargée à la demande)

### 2.2 Challenge des Workflows

**🏃 Bob (SM) :** *"Le boomerang-orchestration.md est un workflow YAML documenté mais jamais exécuté programmatiquement. C'est un guide pour le LLM, pas un workflow exécutable. Le workflow engine de BMAD Core (`workflow.xml`) gère les .yaml step-by-step — mais nos workflows sont des .md que le LLM lit comme des instructions."*

**💻 Amelia (Dev) :** *"C'est le point clé. On a deux mondes : les workflows BMAD Core (YAML + engine) et nos workflows framework (Markdown + LLM). L'orchestrator.py fait du ThreadPool Python, pas de l'orchestration LLM. La confusion est réelle."*

**Résolution :** 
- Les workflows .md = **playbooks pour le LLM** (party-mode, brainstorming)
- L'orchestrator.py = **coordination de workers Python** (pas de LLM réel)
- Il manque un **vrai orchestrateur LLM** qui spawne des sessions Copilot/Claude/API

> **[DÉCIDÉ]** Clarifier la taxonomie : Playbook (MD pour LLM) vs Pipeline (Python exécutable) vs Orchestration (multi-LLM réel)

---

# PARTIE 3 — PARALLÉLISME LLM RÉEL

## 3.1 Analyse de l'existant

### 📋 John (PM) : "Est-ce qu'on lance VRAIMENT plusieurs LLM en parallèle ?"

**Verdict : NON.** Voici la réalité :

| Composant | Ce qu'il prétend | Ce qu'il fait réellement |
|-----------|-----------------|--------------------------|
| `orchestrator.py` mode "parallel" | "Agents sur LLMs séparés" | `ThreadPoolExecutor` Python qui exécute des steps locaux. Aucun appel LLM. Le worker fait du persona switching dans le même contexte. |
| `agent-worker.py` | "Worker isolé avec son propre LLM" | Charge la persona depuis un fichier. `execute_task()` produit un output STRING, pas un appel LLM API. |
| `message-bus.py` | "InProcess, Redis, NATS" | Seul `InProcessBus` (queue mémoire) est implémenté. Redis et NATS sont des stubs. |
| `background-tasks.py` | "Agents en arrière-plan" | Écrit un JSON de tâche sur disque. Pas de vrai processus background. |
| Party Mode | "Multi-agent conversation" | Un seul LLM simule toutes les personas (c'est le bon pattern pour un IDE) |

### 🏗️ Winston (Architecte) : "C'est normal et c'est BIEN."

*"Dans un contexte IDE (VS Code Copilot), on n'a qu'UNE session LLM à la fois. Le parallélisme réel de sessions LLM nécessite :
1. Plusieurs API keys / sessions Copilot simultanées → impossible dans l'IDE
2. Un serveur d'orchestration externe (LangGraph, CrewAI) → hors scope IDE
3. Ou le MCP Server qui expose des tools appelés par le LLM → c'est ce qu'on fait mais c'est séquentiel"*

**Le vrai parallélisme gagnable :**
- **MCP tools parallèles** : Le LLM Copilot peut appeler plusieurs MCP tools en parallèle (batch call). Nos tools le supportent déjà.
- **Background processing** : Pendant que le user parle au LLM, des scripts Python font du travail (indexation, dream, stigmergy evaporate). C'est du **parallélisme CPU**, pas LLM.
- **Multi-IDE** : Un projet ouvert dans VS Code + Cursor simultanément → deux sessions LLM réelles. Le A2A protocol (`agent2agent.md`) adresse ce use case.

> **[DÉCIDÉ]** L'orchestrator.py ne doit PAS prétendre faire du multi-LLM. Renommer le mode "parallel" en "concurrent-cpu" et documenter honnêtement les limites.

## 3.2 Ce qu'on pourrait réellement faire

| Stratégie | Faisabilité | Impact |
|-----------|-------------|--------|
| MCP batch tools (déjà supporté) | ✅ Existant | Rapide — tools indépendants en parallèle |
| Background Python daemon (dream, indexing) | ✅ Faisable | Consolidation hors-session pendant que l'user travaille |
| Multi-IDE via A2A | 🟡 Prototype | 2 LLM réels sur la même codebase |
| API externe (Claude API, OpenAI API) | 🟡 Possible | Spawner des agents via API, coûteux |
| Agent Protocol (Google A2A) cross-tool | 🔴 Futur | Standard pas encore stabilisé |

---

# PARTIE 4 — BACKGROUND ET BRANCHING AUTOMATIQUES

## 4.1 État actuel

**💻 Amelia (Dev) :** *"Les outils existent mais ne sont pas AUTO-DÉCLENCHÉS."*

- `background-tasks.py` — crée des fichiers JSON mais ne lance pas de vrais processus
- `conversation-branch.py` — branching de contexte, mais faut le demander manuellement
- `session-save.py` — sauvegarde de session, idem
- `bmad-init.sh session-branch` — branching git, fonctionnel mais manuel

**Ce qui manque :**
1. **Auto-branch** : Quand un agent dit `[THINK]` sur une décision, créer automatiquement une branche de conversation pour explorer sans polluer le main
2. **Auto-background** : Déclencher `dream.py --quick` et `stigmergy.py evaporate` automatiquement en fin de session
3. **Pre-session hook** : `maintenance.py health-check` + `memory-lint` au démarrage

> **[DÉCIDÉ]** Créer un `session-lifecycle.py` qui orchestre : pre-session (health-check, memory-lint) → post-session (dream quick, stigmergy evaporate, session-save)

---

# PARTIE 5 — BENCHMARK VS OPENCLAW

## 5.1 Qu'est-ce qu'OpenClaw fait ?

**📊 Mary (Analyste) :** *"OpenClaw (anciennement OpenHands/OpenDevin) est un framework d'agents coding avec :"*

| Feature OpenClaw | Grimoire-kit l'a ? | Commentaire |
|-----------------|---------------------|-------------|
| **Sandboxed execution** (Docker container) | ❌ Non | Nos agents exécutent dans le terminal user, pas isolé |
| **Tool calling natif** (bash, python, browser) | 🟡 Via MCP | On expose des tools MCP mais pas browser |
| **Plan → Execute loop** | ✅ Plan/Act Mode | Équivalent |
| **Memory across sessions** | ✅ Supérieur | Notre mémoire (Qdrant, JSONL, learnings, failure-museum) est plus riche |
| **Multi-model routing** | ✅ llm-router.py | Équivalent |
| **Self-reflection / self-critique** | 🟡 Partiel | Reasoning-stream existe mais pas de boucle auto-critique systématique |
| **Web browsing** | ❌ Non | OpenClaw peut naviguer le web pour research |
| **File editing tools** | ✅ Via IDE | Copilot/Cursor éditent les fichiers nativement |
| **GUI interaction** | ❌ Non | OpenClaw a un computer-use-like agent |
| **Evaluation framework** | 🟡 Agent-bench | OpenClaw a SWE-Bench intégré, nous avons agent-bench |
| **Multi-agent orchestration** | 🟡 Simulated | OpenClaw fait du multi-agent avec Workers réels |

### 5.2 Ce qu'on devrait prendre d'OpenClaw

> **Débat 🏗️ Winston vs ⚡ Victor (Innovation Strategist)**

**Winston :** *"On ne devrait PAS copier le sandboxing Docker. Notre force c'est l'intégration IDE native. On est dans le workflow du développeur, pas à côté."*

**Victor :** *"D'accord. Mais 3 choses manquent cruellement :"*

1. **Self-critique automatique** — Après chaque output agent, un "critique intérieur" vérifie la cohérence avec les principes, le contexte, les décisions passées. OpenClaw le fait via self-reflection loops.

2. **Web research capability** — Les agents n'ont aucun accès au web. Pas de Perplexity, pas de search. Pour la veille techno (what's new in Go 1.24 ?) l'agent est aveugle.

3. **Evaluation systématique** — Agent-bench analyse les traces APRÈS. Il faudrait un "runtime quality gate" : chaque réponse agent est scorée EN TEMPS RÉEL (cohérence, hallucination, pertinence).

> **[DÉCIDÉ]** Implémenter : (1) Self-critique post-output, (2) MCP web search tool, (3) Runtime quality scoring

---

# PARTIE 6 — SÉCURITÉ DU PROJET

## 6.1 Audit sécurité par l'équipe

### 🛡️ Immune System — Bugs trouvés

**🧪 Murat (Test Architect) + 💻 Amelia (Dev) :**

| Risque | Sévérité | Détail | Status |
|--------|----------|--------|--------|
| Pas de sandbox d'exécution | 🟡 Medium | Les outils Python lisent/écrivent le filesystem sans restriction. `crispr.py` modifie des fichiers agents directement. | Design intentionnel |
| SSRF potentiel dans `rag-indexer.py` | 🟠 High | `urllib.request.urlopen(req, timeout=30)` à L501 — l'URL est construite depuis la config Qdrant (user-controlled). Un `qdrant_url: http://169.254.169.254/metadata` dans project-context.yaml → SSRF | **À corriger** |
| `importlib.util.exec_module` partout | 🟡 Medium | 10+ outils chargent d'autres outils via `exec_module`. Si un outil est compromis (injection dans le .py), ça cascade. | Acceptable si filesystem sûr |
| Secrets potentiels dans `project-context.yaml` | 🟡 Medium | `qdrant_url`, `api_key` pourraient être commités. Pas de `.gitignore` pattern pour ça. | **À corriger** |
| `subprocess.run` dans `cc-verify.sh` | 🟢 Low | Les commandes sont hardcodées, pas d'injection user | OK |
| Pas de signature des fichiers agents | 🟡 Medium | Un agent modifié par un attaquant (supply chain) serait chargé tel quel | Futur |

### 6.2 Actions sécurité

> **[DÉCIDÉ]**

| # | Action | Priorité |
|---|--------|----------|
| S1 | Valider/sanitiser `qdrant_url` dans rag-indexer.py et rag-retriever.py (whitelist de schémas http/https, blocage IP privées/metadata) | P0 |
| S2 | Ajouter `.gitignore` patterns pour `qdrant_data/`, `*.key`, `*.pem`, `secrets.yaml` | P0 |
| S3 | Mode `--dry-run` par défaut sur les outils destructifs (crispr splice/excise, time-travel restore) | P1 |
| S4 | Checksum SHA256 des fichiers agents au boot, alerte si modifié | P2 |
| S5 | Rate limiting sur MCP tools (éviter DOS accidentel) | P2 |

---

# PARTIE 7 — MÉMOIRE ET INTELLIGENCE DES AGENTS

## 7.1 État actuel de la mémoire

```
_memory/
├── shared-context.md        ← Tout-en-un, risque de bloat
├── decisions-log.md         ← Append-only, pas de pruning auto
├── failure-museum.md        ← Markdown, pas structuré
├── agent-learnings/         ← 1 fichier par agent
├── contradiction-log.md     ← Détection manuelle
├── session-state.md
├── memories.json            ← Backend JSON (fallback Qdrant)
└── activity.jsonl
```

### Débat 🧠 Carson (Brainstorming Coach) vs 🏗️ Winston vs 🔬 Dr. Quinn (Problem Solver)

**Carson :** *"YES AND... la mémoire actuelle est un bon START! Mais elle est PASSIVE. L'agent charge ses learnings et les LIT. Il ne les UTILISE pas activement pour modifier son comportement."*

**Dr. Quinn :** *"AHA! Le vrai problème est la BOUCLE DE FEEDBACK. Un agent fait une erreur → ça va dans failure-museum.md → mais l'agent ne RE-LIT JAMAIS ce fichier automatiquement avant sa prochaine action similaire. C'est comme un étudiant qui note ses erreurs mais ne relit jamais ses notes avant l'examen."*

**Winston :** *"Architecturalement, il faut :"*

### 7.2 Architecture mémoire améliorée proposée

```
COUCHE 1 — Mémoire de travail (Working Memory)
  ├── Durée : session courante
  ├── Contenu : contexte conversation, fichiers chargés, décisions en cours
  ├── Taille : bornée par context-guard.py
  └── Implémentation : conversation-branch state.json

COUCHE 2 — Mémoire épisodique (Session Memory)  
  ├── Durée : cross-session, 30 jours
  ├── Contenu : learnings, décisions, patterns de succès/échec
  ├── Accès : retrieval sémantique (RAG) avant chaque réponse
  └── Implémentation : Qdrant + rag-retriever.py

COUCHE 3 — Mémoire sémantique (Long-term Knowledge)
  ├── Durée : permanente
  ├── Contenu : rules, DNA, shared-context consolidé
  ├── Accès : toujours chargé (P0 context-router)
  └── Implémentation : fichiers MD sous _memory/

COUCHE 4 — Mémoire procédurale (How-to Memory)
  ├── Durée : permanente
  ├── Contenu : patterns de résolution par type de problème
  ├── Accès : matching par type de tâche avant exécution
  └── Implémentation : ❌ N'EXISTE PAS — À CRÉER
```

> **[DÉCIDÉ]** Implémenter la Couche 4 "Mémoire procédurale" — un index de patterns par type de tâche (ex: "migration DB" → steps prouvés, outils, pièges connus)

### 7.3 Injection RAG automatique

Actuellement, le `rag-retriever.py` existe mais n'est PAS appelé automatiquement. L'agent doit explicitement demander.

> **[DÉCIDÉ]** Intégrer le RAG dans le flux agent-base : avant chaque réponse, injecter les 3-5 chunks les plus pertinents depuis Qdrant (si disponible). Le context-router gère le budget.

---

# PARTIE 8 — GESTION DES TÂCHES ET ANTI-HALLUCINATION

## 8.1 Architecture de gestion des tâches

### Débat 📋 John (PM) vs 🏃 Bob (SM) vs 💻 Amelia (Dev)

**John (PM) :** *"WHY est-ce que l'utilisateur parle directement à 11 agents ? C'est CONFUS. Il devrait y avoir UN SEUL point d'entrée — un 'Concierge' qui comprend le besoin, le reformule, et dispatch."*

**Bob (SM) :** *"Exactement. Le pattern devrait être :"*

```
USER → Concierge (comprend, reformule, clarifie)
         │
         ├── Simple ? → Exécute directement (quick-flow)  
         ├── Complexe ? → Crée un plan PM → Stories SM → Dispatch agents
         └── Ambigu ? → Pose des questions de clarification AVANT d'agir
```

**Amelia (Dev) :** *"Le Concierge c'est exactement le rôle du SM (Bob) dans le boomerang workflow. On l'a déjà ! Mais il faut le rendre AUTOMATIQUE."*

### 8.2 Système anti-hallucination

**🔬 Dr. Quinn (Problem Solver) :**

*"3 mécanismes complémentaires :"*

| Mécanisme | Comment | Quand |
|-----------|---------|-------|
| **Grounding check** | Chaque affirmation d'un agent est vérifiée contre les fichiers réels du projet (grep, file exists, test pass) | Post-output |
| **Confidence scoring** | L'agent doit exprimer son niveau de confiance (HIGH/MEDIUM/LOW) sur chaque décision. LOW → pas d'action sans validation humaine | Inline |
| **Contradiction detection** | Comparer l'output de l'agent avec shared-context.md et decisions-log.md. Si contradiction → flag automatique | Post-output |

> Le `reasoning-stream.py` capture déjà HYPOTHESIS, DOUBT, ASSUMPTION — mais ne BLOQUE pas l'agent. Il faudrait un **gate** : si confidence < 0.3 → demander confirmation.

### 8.3 Compréhension utilisateur — Pattern PM/Client

**📋 John (PM) :** *"Quand un humain contredit le workflow, l'agent devrait se comporter comme un PM face à un client :"*

1. **Écouter** — Ne pas interrompre, capturer le VRAI besoin derrière les mots
2. **Reformuler** — "Si je comprends bien, vous voulez X pour obtenir Y, c'est correct ?"
3. **Clarifier les contradictions** — "Plus tôt, nous avions décidé A. Maintenant vous dites B. Voulez-vous : (a) changer la décision A, (b) trouver un compromis, (c) quelque chose d'autre ?"
4. **Confirmer le scope** — "Pour résumer, le périmètre est : [liste], hors périmètre : [liste]. On est alignés ?"

> **[DÉCIDÉ]** Ajouter au protocole agent-base une section "Contradiction Resolution Protocol" qui active ces 4 étapes quand l'user contredit une décision existante.

---

# PARTIE 9 — AGENTS VISUELS ET CRÉATIFS

## 9.1 Agents manquants identifiés

### 🎨 Sally (UX Designer) + ⚡ Victor (Innovation Strategist)

| Agent proposé | Domaine | Justification |
|--------------|---------|---------------|
| **Art Director** (DA) | Direction artistique, charte graphique, identité visuelle | Aucun agent ne gère la cohérence visuelle. Le UX Designer (Sally) fait de l'interaction design, pas de la DA. |
| **Visual Designer** | Création SVG, mockups, wireframes, composants visuels | Pourrait exploiter des MCP tools pour générer des assets |
| **Sound Designer** | Sound design, UX sonore, musique | Pour les projets jeux/multimédia |
| **3D Artist** | Assets 3D, scènes, prototypage spatial | Via MCP vers Blender/Godot |
| **Brand Strategist** | Naming, tone of voice, brand guidelines | Complémentaire à la DA pour une cohérence globale |

**Sally :** *"Mais attention — les agents LLM ne DESSINENT pas. Ils peuvent :"*
- Générer du **SVG inline** (formes simples, icônes, diagrammes)
- Écrire du **CSS/Tailwind** pour les systèmes de design
- Rédiger des **spécifications de design** (color tokens, typography scale, spacing)
- Créer des **prompts pour Midjourney/DALL-E/Stable Diffusion** structurés
- Générer du **code Three.js / Godot GDScript** pour les scènes 3D
- Écrire des **scripts audio** (Web Audio API, Tone.js, FMOD)

> **[DÉCIDÉ]** Créer 2 nouveaux agents : **Art Director** (DA) et **Creative Toolsmith** (génère le code des assets visuels/audio)

---

# PARTIE 10 — OUTILS EXTERNES ET MCP

## 10.1 MCP Tools à intégrer

### ⚡ Victor (Innovation Strategist) + 🏗️ Winston (Architecte)

| Outil MCP | Domaine | Ce que ça débloque |
|-----------|---------|-------------------|
| **Godot MCP** | Jeux/3D | Contrôler l'éditeur Godot depuis les agents (créer scènes, nodes, scripts GDScript) |
| **Blender MCP** | 3D | Modélisation, rigging, export via Python API Blender |
| **Figma MCP** | Design | Lire/écrire les designs Figma, extraire tokens, syncer composants |
| **Browser MCP** | Web research | Naviguer le web, scraper docs, veille techno |
| **Image Generation MCP** | Visuel | Appeler DALL-E/Stable Diffusion/Midjourney API |
| **Audio MCP** | Son | Synthèse audio, TTS, music generation (Suno API, Udio) |
| **Database MCP** | Data | Query PostgreSQL/MySQL depuis les agents |
| **Git MCP** | Versioning | Opérations git avancées (cherry-pick cross-branch, bisect) |
| **Docker MCP** | Containers | Build, run, inspect depuis les agents |
| **Playwright MCP** | Testing | E2E tests visuels, screenshots, assertions UI |

### Architecture d'intégration

```
Agent BMAD
    │
    ├── MCP Tool Call (via bmad-mcp-tools.py)
    │       │
    │       ├── bmad_route_request → llm-router.py
    │       ├── bmad_rag_search → rag-retriever.py
    │       ├── bmad_memory_push → memory-sync.py
    │       │
    │       └── [NEW] External MCP Proxy
    │               ├── godot_* → Godot MCP Server
    │               ├── figma_* → Figma MCP Server
    │               ├── browser_* → Playwright/Puppeteer MCP
    │               ├── image_* → Image Gen MCP
    │               └── audio_* → Audio MCP
    │
    └── IDE natif (file edit, terminal, search)
```

> **[DÉCIDÉ]** Créer un `mcp-proxy.py` qui route les appels vers des MCP servers externes. L'agent n'a pas besoin de savoir quel server gère quoi — le proxy résout.

---

# PARTIE 11 — ÉPICS COMPLETS

## EPIC 1 — Concierge Intelligence Layer

**Objectif :** Un point d'entrée unique qui comprend l'utilisateur, clarifie, et orchestre.

| Story | Description | Effort |
|-------|------------|--------|
| 1.1 | Créer l'agent "Concierge" avec capacité de triage (simple/complex/ambigu) | M |
| 1.2 | Implémenter le "Contradiction Resolution Protocol" dans agent-base | S |
| 1.3 | Auto-reformulation : le Concierge reformule et demande confirmation avant dispatch | S |
| 1.4 | Intégrer le Concierge comme default entrypoint dans copilot-instructions.md | S |
| 1.5 | Confidence gate : bloquer l'action si confidence < 0.3 | M |
| 1.6 | Self-critique post-output (grounding check + contradiction detection) | L |

## EPIC 2 — Mémoire Intelligente v2

**Objectif :** Les agents UTILISENT activement leur mémoire pour améliorer leurs réponses.

| Story | Description | Effort |
|-------|------------|--------|
| 2.1 | RAG auto-injection : injecter 3-5 chunks pertinents avant chaque réponse agent | M |
| 2.2 | Mémoire procédurale : index de patterns par type de tâche | L |
| 2.3 | Feedback loop mémoire : après chaque CC PASS/FAIL, enrichir automatiquement les learnings | S |
| 2.4 | Failure-museum auto-query : avant une tâche similaire, checker les échecs passés | M |
| 2.5 | Session lifecycle hooks (pre: health-check + lint, post: dream + save) | M |
| 2.6 | Compacter agent-base.md en version condensée (30 lignes core) | S |

## EPIC 3 — Sécurité et Fiabilité

**Objectif :** Durcir le framework contre les attaques et les erreurs silencieuses.

| Story | Description | Effort |
|-------|------------|--------|
| 3.1 | Sanitiser qdrant_url (SSRF protection) dans rag-indexer + rag-retriever | S |
| 3.2 | .gitignore hardening (qdrant_data, secrets, keys) | XS |
| 3.3 | Dry-run par défaut sur outils destructifs | S |
| 3.4 | Logging structuré dans les 82 except...pass | M |
| 3.5 | Checksum SHA256 des fichiers agents au boot | M |
| 3.6 | Fix encoding UTF-8 dans maintenance.py | XS |
| 3.7 | Rate limiting MCP tools | M |

## EPIC 4 — Agents Créatifs et Visuels

**Objectif :** Étendre le framework aux domaines visuels, audio et 3D.

| Story | Description | Effort |
|-------|------------|--------|
| 4.1 | Créer l'agent Art Director (DA) — persona, DNA, principes | M |
| 4.2 | Créer l'agent Creative Toolsmith — génération SVG/CSS/3D/audio code | M |
| 4.3 | MCP proxy pour servers externes (Godot, Figma, Browser) | L |
| 4.4 | Template de charte graphique (design tokens, typography, colors) | S |
| 4.5 | Intégration Image Generation MCP (DALL-E/SD via API) | M |
| 4.6 | Archétype "creative-studio" (DA + Creative Toolsmith + UX + Brand) | M |

## EPIC 5 — Orchestration Honnête

**Objectif :** Clarifier et améliorer le multi-agent sans prétendre ce qu'on ne fait pas.

| Story | Description | Effort |
|-------|------------|--------|
| 5.1 | Renommer modes orchestrator (simulated/concurrent-cpu/future-multi-llm) | S |
| 5.2 | Implémenter session-lifecycle.py (pre/post hooks) | M |
| 5.3 | Auto-branch sur [THINK] (conversation branching automatique) | M |
| 5.4 | Document "Architecture Decision: Why We Don't Multi-LLM" (ADR) | S |
| 5.5 | MCP batch tool optimization (grouper les appels tools indépendants) | M |
| 5.6 | Background daemon pour dream/stigmergy/indexing | L |

## EPIC 6 — Developer Experience

**Objectif :** Rendre le kit intuif et rapide à prendre en main.

| Story | Description | Effort |
|-------|------------|--------|
| 6.1 | CLI unifiée `grimoire <cmd>` | M |
| 6.2 | `grimoire doctor` — diagnostic complet en 1 commande | M |
| 6.3 | Progressive onboarding guide (J1 / S1 / M1) | M |
| 6.4 | Découper r-and-d.py en modules | L |
| 6.5 | Registre de dépendances inter-outils | M |
| 6.6 | Test intégration NSO chaîne complète + smoke tests CI | M |

---

# PARTIE 12 — DÉBATS TEAM vs TEAM : RÉSUMÉ DES DÉCISIONS

## Débat 1 : "Simulé vs Réel" — Team Build vs Team Vision

**Team Build (Winston, Amelia, Quinn) :** *"L'orchestration simulée (1 LLM = N personas) est notre FORCE, pas une faiblesse. C'est rapide, pas cher, et marche dans l'IDE."*

**Team Vision (Victor, Mary, John) :** *"Mais ça ne SCALE pas. Un client enterprise veut des agents RÉELS — parallèle, auditables, avec des logs séparés."*

**Résolution :** Les deux ont raison. Court terme = simulé (IDE). Moyen terme = MCP proxy vers agents API. Long terme = A2A protocol quand le standard mûrit.

## Débat 2 : "69 outils c'est trop" — PM vs Dev

**John (PM) :** *"69 outils, personne ne les utilise tous. Couper à 30 core + 39 optional."*

**Amelia (Dev) :** *"Chaque outil a ses tests. Les supprimer = perte de fonctionnalité. Mieux : les organiser en tiers (core / advanced / experimental)."*

**Résolution :** Organisation en tiers, pas suppression. `grimoire list --tier core|advanced|experimental`

## Débat 3 : "Mémoire compliquée" — Architecte vs QA

**Winston :** *"4 couches de mémoire c'est élégant architecturalement."*

**Quinn :** *"C'est aussi 4 sources de bugs et de désynchronisation. La couche procédurale va-t-elle vraiment être maintenue ?"*

**Résolution :** Commencer par automatiser la couche 2 (RAG injection). La couche 4 (procédurale) viendra quand on aura les données d'usage.

---

# RÉCAPITULATIF DES DÉCISIONS FERMES [DÉCIDÉ]

1. ✅ Refactorer agent-base.md en version condensée + complète
2. ✅ Taxonomie claire : Playbook (MD) vs Pipeline (Python) vs Orchestration (multi-LLM)
3. ✅ Renommer orchestrator mode "parallel" → "concurrent-cpu"
4. ✅ Créer session-lifecycle.py (pre/post hooks)
5. ✅ Implémenter self-critique post-output
6. ✅ MCP web search tool
7. ✅ Runtime quality scoring
8. ✅ SSRF protection sur qdrant_url
9. ✅ .gitignore hardening
10. ✅ Mémoire procédurale (couche 4)
11. ✅ RAG auto-injection
12. ✅ Contradiction Resolution Protocol dans agent-base
13. ✅ Agents Art Director + Creative Toolsmith
14. ✅ MCP proxy pour servers externes
15. ✅ CLI unifiée `grimoire <cmd>`
