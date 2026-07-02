/* forge-blueprint.js — Blueprint viewer read-only du catalogue de patterns
   Consomme data/catalogue-export.json (généré depuis le catalogue normatif).
   ======================================================================== */
(function () {
  'use strict';

  const FAMILY_ORDER = ['ORG', 'ORC', 'GOV', 'MOD', 'QUA', 'KNO', 'RUN', 'COG'];
  const FAMILY_COLORS = {
    ORG: '#FF6B3D', ORC: '#6EE7FF', GOV: '#A78BFA', MOD: '#F472B6',
    QUA: '#34D399', KNO: '#FCD34D', RUN: '#F87171', COG: '#8B9DFF',
  };
  const KIND_STYLES = {
    founds:     { color: '#FF6B3D', style: 'solid',  label: 'fonde' },
    depends:    { color: '#6EE7FF', style: 'solid',  label: 'dépend de' },
    feeds:      { color: '#34D399', style: 'solid',  label: 'alimente' },
    governs:    { color: '#A78BFA', style: 'solid',  label: 'gouverne' },
    produces:   { color: '#FCD34D', style: 'solid',  label: 'produit' },
    triggers:   { color: '#F87171', style: 'solid',  label: 'déclenche' },
    extends:    { color: '#F472B6', style: 'dashed', label: 'étend' },
    reinforces: { color: '#8B9DFF', style: 'dashed', label: 'renforce' },
    related:    { color: '#5B6068', style: 'dotted', label: 'apparenté' },
  };
  const MATURITY_COLORS = {
    'Minimal': '#34D399', 'Contrôlé': '#6EE7FF', 'Orchestré': '#FCD34D',
    'Gouverné': '#A78BFA', 'Production': '#F87171',
  };

  function loadData(name) {
    return fetch('data/' + name).catch(() => null)
      .then(r => (r && r.ok) ? r.json() : fetch('/data/' + name).then(r2 => r2.json()));
  }

  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  loadData('catalogue-export.json').then(init).catch(() => {
    document.getElementById('bp-source').innerHTML = 'DONNÉES INDISPONIBLES';
  });

  function init(cat) {
    /* ── Topbar ── */
    document.getElementById('bp-stats').innerHTML =
      `<span><b>${cat.patterns.length}</b> patterns</span>` +
      `<span><b>${cat.relations.length}</b> relations</span>` +
      `<span><b>${cat.contracts.length}</b> contrats</span>` +
      `<span><b>${(cat.useCases || []).length}</b> use-cases</span>`;
    document.getElementById('bp-source').innerHTML =
      `<span class="sync"></span>CATALOGUE v${esc(cat.catalogVersion)} · ${esc(String(cat.source.commit).slice(0, 7))}`;

    /* ── Éléments Cytoscape : layout en colonnes par famille ── */
    const byFamily = {};
    for (const p of cat.patterns) (byFamily[p.family] = byFamily[p.family] || []).push(p);

    const COL_W = 260, ROW_H = 72;
    const nodes = [];
    FAMILY_ORDER.forEach((fam, col) => {
      (byFamily[fam] || []).forEach((p, row) => {
        nodes.push({
          data: { id: p.id, label: p.id + '\n' + p.name, family: fam, pattern: p },
          position: { x: col * COL_W, y: row * ROW_H },
        });
      });
    });
    const ids = new Set(cat.patterns.map(p => p.id));
    const edges = cat.relations
      .filter(r => ids.has(r.from) && ids.has(r.to))
      .map((r, i) => ({ data: { id: 'e' + i, source: r.from, target: r.to, kind: r.kind, label: r.label || '' } }));

    const cy = cytoscape({
      container: document.getElementById('bp-cy'),
      elements: { nodes, edges },
      layout: { name: 'preset', fit: true, padding: 40 },
      wheelSensitivity: 0.2,
      style: [
        {
          selector: 'node',
          style: {
            shape: 'round-rectangle',
            width: 190, height: 46,
            'background-color': '#1A1D22',
            'border-width': 1.5,
            'border-color': ele => FAMILY_COLORS[ele.data('family')] || '#5B6068',
            label: 'data(label)',
            color: '#F6F7F8',
            'font-family': 'Geist Mono, monospace',
            'font-size': 9,
            'text-wrap': 'wrap',
            'text-max-width': 175,
            'text-valign': 'center',
            'text-halign': 'center',
          },
        },
        {
          selector: 'node:selected',
          style: { 'border-width': 3, 'border-color': '#FF6B3D', 'background-color': '#22262C' },
        },
        { selector: 'node.dim', style: { opacity: 0.14 } },
        { selector: 'node.hit', style: { 'border-width': 3 } },
        {
          selector: 'edge',
          style: {
            width: 1.2,
            'curve-style': 'unbundled-bezier',
            'control-point-distances': [40],
            'control-point-weights': [0.5],
            'line-color': ele => KIND_STYLES[ele.data('kind')].color,
            'line-style': ele => KIND_STYLES[ele.data('kind')].style,
            'target-arrow-shape': 'triangle',
            'target-arrow-color': ele => KIND_STYLES[ele.data('kind')].color,
            'arrow-scale': 0.7,
            opacity: 0.55,
          },
        },
        { selector: 'edge.dim', style: { opacity: 0.05 } },
        { selector: 'edge.focus', style: { opacity: 1, width: 2.2 } },
      ],
    });

    /* ── Filtres familles ── */
    const famBox = document.getElementById('bp-families');
    famBox.innerHTML = FAMILY_ORDER.filter(f => byFamily[f]).map(f => {
      const famMeta = (cat.families || []).find(x => x.id === f);
      const title = famMeta ? famMeta.name : f;
      return `<label class="bp-filter" title="${esc(famMeta?.description || '')}">
        <input type="checkbox" data-family="${f}" checked/>
        <span class="dot" style="background:${FAMILY_COLORS[f]}"></span>${f} · ${esc(title)}
        <span class="cnt">${byFamily[f].length}</span></label>`;
    }).join('');

    /* ── Filtres kinds ── */
    const kindCounts = {};
    for (const e of edges) kindCounts[e.data.kind] = (kindCounts[e.data.kind] || 0) + 1;
    document.getElementById('bp-kinds').innerHTML = Object.entries(KIND_STYLES)
      .filter(([k]) => kindCounts[k])
      .map(([k, s]) => `<label class="bp-filter">
        <input type="checkbox" data-kind="${k}" checked/>
        <span class="line ${s.style}" style="border-color:${s.color}"></span>${esc(s.label)}
        <span class="cnt">${kindCounts[k]}</span></label>`).join('');

    function applyFilters() {
      const famOn = new Set([...document.querySelectorAll('[data-family]:checked')].map(i => i.dataset.family));
      const kindOn = new Set([...document.querySelectorAll('[data-kind]:checked')].map(i => i.dataset.kind));
      const q = document.getElementById('bp-search').value.trim().toLowerCase();
      cy.batch(() => {
        cy.nodes().forEach(n => {
          const famOk = famOn.has(n.data('family'));
          const qOk = !q || n.data('id').toLowerCase().includes(q) || n.data('pattern').name.toLowerCase().includes(q);
          n.toggleClass('dim', !(famOk && qOk));
          n.toggleClass('hit', Boolean(q) && famOk && qOk);
        });
        cy.edges().forEach(e => {
          const visible = kindOn.has(e.data('kind')) && !e.source().hasClass('dim') && !e.target().hasClass('dim');
          e.toggleClass('dim', !visible);
        });
      });
    }
    document.getElementById('bp-families').addEventListener('change', applyFilters);
    document.getElementById('bp-kinds').addEventListener('change', applyFilters);
    document.getElementById('bp-search').addEventListener('input', applyFilters);

    /* ── Panneau de détail ── */
    const detail = document.getElementById('bp-detail');
    const relByPattern = {};
    for (const r of cat.relations) {
      (relByPattern[r.from] = relByPattern[r.from] || []).push({ ...r, dir: 'out' });
      (relByPattern[r.to] = relByPattern[r.to] || []).push({ ...r, dir: 'in' });
    }

    function showPattern(p) {
      const color = FAMILY_COLORS[p.family];
      const famMeta = (cat.families || []).find(x => x.id === p.family);
      const rels = (relByPattern[p.id] || []).map(r => {
        const other = r.dir === 'out' ? r.to : r.from;
        const arrow = r.dir === 'out' ? '→' : '←';
        return `<div class="bp-d-rel"><span class="k">${arrow} ${esc(KIND_STYLES[r.kind].label)}</span>
          <a data-goto="${esc(other)}">${esc(other)}</a>
          <span class="lbl">${esc(r.label || '')}</span></div>`;
      }).join('');
      detail.innerHTML = `
        <span class="bp-d-id" style="color:${color};border-color:${color}">${esc(p.id)}</span>
        ${p.maturity ? `<span class="bp-d-mat" style="color:${MATURITY_COLORS[p.maturity] || 'var(--ink-soft)'}">${esc(p.maturity)}</span>` : ''}
        <div class="bp-d-name">${esc(p.name)}</div>
        <div class="bp-d-fam">${esc(famMeta ? famMeta.name : p.family)}</div>
        <div class="bp-d-sec"><h4>Intention</h4><p>${esc(p.intent)}</p></div>
        <div class="bp-d-sec"><h4>Problème</h4><p>${esc(p.problem)}</p></div>
        <div class="bp-d-sec"><h4>Solution</h4><p>${esc(p.solution)}</p></div>
        ${p.controls && p.controls.length ? `<div class="bp-d-sec"><h4>Contrôles</h4><ul>${p.controls.map(c => `<li>${esc(c)}</li>`).join('')}</ul></div>` : ''}
        ${p.antiPattern ? `<div class="bp-d-sec"><h4>Anti-pattern</h4><p>${esc(p.antiPattern)}</p></div>` : ''}
        ${rels ? `<div class="bp-d-sec"><h4>Relations</h4>${rels}</div>` : ''}
        <div class="bp-d-doc">${esc(p.docPath)}</div>`;
      detail.classList.add('open');
      detail.querySelectorAll('[data-goto]').forEach(a => {
        a.addEventListener('click', () => {
          const n = cy.getElementById(a.dataset.goto);
          if (n.length) { cy.animate({ center: { eles: n }, zoom: 1 }, { duration: 240 }); n.select(); }
        });
      });
    }

    cy.on('select', 'node', evt => {
      const n = evt.target;
      showPattern(n.data('pattern'));
      cy.edges().removeClass('focus');
      n.connectedEdges().not('.dim').addClass('focus');
    });
    cy.on('unselect', 'node', () => {
      cy.edges().removeClass('focus');
      detail.classList.remove('open');
    });
  }
})();
