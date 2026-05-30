## Resume

Decrivez clairement ce que fait cette pull request et pourquoi elle existe.

## Type de changement

- [ ] feat
- [ ] fix
- [ ] docs
- [ ] refactor
- [ ] test
- [ ] chore / ci / build / style / perf / revert

## Scope et ticket

Lien vers l'issue, la carte kanban ou le document de roadmap.

## Workflow GitHub

- [ ] Branche de travail hors `main`.
- [ ] Titre de PR au format Conventional Commits.
- [ ] Push direct sur `main` evite ; passage par PR obligatoire.

## Verification

- [ ] `grimoire: flow-quick`, `grimoire: quickcheck` ou equivalent rejoue.
- [ ] Lint passe.
- [ ] Tests passes.
- [ ] Preflight passe.
- [ ] Memory-lint passe.

## Review lanes

- [ ] Implementation et regression.
- [ ] QA et edge cases.
- [ ] Adversarial review ou architecture.
- [ ] Observabilite, memoire et retention.

## Risques et rollback

Principaux risques identifies, mitigation et rollback prevu.

## Observabilite et memoire

Preciser les traces, logs, retention, learnings ou artefacts memoire impactes.

## Documentation et templates

- [ ] README mis a jour si necessaire.
- [ ] Docs roadmap, vision et gouvernance mises a jour si necessaire.
- [ ] Templates, hooks ou skills mis a jour si necessaire.

## Checklist finale

- [ ] Les changements sont limites au scope.
- [ ] Les chemins de migration sont couverts.
- [ ] Aucun secret, log sensible ou bypass durable ajoute.
- [ ] Les reviewers pertinents sont assignes.
- [ ] La PR est prete pour review ou merge queue.
