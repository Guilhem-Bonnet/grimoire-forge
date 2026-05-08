# 03 — Gap Analysis des hooks

> Les hooks sont **présents, gatés, et en enforced**. Mais ils ne produisent pas encore de valeur visible pour l'utilisateur. Analyse et durcissement.

## Cadre de référence

- Contrat officiel : [VS Code Copilot Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- Gateway local : [.github/hooks/scripts/grimoire-hook-gateway.sh](../../../.github/hooks/scripts/grimoire-hook-gateway.sh)
- Registry sécurité : [_grimoire-runtime/_config/hook-safety-registry.json](../../../_grimoire-runtime/_config/hook-safety-registry.json)
- Instruction repo : [.github/copilot-instructions.md](../../../.github/copilot-instructions.md) — section "Hook promotion guard"

## Inventaire courant vs. événements disponibles

### Couverts (9/9 événements Copilot natifs)

| Événement | Hook Grimoire | Mode | Utilité actuelle |
|---|---|---|---|
| `SessionStart` | `grimoire-session-start.sh` | enforced | Injecte contexte (charge config.yaml, alertes preflight) |
| `UserPromptSubmit` | `grimoire-prompt-submit.sh` | enforced | Audit prompt, rappel hooks et task-flow |
| `PreToolUse` | `grimoire-memory-guard.sh` | enforced | Bloque écriture `_grimoire-runtime/_memory/` hors pattern autorisé |
| `PreToolUse` | `grimoire-control-surface-guard.sh` | enforced | Bloque patterns destructifs (rm -rf /, git push --force sans flag, etc.) |
| `PostToolUse` | `grimoire-post-edit.sh` | enforced | Valide ruff + bash -n + JSON hooks + frontmatter YAML |
| `SubagentStart` | `grimoire-subagent-context.sh` | enforced | Injecte contexte sub-agent concis |
| `SubagentStart/Stop` | `grimoire-subagent-trace.sh` | enforced | Trace transitions vers `GRIMOIRE_TRACE.jsonl` |
| `PreCompact` | `grimoire-pre-compact.sh` | enforced | Capsule de contexte avant summarization |
| `Stop` | `grimoire-master-stop-hook.sh` | enforced | Empêche clôture sèche, demande résumé |

### État du registry

- Tous les hooks validés `2026-04-16T20:36:50Z`
- Tous en mode `enforced` (pas de `shadow` ni `canary` en cours)
- Chaque script a son empreinte SHA enregistrée — un drift force un rétrogradage automatique

## Trous identifiés

### Trou 1 : Pas d'émission vers un bus consommable

**Constat** : `grimoire-subagent-trace.sh` écrit dans `GRIMOIRE_TRACE.jsonl`. Mais ce fichier n'est lu par **aucune surface**. Le Mission Board ne sait pas qu'un sub-agent a démarré.

**Conséquence** : la valeur démo du Kanban live tombe à zéro. L'utilisateur voit un mock, pas son agent.

**Correctif proposé (V1)** :

- Définir un schéma JSON unifié `GrimoireEvent` (voir `06-PLAN-execution-phases.md` V1)
- `grimoire-subagent-trace.sh` + `grimoire-post-edit.sh` + `grimoire-prompt-submit.sh` émettent le même format
- Un endpoint `server/control-plane/events` (déjà structuré dans `grimoire-game/src/server/`) consomme le JSONL ou reçoit en push WebSocket
- Les surfaces s'abonnent au `GameState` dérivé

### Trou 2 : Format d'événement hétérogène

**Constat** : chaque script utilise son propre format (certains JSONL, d'autres texte, d'autres Markdown append).

**Impact** : difficile de construire un `GameState` cohérent. Chaque surface devrait connaître 9 formats.

**Correctif (V1)** :

- Schéma commun avec `event_id`, `timestamp`, `scope` (`session|prompt|tool|subagent|compact|stop`), `payload`, `source_hook`
- Chaque script convertit avant d'émettre
- Test de contrat : parsing JSONL round-trip

### Trou 3 : Pas de compteurs d'erreur consommables

**Constat** : quand `grimoire-post-edit.sh` bloque un ruff fail ou un bash -n fail, le compteur d'échec n'est pas exposé. Impossible de surveiller "combien de fois cette session a été corrigée par le hook ?".

**Correctif (V1 + V3)** :

- Émettre `GrimoireEvent` `tool.blocked` et `tool.corrected`
- Les afficher en `observability` (dashboard simple : compteurs roulants 24h)
- Alimenter `_grimoire-runtime/_memory/failure-museum.md` automatiquement au lieu d'update manuel

### Trou 4 : Pas de pont hooks ↔ `_grimoire-runtime/_memory/activity.jsonl`

**Constat** : `activity.jsonl` existe (ligne workspace_info), mais les hooks n'y écrivent pas de façon disciplinée. Les sources sont dispersées.

**Correctif (V1)** :

- Un seul point d'émission centralisé : `grimoire-hook-gateway.sh` pousse tout `GrimoireEvent` validé dans `activity.jsonl`
- Ledger append-only, avec un seul writer : le gateway

### Trou 5 : Pas de mécanisme de replay / time-travel

**Constat** : `GRIMOIRE_TRACE.jsonl` est append-only, mais aucune UI ne permet de scrub.

**Correctif (V3)** :

- Ajouter un panneau `observatory.html` avec slider de temps
- Rejouer l'état agent (déplacements, status) depuis la trace
- Pattern timeline scrubber présent dans skill `grimoire-pixel-observatory`

### Trou 6 : Aucune détection de boucle ou burst

**Constat** : si un sub-agent boucle (même tool appelé 30 fois en 2 min), aucun hook ne signale.

**Correctif (V4)** :

- `grimoire-subagent-trace.sh` calcule une fenêtre glissante
- Émet `GrimoireEvent` `anomaly.burst` quand seuil dépassé
- Alimenter antifragile-history + alerte cockpit

### Trou 7 : Pas d'instrumentation des tasks VS Code

**Constat** : `.vscode/tasks.json` déclenche `grimoire-task-flow.sh` mais l'instrumentation task-flow n'est pas un hook natif (les hooks Copilot ne couvrent pas `tasks.json`).

**Correctif (V1 complément)** :

- Documenter clairement : task-flow est un shim non-hook
- Émettre les mêmes `GrimoireEvent` depuis `grimoire-task-flow.sh` que depuis les hooks
- Mentionner dans `.github/copilot-instructions.md` la séparation (déjà amorcé : section "Hooks vs tasks")

## Durcissement proposé

### D1 — Schéma `GrimoireEvent` versionné

```json
{
  "schema_version": "1.0",
  "event_id": "uuid",
  "ts": "2026-04-21T14:22:31.004Z",
  "scope": "subagent|tool|prompt|session|compact|stop|task|anomaly",
  "phase": "start|end|block|correct",
  "source_hook": "grimoire-post-edit.sh",
  "agent": { "id": "…", "role": "dev", "parent": "grimoire-master" },
  "payload": { "free": "form" },
  "correlation_id": "…"
}
```

### D2 — Contrat de sortie strict pour chaque script

- Exit code 0 : succès, événements émis
- Exit code 2 : bloqué (contrat Copilot `permissionDecision: deny`), `decision: block` stdout
- Exit code 1 : erreur non bloquante, logged dans `hook-runtime/errors.jsonl`
- Tout script doit émettre ≥ 1 `GrimoireEvent` ou justifier l'abstention dans un commentaire `# NO-EVENT: <raison>`

### D3 — Test de contrat unifié

- Script `framework/tools/hook-contract-test.py` (à créer en V1)
- Rejoue des payloads fixtures sur chaque hook
- Valide schéma + exit codes + side effects (pas d'écriture hors zones autorisées)

### D4 — Promotion/rétrogradage automatique

- `grimoire-hook-gateway.sh` détecte un drift SHA → force mode `shadow`
- `hook-safety-gate.py set-mode shadow <hook>` gère la bascule manuelle
- Task `grimoire: hooks-smoke` rejoue tous les contrats et peut promouvoir si tests verts (flag `--promote`)

### D5 — Observability dédiée aux hooks

- Nouvel endpoint `observability` : compteurs par hook sur fenêtre 1h/24h/7j (blocks, corrections, events émis)
- Alimenté par `activity.jsonl` (writer unique : gateway)

## Priorisation du durcissement

| Item | Vague | Impact utilisateur |
|---|---|---|
| D1 Schéma unifié | V1 | Prérequis de tout |
| D2 Contrats scripts | V1 | Prérequis de V2 et V3 |
| D3 Tests de contrat | V1 | Évite régressions |
| D4 Drift handling | V4 | Déjà en place partiellement, durcir en V4 |
| D5 Observability hooks | V3 | Démontre à l'utilisateur que "ça vit" |

## Décisions à confirmer

Inscrites comme ouvertes dans `05-DECISIONS-rationalisation.md` :

1. Canal de transport des événements : JSONL polling vs. WebSocket vs. Server-Sent Events ?
2. Bus runtime : Python (dans `src/grimoire/tools/`) vs. TS (`grimoire-game/src/server/`) ?
3. Garder `activity.jsonl` au root `_grimoire-runtime/_memory/` ou le migrer sous `_grimoire-runtime-output/hook-runtime/` ?
