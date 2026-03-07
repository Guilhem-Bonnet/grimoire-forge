# Agent Base Protocol — Projet Grimoire

> Protocole de base custom pour tous les agents du projet Grimoire.
> Étend `framework/agent-base.md` avec les spécificités projet.

## Base Protocol

Charger et appliquer intégralement : `framework/agent-base.md`

## Overrides Projet

- **Communication** : Français
- **Output** : `_bmad-output/`
- **Stack principal** : Python 3.12+ (pytest + ruff)
- **CC verify** : `python3 -m pytest tests/ -q --tb=short -x && python3 -m ruff check framework/tools/ tests/`
