# BRAINSTORM — DevOps Agents, Outils Experts Externes, Task Management Agents

> **Date** : 2026-03-08
> **Auteur** : BMad Master (Guilhem)
> **Scope** : 3 axes majeurs — Agent DevOps Lifecycle, MCP Expert Tools, Agent Task System
> **Méthode** : Brainstorm → Débat contradictoire → Architecture → Implémentation

---

## Table des matières

1. [Axe 1 — Agent Development Lifecycle (DevOps for Agents)](#axe-1)
2. [Axe 2 — Agents Experts avec Outils Externes (MCP + Vision)](#axe-2)
3. [Axe 3 — Agent Task System (ATS) — Gestion de tâches par et pour les agents](#axe-3)
4. [Débat contradictoire](#debate)
5. [Architecture unifiée](#architecture)
6. [Plan d'implémentation](#implementation)

---

## <a id="axe-1"></a>Axe 1 — Agent Development Lifecycle (ADL)

### Problème actuel

Le cycle de vie d'un agent Grimoire est aujourd'hui **linéaire et manuel** :
1. `agent-forge.py` génère un `.proposed.md`
2. Review humain
3. Installation manuelle
4. Pas de tests automatisés de l'agent en tant qu'entité
5. Pas de versioning d'agent
6. Pas de rollback
7. Pas de métriques de performance agent

### Vision : Agent DevOps Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                    AGENT DEVELOPMENT LIFECYCLE                    │
│                                                                  │
│  ┌──────┐  ┌──────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌─────┐│
│  │FORGE │→ │BUILD │→ │ TEST  │→ │REVIEW │→ │DEPLOY │→ │WATCH││
│  │      │  │      │  │       │  │       │  │       │  │     ││
│  │idea→ │  │lint  │  │bench  │  │peer   │  │stage →│  │perf ││
│  │DNA   │  │schema│  │sandbox│  │advrsrl│  │canary→│  │drift││
│  │      │  │deps  │  │chaos  │  │human  │  │prod   │  │alert││
│  └──────┘  └──────┘  └───────┘  └───────┘  └───────┘  └─────┘│
│      ↑                                           │              │
│      └───────────── FEEDBACK LOOP ──────────────┘              │
└──────────────────────────────────────────────────────────────────┘
```

### Composants proposés

#### 1.1 Agent Build System (`agent-build.py`)

```yaml
# agent.build.yaml — Manifest de build d'un agent
agent_id: blender-expert
version: "1.0.0"
base: creative-studio/art-director  # héritage

dependencies:
  mcp_servers:
    - name: blender-mcp
      required: true
      version: ">=0.1.0"
    - name: vision-mcp
      required: true
  tools:
    - image-prompt
    - sensory-buffer
  skills:
    - 3d-modeling
    - visual-evaluation

build_steps:
  - validate_dna_schema
  - check_mcp_connectivity
  - resolve_dependencies
  - compile_persona       # merge base + overrides
  - generate_test_suite   # auto-generate from capabilities
  - snapshot_baseline     # digital twin baseline
```

#### 1.2 Agent Test Framework (`agent-test.py`)

Tests automatisés d'agent — pas des tests unitaires classiques, mais des **behavioral tests** :

```python
# Tests comportementaux d'agent
class AgentBehavioralTest:
    """Test qu'un agent se comporte comme attendu."""

    def test_persona_consistency(self):
        """L'agent maintient sa persona sur 10 interactions."""

    def test_tool_proficiency(self):
        """L'agent utilise correctement ses outils MCP."""

    def test_boundary_respect(self):
        """L'agent ne sort pas de son domaine."""

    def test_handoff_quality(self):
        """L'agent produit des outputs exploitables par d'autres agents."""

    def test_failure_graceful(self):
        """L'agent gère proprement un outil indisponible."""

    def test_vision_loop(self):
        """L'agent évalue visuellement son output et itère si nécessaire."""
```

#### 1.3 Agent Staging & Canary (`agent-deploy.py`)

```
Production Traffic
       │
  ┌────┴────┐
  │ Router  │
  │ 95%/5%  │
  ├────┬────┤
  │    │    │
  ▼    │    ▼
PROD   │  CANARY
v1.2   │  v1.3
  │    │    │
  └────┴────┘
       │
  Métriques comparées
  Si OK → promote canary
  Si KO → rollback auto
```

#### 1.4 Agent Drift Detection (`agent-watch.py`)

Détecte quand un agent dérive de son comportement baseline :
- Score de persona consistency
- Taux d'utilisation des bons outils
- Qualité des outputs (via vision ou métriques)
- Temps de réponse
- Taux d'échec

---

## <a id="axe-2"></a>Axe 2 — Agents Experts avec Outils Externes (MCP + Vision)

### Problème actuel

- `image-prompt.py` génère des prompts texte mais n'appelle aucun outil
- L'archétype `creative-studio` a des agents sans bras : ils pensent mais n'agissent pas
- Aucun agent ne peut évaluer visuellement un résultat
- Le `mcp-proxy.py` liste des serveurs mais n'intègre pas de workflow expert

### Approche critique — Pourquoi pas juste "ajouter du MCP" ?

**Argument POUR** MCP direct (Blender, Figma, etc.) :
- Standard ouvert, écosystème croissant
- Les serveurs MCP existent déjà (blender-mcp, figma-mcp, etc.)
- Intégration native avec VS Code, Claude Desktop

**Argument CONTRE** MCP direct naïf :
- Un agent qui a accès à Blender ≠ un expert Blender
- MCP expose des outils, pas de l'expertise
- Sans vision/feedback, l'agent est aveugle
- Le coût tokens d'un workflow itératif 3D peut être prohibitif

**VERDICT : Approche hybride — MCP + Expertise Layer + Vision Loop**

### Architecture : Expert Tool Chain (ETC)

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXPERT TOOL CHAIN (ETC)                        │
│                                                                  │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────────┐        │
│  │ EXPERTISE │   │  MCP BRIDGE  │   │   VISION JUDGE   │        │
│  │  LAYER    │   │              │   │                  │        │
│  │           │   │ stdin/stdout │   │ Screenshot →     │        │
│  │ Domain    │   │ protocol     │   │ Multimodal LLM → │        │
│  │ Knowledge │   │              │   │ Quality Score    │        │
│  │ + Best    │   │ Blender MCP  │   │ + Feedback       │        │
│  │ Practices │   │ Figma MCP    │   │                  │        │
│  │ + Error   │   │ SVG MCP      │   │ Accepte / Rejette│        │
│  │ Patterns  │   │ Inkscape MCP │   │ + Instructions   │        │
│  └─────┬─────┘   └──────┬───────┘   └───────┬──────────┘        │
│        │                │                    │                   │
│        └────────────────┼────────────────────┘                   │
│                         │                                        │
│              ┌──────────▼──────────┐                             │
│              │   ITERATION ENGINE  │                             │
│              │                     │                             │
│              │  attempt 1 → judge  │                             │
│              │  attempt 2 → judge  │                             │
│              │  attempt 3 → ACCEPT │                             │
│              │  or ESCALATE        │                             │
│              └─────────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.1 Blender MCP Expert Agent

```yaml
agent_id: blender-expert
name: "Blender 3D Expert"
icon: "🎲"
domain: 3d-modeling

mcp_servers:
  - name: blender-mcp
    package: "blender-mcp"  # npm ou pip
    startup: "blender --background --python blender_mcp_server.py"
    capabilities:
      - create_mesh
      - apply_material
      - set_lighting
      - render_scene
      - export_format

expertise_layer:
  knowledge_base:
    - topology: "Quad-based topology for deformation, triangulate only for game export"
    - materials: "PBR workflow: Base Color, Metallic, Roughness, Normal"
    - lighting: "Three-point lighting as baseline, HDRI for realistic environments"
    - scale: "Real-world units, 1 BU = 1 meter"
  
  workflow_patterns:
    simple_object:
      steps: [create_base_mesh, subdivide, sculpt_detail, apply_material, light, render]
      max_iterations: 5
    scene_composition:
      steps: [block_out, refine_hero, populate_secondary, material_pass, lighting_pass, render]
      max_iterations: 8

vision_loop:
  enabled: true
  method: render_and_evaluate
  render_settings:
    resolution: [1920, 1080]
    samples: 64  # Low for preview, 256+ for final
    format: png
  evaluation_criteria:
    - name: geometry_quality
      weight: 0.3
      checks: ["no_ngons", "clean_topology", "proper_normals"]
    - name: material_quality
      weight: 0.2
      checks: ["pbr_correct", "no_stretching", "proper_scale"]
    - name: composition
      weight: 0.2
      checks: ["balanced_frame", "focal_point", "no_clipping"]
    - name: lighting
      weight: 0.15
      checks: ["no_blown_highlights", "visible_shadows", "mood_match"]
    - name: overall_aesthetic
      weight: 0.15
      checks: ["professional_quality", "matches_brief", "print_ready"]
  acceptance_threshold: 0.75
  max_attempts: 5
  escalation: "human_review"
```

### 2.2 SVG/Illustration Expert Agent

**Débat : SVG code vs outil dédié ?**

| Approche | Pour | Contre |
|----------|------|--------|
| SVG code pur | Simple, versionable, léger | Résultats souvent médiocres, pas de courbes complexes |
| Inkscape MCP | Pro-level, filtres, paths complexes | Plus lourd, dépendance externe |
| Figma MCP | Collaboratif, design system natif | Cloud-dependent, API limitée |
| Recraft/DALL-E API | Résultats impressionnants | Non-déterministe, pas éditable |

**VERDICT : Pipeline hybride**

```
Brief → SVG Code (structure) → Inkscape MCP (raffinement) → Vision Judge → Export
                                     ↑
                              OU     │
                                     │
Brief → AI Image Gen (concept) → Vectorize → Inkscape MCP (cleanup) → Vision Judge → Export
```

```yaml
agent_id: illustration-expert
name: "Illustration & SVG Expert"
icon: "✏️"
domain: vector-graphics

mcp_servers:
  - name: inkscape-mcp
    package: "inkscape-mcp"
    capabilities: [create_path, edit_path, apply_filter, export_svg, export_png]
  - name: recraft-api  # optionnel, pour génération IA
    type: http
    capabilities: [generate_icon, generate_illustration, vectorize]

expertise_layer:
  knowledge_base:
    - svg_optimization: "Minify paths, remove metadata, use viewBox properly"
    - icon_grid: "24x24 or 16x16 grid, 2px stroke, rounded caps"
    - accessibility: "title + desc elements, proper aria labels"
    - color_systems: "Design tokens → CSS custom properties, dark mode support"

vision_loop:
  enabled: true
  method: render_and_evaluate
  evaluation_criteria:
    - name: clarity
      weight: 0.3
      checks: ["readable_at_16px", "distinguishable_shapes", "no_aliasing"]
    - name: consistency
      weight: 0.25
      checks: ["matches_design_system", "consistent_stroke_width", "grid_aligned"]
    - name: accessibility
      weight: 0.2
      checks: ["contrast_ratio_ok", "not_color_dependent", "svg_has_title_desc"]
    - name: file_quality
      weight: 0.25
      checks: ["optimized_paths", "no_raster_embedded", "proper_viewbox"]
  acceptance_threshold: 0.80
```

### 2.3 Vision Judge System (`vision-judge.py`)

Le composant clé qui manque partout : **donner des yeux aux agents**.

```python
"""
vision-judge.py — Visual Quality Assessment for Agent Outputs.

Prend un screenshot/render/export et l'évalue via un LLM multimodal.
Retourne un score structuré + feedback actionnable.

Pipeline :
  1. Capture (screenshot, render, export file)
  2. Encode (base64 pour API multimodal)
  3. Evaluate (LLM multimodal avec rubric)
  4. Score (0-1 par critère + overall)
  5. Decide (accept / iterate / escalate)
  6. Feedback (instructions de correction si iterate)
"""

class VisionJudge:
    def evaluate(self, image_path, rubric, context):
        """
        Évalue une image selon une rubrique de critères.
        
        Returns:
            VisionVerdict:
                scores: dict[str, float]   # critère → score 0-1
                overall: float             # score pondéré
                decision: "accept" | "iterate" | "escalate"
                feedback: list[str]        # instructions de correction
                confidence: float          # confiance du jugement
        """
```

### 2.4 MCP Server Registry enrichi

Évolution de `mcp-proxy.py` → vrai registry avec health checks, capabilities mapping, et auto-discovery.

```yaml
# _grimoire/_config/mcp-servers.yaml (enrichi)
servers:
  - name: blender-mcp
    command: "blender --background --python-expr 'import blender_mcp; blender_mcp.serve()'"
    category: 3d
    capabilities:
      tools: [create_mesh, apply_material, set_lighting, render_scene]
      input_types: [text, json]
      output_types: [mesh, image, scene_file]
    health_check:
      method: ping
      interval: 30s
      timeout: 5s
    agent_affinity: [blender-expert, 3d-artist]
    
  - name: inkscape-mcp
    command: "inkscape-mcp-server"
    category: vector
    capabilities:
      tools: [create_svg, edit_path, export]
      input_types: [text, svg]
      output_types: [svg, png, pdf]
    agent_affinity: [illustration-expert, brand-designer]

  - name: vision-provider
    command: "python -m grimoire.mcp.vision_server"
    category: evaluation
    capabilities:
      tools: [evaluate_image, compare_images, extract_visual_features]
      input_types: [image/png, image/svg+xml, image/jpeg]
      output_types: [json]
    agent_affinity: ["*"]  # tous les agents créatifs
```

---

## <a id="axe-3"></a>Axe 3 — Agent Task System (ATS)

### Pourquoi PAS Kanban/Scrum/SAFe/Cascade ?

Ces méthodologies sont conçues pour des **humains** avec des contraintes humaines :
- Temps de context-switch élevé → d'où les sprints
- Mémoire limitée → d'où les stand-ups
- Communication lente → d'où les cérémonies
- Fatigue → d'où les limites WIP

Les agents n'ont **aucune** de ces contraintes. Ils ont d'**autres** contraintes :
- Context window limitée → besoin de compression intelligente
- Hallucination → besoin de validation continue
- Coût par token → besoin d'optimisation budget
- Pas de mémoire persistante native → besoin de state management
- Parallélisme possible → exploiter au max

### Vision : Agent Task System (ATS)

Un système conçu **par** et **pour** les agents, avec supervision humaine légère.

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT TASK SYSTEM (ATS)                       │
│                                                                  │
│  ┌─────────────┐                                                │
│  │  TASK GRAPH  │  ← DAG de dépendances, pas de backlog plat   │
│  │  (pas de     │                                               │
│  │   backlog)   │  Chaque nœud = TaskAtom                       │
│  └──────┬───────┘                                               │
│         │                                                        │
│  ┌──────▼────────┐  ┌───────────────┐  ┌──────────────────┐    │
│  │  SCHEDULER    │  │ AGENT POOL    │  │  RESULT JUDGE    │    │
│  │               │  │               │  │                  │    │
│  │  - Priority   │  │  - Available  │  │  - Auto-validate │    │
│  │  - Budget     │  │  - Busy       │  │  - Cross-check   │    │
│  │  - Deps ready │  │  - Cooldown   │  │  - Vision check  │    │
│  │  - Deadline   │  │  - Specialist │  │  - Contract verify│   │
│  └──────┬────────┘  └───────┬───────┘  └───────┬──────────┘    │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             │                                    │
│              ┌──────────────▼──────────────┐                    │
│              │     EXECUTION ENGINE        │                    │
│              │                             │                    │
│              │  Parallel when possible     │                    │
│              │  Sequential when deps       │                    │
│              │  Retry with mutation        │                    │
│              │  Escalate when stuck        │                    │
│              └─────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 TaskAtom — L'unité de travail agent

Pas une "user story", pas un "ticket". Un **TaskAtom** : la plus petite unité de travail significative pour un agent.

```yaml
# Exemple de TaskAtom
task_id: "ta-2026-0308-001"
type: creative  # creative | analytical | transformative | evaluative | meta
title: "Créer l'icône SVG du module memory"
description: "Icône 24x24 représentant une mémoire/cerveau, style line art"

# Graphe de dépendances (pas d'ordre de sprint !)
depends_on: ["ta-2026-0308-000"]  # design tokens doivent exister
blocks: ["ta-2026-0308-005"]       # la doc en a besoin
parallel_with: ["ta-2026-0308-002", "ta-2026-0308-003"]  # indépendants

# Affectation intelligente
required_capabilities: [svg-creation, icon-design, vision-evaluation]
preferred_agent: illustration-expert
fallback_agents: [brand-designer, dev]  # si l'expert n'est pas dispo

# Budget et contraintes
budget:
  max_tokens: 50000
  max_iterations: 5
  max_duration: "10m"
  cost_ceiling: "$0.50"

# Contrat de livraison
delivery_contract:
  outputs:
    - type: svg
      path: "docs/assets/icons/memory.svg"
      validation:
        - file_exists
        - svg_valid
        - viewbox_24x24
        - optimized_size_lt_5kb
    - type: png
      path: "docs/assets/icons/memory.png"
      validation:
        - file_exists
        - dimensions_48x48  # @2x
  quality_gate:
    vision_score: 0.80
    peer_review: optional
    human_approval: false  # auto-approve si vision_score >= threshold

# État
status: pending  # pending | scheduled | running | blocked | review | done | failed
attempts: 0
results: []
```

### 3.2 Task Graph vs Backlog

```
TRADITIONNEL (FLAT BACKLOG) :           AGENT TASK SYSTEM (DAG) :

  ┌────────┐                             A ──→ B ──→ E
  │ Task 1 │                             │     ↗
  │ Task 2 │  (pas de structure)         C ──→ D ──→ F ──→ G
  │ Task 3 │                                   ↑
  │ Task 4 │                                   H (parallèle avec C)
  │ ...    │
  └────────┘

Le DAG permet :
- Parallélisme automatique (C et H en même temps)
- Détection de blocages (si B échoue, E est bloqué)
- Chemin critique visible (C→D→F→G = chemin le plus long)
- Ré-ordonnancement dynamique sans cérémonie
```

### 3.3 Scheduler Intelligent

```python
class AgentScheduler:
    """
    Scheduler qui tient compte des contraintes agent-spécifiques.
    
    Facteurs de scheduling :
      1. Dépendances satisfaites ? (DAG)
      2. Agent qualifié disponible ?
      3. Budget restant suffisant ?
      4. Priorité ajustée par urgence + impact
      5. Token budget du context window
      6. Affinité MCP (l'agent a les bons serveurs ?)
    """
    
    def schedule_next(self) -> list[TaskAtom]:
        """Retourne les tâches prêtes à exécuter en parallèle."""
        ready = [t for t in self.graph if t.deps_satisfied and t.status == "pending"]
        return self.optimize_batch(ready)
    
    def optimize_batch(self, tasks):
        """
        Optimise le batch pour :
        - Maximiser le parallélisme
        - Minimiser les changements de contexte MCP
        - Respecter le budget global
        """
```

### 3.4 Feedback Loops Natifs

Contrairement aux sprints avec rétrospective en fin de cycle, l'ATS a des feedback loops **continus** :

```yaml
feedback_loops:
  immediate:
    - vision_judge_after_each_output
    - contract_verify_on_completion
    - budget_check_every_1000_tokens
  
  short_term:
    - agent_performance_after_5_tasks
    - drift_detection_hourly
    - dependency_health_check
  
  long_term:
    - weekly_agent_bench_report
    - cost_optimization_suggestions
    - capability_gap_analysis
```

---

## <a id="debate"></a>Débat Contradictoire

### Question 1 : MCP Blender — est-ce RÉELLEMENT viable aujourd'hui ?

**Pour (Amelia/Dev)** :
- blender-mcp existe déjà sur GitHub (plusieurs implémentations)
- Blender en mode `--background` est stable et scriptable
- Le pattern est identique à ce qu'on fait en CLI : on envoie des commandes, on récupère des résultats

**Contre (Winston/Architect)** :
- La modélisation 3D de qualité nécessite des centaines d'itérations avec feedback visuel rapide
- Le coût en tokens pour décrire une scène 3D complète est énorme
- Un humain avec Blender fait en 10 minutes ce qu'un agent fera en 2h et $50

**Synthèse** :
- ✅ Viable pour : objets simples (primitives, low-poly, icônes 3D, logos)
- ✅ Viable pour : modifications paramétriques (changer couleur, taille, matériau)
- ⚠️ Limite : modélisation organique complexe
- ❌ Pas viable pour : personnages haute-résolution, environnements complexes
- **RECOMMANDATION** : Commencer par les cas simples (icônes 3D, objets géométriques) avec cap budgétaire strict

### Question 2 : Vision Loop — quel modèle multimodal ?

**Options** :
| Modèle | Qualité vision | Coût | Latence |
|--------|---------------|------|---------|
| Claude Opus 4 | Excellent | Élevé | ~5s |
| Claude Sonnet 4 | Très bon | Moyen | ~2s |
| GPT-4o | Très bon | Moyen | ~2s |
| Gemini 2.0 | Bon | Bas | ~1s |
| Local (LLaVA) | Passable | Gratuit | ~10s |

**RECOMMANDATION** : Configurable dans `project-context.yaml`, défaut sur Sonnet 4 (bon ratio), avec fallback Gemini pour le budget-conscious.

### Question 3 : ATS — overengineering ?

**Pour la simplicité (Bob/SM)** :
- Un simple fichier YAML avec une liste ordonnée suffit
- Le DAG est intellectuellement élégant mais la complexité d'implémentation est réelle
- Les agents Grimoire travaillent séquentiellement la plupart du temps

**Contre la simplicité (Quinn/QA)** :
- Dès qu'on a 3+ agents en parallèle, un backlog plat crée des conflits
- Le digital-twin.py montre que le projet pense déjà en graphes
- L'orchestrator.py a déjà un mode concurrent-cpu
- Un DAG simple (dict + toposort) c'est 50 lignes de code, pas du rocket science

**VERDICT** : DAG simple. Pas de scheduler distribué, pas de système de queues complexes. Un fichier YAML qui décrit le graphe + un scheduler Python stdlib.

### Question 4 : SVG — code vs outil ?

**Pour le code SVG pur** :
- Versioning natif (git diff)
- Léger, pas de dépendance
- Les icônes simples sont faisables en SVG pur

**Pour l'outil (Inkscape MCP)** :
- Les paths de Bézier complexes sont quasi impossibles à coder à la main
- Inkscape est gratuit, installable partout, scriptable
- Les filtres SVG (blur, shadow, gradient mesh) sont complexes en code brut

**VERDICT** : Pipeline à 2 niveaux
1. **Niveau 1 (simple)** : SVG code pur pour icônes géométriques, badges, diagrammes
2. **Niveau 2 (avancé)** : Inkscape MCP pour illustrations complexes, logos, assets marketing

L'agent choisit le niveau selon la complexité de la demande.

---

## <a id="architecture"></a>Architecture Unifiée

### Nouveaux composants à créer

```
framework/tools/
  ├── agent-build.py          # [NEW] Build system pour agents
  ├── agent-test.py           # [NEW] Behavioral tests pour agents
  ├── agent-deploy.py         # [NEW] Staging/canary deployment
  ├── agent-watch.py          # [NEW] Drift detection & monitoring
  ├── vision-judge.py         # [NEW] Visual quality assessment
  ├── expert-tool-chain.py    # [NEW] MCP expertise + iteration
  ├── agent-task-system.py    # [NEW] ATS core (graph, scheduler, runner)
  ├── mcp-proxy.py            # [EVOLVE] → enrichir avec health checks
  ├── agent-forge.py          # [EVOLVE] → intégrer avec build system
  ├── tool-registry.py        # [EVOLVE] → MCP server capabilities
  └── image-prompt.py         # [EVOLVE] → connecter au vision loop

src/grimoire/
  └── mcp/
      ├── server.py           # [EVOLVE] → exposer ATS + vision tools
      ├── vision_server.py    # [NEW] MCP server pour vision evaluation
      └── external_bridge.py  # [NEW] Bridge vers MCP externes

archetypes/
  └── creative-studio/
      └── agents/
          ├── blender-expert.md       # [NEW]
          ├── illustration-expert.md  # [NEW]
          └── vision-judge.md         # [NEW] agent évaluateur visuel
```

### Configuration enrichie `project-context.yaml`

```yaml
# Ajouts à project-context.yaml
vision:
  provider: "anthropic"          # ou openai, google, local
  model: "claude-sonnet-4-20250514"
  fallback_model: "gemini-2.0-flash"
  max_cost_per_evaluation: 0.05  # $

agent_task_system:
  enabled: true
  graph_file: "_grimoire-output/.ats/task-graph.yaml"
  max_parallel_tasks: 3
  budget:
    daily_ceiling: "$5.00"
    per_task_ceiling: "$1.00"
  auto_approve_threshold: 0.85   # vision score

mcp_external:
  servers:
    - name: blender
      command: "blender --background --python blender_mcp.py"
      enabled: false  # opt-in
    - name: inkscape
      command: "inkscape-mcp"
      enabled: false
```

---

## <a id="implementation"></a>Plan d'Implémentation

### Phase 1 — Fondations (immédiat)

1. **`vision-judge.py`** — Le composant le plus transversal
2. **`agent-task-system.py`** — Core ATS avec DAG + scheduler
3. **Enrichir `mcp-proxy.py`** — Health checks + capabilities

### Phase 2 — Expert Tool Chain

4. **`expert-tool-chain.py`** — Pipeline expertise + vision loop
5. **Agent `blender-expert.md`** — Premier agent expert outil
6. **Agent `illustration-expert.md`** — SVG/icon expert

### Phase 3 — Agent DevOps

7. **`agent-build.py`** — Build system
8. **`agent-test.py`** — Behavioral tests
9. **`agent-deploy.py`** + **`agent-watch.py`** — Deploy + monitoring

---

## Priorités déterminées par impact × effort

| Composant | Impact | Effort | Ratio | Phase |
|-----------|--------|--------|-------|-------|
| vision-judge.py | 🔥🔥🔥 | Moyen | Élevé | 1 |
| agent-task-system.py | 🔥🔥🔥 | Élevé | Moyen | 1 |
| expert-tool-chain.py | 🔥🔥 | Moyen | Moyen | 2 |
| mcp-proxy enrichi | 🔥🔥 | Faible | Élevé | 1 |
| blender-expert agent | 🔥🔥 | Moyen | Moyen | 2 |
| illustration-expert agent | 🔥🔥 | Moyen | Moyen | 2 |
| agent-build.py | 🔥 | Moyen | Moyen | 3 |
| agent-test.py | 🔥🔥 | Élevé | Moyen | 3 |
| agent-deploy.py | 🔥 | Moyen | Faible | 3 |
| agent-watch.py | 🔥 | Moyen | Faible | 3 |

---

## État d'Implémentation (mis à jour 2026-03-09)

### ✅ Phase 1 — Fondations (TERMINÉE)
- [x] `vision-judge.py` — 4 rubrics, SVG offline validation, MCP tools, CLI  (Grade A, lint clean)
- [x] `agent-task-system.py` — DAG, toposort, scheduler, budget, delivery contract, MCP tools, CLI
- [x] `mcp-proxy.py` v2.0 — capabilities, health checks, agent affinity, blender/inkscape/vision servers

### ✅ Phase 2 — Expert Tool Chain (TERMINÉE)
- [x] `expert-tool-chain.py` — 5 expertise profiles, iteration engine, MCP bridge
- [x] `blender-expert.md` — Agent "Voxel", Grade A (0.94), 17/17 tests passed
- [x] `illustration-expert.md` — Agent "Pixel", Grade A (0.94), 16/17 → 17/17 after fix

### ✅ Phase 3 — Agent DevOps (TERMINÉE)
- [x] `agent-build.py` — Validation, dependency resolution, baseline generation
- [x] `agent-test.py` — 6 catégories comportementales, benchmark, history, suites full/quick
- [x] `agent-watch.py` — Fingerprint, baseline, drift detection multi-vecteur, alertes
- [ ] `agent-deploy.py` — Staging/canary (REPORTÉ — pertinent uniquement en multi-instance)

### ✅ Intégration
- [x] `archetype.dna.yaml` creative-studio enrichi — 2 nouveaux agents, 2 nouveaux traits, MCP servers, tools
- [x] Tous lint clean (ruff 0 erreurs)
- [x] 58/58 tests de régression passent (test_python_tools + test_mcp_proxy)
- [x] Benchmark comparatif : blender-expert 0.94 = illustration-expert 0.94

### ✅ Phase 4 — Tool Resolution & Auto-Provision (TERMINÉE)
- [x] `tool-resolver.py` v1.0 — Le chaînon manquant : Intent→Tool Discovery→Provision→Plan
  - 12 capabilities dans le catalogue (3d-modeling, svg-creation, testing, web-browsing…)
  - 12 intent patterns FR/EN → matching automatique capabilities
  - 6 modes CLI : resolve, discover, check, provision, catalog, cache
  - 4 interfaces MCP : mcp_tool_resolve, mcp_tool_discover, mcp_tool_check, mcp_tool_provision
  - Provision sécurisée : whitelist de commandes, dry-run par défaut, confirmation requise
  - Cache de résolution avec expiration automatique
  - Log de provision en JSONL pour audit
- [x] `tool-advisor.py` enrichi — CTX-011 (outillage/discover/provision), CTX-007 étendu au resolver
- [x] Lint clean (0 erreurs ruff)
- [x] 269/269 tests de régression passent (outils connexes)

### ✅ Phase 5 — Deep Integration : Orchestrateur + Agents (TERMINÉE)
- [x] `orchestrator.py` v1.2 — Hook pre-execution tool-resolve
  - `_pre_resolve_tools()` : résout les outils nécessaires avant chaque step
  - `auto_resolve_tools=True` par défaut, désactivable
  - Charge tool-resolver.py via importlib (graceful degradation si absent)
  - Injecte `resolved_tools` dans le contexte des workers
  - 53/53 tests orchestrateur + 7 nouveaux tests pour le hook
- [x] `agent-base.md` framework — Nouvelle section TRP (Tool Resolution Protocol)
  - QUATRIÈME PRINCIPE fondateur : "un agent qui code ce qui existe déjà gaspille"
  - 5 étapes : Identifier → Résoudre → Vérifier → Provisionner → Utiliser
  - Exemples concrets d'utilisation (SVG, web, 3D)
  - Documentation web-browser.py (toujours disponible via urllib)
  - Règles explicites : pas de réinvention, check MCP via resolver
- [x] `archetype.dna.yaml` minimal — Trait `tool-resolve-first` (hérité par TOUS les archétypes)
- [x] `archetype.dna.yaml` creative-studio — Traits `tool-resolve-first` + `web-aware` + `tool-resolver` et `web-browser` dans tools_required
- [x] `archetype.dna.yaml` web-app — Traits `tool-resolve-first` + `web-aware` + tools_required
- [x] 22 agents mis à jour avec règles TOOL RESOLVE + WEB AWARE :
  - Creative-studio (4) : blender-expert, illustration-expert, brand-designer, content-creator
  - Web-app (2) : fullstack-dev, frontend-specialist
  - Stack (7) : python, typescript, go, docker, k8s, ansible, terraform
  - Infra-ops (7) : ops-engineer, backup-dr, k8s-navigator, monitoring, pipeline-architect, security-hardener, systems-debugger
  - Platform-engineering (4) : backend-engineer, deploy-orchestrator, platform-architect, reliability-engineer
- [x] `subagent-orchestration.md` — Règle 11 ajoutée : tool-resolve automatique pré-spawn
- [x] Lint clean sur fichiers modifiés
- [x] 295/295 tests de régression (orchestrateur + tool-resolver + web-browser + grimoire-mcp-tools + python-tools)
