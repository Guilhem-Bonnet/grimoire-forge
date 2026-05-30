---
description: "Conventions du runtime Game UI de Grimoire. Use when: editing grimoire-game TypeScript, Svelte components, WebSocket contracts, AgentAdapter, GameState, runtime auth, replay logic, contract tests."
applyTo: "grimoire-kit/apps/grimoire-game/**"
---

# Grimoire Game Runtime Conventions

## Structure

- `src/contracts/` porte la source de verite des evenements et schemas externes.
- `src/bridge/` encapsule le couplage au runtime Grimoire et expose `AgentAdapter`.
- `src/state/` porte `GameState`, les snapshots et l'hydration.
- `src/server/auth/` porte auth, RBAC et garde-fous write versus read-only.
- `tests/contracts/` couvre les schemas, versions et payloads invalides.
- `tests/integration/` couvre reconnect, replay, adapter mock et auth.

## Regles runtime

- Contract-first : toute evolution d'event commence par `src/contracts/` avant le transport, le store ou l'UI.
- Toute donnee qui traverse WebSocket, API ou adapter est validee explicitement.
- `GameState` reste la source unique de verite pour le board ; l'UI derive de cet etat et ne cree pas son propre modele concurrent.
- Le couplage direct aux details internes de Grimoire hors `src/bridge/` est interdit.
- Toute action write exige authz explicite et mode spectateur read-only verifiable.
- Replay, idempotence et resync font partie du comportement normal, pas d'un hardening reporte.

## Regles UI

- Une surface UI ne contourne jamais les contrats runtime pour aller plus vite.
- Les composants Svelte ou canvas restent presentationnels autant que possible ; la logique d'etat vit hors composant.
- Aucune room, HUD ou interaction canvas n'est fermee sans source d'etat stable et testee.

## Tests et preuves

- Tout changement de contrat met a jour au moins un test de contrat.
- Tout changement sur replay, reconnect, adapter ou auth met a jour un test d'integration.
- Une feature UI critique n'est pas consideree finie si les invariants runtime qui la portent restent non testes.

## Garde-fou de depot

- La toolchain Node reste locale a `grimoire-kit/apps/grimoire-game/` tant qu'une seule app TypeScript existe.
- Ne pas introduire de workspace JavaScript au niveau du depot racine sans nouvelle decision explicite.
