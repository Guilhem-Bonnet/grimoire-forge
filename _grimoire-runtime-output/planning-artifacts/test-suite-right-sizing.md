# Plan de réduction des tests

## Objectif

- réduire les doublons entre suites legacy et suites canoniques ;
- garder une couverture forte sur la logique métier actuelle ;
- limiter les assertions de wording et de `--help` aux surfaces réellement utiles.

## Coupes exécutées

- [grimoire-kit/tests/test_doc_fetcher.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/test_doc_fetcher.py) est ramené à du smoke coverage sur l'entrée legacy dépréciée ; la couverture détaillée reste dans [grimoire-kit/tests/test_docs_fetcher.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/test_docs_fetcher.py).
- [grimoire-kit/tests/test_memory_lint.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/test_memory_lint.py) est ramené à du smoke coverage CLI et sérialisation ; la couverture métier reste dans [grimoire-kit/tests/unit/tools/test_memory_lint.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/unit/tools/test_memory_lint.py).
- [grimoire-kit/tests/test_preflight_check.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/test_preflight_check.py) est ramené à du smoke coverage report/CLI ; la couverture métier reste dans [grimoire-kit/tests/unit/tools/test_preflight_check.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/unit/tools/test_preflight_check.py).

## A garder comme sources canoniques

- [grimoire-kit/tests/test_docs_fetcher.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/test_docs_fetcher.py) pour le fetcher actuel ;
- [grimoire-kit/tests/unit/tools/test_memory_lint.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/unit/tools/test_memory_lint.py) pour `memory_lint` ;
- [grimoire-kit/tests/unit/tools/test_preflight_check.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/unit/tools/test_preflight_check.py) pour `preflight_check` ;
- quelques smokes root pour garantir que les scripts legacy restent encore appelables.

## Tranche suivante proposée

- rabattre [grimoire-kit/tests/test_context_guard.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/test_context_guard.py) et [grimoire-kit/tests/test_harmony_check.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/test_harmony_check.py) au même modèle smoke ;
- remplacer dans [grimoire-kit/tests/test_guardrail_policy.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/test_guardrail_policy.py) les assertions de formulation exacte par des assertions sur structure, tags et branches de décision ;
- faire un second passage sur [grimoire-kit/tests/unit/cli/test_app.py](/mnt/Travail/Projets/Dev/bmad-custom/grimoire-kit/tests/unit/cli/test_app.py) si la suite reste trop centrée sur des flags décoratifs.