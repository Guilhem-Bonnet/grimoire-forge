# Proof Pack

## Scope

- Ticket: `HOUSEKEEPING-20260415-ROOT-CAPTURES`
- Objective: sortir les captures historiques de la racine, supprimer `_bmad-output/` de la racine et reclasser les artefacts utiles dans les surfaces canoniques.

## Validation Authority

- [ ] User approval: pending final review.
- [x] UX review available in `_grimoire-runtime-output/implementation-artifacts/visual-evidence/ux-visual-da-review.md`.
- [x] Art direction review available in `_grimoire-runtime-output/implementation-artifacts/visual-evidence/ux-visual-da-review.md`.
- [x] Technical governance check prepared through retention metadata and canonical landing zone.

## Checks

- [x] Les captures racine ont ete deplacees vers `_grimoire-runtime-output/implementation-artifacts/visual-evidence/legacy-root-captures/`.
- [x] `retention-manifest.json` documente les captures deplacees avec un `ticket_id` dedie.
- [x] La racine du depot ne conserve plus de captures `.png` ni de snapshot Markdown relies a cette serie de preuves.
- [x] Les artefacts utiles issus de `_bmad-output/` ont ete migres vers `_grimoire-runtime-output/test-artifacts/`.
- [x] `_bmad-output/` n'est plus present a la racine.

## Non-regression visuelle

- [x] PASS: le stockage des preuves visuelles suit maintenant la landing zone canonique du depot.
- [x] PASS: les captures `desktop` et `mobile` restent couvertes dans le manifeste de retention.
- [x] PASS: le rangement n'a supprime aucune preuve, il a seulement reclasse les fichiers vers une surface gouvernee.

## Open Risks

- Toute reapparition d'une surface BMAD legacy doit etre migree vers les surfaces Grimoire canoniques avant suppression.
- Certaines preuves legacy peuvent meriter une conservation plus longue apres verification fonctionnelle ; la retention actuelle reste au TTL par defaut.

## Revue UX / Visuel / DA

- [x] Surface analysee: `runtime-views-report.html`
- [x] Surface analysee: [cockpit local](http://127.0.0.1:4174/)
- [x] Rapport de revue: `_grimoire-runtime-output/implementation-artifacts/visual-evidence/ux-visual-da-review.md`
