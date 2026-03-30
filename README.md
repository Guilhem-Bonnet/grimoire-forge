# Grimoire Forge

Moteur de création de projets agentiques, construit en dogfooding continu avec BMAD.

## Positionnement

Ce dépôt est le cockpit de conception du moteur.
Le code produit reste dans [bmad-custom-kit](bmad-custom-kit/).

Objectif produit : permettre de lancer, structurer et faire évoluer des projets pilotés par agents IA avec un niveau entreprise.

## Nouveau nom

Nom retenu pour le projet de création : Grimoire Forge.

Ce nom conserve l'ADN Grimoire et clarifie la promesse : forger un projet agentique de bout en bout.

## Architecture de travail

```text
bmad-custom/
├── _bmad/                    Runtime BMAD installé dans ce workspace
├── _bmad-output/             Artefacts produits (plans, implémentation, traces)
├── docs/                     Cible produit, architecture, roadmap, publication
├── bmad-custom-kit/          Produit implémenté (framework, CLI, tests)
└── .github/                  Instructions, skills, workflows, agents
```

## Ce qui est déjà capitalisé

- Orchestrateur SOG BM-53 comme point d'entrée unique.
- Protocoles d'autonomie ALS, AORA, PIP, DCF.
- Unified Dynamic Factory pour créer agents, workflows, skills et instructions.
- Tooling de robustesse : health check, antifragile, self-heal, memory audit, pre-push.
- Boucle d'apprentissage via mémoire projet et artefacts d'exécution.

## Documentation structurée

- Vision et périmètre : [docs/vision/objectif-moteur-agentique.md](docs/vision/objectif-moteur-agentique.md)
- Plan d'exécution : [docs/roadmap/plan-vers-objectif.md](docs/roadmap/plan-vers-objectif.md)
- Passage open source : [docs/governance/publication-open-source.md](docs/governance/publication-open-source.md)
- Changelog : [CHANGELOG.md](CHANGELOG.md)
- Hub de navigation : [docs/index.md](docs/index.md)

## Workflow recommandé

1. Formaliser la cible et les contraintes dans la documentation.
2. Transformer la cible en stories exploitables via BMAD.
3. Implémenter dans [bmad-custom-kit](bmad-custom-kit/).
4. Réinstaller dans ce workspace et valider en conditions réelles.
5. Rejouer la boucle d'amélioration continue.

## Commandes utiles

```bash
# Validation rapide
python3 -m ruff check bmad-custom-kit/framework/tools/ bmad-custom-kit/tests/ --statistics
python3 -m pytest bmad-custom-kit/tests/ -q --tb=short -x --ignore=bmad-custom-kit/tests/test_background_tasks.py

# Santé BMAD
python3 bmad-custom-kit/framework/tools/preflight-check.py --project-root .
python3 bmad-custom-kit/framework/tools/memory-lint.py --project-root .
```

## Statut du dépôt

Le dépôt doit être public pour soutenir l'objectif produit.
Voir [docs/governance/publication-open-source.md](docs/governance/publication-open-source.md) pour la procédure et le checklist de diffusion.
