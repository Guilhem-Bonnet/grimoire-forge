#!/usr/bin/env node
// Applique les transformations du socle HTML (assets + nav) et écrit dans web/public/.
// Source: /tmp/grimoire-new-socle ou web/src/_socle/ selon dispo.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(new URL('.', import.meta.url).pathname, '..');
const CANDIDATES = [
  path.join(ROOT, 'src/_socle'),
  '/tmp/grimoire-new-socle',
];
let SRC = null;
for (const c of CANDIDATES) {
  if (fs.existsSync(path.join(c, 'index.html'))) { SRC = c; break; }
}
if (!SRC) {
  console.error('✗ Socle HTML introuvable. Attendu dans web/src/_socle/ ou /tmp/grimoire-new-socle/.');
  process.exit(1);
}

const DST = path.join(ROOT, 'public');

const PAGES = [
  { src: 'index.html', out: 'index.html' },
  { src: 'anatomy.html', out: 'anatomy/index.html' },
  { src: 'demo.html', out: 'demo/index.html' },
  { src: 'observability.html', out: 'observability/index.html' },
  { src: 'game-ui.html', out: 'game-ui/index.html' },
  { src: 'manifesto.html', out: 'manifesto/index.html' },
  { src: 'Grimoire Forge.html', out: 'forge/index.html' },
  { src: 'documentation.html', out: 'documentation/index.html' },
  { src: 'extensions.html', out: 'extensions/index.html' },
  { src: 'blueprint.html', out: 'blueprint/index.html' },
  { src: 'setup.html', out: 'setup/index.html' },
];

const NAV_MAP = {
  'index.html': '/',
  'anatomy.html': '/anatomy/',
  'demo.html': '/demo/',
  'observability.html': '/observability/',
  'game-ui.html': '/game-ui/',
  'manifesto.html': '/manifesto/',
  'Grimoire Forge.html': '/forge/',
  'documentation.html': '/documentation/',
  'extensions.html': '/extensions/',
  'blueprint.html': '/blueprint/',
  'setup.html': '/setup/',
};

// Copier les assets bruts (CSS intacts, JS patché pour pretty URLs)
fs.mkdirSync(path.join(DST, 'styles'), { recursive: true });
fs.mkdirSync(path.join(DST, 'scripts'), { recursive: true });

// Copier les données consommées par les pages (catalogue, extensions)
const DATA_SRC = path.join(SRC, 'data');
if (fs.existsSync(DATA_SRC)) {
  fs.mkdirSync(path.join(DST, 'data'), { recursive: true });
  for (const f of fs.readdirSync(DATA_SRC)) {
    if (f.endsWith('.json')) {
      fs.copyFileSync(path.join(DATA_SRC, f), path.join(DST, 'data', f));
    }
  }
}
for (const f of fs.readdirSync(SRC)) {
  if (f.startsWith('forge-') && f.endsWith('.css')) {
    fs.copyFileSync(path.join(SRC, f), path.join(DST, 'styles', f));
  }
  if (f.startsWith('forge-') && f.endsWith('.js')) {
    let js = fs.readFileSync(path.join(SRC, f), 'utf8');
    js = patchJsNav(js);
    fs.writeFileSync(path.join(DST, 'scripts', f), js, 'utf8');
  }
}

// Patche la navigation générée dans forge-nav.js :
//   - chemins pretty URLs
//   - ajout des liens /agents/ et /changelog/
//   - active-class détection par pathname
function patchJsNav(js) {
  // Remplace la liste <ul class="nav-links">
  js = js.replace(
    /<ul class="nav-links" role="list">[\s\S]*?<\/ul>/,
    `<ul class="nav-links" role="list">
            <li><a href="/manifesto/"    class="\${isActive('/manifesto/') ? 'active' : ''}">MANIFESTO</a></li>
            <li><a href="/demo/"          class="\${isActive('/demo/') ? 'active' : ''}">DÉMO</a></li>
            <li><a href="/game-ui/"       class="\${isActive('/game-ui/') ? 'active' : ''}">GAME UI</a></li>
            <li><a href="/observability/" class="\${isActive('/observability/') ? 'active' : ''}">OBSERVATORY</a></li>
            <li><a href="/anatomy/"       class="\${isActive('/anatomy/') ? 'active' : ''}">ANATOMIE</a></li>
            <li><a href="/documentation/" class="\${isActive('/documentation/') ? 'active' : ''}">DOCS</a></li>
            <li><a href="/extensions/"    class="\${isActive('/extensions/') ? 'active' : ''}">EXTENSIONS</a></li>
            <li><a href="/blueprint/"     class="\${isActive('/blueprint/') ? 'active' : ''}">BLUEPRINT</a></li>
            <li><a href="/setup/"         class="\${isActive('/setup/') ? 'active' : ''}">SETUP</a></li>
            <li><a href="/agents/"        class="\${isActive('/agents/') ? 'active' : ''}">AGENTS</a></li>
            <li><a href="/changelog/"     class="\${isActive('/changelog/') ? 'active' : ''}">CHANGELOG</a></li>
          </ul>`
  );

  // Logo href
  js = js.replace(/href="index\.html"/g, 'href="/"');

  // Footer links
  const footerMap = {
    'game-ui.html': '/game-ui/',
    'observability.html': '/observability/',
    'demo.html': '/demo/',
    'anatomy.html': '/anatomy/',
    'manifesto.html': '/manifesto/',
    'documentation.html': '/documentation/',
  };
  for (const [k, v] of Object.entries(footerMap)) {
    js = js.replace(new RegExp(`href="${k.replace('.', '\\.')}"`, 'g'), `href="${v}"`);
  }

  // isActive redéfini pour les pretty URLs
  js = js.replace(
    /function isActive\(href\) \{[\s\S]*?\n\s*\}/,
    `function isActive(href) {
    const current = location.pathname;
    if (href === '/') return current === '/' || current === '/index.html';
    return current === href || current === href.replace(/\\/$/, '');
  }`
  );

  // Footer : liens utiles pour nos routes réelles
  js = js.replace(/<a href="#">Changelog<\/a>/g, '<a href="/changelog/">Changelog</a>');
  js = js.replace(/<a href="#">Cockpit<\/a>/g, '<a href="/cockpit/?mode=cockpit">Cockpit</a>');
  js = js.replace(/<a href="#">War Room<\/a>/g, '<a href="/cockpit/?mode=war-room">War Room</a>');
  js = js.replace(/<a href="#">Contrats<\/a>/g, '<a href="/cockpit/?mode=proofs">Contrats</a>');
  js = js.replace(/<a href="#">Documentation<\/a>/g, '<a href="/anatomy/">Documentation</a>');

  return js;
}

for (const { src, out } of PAGES) {
  const full = path.join(SRC, src);
  if (!fs.existsSync(full)) { console.warn(`⚠  ${src} absent`); continue; }
  let html = fs.readFileSync(full, 'utf8');

  html = html.replace(/(href|src)="(forge-[a-z0-9-]+\.(css|js))"/g, (_m, attr, file, ext) => {
    const dir = ext === 'css' ? 'styles' : 'scripts';
    return `${attr}="/${dir}/${file}"`;
  });

  for (const [file, route] of Object.entries(NAV_MAP)) {
    const esc = file.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    html = html.replace(new RegExp(`href="${esc}(#[^"]*)?"`, 'g'), (_m, anchor = '') => {
      return `href="${route}${anchor}"`;
    });
  }

  const target = path.join(DST, out);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, html, 'utf8');
  console.log(`✓ ${src} → public/${out}`);
}
