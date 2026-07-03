#!/usr/bin/env node
// Génère src/_socle/data/extensions.json.
// Source de vérité marketplace : registry.json du repo dédié
// grimoire-extensions-registry (clone local attendu à côté du projet).
// Enrichissement (provides, nodes, requires) depuis les manifestes du kit
// quand disponibles ; fallback complet sur le kit si le registry est absent.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const EXT_DIR = path.resolve(ROOT, '../grimoire-kit/extensions');
const REGISTRY_CANDIDATES = [
  path.resolve(ROOT, '../../grimoire-extensions-registry/registry.json'),
  path.resolve(ROOT, '../grimoire-extensions-registry/registry.json'),
];
const OUT = path.join(ROOT, 'src/_socle/data/extensions.json');

// Frameworks candidats (inventaire Référence-Agentique) non encore packagés.
const CANDIDATES = [
  { id: 'dify', name: 'Dify', description: 'Plateforme LLM apps — workflows visuels, RAG, agents.', upstream: 'https://github.com/langgenius/dify' },
  { id: 'openhands', name: 'OpenHands', description: 'Agents développeurs autonomes en sandbox.', upstream: 'https://github.com/All-Hands-AI/OpenHands' },
  { id: 'mem0', name: 'Mem0', description: 'Couche mémoire persistante pour agents.', upstream: 'https://github.com/mem0ai/mem0' },
  { id: 'langgraph', name: 'LangGraph', description: 'Graphes d’agents avec état persistant et checkpoints.', upstream: 'https://github.com/langchain-ai/langgraph' },
  { id: 'langfuse', name: 'Langfuse', description: 'Observabilité et évaluation LLM — traces, scores, datasets.', upstream: 'https://github.com/langfuse/langfuse' },
  { id: 'autogen', name: 'AutoGen', description: 'Conversations multi-agents et patterns de coopération Microsoft.', upstream: 'https://github.com/microsoft/autogen' },
  { id: 'browser-use', name: 'Browser Use', description: 'Agents de navigation web pilotés par LLM.', upstream: 'https://github.com/browser-use/browser-use' },
  { id: 'haystack', name: 'Haystack', description: 'Pipelines RAG et recherche sémantique en production.', upstream: 'https://github.com/deepset-ai/haystack' },
];

function readKitManifests() {
  if (!fs.existsSync(EXT_DIR)) return new Map();
  const manifests = new Map();
  for (const entry of fs.readdirSync(EXT_DIR, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const manifestPath = path.join(EXT_DIR, entry.name, 'extension.json');
    if (!fs.existsSync(manifestPath)) continue;
    const m = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    manifests.set(m.id, m);
  }
  return manifests;
}

function fromManifest(m) {
  return {
    id: m.id,
    kind: m.kind ?? null,
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
  };
}

const kitManifests = readKitManifests();
const registryPath = REGISTRY_CANDIDATES.find((p) => fs.existsSync(p));
let available = [];
let source = null;

if (registryPath) {
  // Marketplace = le registry publié fait foi.
  const index = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
  source = 'registry';
  for (const [id, entry] of Object.entries(index.extensions ?? {})) {
    const release = entry.versions.find((r) => r.version === entry.latest);
    const kit = kitManifests.get(id);
    if (kit) {
      available.push({ ...fromManifest(kit), version: entry.latest });
    } else {
      const s = release.summary;
      available.push({
        id, kind: s.kind ?? null, name: s.name, version: entry.latest, description: s.description,
        license: s.license, upstream: s.upstream ?? null, upstreamKind: null,
        patterns: s.patterns ?? [], requires: [], permissions: s.permissions ?? {},
        provides: {}, nodes: [], status: 'available',
      });
    }
  }
} else if (kitManifests.size) {
  source = 'kit';
  available = [...kitManifests.values()].map(fromManifest);
} else if (fs.existsSync(OUT)) {
  console.log('⚠  registry et kit absents — extensions.json existant conservé.');
  process.exit(0);
} else {
  console.error('✗ Aucune source (registry, kit) et aucun extensions.json existant.');
  process.exit(1);
}

let blueprints = [];
if (registryPath) {
  const index = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
  blueprints = Object.entries(index.blueprints ?? {}).map(([id, e]) => ({
    id,
    name: e.summary.name,
    description: e.summary.description ?? '',
    nodes: e.summary.nodes,
    edges: e.summary.edges,
    extensions: e.summary.extensions ?? [],
    catalogVersion: e.summary.catalogVersion ?? null,
  }));
}

const packaged = new Set(available.map((m) => m.id));
const data = {
  generatedAt: new Date().toISOString(),
  source,
  registry: 'https://github.com/Guilhem-Bonnet/grimoire-extensions-registry',
  available: available.sort((a, b) => a.id.localeCompare(b.id)),
  blueprints: blueprints.sort((a, b) => a.id.localeCompare(b.id)),
  candidates: CANDIDATES.filter((c) => !packaged.has(c.id)).map((c) => ({ ...c, status: 'candidate' })),
};

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(data, null, 2) + '\n', 'utf8');
console.log(`✓ extensions.json (source: ${source}) — ${data.available.length} disponible(s), ${data.blueprints.length} blueprint(s), ${data.candidates.length} candidat(s)`);
