---
description: "Conventions Python du projet Grimoire Kit. Use when: writing Python code, creating Python files, editing Python, Python style, Python imports, Python dataclasses, Python exceptions, type hints."
applyTo: "**/*.py"
---

# Python Conventions — Grimoire Kit

## Imports

- `from __future__ import annotations` toujours en première ligne d'import
- Tri automatique par isort (groupes : stdlib, third-party, local)
- f-strings exclusivement — jamais `.format()` ni `%`

## Style

- Line length max : 120 caractères (configuré dans `ruff.toml`)
- Target : Python 3.12+
- Linter : ruff avec bandit (sécurité), bugbear, simplify, pathlib

## Data Models

- `@dataclass(frozen=True, slots=True)` pour les structures de données
- Type hints obligatoires sur toutes les fonctions publiques
- Exceptions : hériter de `GrimoireError` (base custom)

## Outils framework (`framework/tools/`)

- Noms de fichiers avec tirets : `memory-lint.py`, `auto-doc.py`
- Import via `importlib.import_module()` dans les tests (noms avec tirets)
- Chaque tool expose une constante `*_VERSION`
- CLI via argparse avec `--project-root`

## Tests (`tests/`)

- Pattern : `test_<module_avec_underscores>.py`
- Classes unittest : `TestClassName` avec `setUp()`
- Fixtures partagées dans `conftest.py`
- Couverture cible : >90% sur le code nouveau
- Jamais de tests en parallèle avec xdist dans ce projet (séquentiel `-x`)

## Anti-patterns

- Ne PAS utiliser `os.path` — utiliser `pathlib.Path`
- Ne PAS laisser de code commenté (ERA001)
- Ne PAS utiliser `random` pour la sécurité (S311 autorisé uniquement pour les IDs non-crypto)
