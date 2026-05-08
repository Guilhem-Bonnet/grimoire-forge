# Grimoire Forge — Site public (Astro)

Site statique de Grimoire Forge, basé sur [Astro](https://astro.build).
Le socle HTML/CSS/JS premium (dark control plane + FX layer futuriste) est
stocké dans [src/_socle/](src/_socle/) et projeté dans `public/` au build.

## Structure

```
web/
├── astro.config.mjs           # Astro + sitemap
├── src/
│   ├── _socle/                # HTML/CSS/JS source (committed)
│   ├── layouts/
│   │   └── BaseLayout.astro   # layout des pages dynamiques
│   └── pages/
│       ├── agents/index.astro    # liste d'agents (depuis agent-manifest.csv)
│       └── changelog/index.astro # changelog (depuis ../CHANGELOG.md)
├── public/                    # assets statiques servis tels quels
│   ├── styles/forge-*.css     # généré par prebuild
│   ├── scripts/forge-*.js     # généré par prebuild (nav patchée)
│   ├── cockpit/               # généré par prebuild (copy de grimoire-game)
│   ├── runtime-views-report.html
│   └── {anatomy,demo,observability,game-ui,forge}/index.html
└── scripts/
    ├── build-pages.mjs        # socle → public/ + patch forge-nav.js
    └── copy-cockpit.mjs       # cockpit-app + runtime-views-report → public/
```

## Routes

| Route | Source | Type |
|---|---|---|
| `/` | `src/_socle/index.html` | Landing principale avec ChatOrchestrator demo |
| `/forge/` | `src/_socle/Grimoire Forge.html` | Landing alternative (long-scroll) |
| `/anatomy/` | `src/_socle/anatomy.html` | Anatomie du runtime |
| `/demo/` | `src/_socle/demo.html` | Démonstration |
| `/observability/` | `src/_socle/observability.html` | Observatory |
| `/game-ui/` | `src/_socle/game-ui.html` | Game UI |
| `/agents/` | Astro dynamique ← `_grimoire-runtime/_config/agent-manifest.csv` | Catalogue d'agents |
| `/changelog/` | Astro dynamique ← `CHANGELOG.md` | Notes de release |
| `/cockpit/` | Copié depuis `grimoire-kit/apps/grimoire-game/.release/cockpit-app/` | SPA cockpit live |
| `/runtime-views-report.html` | Copié depuis `.release/` | Rapport de surfaces |

## Développement

```bash
cd web
npm install          # une seule fois
npm run dev          # http://localhost:4321 avec HMR
npm run build        # dist/ statique prêt à déployer
npm run preview      # sert dist/
```

Les hooks `prebuild` / `predev` lancent automatiquement la reprojection du
socle et la copie du cockpit. Pour les lancer manuellement :

```bash
npm run pages:rebuild   # socle → public/
npm run cockpit:copy    # cockpit + runtime-views-report → public/
```

## Cockpit live

Le cockpit SPA est copié depuis `grimoire-kit/apps/grimoire-game/.release/`.
Pour re-générer cette release avant un build :

```bash
cd grimoire-kit/apps/grimoire-game
npm run cockpit:verify
```

Puis `cd ../../../web && npm run build`.

## Déploiement

Le dossier `dist/` est 100 % statique (HTML + CSS + JS). Compatible avec
GitHub Pages, Netlify, Vercel, Cloudflare Pages, nginx, etc.

Variable d'environnement :

- `SITE_URL` — URL canonique (défaut : `https://grimoire-forge.dev`).
  Utilisée pour le sitemap et les balises `og:`.
# Astro Starter Kit: Minimal

```sh
npm create astro@latest -- --template minimal
```

> 🧑‍🚀 **Seasoned astronaut?** Delete this file. Have fun!

## 🚀 Project Structure

Inside of your Astro project, you'll see the following folders and files:

```text
/
├── public/
├── src/
│   └── pages/
│       └── index.astro
└── package.json
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro/React/Vue/Svelte/Preact components.

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

## 👀 Want to learn more?

Feel free to check [our documentation](https://docs.astro.build) or jump into our [Discord server](https://astro.build/chat).
