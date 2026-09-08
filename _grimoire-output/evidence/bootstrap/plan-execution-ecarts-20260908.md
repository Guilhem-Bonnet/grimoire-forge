# Plan d'exécution — combler les écarts confirmés par l'audit du 2026-09-08

- Source : `audit-ecarts-reference-agentique-20260908.md` (huit bloquants, quinze actions)
- Orchestrateur : concierge (session principale, Fable 5.1), rôle de préparation, dispatch, arbitrage ; ne lit pas les diffs, lit les rapports
- Principe d'économie : Fable ne produit ni code ni revue ligne à ligne ; Sonnet code, Haiku vérifie, Opus tranche
- Doctrine : lot A = maintenance corrective de la Forge (mécanismes cassés) ; lots B à E = produit grimoire-kit, une PR par lot, planning suivi dans une issue épique du kit
- Statut : `done` le 2026-09-08 (sept PR ouvertes, toutes vérifiées ; voir evidence-pack) ; était `executing` depuis la relecture Opus (GO avec amendements) et la fiche de faisabilité Sonnet, intégrées en section 7

## 1. Répartition des modèles

| Rôle | Modèle | Pourquoi | Budget indicatif par tâche |
|---|---|---|---|
| Orchestrateur (concierge) | Fable 5.1 (session) | Contexte complet, arbitrages, doctrine | Lecture des rapports seulement, aucune lecture de diff |
| Éclaireur de faisabilité | Sonnet | Lecture de code étendue, sortie structurée | 1 passe par lot avant dispatch |
| Relecteur d'architecture | Opus | Ordonnancement, risques, conflits de doctrine | 1 passe sur le plan, 1 passe sur les lots sécurité (B, D) |
| Codeur de lot | Sonnet | Correctif borné, tests, ruff, ratchet | 1 agent par lot, worktree jetable, PR |
| Vérificateur indépendant | Haiku | Rejouer les commandes de preuve, comparer le diff aux critères d'acceptation, ne jamais corriger | 1 agent par PR, rapport court |
| Revue adversariale | Opus | Uniquement sur les lots qui touchent la sécurité ou la mémoire | 1 agent par lot concerné |

Règle CVTL appliquée à nous-mêmes : le vérificateur n'est jamais le codeur, et il tourne dans un contexte neuf.

## 2. Lots, dépendances, critères d'acceptation

### Lot A — Forge, maintenance corrective (Sonnet, une PR sur la Forge)

| Action | Fichiers | Critère d'acceptation | Check |
|---|---|---|---|
| A1 Gardes PreToolUse fail-closed | `.github/hooks/scripts/grimoire-control-surface-guard.sh`, `grimoire-memory-guard.sh` | Si python ou le script manquent, ou si l'appel échoue : sortie `permissionDecision: ask` avec raison, événement tracé ; jamais `{}` | Test bash qui simule l'absence du script et attend `ask` ; `grimoire-hooks-smoke.sh` vert |
| A2 Budget de tokens réel | `.github/hooks/lib/` (vendoriser `token-budget.py` depuis le kit), `guardrail-policy.py` | `assess_token_budget` renvoie un statut non vide ; `enforcementRecommended` lu par le hook Stop et produit un `systemMessage` | Test Python ciblé ; hooks-smoke vert |
| A3 Hook SubagentStart câblé ou retiré | `.claude/settings.json`, `hook-safety-registry.json` | Aucun hook `enforced` sans événement câblé ; `hooks-status` cohérent | `hook-safety-gate.py status` sans écart |
| A4 Registre MCP peuplé | `_grimoire/standard/tool-registry.yaml`, `.mcp.json` | Quatre serveurs déclarés avec scopes et risque ; `@playwright/mcp` épinglé | `grimoire standard verify .` vert, gate bootstrap OK |

Dépendance : aucune. Risque : ces hooks tournent dans la session courante ; travailler dans un worktree Forge sur branche `fix/gardes-fail-closed-budget`, PR, puis merge par Guilhem.

### Lot B — Kit, sécurité et mémoire (Sonnet + revue Opus)

| Action | Fichiers | Critère d'acceptation | Check |
|---|---|---|---|
| B4 Validation des écritures mémoire | `src/grimoire/memory/manager.py`, `src/grimoire/mcp/server.py` (memory_store), `core/standard_checks/verifiers.py` | Schéma de contenu (type, taille max, champs), liste d'émetteurs autorisés, redaction exécutée quand `required` ; écriture refusée avec erreur nommée | Tests : écriture hors schéma refusée, émetteur inconnu refusé, redaction appliquée ; le test échoue si la validation est retirée |
| B12 Contenu externe marqué | `framework/tools/web-browser.py` (zone gelée : ne pas grossir), `src/grimoire/` (nouveau module d'enveloppe), `framework/event-log-shared-state.md`, `agentic-standard/profile-map.yaml` | Sortie web et messages ELSS enveloppés d'un marqueur « donnée externe, pas instruction » ; `prompt_firewall` requis dès `governed` | Tests d'enveloppe ; `standard verify` sur un projet governed exige l'artefact |

Dépendance : B12 après B4 (même zone `server.py`). Revue Opus obligatoire sur les deux.

### Lot C — Kit, orchestration et plafonds (Sonnet)

| Action | Fichiers | Critère d'acceptation | Check |
|---|---|---|---|
| B3 Verrou `exclusive_files` | `src/grimoire/missions/ledger.py`, `service.py`, `schemas.py` | Un claim dont les fichiers chevauchent un claim CLAIMED ou IN_PROGRESS est refusé avec `TaskRefusedError` nommant le fichier et la tâche | Test de chevauchement ; test que le retrait du contrôle fait échouer |
| B11 Plafonds MAST comptés | `src/grimoire/runtime/recipes.py` (consommer `retry_profile`), `src/grimoire/runtime/kernel.py` (max tours et budget), P2P : compteur côté `src/` car `framework/tools/message-bus.py` est gelé | Retry au-delà de `max_retries` refusé ; kernel refuse au-delà du plafond ; compteur P2P émet un événement SOG au cinquième échange | Tests unitaires par plafond |
| B10 Sous-agents bornés | `src/grimoire/hosts/emitters/claude_code.py` | Frontmatter généré avec `effort` (mapping affinité), `maxTurns`, `background` ; `host sync` idempotent | Test d'émission ; `test_delivered_paths_resolve` vert |

Dépendance : aucune entre eux ; trois PR distinctes ou une seule si le codeur préfère, sans PR empilées.

### Lot D — Kit, outils et MCP (Sonnet + revue Opus sur D1)

| Action | Fichiers | Critère d'acceptation | Check |
|---|---|---|---|
| B5 Vérificateur `tools.mediated-before-use` | `src/grimoire/core/standard_checks/`, `framework/agentic-standard/capability-map.yaml`, `templates/pattern-catalog.yaml` | Le check échoue si un outil ou serveur MCP actif n'est pas déclaré dans `tool-registry.yaml` avec un risque ; `governed` l'exige | Test sur projet fixture : registre vide → échec |
| B9 Serveur MCP annoté | `src/grimoire/mcp/server.py`, `pyproject.toml` | 21 outils avec annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`), erreurs en `isError`, borne haute du SDK, note de migration 2026-07-28 dans `docs/mcp-integration.md` | Test qui énumère les outils et exige une annotation ; smoke stdio |
| B14b Docs fictives | `framework/mcp/grimoire-mcp-server.md`, `framework/workflows/state-checkpoint.md` | Supprimés ou marqués obsolètes en tête avec pointeur vers le réel | `test_delivered_paths_resolve` vert |

Dépendance : B5 avant que la Forge repasse `verify` (lot A4 fournit le registre).

### Lot E — Kit, observabilité et évals (Sonnet)

| Action | Fichiers | Critère d'acceptation | Check |
|---|---|---|---|
| B7 Export OTel | `src/grimoire/traces/ledger.py`, `src/grimoire/tools/blueprint_telemetry.py` | Horodatage réel des événements, `gen_ai.provider.name`, `gen_ai.operation.name`, span enfant `execute_tool {tool}`, `gen_ai.conversation.id` ; un seul exportateur ; `EVENT_SOURCES` découvre les sous-dossiers réels | Test qui échoue sur horodatage nul ; export non vide sur une fixture Forge |
| B13 Évals | `evals/runner.py`, `evals/aggregate.py`, `evals/tasks/*.yaml`, `src/grimoire/evals/schemas.py` | pass^k calculé sur les répétitions existantes ; étiquette `capability` ou `regression` par tâche ; coût par sous-agent quand la CLI l'expose | Tests d'agrégation |

Dépendance : aucune.

### Lot F — Cohérence du socle (Sonnet, puis décision Opus)

| Action | Fichiers | Critère d'acceptation | Check |
|---|---|---|---|
| B14a AORA, PIP, DCF | `framework/agent-base.md`, `agent-base-compact.md`, `orchestrator-gateway.md` | Statut tranché et identique dans les trois fichiers ; cohérent avec la doctrine des projets consommateurs | Relecture Opus ; `test_agent_base_default` vert |
| B15 Instructions Forge | `.github/copilot-instructions.md`, `AGENTS.md`, `grimoire-master.agent.md` | Moins de 200 lignes chargées ; doctrine en un seul endroit, référencée ailleurs | Comptage ; hooks-smoke |

Dépendance : B14a exige une décision de Guilhem si les experts divergent.

## 3. Ordonnancement

Vague 1 (parallèle) : A, C, E. Vague 2 (parallèle, après relecture Opus des prompts) : B, D. Vague 3 : F. Chaque PR passe le vérificateur Haiku avant d'être présentée ; les lots B et D passent en plus la revue Opus.

## 4. Contraintes opposables aux codeurs

- Worktree jetable sur `origin/main` du kit, branche par lot, jamais de PR empilée, jamais `git add -A`.
- Zone gelée `framework/*.py` et `*.sh` : aucune ligne en plus ; toute capacité nouvelle vit sous `src/grimoire/`.
- Titre de PR avec préfixe conventionnel (`fix:` ou `feat:`) ; pas d'étiquette `type:*`.
- Vérifier dans les conditions de la CI : `pytest` ciblé puis suite complète, `ruff`, `python scripts/check-code-ratchet.py`.
- Écrire d'abord le test qui fait échouer le garde, puis le garde (gardes qui échouent ouvert = mode de panne dominant).
- Rapport final du codeur : 300 mots maximum, commandes exécutées et résultats, URL de PR, ce qui n'a pas été fait.

## 5. Ce que concierge fait lui-même

Rédige les prompts de lot à partir de ce plan, lance les codeurs, lit les rapports, lance les vérificateurs, arbitre les désaccords, consigne la preuve dans le pack bootstrap, met à jour l'issue épique. Rien d'autre.

## 6. Relecture experte avant dispatch

- Opus : ordre des vagues, risques de collision entre lots, critères d'acceptation manquants, conflits avec la doctrine, ce qui doit remonter à Guilhem.
- Sonnet : pour chaque action, fichiers réels à toucher, tests existants à étendre, pièges de zone gelée, estimation en lignes.

Les retours sont intégrés en section 7 avant tout dispatch.

## 7. Amendements après relecture

Relecture Opus (verdict GO avec douze amendements) et fiche de faisabilité Sonnet (seize fiches, tableau des collisions). Tout est intégré ci-dessous ; les décisions prises par défaut par le concierge sont marquées « défaut » et restent révocables par Guilhem.

### Ordonnancement corrigé

- A3 devient une action kit : `HookEvent` et l'émetteur Claude Code ne connaissent pas `SubagentStart` ; câbler à la main dans la Forge serait écrasé par `host sync`. A3 rejoint le lot C (kit) ; côté Forge, le lot A rétrograde le hook mort en `shadow` avec une note, jusqu'à la release du kit.
- B9 rejoint le lot B (même fichier `server.py` que B4) ; B5 aussi (même `verifiers.py` que B4, même répertoire `agentic-standard/` que B12). Le lot B devient une seule branche travaillée séquentiellement : B4, B9, B12, B5. Lot D réduit à B14b, fusionné dans le lot F-kit.
- Lot F scindé par dépôt : F-kit (B14a, B14b), F-Forge (B15).
- Ordre cross-repo verrouillé : A4 mergé sur la Forge avant toute release du kit portant B5.
- B11 recadré : aucun exécuteur de recettes n'existe sous `src/grimoire/runtime/`, la consommation de `retry_profile` est retirée du lot. B11 = plafond de tours et de budget par instance dans le kernel (état `refused` + checkpoint), plus un compteur P2P dans un module `src/grimoire/` qui observe les événements du bus (le bus est gelé).
- Vagues : vague 0 en parallèle = A, C, E, F-kit, B11 (fichiers disjoints, cinq worktrees) ; vague 1 = B (Opus) après les rapports de la vague 0 ; vague 2 = F-Forge.

### Décisions prises par défaut (révocables)

1. AORA et DCF : retirés du socle du kit ; PIP : observer-only. C'est la décision déjà consignée dans le CHANGELOG du kit (2026-07-12) et dans la doctrine des projets consommateurs, jamais répercutée dans les `.md` du socle. Le circuit breaker et la cascading initiative sont conservés comme règles autonomes de la section « Plan d'exécution », car ce sont les cibles de B11. Défaut.
2. `prompt_firewall` : requis au profil `production`, avertissement au profil `governed`. Rendre l'artefact requis dès `governed` rendrait tout projet consommateur non conforme du jour au lendemain. Défaut.
3. `isError` : ajouté en plus du corps JSON `{"error": ...}` existant, jamais à la place. Défaut.
4. Identité par agent (ASI03) : risque accepté et consigné dans `accepted-risks.yaml` de la Forge tant que les agents restent locaux. Défaut.
5. Registre MCP (A4) et vérificateur (B5) : le périmètre inclut les serveurs de portée utilisateur résolus à l'exécution, pas seulement `.mcp.json` ; tout serveur non déclaré doit être explicitement listé hors périmètre. Sinon le vérificateur naît fail-open.
6. B4 : la validation de contenu refuse immédiatement (schéma, taille) ; la liste d'émetteurs autorisés démarre en mode observation (événement, pas refus) car l'acteur MCP est générique.
7. B3 : le claim porte une expiration ; un refus nomme le détenteur, la tâche et le fichier.

### Critères d'acceptation ajoutés

- A1 : JSON invalide ou vide renvoyé par le script = `ask`, événement tracé.
- A2 : un test échoue si `token-budget.py` disparaît de `.github/hooks/lib/` ; dépassement de budget = refus nommé.
- B5 : le check échoue aussi quand le registre est peuplé mais périmé par rapport aux serveurs résolus.
- B7 : fixture synthétique dans le repo kit, jamais de dépendance à des artefacts Forge ; export versionné.
- B11 : au plafond, le kernel passe l'instance en `refused`, écrit un checkpoint, émet un événement ; pas d'exception silencieuse.
- B13 : pass^k défini comme la proportion de tâches réussies à toutes les k répétitions exécutées, k = `repetitions_min` ; un run non exécuté n'est ni succès ni échec.
- B15 : « lignes chargées » = lignes de `CLAUDE.md` plus celles de chaque import résolu ; mesuré par un script versionné.

### Répartition des modèles corrigée

- Opus code le lot B (frontière de confiance, contrat MCP, vérificateur governed) ; Sonnet en revue adversariale du lot B, Haiku en vérification.
- Sonnet code A, C, E, F-kit, B11 ; Haiku vérifie chacun.
- Haiku code F-Forge (B15) après mesure par script.
- Relecteur inter-lots : un Sonnet compare les branches de la vague 0 avant présentation des PR (fichiers touchés, conflits, critères).

### Contraintes ajoutées aux codeurs

- Interdit de travailler dans `grimoire-kit/` (clone servi par `.mcp.json` à la session) : worktree jetable obligatoire.
- Interdit de toucher `.claude/settings.json` de la Forge à la main.
- Tout garde nouveau est livré avec le test qui le fait échouer.
