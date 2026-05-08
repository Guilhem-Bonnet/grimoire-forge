# 05 — Décisions de rationalisation (ADR-synthèse)

> Décisions groupées pour ce pack. Chacune sera formalisée en ADR individuel au moment de l'exécution de la vague concernée.

## Format

- **Statut** : `proposé` (ce pack) → `accepté` (au go de la vague) → `implémenté` (au merge) → `superseded` si remplacé
- **Portée** : quelle vague V1/V2/V3/V4 consomme la décision
- **Irréversibilité** : facile / moyen / difficile

## ADR-S01 — Bus d'événements unifié `GrimoireEvent`

- **Statut** : proposé
- **Portée** : V1
- **Décision** : Tous les hooks et tasks Grimoire émettent un objet `GrimoireEvent` (schéma défini dans `03-GAP-ANALYSIS-hooks.md` D1). Un seul writer (le gateway) persiste dans `_grimoire-runtime/_memory/activity.jsonl`.
- **Alternatives écartées** : laisser chaque script écrire son propre format (statu quo → rend impossible la consommation par les surfaces).
- **Irréversibilité** : moyen (changer le schéma imposerait une migration). Versionner par `schema_version`.

## ADR-S02 — Transport événements → surfaces via WebSocket

- **Statut** : proposé
- **Portée** : V1
- **Décision** : Les surfaces (`cockpit`, `mission-board`, `observatory`) s'abonnent au serveur `grimoire-game/src/server/control-plane/` via WebSocket. Fallback polling JSONL en dégradé.
- **Alternatives** : SSE (proche mais moins bidirectionnel), pure JSONL polling (simple mais latence perceptible sur démo).
- **Irréversibilité** : facile (contrat client/server isolé).

## ADR-S03 — GameState est le canon des surfaces

- **Statut** : accepté (déjà en place implicitement)
- **Portée** : V1 → V3
- **Décision** : Une seule store `GameState` (déjà présent dans `apps/grimoire-game/src/state/`) reçoit les `GrimoireEvent` et dérive les vues. Aucune surface n'a son propre store.
- **Conséquence** : Mission Board, Office View, Observability sont des **projections** de `GameState`, pas des silos.

## ADR-S04 — Mission Board adopte la taxonomie de rôles Switchboard

- **Statut** : proposé
- **Portée** : V2
- **Décision** : Colonnes du Mission Board alignées sur les rôles Switchboard (Planner, Lead Coder, Coder, Reviewer, Acceptance, Analyst, Intern), mappés sur nos sub-agents SOG.
- **Alternatives** : colonnes "workflow phase" (discovery/build/qa/ship) — plus proche de BMM mais moins reconnaissable. Possible de garder les deux modes (toggle UI) en V2+.
- **Irréversibilité** : facile (UI configurable).

## ADR-S05 — Drag→trigger passe par SOG, pas par terminal direct

- **Statut** : proposé
- **Portée** : V2
- **Décision** : Un drag sur une carte → appel SOG avec `runSubagent` ciblant l'agent mappé à la colonne destination. Jamais d'injection directe dans un terminal.
- **Alternative écartée** : reproduire `terminal.sendText` Switchboard → rompt SOG, bypasse HUP/CVTL.
- **Irréversibilité** : moyen (contrats d'interaction visibles).

## ADR-S06 — Pas d'extension VS Code additionnelle

- **Statut** : proposé
- **Portée** : ce pack
- **Décision** : Pixel Agents et Switchboard restent forks de lecture. Aucune extension Grimoire n'est packagée maintenant. Si le besoin émerge (V5+), pack séparé.
- **Motivation** : limiter la surface, la SPA cockpit + hooks natifs suffisent pour la maturité visée.

## ADR-S07 — Office View branché sur `GameState`, pas sur JSONL Claude

- **Statut** : proposé
- **Portée** : V3
- **Décision** : La vue bureau style Pixel Agents dérive l'état depuis `GameState` (peuplé par V1). On NE reproduit PAS le parser JSONL Claude Code.
- **Motivation** : un seul canal d'événements, agent-agnostic, intégré au SOG.

## ADR-S08 — Registre BM-* figé dans `_grimoire-runtime/_memory/bm-registry.md`

- **Statut** : proposé
- **Portée** : V4
- **Décision** : Produire un fichier unique `bm-registry.md` listant les 42 IDs référencés + les trous (IDs non trouvés). Source de vérité pour créer/archiver de nouveaux concepts.
- **Irréversibilité** : moyen (futurs IDs numérotés à partir de ce registre).

## ADR-S09 — Archiver BM-23 et BM-59

- **Statut** : proposé
- **Portée** : V4
- **Décision** : BM-23 (Semantic routing 3-niveaux) et BM-59 (ELSS) sont archivés. Remplacés par `llm_router.py` et dispatch SOG respectivement.
- **Procédure** : marquer `# ARCHIVED BM-XX — 2026-04-** — <motif>` en tête des fichiers concernés + supprimer références dans `.github/copilot-instructions.md`.

## ADR-S10 — Les forks `apps/pixel-agents-fork` et `apps/switchboard-fork` restent **en lecture seule**

- **Statut** : accepté
- **Portée** : ce pack
- **Décision** : aucune modification, aucun `npm install` dans ces répertoires en CI Grimoire. Ils sont matière première de copier-mental. Un `.gitkeep` ou `README.ref.md` documente la politique.
- **Optionnel** : déplacer vers `grimoire-kit/refs/` pour signaler l'intention.

## ADR-S11 — Une seule vague en cours à la fois

- **Statut** : proposé
- **Portée** : ce pack
- **Décision** : V1 → V2 → V3 → V4 strictement séquentiel. Pas de travail parallèle sur plusieurs vagues pour préserver la cohérence `GameState`.
- **Motivation** : chaque vague crée des contrats consommés par la suivante. Paralléliser = rebase perpétuel.

## ADR-S12 — Maturation documentaire en fin de vague

- **Statut** : proposé
- **Portée** : V1/V2/V3/V4
- **Décision** : Chaque vague produit en clôture un pack planning-artifact dédié avec DOC-TECHNIQUE + GUIDE-utilisation (convention repo), et met à jour [docs/exploitation/plan-maitre-agent-os-game-ui.md](../../../docs/exploitation/plan-maitre-agent-os-game-ui.md).
- **Motivation** : la documentation suit l'exécution, pas l'inverse. Évite l'effet "doc dette".

## Décisions ouvertes à trancher avant V1

| # | Question | Recommandation par défaut |
|---|---|---|
| O1 | Canal transport événements | WebSocket (S02) — confirmer à l'entrée de V1 |
| O2 | Bus serveur en Python ou TS ? | TS (déjà dans `grimoire-game/src/server/`) + client Python léger |
| O3 | Renommer `apps/*-fork/` → `refs/*/` ? | Oui, en V4 |
| O4 | Activer Qdrant par défaut ? | Non, rester opt-in BM-22 |
| O5 | Mode dégradé hors réseau/WS | Polling JSONL toutes les 2s |

## Ce que ces décisions N'IMPOSENT PAS

- Aucun choix de framework UI nouveau (on reste Svelte/Vite déjà présent)
- Aucune nouvelle dépendance Python
- Aucune migration de `_grimoire-runtime/`
- Aucune remise en cause de la charte graphique v20260417p/q
