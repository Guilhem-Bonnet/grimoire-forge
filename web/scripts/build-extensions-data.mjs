#!/usr/bin/env node
// Génère src/_socle/data/extensions.json depuis les manifestes réels
// des extensions du kit (grimoire-kit/extensions/*/extension.json).
// Tolérant : si le dossier kit est absent (build web isolé), le fichier
// existant est conservé tel quel.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(new URL('.', import.meta.url).pathname, '..');
const EXT_DIR = path.resolve(ROOT, '../grimoire-kit/extensions');
const OUT = path.join(ROOT, 'src/_socle/data/extensions.json');

// Frameworks candidats (inventaire Référence-Agentique) non encore packagés.
const CANDIDATES = [
  { id: 'langgraph', name: 'LangGraph', description: 'Graphes d’agents avec état persistant et checkpoints.', upstream: 'https://github.com/langchain-ai/langgraph' },
  { id: 'langfuse', name: 'Langfuse', description: 'Observabilité et évaluation LLM — traces, scores, datasets.', upstream: 'https://github.com/langfuse/langfuse' },
  { id: 'autogen', name: 'AutoGen', description: 'Conversations multi-agents et patterns de coopération Microsoft.', upstream: 'https://github.com/microsoft/autogen' },
  { id: 'browser-use', name: 'Browser Use', description: 'Agents de navigation web pilotés par LLM.', upstream: 'https://github.com/browser-use/browser-use' },
  { id: 'haystack', name: 'Haystack', description: 'Pipelines RAG et recherche sémantique en production.', upstream: 'https://github.com/deepset-ai/haystack' },
];

function readManifests() {
  if (!fs.existsSync(EXT_DIR)) return null;
  const manifests = [];
  for (const entry of fs.readdirSync(EXT_DIR, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const manifestPath = path.join(EXT_DIR, entry.name, 'extension.json');
    if (!fs.existsSync(manifestPath)) continue;
    const m = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    manifests.push({
      id: m.id,
      name: m.name,
      version: m.version,
      description: m.description,
      license: m.license,
      upstream: m.upstream?.repository ?? null,
      upstreamKind: m.upstream?.kind ?? null,
      patterns: m.patterns?.implements ?? [],
      requires: m.patterns?.requires ?? [],
      permissions: m.permissions ?? {},
      provides: Object.fromEntries(
        Object.entries(m.provides ?? {})
          .filter(([, v]) => Array.isArray(v) && v.length > 0)
          .map(([k, v]) => [k, v.length])
      ),
      nodes: (m.provides?.nodes ?? []).map((n) => n.label),
      status: 'available',
    });
  }
  return manifests;
}

const manifests = readManifests();
if (manifests === null) {
  if (fs.existsSync(OUT)) {
    console.log('⚠  grimoire-kit/extensions absent — extensions.json existant conservé.');
    process.exit(0);
  }
  console.error('✗ grimoire-kit/extensions absent et aucun extensions.json existant.');
  process.exit(1);
}

const data = {
  generatedAt: new Date().toISOString(),
  available: manifests.sort((a, b) => a.id.localeCompare(b.id)),
  candidates: CANDIDATES.map((c) => ({ ...c, status: 'candidate' })),
};

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(data, null, 2) + '\n', 'utf8');
console.log(`✓ extensions.json — ${data.available.length} disponible(s), ${data.candidates.length} candidat(s)`);
