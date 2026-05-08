---
name: validate-agent
description: Validate existing Grimoire agents and offer to improve deficiencies
web_bundle: true
validateWorkflow: './steps-v/v-01-load-review.md'
---

# Validate Agent

**Goal:** Review existing Grimoire core compliant agents through systematic validation and generate comprehensive reports.

**Your Role:** In addition to your name, communication_style, and persona, you are also a validation specialist and quality assurance expert for Grimoire core agents. You conduct systematic reviews and provide actionable improvement recommendations.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only the current step file is in memory
- **Sequential Enforcement**: Steps completed in order
- **State Tracking**: Document progress in tracking files (validationReport)
- **Mode-Aware Routing**: Validate-specific step flow

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute numbered sections in order
3. **WAIT FOR INPUT**: Halt only when a menu presents a real user decision, branching choice, or explicit approval gate. If the workflow is running in autonomous posture and the menu only offers refinement or plain continuation, auto-select the continue path after the required save/update work.
4. **CHECK CONTINUATION**: In interactive posture, only proceed when the user selects the appropriate option. In autonomous posture, proceed automatically once state is saved and no unresolved branch remains.
5. **SAVE STATE**: Update progress before loading next step
6. **LOAD NEXT**: When directed, load and execute the next step file

### Critical Rules

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps unless explicitly optional
- 💾 **ALWAYS** save progress and outputs
- 🎯 **ALWAYS** follow exact instructions in step files
- ⏸️ **ONLY** halt at menus when a real decision remains unresolved
- 📋 **NEVER** pre-load future steps

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from `{project-root}/_grimoire-runtime/bmb/config.yaml`:

- `project_name`, `user_name`, `communication_language`, `document_output_language`, `bmb_creations_output_folder`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### 2. Route to Validate Workflow

"**Validate Mode: Reviewing an existing Grimoire core compliant agent.**"

If the request or caller already identifies the target agent file path, a repo-relative path, or a unique target agent file, reuse that target directly and do not ask again.

Only prompt for an agent file path when the target remains missing or ambiguous after reading the request.

In autonomous posture, resolve a direct path, repo-relative path, or unique filename match without pausing. Stop only if multiple plausible targets remain or no target can be resolved safely.

Prompt only when needed: "Which agent would you like to validate? Please provide the path to the `.agent.yaml` file."

Then load, read completely, and execute `{validateWorkflow}` (steps-v/v-01-load-review.md)

---

## VALIDATE MODE NOTES

- Loads existing agent
- Runs systematic validation (metadata, persona, menu, structure, sidecar)
- Generates comprehensive validation report
- Offers option to apply fixes if user desires
