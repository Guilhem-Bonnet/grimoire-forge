---
name: 'step-01-mode-detection'
description: 'Determine execution mode (tech-spec vs direct), handle escalation, set state variables'

nextStepFile_modeA: './step-03-execute.md'
nextStepFile_modeB: './step-02-context-gathering.md'
---

# Step 1: Mode Detection

**Goal:** Determine execution mode, capture baseline, handle escalation if needed.

---

## STATE VARIABLES (capture now, persist throughout)

These variables MUST be set in this step and available to all subsequent steps:

- `{baseline_commit}` - Git HEAD at workflow start (or "NO_GIT" if not a git repo)
- `{execution_mode}` - "tech-spec" or "direct"
- `{tech_spec_path}` - Path to tech-spec file (if Mode A)
- `{autonomous_execution}` - "true" when the user explicitly wants uninterrupted execution, else "false"

---

## EXECUTION SEQUENCE

### 1. Capture Baseline

First, check if the project uses Git version control:

**If Git repo exists** (`.git` directory present or `git rev-parse --is-inside-work-tree` succeeds):

- Run `git rev-parse HEAD` and store result as `{baseline_commit}`

**If NOT a Git repo:**

- Set `{baseline_commit}` = "NO_GIT"

### 2. Load Project Context

Check if `{project_context}` exists (`**/project-context.md`). If found, load it as a foundational reference for ALL implementation decisions.

### 3. Parse User Input

Analyze the user's input to determine mode:

First determine execution posture:

- Set `{autonomous_execution}` = "true" when the user explicitly asks to implement, proceed, continue, follow a provided plan/spec, or otherwise signals that execution should run through without checkpoint prompts
- Set `{autonomous_execution}` = "false" when the user is exploratory, comparing options, or explicitly asking for planning/discussion first
- When the request is imperative and implementation-oriented, prefer `"true"`

### Mode A: Tech-Spec

- User provided a path to a tech-spec file (e.g., `quick-dev tech-spec-auth.md`)
- Load the spec, extract tasks/context/AC
- Set `{execution_mode}` = "tech-spec"
- Set `{tech_spec_path}` = provided path
- **NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-03-execute.md`

### Mode B: Direct Instructions

- User provided task description directly (e.g., `refactor src/foo.ts...`)
- Set `{execution_mode}` = "direct"
- **NEXT:** Evaluate escalation threshold, then proceed

---

## ESCALATION THRESHOLD (Mode B only)

Evaluate user input with minimal token usage (no file loading):

**Triggers escalation (if 2+ signals present):**

- Multiple components mentioned (dashboard + api + database)
- System-level language (platform, integration, architecture)
- Uncertainty about approach ("how should I", "best way to")
- Multi-layer scope (UI + backend + data together)
- Extended timeframe ("this week", "over the next few days")

**Reduces signal:**

- Simplicity markers ("just", "quickly", "fix", "bug", "typo", "simple")
- Single file/component focus
- Confident, specific request

Use holistic judgment, not mechanical keyword matching.

---

## ESCALATION HANDLING

### No Escalation (simple request)

If `{autonomous_execution}` is "true":

- Default to `[E] Execute directly`
- Do not present the P/E menu again
- **NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-02-context-gathering.md`

If `{autonomous_execution}` is "false":

Display: "**Select:** [P] Plan first (tech-spec) [E] Execute directly"

Menu handling logic:

- IF P: Direct user to `{quick_spec_workflow}`. **EXIT Quick Dev.**
- IF E: Ask for any additional guidance, then **NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-02-context-gathering.md`

Execution rules:

- ONLY halt and wait for user input if the menu was actually presented
- ONLY proceed from the menu when user makes a selection

---

### Escalation Triggered - Level 0-2

If `{autonomous_execution}` is "true":

- Note briefly that the work spans multiple components but still fits quick-dev
- Default to `[E] Execute directly`
- Do not present the escalation menu again
- **NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-02-context-gathering.md`

If `{autonomous_execution}` is "false":

Present: "This looks like a focused feature with multiple components."

Display:

**[P] Plan first (tech-spec)** (recommended)
**[W] Seems bigger than quick-dev** - Recommend the Full Grimoire Flow PRD Process
**[E] Execute directly**

Menu handling logic:

- IF P: Direct to `{quick_spec_workflow}`. **EXIT Quick Dev.**
- IF W: Direct user to run the PRD workflow instead. **EXIT Quick Dev.**
- IF E: Ask for guidance, then **NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-02-context-gathering.md`

Execution rules:

- ONLY halt and wait for user input if the menu was actually presented
- ONLY proceed from the menu when user makes a selection

---

### Escalation Triggered - Level 3+

When the scope is truly platform/system-wide and not already reduced to a concrete, bounded task list or acceptance criteria, present the menu below even if `{autonomous_execution}` is "true".

If the user has already supplied a concrete, bounded task list or acceptance criteria and explicitly asked for execution, you may accept `[E] Execute directly` without re-asking.

Present: "This sounds like platform/system work."

Display:

**[W] Start Grimoire** (recommended)
**[P] Plan first (tech-spec)** (lighter planning)
**[E] Execute directly** - feeling lucky

Menu handling logic:

- IF P: Direct to `{quick_spec_workflow}`. **EXIT Quick Dev.**
- IF W: Direct user to run the PRD workflow instead. **EXIT Quick Dev.**
- IF E: Ask for guidance, then **NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-02-context-gathering.md`

Execution rules:

- ONLY halt and wait for user input if the menu was actually presented
- ONLY proceed from the menu when user makes a selection

---

## NEXT STEP DIRECTIVE

**CRITICAL:** When this step completes, explicitly state which step to load:

- Mode A (tech-spec): "**NEXT:** read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-03-execute.md`"
- Mode B (direct, [E] selected): "**NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-02-context-gathering.md`"
- Escalation ([P] or [W]): "**EXITING Quick Dev.** Follow the directed workflow."

---

## SUCCESS METRICS

- `{baseline_commit}` captured and stored
- `{execution_mode}` determined ("tech-spec" or "direct")
- `{tech_spec_path}` set if Mode A
- `{autonomous_execution}` set correctly for the request posture
- Project context loaded if exists
- Escalation evaluated appropriately (Mode B)
- Explicit NEXT directive provided

## FAILURE MODES

- Proceeding without capturing baseline commit
- Not setting execution_mode variable
- Not setting autonomous_execution variable
- Loading step-02 when Mode A (tech-spec provided)
- Attempting to "return" after escalation instead of EXIT
- Presenting a checkpoint menu despite an explicit autonomous execution request on simple or level 0-2 work
- No explicit NEXT directive at step completion
