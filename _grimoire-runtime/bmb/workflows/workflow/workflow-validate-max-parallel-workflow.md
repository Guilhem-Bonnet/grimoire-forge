---
name: validate-max-parallel-workflow
description: Run validation checks in MAX-PARALLEL mode against a workflow requires a tool that supports Parallel Sub-Processes
web_bundle: true
validateWorkflow: './steps-v/step-01-validate-max-mode.md'
---

# Validate Max-Parallel Workflow

**Goal:** Validate existing workflows against Grimoire standards using maximum parallel execution for comprehensive review.

**Your Role:** Validation Architect and Quality Assurance Specialist with parallel processing expertise. You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution with parallel optimization:

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Append-Only Building**: Build documents by appending content as directed to the output file
- **Parallel Optimization**: When available, use subprocess/Task tools to run independent validation steps in parallel

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu presents a real user decision, branching choice, or explicit approval gate, halt and wait for user selection. If `{autonomous_execution}` is true and the menu only offers refinement or plain continuation, auto-select the continue path after the required save/update work.
4. **CHECK CONTINUATION**: In interactive posture, only proceed to the next step when the user selects `C` (Continue). In autonomous posture, proceed automatically once state is saved and no unresolved branch remains.
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ONLY** halt at menus when a real decision remains unresolved
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from {project-root}/_grimoire-runtime/bmb/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`, `bmb_creations_output_folder`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### 2. Route to Validate Max-Parallel Workflow

"**Validate Max-Parallel Mode: Validating an existing workflow against Grimoire standards using maximum parallel execution.**"

If the request or caller already identifies the target workflow path, a repo-relative path, or a unique target workflow, reuse it directly and do not ask again.

Only prompt for the workflow path when the target remains missing or ambiguous after reading the request.

In autonomous posture, resolve a direct path, repo-relative path, or unique workflow match without pausing. Stop only if multiple plausible targets remain or no target can be resolved safely.

Prompt only when needed: "Which workflow would you like to validate? Please provide the path to the workflow.md file."

Then load, read completely, and execute `{validateWorkflow}` (steps-v/step-01-validate-max-mode.md)
