# ÉPICS — BMAD Kit v3 : De Framework à Plateforme

> **Référence PRD** : PRD-bmad-kit-v3-platform.md  
> **Date** : 3 mars 2026  
> **Auteur** : Bob (SM) + Amelia (Dev) + Winston (Architect)  
> **Convention** : Chaque épic = un lot livrable indépendamment. Chaque story = un incrément testable.
> **Estimation** : T-shirt sizing (XS < 0.5j, S = 0.5-1j, M = 1-2j, L = 3-5j, XL = 5-8j)
> **ID Convention** : `V3-EP{epic}-S{story}` (ex: V3-EP01-S03 = Epic 1, Story 3)

---

## Vue d'ensemble des Épics

```
Phase 0 — SCAFFOLD          Phase 1 — EXTRACT           Phase 2 — INTERFACE         Phase 3 — PLATFORM
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│ EP01 Package     │───────▶│ EP04 Core Lib    │───────▶│ EP07 CLI Typer   │───────▶│ EP10 Registry    │
│ EP02 Config      │        │ EP05 Tools       │        │ EP08 MCP Server  │        │ EP11 Marketplace │
│ EP03 Tests Infra │        │ EP06 Memory      │        │ EP09 bmad.yaml   │        │ EP12 Eject       │
└──────────────────┘        └──────────────────┘        └──────────────────┘        └──────────────────┘
                                                                │
                                                        ┌───────▼──────────┐
                                                        │ EP13 Merge Engine│
                                                        │ EP14 Migration   │
                                                        │ EP15 CI/CD + Doc │
                                                        └──────────────────┘
```

**Dépendances critiques :**
- EP04 dépend de EP01 (structure package)
- EP05 dépend de EP04 (core lib disponible)
- EP07 dépend de EP04 (CLI wrape core)
- EP08 dépend de EP04 (MCP wrape core)
- EP09 dépend de EP02 (config système)
- EP10 dépend de EP07 (CLI commands registry)
- EP13 dépend de EP04 + EP09 (merge nécessite core + config)

**Épics parallélisables :**
- EP01 + EP02 + EP03 (scaffold — pas de dépendance entre eux)
- EP05 + EP06 (extract — indépendants si EP04 fait)
- EP07 + EP08 (interfaces — même source, sorties différentes)
- EP10 + EP11 + EP12 (platform — indépendants)

---

## Phase 0 — SCAFFOLD

### EP01 — Création du Package Python

> **Objectif** : Créer la structure de package Python installable avec `pyproject.toml`, layout `src/`, et packaging `hatch`.
> **Valeur** : Sans cette structure, rien n'est importable ni distribuable.
> **Risque principal** : Mauvais layout initial → refactoring douloureux plus tard.
> **Critère de Done épic** : `pip install -e .` fonctionne, `python -c "import bmad"` réussit, `bmad --version` affiche la version.

#### V3-EP01-S01 — Créer pyproject.toml et structure src/ [M]

**Description** : Créer le `pyproject.toml` complet avec les métadonnées du package, les dépendances core et optionnelles, les scripts d'entrée, et la configuration des outils (ruff, mypy, pytest). Créer le layout `src/bmad/` avec les sous-packages vides (`core/`, `cli/`, `tools/`, `memory/`, `mcp/`, `registry/`).

**Tâches :**
- [ ] Créer `pyproject.toml` avec section `[project]` (name, version, description, dependencies)
- [ ] Configurer `[project.optional-dependencies]` : mcp, qdrant, ollama, all, dev
- [ ] Configurer `[project.scripts]` : `bmad = "bmad.cli.app:main"`
- [ ] Configurer `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`
- [ ] Créer `src/bmad/__init__.py` avec exports publics
- [ ] Créer `src/bmad/__version__.py` avec `__version__ = "3.0.0-alpha.1"`
- [ ] Créer `src/bmad/py.typed` (marker PEP 561)
- [ ] Créer tous les `__init__.py` des sous-packages (core, cli, tools, memory, mcp, registry)
- [ ] Vérifier `pip install -e .` dans un venv propre
- [ ] Vérifier `python -c "from bmad import __version__; print(__version__)"`

**Critères d'acceptation :**
- [ ] `pip install -e ".[dev]"` réussit sans erreur
- [ ] `python -c "import bmad"` réussit
- [ ] `ruff check src/` passe
- [ ] `mypy --strict src/bmad/__init__.py` passe
- [ ] La structure de dossiers correspond exactement au PRD section 3.4

**Fichiers créés/modifiés :**
- `pyproject.toml` (nouveau)
- `src/bmad/__init__.py` (nouveau)
- `src/bmad/__version__.py` (nouveau)
- `src/bmad/py.typed` (nouveau)
- `src/bmad/core/__init__.py` (nouveau)
- `src/bmad/cli/__init__.py` (nouveau)
- `src/bmad/tools/__init__.py` (nouveau)
- `src/bmad/memory/__init__.py` (nouveau)
- `src/bmad/mcp/__init__.py` (nouveau)
- `src/bmad/registry/__init__.py` (nouveau)

---

#### V3-EP01-S02 — Créer le module d'exceptions typées [S]

**Description** : Créer `src/bmad/core/exceptions.py` avec une hiérarchie d'exceptions typées couvrant tous les cas d'erreur prévisibles. Chaque exception porte un message descriptif pour faciliter le diagnostic par les agents IA.

**Tâches :**
- [ ] Créer `BmadError` (base exception)
- [ ] Créer `BmadConfigError` (erreur de configuration bmad.yaml)
- [ ] Créer `BmadProjectError` (projet non initialisé, structure invalide)
- [ ] Créer `BmadAgentError` (agent introuvable, persona invalide)
- [ ] Créer `BmadMergeConflict` (conflit de merge non-résolu)
- [ ] Créer `BmadMergeError` (erreur de merge générale)
- [ ] Créer `BmadRegistryError` (erreur registry — network, auth, package not found)
- [ ] Créer `BmadToolError` (erreur d'exécution d'un outil)
- [ ] Créer `BmadMemoryError` (erreur backend mémoire)
- [ ] Créer `BmadValidationError` (validation schema échouée)
- [ ] Docstrings exhaustives avec exemples de quand chaque exception est levée
- [ ] Tests unitaires pour chaque exception (instantiation, message, héritage)

**Critères d'acceptation :**
- [ ] Toutes les exceptions héritent de `BmadError`
- [ ] Chaque exception a un docstring avec un exemple
- [ ] `mypy --strict src/bmad/core/exceptions.py` passe
- [ ] Tests : 100% coverage sur ce fichier
- [ ] Fichier < 150 lignes

**Fichiers créés :**
- `src/bmad/core/exceptions.py`
- `tests/unit/core/test_exceptions.py`

---

#### V3-EP01-S03 — Configurer CI GitHub pour le package Python [M]

**Description** : Mettre à jour ou créer les workflows CI GitHub pour valider le package Python : linting (ruff), typage (mypy), tests (pytest), et vérification de packaging.

**Tâches :**
- [ ] Créer `.github/workflows/ci.yml` avec matrix Python 3.12 + 3.13
- [ ] Job `lint` : `ruff check src/ tests/`
- [ ] Job `type-check` : `mypy --strict src/bmad/`
- [ ] Job `test` : `pytest tests/ --cov=bmad --cov-report=xml`
- [ ] Job `build` : `python -m build && twine check dist/*`
- [ ] Trigger : push sur main + toutes les PR
- [ ] Badge dans README.md

**Critères d'acceptation :**
- [ ] CI passe en vert sur une PR
- [ ] Rapport de coverage généré et accessible
- [ ] Les 4 jobs s'exécutent en parallèle
- [ ] Temps total CI < 3 minutes

**Fichiers créés/modifiés :**
- `.github/workflows/ci.yml` (nouveau ou refactoré depuis l'existant)
- `README.md` (badge ajouté)

---

### EP02 — Système de Configuration (BmadConfig)

> **Objectif** : Créer le module de configuration qui charge, valide, et expose `bmad.yaml` comme objet Python typé.
> **Valeur** : Toute la plateforme dépend d'une configuration fiable et validée.
> **Risque principal** : Schema trop rigide → frustration utilisateur. Trop permissif → bugs runtime.
> **Critère de Done épic** : `BmadConfig.load("bmad.yaml")` retourne un objet typé validé, avec valeurs par défaut complètes.

#### V3-EP02-S01 — Définir le schéma bmad.yaml en dataclasses Python [L]

**Description** : Modéliser la totalité du schéma `bmad.yaml` (spécifié dans le PRD section 3.5) en dataclasses Python typées avec valeurs par défaut. Chaque section du YAML correspond à une dataclass.

**Tâches :**
- [ ] Créer `src/bmad/core/config.py`
- [ ] `ProjectConfig` dataclass (name, description, type, metaphor, stack, repos)
- [ ] `UserConfig` dataclass (name, language, document_language, skill_level)
- [ ] `AgentConfig` dataclass (id, source, persona, path, package, version, modules)
- [ ] `MemoryModuleConfig` dataclass (enabled, backend, consolidation, retention_days, qdrant_url)
- [ ] `CompletionContractConfig` dataclass (enabled, stacks, strict)
- [ ] `ContextRouterConfig` dataclass (enabled, model, warning_threshold, critical_threshold)
- [ ] `StigmergyConfig` dataclass (enabled, evaporation_hours)
- [ ] `DreamModeConfig` dataclass (enabled, schedule)
- [ ] `ModulesConfig` dataclass (memory, completion_contract, context_router, stigmergy, dream_mode)
- [ ] `WorkflowsConfig` dataclass (default, completion_contract, session_branching)
- [ ] `PathsConfig` dataclass (bmad_dir, output_dir, agents_dir, memory_dir, custom_agents_dir)
- [ ] `HooksConfig` dataclass (pre_commit, post_commit, pre_push)
- [ ] `SettingsConfig` dataclass (telemetry, auto_update_check, max_agent_context_tokens, trace_enabled, immune_system)
- [ ] `BmadConfig` dataclass racine (version, project, user, agents, modules, workflows, paths, hooks, settings)
- [ ] Valeurs par défaut raisonnables pour TOUTES les options
- [ ] Enum pour les valeurs contraintes (SkillLevel, MemoryBackend, WorkflowMode, etc.)
- [ ] Tests unitaires pour chaque dataclass (instantiation, defaults, validation)

**Critères d'acceptation :**
- [ ] Toutes les sections de bmad.yaml du PRD sont couvertes
- [ ] `mypy --strict` passe sur le fichier complet
- [ ] Chaque dataclass est `frozen=True` (immutable après création)
- [ ] Les Enums empêchent les valeurs invalides
- [ ] > 30 tests unitaires
- [ ] Fichier < 300 lignes (sinon splitter en config_types.py + config.py)

**Fichiers créés :**
- `src/bmad/core/config.py`
- `tests/unit/core/test_config.py`

---

#### V3-EP02-S02 — Parser bmad.yaml avec ruamel.yaml [M]

**Description** : Implémenter le chargement du fichier `bmad.yaml` depuis le disque avec parsing YAML (ruamel.yaml pour préserver les commentaires), validation des types, et mapping vers les dataclasses.

**Tâches :**
- [ ] Créer la méthode `BmadConfig.load(path: Path) -> BmadConfig`
- [ ] Utiliser `ruamel.yaml` pour le parsing (préserve commentaires round-trip)
- [ ] Valider le champ `version` (doit être "3.0")
- [ ] Mapper chaque section YAML vers la dataclass correspondante
- [ ] Gérer les sections absentes (valeurs par défaut)
- [ ] Gérer les clés inconnues (warning, pas erreur — forward compatibility)
- [ ] Lever `BmadConfigError` avec messages descriptifs si validation échoue
- [ ] Méthode `BmadConfig.save(path: Path)` pour réécrire le YAML (avec commentaires préservés)
- [ ] Tests avec 5+ variantes de bmad.yaml (minimal, full, partiel, invalide, vide)

**Critères d'acceptation :**
- [ ] `BmadConfig.load()` parse un bmad.yaml complet en < 50ms
- [ ] Les commentaires YAML sont préservés lors de `load() -> save()` round-trip
- [ ] Un yaml minimal (`version: "3.0"\nproject:\n  name: "test"`) charge avec defaults
- [ ] Un yaml invalide lève BmadConfigError avec message clair
- [ ] `mypy --strict` passe

**Fichiers créés/modifiés :**
- `src/bmad/core/config.py` (modifié — ajout méthodes load/save)
- `tests/unit/core/test_config.py` (modifié — ajout tests load/save)
- `tests/fixtures/bmad-yaml/minimal.yaml` (nouveau)
- `tests/fixtures/bmad-yaml/full.yaml` (nouveau)
- `tests/fixtures/bmad-yaml/invalid.yaml` (nouveau)

---

#### V3-EP02-S03 — Résolution des chemins et variables [S]

**Description** : Implémenter la résolution des chemins relatifs dans bmad.yaml (par rapport à la racine du projet), et la substitution des variables (`{project-root}`, `{user_name}`, etc.).

**Tâches :**
- [ ] Créer `src/bmad/core/resolver.py`
- [ ] `PathResolver` classe : résout les chemins relatifs par rapport au project root
- [ ] Résolution `{project-root}` → chemin absolu du projet
- [ ] Résolution des variables utilisateur (`{user_name}`, `{communication_language}`, etc.)
- [ ] Méthode `resolve_path(relative: str) -> Path` avec validation d'existence optionnelle
- [ ] Méthode `resolve_template(template: str, context: dict) -> str`
- [ ] Tests unitaires

**Critères d'acceptation :**
- [ ] `{project-root}/agents` résolu en chemin absolu correct
- [ ] Les chemins relatifs (`./agents/my-agent.md`) sont résolus par rapport au dossier contenant bmad.yaml
- [ ] Variables inconnues lèvent BmadConfigError (pas de substitution silencieuse vide)
- [ ] `mypy --strict` passe
- [ ] Fichier < 100 lignes

**Fichiers créés :**
- `src/bmad/core/resolver.py`
- `tests/unit/core/test_resolver.py`

---

#### V3-EP02-S04 — Génération de bmad.yaml depuis template [M]

**Description** : Implémenter la génération d'un fichier `bmad.yaml` depuis un template, avec pré-remplissage basé sur la détection du stack (pour `bmad init --auto`) ou les paramètres utilisateur.

**Tâches :**
- [ ] Créer `templates/bmad.yaml.tpl` — template commenté et documenté
- [ ] Méthode `BmadConfig.generate(project_name, user_name, stack, ...) -> BmadConfig`
- [ ] Méthode `BmadConfig.to_yaml(path: Path)` — écrit le YAML formaté avec commentaires
- [ ] Sélection automatique des agents basée sur le stack détecté
- [ ] Sélection automatique des modules activés basée sur le type de projet
- [ ] Tests : vérifier qu'un yaml généré est rechargeable (`generate -> save -> load` round-trip)

**Critères d'acceptation :**
- [ ] `BmadConfig.generate("Mon API", "Guilhem", ["python", "fastapi"])` produit un yaml valide
- [ ] Le yaml généré contient des commentaires explicatifs pour chaque section
- [ ] Round-trip `generate -> to_yaml -> load` produit un objet équivalent
- [ ] `mypy --strict` passe

**Fichiers créés :**
- `templates/bmad.yaml.tpl`
- `src/bmad/core/config.py` (modifié — ajout generate/to_yaml)
- `tests/unit/core/test_config.py` (modifié)

---

### EP03 — Infrastructure de Tests

> **Objectif** : Mettre en place l'infrastructure de tests (conftest, fixtures, helpers) et migrer les tests existants.
> **Valeur** : Sans tests solides, chaque refactoring est un risque.
> **Critère de Done épic** : `pytest tests/` passe avec fixtures pour projets factices et mocking des I/O.

#### V3-EP03-S01 — Créer conftest.py et fixtures de projets factices [M]

**Description** : Créer les fixtures pytest partagées : projets factices (django, express, terraform, vide), configuration temporaire, mocking du filesystem.

**Tâches :**
- [ ] Créer `tests/conftest.py` avec fixtures partagées
- [ ] Fixture `tmp_project` : crée un projet temporaire vide avec structure minimale
- [ ] Fixture `tmp_bmad_config` : crée un BmadConfig temporaire
- [ ] Fixture `django_project` : structure de projet Django factice (manage.py, requirements.txt, app/)
- [ ] Fixture `express_project` : structure Express.js factice (package.json, src/, tsconfig.json)
- [ ] Fixture `terraform_project` : structure Terraform factice (main.tf, variables.tf, modules/)
- [ ] Fixture `empty_project` : répertoire vide
- [ ] Fixture `existing_bmad_project` : projet avec _bmad/ déjà initialisé
- [ ] Helper `assert_file_exists(path)` et `assert_file_contains(path, content)`
- [ ] Créer `tests/fixtures/` avec les arbres de fichiers statiques si nécessaire

**Critères d'acceptation :**
- [ ] Chaque fixture crée un répertoire propre via `tmp_path`
- [ ] Les projets factices ont une structure réaliste (pas juste des fichiers vides)
- [ ] Pas d'effets de bord entre tests (isolation complète)
- [ ] `pytest tests/unit/core/test_config.py` utilise les fixtures correctement

**Fichiers créés :**
- `tests/conftest.py`
- `tests/unit/__init__.py`
- `tests/unit/core/__init__.py`
- `tests/integration/__init__.py`
- `tests/fixtures/` (statiques si besoin)

---

#### V3-EP03-S02 — Plan de migration des tests existants [M]

**Description** : Analyser les 19 200 lignes de tests existants, créer le mapping vers la nouvelle structure, et migrer les premiers tests (les plus simples) comme preuve de concept.

**Tâches :**
- [ ] Inventorier tous les fichiers test existants et leur couverture
- [ ] Mapper chaque `test_*.py` existant vers son emplacement dans `tests/unit/tools/`
- [ ] Identifier les tests qui nécessitent une adaptation (changement d'imports, paths)
- [ ] Migrer 5 fichiers tests simples comme proof of concept
- [ ] Documenter la procédure de migration pour les stories suivantes
- [ ] Vérifier que les tests migrés passent avec `pytest`

**Critères d'acceptation :**
- [ ] Document de mapping complet : ancien chemin → nouveau chemin pour les 56 fichiers test
- [ ] 5 fichiers test migrés et passants
- [ ] Procédure de migration documentée dans un commentaire en en-tête de conftest.py
- [ ] Aucune régression sur les tests non-migrés (ils continuent de fonctionner à leur emplacement d'origine)

**Fichiers créés :**
- `tests/unit/tools/test_context_router.py` (migré)
- `tests/unit/tools/test_agent_forge.py` (migré)
- `tests/unit/tools/test_agent_bench.py` (migré)
- `tests/unit/tools/test_harmony_check.py` (migré)
- `tests/unit/tools/test_antifragile_score.py` (migré)

---

## Phase 1 — EXTRACT

### EP04 — Extraction du Core Library (bmad.core)

> **Objectif** : Extraire la logique du noyau depuis `bmad-init.sh` (2 733 lignes Bash) et les scripts Python vers des modules importables dans `bmad.core`.
> **Valeur** : C'est LE pivot. Sans un core importable, pas de CLI, pas de SDK, pas de MCP.
> **Risque principal** : Le Bash contient de la logique implicite (état global, side effects) difficile à extraire proprement.
> **Critère de Done épic** : `from bmad.core import BmadProject; p = BmadProject(".")` fonctionne avec toutes les opérations de base (status, info, agents list).

#### V3-EP04-S01 — BmadProject : point d'entrée principal [L]

**Description** : Créer la classe `BmadProject` qui est le point d'entrée unique pour interagir avec un projet BMAD. Elle charge la config (`bmad.yaml`), résout les chemins, et fournit l'accès à toutes les sous-systèmes.

**Tâches :**
- [ ] Créer `src/bmad/core/project.py`
- [ ] `BmadProject.__init__(root: Path)` : détecte et charge `bmad.yaml`
- [ ] `BmadProject.config` : propriété retournant `BmadConfig`
- [ ] `BmadProject.root` : chemin racine du projet
- [ ] `BmadProject.bmad_dir` : chemin vers `_bmad/`
- [ ] `BmadProject.is_initialized() -> bool` : vérifie si le projet a une installation BMAD
- [ ] `BmadProject.agents() -> list[AgentInfo]` : liste des agents déployés
- [ ] `BmadProject.status() -> ProjectStatus` : dataclass avec état complet
- [ ] `BmadProject.context() -> ProjectContext` : contexte pour les agents (stack, structure, métriques)
- [ ] Dataclass `AgentInfo` (id, name, title, icon, path, module)
- [ ] Dataclass `ProjectStatus` (initialized, agents_count, memory_status, last_activity, etc.)
- [ ] Dataclass `ProjectContext` (name, stack, file_count, test_status, etc.)
- [ ] Tests unitaires avec les fixtures de projet factice

**Critères d'acceptation :**
- [ ] `BmadProject(".")` sur un projet initialisé retourne un objet valide
- [ ] `BmadProject(".")` sur un projet non-initialisé lève `BmadProjectError`
- [ ] `project.agents()` liste correctement tous les agents du `_bmad/agents/`
- [ ] `project.status()` retourne toutes les métriques
- [ ] `mypy --strict` passe
- [ ] Fichier < 300 lignes
- [ ] > 20 tests unitaires

**Fichiers créés :**
- `src/bmad/core/project.py`
- `tests/unit/core/test_project.py`

---

#### V3-EP04-S02 — StackScanner : détection automatique du stack [L]

**Description** : Extraire et améliorer la logique de détection de stack de `bmad-init.sh` vers un module Python propre. Le scanner analyse l'arborescence de fichiers pour détecter les technologies utilisées.

**Tâches :**
- [ ] Créer `src/bmad/core/scanner.py`
- [ ] `StackScanner.__init__(root: Path)`
- [ ] `StackScanner.scan() -> ScanResult` : scanne tout le projet
- [ ] Dataclass `ScanResult` (stacks: list[StackDetection], project_type: str, confidence: float)
- [ ] Dataclass `StackDetection` (name: str, confidence: float, evidence: list[str])
- [ ] Détection par fichiers marqueurs :
  - `go.mod` → Go
  - `package.json` + `tsconfig.json` → TypeScript
  - `package.json` + `*.tsx` → React
  - `requirements.txt` / `pyproject.toml` / `setup.py` → Python
  - `*.tf` / `*.tfvars` → Terraform
  - `Dockerfile` / `docker-compose*.yml` → Docker
  - `*.yaml` avec `kind:` + `apiVersion:` → Kubernetes
  - `playbook*.yml` / `ansible.cfg` → Ansible
  - `Cargo.toml` → Rust
  - `pom.xml` / `build.gradle` → Java
  - `Gemfile` → Ruby
  - `*.csproj` → C#/.NET
- [ ] Détection par analyse du contenu (imports, dépendances)
- [ ] Scoring de confiance multi-signal
- [ ] Déduction du type de projet (api, webapp, infrastructure, etc.)
- [ ] Tests avec les fixtures de projet factice (django, express, terraform)

**Critères d'acceptation :**
- [ ] Détecte correctement au moins 12 stacks différents
- [ ] Confiance > 0.8 quand le fichier marqueur principal est présent
- [ ] Gère les projets multi-stack (Python + Docker + K8s → infrastructure)
- [ ] Scan complet en < 500ms pour un projet de 1000 fichiers
- [ ] `mypy --strict` passe
- [ ] > 25 tests unitaires
- [ ] Fichier < 300 lignes

**Fichiers créés :**
- `src/bmad/core/scanner.py`
- `tests/unit/core/test_scanner.py`

---

#### V3-EP04-S03 — AgentLoader : chargement et instanciation d'agents [L]

**Description** : Créer le module qui charge les définitions d'agents depuis les fichiers `.md`, les fusionne avec les surcharges de bmad.yaml, et les expose comme objets Python typés.

**Tâches :**
- [ ] Créer `src/bmad/core/agent.py`
- [ ] `AgentLoader.__init__(project: BmadProject)`
- [ ] `AgentLoader.load(agent_id: str) -> AgentDefinition` : charge un agent par ID
- [ ] `AgentLoader.load_all() -> list[AgentDefinition]` : charge tous les agents déployés
- [ ] `AgentLoader.available() -> list[AgentInfo]` : agents disponibles (built-in + locaux + registry)
- [ ] Dataclass `AgentDefinition` (id, name, title, icon, role, identity, communication_style, principles, capabilities, module, path, persona_overrides)
- [ ] Parser le frontmatter YAML des fichiers `.md` d'agents
- [ ] Parser les blocs XML `<agent>` dans les fichiers `.md`
- [ ] Fusionner les surcharges de persona depuis bmad.yaml
- [ ] Résoudre les `source: builtin | local | registry`
- [ ] Tests unitaires avec agents factices

**Critères d'acceptation :**
- [ ] Charge un agent built-in depuis `archetypes/`
- [ ] Charge un agent custom local depuis un chemin relatif
- [ ] Fusionne les overrides de persona (communication_style, additional_principles)
- [ ] Gère les agents `modules: [context-router, ...]` associés
- [ ] `mypy --strict` passe
- [ ] > 20 tests unitaires

**Fichiers créés :**
- `src/bmad/core/agent.py`
- `tests/unit/core/test_agent.py`

---

#### V3-EP04-S04 — ArchetypeManager : gestion des templates d'équipe [M]

**Description** : Créer le module qui gère les archétypes (templates d'équipe pré-configurées). Listing, inspection, sélection basée sur le stack détecté, et déploiement des agents dans le projet.

**Tâches :**
- [ ] Créer `src/bmad/core/archetype.py`
- [ ] `ArchetypeManager.__init__(kit_root: Path)` : pointe vers le dossier `archetypes/`
- [ ] `ArchetypeManager.list() -> list[ArchetypeInfo]` : tous les archétypes disponibles
- [ ] `ArchetypeManager.inspect(archetype_id: str) -> ArchetypeDetail` : agents, DNA, contraintes
- [ ] `ArchetypeManager.recommend(scan_result: ScanResult) -> list[str]` : recommandation basée sur le stack
- [ ] `ArchetypeManager.deploy(archetype_id: str, target: Path) -> DeployResult` : copie les agents dans le projet
- [ ] Dataclass `ArchetypeInfo` (id, name, description, agent_count, stack_tags)
- [ ] Dataclass `ArchetypeDetail` (info + agents, dna, constraints)
- [ ] Dataclass `DeployResult` (deployed_agents, skipped_agents, warnings)
- [ ] Parsing du `archetype.dna.yaml` de chaque archétype
- [ ] Tests unitaires

**Critères d'acceptation :**
- [ ] Liste les 6 archétypes existants (minimal, web-app, infra-ops, fix-loop, stack, meta)
- [ ] `recommend()` avec un scan Python+Docker retourne `["minimal", "stack/python", "stack/docker"]`
- [ ] `deploy()` copie les fichiers sans écraser les existants
- [ ] `mypy --strict` passe
- [ ] > 15 tests unitaires

**Fichiers créés :**
- `src/bmad/core/archetype.py`
- `tests/unit/core/test_archetype.py`

---

#### V3-EP04-S05 — InitEngine : logique d'initialisation de projet [XL]

**Description** : Extraire toute la logique de `bmad init` de `bmad-init.sh` vers Python. C'est la story la plus grosse — elle couvre la création de `_bmad/`, le déploiement des agents, la génération de `bmad.yaml`, et la configuration initiale.

**Tâches :**
- [ ] Créer `src/bmad/core/init.py`
- [ ] `InitEngine.__init__(target: Path)`
- [ ] `InitEngine.init(name: str, user: str, language: str, archetype: str, auto: bool) -> InitResult`
- [ ] Orchestration : scanner → recommander archétype → générer config → déployer agents → écrire bmad.yaml
- [ ] Mode `--auto` : détect stack + choix archétype automatique
- [ ] Mode `--archetype TYPE` : archétype explicite
- [ ] Créer la structure `_bmad/` (agents, memory, config)
- [ ] Générer `bmad.yaml` avec la config détectée
- [ ] Vérifier que le projet cible n'est pas déjà initialisé (sauf `--force`)
- [ ] Dataclass `InitResult` (success, agents_deployed, config_path, warnings)
- [ ] Logging détaillé de chaque étape (pour debug)
- [ ] Tests d'intégration avec les fixtures de projet factice

**Critères d'acceptation :**
- [ ] `InitEngine.init("Test", "Guilhem", "Français", archetype="minimal")` crée une installation BMAD valide
- [ ] `InitEngine.init(..., auto=True)` sur un projet Django détecte Python et choisit le bon archétype
- [ ] Sur un projet déjà initialisé, lève `BmadProjectError` (sauf si force=True)
- [ ] `bmad.yaml` généré est rechargeable par `BmadConfig.load()`
- [ ] `BmadProject(target)` fonctionne après init
- [ ] `mypy --strict` passe
- [ ] > 15 tests d'intégration

**Fichiers créés :**
- `src/bmad/core/init.py`
- `tests/integration/test_init_workflow.py`

---

### EP05 — Extraction des Tools (bmad.tools)

> **Objectif** : Refactorer les 48 scripts Python standalone en modules importables dans `bmad.tools/`.
> **Valeur** : Chaque outil devient utilisable en tant que SDK et en tant que CLI.
> **Risque principal** : Régression sur les tests existants.
> **Critère de Done épic** : `from bmad.tools import ContextRouter, AgentForge` fonctionne ET les anciens scripts continuent de fonctionner.

#### V3-EP05-S01 — Définir le pattern de refactoring (Tool Base Class + migration guide) [M]

**Description** : Créer la classe de base `BmadTool` et documenter le pattern de migration pour chaque outil. Chaque outil refactoré sera une classe avec une API publique typée + un `__main__` CLI wrapper.

**Tâches :**
- [ ] Créer `src/bmad/tools/_common.py` avec `BmadTool` ABC
- [ ] `BmadTool.__init__(project: BmadProject)` : accès au projet
- [ ] `BmadTool.run(args)` : méthode d'exécution abstraite
- [ ] Helper `find_project_root(start: Path) -> Path` : remonte l'arbre pour trouver bmad.yaml
- [ ] Helper `load_yaml(path: Path) -> dict` : wrapper ruamel.yaml
- [ ] Helper `save_yaml(data: dict, path: Path)` : wrapper ruamel.yaml avec commentaires
- [ ] Helper `estimate_tokens(text: str) -> int` : estimation standard
- [ ] Documenter le pattern dans un commentaire en en-tête de `_common.py`
- [ ] Migrer 1 outil simple comme proof of concept (`harmony_check.py`)
- [ ] Tests unitaires pour les helpers

**Critères d'acceptation :**
- [ ] `BmadTool` a une interface claire documentée
- [ ] Le proof of concept `HarmonyCheck` est importable ET exécutable en CLI
- [ ] Pattern documenté : chaque outil a une classe publique + un `if __name__` wrapper
- [ ] `mypy --strict` passe sur _common.py
- [ ] > 10 tests unitaires pour les helpers

**Fichiers créés :**
- `src/bmad/tools/_common.py`
- `src/bmad/tools/harmony_check.py` (migré comme PoC)
- `tests/unit/tools/test_common.py`
- `tests/unit/tools/test_harmony_check.py` (migré)

---

#### V3-EP05-S02 — Migrer les outils Tier 1 (6 outils core) [XL]

**Description** : Migrer les 6 outils les plus importants vers le nouveau pattern. Ce sont les outils utilisés par le CLI principal.

**Outils Tier 1 :**
1. `context-router.py` → `context_router.py` (604 lignes)
2. `agent-forge.py` → `agent_forge.py` (923 lignes)
3. `agent-bench.py` → `agent_bench.py` (576 lignes)
4. `context-guard.py` → `context_guard.py` (756 lignes)
5. `dna-evolve.py` → `dna_evolve.py` (790 lignes)
6. `dashboard.py` → `dashboard.py`

**Tâches (pour chaque outil) :**
- [ ] Extraire les classes/fonctions en classe publique héritant de `BmadTool` (si pertinent) ou en fonctions standalone typées
- [ ] Séparer la logique métier de la présentation CLI
- [ ] Remplacer les `print()` par des structures de données retournées
- [ ] Ajouter les type hints manquants
- [ ] Conserver le `if __name__ == "__main__"` comme wrapper
- [ ] Migrer les tests existants correspondants
- [ ] Vérifier mypy --strict sur chaque fichier migré
- [ ] Si le fichier > 300 lignes, le splitté en sous-modules

**Critères d'acceptation :**
- [ ] `from bmad.tools import ContextRouter` fonctionne
- [ ] `ContextRouter(project).plan("atlas")` retourne un objet structuré (pas du texte)
- [ ] `python -m bmad.tools.context_router --help` fonctionne (backward compat)
- [ ] Tous les tests existants pour ces 6 outils passent
- [ ] `mypy --strict` passe sur les 6 fichiers
- [ ] 0 régression

**Fichiers créés/modifiés :**
- `src/bmad/tools/context_router.py` (migré)
- `src/bmad/tools/agent_forge.py` (migré)
- `src/bmad/tools/agent_bench.py` (migré)
- `src/bmad/tools/context_guard.py` (migré)
- `src/bmad/tools/dna_evolve.py` (migré)
- `src/bmad/tools/dashboard.py` (migré)
- `tests/unit/tools/` (6 fichiers test migrés)

---

#### V3-EP05-S03 — Migrer les outils Tier 2 (14 outils intelligence) [XL]

**Description** : Migrer les 14 outils de la couche intelligence contextuelle et résilience.

**Outils Tier 2 :**
1. `preflight-check.py` → `preflight_check.py`
2. `nudge-engine.py` → `nudge_engine.py`
3. `desire-paths.py` → `desire_paths.py`
4. `early-warning.py` → `early_warning.py`
5. `semantic-chain.py` → `semantic_chain.py`
6. `rosetta.py` → `rosetta.py`
7. `immune-system.py` → `immune_system.py`
8. `self-healing.py` → `self_healing.py`
9. `dark-matter.py` → `dark_matter.py`
10. `oracle.py` → `oracle.py`
11. `bias-toolkit.py` → `bias_toolkit.py`
12. `crescendo.py` → `crescendo.py`
13. `stigmergy.py` → `stigmergy.py`
14. `failure-museum.py` → `failure_museum.py`

**Tâches (pattern identique à EP05-S02) :**
- [ ] Migrer chaque outil vers une classe/module importable
- [ ] Séparer logique métier / présentation
- [ ] Type hints complets
- [ ] Tests migrés et passants
- [ ] mypy --strict

**Critères d'acceptation :**
- [ ] Les 14 outils sont importables via `from bmad.tools import *`
- [ ] Tous les tests existants passent
- [ ] `mypy --strict` passe sur les 14 fichiers
- [ ] 0 régression

---

#### V3-EP05-S04 — Migrer les outils Tier 3 (28 outils restants) [XL]

**Description** : Migrer les 28 outils restants (évolution, simulation, visualisation, etc.).

**Outils Tier 3 :**
`adversarial-consensus`, `antifragile-score`, `auto-doc`, `cognitive-flywheel`, `cross-migrate`, `crispr`, `decision-log`, `digital-twin`, `distill`, `dream`, `gen-tests`, `incubator`, `memory-lint`, `mirror-agent`, `mycelium`, `new-game-plus`, `nso`, `project-graph`, `quantum-branch`, `r-and-d`, `reasoning-stream`, `schema-validator`, `sensory-buffer`, `swarm-consensus`, `time-travel`, `workflow-adapt`, `workflow-snippets` (si existe), `session-save` (framework/memory/)

**Tâches (pattern identique) :**
- [ ] Migrer chaque outil
- [ ] Tests migrés
- [ ] mypy --strict

**Critères d'acceptation :**
- [ ] Les 48 outils au total sont importables
- [ ] `from bmad.tools import *` expose toutes les classes publiques
- [ ] Tous les tests passent
- [ ] 0 régression

---

#### V3-EP05-S05 — Exports publics et __init__.py des tools [S]

**Description** : Créer le `__init__.py` de `bmad.tools` qui expose tous les outils de manière propre avec des imports typés.

**Tâches :**
- [ ] `src/bmad/tools/__init__.py` avec `__all__` listant tous les exports publics
- [ ] Imports lazy si nécessaire (pour ne pas charger tous les 48 modules au import)
- [ ] Documentation inline des exports
- [ ] Export `from bmad.tools import ContextRouter, AgentForge, HarmonyCheck, ...`
- [ ] Vérifier que `import bmad.tools` ne prend pas > 100ms (lazy loading si besoin)

**Critères d'acceptation :**
- [ ] `from bmad.tools import ContextRouter` fonctionne
- [ ] `from bmad.tools import *` expose tous les outils
- [ ] Import time < 100ms (mesuré)
- [ ] `mypy --strict` passe

---

### EP06 — Extraction du Système Mémoire (bmad.memory)

> **Objectif** : Refactorer le système mémoire (backends, maintenance, session) en un module propre.
> **Valeur** : La mémoire est un module cherrypickable — des gens voudront JUSTE la mémoire.
> **Critère de Done épic** : `from bmad.memory import MemoryManager; mm = MemoryManager(config)` fonctionne avec tous les backends.

#### V3-EP06-S01 — MemoryBackend ABC et backend local [M]

**Description** : Créer l'interface abstraite `MemoryBackend` et le backend local (JSON fichier) comme implémentation de référence.

**Tâches :**
- [ ] Créer `src/bmad/memory/backends/base.py` avec ABC `MemoryBackend`
- [ ] Méthodes abstraites : `store()`, `recall()`, `search()`, `consolidate()`, `health_check()`
- [ ] Créer `src/bmad/memory/backends/local.py` : implémentation JSON/fichier
- [ ] Migration depuis `framework/memory/backends/backend_local.py` existant
- [ ] Type hints complets
- [ ] Tests unitaires

**Critères d'acceptation :**
- [ ] `LocalMemoryBackend` implémente toutes les méthodes de l'ABC
- [ ] Store/recall round-trip fonctionne
- [ ] `mypy --strict` passe
- [ ] > 15 tests

---

#### V3-EP06-S02 — Backends Qdrant et Ollama [L]

**Description** : Migrer les backends Qdrant (local + server) et Ollama.

**Tâches :**
- [ ] `src/bmad/memory/backends/qdrant.py` : migration de `backend_qdrant_local.py` + `backend_qdrant_server.py`
- [ ] `src/bmad/memory/backends/ollama.py` : migration de `backend_ollama.py`
- [ ] Gestion gracieuse des dépendances optionnelles (import conditionnel)
- [ ] Tests avec mocking des clients externes

**Critères d'acceptation :**
- [ ] Les backends fonctionnent si la dépendance optionnelle est installée
- [ ] Message d'erreur clair si la dépendance manque (`pip install bmad-kit[qdrant]`)
- [ ] `mypy --strict` passe

---

#### V3-EP06-S03 — MemoryManager : API unifiée [M]

**Description** : Créer le `MemoryManager` qui expose une API unifiée au-dessus des backends, avec sélection automatique du backend basée sur la config.

**Tâches :**
- [ ] Créer `src/bmad/memory/manager.py`
- [ ] `MemoryManager.__init__(config: MemoryModuleConfig)`
- [ ] Auto-sélection du backend basée sur `config.backend`
- [ ] `store()`, `recall()`, `search()`, `consolidate()`, `health()`
- [ ] Fallback automatique : si Qdrant échoue → local
- [ ] Migration de `maintenance.py` et `session-save.py`
- [ ] Tests unitaires

**Critères d'acceptation :**
- [ ] `MemoryManager(config)` avec backend="local" fonctionne sans dépendance externe
- [ ] Fallback testé et fonctionnel
- [ ] `mypy --strict` passe

---

## Phase 2 — INTERFACE

### EP07 — CLI Typer (bmad.cli)

> **Objectif** : Construire le CLI moderne avec Typer comme thin wrapper sur `bmad.core`.
> **Valeur** : Remplace les 2 733 lignes de Bash. UX professionnelle avec couleurs, auto-completion, help formatée.
> **Critère de Done épic** : `bmad --help` affiche toutes les commandes. `bmad init`, `bmad status`, `bmad add` fonctionnent.

#### V3-EP07-S01 — App Typer principal + commande version/status [M]

**Description** : Créer l'application Typer principale avec les commandes de base (`--version`, `status`, `doctor`).

**Tâches :**
- [ ] Créer `src/bmad/cli/app.py` avec `typer.Typer()`
- [ ] Callback `--version` qui affiche la version
- [ ] Commande `bmad status` : affiche le dashboard du projet (nom, stack, agents, health)
- [ ] Commande `bmad doctor` : diagnostic de l'installation
- [ ] Output formaté avec Rich (tables, couleurs, icons)
- [ ] Gestion d'erreurs globale (catch `BmadError` → message formaté)
- [ ] `main()` qui lance `app()`
- [ ] Tests CLI unitaires (CliRunner de Typer)

**Critères d'acceptation :**
- [ ] `bmad --version` affiche `bmad-kit 3.0.0-alpha.1`
- [ ] `bmad status` dans un projet initialisé affiche le dashboard
- [ ] `bmad status` dans un projet non-initialisé affiche un message d'erreur clair
- [ ] `bmad doctor` vérifie l'installation et affiche un rapport
- [ ] `mypy --strict` passe

**Fichiers créés :**
- `src/bmad/cli/app.py`
- `src/bmad/cli/cmd_status.py`
- `src/bmad/cli/cmd_doctor.py`
- `tests/unit/cli/test_app.py`

---

#### V3-EP07-S02 — Commande bmad init [L]

**Description** : Implémenter la commande `bmad init` qui wrape `InitEngine`.

**Tâches :**
- [ ] Créer `src/bmad/cli/cmd_init.py`
- [ ] Options : `--name`, `--user`, `--lang`, `--archetype`, `--auto`, `--force`
- [ ] Mode interactif si options manquantes (prompt avec Rich)
- [ ] Affichage progressif avec spinner Rich pendant le scan
- [ ] Résumé final : agents déployés, fichiers créés, prochaines étapes
- [ ] Tests CLI avec CliRunner

**Critères d'acceptation :**
- [ ] `bmad init --name "Test" --user "Guilhem" --auto` fonctionne end-to-end
- [ ] Mode interactif fonctionne (prompt pour chaque option manquante)
- [ ] Output clair et informatif
- [ ] `mypy --strict` passe

---

#### V3-EP07-S03 — Commande bmad add / remove [L]

**Description** : Implémenter les commandes pour ajouter et retirer des agents et modules individuellement.

**Tâches :**
- [ ] Créer `src/bmad/cli/cmd_add.py`
- [ ] `bmad add agent <id>` : ajoute un agent built-in ou depuis un chemin
- [ ] `bmad add module <name>` : active un module dans bmad.yaml
- [ ] `bmad add archetype <id>` : déploie un archétype complet
- [ ] Créer `src/bmad/cli/cmd_remove.py`
- [ ] `bmad remove agent <id>` : retire un agent (avec confirmation)
- [ ] `bmad remove module <name>` : désactive un module
- [ ] Mise à jour automatique de `bmad.yaml` après chaque opération
- [ ] Tests CLI

**Critères d'acceptation :**
- [ ] `bmad add agent architect` ajoute l'agent et met à jour bmad.yaml
- [ ] `bmad add module memory --backend qdrant` active la mémoire Qdrant
- [ ] `bmad remove agent architect` retire l'agent avec confirmation
- [ ] Opérations idempotentes (ajouter deux fois le même ≠ erreur)
- [ ] `mypy --strict` passe

---

#### V3-EP07-S04 — Commande bmad up / down [M]

**Description** : Implémenter `bmad up` qui instancie tout depuis `bmad.yaml` (comme `docker-compose up`) et `bmad down` qui nettoie.

**Tâches :**
- [ ] Créer `src/bmad/cli/cmd_up.py`
- [ ] `bmad up` : lit bmad.yaml → déploie agents → active modules → vérifie health
- [ ] `bmad up --dry-run` : affiche ce qui serait fait sans le faire
- [ ] Créer `src/bmad/cli/cmd_down.py` (optionnel, usage rare)
- [ ] `bmad down` : nettoie les fichiers BMAD (avec confirmation)
- [ ] Tests CLI

**Critères d'acceptation :**
- [ ] `bmad up` sur un projet avec bmad.yaml valide déploie tout
- [ ] `bmad up --dry-run` n'écrit rien, affiche le plan
- [ ] `bmad down` demande confirmation avant de supprimer

---

#### V3-EP07-S05 — Commandes tools (forge, bench, guard, evolve, trace, dream, etc.) [XL]

**Description** : Créer les commandes CLI pour tous les outils existants. Chaque commande est un thin wrapper sur la classe de `bmad.tools`.

**Tâches :**
- [ ] `cmd_forge.py` : bmad forge "description" | --from-gap | --from-trace | --list | --install
- [ ] `cmd_bench.py` : bmad bench --report | --improve | --summary | --agent NAME
- [ ] `cmd_guard.py` : bmad guard | --agent NAME | --detail | --suggest
- [ ] `cmd_evolve.py` : bmad evolve | --report | --apply | --since DATE
- [ ] `cmd_trace.py` : bmad trace --tail N | --agent NAME | --type TYPE
- [ ] `cmd_dream.py` : bmad dream | --since DATE | --quick | --dry-run
- [ ] `cmd_session.py` : bmad session branch NAME | list | diff | merge | archive
- [ ] `cmd_hooks.py` : bmad hooks --install | --list | --status
- [ ] `cmd_validate.py` : bmad validate --dna PATH | --all
- [ ] `cmd_changelog.py` : bmad changelog
- [ ] `cmd_consensus.py` : bmad consensus --proposal "..." | --history | --stats
- [ ] `cmd_antifragile.py` : bmad antifragile | --detail | --trend
- [ ] `cmd_reasoning.py` : bmad reasoning log | query | analyze
- [ ] `cmd_migrate.py` : bmad migrate export | import | inspect | diff
- [ ] `cmd_darwinism.py` : bmad darwinism evaluate | leaderboard | evolve | history
- [ ] `cmd_stigmergy.py` : bmad stigmergy emit | sense | amplify | landscape
- [ ] Tests CLI pour chaque commande (au moins smoke test)

**Critères d'acceptation :**
- [ ] Toutes les subcommands de l'ancien `bmad-init.sh` sont couvertes
- [ ] `bmad --help` affiche toutes les commandes avec descriptions
- [ ] Chaque commande a son propre `--help` détaillé
- [ ] Auto-completion Zsh/Bash/Fish fonctionne (générée par Typer)
- [ ] `mypy --strict` passe sur tous les cmd_*.py

---

#### V3-EP07-S06 — Commande bmad eject [M]

**Description** : Implémenter `bmad eject` qui transforme l'installation BMAD en fichiers statiques sans dépendance au package.

**Tâches :**
- [ ] Créer `src/bmad/cli/cmd_eject.py`
- [ ] Copier tous les agents, configs, templates en fichiers standalone
- [ ] Remplacer les imports `bmad.*` par des scripts inline si applicable
- [ ] Supprimer les références au package bmad-kit
- [ ] Conserver les fichiers MD/YAML tels quels (déjà standalone)
- [ ] Générer un README expliquant la structure éjectée
- [ ] Confirmation requise (irréversible)
- [ ] Tests

**Critères d'acceptation :**
- [ ] Après `bmad eject`, le projet n'a plus de dépendance à bmad-kit
- [ ] Les fichiers d'agents et workflows restent fonctionnels
- [ ] Message de confirmation clair
- [ ] `mypy --strict` passe

---

### EP08 — Serveur MCP Natif (bmad.mcp)

> **Objectif** : Implémenter le serveur MCP qui expose `bmad.core` et `bmad.tools` via le protocole MCP.
> **Valeur** : Permet aux agents IA (Claude Desktop, Cursor, Copilot) de consommer BMAD programmatiquement.
> **Critère de Done épic** : Le serveur MCP démarre, expose ≥ 10 tools, et est consommable depuis Claude Desktop.

#### V3-EP08-S01 — Serveur MCP de base avec tools Project [L]

**Description** : Créer le serveur MCP avec les tools fondamentaux (project context, agent list, status).

**Tâches :**
- [ ] Créer `src/bmad/mcp/server.py`
- [ ] Utiliser le SDK `mcp` officiel (Anthropic)
- [ ] Tool `bmad_project_context` : retourne le contexte complet du projet
- [ ] Tool `bmad_agent_list` : liste des agents déployés
- [ ] Tool `bmad_status` : dashboard complet
- [ ] Tool `bmad_config` : retourne la config bmad.yaml parsée
- [ ] Configuration du serveur MCP dans `bmad.yaml` (activé/désactivé)
- [ ] Documentation d'intégration (Claude Desktop, Cursor)
- [ ] Tests avec client MCP mock

**Critères d'acceptation :**
- [ ] `python -m bmad.mcp.server` démarre un serveur MCP fonctionnel
- [ ] Claude Desktop peut se connecter et utiliser les tools
- [ ] Réponses JSON structurées (pas de texte brut)
- [ ] `mypy --strict` passe

**Fichiers créés :**
- `src/bmad/mcp/server.py`
- `tests/integration/test_mcp_server.py`

---

#### V3-EP08-S02 — Tools MCP pour les outils avancés [L]

**Description** : Exposer les outils avancés (context router, forge, bench, guard, etc.) via MCP.

**Tâches :**
- [ ] Tool `bmad_context_plan` : plan de chargement contexte pour un agent
- [ ] Tool `bmad_forge_create` : créer un agent depuis une description
- [ ] Tool `bmad_bench_report` : rapport de benchmark
- [ ] Tool `bmad_guard_budget` : budget de contexte
- [ ] Tool `bmad_merge_plan` : plan de merge non-destructif
- [ ] Tool `bmad_stigmergy_sense` : phéromones actives
- [ ] Tool `bmad_harmony_check` : score d'harmonie
- [ ] Tool `bmad_oracle_report` : rapport Oracle introspectif
- [ ] Tool `bmad_immune_scan` : scan du système immunitaire
- [ ] Tool `bmad_dream_insights` : insights du Dream Mode
- [ ] Tests

**Critères d'acceptation :**
- [ ] ≥ 10 tools MCP exposés
- [ ] Chaque tool a une description claire et des paramètres typés
- [ ] Input validation (mauvais paramètres → message d'erreur, pas crash)
- [ ] `mypy --strict` passe

---

### EP09 — bmad.yaml Lifecycle (déclaratif)

> **Objectif** : Faire de `bmad.yaml` la source unique de vérité qui drive tout le système.
> **Valeur** : Reproductibilité. `git clone && bmad up` = même équipe, même config.
> **Critère de Done épic** : `bmad up` instancie correctement un projet depuis bmad.yaml seul.

#### V3-EP09-S01 — Validation de schéma bmad.yaml [M]

**Description** : Implémenter une validation stricte du schema bmad.yaml avec messages d'erreur actionables.

**Tâches :**
- [ ] Créer `src/bmad/core/validator.py`
- [ ] Validation des types (string, int, bool, list, enum)
- [ ] Validation des contraintes (agent IDs uniques, modules reconnus, stacks valides)
- [ ] Validation des références (agent paths existent, backends reconnus)
- [ ] Messages d'erreur avec ligne + suggestion de correction
- [ ] Commande `bmad validate` qui vérifie bmad.yaml
- [ ] Tests avec 10+ cas de validation (valide, invalide, edge cases)

**Critères d'acceptation :**
- [ ] Un yaml invalide produit un message d'erreur clair avec la ligne et une suggestion
- [ ] Un yaml valide passe sans warning
- [ ] `bmad validate` retourne exit code 0 (ok) ou 1 (erreur)
- [ ] `mypy --strict` passe

---

#### V3-EP09-S02 — Réconciliation state ← → bmad.yaml [L]

**Description** : Détecter et résoudre les drifts entre l'état réel du filesystem (`_bmad/`) et la config déclarée dans `bmad.yaml`.

**Tâches :**
- [ ] `bmad up --reconcile` : détecte les drifts et les corrige
- [ ] Détection : agent dans bmad.yaml mais pas déployé, agent déployé mais pas dans bmad.yaml
- [ ] Détection : module activé dans yaml mais fichiers manquants
- [ ] Résolution : proposer les actions correctives
- [ ] Mode interactif : demander approbation pour chaque action
- [ ] Mode force : appliquer toutes les corrections
- [ ] Tests d'intégration

**Critères d'acceptation :**
- [ ] Détecte les agents manquants, les modules désactivés, les fichiers orphelins
- [ ] Mode interactif fonctionne
- [ ] `bmad up` après réconciliation = état cohérent
- [ ] `mypy --strict` passe

---

## Phase 3 — PLATFORM

### EP10 — Registry Local

> **Objectif** : Permettre l'installation d'agents et modules depuis des sources locales (archetypes built-in + fichiers locaux).
> **Valeur** : Fondation pour le registry communautaire. Unifie la gestion des sources.
> **Critère de Done épic** : `bmad registry list` affiche tous les agents/modules disponibles.

#### V3-EP10-S01 — LocalRegistry : inventaire des builtin [M]

**Description** : Créer le `LocalRegistry` qui expose les agents et modules built-in comme un catalogue consultable.

**Tâches :**
- [ ] Créer `src/bmad/registry/local.py`
- [ ] `LocalRegistry.__init__(kit_root: Path)`
- [ ] `LocalRegistry.agents() -> list[AgentInfo]` : tous les agents des archetypes
- [ ] `LocalRegistry.modules() -> list[ModuleInfo]` : tous les modules disponibles
- [ ] `LocalRegistry.search(query: str) -> list[RegistryItem]` : recherche textuelle
- [ ] `LocalRegistry.get(item_id: str) -> RegistryItem` : détail d'un item
- [ ] Indexation des agents par stack, capability, archetype
- [ ] Tests unitaires

**Critères d'acceptation :**
- [ ] Liste les 21+ agents existants avec métadonnées complètes
- [ ] `search("kubernetes")` retourne les agents K8s
- [ ] `mypy --strict` passe

---

#### V3-EP10-S02 — Commande bmad registry [M]

**Description** : Implémenter les commandes CLI pour interagir avec le registry.

**Tâches :**
- [ ] `bmad registry list` : affiche tous les agents/modules disponibles
- [ ] `bmad registry search <query>` : recherche dans le catalogue
- [ ] `bmad registry inspect <id>` : détail d'un agent/module
- [ ] `bmad registry install <id>` : installe depuis le registry local
- [ ] Output formaté avec Rich (tables, descriptions)
- [ ] Tests CLI

**Critères d'acceptation :**
- [ ] `bmad registry list` affiche une table formatée
- [ ] `bmad registry install stack/go` déploie l'agent Go
- [ ] `mypy --strict` passe

---

### EP11 — Registry Communautaire (v3.1+)

> **Objectif** : Permettre la publication et l'installation d'agents depuis des sources distantes.
> **Priorité** : BASSE — v3.1 au minimum. Ne pas commencer avant EP01-EP10 validés.
> **Critère de Done épic** : `bmad registry publish` et `bmad registry install @user/agent` fonctionnent.

#### V3-EP11-S01 — Spec du format de package agent [M]

**Description** : Définir le format de packaging d'un agent communautaire (structure de fichiers, metadata, versions).

**Tâches :**
- [ ] Définir le schéma `agent-package.yaml` (name, version, author, agent.md, tests, README)
- [ ] Définir les conventions de nommage (`bmad-agent-<name>`)
- [ ] Définir le workflow de publication (validation → packaging → upload)
- [ ] Documenter dans `docs/publishing-agents.md`

---

#### V3-EP11-S02 — RemoteRegistry : client PyPI / GitHub Packages [L]

**Description** : Implémenter le client pour publier et installer des agents depuis PyPI ou GitHub Packages.

**Tâches :**
- [ ] `src/bmad/registry/remote.py`
- [ ] `RemoteRegistry.search(query) -> list[RemoteAgent]`
- [ ] `RemoteRegistry.install(package_name) -> Path`
- [ ] `RemoteRegistry.publish(agent_dir) -> str` (retourne l'URL)
- [ ] Gestion des versions (SemVer, compatibilité)
- [ ] Cache local des packages téléchargés
- [ ] Tests avec mocking des API

---

### EP12 — bmad eject (Standalone Mode)

> (Couvert par V3-EP07-S06 — pas d'épic séparé nécessaire)

---

### EP13 — Merge Engine (Non-Destructif)

> **Objectif** : Permettre de fusionner BMAD dans un projet existant sans collision de fichiers.
> **Valeur** : Le "plug-and-play" pour le Persona A ("Le Greffeur").
> **Risque principal** : Edge cases multiples (conflits .github/, hooks existants, _bmad/ existant).
> **Critère de Done épic** : `bmad merge` fusionne sans toucher aux fichiers existants, avec rollback.

#### V3-EP13-S01 — MergeEngine : analyse de conflits [L]

**Description** : Créer le moteur d'analyse qui scanne le projet cible et identifie tous les conflits potentiels avant le merge.

**Tâches :**
- [ ] Créer `src/bmad/core/merge.py`
- [ ] `MergeEngine.__init__(source: Path, target: Path)`
- [ ] `MergeEngine.analyze() -> MergePlan` : analyse sans modification
- [ ] Dataclass `MergePlan` (files_to_create, files_conflict, directories_to_create, warnings)
- [ ] Dataclass `MergeConflict` (path, source_content, target_content, resolution_type)
- [ ] Détection des conflits :
  - `_bmad/` existe déjà
  - `.github/copilot-instructions.md` existe
  - Git hooks existants
  - Fichiers YAML avec mêmes noms
- [ ] Proposition de résolution pour chaque conflit (skip, rename, merge-content, overwrite)
- [ ] Tests avec fixtures de projets avec pré-existants

**Critères d'acceptation :**
- [ ] Analyse un projet Django avec `.github/` existant → détecte les conflits
- [ ] Aucune modification de fichier pendant l'analyse
- [ ] Plan de merge complet et actionable
- [ ] `mypy --strict` passe
- [ ] > 20 tests

---

#### V3-EP13-S02 — MergeEngine : exécution et rollback [L]

**Description** : Exécuter le plan de merge avec journalisation et capacité de rollback.

**Tâches :**
- [ ] `MergeEngine.execute(plan: MergePlan) -> MergeResult`
- [ ] Journalisation dans `.bmad-merge-log.json` (chaque opération enregistrée)
- [ ] Mode dry-run (affiche les opérations sans les exécuter)
- [ ] Rollback : `MergeEngine.undo(log_path: Path)` — annule le dernier merge
- [ ] Gestion atomique : si une opération échoue, tout est rollbacké
- [ ] Commande CLI : `bmad merge --from <path|url>`
- [ ] Commande CLI : `bmad merge --undo`
- [ ] Tests d'intégration

**Critères d'acceptation :**
- [ ] Merge sur un projet de 500 fichiers sans collision
- [ ] Rollback restaure l'état exact d'avant le merge
- [ ] `--dry-run` n'écrit rien
- [ ] `.bmad-merge-log.json` traçable
- [ ] `mypy --strict` passe

---

#### V3-EP13-S03 — Merge depuis URL (GitHub) [M]

**Description** : Permettre le merge depuis un repo GitHub ou une URL.

**Tâches :**
- [ ] Support `bmad merge --from https://github.com/user/repo`
- [ ] Clone temporaire dans un répertoire tmp
- [ ] Analyse des conflits
- [ ] Merge sélectif (l'utilisateur choisit quels agents/modules importer)
- [ ] Nettoyage du clone temporaire après merge
- [ ] Tests

**Critères d'acceptation :**
- [ ] `bmad merge --from https://github.com/user/bmad-agents` fonctionne
- [ ] L'utilisateur peut sélectionner les éléments à merger
- [ ] Nettoyage propre après opération

---

### EP14 — Migration v2 → v3

> **Objectif** : Permettre aux projets existants (v2) de migrer vers la structure v3.
> **Valeur** : Rétrocompatibilité — les 2 projets existants de Guilhem doivent fonctionner.
> **Critère de Done épic** : `bmad upgrade` migre un projet v2 vers v3.

#### V3-EP14-S01 — Commande bmad upgrade [L]

**Description** : Implémenter la migration automatique de la structure v2 vers v3.

**Tâches :**
- [ ] Créer `src/bmad/cli/cmd_upgrade.py`
- [ ] Détecter la version actuelle du projet (v2 = pas de bmad.yaml, structure _bmad/ ancienne)
- [ ] Générer `bmad.yaml` depuis `project-context.yaml` existant
- [ ] Réorganiser l'arborescence si nécessaire
- [ ] Conserver tous les fichiers mémoire (shared-context, decisions-log, learnings)
- [ ] Mode `--dry-run` : afficher les changements sans les appliquer
- [ ] Tests avec un projet v2 factice

**Critères d'acceptation :**
- [ ] Un projet v2 (avec project-context.yaml) est migré en v3 (avec bmad.yaml)
- [ ] Aucune perte de données mémoire
- [ ] Le projet migré passe `bmad doctor`
- [ ] `--dry-run` n'écrit rien

---

### EP15 — CI/CD, Documentation, et Distribution

> **Objectif** : Préparer la release publique : documentation complète, CI robuste, publication PyPI.
> **Critère de Done épic** : `pip install bmad-kit` fonctionne depuis PyPI. Docs déployées.

#### V3-EP15-S01 — Documentation complète [XL]

**Description** : Réécrire la documentation pour couvrir les nouveaux concepts v3 et la distribuer via un site.

**Tâches :**
- [ ] Mettre à jour `README.md` avec nouveau pitch, installation pip, quick start
- [ ] Réécrire `docs/getting-started.md` pour la v3
- [ ] Créer `docs/bmad-yaml-reference.md` : référence complète du schéma
- [ ] Créer `docs/sdk-guide.md` : guide d'utilisation du SDK Python
- [ ] Créer `docs/mcp-integration.md` : guide d'intégration MCP
- [ ] Créer `docs/migration-v2-v3.md` : guide de migration
- [ ] Créer `docs/publishing-agents.md` : guide de publication d'agents
- [ ] Configurer MkDocs ou Sphinx pour générer un site de documentation
- [ ] Mettre à jour `CONTRIBUTING.md`
- [ ] Ajouter docstrings manquants dans tous les modules publics

**Critères d'acceptation :**
- [ ] Chaque concept v3 est documenté
- [ ] Chaque commande CLI est documentée avec exemples
- [ ] Le SDK a des exemples d'utilisation
- [ ] Le site de doc se build sans erreur

---

#### V3-EP15-S02 — Publication PyPI + GitHub Release [M]

**Description** : Configurer le workflow de publication sur PyPI et les releases GitHub.

**Tâches :**
- [ ] Workflow GitHub Actions pour release automatique sur tag
- [ ] Build du package avec hatch
- [ ] Publication sur PyPI (configuré avec trusted publishers)
- [ ] Publication sur TestPyPI d'abord pour validation
- [ ] Release notes automatiques depuis CHANGELOG.md
- [ ] Vérifier `pip install bmad-kit` depuis PyPI

**Critères d'acceptation :**
- [ ] `pip install bmad-kit` installe la dernière version depuis PyPI
- [ ] `uvx bmad --version` fonctionne sans installation préalable
- [ ] Release notes formatées sur GitHub

---

#### V3-EP15-S03 — Auto-completion shell [S]

**Description** : Générer et distribuer les scripts d'auto-completion pour Bash, Zsh, et Fish.

**Tâches :**
- [ ] Commande `bmad --install-completion` (built-in Typer)
- [ ] Scripts de completion inclus dans le package
- [ ] Documentation dans le getting-started
- [ ] Tests

**Critères d'acceptation :**
- [ ] Tab-completion fonctionne pour toutes les commandes et options
- [ ] Support Bash, Zsh, et Fish

---

## Résumé des Estimations

| Epic | Stories | Estimation totale | Phase |
|---|---|---|---|
| **EP01** — Package Python | 3 | **4-5 jours** | Phase 0 |
| **EP02** — Configuration | 4 | **6-8 jours** | Phase 0 |
| **EP03** — Tests Infra | 2 | **3-4 jours** | Phase 0 |
| **EP04** — Core Library | 5 | **15-20 jours** | Phase 1 |
| **EP05** — Tools Migration | 5 | **20-30 jours** | Phase 1 |
| **EP06** — Memory System | 3 | **5-7 jours** | Phase 1 |
| **EP07** — CLI Typer | 6 | **12-18 jours** | Phase 2 |
| **EP08** — MCP Server | 2 | **6-8 jours** | Phase 2 |
| **EP09** — bmad.yaml Lifecycle | 2 | **5-7 jours** | Phase 2 |
| **EP10** — Registry Local | 2 | **3-4 jours** | Phase 3 |
| **EP11** — Registry Communautaire | 2 | **5-8 jours** | Phase 3 (v3.1) |
| **EP13** — Merge Engine | 3 | **8-10 jours** | Phase 3 |
| **EP14** — Migration v2→v3 | 1 | **3-5 jours** | Phase 3 |
| **EP15** — CI/CD + Doc + Release | 3 | **6-10 jours** | Phase 3 |

### Total

| Phase | Jours estimés | Pourcentage |
|---|---|---|
| **Phase 0 — Scaffold** | 13-17 | ~15% |
| **Phase 1 — Extract** | 40-57 | ~45% |
| **Phase 2 — Interface** | 23-33 | ~25% |
| **Phase 3 — Platform** | 25-37 | ~15% |
| **TOTAL** | **~100-145 jours** | 100% |

> **Note** : Ces estimations supposent un agent IA performant (Claude Opus 4, GPT-4o niveau) comme exécutant principal. Avec un agent expérimenté sur le codebase, les Phases 0 et 1 devraient être réalisables en ~30-40 jours effectifs.

---

## Ordonnancement recommandé

```
Semaine 1-2 :  EP01 + EP02 + EP03        (scaffold — parallélisable)
Semaine 3-5 :  EP04                        (core lib — critique)
Semaine 5-8 :  EP05 + EP06                (extract — parallélisable)
Semaine 8-10:  EP07 + EP08                (interfaces — parallélisable)
Semaine 10-11: EP09                        (bmad.yaml lifecycle)
Semaine 11-13: EP13 + EP14                (merge + migration)
Semaine 13-14: EP10 + EP15                (registry + release)
Semaine 15+ :  EP11                        (communautaire — v3.1)
```

---

## Glossaire

| Terme | Définition |
|---|---|
| **bmad.yaml** | Fichier déclaratif à la racine du projet, source unique de vérité pour la config BMAD |
| **Archétype** | Template d'équipe pré-configurée (minimal, web-app, infra-ops, etc.) |
| **Module** | Fonctionnalité BMAD installable séparément (memory, completion-contract, context-router) |
| **Tool** | Un des 48 outils Python (context-router, agent-forge, etc.) |
| **Registry** | Catalogue d'agents et modules (local = built-in, remote = PyPI/GitHub) |
| **Merge** | Fusion non-destructive de BMAD dans un projet existant |
| **Eject** | Transformation de l'installation BMAD en fichiers statiques autonomes |
| **MCP** | Model Context Protocol — protocole pour exposer des tools aux LLMs |

---

*Document rédigé le 3 mars 2026 — 42 stories, 15 épics, 4 phases*
