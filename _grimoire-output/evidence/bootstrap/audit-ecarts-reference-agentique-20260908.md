# Audit d'écart — Grimoire contre la référence agentique industrielle

- Date : 2026-09-08
- Référentiel : `grimoire-kit/framework/agentic-industry-reference.md` (PR Grimoire-kit#315)
- Périmètre audité : grimoire-kit à `9d5ca9f6` (origin/main 3.40.0 + référence) et Grimoire-Forge (hooks, standard, runtime) en lecture seule
- Méthode : cinq audits parallèles sur Sonnet, un par axe de la référence, chaque constat avec fichier et ligne ; les constats bloquants ont été revérifiés à la main par la session principale (marqués « confirmé »)
- Statut : aucun fichier modifié par l'audit

## 1. Verdict

Sur le papier, Grimoire est aligné ou en avance sur la référence : preuve avant clôture, incertitude honnête, questions groupées, capsule PreCompact, refus structurés, gouvernance shadow/canary/enforced des hooks, exécution durable testée. La distance réelle est ailleurs : une large part des règles que le socle énonce n'existe qu'en prose, et plusieurs mécanismes présentés comme actifs sont morts ou échouent ouvert.

| Axe | Constats | Prose seule | Bloquants | Distance |
|---|---|---:|---:|---|
| Orchestration et workflows | 20 | 11 | 1 | Moyenne : les plafonds MAST (répétition, arrêt, P2P) sont décrits, jamais comptés |
| Contexte, mémoire, skills, sous-agents | 20 | 6 | 2 | Moyenne : budget de tokens mort, mémoire non validée, sous-agents sans plafond |
| Outils, MCP, hooks | 16 | 3 | 2 | Moyenne à forte : révision MCP en retard, aucune annotation, gate de médiation exigé par le profil sans vérificateur |
| Sécurité, identité | 12 | 3 | 2 | Forte : gardes Copilot fail-open, contenu externe non marqué, registre MCP vide |
| Évals, observabilité, économie | 20 | 5 | 3 | Forte : export OTel cassé et vide, aucun pass^k, routing statique sans boucle de coût |

Lecture : le kit tient sa promesse là où un module Python porte la règle (gates de preuve, kernel de reprise, décisions PreToolUse côté Claude Code). Il ne la tient pas là où la règle vit dans un `.md` ou un YAML sans vérificateur. La priorité n'est pas d'écrire de nouvelles règles, c'est de câbler celles qui existent.

## 2. Écarts bloquants confirmés

| # | Écart | Preuve | Cible |
|---|---|---|---|
| B1 | Les gardes PreToolUse du hôte Copilot autorisent en silence si le script de politique manque ou plante (`echo "{}"; exit 0`), alors que le moteur produit renvoie `ask` dans le même cas | `.github/hooks/scripts/grimoire-control-surface-guard.sh:18-26`, `grimoire-memory-guard.sh:16-24` contre `src/grimoire/hosts/decisions.py:743-751` ; confirmé | Forge (maintenance corrective) puis kit |
| B2 | Le budget de tokens est un no-op : `load_tool_module("token-budget.py")` résout dans `.github/hooks/lib/`, où le fichier n'existe pas | `.github/hooks/lib/guardrail-policy.py:1007-1030, 2065-2073` ; confirmé | Forge (vendoriser) |
| B3 | Le verrou de fichiers `exclusive_files` est stocké mais jamais comparé entre deux claims actifs : aucun garde contre deux agents écrivant le même fichier | `src/grimoire/missions/ledger.py:347-349`, `schemas.py:96`, `service.py:183` ; confirmé | Kit |
| B4 | L'écriture mémoire n'est ni validée ni cloisonnée (format, taille, émetteur) ; `redaction: required` est un booléen YAML jamais exécuté | `src/grimoire/memory/manager.py:375-379`, `src/grimoire/mcp/server.py:241-257`, `core/standard_checks/verifiers.py:842-846` | Kit |
| B5 | Le pattern `tool-mediation-gate` est exigé par le profil `governed` mais n'a aucun vérificateur (`checks: []`) ; la Forge est en `governed` sans cette capacité | `framework/agentic-standard/capability-map.yaml:138-144`, `_grimoire/standard/standard-profile.yaml:38`, `capability-registry.yaml` | Kit puis Forge |
| B6 | Registre d'outils vide côté MCP alors que quatre serveurs sont actifs, dont un `@latest` non épinglé | `_grimoire/standard/tool-registry.yaml:23`, `.mcp.json` ; confirmé | Forge |
| B7 | Export OTel : horodatage des événements d'outil toujours nul (`_ns("float")`), attribut `gen_ai.system` déprécié, pas d'`operation.name` ni de span `execute_tool` ; et `EVENT_SOURCES` pointe un fichier qui n'existe pas sur la Forge, donc l'export est vide | `src/grimoire/traces/ledger.py:259-274`, `src/grimoire/tools/blueprint_telemetry.py:32-35` ; confirmé | Kit |
| B8 | Hook `grimoire-subagent-context` déclaré `enforced` sur `SubagentStart` mais l'événement n'est pas câblé dans `.claude/settings.json` : hook mort | `_grimoire-runtime/_config/hook-safety-registry.json`, `.claude/settings.json` ; confirmé | Forge |

## 3. Écarts importants

Orchestration

- « Mono-agent d'abord » et « mono-fil en écriture » n'existent que dans la référence, pas dans `orchestrator-gateway.md` (`framework/orchestrator-gateway.md:184-204`).
- Circuit breaker AORA, `max_iterations_per_task`, `max_p2p_without_sog: 5`, `RecipeRetryProfile.max_retries` : tous déclarés, aucun compté par du code (`agent-base.md:407-414`, `agent-mesh-network.md:244`, `framework/tools/message-bus.py`, `src/grimoire/runtime/recipes.py:27-29`).
- CVTL : aucune assertion `validator != producer` (`framework/cross-validation-trust.md:42-48`).
- HPE (402 lignes de DAG et scheduler) : aucune implémentation ; `teams.py` est un catalogue, pas un exécuteur de handoff.
- PCE : plafond de rounds mais aucun seuil de déclenchement, alors que la recherche montre un gain rarement supérieur à Self-Consistency.
- `governed-agent-orchestration` catalogué `orchestrated` avec `check_refs: []` ; seul un contrôle de schéma existe (`verifiers.py:998`).

Contexte, mémoire, sous-agents

- `ContextGuard` mesure un vrai budget mais n'est appelé par personne (`src/grimoire/tools/context_guard.py:36-124`).
- Les sept sous-agents générés n'ont ni `effort`, ni `maxTurns`, ni `background`, ni `isolation` (`src/grimoire/hosts/emitters/claude_code.py:85-91`).
- Fichier d'instructions effectif de la Forge : 332 lignes chargées contre une cible sous 200 ; doctrine atelier dupliquée dans trois fichiers.
- Aucun validateur `skills-ref` ; 47 skills sur 47 conformes par convention, 2 sur 47 utilisent `references/`.
- Le budget de contexte est compté en items, pas en tokens (`_grimoire/standard/context-contract.yaml:37-40`).

Outils, MCP, hooks

- SDK `mcp==1.28.1`, révision la plus haute 2025-11-25 ; la feuille de route prévoit encore « MCP v2 Sampling » alors que Sampling est déprécié (`framework/mcp/grimoire-mcp-server.md:420`).
- `framework/mcp/grimoire-mcp-server.md` décrit neuf outils fictifs qui n'existent pas dans le serveur réel (21 outils).
- 21 outils MCP sans annotation, sans `outputSchema`, erreurs renvoyées en JSON texte sans `isError`.
- Le modèle interne des hooks ne connaît que 7 événements sur la famille Claude Code (`src/grimoire/hosts/surface.py:54-60`).
- Deux moteurs de gouvernance divergents : 6 163 lignes côté Copilot legacy contre 755 lignes host-neutre côté produit.

Sécurité

- Contenu web et messages inter-agents ne portent aucun marquage « donnée, pas instruction » (`framework/tools/web-browser.py`, `event-log-shared-state.md`) ; aucun des six patterns de Beurer-Kellner n'est appliqué explicitement.
- Le template `prompt_firewall` n'est requis par aucun profil, pas même `production` (`profile-map.yaml:125,285-380`) ; idem `blast_radius`, `privilege_boundary`, `workspace_isolation`.
- Un seul `actor_id` générique, pas d'identité par agent (`decisions.py:355-357`) ; accepté par doctrine tant que les agents restent locaux, à consigner comme risque accepté.
- Déclaration de conformité obsolète : Claude marqué « supported-disabled » alors que la session tourne sous Claude Code.

Évals, observabilité, économie

- Aucun pass^k alors que les tâches sont déjà répétées cinq fois (`evals/runner.py`).
- Pas de distinction capability contre regression, aucune tâche sourcée d'un vrai échec.
- Le coût par tâche existe (`evals/aggregate.py:70-72`) mais jamais par sous-agent ; `model-routing.yaml` est une table statique sans `effort`, `cost`, `budget` ni boucle de mesure.
- `provider-cost-slo` : `checks: []`, et `profile_min: production`, donc jamais actif sur la Forge.
- Aucun plafond de tours ou de coût dans `src/grimoire/runtime/kernel.py` ; seul le harness d'évals en a.
- Aucune mesure de hit rate de cache ni de stabilité de préfixe.

## 4. Couverture OWASP

LLM Top 10 2026 : couvert 1 (LLM02), partiel 5 (LLM01, LLM03, LLM07, LLM10 et LLM05 hors périmètre), absent 4 (LLM04 supply chain, LLM06 consommation non bornée, LLM08 contexte caché, LLM09 mémoire vectorielle).

Top 10 agentique : couvert 1 (ASI02 tool misuse), partiel 5 (ASI01, ASI05, ASI06, ASI08, ASI09), absent 4 (ASI03 identité, ASI04 supply chain, ASI07 communication inter-agents, ASI10 agents déviants).

## 5. Points où Grimoire est en avance, confirmés par le code

- Gates de preuve exécutés et câblés (`src/grimoire/missions/gates.py`, `service.py:172-175`).
- Kernel d'exécution durable avec machine à états, checkpoints JSONL, reprise, 16 tests (`src/grimoire/runtime/kernel.py`).
- Décisions PreToolUse côté Claude Code qui échouent en `ask` et non en `allow` (`decisions.py:743-751`).
- Journal d'audit vivant avec digest des arguments, jamais la commande brute (`_grimoire-output/traces/traces.jsonl`).
- Capsule PreCompact structurée (`guardrail-policy.py:4870-4901`).
- Refus MCP nommés avec preuve manquante et remède (`server.py:534-537`).
- Gouvernance shadow, canary, enforced appliquée par code (`hook-safety-gate.py:430-443`).
- Évals : rejeu déterministe fail-closed, jugement humain en aveugle, règle d'arrêt pré-enregistrée (`blueprint_eval_runner.py`, `evals/judge.py`, `docs/evals-protocol.md:45-56`).
- Transparence documentaire sur ce que l'hôte n'exécute pas réellement (`orchestrator-gateway.md:524-588`).

## 6. Incohérences internes relevées

1. AORA, PIP et DCF sont présentés comme actifs dans le socle du kit (`agent-base.md:361-500`, `agent-base-compact.md:21-23`) alors que la doctrine Forge les dit retirés ou observer-only : le produit distribué contredit l'atelier.
2. Deux systèmes de checkpoint qui s'ignorent : BM-06 (`framework/workflows/state-checkpoint.md`) et le kernel réel.
3. `framework/mcp/grimoire-mcp-server.md` décrit un serveur qui n'existe pas.
4. La section 10 de la référence marque « aligné » plusieurs protocoles dont l'audit montre qu'ils sont prose seule (CVTL, AMN, ARG, ELSS) ; à corriger dans la PR #315.

## 7. Plan d'actions consolidé

Ordre par rapport bénéfice sur effort, cible et nature indiquées. Les actions Forge relèvent de la maintenance corrective autorisée par la doctrine (mécanisme cassé).

| # | Action | Cible | Couvre |
|---|---|---|---|
| 1 | Faire échouer fermé les deux gardes PreToolUse Copilot (renvoyer `ask`, tracer) | Forge | B1 |
| 2 | Vendoriser `token-budget.py` dans `.github/hooks/lib/` et lire `enforcementRecommended` dans Stop | Forge | B2 |
| 3 | Câbler `SubagentStart` dans `.claude/settings.json` ou retirer le hook du registre | Forge | B8 |
| 4 | Peupler `tool-registry.yaml` avec les quatre serveurs MCP, épingler la version de `@playwright/mcp` | Forge | B6 |
| 5 | Vérifier le chevauchement `exclusive_files` dans `ledger.claim_task` et refuser le claim | Kit | B3 |
| 6 | Valider les écritures mémoire (schéma, taille, émetteur autorisé) et exécuter la redaction | Kit | B4 |
| 7 | Corriger `ledger.py` (horodatage, `gen_ai.provider.name`, `gen_ai.operation.name`, span `execute_tool`), unifier avec `blueprint_telemetry.py`, corriger `EVENT_SOURCES` | Kit | B7 |
| 8 | Écrire le vérificateur `tools.mediated-before-use` et le brancher sur `tool-mediation-gate` ; ajouter compteurs et budgets par session | Kit | B5 |
| 9 | Annoter les 21 outils MCP (`readOnlyHint`, `destructiveHint`), passer les erreurs en `isError`, borner la version du SDK et planifier la révision 2026-07-28 | Kit | MCP |
| 10 | Émettre `effort: low`, `maxTurns` et `background` dans l'émetteur de sous-agents | Kit | sous-agents |
| 11 | Compter en code au moins un plafond MAST : `max_retries` des recettes et `max_p2p_without_sog` | Kit | MAST FM-1.3, FM-1.5 |
| 12 | Marquer le contenu web et les messages ELSS comme « donnée, pas instruction » ; rendre `prompt_firewall` requis à partir de `governed` | Kit | LLM01, ASI01, ASI07 |
| 13 | Ajouter pass^k et l'étiquette capability contre regression aux évals ; ventiler le coût par sous-agent | Kit | évals, économie |
| 14 | Trancher AORA, PIP, DCF dans le socle ; supprimer `grimoire-mcp-server.md` et BM-06 ou les marquer obsolètes | Kit | cohérence |
| 15 | Réduire les instructions de la Forge sous 200 lignes chargées et dédupliquer la doctrine | Forge | contexte |

## 8. Coût de l'audit

Cinq sous-agents Sonnet, environ 840 000 tokens au total, 339 appels d'outils ; la session principale n'a lu que les rapports et vérifié huit constats.
