#!/usr/bin/env node
// Copie l'app cockpit + runtime views report vers web/public/.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REPO = path.resolve(ROOT, '..');
const SRC_COCKPIT = path.join(REPO, 'grimoire-kit/apps/grimoire-game/.release/cockpit-app');
const SRC_REPORT = path.join(REPO, 'grimoire-kit/apps/grimoire-game/.release/runtime-views-report.html');
const DST_COCKPIT = path.join(ROOT, 'public/cockpit');
const DST_REPORT = path.join(ROOT, 'public/runtime-views-report.html');

function copyDir(src, dst) {
  if (!fs.existsSync(src)) {
    console.warn(`⚠  Source introuvable: ${src} — skip`);
    return false;
  }
  fs.rmSync(dst, { recursive: true, force: true });
  fs.cpSync(src, dst, { recursive: true });
  return true;
}

function copyFile(src, dst) {
  if (!fs.existsSync(src)) {
    console.warn(`⚠  Source introuvable: ${src} — skip`);
    return false;
  }
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.copyFileSync(src, dst);
  return true;
}

const okCockpit = copyDir(SRC_COCKPIT, DST_COCKPIT);
const okReport = copyFile(SRC_REPORT, DST_REPORT);

if (okCockpit) console.log(`✓ cockpit → public/cockpit/`);
if (okReport) console.log(`✓ runtime-views-report → public/runtime-views-report.html`);
if (!okCockpit || !okReport) {
  console.log('\nAstuce: produire les artefacts via `cd grimoire-kit/apps/grimoire-game && npm run cockpit:verify`.');
}
