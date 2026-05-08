# Automatic Workflow Detection

Companion to `architecture-docs/SKILL.md` — detection logic for routing user requests to the right workflow upon skill invocation.

**IMPORTANT**: Immediately upon skill invocation, analyze the user's request to detect their intent.

## Detection Logic

Check the user's original message (before `/architecture-docs` was invoked) for these patterns:

### Workflow 8: Diagram Generation

**Triggers:**

- Keywords: "generate", "create", "add", "update", "make" + "diagram", "diagrams", "Mermaid diagram", "architecture diagram"
- Examples: "generate my architecture diagrams", "create diagrams from ARCHITECTURE.md", "add diagrams to my architecture"
- Section-specific: "generate diagrams for Section 4", "create data flow diagrams"
- Format mentions: "Mermaid diagrams", "visual diagrams", "architecture diagrams"
- Reconciliation: "reconcile diagrams", "move diagrams", "consolidate diagrams"
- Audit/coverage: "check diagram coverage", "audit diagrams", "diagram completeness", "diagram audit"
- Placement: "diagrams in wrong location", "fix diagram placement", "diagram location"
- External intake: user provides external file path and mentions diagrams

**Action when detected:**

1. Confirm: "I'll help you generate architecture diagrams."
2. Jump directly to **Workflow 8, Step 1** (Diagram Type Selection)
3. Do NOT ask which workflow - proceed automatically

**Scope clarification**: Workflow 8 is for **regenerating, updating, or auditing diagrams on an existing ARCHITECTURE.md**. It is NOT how new architectures get their first diagrams — Workflow 1 (initial creation) auto-runs diagram generation as Step 7 (Mandatory Diagram Generation) and will not complete until the BLOCKING DIAGRAMS_GATE in Step 7.3 passes. If the user is creating a new architecture, route to Workflow 1, not Workflow 8.

### Workflow 9: Migrate to docs/ Structure

**Triggers:**

- Keywords: "migrate", "restructure", "split", "reorganize", "convert" + "architecture", "ARCHITECTURE.md"
- Size complaints: "too large", "too long", "hard to navigate", "split into files"
- Explicit: "migrate my architecture to the new structure", "convert to docs/ layout"

**Action when detected:**

1. Confirm: "I'll help you migrate ARCHITECTURE.md to the multi-file docs/ structure."
2. Jump directly to **Workflow 9, Step 1**
3. Do NOT ask which workflow - proceed automatically

### Workflow 10: Release Architecture Version

**Triggers:**

- Keywords: "release architecture", "release architecture version", "bump architecture version", "freeze architecture", "tag architecture version"
- Lifecycle: "publish architecture", "ship architecture", "finalize architecture", "architecture release"
- Semver: "bump architecture to major/minor/patch", "architecture v1.1.0"

**Action when detected:**

1. Confirm: "I'll run the Release Architecture Version workflow."
2. Read `RELEASE_WORKFLOW.md` for the full procedure
3. Jump directly to **Workflow 10, Step 1** (Read Current Version)
4. Do NOT ask which workflow — proceed automatically

### Other Workflows

If the user's request matches other documented workflows (1-10), follow their respective trigger patterns.

**Note**: Workflow 1 (new ARCHITECTURE.md creation) starts at Step 0 (PO Spec prerequisite check), then Step 0.5 (ADR pre-identification) establishes the **ADR Context Block** — a list of ADR candidates derived from PO Spec analysis that is maintained through all creation steps for decision consistency. **Workflow 1 always concludes with Step 7 (Mandatory Diagram Generation), which produces the 4 standard diagrams (Logical View ASCII, C4 L1, C4 L2, Detailed View) into `docs/03-architecture-layers.md` and a mode-aware set of sequence diagrams into `docs/04-data-flow-patterns.md`: in Phase Catalog mode (default — see `ARCHITECTURE_DOCUMENTATION_GUIDE.md` → Section 6 → "Mode selection") one `sequenceDiagram` per phase H4 in `## Phase Catalog` plus one full wire sequence per UC in `## End-to-End Wire Sequences`; in Single-Flow mode (legacy fallback) one `sequenceDiagram` per `### [Flow Name] Flow` H3. Step 7.3 is a BLOCKING audit gate (DIAGRAMS_GATE) — Workflow 1 does NOT print `✅ Architecture creation complete` until every mandatory diagram is verified present and Pre-Write-Validation-clean. There is no `SKIP DIAGRAMS` override.** See ARCHITECTURE_TYPE_SELECTION_WORKFLOW.md for the full flow and `examples/04-data-flow-patterns.example.md` for a Phase Catalog mode reference.

## If No Pattern Matches

If the user's request doesn't match any workflow triggers:

1. Acknowledge the skill invocation
2. Ask which workflow they want to use
3. Provide brief description of available workflows
