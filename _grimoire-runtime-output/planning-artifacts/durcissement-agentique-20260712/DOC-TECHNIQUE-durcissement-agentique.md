---
title: Documentation technique — durcissement agentique
description: Base factuelle, sources et mécanismes concernés par le plan de durcissement du 2026-07-12
author: Grimoire Master (session Claude)
date: 2026-07-12
---

## Objet

Ce document consigne la base factuelle qui fonde `PLAN-durcissement-agentique.md` : les sources de preuve, les chiffres clés et les mécanismes techniques concernés par chaque lot. Il permet de vérifier ou de contester chaque décision du plan sans refaire l'évaluation.

## Sources de preuve

### Campagne benchmark web-app-todo (preuve causale)

- Rapport : `grimoire-kit/evals/reports/2026-07-03/report.md`
- Protocole pré-enregistré : `grimoire-kit/docs/evals-protocol.md`
- Grille de jugement : `grimoire-kit/evals/witnesses/web-app-todo/JUDGING.md`
- Tâches figées : `grimoire-kit/evals/tasks/web-app-todo.yaml`

Chiffres clés : 80 runs (8 tâches, 2 bras, 5 répétitions), modèle claude-sonnet-4-6, baseline pinnée. Régressions 16 (governed) contre 13 (baseline), soit +23 % là où le critère pré-enregistré exigeait −30 %. Complétion 7/40 contre 6/40. Coût +10,2 % pour le bras governed. Constat central : 0/40 runs governed ont engagé le protocole du standard (aucune enveloppe de tâche, aucun appel de gate) — la campagne mesure la présence passive des artefacts, pas leur usage. Analyse de sensibilité post-hoc : en ne comptant que les régressions dures, le résultat s'inverse (7 contre 12).

### Télémétrie runtime (preuve d'exécution)

- Log principal : `_grimoire-runtime-output/hook-runtime/safety-gate/events.jsonl` — 34 486 invocations (2026-04-13 → 2026-05-27), 3 exits non nuls, environ 0,03 % d'échec global.
- Erreurs : `_grimoire-runtime-output/hook-runtime/events-errors.jsonl` — 7 lignes, dont 6 pour l'échec récurrent `vscode-agent-terminals-autoprune` (exit=2, d'avril au 2026-07-12).
- Task-flow : `_grimoire-runtime-output/task-flow/events.jsonl` — 350 événements, 152 succès, 23 échecs.
- Trace SOG : `_grimoire-runtime-output/GRIMOIRE_TRACE.jsonl` — 432 événements SubagentStart/Stop corrélés avec `hook-runtime/subagent-stop/` et le safety-gate.
- Registre : `_grimoire-runtime/_config/hook-safety-registry.json` — 11 hooks enforced, 1 canary, 1 shadow.
- UDF : `_grimoire-runtime/_memory/udf-usage-tracker.json` vide ; zéro artefact `_dyn-*` sur disque.

Incohérences constatées (fondent le lot 0) : `grimoire-rtk-rewrite` enforced au registre mais 0 invocation loggée ; `grimoire-doc-drift` canary au registre mais 938 événements tous en shadow ; `grimoire-terminal-guard` shadow permanent à 0 événement ; `mcp-audit.jsonl` contient des outils factices (`bmad_totally_fake_tool`).

### Audits internes (preuve documentaire)

- `_grimoire-runtime-output/planning-artifacts/stigmergy-activation-20260707/AUDIT-bonnes-pratiques-agentiques.md` — audit du code livré contre le catalogue normatif (78 patterns, 52 anti-patterns) : 5 anti-patterns violés par le kit lui-même, 5 patterns correctement appliqués, priorisation en 6 items (reprise au lot 5).
- `_grimoire-runtime-output/planning-artifacts/stigmergy-activation-20260707/INVENTAIRE-features-dormantes.md` — 15 outils intégrés sur 108, environ 86 % de capacités dormantes.
- `_grimoire-runtime-output/planning-artifacts/maturation-agentique-20260421/04-CARTOGRAPHIE-concepts.md` — grille fonctionnel/partiel/théorique et verdicts par protocole BM-*.
- `_grimoire-runtime-output/planning-artifacts/audit-agentique-2026-04-10.md` — « la vision est en avance sur l'exécution » ; harmony 0/100, 555 dissonances.

## Verdicts par protocole (état au 2026-07-12)

| Protocole | Sigle interne | Verdict des audits | Preuve d'exécution réelle | Traitement au plan |
| --- | --- | --- | --- | --- |
| SOG | BM-53 | Fonctionnel | Structurelle (topologie 1 agent + masquage, trace dédiée) | Conservé |
| HUP | BM-50 | « Fonctionnel » | Déclarative uniquement | Lot 3 : instrumenter ou archiver |
| QEC | BM-51 | « Fonctionnel » | Déclarative uniquement | Lot 3 : instrumenter ou archiver |
| CVTL | BM-52 | « Fonctionnel » | Déclarative uniquement | Lot 3a : conversion en hook |
| PCE | BM-54 | « Fonctionnel » | Existence d'un skill | Lot 3 |
| ALS | BM-55 | « Fonctionnel » | Documentaire (« documenté dans agent-base.md ») | Lot 3 |
| PIP | BM-58 | Observer seulement | Aucune | Lot 1.4 : statut acté |
| ARG | BM-57 | Fonctionnel | Déclarative (routing SOG) | Conservé, à instrumenter en 3a.2 si lot 3a |
| ELSS | BM-59 | Archiver (non implémenté) | Aucune | Lot 1.4 : archivé |
| AORA | — | Non audité | Aucune (une mention en prose) | Lot 1.1 : purge |
| DCF | — | Inexistant sous ce sigle | Aucune | Lot 1.1 : purge |
| UDF | — | « Terminé et vivant » (affirmé) | Tracker vide, zéro artefact créé | Lot 1.2 : suppression ou sursis |

## Mécanismes techniques concernés

### Chaîne des hooks (lots 0 et 4)

Tous les hooks passent par `.github/hooks/scripts/grimoire-hook-gateway.sh` avec le registre `_grimoire-runtime/_config/hook-safety-registry.json`. Tout nouveau hook (lot 4) doit être déclaré au registre et démarrer en `shadow`, sous peine d'échec de `hooks-status` et `grimoire-hooks-smoke.sh`. La promotion suit `hook-safety-gate.py set-mode` ou les tasks `grimoire: hooks-shadow` / `hooks-canary` / `hooks-promote`.

### Mécanisme d'activation de la campagne (lot 2)

Le bras « activé » ajoute au bras governed : un hook `SessionStart` injectant l'obligation d'ouvrir une enveloppe de tâche, et un contrôle bloquant `gate check` avant clôture. La comparaison à trois bras isole l'effet de l'usage (activé contre governed passif) de l'effet de la présence (governed passif contre baseline).

### Garde-fou « fonctionnel = consommé » (lot 4)

Deux niveaux de contrôle : statique (tout sigle déclaré dans `copilot-instructions.md` ou les agents doit référencer un artefact exécutable existant) et dynamique (tout artefact enforced doit produire des événements de trace sur une fenêtre glissante). Le second niveau aurait détecté les trois incohérences du lot 0 (rtk-rewrite, doc-drift, terminal-guard).

## Limites connues

- La télémétrie s'arrête majoritairement fin mai 2026 ; l'activité récente est faible. Les conclusions « vivant/mort » reflètent l'usage du printemps 2026.
- Les répétitions de la campagne (n=5 par cellule) n'autorisent aucun test statistique ; les verdicts sont des signaux, le critère pré-enregistré en tient compte.
- Les verdicts « fonctionnel » de la cartographie d'avril mélangent preuve structurelle et preuve déclarative ; ce document requalifie chaque ligne (tableau ci-dessus).

## Addendum post-exécution (2026-07-12)

L'exécution des lots a requalifié trois faits de la base ci-dessus :

- **Canal enforced gelé, pas seulement « tari »** : le diagnostic du lot 0 établit que plus aucun hook enforced n'a journalisé depuis le 2026-05-27 — le runtime actif (Claude Code) n'a pas de bloc `hooks` dans `.claude/settings.json`, le canal gateway n'était joué que par VS Code Copilot. Les 34 486 invocations restent une preuve de fonctionnement passé, pas d'un état courant. Le canal shadow, lui, vit encore (événements du 2026-07-12).
- **L'échec autoprune n'était pas un bug de tâche** : le script cible `grimoire-kit/framework/tools/vscode-terminal-prune.py` n'existait pas (arbre kit gitignoré, outil jamais vendoré) — exit=2 de l'interpréteur Python. Corrigé par retrait des 8 tasks et de l'allowlist.
- **Le « 0/40 engagement » de juillet est en partie un artefact d'instrument** : le collecteur v1 (`evals/collect.py`) évaluait verify/gate avec le label de tâche d'éval au lieu de l'id standard `bootstrap`, produisant mécaniquement « missing evidence » partout. Corrigé en v2. Le constat qualitatif (aucune enveloppe créée, aucun gate appelé par les agents) reste vrai, mais les compteurs chiffrés de juillet le surestimaient.
- État du registre après lot 0/4 : 15 hooks — 10 enforced revalidés, 1 canary (doc-drift), 4 shadow (rtk-rewrite, pattern-consumption, board-transitions, engagement). Le tableau « 11 enforced, 1 canary, 1 shadow » ci-dessus décrit l'état antérieur.
