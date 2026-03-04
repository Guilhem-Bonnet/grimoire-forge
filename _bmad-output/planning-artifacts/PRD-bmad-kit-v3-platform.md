# PRD — BMAD Kit v3 : De Framework à Plateforme

> **Statut** : Draft v1 — 3 mars 2026  
> **Auteur** : John (PM) + Victor (Innovation Strategist) + Winston (Architect)  
> **Version cible** : 3.0.0  
> **Précédent** : PRD-bmad-custom-kit-v2.md (100% livré)  
> **Nom de code** : **Catalyst**

---

## 1. Contexte et Diagnostic

### 1.1 Ce qu'on a construit (v2 — état des lieux)

| Métrique | Valeur |
|---|---|
| Lignes de code framework Python | ~34 000 |
| Lignes de tests Python | ~19 200 |
| Outils CLI Python (stdlib-only) | 48 |
| Lignes de Bash (`bmad-init.sh`) | 2 733 |
| Archétypes d'agents | 6 (minimal, web-app, infra-ops, fix-loop, stack, meta) |
| Agents spécialisés | 21 |
| Fichiers Markdown structurants | 74 |
| Innovations implémentées (6 vagues) | 63 |
| Smoke tests passing | 121/121 |

### 1.2 Le problème fondamental

**bmad-custom-kit v2 est un monorepo d'utilitaires, pas une plateforme.**

| Symptôme | Cause racine |
|---|---|
| `bmad-init.sh` fait 2 733 lignes | God-script monolithique — toute la logique dans un seul fichier Bash |
| Les 48 outils Python sont des scripts isolés | Chaque outil est `if __name__ == "__main__"` — aucun package importable |
| Le MCP server est un README vide | Il n'y a rien à exposer programmatiquement — pas de bibliothèque sous-jacente |
| Le registry communautaire est un concept | Pas d'infrastructure de distribution |
| Impossible d'installer "juste la mémoire" | Architecture monolithique : tout ou rien |
| Un agent IA ne peut pas utiliser BMAD comme SDK | Aucune API Python, uniquement des commandes shell à parser |
| Merge sur projet existant = risque élevé | Pas de moteur de merge non-destructif |

### 1.3 La vision v3

> **BMAD Kit v3 est une plateforme composable d'agents IA** : un package Python installable (`pip install bmad-kit`) avec un CLI moderne, un SDK importable, un serveur MCP natif, et un fichier déclaratif `bmad.yaml` — qui se greffe sur n'importe quel projet existant sans collision, ou bootstrap un projet neuf en une commande.

### 1.4 Positionnement stratégique

| Dimension | v2 (aujourd'hui) | v3 (cible) |
|---|---|---|
| **Nature** | Starter kit (clone + init) | Package installable + plateforme |
| **Architecture** | Monolithique | Micro-noyau + modules composables |
| **Configuration** | Manuelle (YAML édité à la main) | Déclarative (`bmad.yaml`) |
| **Cible projet** | Projet neuf uniquement | Projet neuf **ET** existant (merge) |
| **Distribution** | `git clone` + `bash bmad-init.sh` | `pip install bmad-kit` / `uvx bmad init` |
| **Granularité** | Tout ou rien | Cherry-pick de fonctionnalités |
| **Consommation IA** | Shell commands à parser | SDK Python importable + MCP natif |
| **Communauté** | Zéro | Registry d'agents et modules |
| **Dépendance framework mère** | `BMAD-METHOD` v6+ requis | Standalone (BMAD optionnel) |

---

## 2. Utilisateurs Cibles et Scénarios

### 2.1 Personas

#### Persona A — "Le Greffeur"
- **Profil** : Dev senior avec un projet existant (Express.js, Django, Spring Boot...)
- **Besoin** : Ajouter des agents IA *sans restructurer* son projet
- **Frustration actuelle** : `bmad-init.sh` suppose un projet vierge. Risque de collision.
- **Métrique de succès** : `bmad init` dans un projet de 500 fichiers en < 30 secondes, zéro conflit

#### Persona B — "Le Bootstrapper"
- **Profil** : Dev qui démarre un nouveau projet
- **Besoin** : Équipe d'agents IA complète dès le jour 1
- **Frustration actuelle** : Aucune. C'est le use case actuel bien servi.
- **Métrique de succès** : `bmad init --auto` détecte le stack et compose l'équipe optimale en < 10s

#### Persona C — "Le Cherry-Picker"
- **Profil** : Dev qui veut UNE fonctionnalité, pas tout le framework
- **Besoin** : Installer juste le Context Router, ou juste le système de mémoire
- **Frustration actuelle** : Tout est couplé. Impossible d'extraire un module seul.
- **Métrique de succès** : `bmad add module memory` installe seulement le système mémoire

#### Persona D — "L'Agent Builder"
- **Profil** : Power user qui crée ses propres agents
- **Besoin** : SDK pour créer, tester, publier des agents custom
- **Frustration actuelle** : Création manuelle de fichiers MD. Pas de validation. Pas de publication.
- **Métrique de succès** : `bmad forge "expert Kubernetes sécurité" && bmad test && bmad publish`

#### Persona E — "L'Agent IA exécutant"
- **Profil** : Un LLM (Claude, GPT-4o, Gemini) qui consomme BMAD pour travailler sur un projet
- **Besoin** : API programmatique, pas des parseurs de sortie CLI
- **Frustration actuelle** : Doit exécuter `python3 context-router.py --agent atlas | grep ...`
- **Métrique de succès** : `from bmad.tools import ContextRouter; plan = ContextRouter(root).plan("atlas")`

### 2.2 Scénarios concrets

#### Scénario 1 — Greffe sur projet Django existant
```bash
cd mon-projet-django/  # 200 fichiers, 3 ans d'historique
pip install bmad-kit
bmad init --auto
# → Détecte Python+Django+PostgreSQL
# → Crée _bmad/ avec agents adaptés
# → Génère bmad.yaml
# → Zéro fichier existant modifié
```

#### Scénario 2 — Cherry-pick du Context Router
```bash
pip install bmad-kit
bmad add module context-router
# → Installe uniquement context-router dans _bmad/tools/
# → Ajoute l'entrée dans bmad.yaml
# → Pas de mémoire, pas d'agents, pas de workflows
```

#### Scénario 3 — Agent IA consomme le SDK
```python
from bmad import BmadProject
from bmad.tools import ContextRouter, AgentForge

project = BmadProject(".")
router = ContextRouter(project)
plan = router.plan(agent="atlas", task="refactor auth module")

forge = AgentForge(project)
agent = forge.create(description="expert sécurité Django OWASP")
```

#### Scénario 4 — Merge depuis un template communautaire
```bash
bmad merge --from https://github.com/user/bmad-rust-agents
# → Télécharge le package
# → Analyse les conflits potentiels
# → Propose un plan de merge interactif
# → Fusionne de manière non-destructive
```

#### Scénario 5 — Déclaratif pur avec bmad.yaml
```yaml
# bmad.yaml — Committable, diffable, reproductible
version: "3.0"
project:
  name: "Mon API"
  stack: [python, fastapi, postgresql]

agents:
  - id: analyst
    persona: default
  - id: architect  
    persona: default
    modules: [context-router, harmony-check]
  - id: custom-security
    from: ./agents/security-expert.md

modules:
  memory:
    backend: local          # local | qdrant | ollama
  completion-contract:
    stacks: [python, docker]
  context-router:
    model: copilot
    threshold: 40

settings:
  language: Français
  skill_level: expert
  output_folder: _bmad-output
```

```bash
bmad up    # Instancie tout depuis bmad.yaml
bmad down  # Nettoie (optionnel)
```

---

## 3. Décisions Techniques Structurantes

### 3.1 Langage : Python (décision verrouillée)

**Rationale complète (issue du brainstorm adversarial multi-agent) :**

| Critère (pondéré) | Python | Rust | Go | TypeScript |
|---|---|---|---|---|
| 🤖 Aptitude agent-IA (30%) | **9/10** — Meilleur langage LLM : ~92% HumanEval, 2x plus de tickets SWE-Bench résolus vs Rust | 5/10 — 30-40% inférieur en benchmarks IA | 7/10 — Correct, inférieur à Python | 8/10 — Juste derrière Python |
| 📦 Écosystème CLI/packaging (20%) | **8/10** — `uv` révolutionne : `uvx bmad` sans install, embarque Python si absent | 9/10 — Single binary | 9/10 — Single binary, cobra | 7/10 — npm/deno fragmentation |
| 🔗 Interop existant (15%) | **10/10** — 34K lignes + 19K tests. Coût migration = 0 | 1/10 — Réécriture totale | 1/10 — Réécriture totale | 2/10 — Réécriture |
| ⚡ Perf runtime (10%) | **7/10** — ~200ms cold start avec `uv tool`. Acceptable pour CLI interactif | 10/10 — 5ms | 9/10 — 15ms | 6/10 — Variable |
| 🧩 Expressivité fichiers/YAML/MD (15%) | **9/10** — pathlib, ruamel.yaml, Jinja2. Le plus expressif pour manipuler des arborescences | 6/10 — borrow checker inutile ici | 7/10 — Correct mais verbeux | 8/10 — Bon en JSON/YAML |
| 🌍 Portabilité (10%) | **8/10** — `uv` embarque Python si nécessaire. Pas besoin d'installation préalable | 10/10 — Zero dep | 10/10 — Zero dep | 5/10 — Node requis |
| **Score pondéré** | **8.5/10** | **5.3/10** | **5.8/10** | **6.2/10** |

**Argument décisif** : Les agents IA performants (Claude, GPT-4o, Gemini) produisent un code Python avec 27 points de score en plus vs Rust sur HumanEval. Quand la force d'exécution est l'IA, optimiser pour le langage que l'IA maîtrise le mieux est la décision rationnelle.

**Outils de l'écosystème Python retenus :**

| Outil | Rôle | Justification |
|---|---|---|
| `uv` (Astral) | Package manager + runtime | `uvx bmad init` = installation+exécution en une commande. Embarque Python si absent. Build < 500ms. |
| `typer` | Framework CLI | Type hints natifs → agents IA génèrent du code CLI plus correct. Auto-completion shell. Construit sur click. |
| `rich` | Output terminal formaté | Tables, spinners, couleurs, Markdown dans le terminal. UX professionnelle. |
| `ruamel.yaml` | Parsing YAML | Préserve les commentaires lors de l'édition — critique pour `bmad.yaml` qui sera édité par l'utilisateur ET par les agents. |
| `mcp` (Anthropic SDK) | Serveur MCP | SDK officiel. Interop native avec Claude Desktop, Cursor, VS Code Copilot. |
| `ruff` | Linting + formatting | Déjà configuré (ruff.toml existe). Industriel. |
| `mypy` | Typage statique | `--strict` — les agents génèrent du code plus correct sur les codebases typées. |
| `pytest` | Tests | Déjà utilisé (19K lignes de tests existants). |

### 3.2 Architecture cible : Micro-noyau + Interfaces multiples

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERFACES                                │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │   CLI    │  │  MCP     │  │  Python  │  │  bmad.yaml     │  │
│  │ (typer)  │  │  Server  │  │  SDK     │  │  (déclaratif)  │  │
│  │          │  │ (mcp)    │  │  import  │  │                │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───────┬────────┘  │
│       │             │             │                  │           │
│  ┌────▼─────────────▼─────────────▼──────────────────▼────────┐  │
│  │                   bmad-core (package Python)                │  │
│  │                                                             │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │  │
│  │  │ Project  │ │  Agent   │ │ Workflow │ │    Config    │  │  │
│  │  │ Engine   │ │  Engine  │ │  Engine  │ │   Manager    │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │  │
│  │                                                             │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │  │
│  │  │  Memory  │ │  Merge   │ │  Forge   │ │   Registry   │  │  │
│  │  │  System  │ │  Engine  │ │  Engine  │ │   Client     │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │  │
│  │                                                             │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │              Tools (48 outils refactorés)            │  │  │
│  │  │  context_router │ agent_bench │ harmony_check │ ...  │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    Filesystem Layer                          │  │
│  │   bmad.yaml │ _bmad/ │ agents/*.md │ memory/ │ workflows/  │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

### 3.3 Contraintes architecturales pour code écrit par agents IA

Puisque les agents performants sont la force d'exécution principale, le code doit être optimisé pour leur productivité :

| Contrainte | Règle | Justification |
|---|---|---|
| **Taille fichiers** | Max 300 lignes par fichier | Les LLMs performent mieux sur des fichiers courts. Au-delà, le taux d'erreur augmente. |
| **Docstrings** | Obligatoires sur chaque fonction/classe publique | L'agent a besoin de contexte inline pour comprendre l'intention sans lire tout le fichier. |
| **Typage** | `mypy --strict` 100% passant | Les agents génèrent du code significativement plus correct quand le codebase est typé. |
| **Imports** | Explicites, jamais de `*` | Les agents se perdent avec les imports implicites et la métaprogrammation. |
| **Tests** | `test_<module>.py` pour chaque `<module>.py` dans `tests/` | Pattern évident = l'agent sait immédiatement où trouver/créer les tests. |
| **Métaprogrammation** | Minimale. Pas de metaclasses, decorators complexes limités | Les LLMs se perdent dans la magie Python. Keep it boring. |
| **Nommage** | snake_case strict, noms descriptifs, pas d'abbréviations | Réduit l'ambiguïté pour le LLM. |
| **Erreurs** | Exceptions typées avec messages descriptifs | L'agent doit comprendre l'erreur pour la corriger. |

### 3.4 Structure du package cible

```
bmad-kit/                            ← Racine du package PyPI
├── pyproject.toml                   ← Définition du package
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ruff.toml
├── bmad.yaml.tpl                    ← Template du fichier déclaratif
│
├── src/                             ← Source layout (PEP 621 recommandé)
│   └── bmad/                        ← Le package importable
│       ├── __init__.py              ← from bmad import BmadProject, Agent, Workflow
│       ├── __version__.py           ← Version unique (SSoT)
│       ├── py.typed                 ← Marker PEP 561 pour mypy
│       │
│       ├── core/                    ← Le noyau — logique métier pure
│       │   ├── __init__.py
│       │   ├── project.py           ← BmadProject — point d'entrée principal
│       │   ├── config.py            ← BmadConfig — chargement et validation bmad.yaml
│       │   ├── agent.py             ← AgentLoader — chargement, merge, instanciation
│       │   ├── workflow.py          ← WorkflowEngine — exécution de workflows YAML/MD
│       │   ├── merge.py             ← MergeEngine — fusion non-destructive sur projet existant
│       │   ├── scanner.py           ← StackScanner — détection automatique du stack
│       │   ├── archetype.py         ← ArchetypeManager — gestion des templates d'équipe
│       │   └── exceptions.py        ← Exceptions typées (BmadConfigError, MergeConflict, etc.)
│       │
│       ├── cli/                     ← Interface CLI (thin wrapper sur core/)
│       │   ├── __init__.py
│       │   ├── app.py               ← Typer app principal : bmad [commande]
│       │   ├── cmd_init.py          ← bmad init [--auto] [--archetype TYPE]
│       │   ├── cmd_add.py           ← bmad add [agent|module|archetype] NAME
│       │   ├── cmd_remove.py        ← bmad remove [agent|module] NAME
│       │   ├── cmd_up.py            ← bmad up — instancie depuis bmad.yaml
│       │   ├── cmd_merge.py         ← bmad merge --from URL
│       │   ├── cmd_forge.py         ← bmad forge "description" | --from-gap | --from-trace
│       │   ├── cmd_bench.py         ← bmad bench [--report] [--improve]
│       │   ├── cmd_guard.py         ← bmad guard [--agent NAME] [--suggest]
│       │   ├── cmd_doctor.py        ← bmad doctor [--fix]
│       │   ├── cmd_status.py        ← bmad status — dashboard unifié
│       │   ├── cmd_eject.py         ← bmad eject — supprime le runtime, garde les fichiers statiques
│       │   ├── cmd_session.py       ← bmad session [branch|list|diff|merge]
│       │   ├── cmd_dream.py         ← bmad dream — consolidation hors-session
│       │   ├── cmd_evolve.py        ← bmad evolve — évolution DNA
│       │   ├── cmd_trace.py         ← bmad trace — gestion BMAD_TRACE
│       │   ├── cmd_hooks.py         ← bmad hooks [--install|--list]
│       │   ├── cmd_validate.py      ← bmad validate [--dna|--all]
│       │   ├── cmd_changelog.py     ← bmad changelog
│       │   ├── cmd_consensus.py     ← bmad consensus [--proposal|--history]
│       │   ├── cmd_antifragile.py   ← bmad antifragile [--detail|--trend]
│       │   ├── cmd_reasoning.py     ← bmad reasoning [log|query|analyze]
│       │   ├── cmd_migrate.py       ← bmad migrate [export|import|inspect|diff]
│       │   ├── cmd_darwinism.py     ← bmad darwinism [evaluate|leaderboard|evolve]
│       │   ├── cmd_stigmergy.py     ← bmad stigmergy [emit|sense|amplify|landscape]
│       │   └── cmd_registry.py      ← bmad registry [search|install|publish]
│       │
│       ├── tools/                   ← Les 48 outils refactorés en modules importables
│       │   ├── __init__.py          ← from bmad.tools import ContextRouter, AgentForge, ...
│       │   ├── context_router.py
│       │   ├── agent_forge.py
│       │   ├── agent_bench.py
│       │   ├── antifragile_score.py
│       │   ├── harmony_check.py
│       │   ├── ...                  ← (48 modules)
│       │   └── _common.py           ← Utilitaires partagés entre outils
│       │
│       ├── memory/                  ← Système mémoire avec backends pluggables
│       │   ├── __init__.py
│       │   ├── manager.py           ← MemoryManager — API unifiée
│       │   ├── maintenance.py       ← Consolidation, cleanup
│       │   ├── session.py           ← Session save/restore
│       │   └── backends/
│       │       ├── __init__.py
│       │       ├── base.py          ← MemoryBackend — ABC
│       │       ├── local.py         ← Backend JSON fichier
│       │       ├── qdrant.py        ← Backend Qdrant (local + server)
│       │       └── ollama.py        ← Backend Ollama embeddings
│       │
│       ├── mcp/                     ← Serveur MCP natif
│       │   ├── __init__.py
│       │   └── server.py            ← Expose core/ et tools/ via MCP protocol
│       │
│       └── registry/                ← Client pour le registry d'agents/modules
│           ├── __init__.py
│           ├── client.py            ← RegistryClient — search, install, publish
│           ├── local.py             ← LocalRegistry — archetypes built-in
│           └── remote.py            ← RemoteRegistry — PyPI / GitHub Packages
│
├── archetypes/                      ← Templates d'équipes (inclus dans le package)
│   ├── minimal/
│   ├── web-app/
│   ├── infra-ops/
│   ├── fix-loop/
│   ├── stack/
│   ├── meta/
│   └── features/
│
├── templates/                       ← Templates de fichiers générés
│   ├── bmad.yaml.tpl
│   ├── agent.md.tpl
│   ├── workflow.yaml.tpl
│   └── project-context.yaml.tpl
│
├── docs/
│
└── tests/                           ← Tests (pytest)
    ├── conftest.py                  ← Fixtures partagées
    ├── unit/                        ← Tests unitaires (rapides, isolés)
    │   ├── core/
    │   │   ├── test_project.py
    │   │   ├── test_config.py
    │   │   ├── test_agent.py
    │   │   ├── test_merge.py
    │   │   ├── test_scanner.py
    │   │   └── ...
    │   ├── tools/
    │   │   ├── test_context_router.py
    │   │   ├── test_agent_forge.py
    │   │   └── ...
    │   ├── memory/
    │   └── cli/
    ├── integration/                 ← Tests d'intégration (plus lents)
    │   ├── test_init_workflow.py
    │   ├── test_merge_existing.py
    │   ├── test_bmad_yaml_lifecycle.py
    │   └── test_mcp_server.py
    └── fixtures/                    ← Projets factices pour les tests
        ├── empty-project/
        ├── django-project/
        ├── express-project/
        └── terraform-project/
```

### 3.5 Le fichier `bmad.yaml` — Spécification complète

`bmad.yaml` est **la source unique de vérité** pour la configuration BMAD d'un projet. Il remplace `project-context.tpl.yaml` et unifie toute la configuration dispersée.

```yaml
# bmad.yaml — Source unique de vérité du projet
# Généré par `bmad init`, éditable manuellement, versionné dans git.
# Documentation : https://bmad-kit.readthedocs.io/bmad-yaml

# ── Méta ──────────────────────────────────────────────────────────
version: "3.0"                        # Version du schéma bmad.yaml

# ── Projet ────────────────────────────────────────────────────────
project:
  name: "Mon API Backend"
  description: "API REST pour la gestion de commandes"
  type: api                           # api | webapp | infrastructure | mobile | data-pipeline | game
  metaphor: "forteresse"              # Métaphore structurante (optionnel)
  stack:                              # Détecté automatiquement par `bmad init --auto`
    - python
    - fastapi
    - postgresql
    - docker
  repos:
    - name: main
      path: "."
      default_branch: main

# ── Utilisateur ───────────────────────────────────────────────────
user:
  name: "Guilhem"
  language: "Français"
  document_language: "Français"
  skill_level: expert                 # beginner | intermediate | expert

# ── Agents ────────────────────────────────────────────────────────
agents:
  # Agent built-in (from archétype)
  - id: analyst
    source: builtin                   # builtin | local | registry
    persona: default                  # default = persona d'origine

  # Agent built-in avec surcharge de persona
  - id: architect
    source: builtin
    persona:
      name: "Winston-Custom"
      communication_style: "Ultra-concis, en Français seulement"
      additional_principles:
        - "Toujours proposer 2 alternatives"
    modules:                          # Modules attachés à cet agent
      - context-router
      - harmony-check

  # Agent custom local (fichier .md dans le projet)
  - id: security-expert
    source: local
    path: ./agents/security-expert.md

  # Agent depuis le registry communautaire (v3.1+)
  # - id: rust-expert
  #   source: registry
  #   package: "@community/rust-expert"
  #   version: "^1.2.0"

# ── Modules ───────────────────────────────────────────────────────
modules:
  memory:
    enabled: true
    backend: local                    # local | qdrant-local | qdrant-server | ollama
    # qdrant_url: "http://localhost:6333"  # si qdrant-server
    consolidation: auto               # auto | manual
    retention_days: 90

  completion-contract:
    enabled: true
    stacks:                           # Auto-détecté si omis
      - python
      - docker
    strict: true                      # false = warning seulement

  context-router:
    enabled: true
    model: copilot                    # Modèle LLM cible pour le calcul de budget
    warning_threshold: 60             # % budget → warning
    critical_threshold: 80            # % budget → suggestions agressives

  stigmergy:
    enabled: false                    # Désactivé par défaut
    evaporation_hours: 72

  dream-mode:
    enabled: false
    schedule: manual                  # manual | daily | weekly

# ── Workflows ─────────────────────────────────────────────────────
workflows:
  default: standard                    # standard | quick-flow | fix-loop
  completion_contract: required        # required | optional | disabled
  session_branching: true

# ── Paths ─────────────────────────────────────────────────────────
paths:
  bmad_dir: _bmad                     # Répertoire BMAD
  output_dir: _bmad-output            # Artefacts de sortie
  agents_dir: _bmad/agents            # Agents déployés
  memory_dir: _bmad/memory            # Mémoire persistante
  custom_agents_dir: ./agents         # Agents custom locaux

# ── Hooks ─────────────────────────────────────────────────────────
hooks:
  pre_commit:
    - completion-contract             # Vérifie le CC avant commit
  post_commit:
    - trace-log                       # Log dans BMAD_TRACE
  pre_push:
    - memory-consolidation            # Consolide la mémoire avant push

# ── Settings avancés ──────────────────────────────────────────────
settings:
  telemetry: false                    # Jamais de télémétrie par défaut
  auto_update_check: true             # Vérifie les nouvelles versions
  max_agent_context_tokens: 200000    # Budget max par agent
  trace_enabled: true
  immune_system: true                 # Auto-détection d'anomalies
```

### 3.6 Le `pyproject.toml` cible

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "bmad-kit"
dynamic = ["version"]
description = "Composable AI agent platform — plug-and-play teams for any project"
readme = "README.md"
license = "MIT"
requires-python = ">=3.12"
authors = [{ name = "Guilhem Bonnet" }]
keywords = ["ai", "agents", "llm", "mcp", "workflow", "copilot"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Quality Assurance",
]

dependencies = [
    "typer>=0.12,<1.0",
    "rich>=13.0,<15.0",
    "ruamel.yaml>=0.18,<1.0",
]

[project.optional-dependencies]
mcp = ["mcp>=1.0,<2.0"]              # Serveur MCP (optionnel)
qdrant = ["qdrant-client>=1.7,<2.0"]  # Backend mémoire Qdrant
ollama = ["ollama>=0.3,<1.0"]         # Embeddings Ollama
all = ["bmad-kit[mcp,qdrant,ollama]"]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "mypy>=1.10",
    "ruff>=0.5",
]

[project.scripts]
bmad = "bmad.cli.app:main"

[project.urls]
Homepage = "https://github.com/Guilhem-Bonnet/bmad-custom-kit"
Documentation = "https://bmad-kit.readthedocs.io"
Repository = "https://github.com/Guilhem-Bonnet/bmad-custom-kit"
Issues = "https://github.com/Guilhem-Bonnet/bmad-custom-kit/issues"

[tool.hatch.version]
path = "src/bmad/__version__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/bmad"]

[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "N", "ANN", "S", "T20", "SIM"]
ignore = ["ANN101", "ANN102", "S101"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q --strict-markers"
markers = [
    "slow: marks tests as slow (deselect with '-m not slow')",
    "integration: marks integration tests",
]
```

---

## 4. Stratégie de Migration v2 → v3

### 4.1 Principe directeur : Refactoring, pas réécriture

Le code existant (34K lignes Python + 19K tests) est **préservé et restructuré**, jamais jeté. La migration est incrémentale : chaque étape produit un système fonctionnel.

### 4.2 Plan de migration en 4 phases

```
Phase 0 ─── Phase 1 ─── Phase 2 ─── Phase 3
Scaffold     Extract     Interface    Platform
(structure)  (core lib)  (CLI+MCP)    (registry)
```

**Phase 0 — Scaffold** : Créer la structure du package Python (`src/bmad/`, `pyproject.toml`, `tests/`). Les 48 scripts continuent de fonctionner tels quels.

**Phase 1 — Extract** : Extraire la logique de chaque script vers des classes importables dans `bmad.core/` et `bmad.tools/`. Chaque outil garde sa CLI `if __name__` comme wrapper temporaire. Les tests existants continuent de passer.

**Phase 2 — Interface** : Construire le CLI Typer et le serveur MCP comme thin wrappers sur `bmad.core`. Migrer `bmad-init.sh` vers `bmad.cli.cmd_init`. Le fichier `bmad.yaml` devient opérationnel.

**Phase 3 — Platform** : Registry, merge engine, `bmad eject`, distribution PyPI.

### 4.3 Garantie de non-régression

- Les 19 200 lignes de tests existants sont migrées en premier
- Chaque phase se termine par : `pytest --tb=short && ruff check && mypy --strict`
- CI GitHub exécute la suite complète à chaque PR
- Le `bmad-init.sh` reste fonctionnel jusqu'à ce que le CLI Python le remplace complètement

---

## 5. Fonctionnalités Nouvelles v3

### 5.1 Merge Engine non-destructif

Le cœur du "plug-and-play". Permet d'ajouter BMAD à un projet existant sans toucher aux fichiers existants.

**Algorithme :**
1. Scanner l'arborescence cible
2. Identifier les conflits potentiels (`.github/`, `_bmad/` existant, hooks git)
3. Générer un plan de merge avec résolution de conflit
4. Exécuter le merge avec rollback automatique en cas d'erreur
5. Valider l'intégrité post-merge

**Garanties :**
- Aucun fichier existant n'est modifié sans confirmation explicite
- Un fichier `.bmad-merge-log.json` trace toutes les opérations
- `bmad merge --undo` annule le dernier merge

### 5.2 `bmad eject`

À la manière de Create React App `eject` : transforme l'installation BMAD en fichiers statiques sans dépendance au runtime.

```bash
bmad eject
# → Copie tous les agents, configs, templates en fichiers statiques
# → Supprime la dépendance à bmad-kit
# → Les fichiers sont autonomes et éditables à 100%
# → Irréversible (mais avec confirmation)
```

**Valeur** : Réduit la peur d'adoption. L'utilisateur sait qu'il peut toujours "quitter" le framework.

### 5.3 Serveur MCP natif

Expose toute l'API `bmad.core` via le protocole MCP :

| Tool MCP | Méthode core | Description |
|---|---|---|
| `bmad_project_context` | `BmadProject.context()` | Contexte complet du projet |
| `bmad_agent_list` | `BmadProject.agents()` | Liste des agents déployés |
| `bmad_agent_memory` | `MemoryManager.recall()` | Mémoire d'un agent |
| `bmad_context_plan` | `ContextRouter.plan()` | Plan de chargement contexte |
| `bmad_forge_create` | `AgentForge.create()` | Créer un agent from description |
| `bmad_bench_report` | `AgentBench.report()` | Rapport de benchmark |
| `bmad_guard_budget` | `ContextGuard.budget()` | Budget de contexte |
| `bmad_status` | `BmadProject.status()` | Dashboard complet |
| `bmad_merge_plan` | `MergeEngine.plan()` | Plan de merge non-destructif |
| `bmad_stigmergy_sense` | `Stigmergy.sense()` | Phéromones actives |

Compatible avec : Claude Desktop, Cursor, VS Code Copilot, Cline, Windsurf.

### 5.4 SDK Python pour agents IA

```python
# Usage par un agent IA dans un pipeline
from bmad import BmadProject
from bmad.tools import ContextRouter, AgentForge, HarmonyCheck

# Initialiser un projet
project = BmadProject("/path/to/project")

# Obtenir le plan de contexte pour un agent
router = ContextRouter(project)
plan = router.plan(agent="architect", task="refactor auth")
# → Retourne un objet structuré, pas du texte à parser

# Créer un agent à la volée
forge = AgentForge(project)
agent = forge.create(
    description="Expert sécurité Django OWASP",
    stack=["python", "django"],
)
# → Retourne un AgentSpec avec fichier .md généré

# Vérifier l'harmonie architecturale
harmony = HarmonyCheck(project)
report = harmony.scan()
print(report.score)         # 78/100
print(report.dissonances)   # Liste typée de Dissonance objects
```

### 5.5 Registry communautaire (v3.1+)

```bash
# Chercher un agent dans le registry
bmad registry search "kubernetes security"

# Installer un agent communautaire
bmad registry install @guilhem/k8s-security-expert

# Publier un agent custom
bmad registry publish ./agents/my-custom-agent.md
```

**Infrastructure prévue :** PyPI pour la distribution (chaque agent = un micro-package `bmad-agent-*`), GitHub Packages comme alternative.

---

## 6. Contraintes Non-Négociables

| # | Contrainte | Rationale |
|---|---|---|
| C1 | **Zero cloud requis** | Tout fonctionne hors-ligne. Les features réseau (registry) sont optionnelles. |
| C2 | **Python 3.12+** | Version minimale pour les features de typage utilisées (`type`, `TypeAlias`). |
| C3 | **Dépendances minimales** | 3 deps core (`typer`, `rich`, `ruamel.yaml`). Le reste est optionnel. |
| C4 | **Non-destructif** | `bmad init` et `bmad merge` ne modifient JAMAIS un fichier existant sans confirmation explicite. |
| C5 | **Rétrocompatible** | Les projets v2 fonctionnent après migration via `bmad upgrade`. |
| C6 | **Éjectable** | `bmad eject` produit des fichiers statiques autonomes. Pas de vendor lock-in. |
| C7 | **mypy --strict** | 100% du code typé. Pas de `Any` non justifié. |
| C8 | **Tests > 80% coverage** | Chaque module a ses tests unitaires. Coverage mesuré en CI. |
| C9 | **Fichiers < 300 lignes** | Optimisé pour la productivité des agents IA. |
| C10 | **stdlib-only pour tools critiques** | Les 48 outils dans `bmad.tools` restent sans dépendance externe (sauf `ruamel.yaml`). |

---

## 7. Métriques de Succès v3

| Métrique | v2 (actuel) | v3 (cible) |
|---|---|---|
| Temps d'installation | `git clone` + `bash` (~2 min) | `pip install bmad-kit` (~10s) |
| Temps init sur projet existant | Non supporté | < 30s, zéro conflit |
| Nombre d'interfaces consommation | 1 (CLI shell) | 4 (CLI, SDK, MCP, déclaratif) |
| Modules installables séparément | 0 | ≥ 5 (memory, CC, router, stigmergy, dream) |
| Tests Python passants | ~19 200 lignes | ~30 000 lignes (+55%) |
| Coverage | Non mesuré | ≥ 80% |
| mypy --strict | Non | 100% passant |
| Cold start CLI | N/A (Bash) | < 300ms |
| Agents communautaires disponibles | 0 | ≥ 10 (v3.1) |
| Projets utilisant BMAD Kit | 2 (Guilhem) | ≥ 20 (6 mois post-release) |

---

## 8. Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Le refactoring casse les tests existants | Moyenne | Haute | Migration test-par-test avec CI à chaque commit |
| `uv` change d'API ou de comportement | Faible | Moyenne | Dépendance à pip standard. `uv` est recommandé, pas requis. |
| La communauté ne contribue pas d'agents | Haute | Basse | Le produit est autonome. Le registry est un bonus, pas le cœur. |
| Le merge non-destructif ne couvre pas tous les edge cases | Haute | Haute | Mode dry-run par défaut. Rollback automatique. Tests sur 10+ structures de projet. |
| Scope creep sur le registry/marketplace | Haute | Haute | Lot 3 séparé. Ne pas commencer avant Lot 1 et 2 validés. |
| Python 3.12 minimum exclut des utilisateurs | Faible | Basse | Python 3.12 est sorti en oct 2023. En mars 2026, c'est mainstream. |

---

## 9. Ce qui est HORS SCOPE v3.0

- **UI Web** : pas de dashboard web. Tout reste terminal + IDE.
- **SaaS/Cloud** : pas de service hébergé. BMAD Kit est 100% local.
- **Agents autonomes long-running** : BMAD Kit configure des agents IDE, pas des daemons.
- **Support de langages autres que Python pour le framework** : le runtime est Python. Les agents supportent tous les langages de projet.
- **Monétisation** : pas de freemium, pas de premium, pas de telemetry. Open source pur.

---

## 10. Décision d'approbation

> **Ce PRD transforme bmad-custom-kit d'un starter kit monolithique en une plateforme composable installable via pip, avec 4 interfaces de consommation (CLI, SDK, MCP, déclaratif), un merge non-destructif sur projets existants, et une architecture optimisée pour les agents IA exécutants.**

**Prochaine étape** : Validation du PRD → Création des épics détaillées → Sprint planning.

---

*Document rédigé le 3 mars 2026 — Session brainstorm adversarial multi-agent*
