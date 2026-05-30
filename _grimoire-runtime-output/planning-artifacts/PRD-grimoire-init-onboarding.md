# PRD — grimoire init : Onboarding Experience

> **Statut** : Draft v1 — 24 mars 2026
> **Auteur** : John (PM)
> **Destinataire** : Guilhem (expert)
> **Contexte** : `grimoire init .` produit un YAML vide — pas d'agents, pas de framework. CASSÉ.
> **Inputs** : ADR-004 (Winston), Brainstorm UX (4 lots), Brainstorm Innovation (P1-P8), Scanner existant (17 stacks), 9 archétypes

---

## 1. Problem Statement

> **Qui ne dort pas à cause de ce problème ?** Tout développeur qui fait `pip install grimoire-kit && grimoire init .` et obtient un fichier YAML vide avec 3 répertoires. Le bash produit un projet vivant avec 18+ agents, un framework complet, des hooks git, des manifests. Le Python produit un cadavre.

**Job-to-be-Done** : *Quand j'initialise Grimoire sur mon projet, je veux obtenir un environnement agentique opérationnel en une commande, pour pouvoir immédiatement commencer à travailler avec des agents adaptés à mon stack.*

**Écart mesuré** :
- Bash : ~45 secondes → projet vivant (agents + framework + hooks + manifests)
- Python actuel : ~2 secondes → fichier YAML + 3 dossiers vides
- **Delta de valeur** : 100% de la valeur est dans le bash, 0% dans le Python

---

## 2. User Segments

| Segment | Profil | Job-to-be-Done | Volume estimé |
|---|---|---|---|
| **S1 — First-timer** | Dev curieux, découvre Grimoire via `pip install` | "Je veux voir ce que ça fait en 30 secondes" | 70% |
| **S2 — Migrateur bash** | Utilisateur actuel du bash, passe à pip | "Je veux la même chose, mais en mieux" | 15% |
| **S3 — CI/CD engineer** | Intègre Grimoire dans un pipeline | "Je veux un init scriptable, déterministe, sans prompt" | 8% |
| **S4 — Team lead** | Onboarde son équipe sur un projet Grimoire existant | "Mes devs doivent être opérationnels en 2 minutes" | 5% |
| **S5 — Monorepo architect** | Projet multi-services | "Je veux Grimoire ciblé par service, pas un blob global" | 2% |

---

## 3. Feature Map Exhaustive (MoSCoW)

### 3.1 Must-Have — L'install est cassée sans ça

| ID | Feature | Description | Segment cible |
|---|---|---|---|
| **F01** | Stack Detection intégrée | `grimoire init .` scanne le projet et détecte les stacks automatiquement via `StackScanner` existant | S1, S2, S3 |
| **F02** | Archetype auto-resolution | Le stack détecté est mappé vers l'archétype optimal via `ArchetypeResolver` | S1, S2, S3 |
| **F03** | Full scaffold | Copie complète : répertoires, agents meta, agents archétype, agents stack, framework, templates mémoire, manifests | S1, S2, S3, S4 |
| **F04** | project-context.yaml riche | Template rendu avec : nom, archétype, backend, stacks détectés, agents installés, version kit | S1, S2, S3 |
| **F05** | copilot-instructions.md généré | Instructions IDE auto-générées depuis l'archétype et les agents installés | S1, S2 |
| **F06** | Data packaging (framework dans le wheel) | `force-include` du framework complet dans le wheel pip pour que le scaffolder ait les fichiers source | S1, S2, S3, S4, S5 |
| **F07** | Mode express (`--auto`) | Détection + résolution + scaffold sans question — une seule commande | S1, S3 |
| **F08** | Mode scriptable (`-o json -y`) | Sortie JSON, pas de prompt, exit code exploitable — CI/CD first | S3 |
| **F09** | `--dry-run` enrichi | Affiche le plan complet (fichiers, agents, répertoires) sans écrire — pas juste 3 lignes | S2, S3 |
| **F10** | Idempotence (`--force`) | Relancer `init --force` ne casse pas un projet existant — merge intelligent | S2, S4 |

### 3.2 Should-Have — Différenciation forte

| ID | Feature | Description | Segment cible |
|---|---|---|---|
| **F11** | Mode interactif (Rich prompts) | Wizard avec présentation du scan, choix d'archétype, confirmation du plan avant exécution | S1 |
| **F12** | Descriptions d'archétypes riches | Chaque archétype expliqué avec ses agents, ses traits, ses cas d'usage — pas juste un nom | S1 |
| **F13** | Détection backend mémoire | Probe localhost pour Qdrant/Ollama, sélection automatique avec fallback `local` | S1, S2 |
| **F14** | Rich summary post-init | Résumé coloré : agents installés, stacks détectés, prochaines étapes suggérées | S1, S2 |
| **F15** | Next steps contextuels | Messages post-init adaptés à l'archétype ("Tu as web-app → lance `grimoire party` pour démarrer ta première story") | S1 |
| **F16** | Git hooks installation | Si `.git/` présent, installe automatiquement les hooks Grimoire (cc-verify, sil-collect) | S1, S2 |
| **F17** | Agent manifest généré | `agent-manifest.csv` auto-généré listant tous les agents installés et leur source | S2, S4 |
| **F18** | Scan confidence display | Affiche le score de confiance par stack ("python 95%, docker 70%, terraform 80%") pour transparence | S1, S2 |
| **F19** | Migration bash → Python | Détecte un projet initialisé par le bash (`installer: "bash-script"`) et migre proprement | S2 |
| **F20** | Archétype override partiel | `grimoire init . --auto --add-agent security-expert` — ajouter des agents hors archétype | S2, S5 |

### 3.3 Could-Have — Nice polish

| ID | Feature | Description | Segment cible |
|---|---|---|---|
| **F21** | `grimoire add archetype <name>` | Ajouter un archétype secondaire à un projet existant sans réinit | S5 |
| **F22** | `grimoire init --from-config config.yaml` | Init depuis un fichier de config pré-existant (onboarding équipe) | S4 |
| **F23** | Monorepo support (`grimoire init services/api`) | Init ciblé sur un sous-répertoire avec isolation de contexte | S5 |
| **F24** | Health score post-init | Après scaffold, lancer un mini `doctor` pour confirmer que tout est sain | S1, S2 |
| **F25** | Template custom directory | `--templates /path/to/custom/` — utiliser des templates d'entreprise | S4 |
| **F26** | IDE detection + config gen | Détecter VS Code/Cursor et générer les bons `.vscode/settings.json` + extensions recommandées | S1 |
| **F27** | Progress bar (Rich) | Barre de progression pendant le scaffold (pas bloquant, mais UX premium) | S1 |
| **F28** | `grimoire clone-config` | Copier la config d'un projet existant vers un nouveau (onboarding rapide) | S4 |
| **F29** | Changelog post-init | Générer un `_grimoire/INIT_LOG.md` traçant exactement ce qui a été fait | S2, S3 |
| **F30** | Rollback (`grimoire init --undo`) | Défaire un init récent en supprimant les fichiers créés (via le log F29) | S1 |

### 3.4 Won't-Have v1 — Explicitement hors scope

| ID | Feature | Raison d'exclusion |
|---|---|---|
| **W01** | GUI / TUI wizard plein écran | Over-engineering — Rich prompts suffisent. Textual plus tard si demande. |
| **W02** | Remote init (SSH/Docker) | Complexité réseau, sécurité, hors cas d'usage principal |
| **W03** | Init depuis un repo template GitHub | Dépendance GitHub API, complexité auth, `git clone` suffit |
| **W04** | Auto-update des agents post-init | Grimoire `upgrade` existe déjà — pas dans init |
| **W05** | Plugin system pour archétypes tiers | Convention-over-configuration via filesystem suffit pour v1 |
| **W06** | Init dans un container Docker | `docker run grimoire init` — hors scope, le user mount son volume |
| **W07** | Multi-LLM routing dans l'init | Pas lié à l'onboarding — c'est du runtime Intelligence Layer |
| **W08** | Questionnaire "quel archétype pour moi ?" | Le scanner le fait automatiquement — pas besoin de questionnaire |

---

## 4. User Stories Détaillées

### Must-Have Stories

---

#### US-01 : Stack Detection automatique

**En tant que** développeur qui fait `grimoire init .`,
**je veux que** Grimoire détecte automatiquement les technologies de mon projet,
**afin de** recevoir un setup adapté sans avoir à spécifier manuellement mon stack.

**Acceptance Criteria** :
- [ ] AC1 : `grimoire init . --auto` appelle `StackScanner.scan()` sur le répertoire cible
- [ ] AC2 : Les 17 stacks supportés sont détectés (python, js, ts, go, rust, java, ruby, c#, docker, terraform, kubernetes, ansible, react, vue, django, fastapi, flutter)
- [ ] AC3 : Chaque stack détecté a un score de confiance (0.0–1.0) et une liste d'evidence (fichiers trouvés)
- [ ] AC4 : Le scan respecte `.gitignore` et les dossiers exclus (`node_modules`, `.venv`, etc.)
- [ ] AC5 : Le scan s'exécute en < 2 secondes sur un projet de 10 000 fichiers
- [ ] AC6 : Projet vide → aucun stack détecté → archétype `minimal` par défaut

---

#### US-02 : Résolution automatique stack → archétype

**En tant que** développeur,
**je veux que** les stacks détectés soient automatiquement mappés vers l'archétype optimal,
**afin de** recevoir les bons agents sans devoir connaître les 9 archétypes.

**Acceptance Criteria** :
- [ ] AC1 : Le mapping est déclaratif (données, pas code) — modifiable sans toucher au code
- [ ] AC2 : `terraform` OU `kubernetes` OU `ansible` → `infra-ops`
- [ ] AC3 : `react`/`vue` + backend (`python`/`go`/`ts`) → `web-app`
- [ ] AC4 : `python` seul avec `fastapi`/`django` → `web-app`
- [ ] AC5 : Aucun match → `minimal`
- [ ] AC6 : Le `ResolvedArchetype` inclut : archétype, agents stack, agents features, raison textuelle
- [ ] AC7 : L'utilisateur peut override avec `--archetype web-app` (le flag l'emporte toujours)

---

#### US-03 : Scaffold complet du projet

**En tant que** développeur,
**je veux que** `grimoire init .` crée un projet Grimoire opérationnel complet,
**afin de** pouvoir commencer à travailler avec les agents immédiatement.

**Acceptance Criteria** :
- [ ] AC1 : Crée la structure `_grimoire/` complète : `_config/`, `_config/custom/agents/`, `_memory/`, `team-*/` selon archétype
- [ ] AC2 : Copie les agents meta (6 : atlas, sentinel, mnemo, concierge, navigator, optimizer)
- [ ] AC3 : Copie les agents spécifiques à l'archétype sélectionné
- [ ] AC4 : Copie les agents stack conditionnels (ex: `python-expert.md` si python détecté)
- [ ] AC5 : Copie le framework complet (agent-base.md, cc-verify.sh, sil-collect.sh, mémoire, hooks)
- [ ] AC6 : Render `project-context.yaml` avec toutes les valeurs résolues
- [ ] AC7 : Render `copilot-instructions.md` adapté aux agents installés
- [ ] AC8 : Render configs mémoire (`memory-config.yaml`, `shared-context.md`)
- [ ] AC9 : Génère `agent-manifest.csv` listant tous les agents
- [ ] AC10 : Le résultat est **identique en sortie** au bash `grimoire-init.sh` pour le même input

---

#### US-04 : Mode express (zero-question)

**En tant que** développeur pressé ou script CI,
**je veux** `grimoire init . --auto -y`,
**afin de** obtenir un projet initialisé sans aucune interaction.

**Acceptance Criteria** :
- [ ] AC1 : Aucun prompt interactif en mode `--auto`
- [ ] AC2 : Détection stack → résolution archétype → scaffold enchaînés automatiquement
- [ ] AC3 : Valeurs par défaut appliquées : nom = nom du répertoire, langue = English, backend = auto-détecté ou `local`
- [ ] AC4 : Exit code 0 = succès, 1 = erreur avec message JSON si `-o json`
- [ ] AC5 : Durée totale < 5 secondes sur un projet typique

---

#### US-05 : Mode scriptable CI/CD

**En tant qu'** ingénieur CI/CD,
**je veux** `grimoire init . --auto -y -o json`,
**afin d'** intégrer l'initialisation dans un pipeline avec parsing de sortie.

**Acceptance Criteria** :
- [ ] AC1 : `-o json` produit un JSON valide sur stdout avec `ok`, `project`, `archetype`, `agents_installed`, `directories_created`, `warnings`
- [ ] AC2 : Aucune sortie Rich/ANSI en mode JSON
- [ ] AC3 : Les erreurs sont aussi en JSON : `{"ok": false, "error": "...", "code": "E001"}`
- [ ] AC4 : `--dry-run -o json` retourne le plan en JSON sans écrire
- [ ] AC5 : Compatible avec `jq`, `yq`, et parsing standard

---

#### US-06 : Dry-run enrichi

**En tant que** développeur prudent,
**je veux** `grimoire init . --auto --dry-run`,
**afin de** voir exactement ce qui va être créé avant d'écrire quoi que ce soit.

**Acceptance Criteria** :
- [ ] AC1 : Affiche la liste complète des répertoires à créer
- [ ] AC2 : Affiche la liste des fichiers à copier (agents, framework) avec source et destination
- [ ] AC3 : Affiche les templates à render avec les variables résolues
- [ ] AC4 : Affiche les stacks détectés et l'archétype résolu
- [ ] AC5 : Affiche le nombre total d'opérations ("12 dirs, 35 files, 4 templates")
- [ ] AC6 : Aucune écriture filesystem — vérifiable par diff avant/après

---

#### US-07 : Idempotence et --force

**En tant que** développeur qui relance `init` sur un projet existant,
**je veux que** `grimoire init . --force` mette à jour sans détruire mes customisations,
**afin de** pouvoir upgrader mon setup sans perdre mon travail.

**Acceptance Criteria** :
- [ ] AC1 : Sans `--force`, une erreur claire est affichée si `project-context.yaml` existe déjà
- [ ] AC2 : Avec `--force` : les fichiers framework sont mis à jour (overwrite)
- [ ] AC3 : Avec `--force` : les fichiers dans `_config/custom/` ne sont JAMAIS overwrite (customisations protégées)
- [ ] AC4 : Avec `--force` : les fichiers mémoire (`_memory/`) ne sont JAMAIS overwrite
- [ ] AC5 : Un backup est créé avant le force-overwrite : `project-context.yaml.bak`
- [ ] AC6 : Le résumé post-force indique ce qui a été mis à jour vs préservé

---

#### US-08 : Data packaging (framework dans le wheel)

**En tant que** développeur qui installe via `pip install grimoire-kit`,
**je veux que** le wheel contienne le framework complet,
**afin que** `grimoire init` ait les fichiers source pour le scaffold.

**Acceptance Criteria** :
- [ ] AC1 : `pyproject.toml` inclut `framework/` via `force-include` dans le wheel
- [ ] AC2 : `importlib.resources.files("grimoire.data")` retourne un chemin vers framework bundlé
- [ ] AC3 : En editable install (`pip install -e .`), fallback vers `framework/` à la racine du repo
- [ ] AC4 : Les fichiers `.sh`, `.md`, `.yaml`, `.py` du framework sont tous inclus
- [ ] AC5 : La taille du wheel augmente de < 500 Ko (framework complet)
- [ ] AC6 : `__pycache__` et `.pyc` exclus du wheel

---

### Should-Have Stories

---

#### US-11 : Mode interactif wizard

**En tant que** développeur qui découvre Grimoire pour la première fois,
**je veux** un wizard interactif qui me guide à travers les choix,
**afin de** comprendre ce que fait chaque option avant de m'engager.

**Acceptance Criteria** :
- [ ] AC1 : `grimoire init .` (sans `--auto`) lance le mode interactif
- [ ] AC2 : Affiche le résultat du scan avec scores de confiance par stack
- [ ] AC3 : Propose l'archétype recommandé avec alternatives et descriptions
- [ ] AC4 : Permet de choisir le backend mémoire avec détection auto
- [ ] AC5 : Affiche le plan complet avant confirmation
- [ ] AC6 : Un seul `[Y/n]` final pour confirmer — pas 15 questions

---

#### US-12 : Descriptions d'archétypes riches

**En tant que** développeur en mode interactif,
**je veux** voir une description détaillée de chaque archétype proposé,
**afin de** faire un choix éclairé sans lire la documentation.

**Acceptance Criteria** :
- [ ] AC1 : Chaque archétype affiché avec : nom, icône, description (1 ligne), nombre d'agents, traits principaux
- [ ] AC2 : Les données viennent du `archetype.dna.yaml` (source de vérité unique)
- [ ] AC3 : L'archétype recommandé est marqué visuellement (⭐ ou `[recommended]`)
- [ ] AC4 : `grimoire init --list-archetypes` affiche tous les 9 archétypes disponibles

---

#### US-13 : Détection backend mémoire

**En tant que** développeur avec Qdrant ou Ollama installé localement,
**je veux que** Grimoire détecte automatiquement mes services mémoire,
**afin d'** obtenir le backend optimal sans configuration manuelle.

**Acceptance Criteria** :
- [ ] AC1 : Probe HTTP vers `localhost:6333/healthz` (Qdrant) et `localhost:11434/api/tags` (Ollama)
- [ ] AC2 : Timeout de 2 secondes par probe, non bloquant
- [ ] AC3 : Qdrant trouvé → `qdrant-local`, Ollama trouvé → `ollama`, rien → `local`
- [ ] AC4 : `--backend local` force le backend sans probe
- [ ] AC5 : En mode `--auto`, pas de message si rien trouvé — fallback silencieux
- [ ] AC6 : URLs hardcodées (localhost uniquement) — pas de SSRF possible

---

#### US-14 : Rich summary + next steps

**En tant que** développeur qui vient de faire `grimoire init .`,
**je veux** un résumé visuel riche avec les prochaines étapes concrètes,
**afin de** savoir immédiatement quoi faire ensuite.

**Acceptance Criteria** :
- [ ] AC1 : Panel Rich avec : nom du projet, archétype, stacks détectés, backend, nombre d'agents
- [ ] AC2 : Tree Rich des répertoires créés (collapsé, pas 50 lignes)
- [ ] AC3 : Section "Next Steps" avec 3–5 actions concrètes adaptées à l'archétype
- [ ] AC4 : Ex: archétype `web-app` → "1. `grimoire party` pour ta première story, 2. Configure tes tests dans `copilot-instructions.md`"
- [ ] AC5 : Lien vers la doc en ligne si disponible

---

#### US-15 : Migration bash → Python

**En tant que** utilisateur existant du bash `grimoire-init.sh`,
**je veux** que `grimoire init . --force` migre proprement mon projet,
**afin de** passer au Python sans perdre mes customisations ni mes données mémoire.

**Acceptance Criteria** :
- [ ] AC1 : Détecte `installer: "bash-script"` dans `project-context.yaml` existant
- [ ] AC2 : Met à jour `installer: "python-cli"` + `grimoire_kit_version: "X.Y.Z"`
- [ ] AC3 : Préserve `_grimoire/_memory/` intégralement (jamais touché)
- [ ] AC4 : Préserve `_grimoire/_config/custom/` intégralement
- [ ] AC5 : Met à jour les agents framework et archétype (overwrite des fichiers non-custom)
- [ ] AC6 : Affiche un diff résumé de ce qui a changé
- [ ] AC7 : Log de migration dans `_grimoire/MIGRATION_LOG.md`

---

#### US-16 : Scan confidence display

**En tant que** développeur en mode interactif,
**je veux** voir le score de confiance et les preuves pour chaque stack détecté,
**afin de** corriger les faux positifs avant le scaffold.

**Acceptance Criteria** :
- [ ] AC1 : Tableau Rich affichant stack, score (%), fichiers evidence
- [ ] AC2 : Stacks triés par score décroissant
- [ ] AC3 : Seuil de confiance visuel : vert > 70%, jaune 40–70%, rouge < 40%
- [ ] AC4 : Option d'exclure un stack détecté en interactif ("Exclure terraform ? [y/N]")

---

#### US-17 : Git hooks installation

**En tant que** développeur sur un projet git,
**je veux que** `grimoire init` installe automatiquement les hooks git,
**afin d'** avoir les guardrails CC-verify et SIL-collect dès le premier commit.

**Acceptance Criteria** :
- [ ] AC1 : Si `.git/` présent, copie `cc-verify.sh` dans `.git/hooks/pre-commit` (ou `.husky/` si détecté)
- [ ] AC2 : Si hooks existants, ne pas overwrite — merge ou warning
- [ ] AC3 : Si pas de `.git/`, skip silencieusement (pas d'erreur)
- [ ] AC4 : `--no-hooks` pour opt-out explicite

---

## 5. Scénarios d'Utilisation Avancés

### 5.1 Réinstallation sur un projet existant

```bash
# Le dev a déjà un projet Grimoire initialisé il y a 3 mois
# Il veut upgrader vers les derniers agents/framework
grimoire init . --force --auto

# Comportement attendu :
# 1. Détecte installer existant (bash ou python)
# 2. Préserve _memory/ et _config/custom/
# 3. Met à jour framework, agents archétype/meta/stack
# 4. Met à jour project-context.yaml (garde les champs custom, update version)
# 5. Affiche diff des changements
```

### 5.2 Migration bash → Python

```bash
# Projet initié avec grimoire-init.sh, maintenant grimoire-kit est sur pip
grimoire init . --force

# Comportement attendu :
# 1. Lit project-context.yaml → voit installer: "bash-script"
# 2. Mode migration activé automatiquement
# 3. Compare structure existante vs attendue
# 4. Update fichiers framework (agit comme un upgrade)
# 5. Marque installer: "python-cli" + version
# 6. Crée MIGRATION_LOG.md
```

### 5.3 Utilisation en CI/CD

```yaml
# GitHub Actions
jobs:
  init-grimoire:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install grimoire-kit
      - run: grimoire init . --auto -y -o json > grimoire-init.json
      - run: |
          ARCHETYPE=$(jq -r '.archetype' grimoire-init.json)
          echo "Archétype résolu : $ARCHETYPE"
          # Valider que l'archétype est celui attendu
          test "$ARCHETYPE" = "web-app"
```

### 5.4 Ajout d'archétype à un projet existant

```bash
# Le projet est initialisé en web-app
# Le dev ajoute de l'infra (Terraform) et veut les agents correspondants
grimoire add archetype infra-ops

# Comportement attendu :
# 1. Ne touche PAS aux agents existants
# 2. Copie les agents infra-ops en complément
# 3. Met à jour l'agent-manifest.csv
# 4. Ajoute les traits infra-ops dans project-context.yaml
# 5. Note dans shared-context.md les nouvelles capacités
```

### 5.5 Changement de backend mémoire

```bash
# Initialement en local, le dev installe Qdrant
grimoire setup --backend qdrant-local

# Utilise la commande setup existante (cmd_setup.py)
# Pas dans le scope du init — mais l'init doit bien détecter pour le premier setup
```

### 5.6 Onboarding nouveau dev sur un projet existant

```bash
# Le lead a déjà initialisé le projet et pushé _grimoire/ sur git
# Le nouveau dev clone le repo
git clone git@github.com:company/my-project.git
cd my-project

# Option A — Le projet est complet dans git (recommandé)
grimoire doctor .   # Vérifie que tout est sain
grimoire setup --sync  # Synchronise les configs locales

# Option B — Le projet a un project-context.yaml mais pas de _grimoire/
grimoire init . --from-config project-context.yaml
# Scaffold depuis la config existante sans re-scanner
```

### 5.7 Monorepo avec plusieurs services

```bash
my-monorepo/
├── services/
│   ├── api/        # Python FastAPI
│   ├── frontend/   # React TypeScript
│   └── infra/      # Terraform
├── libs/
│   └── shared/     # Python library
└── project-context.yaml  # Global

# Approche v1 : init au root, le scanner détecte tout
grimoire init . --auto
# → Résout web-app (react + python), installe agents pour les deux stacks

# Approche future (F23) : init par service
grimoire init services/api --auto
grimoire init services/frontend --auto
grimoire init services/infra --auto
```

---

## 6. Success Metrics (KPIs)

### 6.1 Métriques d'adoption

| KPI | Cible v1 | Mesure |
|---|---|---|
| **Time-to-first-agent** | < 60 secondes (pip install + init + premier agent actif) | Chrono E2E dans les tests |
| **Init success rate** | > 95% des `grimoire init` sans erreur | Telemetry opt-in ou issue tracker |
| **Archetype auto-match accuracy** | > 85% des users acceptent l'archétype suggéré | Log du mode interactif (accept vs override) |
| **Parité bash ↔ Python** | 100% des fichiers de sortie identiques | Tests diff E2E automatisés |
| **Zero-config ratio** | > 60% des users utilisent `--auto` sans override | Usage logs |

### 6.2 Métriques de qualité

| KPI | Cible v1 | Mesure |
|---|---|---|
| **Doctor pass rate post-init** | 100% des projets passent `doctor` après `init` | Test automatisé |
| **Scaffold completeness** | 100% des agents archétype installés | Vérification par manifest |
| **Regression count bash→python** | 0 régression — le Python fait au minimum autant que le bash | Tests de comparaison |
| **Rollback needed** | < 2% des init nécessitent un rollback | Issue tracking |

### 6.3 Métriques d'engagement post-init

| KPI | Cible v1 | Mesure |
|---|---|---|
| **Commande suivante dans les 5 min** | > 50% des users lancent une commande Grimoire dans les 5 min après init | Usage logs |
| **Retention J+7** | > 30% des users ont lancé au moins 3 commandes Grimoire en 7 jours | Usage logs |
| **Issue "init cassé"** | 0 issue GitHub avec label "init" non résolue en 48h | Issue tracker |

---

## 7. Risques Produit

| # | Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|---|
| **R1** | **Confusion naming** : l'utilisateur ne sait pas quoi faire entre `grimoire init`, `grimoire setup`, `grimoire doctor` | Haute | Moyen | Help text clair, message post-init qui guide, aide contextuelle |
| **R2** | **Overengineering wizard** : trop de questions en mode interactif tue l'expérience | Moyenne | Haut | Max 1 question (confirmer le plan) — tout le reste auto-détecté |
| **R3** | **Faux positifs scanner** : un `Dockerfile` de CI fait croire à un projet Docker | Moyenne | Faible | Seuil de confiance + possibilité d'exclure en interactif |
| **R4** | **Backward compat** : casser les projets bash existants au moment du force-init Python | Haute | Haut | Migration path explicite, backup automatique, MIGRATION_LOG |
| **R5** | **Wheel trop gros** : le framework + archetypes + agents gonflent le package pip | Faible | Moyen | Audit taille à chaque release, exclure `__pycache__`, `.pyc` |
| **R6** | **Adoption lente** : les users bash préfèrent rester sur le bash "qui marche" | Moyenne | Moyen | Feature parity d'abord, puis valeur ajoutée (interactif, dry-run enrichi) |
| **R7** | **Monorepo confusion** : init au root ne convient pas, mais init par service pas dispo en v1 | Faible | Moyen | Documenter la stratégie recommandée, roadmap publique |
| **R8** | **Documentation insuffisante** : l'init marche mais personne ne sait quoi en faire | Moyenne | Haut | Next steps contextuels (F15), lien vers getting-started, exemples |
| **R9** | **Archétype inadéquat** : le mapping auto choisit mal et l'utilisateur ne sait pas corriger | Faible | Moyen | Raison textuelle dans le résumé, `--archetype` pour override, `add archetype` en v1.1 |
| **R10** | **Dépendance au scanner** : si le scanner a un bug, tout l'init est faux | Moyenne | Haut | Scanner testé unitairement à 100%, fallback `minimal` robuste |

---

## 8. Lotissement Enrichi — Milestones

### Milestone 0 — URGENCE : Init fonctionnel (MVP absolu)

> **Critère de "done"** : `grimoire init . --auto` produit un projet identique au bash.
> **Deadline interne** : Priorité immédiate — c'est le bug #1.

| Livrable | Features | Effort estimé |
|---|---|---|
| `core/archetype_resolver.py` + tests | F02 | 2–3j |
| `data/__init__.py` + pyproject.toml force-include | F06 | 1–2j |
| `core/scaffold.py` + plan/execute + tests | F03 | 3–4j |
| Remplacement de `init()` dans `app.py` → `cmd_init.py` | F01, F04, F05, F07, F08, F09 | 2–3j |
| Tests d'intégration (parité bash) | — | 2j |
| **Total** | **F01–F10** | **~12j** |

**Definition of Done** :
- [ ] `grimoire init . --auto` détecte le stack et scaffold le projet complet
- [ ] `grimoire init . --dry-run` affiche le plan complet
- [ ] `-o json` produit un JSON valide
- [ ] `--force` sur projet existant ne casse pas les custom
- [ ] Parité vérifiée par tests diff E2E vs bash
- [ ] `grimoire doctor` passe à 100% sur le résultat

---

### Milestone 1 — UX Premium : Mode interactif + polish

> **Critère de "done"** : Un premier utilisateur peut faire `grimoire init .` et être guidé de A à Z.

| Livrable | Features | Effort estimé |
|---|---|---|
| Mode interactif Rich | F11, F12, F18 | 3–4j |
| Détection backend mémoire | F13 | 1j |
| Rich summary + next steps | F14, F15 | 2j |
| Git hooks installation | F16, F17 | 1–2j |
| **Total** | **F11–F18** | **~8j** |

**Definition of Done** :
- [ ] Le wizard ne pose qu'une question de confirmation
- [ ] Les 9 archétypes ont des descriptions lisibles depuis `dna.yaml`
- [ ] Les next steps sont adaptés à l'archétype
- [ ] Les hooks git sont installés si `.git/` présent
- [ ] Qdrant/Ollama détectés automatiquement

---

### Milestone 2 — Backward Compat : Migration + upgrade path

> **Critère de "done"** : Un utilisateur bash peut migrer proprement vers Python.

| Livrable | Features | Effort estimé |
|---|---|---|
| Détection installer existant + migration | F19 | 2–3j |
| Archetype override / add-agent | F20 | 2j |
| Migration log + backup | — | 1j |
| **Total** | **F19–F20** | **~5j** |

**Definition of Done** :
- [ ] `grimoire init . --force` sur un projet bash migre correctement
- [ ] `_memory/` et `_config/custom/` jamais touchés
- [ ] `MIGRATION_LOG.md` créé avec diff
- [ ] Tests E2E avec un projet bash de référence

---

### Milestone 3 — Power Features : add archetype, monorepo, from-config

> **Critère de "done"** : Les cas d'usage avancés sont couverts.

| Livrable | Features | Effort estimé |
|---|---|---|
| `grimoire add archetype` | F21 | 3j |
| `grimoire init --from-config` | F22 | 2j |
| Monorepo support basique | F23 | 3j |
| Health check post-init | F24 | 1j |
| **Total** | **F21–F24** | **~9j** |

**Definition of Done** :
- [ ] `add archetype` sur projet existant ne casse rien
- [ ] `--from-config` scaffold depuis un YAML existant
- [ ] Init ciblé sur sous-répertoire fonctionne
- [ ] `doctor` automatique post-init optionnel

---

### Milestone 4 — Polish & Enterprise : templates custom, IDE detection

> **Cible** : v2 — pas urgent.

| Livrable | Features | Effort estimé |
|---|---|---|
| Templates custom d'entreprise | F25 | 2j |
| IDE detection + config gen | F26 | 2–3j |
| Progress bar | F27 | 0.5j |
| Clone-config | F28 | 1j |
| Init log + rollback | F29, F30 | 2j |
| **Total** | **F25–F30** | **~8j** |

---

### Vue chronologique

```
      M0 (MVP)         M1 (UX)        M2 (Compat)     M3 (Power)      M4 (v2)
  ──────────────── ──────────────── ──────────────── ──────────────── ────────────
  F01-F10          F11-F18          F19-F20          F21-F24          F25-F30
  ~12j             ~8j              ~5j              ~9j              ~8j
  ███████████████  ████████████     ██████           ████████████     ████████████

  BLOQUANT         DIFFÉRENCIANT    CONFIANCE        AVANCÉ           POLISH
  "ça marche"      "c'est beau"     "ça migre"       "ça scale"       "c'est pro"
```

---

## 9. Positionnement Concurrentiel

### 9.1 Paysage concurrentiel

| Outil | Ce qu'il fait | Où Grimoire est meilleur |
|---|---|---|
| **Copilot Workspace** (GitHub) | Setup automatique d'un projet | Limité à GitHub, pas d'agents persistants, pas d'archétypes |
| **Cursor init** | Auto-configure .cursorrules | Mono-IDE, pas de mémoire, pas de framework agentique |
| **Aider** | CLI dev assistant | Pas de scaffold, pas d'agents spécialisés, pas de mémoire projet |
| **Create React App / Vite** | Scaffold frontend | Mono-stack, pas d'agents, pas de gestion de connaissance |
| **Yeoman** | Project generator | Templates statiques, pas d'intelligence contextuelle |
| **cookiecutter** | Template-based scaffolding | Pas de détection auto, pas d'agents, pas de runtime |

### 9.2 Différenciateurs uniques

1. **Stack Telepathy** : Grimoire *comprend* ton projet avant de toucher quoi que ce soit
2. **Agents adaptatifs** : pas un template statique — des agents vivants adaptés à ton stack
3. **Mémoire projet** : l'init crée un système de mémoire qui apprend et évolue
4. **Progressive disclosure** : 1 commande pour les débutants, 87+ outils pour les experts
5. **Migration-safe** : upgrade et re-init sans perdre de données

### 9.3 Tagline

> **"grimoire init — Your project already knows what it needs."**

*Variantes selon le contexte :*
- **Pitch technique** : "Grimoire scanne ton stack, choisit les bons agents, et scaffold un projet agentique opérationnel en une commande."
- **Pitch adoption** : "Stop configuring, start building. One command → 18 AI agents tailored to your project."
- **Pitch enterprise** : "Onboard your entire team's AI workflow — deterministic, scriptable, CI/CD-ready."

### 9.4 Elevator Pitch (30s)

> Tu as un projet Python + React + Docker. Tu fais `pip install grimoire-kit && grimoire init .`. En 5 secondes, Grimoire a détecté tes 3 stacks, choisi l'archétype web-app, installé 18 agents spécialisés — un pour le frontend, un pour l'API, un pour les tests, un pour la mémoire — plus un framework complet avec guardrails et hooks git. Ton projet est passé de "dossier avec du code" à "projet agentique opérationnel". Tout ça, en une commande, sans configuration.

---

## 10. Open Questions

| # | Question | Impact | Proposition |
|---|---|---|---|
| **Q1** | Faut-il déprécier le bash immédiatement après M0, ou le garder en parallèle pendant ~3 mois ? | Confusion si deux installers coexistent | Garder bash en mode maintenance 3 mois, deprecation warning dès M0, suppression à M2 |
| **Q2** | Le mode interactif est-il le défaut (sans flag) ou faut-il un `--interactive` explicite ? | UX first-timer vs scriptability | Interactif par défaut si TTY détecté, express par défaut sinon |
| **Q3** | Faut-il un `grimoire add archetype` ou un `grimoire init . --force --archetype infra-ops` suffit ? | Complexité vs flexibilité | Les deux : `add archetype` est cleaner, `--force` est le fallback |
| **Q4** | Comment gérer les archétypes conflictuels ? (`web-app` + `infra-ops` sur le même projet) | Agents dupliqués ? Traits contradictoires ? | Union des agents, intersection des traits, log de résolution |
| **Q5** | Faut-il supporter `grimoire init` à distance via MCP/REST ? | Cas d'usage edge (cloud IDE) | Won't-have v1 — utiliser le CLI pipe ou le SDK Python |
| **Q6** | Comment traiter le feedback d'archétype incorrect ? ("J'ai eu infra-ops mais je voulais web-app") | Si fréquent, le mapping est mauvais | Log des overrides, ajuster les seuils du resolver, ouvrir une issue template |

---

## Annexe A — Mapping complet Stack → Archétype (état actuel)

| Stacks détectés | Archétype résolu | Raison |
|---|---|---|
| `terraform` | infra-ops | IaC dominant |
| `kubernetes` | infra-ops | Orchestration dominant |
| `ansible` | infra-ops | Configuration management |
| `terraform` + `kubernetes` | infra-ops | Infra complète |
| `react` + `python` | web-app | Full-stack React + API |
| `vue` + `python` | web-app | Full-stack Vue + API |
| `react` + `go` | web-app | Full-stack React + Go API |
| `react` + `typescript` | web-app | Frontend SPA |
| `django` | web-app | Framework web Python |
| `fastapi` | web-app | API Python |
| `python` seul | minimal | Ambiguë — lib, script, API ? |
| `go` seul | minimal | Ambiguë — CLI, API, lib ? |
| `rust` seul | minimal | Ambiguë — CLI, lib, système ? |
| `java` seul | minimal | Ambiguë |
| `ruby` seul | minimal | Ambiguë |
| `c#` seul | minimal | Ambiguë |
| Aucun stack | minimal | Projet vide ou non reconnu |

## Annexe B — Comparaison Bash vs Python (état cible M0)

| Fonctionnalité | Bash (actuel) | Python M0 (cible) | Delta |
|---|---|---|---|
| Stack detection | Rudimentaire (presence-based) | Riche (scoring, evidence) | **Python meilleur** |
| Archétype auto | Heuristiques codées en dur | Resolver déclaratif extensible | **Python meilleur** |
| Scaffold complet | Oui (~3200 lignes bash) | Oui (ScaffoldPlan + execute) | **Parité** |
| project-context.yaml | Template sed | Template string.Template | **Parité** |
| copilot-instructions.md | Généré | Généré | **Parité** |
| Git hooks | Manuel (`cp`) | Automatique avec détection | **Python meilleur** |
| Mode interactif | `read -p` basique | Rich prompts (M1) | **Python meilleur** |
| Dry-run | Non existant | `--dry-run` complet | **Python meilleur** |
| JSON output | Non existant | `-o json` complet | **Python meilleur** |
| CI/CD compatible | Partiellement (`-y`) | Nativement (`-o json -y`) | **Python meilleur** |
| Windows | Non supporté | Supporté (Python natif) | **Python meilleur** |
| Taille | ~3200 lignes, 1 fichier | ~800 lignes, 5 modules | **Python meilleur** |

---

*"Si un dev fait `grimoire init .` et ne reçoit rien d'utile, on a perdu cette personne pour toujours. Le premier init EST le produit."* — John
