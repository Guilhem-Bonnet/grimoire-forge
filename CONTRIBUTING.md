# Contribuer a Grimoire Forge

## But

Ce depot regroupe le cadrage, la gouvernance et les surfaces runtime du projet.

Le chemin de contribution le plus court pour le cockpit web et ses shells lives est documente dans [docs/exploitation/parcours-contributeur-cockpit-v5.md](docs/exploitation/parcours-contributeur-cockpit-v5.md).

## Prerequis minimaux

- `git`
- `node >= 22`
- `npm`
- `python3`

## Regles GitHub obligatoires

- Ne jamais pousser directement sur `main` ; travailler sur une branche de travail puis ouvrir une PR.
- Installer les garde-fous locaux une fois par clone avec `bash grimoire-init.sh hooks --install`.
- Utiliser des commits et des titres de PR en Conventional Commits : `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build`, `perf`, `revert`, `style`.
- Rejouer `grimoire: flow-quick`, `grimoire: quickcheck` ou l'equivalent avant tout push.
- Considerer CODEOWNERS, required checks et merge queue comme obligatoires sur GitHub des que la protection de branche est activee.

## Boucle agentique recommandee

1. Toute nouvelle tache entre par le kanban et passe par reformulation / priorisation SM.
2. L'implementation se fait sur une branche courte avec hooks locaux actifs.
3. La review de PR couvre au minimum implementation, QA / edge cases, challenge architecture et observabilite / memoire.
4. Les learnings, traces et impacts de retention sont notes avant merge si le changement touche l'orchestration agentique.

## Plugin agentique: definition utile

Un plugin agentique est une surface d'extension exposee aux agents. Dans ce depot, cela couvre surtout les serveurs MCP, bridges, hooks, skills, workflows et tools locaux. Un plugin ne doit pas exister sans contrat clair, permissions bornees, traces et owner explicite.

## Choisir la bonne landing zone

| Si vous modifiez... | Travaillez d'abord dans... | Validation minimale |
| --- | --- | --- |
| Les read models, bridges ou shells web du cockpit | `grimoire-kit/apps/grimoire-game/` | `cd grimoire-kit/apps/grimoire-game && npm run release:verify` |
| Le framework Python et les outils Grimoire Kit | `grimoire-kit/` | Voir [grimoire-kit/CONTRIBUTING.md](grimoire-kit/CONTRIBUTING.md) |
| La gouvernance, les claims ou les release gates | `docs/` et les fichiers racine | `python3 grimoire-kit/framework/tools/preflight-check.py --project-root .` |
| Les assets visuels du board | `grimoire-game-assets/` | Respecter les conventions de pipeline et les manifests |

## Boucle de contribution recommandee

```bash
git clone <repo-url>
cd bmad-custom/grimoire-kit/apps/grimoire-game
npm install
npm run release:verify
```

Depuis la racine du depot, rejouez ensuite les checks de gouvernance si votre changement touche la documentation, les policies ou les artefacts Grimoire.

```bash
bash grimoire-init.sh hooks --install
python3 grimoire-kit/framework/tools/preflight-check.py --project-root .
python3 grimoire-kit/framework/tools/memory-lint.py --project-root .
```

## Avant une pull request

- Garder les README et les docs publiques alignes avec les preuves rejouables.
- Mettre a jour [docs/governance/claims-publics-cockpit-v5.md](docs/governance/claims-publics-cockpit-v5.md) si le wording autorise change.
- Mettre a jour [docs/governance/release-checklist-v0.1.0.md](docs/governance/release-checklist-v0.1.0.md) si une gate de release evolue.
- Ne pas ouvrir de nouveau chemin de mutation hors `preview -> validation -> commit borne`.
- Garder les taches kanban, les revues et les merges relies a une PR ; pas de push direct sur `main`.

## References

- [README.md](README.md)
- [docs/governance/referentiel-bonnes-pratiques-agentiques.md](docs/governance/referentiel-bonnes-pratiques-agentiques.md)
- [docs/exploitation/parcours-contributeur-cockpit-v5.md](docs/exploitation/parcours-contributeur-cockpit-v5.md)
- [docs/governance/claims-publics-cockpit-v5.md](docs/governance/claims-publics-cockpit-v5.md)
- [docs/governance/publication-open-source.md](docs/governance/publication-open-source.md)
- [grimoire-kit/CONTRIBUTING.md](grimoire-kit/CONTRIBUTING.md)
