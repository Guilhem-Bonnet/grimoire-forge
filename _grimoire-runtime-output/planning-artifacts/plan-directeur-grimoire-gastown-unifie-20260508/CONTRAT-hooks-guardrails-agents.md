---
title: Contrat hooks guardrails agents
description: Contrat d'execution pour adapter le nouveau plan aux agents, hooks, guardrails, policies, evidence et verification.
author: Codex
date: 2026-05-08
---

# Contrat hooks guardrails agents

## But

Ce contrat fixe comment les agents doivent executer le plan directeur sans recreer une orchestration fragile.

Principe :

```text
Les agents executent.
Les hooks encadrent.
Les guardrails autorisent ou refusent.
Le ledger garde la source de verite.
La verification decide de la fermeture.
Le cockpit explique.
```

## Evenements canoniques

| Event | Role | Mutation autorisee |
| --- | --- | --- |
| `mission.created` | Nouvelle mission ou import de plan | Creer mission, jamais close |
| `task.created` | Nouvelle task atomique | Creer task avec provenance |
| `task.qualified` | Classification type, risque, preuve | Ajouter metadata, pas executer |
| `task.claimed` | Agent prend ownership | Claim atomique avec actor |
| `workflow.started` | Instance de recipe lancee | Ouvrir run et trace |
| `workflow.checkpointed` | Etat durable intermediaire | Ecrire checkpoint |
| `tool.requested` | Tool ou commande demandee | Preparer policy verdict |
| `tool.completed` | Tool termine | Ajouter evidence candidate |
| `verification.requested` | Fermeture demandee | Ouvrir verification queue |
| `verification.failed` | Gate refusee | Reouvrir ou bloquer |
| `verification.passed` | Gate acceptee | Autoriser closure |
| `task.closed` | Task terminee | Fermer avec evidence |
| `incident.created` | Blocage, stall, conflit ou policy fail | Ouvrir incident |
| `memory.promoted` | Memoire durable creee | Lier provenance et task |
| `pack.activated` | Pack active | Ecrire policy verdict et lock |

## Hooks host

| Hook host | Usage Grimoire | Sortie attendue |
| --- | --- | --- |
| `UserPromptSubmit` | Triage initial, rappel proceduriel, detection plan ancien, routing vers Mission Ledger | `task.created` ou contexte enrichi |
| `SessionStart` | Injection contexte borne, host identity, policies actives | Capsule contexte avec provenance |
| `PreToolUse` | Policy check, command guard, memory guard, terminal guard | `allow`, `warn` ou `block` avec raison |
| `PostToolUse` | Evidence capture, doc drift, mutation audit, output scoring | Evidence candidate ou warning |
| `SubagentStart` | Context capsule, task binding, actor binding | Trace liee a task |
| `SubagentStop` | Evaluation sortie, trust score, failure capture | Score et event de resultat |
| `PreCompact` | Resume, learning candidate, memory promotion candidate | Summary et memory candidates |
| `Stop` | Session closure, incomplete work report, hook ledger flush | Evidence/session lineage |

## Modes de hook

| Mode | Sens | Usage |
| --- | --- | --- |
| `shadow` | Observe sans influencer | Nouveaux controles ou heuristiques |
| `canary` | Peut avertir et collecter preuve | Controle presque stable |
| `enforced` | Peut bloquer | Controle deterministe ou policy critique |

Aucun hook ne passe `enforced` sans digest, control files, test ou smoke, et raison de blocage comprehensible.

## Guardrails obligatoires

### Guardrail 1 - Source de verite

Un agent ne peut pas fermer une task si la fermeture n'est pas inscrite dans le Mission Ledger.

### Guardrail 2 - Evidence first

Une task critique ne peut pas passer `done` sans `EvidencePack`.

### Guardrail 3 - Policy before tool

Un tool mutateur doit produire un `PolicyVerdict` avant execution.

### Guardrail 4 - Memory provenance

Une memoire injectee dans un run critique doit porter source, fraicheur et task ou doc ref.

### Guardrail 5 - Pack activation

Un pack ne peut pas activer commandes, services ou hooks sans manifest valide et lock.

### Guardrail 6 - Host capability

Un host qui ne supporte pas les hooks doit passer par fallback CLI/API et ne peut pas pretendre au meme niveau de controle.

### Guardrail 7 - No silent stall

Un workflow sans progression devient `incident.created`, `blocked`, `paused`, `escalated` ou `cancelled`. Il ne reste jamais invisible.

### Guardrail 8 - No hidden source

Une UI, un pack, un hook ou une memoire ne cree pas un etat metier parallele.

## Profils de preuve

| Profil | Quand l'utiliser | Preuve minimale |
| --- | --- | --- |
| `light` | Doc, triage, analyse non mutatrice | Source et decision |
| `standard` | Implementation normale | Test cible ou validation comportementale |
| `strict` | Runtime, ledger, pack, guardrail | Test, replay ou schema validation |
| `security_critical` | Secrets, policies, MCP, shell, external tools | Refus negatif, audit trail, policy explicite |
| `release` | Publication de pack ou version | Doctor, lock, changelog, compatibility, evidence |

## Contrat de task

```yaml
task:
  id: GAO-EXAMPLE
  title: Exemple de tache
  surface: grimoire-kit
  type: implementation
  risk: strict
  origin: plan-directeur
  dependencies: []
  acceptance:
    - schema valide
    - tests de replay
  hooks:
    entry:
      - UserPromptSubmit
      - task.qualified
    execution:
      - PreToolUse
      - PostToolUse
    exit:
      - verification.requested
      - task.closed
  guardrails:
    - Evidence first
    - Policy before tool
  evidence:
    profile: strict
    expected:
      - tests
      - docs
      - ledger event
```

## Contrat de pack

Un pack valide declare :

- `name`;
- `version`;
- `status`;
- `owner`;
- `source`;
- `compatibility`;
- `components`;
- `commands`;
- `doctor`;
- `services`;
- `policies`;
- `tests`;
- `permissions`;
- `activation`.

Un pack converti depuis Gas City reste `experimental` tant que les commands et services n'ont pas de policy Grimoire-native.

## Contrat de provider

Chaque provider host doit publier un `Capability Manifest` :

| Champ | Role |
| --- | --- |
| `hostId` | Identite du host |
| `supportsHooks` | Hooks disponibles |
| `supportsMcp` | MCP disponible |
| `supportsStreaming` | Streaming utilisable |
| `supportsWorkspaceMutation` | Peut modifier le workspace |
| `supportsToolPolicy` | Peut appliquer une policy avant tool |
| `fallbackMode` | CLI, API, instructions only |

Le routing agentique doit choisir workflow et verification selon ce manifest.

## Regles de conception

- Hooks courts, logique durable dans outils versionnes.
- Guardrails deterministes avant blocage.
- Warnings permis si heuristique.
- Toutes les mutations critiques produisent event, policy et evidence.
- Tout fallback doit garder les memes identifiants metier.
- Aucun agent interne ne devient user-facing sans decision explicite.

