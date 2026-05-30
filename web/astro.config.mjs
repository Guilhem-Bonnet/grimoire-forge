// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const SITE = process.env.SITE_URL || 'https://grimoire-forge.dev';

export default defineConfig({
  site: SITE,
  output: 'static',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/cockpit/') && !page.includes('runtime-views-report'),
    }),
  ],
  build: {
    assets: 'astro-assets',
  },
});
