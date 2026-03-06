---
name: grimoire-project-explore
description: 'Explore BMAD Grimoire project structure and hidden patterns. Use when: project archeology, hidden patterns, dark matter, desire paths, project graph, orphan files, unused agents, dead code, bus factor, tribal knowledge, who knows what, implicit assumptions. Combines project-graph, dark-matter, and desire-paths analysis.'
---

# Grimoire Project Explore

Deep structural analysis: graph topology, tribal knowledge detection, and real-vs-designed usage patterns.

## When to Use

- Onboarding to the project (understanding hidden structure)
- Before major refactoring (know what you're touching)
- When something seems "off" but you can't pinpoint why
- When the user asks "what's unused?", "who knows what?", or "hidden patterns"
- Periodic structural hygiene review

## Procedure

### Step 1 — Project Graph (Topology)

```bash
python3 framework/tools/project-graph.py --project-root . build
```

Then check key topology metrics:

```bash
python3 framework/tools/project-graph.py --project-root . centrality
```

Identify the most connected nodes (agents, tools, workflows) — these are critical paths.

```bash
python3 framework/tools/project-graph.py --project-root . orphans
```

Find disconnected nodes — files that exist but aren't referenced by anything.

### Step 2 — Dark Matter Scan (Tribal Knowledge)

```bash
python3 framework/tools/dark-matter.py --project-root . scan
```

Detects:
- Undocumented conventions and naming patterns
- Implicit assumptions in artifacts
- Knowledge silos (bus factor = 1)
- Tacit dependencies between components

For specific deep-dives:

```bash
python3 framework/tools/dark-matter.py --project-root . silos     # Knowledge silos
python3 framework/tools/dark-matter.py --project-root . implicit  # Implicit assumptions
python3 framework/tools/dark-matter.py --project-root . patterns  # Unwritten conventions
```

### Step 3 — Desire Paths (Real vs Designed Usage)

```bash
python3 framework/tools/desire-paths.py --project-root . analyze
```

Compares actual usage against intended design:
- Which agents are activated vs which exist
- Which workflows are run vs which are defined
- Which tools are invoked vs which are available

```bash
python3 framework/tools/desire-paths.py --project-root . recommend
```

Recommendations based on usage patterns.

### Step 4 — Visual Export (Optional)

```bash
python3 framework/tools/project-graph.py --project-root . mermaid
```

Generates a Mermaid diagram of the project graph for visual inspection.

### Step 5 — Exploration Report

```
## 🔭 Project Exploration Report

### Graph Topology
- Total nodes: N (agents: X, tools: Y, workflows: Z)
- Orphans: N — [list]
- Most central: [top 5 nodes]
- Clusters: N detected

### Dark Matter
| Finding Type       | Count | Severity |
|--------------------|-------|----------|
| Undocumented patterns | N  | ⚠️       |
| Knowledge silos       | N  | 🔴       |
| Implicit assumptions  | N  | ⚠️       |
| Tacit dependencies    | N  | ⚠️       |

### Desire Paths
| Category   | Designed | Actually Used | Delta |
|------------|----------|---------------|-------|
| Agents     | N        | N             | ±N    |
| Workflows  | N        | N             | ±N    |
| Tools      | N        | N             | ±N    |

### Top Recommendations
1. [Based on orphans — candidates for cleanup or documentation]
2. [Based on silos — knowledge to distribute]
3. [Based on desire paths — design to align with reality]
```

## Notes

- All three tools are read-only — they analyze without modifying
- `dark-matter document` can auto-generate missing documentation
- Best run periodically (monthly) or before architectural decisions
- All tools support `--json` for machine-readable output
