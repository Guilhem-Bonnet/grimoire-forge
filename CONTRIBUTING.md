# Contribuer a Grimoire Forge

Merci de vouloir contribuer. Ce guide explique ou travailler, comment valider,
et quelles regles GitHub respecter pour que chaque changement reste tracable.

## Ce qu'est ce depot

Grimoire Forge est le cockpit de conception du moteur agentique. Il regroupe le
cadrage produit, la gouvernance, le site public et les surfaces runtime.
Le code produit, lui, vit dans [`grimoire-kit/`](grimoire-kit/).

## Prerequis

- `git`
- `node >= 22` et `npm`
- `python3`

## Regles GitHub

- Ne jamais pousser directement sur `main` : travailler sur une branche courte puis ouvrir une PR.
- Installer les garde-fous locaux une fois par clone : `bash grimoire-init.sh hooks --install`.
- Utiliser des commits et titres de PR en Conventional Commits : `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build`, `perf`, `revert`, `style`.
- Rejouer les checks rapides avant chaque push (voir **Valider avant une PR**).
- Quand la protection de branche est active, considerer CODEOWNERS, required checks et merge queue comme obligatoires.

## Ou travailler : choisir la bonne landing zone

| Si vous modifiez... | Travaillez d'abord dans... | Validation minimale |
| --- | --- | --- |
| Les read models, bridges ou shells web du cockpit | [`grimoire-kit/apps/grimoire-game/`](grimoire-kit/apps/grimoire-game/README.md) | `cd grimoire-kit/apps/grimoire-game && npm run release:verify` |
| Le framework Python et les outils Grimoire Kit | [`grimoire-kit/`](grimoire-kit/CONTRIBUTING.md) | Voir le guide du kit |
| Le site public | [`web/`](web/README.md) | `cd web && npm run build` |
| La gouvernance, les claims ou les release gates | Fichiers racine (`README.md`, ce guide) | `python3 grimoire-kit/framework/tools/preflight-check.py --project-root .` |
| Les assets visuels du board | [`grimoire-game-assets/`](grimoire-game-assets/) | Respecter les conventions de pipeline et les manifests |

## Boucle de contribution recommandee

1. Toute nouvelle tache passe par une reformulation et une priorisation claires.
2. L'implementation se fait sur une branche courte, hooks locaux actifs.
3. La review de PR couvre au minimum : implementation, QA / edge cases, challenge
   d'architecture, et impact observabilite / memoire.
4. Les learnings, traces et impacts de retention sont notes avant merge si le
   changement touche l'orchestration agentique.

```bash
git clone <repo-url>
cd grimoire-forge
bash grimoire-init.sh hooks --install
```

## Plugin agentique : definition utile

Un plugin agentique est une surface d'extension exposee aux agents : serveurs MCP,
bridges, hooks, skills, workflows et tools locaux. Un plugin ne doit jamais exister
sans contrat clair, permissions bornees, traces et owner explicite.

## Valider avant une PR

```bash
# Garde-fous locaux
bash grimoire-init.sh hooks --install

# Sante du runtime
python3 grimoire-kit/framework/tools/preflight-check.py --project-root .
python3 grimoire-kit/framework/tools/memory-lint.py --project-root .
```

- Garder les README et le site public alignes avec les preuves rejouables.
- Ne pas ouvrir de nouveau chemin de mutation hors `preview -> validation -> commit borne`.
- Relier chaque tache, review et merge a une PR ; pas de push direct sur `main`.

## References

- [README.md](README.md) — vue d'ensemble du cockpit
- [Site public (web/)](web/README.md)
- [grimoire-kit/CONTRIBUTING.md](grimoire-kit/CONTRIBUTING.md) — contribuer au produit
- [SECURITY.md](SECURITY.md) — signaler une vulnerabilite
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — regles de participation
- [CHANGELOG.md](CHANGELOG.md) — historique des changements
