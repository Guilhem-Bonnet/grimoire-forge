# DOC-TECHNIQUE — Maturation Agentique

> Contrat technique du pack planning-artifact `maturation-agentique-20260421`.

## Identité

- **Slug** : `maturation-agentique-20260421`
- **Type** : planning-artifact durable (audit + plan pluri-vagues)
- **Version** : 1.0
- **Date** : 2026-04-21
- **Langue** : Français
- **Statut** : proposé (à valider par l'utilisateur pour déclencher V1)

## Portée

Ce pack **ne modifie aucun code**. Il établit :

1. Un **audit mesuré** de l'état existant (surfaces, runtime, hooks, concepts, métriques)
2. Une **extraction documentée** des patterns utilisables depuis 2 forks de référence (Pixel Agents, Switchboard)
3. Une **analyse des trous** dans la chaîne hooks
4. Un **registre figé** des 42 concepts BM-*
5. Un **plan d'exécution** en 4 vagues séquentielles
6. Une **baseline métrique** pour piloter la progression

## Prérequis respectés

- [.github/copilot-instructions.md](../../../.github/copilot-instructions.md) : convention planning-artifact + documentation companions (ce fichier + GUIDE)
- [.github/instructions/markdown-standards.instructions.md](../../../.github/instructions/markdown-standards.instructions.md) : CommonMark strict, pas d'estimations temporelles
- [.github/instructions/artefact-governance.instructions.md](../../../.github/instructions/artefact-governance.instructions.md) : statut, preuve, compatibilité
- Chartier documentaire `_grimoire-runtime/_memory/tech-writer-sidecar/documentation-standards.md` (chargé à la rédaction)

## Inputs consommés

| Source | Usage |
|---|---|
| `.github/copilot-instructions.md` | Convention repo (SOG, hooks, UDF, structure) |
| `.github/agents/*.agent.md` | Inventaire des 23 agents |
| `.github/skills/grimoire-*/` | Inventaire des 41 skills |
| `.github/hooks/` + `hook-safety-registry.json` | Cartographie hooks |
| `_grimoire-runtime/` | Runtime BMM/CIS/BMB/TEA/core |
| `grimoire-kit/src/grimoire/tools/` | Modules canoniques |
| `grimoire-kit/framework/tools/` | Dette structurelle |
| `grimoire-kit/apps/grimoire-game/` | Runtime des surfaces |
| `grimoire-kit/apps/pixel-agents-fork/` | Référence office view |
| `grimoire-kit/apps/switchboard-fork/` | Référence Kanban drag→trigger |
| `docs/exploitation/benchmark-github-agent-os-game-ui.md` | Benchmark GM-* existant |
| `docs/exploitation/plan-maitre-agent-os-game-ui.md` | Plan maître antérieur |

## Outputs produits

Dans `_grimoire-runtime-output/planning-artifacts/maturation-agentique-20260421/` :

| Fichier | Rôle | Consommateur |
|---|---|---|
| `README.md` | Index + synthèse 30s | Utilisateur (entrée) |
| `01-AUDIT-etat-existant.md` | Inventaire mesuré | Équipe livraison V1+ |
| `02-EXTRACTIONS-refs.md` | Plans d'adaptation forks | V2 + V3 |
| `03-GAP-ANALYSIS-hooks.md` | Trous + durcissements | V1 (D1-D3) + V4 (D4-D6) |
| `04-CARTOGRAPHIE-concepts.md` | Registre BM-* éclaté | V4 |
| `05-DECISIONS-rationalisation.md` | ADR synthèse (12 items) | Toutes vagues |
| `06-PLAN-execution-phases.md` | Roadmap 4 vagues + gates | Utilisateur + packs V1-V4 |
| `07-METRIQUES-baseline.md` | Baseline mesurable + commandes | CI + sortie de chaque vague |
| `DOC-TECHNIQUE-maturation-agentique.md` | Ce fichier | Méta |
| `GUIDE-utilisation-maturation-agentique.md` | Comment consommer | Utilisateur |

## Invariants de ce pack

1. **Aucune estimation temporelle** (jours, semaines, sprints en durée). Les vagues sont définies par critère de sortie, pas par durée.
2. **Aucune modification de code** produite ici. Le code modifié arrivera dans les packs V1/V2/V3/V4.
3. **Aucune suppression** d'artefact ou concept sans ADR explicite (ADR-S09 pour BM-23/59, ADR-S10 pour forks).
4. **Aucune nouvelle dépendance** introduite dans ce pack.
5. **SOG préservé** : un seul agent user-facing dans toutes les vagues.

## Dépendances

### Lecture obligatoire avant consommation

- [.github/copilot-instructions.md](../../../.github/copilot-instructions.md)
- [_grimoire-runtime/_config/hook-safety-registry.json](../../../_grimoire-runtime/_config/hook-safety-registry.json)

### Dépendance des vagues

```text
V1 ──┬── V2 (Mission Board vivant)
     ├── V3 (Office View)
     └── V4 (Rationalisation)
```

V1 est bloquant pour V2/V3/V4. L'ordre V2 → V3 → V4 est recommandé mais pas obligatoire (ADR-S11 impose la sérialisation mais l'ordre entre V2/V3/V4 peut être ajusté au go).

## Contrat de validation

Ce pack est **validé** si :

- [x] Les 10 fichiers sont présents
- [x] Chaque section référence des preuves vérifiables (chemins, commandes, métriques)
- [x] Les ADR sont traçables vers une vague d'exécution
- [x] Les métriques baseline sont reproductibles
- [x] Le graphe de dépendances est cohérent
- [x] Les compagnons DOC-TECHNIQUE + GUIDE sont produits (convention repo)

Ce pack **passe à l'état "accepté"** quand l'utilisateur confirme les 3 éléments du Go/No-Go (voir `06-PLAN-execution-phases.md`).

## Traçabilité

- Conversation d'origine : session SOG 2026-04-21, demande utilisateur verbatim dans `README.md`
- Commits kit précédents de la session : 51b78181, 896d891e, f85f9242, 0c6a3378, 85b0c277, d4f549b9 (contexte refactor Task 4)
- Branche au moment de la production : `backup/main-before-origin-sync-20260415`

## Compatibilité

- **Amont** : CommonMark strict, compatible MkDocs Material (utilisé pour le site public)
- **Aval** : consommable par tout prochain pack V1-V4 via références relatives stables
- **Liens cassants** : aucun lien absolu (tout relatif au workspace)

## Risques de ce pack (pas des vagues)

| Risque | Probabilité | Mitigation |
|---|---|---|
| L'utilisateur refuse V1 → le pack devient dormant | Moyenne | Acceptable : le pack reste source de vérité pour futurs choix |
| Un concept BM-* identifié "archiver" est défendu par l'utilisateur | Faible | ADR-S09 révisable avant exécution V4 |
| Les forks sont supprimés avant exécution V2/V3 | Faible | Cloner localement dans `grimoire-kit/refs/` si besoin |

## Évolution prévue

- **V1.1** : mise à jour au go de l'utilisateur avec ses réponses aux décisions ouvertes O1-O5
- **V1.2** : corrections de faits détectées en exécution V1
- **V2.0** : refonte si une vague révèle une incohérence structurelle majeure

## Auteur & revue

- **Orchestrateur** : `grimoire-master` (SOG BM-53)
- **Sub-agents contributeurs virtuels** : `analyst` (audit), `architect` (décisions), `pm` (plan), `tech-writer` (rédaction)
- **Revue adverse** : à exécuter via skill `grimoire-code-review` ou sub-agent `rodin` au go de l'utilisateur (optionnel)
