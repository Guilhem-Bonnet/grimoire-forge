---
description: "Pipeline de développement du Pixel Observatory V2. Orchestre les phases : game engine, timeline, intégration, polish, tests."
mode: "ask"
tools: ["read_file", "replace_string_in_file", "create_file", "run_in_terminal", "grep_search", "semantic_search", "get_errors", "file_search", "runSubagent"]
---

# Pixel Observatory V2 — Workflow de développement

## Contexte

Ce workflow orchestre la transformation de l'Observatory en un tableau de bord
agentic gamifié avec pixel art, timeline scrubber, et configuration agents.

## Fichier cible principal

`grimoire-kit/framework/tools/observatory.py` — extension du template HTML/CSS/JS embarqué.

## Phases

### Phase 1 : Game Engine Core

1. Lire `observatory.py` pour comprendre la structure du template HTML
2. Insérer le système de sprites procéduraux (`SpriteFactory`)
3. Insérer le layout manager (`OfficeLayout`)
4. Insérer le pathfinder A*
5. Insérer le contrôleur d'agents (`AgentCharacter`)
6. Vérifier : pas d'erreur console, sprites se génèrent

### Phase 2 : Timeline Engine

1. Insérer `TimelineEngine` (events queue, state snapshots, playback)
2. Ajouter la timeline bar UI (HTML + CSS + JS)
3. Connecter les contrôles (play, pause, seek, speed)
4. Vérifier : la timeline parse et rejoue les événements

### Phase 3 : Intégration Observatory

1. Ajouter l'onglet "🎮 Office" en position 0
2. Insérer le canvas et le Renderer
3. Ajouter le Camera (pan/zoom)
4. Ajouter l'InteractionManager (click, hover, keyboard)
5. Créer l'agent config drawer
6. Connecter timeline → toutes les vues (cross-view sync)
7. Vérifier : l'onglet fonctionne, les agents s'animent

### Phase 4 : Polish

1. Ajouter les effets visuels (particules, halos, trails)
2. Ajouter les sounds optionnels (Web Audio API)
3. Ajouter le mode démo (données simulées)
4. Ajouter la minimap
5. Ajouter les keyboard shortcuts gaming
6. Vérifier : expérience "jeu vidéo" complète

### Phase 5 : Tests

1. Étendre `test_observatory.py` avec tests pour le HTML V2
2. Test Playwright : vérifier rendu canvas, interactions
3. Run full test suite : `python -m pytest tests/ -x --tb=short`

## Règles d'exécution

- Lire la skill `grimoire-pixel-observatory/SKILL.md` AVANT chaque phase
- Chaque phase produit un livrable testable
- Ne pas passer à la phase suivante sans vérification
- Le code JS doit être injecté dans le template `_HTML_TEMPLATE` de observatory.py
- Respecter les conventions du fichier existant (variables CSS, naming, patterns)

## Artifacts de référence

- Brainstorm : `_grimoire-runtime-output/planning-artifacts/BRAINSTORM-PIXEL-OBSERVATORY-V2.md`
- Plan : `_grimoire-runtime-output/planning-artifacts/PLAN-PIXEL-OBSERVATORY-V2.md`
- Skill : `.github/skills/grimoire-pixel-observatory/SKILL.md`
- Code : `grimoire-kit/framework/tools/observatory.py`
- Tests : `grimoire-kit/tests/tools/test_observatory.py`
