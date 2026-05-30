# Changelog

Ce document suit le format Keep a Changelog.

## [Unreleased]

### Added

- Nouveau site public base sur [Astro](https://astro.build) dans `web/`, avec socle HTML/CSS/JS premium (dark control plane + FX layer futuriste) sous `web/src/_socle/`.
- Pages `/agents/` (generee depuis `_grimoire-runtime/_config/agent-manifest.csv`) et `/changelog/` (generee depuis `CHANGELOG.md`).
- Scripts `web/scripts/build-pages.mjs` et `web/scripts/copy-cockpit.mjs` pour projeter le socle et le cockpit dans `public/` au build.
- Sitemap automatique via `@astrojs/sitemap`, pretty URLs (trailing slash).
- [web/README.md](web/README.md) avec structure, routes et workflow de dev.

### Removed

- Ancien site MkDocs : `docs/`, `mkdocs.yml`, `mkdocs_hooks/`, `site/`, `project-context.yaml` supprimes au profit du nouveau site Astro.

### Changed

- README racine mis a jour : nouvelle section **Site public**, suppression des liens `docs/`.

## [0.1.0] - 2026-03-27

### Added

- Baseline publique de Grimoire Forge orientee moteur de creation de projets agentiques.
- Vision produit, plan d'execution et gouvernance de publication.
- Structuration de la documentation en trois axes : vision, roadmap, gouvernance.
- Roadmap publique v1 et backlog initial priorise.
- Kit open source de contribution : templates d'issues et template de pull request.
- Message de lancement public versionne et pret a diffuser.

### Changed

- Passage de meta-projet interne vers une structure prete a l'ouverture open source.
- Mise a jour du contexte projet pour l'aligner sur l'objectif moteur agentique.
- Mise a jour du README et des liens de navigation vers la nouvelle arborescence docs.
- Mise a jour de la description du depot GitHub.

### Project Management

- Creation de 5 issues initiales de backlog pour piloter la v1.
- Application de labels de priorite et de domaine sur les issues initiales.
