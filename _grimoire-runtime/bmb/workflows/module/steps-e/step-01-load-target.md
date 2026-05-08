---
name: 'step-01-load-target'
description: 'Load target for editing'

nextStepFile: './step-02-select-edit.md'
moduleStandardsFile: '../data/module-standards.md'
---

# Step 1: Load Target (Edit Mode)

## STEP GOAL:

Load the target (brief, module.yaml, agent specs, or workflow specs) for editing.

## MANDATORY EXECUTION RULES:

### Universal Rules:
- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ Speak in `{communication_language}`

### Role Reinforcement:
- ✅ You are the **Module Editor** — helpful, ready to assist
- ✅ Understand what we're editing

---

## MANDATORY SEQUENCE

### 1. Determine Edit Target

If routing already provided a concrete target path or target type, use it directly and skip the chooser below.

In autonomous posture, infer the target type from the provided path when possible:
- `module-brief-*.md` → **Brief**
- `module.yaml` or a module root directory → **Yaml**
- `/agents/` or an agent spec file → **Agents**
- `/workflows/` or a workflow spec file → **Workflows**
- `README.md` or `TODO.md` → **Docs**

Only present the menu when the target type or target path remains unclear.

"**What would you like to edit?**"

Options:
- **[B]rief** — Module brief from Brief mode
- **[Y]aml** — module.yaml configuration
- **[A]gents** — Agent specifications
- **[W]orkflows** — Workflow specifications
- **[D]ocs** — README.md or TODO.md

### 2. Load Target

Based on the resolved selection or inferred target, load the target file(s).

**IF Brief:**
- Path: `{bmb_creations_output_folder}/modules/module-brief-{code}.md`

**IF Yaml:**
- Path: `src/modules/{code}/module.yaml`

**IF Agents:**
- Path: `src/modules/{code}/agents/`
- List available agent specs

**IF Workflows:**
- Path: `src/modules/{code}/workflows/`
- List available workflow specs

**IF Docs:**
- Path: `src/modules/{code}/README.md` or `TODO.md`

### 3. Display Current Content

Show the current content of the target file.

"**Here's the current content:**"

{display relevant sections or summary}

### 4. Proceed to Selection

"**What would you like to change?**"

Load `{nextStepFile}` to select the edit type.

---

## Success Metrics

✅ Target loaded
✅ Current content displayed
✅ Ready to select edit type
