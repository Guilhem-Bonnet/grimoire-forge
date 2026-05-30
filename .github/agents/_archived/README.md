# Archive — Agents pré-SOG (BMAD era)

Ce dossier contient les versions **BMAD** des agents, antérieures à la migration SOG (BM-53).

## Pourquoi ils sont ici

Lors du passage au SOG (Smart Orchestrator Gateway), tous les agents ont été refactorisés :

| Avant (BMAD) | Après (SOG) |
|---|---|
| `user-invocable: true` | `user-invocable: false` |
| Descriptions persona-centrées | Descriptions intent-centrées (`Use when:`) |
| Outils larges (`read, edit, search, execute`) | Outils scopés au rôle |
| Pas de `handoffs` | `handoffs` définis explicitement |

## Source de vérité

**Les agents actifs sont dans `.github/agents/`** (dossier parent).

Ce dossier est un **archivage de référence uniquement**. Ne pas modifier, ne pas utiliser directement.

## Migration effectuée

Commit : `ec2c996 feat: SOG orchestrator + 10 intelligence protocols integration`
