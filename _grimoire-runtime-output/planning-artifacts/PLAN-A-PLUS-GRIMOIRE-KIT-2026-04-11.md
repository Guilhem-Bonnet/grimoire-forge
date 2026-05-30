# Plan A+ — Grimoire-kit Quality Roadmap

> **Objectif** : passer de **B (6.7/10)** à **A+ (≥9/10)** sur les 7 dimensions de l'audit
> **Baseline** : audit comparatif 2026-04-10, rescoring 2026-04-11 (v3.4.2)
> **Philosophie** : chaque phase inclut ses règles anti-régression — on ne monte pas sans verrouiller

---

## Scores cibles par dimension

| Dimension | Actuel | Cible A+ | Delta |
|---|---|---|---|
| Architecture | 7.0 | 9.0 | +2.0 |
| Code Quality | 6.5 | 9.0 | +2.5 |
| Test Quality | 5.0 | 9.0 | +4.0 |
| Sécurité | 6.0 | 9.5 | +3.5 |
| Build & CI | 7.0 | 9.5 | +2.5 |
| Observabilité | 7.5 | 9.0 | +1.5 |
| Documentation | 8.0 | 9.0 | +1.0 |
| **Moyenne** | **6.7** | **9.1** | **+2.4** |

---

## Phase 1 — Fondations structurelles (Architecture + Code Quality)

> **Impact** : +2.0 Architecture, +2.5 Code Quality → effet cascade sur Test Quality
> **Prérequis** : aucun

### 1.1 Split de `app.py` (2,926L → 6 modules ≤ 500L)

Le God File est la racine de tous les autres problèmes. Le découpage suit les groupes Typer déjà présents.

| Module cible | Commandes à extraire | LOC estimé |
|---|---|---|
| `cmd_workflows.py` | `workflows_list/search/show/install/prune/doctor/sync/diff` | ~450L |
| `cmd_config.py` | `config_show/get/path/set/list/edit/validate` + `diff_config/schema_cmd` | ~400L |
| `cmd_self.py` | `self_version/update/diagnose` + `completion_install/export` + `plugins_list` | ~350L |
| `cmd_history.py` | `history_cmd` + `repair` + `_log_operation` | ~300L |
| `cmd_check.py` | `check` + `validate` + `lint` | ~300L |
| `app.py` résiduel | `main/cli` entry, alias expansion, signal handlers, profiling | ≤ 500L |

**Règle anti-régression** : ajouter dans `ruff.toml` une règle custom ou un hook pre-commit :
```
# .pre-commit-config.yaml — à ajouter
- repo: local
  hooks:
    - id: file-size-guard
      name: "No Python file > 600 lines"
      entry: python scripts/check_file_size.py --max-lines 600 --paths src/
      language: python
      pass_filenames: false
```

### 1.2 Split de `mcp/server.py` (2,063L → 4 modules)

| Module cible | Contenu | LOC estimé |
|---|---|---|
| `mcp/handlers/knowledge.py` | `_knowledge_scope_*`, `_search_knowledge_file` | ~200L |
| `mcp/handlers/analysis.py` | `_analyze_path_impact`, `_collect_candidate_paths`, `_path_categories` | ~200L |
| `mcp/handlers/mcp_config.py` | `_load_mcp_config/policy`, `_classify_mcp_server`, `_infer_*` | ~250L |
| `mcp/security.py` | `_ensure_within_root`, `_resolve_path_within`, `_resolve_path` | ~50L |
| `mcp/server.py` résiduel | Registration MCP tools, entry point | ≤ 400L |

### 1.3 Traitement des `except Exception` larges (36 fichiers)

Chaque `except Exception` sans commentaire justificatif doit devenir soit :
- Une exception spécifique (`except FileNotFoundError`, `except json.JSONDecodeError`, etc.)
- Un `except Exception` avec `# noqa: BLE001 — raison explicite`

**Règle anti-régression** : activer la règle ruff `BLE001` (blind exception) dans `ruff.toml` :
```toml
# À ajouter dans [lint] select
"BLE",  # blind exception — force explicit exception types
```
Avec `per-file-ignores` pour les patterns légitimes uniquement.

---

## Phase 2 — Sécurité & CI (Security + Build & CI)

> **Impact** : +3.5 Security, +2.5 Build & CI
> **Prérequis** : Phase 1 terminée (surface réduite = audit plus propre)

### 2.1 SHA-pinning de tous les GitHub Actions

Toutes les actions utilisent actuellement des tags versionnés (`@v6`, `@v7`) — vulnérables à la compromission de tag.

Remplacements requis dans tous les workflows :
```yaml
# Avant (vulnérable)
uses: actions/checkout@v6
uses: actions/setup-python@v6
uses: astral-sh/setup-uv@v7
uses: actions/upload-artifact@v7
uses: codecov/codecov-action@v5

# Après (sûr)
uses: actions/checkout@<SHA40>  # + commentaire version
uses: actions/setup-python@<SHA40>
uses: astral-sh/setup-uv@<SHA40>
uses: actions/upload-artifact@<SHA40>
uses: codecov/codecov-action@<SHA40>
```

Outil recommandé : `pinact` ou `pin-github-actions` pour automatiser.

**Règle anti-régression** : ajouter `zizmor` ou `actionlint` en CI :
```yaml
- name: Lint GitHub Actions
  run: |
    pip install zizmor
    zizmor .github/workflows/
```

### 2.2 Payload size limits dans les handlers MCP

`_MAX_KNOWLEDGE_FILE_BYTES = 262_144` existe pour les fichiers knowledge mais pas pour les inputs MCP entrants.

À ajouter dans `mcp/server.py` :
```python
_MAX_MCP_INPUT_BYTES = 65_536   # 64 KB par paramètre string
_MAX_MCP_PATHS_COUNT = 50       # nombre de paths par requête

def _validate_input_size(value: str, *, label: str, max_bytes: int = _MAX_MCP_INPUT_BYTES) -> None:
    if len(value.encode()) > max_bytes:
        raise ValueError(f"{label} exceeds {max_bytes} bytes limit")
```

Appel systématique en tête de chaque tool handler MCP.

### 2.3 Élever la gate de couverture

```toml
# pyproject.toml — progression par phase
[tool.coverage.report]
fail_under = 80   # Phase 2 : 70 → 80
# Phase 3 : 80 → 85 (branch coverage)
```

Et activer la branch coverage :
```toml
[tool.coverage.run]
branch = true
```

### 2.4 Ajouter mutation testing en CI (optionnel, weekly)

```yaml
# .github/workflows/weekly-mutation.yml
- name: Mutation testing
  run: uv run mutmut run --paths-to-mutate src/grimoire/core/ src/grimoire/mcp/
```

**Règle anti-régression** : CONTRIBUTING.md doit documenter la politique SHA-pinning. Toute PR ajoutant une nouvelle Action sans SHA est bloquée par `zizmor`.

---

## Phase 3 — Qualité des tests (Test Quality)

> **Impact** : +4.0 Test Quality (le plus grand delta, le plus structurant)
> **Prérequis** : Phase 1 (split app.py débloque split test_app.py)

### 3.1 Refactoring de `test_app.py` (3,757L)

Miroir direct du God File — se découpe en parallèle du split Phase 1 :

| Module test cible | Couvre | Objectif |
|---|---|---|
| `tests/unit/cli/test_cmd_workflows.py` | commandes workflows | Tests comportementaux uniquement |
| `tests/unit/cli/test_cmd_config.py` | commandes config | Paramétrisés avec `pytest.mark.parametrize` |
| `tests/unit/cli/test_cmd_self.py` | self/completion/plugins | Mocks minimaux |
| `tests/unit/cli/test_cmd_history.py` | history/repair | Fixtures d'état |
| `tests/unit/cli/test_app_core.py` | main/entry/aliases | < 300L |

### 3.2 Remplacement des assertions d'existence

Problème identifié dans l'audit : assertions qui vérifient que du code *existe* plutôt que ce qu'il *fait*.

```python
# AVANT — assertion d'existence (à éliminer)
assert result.exit_code == 0

# APRÈS — assertion comportementale
assert result.exit_code == 0
assert "workflow" in result.output
assert json.loads(result.output)["status"] == "installed"
```

Règle : toute assertion `assert result.exit_code == 0` seule (sans assertion sur l'output ou l'effet) est un smell. Minimum 2 assertions comportementales par test de commande.

### 3.3 Étendre Hypothesis aux invariants core

Actuellement 4 fichiers utilisent Hypothesis. Candidats naturels supplémentaires :

```python
# Exemples d'invariants à fuzzifier
from hypothesis import given, strategies as st

@given(path=st.text())
def test_ensure_within_root_never_escapes(path):
    """Quelle que soit l'entrée, _ensure_within_root ne sort jamais du root."""
    ...

@given(config=st.fixed_dictionaries({...}))
def test_config_roundtrip(config):
    """Sérialisation/désérialisation est idempotente."""
    ...
```

Modules prioritaires : `mcp/security.py`, `core/config.py`, `core/scaffold.py`

### 3.4 Audit des tests racine (tests/*.py — 185 fichiers)

La majorité des tests sont dans `tests/` (racine) et ne sont PAS dans `tests/unit/` — donc non inclus dans la gate CI (`pytest tests/unit/`). C'est un angle mort majeur.

Options :
- **Option A** : migrer progressivement les tests pertinents vers `tests/unit/`
- **Option B** : étendre la gate CI à `tests/` avec timeout strict
- **Option C** : créer `tests/integration/` avec CI séparé (weekly)

Recommandation : **Option A** pour les tests de modules core, **Option C** pour les tests qui requièrent des services externes.

**Règle anti-régression** :
```toml
# pyproject.toml
[tool.pytest.ini_options]
# Aucun nouveau test file > 500 lignes
# Enforced par le hook file-size-guard (Phase 1)
```

---

## Phase 4 — Observabilité & Documentation (polish A+)

> **Impact** : +1.5 Observabilité, +1.0 Documentation
> **Prérequis** : Phases 1-3

### 4.1 Structured logging

Remplacer les `print()` résiduels et les logs ad-hoc par un logger structuré cohérent :

```python
# src/grimoire/core/logging.py — à créer
import logging
import json

class GrimoireJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "level": record.levelname,
            "module": record.module,
            "msg": record.getMessage(),
            "ts": self.formatTime(record),
        })
```

Règle : toute fonction publique qui fait du I/O (fichier, réseau, subprocess) doit émettre au moins un `logger.debug(...)` à l'entrée.

### 4.2 ADRs pour les décisions majeures

Créer `docs/adr/` avec :
- `ADR-001-god-file-split.md` — décision et contexte du split Phase 1
- `ADR-002-mcp-security-boundary.md` — modèle de sécurité MCP
- `ADR-003-test-strategy.md` — behavioral over structural

### 4.3 API reference auto-générée

Activer `mkdocstrings` dans `mkdocs.yml` pour auto-générer la référence API depuis les docstrings existants. Zéro travail de rédaction, gain de 0.5 point documentation.

---

## Règles anti-régression consolidées

Ces règles sont permanentes — elles s'appliquent à toute PR dès leur activation.

### Règles CI (bloquantes)

| Règle | Outil | Déclencheur |
|---|---|---|
| Aucun fichier Python > 600L | `scripts/check_file_size.py` + pre-commit | pre-commit + CI |
| Aucun `except Exception` nu | ruff `BLE001` | CI lint |
| Aucune Action GitHub sans SHA | `zizmor` | CI |
| Coverage ≥ 80% (→85% Phase 3) | pytest-cov `fail_under` | CI test |
| `mypy --strict` sans régression | mypy | CI |
| pip-audit 0 vulnérabilité | pip-audit | CI |
| Branch coverage activée | pytest-cov `branch=true` | CI |

### Règles de review (guidelines PR)

| Règle | Vérification |
|---|---|
| Tout nouveau module > 300L doit avoir une justification | Description PR |
| Tout test qui assert uniquement `exit_code == 0` est un smell | Code review |
| Tout nouveau tool MCP doit appeler `_validate_input_size` | Checklist PR |
| Tout nouveau GitHub Action doit être SHA-pinné | `zizmor` automatique |
| Toute fonction I/O publique doit avoir un `logger.debug` | Code review |

### Règles de structure (invariants permanents)

```
src/grimoire/
├── cli/           # Un cmd_*.py par groupe de commandes — max 600L chacun
├── mcp/
│   ├── handlers/  # Un handler par domaine fonctionnel
│   └── security.py  # Boundary checks centralisés — ne jamais dupliquer
├── core/          # Logique métier pure — zéro I/O directe
└── memory/        # Backends isolés — zéro dépendance croisée
```

---

## Séquençage et dépendances

```
Phase 1 ──────────────────────────────────────────────────────────
  1.1 Split app.py          ──→ débloque 3.1 (test_app.py split)
  1.2 Split mcp/server.py   ──→ débloque 2.2 (payload limits propres)
  1.3 BLE001 ruff rule      ──→ bloque toute régression dès activation

Phase 2 ──────────────────────────────────────────────────────────
  2.1 SHA-pinning           ──→ indépendant, peut commencer en parallèle
  2.2 MCP payload limits    ──→ après 1.2
  2.3 Coverage gate 80%     ──→ après 3.1 (sinon gate trop agressive)
  2.4 Mutation testing      ──→ weekly, non bloquant

Phase 3 ──────────────────────────────────────────────────────────
  3.1 Split test_app.py     ──→ après 1.1
  3.2 Behavioral assertions ──→ pendant 3.1
  3.3 Hypothesis extension  ──→ après 1.2 (mcp/security.py cible principale)
  3.4 Audit tests racine    ──→ parallélisable

Phase 4 ──────────────────────────────────────────────────────────
  4.1 Structured logging    ──→ après Phases 1+2
  4.2 ADRs                  ──→ rédiger pendant les phases
  4.3 API reference         ──→ mkdocstrings, rapide
```

---

## Score projeté par phase

| Après | Arch | Code | Test | Secu | CI | Obs | Doc | **Moy** |
|---|---|---|---|---|---|---|---|---|
| Baseline | 7.0 | 6.5 | 5.0 | 6.0 | 7.0 | 7.5 | 8.0 | **6.7** |
| Phase 1 | **8.5** | **8.5** | 6.0 | 6.0 | 7.5 | 7.5 | 8.0 | **7.4** |
| Phase 2 | 8.5 | 8.5 | 6.0 | **9.0** | **9.0** | 7.5 | 8.0 | **8.1** |
| Phase 3 | 8.5 | 8.5 | **9.0** | 9.0 | 9.5 | 7.5 | 8.0 | **8.6** |
| Phase 4 | 9.0 | 9.0 | 9.0 | 9.5 | 9.5 | **9.0** | **9.0** | **9.1 → A+** |

---

*Généré le 2026-04-11 — Plan d'action post-rescoring Grimoire-kit v3.4.2*
