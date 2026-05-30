---
name: 'step-02-context-gathering'
description: 'Quick context gathering for direct mode - identify files, patterns, dependencies'

nextStepFile: './step-03-execute.md'
---

# Step 2: Context Gathering (Direct Mode)

**Goal:** Quickly gather context for direct instructions - files, patterns, dependencies.

**Note:** This step only runs for Mode B (direct instructions). If `{execution_mode}` is "tech-spec", this step was skipped.

---

## AVAILABLE STATE

From step-01:

- `{baseline_commit}` - Git HEAD at workflow start
- `{execution_mode}` - Should be "direct"
- `{autonomous_execution}` - Whether execution should continue without confirmation prompts
- `{project_context}` - Loaded if exists

---

## EXECUTION SEQUENCE

### 1. Identify Files to Modify

Based on user's direct instructions:

- Search for relevant files using glob/grep
- Identify the specific files that need changes
- Note file locations and purposes

### 2. Find Relevant Patterns

Examine the identified files and their surroundings:

- Code style and conventions used
- Existing patterns for similar functionality
- Import/export patterns
- Error handling approaches
- Test patterns (if tests exist nearby)

### 3. Note Dependencies

Identify:

- External libraries used
- Internal module dependencies
- Configuration files that may need updates
- Related files that might be affected

### 4. Create Mental Plan

Synthesize gathered context into:

- List of tasks to complete
- Acceptance criteria (inferred from user request)
- Order of operations
- Files to touch

---

## PRESENT CONTEXT AND PLAN

Always present a concise summary of the gathered context.

If `{autonomous_execution}` is "true":

- Present the context summary, inferred plan, and acceptance criteria
- State that autonomous execution was requested and you are proceeding immediately
- **NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-03-execute.md`

If `{autonomous_execution}` is "false", display to user:

```text
**Context Gathered:**

**Files to modify:**
- {list files}

**Patterns identified:**
- {key patterns}

**Plan:**
1. {task 1}
2. {task 2}
...

**Inferred AC:**
- {acceptance criteria}

Ready to execute? (y/n/adjust)
```

- **y:** Proceed to execution
- **n:** Gather more context or clarify
- **adjust:** Modify the plan based on feedback

---

## NEXT STEP DIRECTIVE

**CRITICAL:** When autonomous execution applies or when user confirms ready, explicitly state:

- autonomous: "**NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-03-execute.md`"
- **y:** "**NEXT:** Read fully and follow: `{project-root}/_grimoire-runtime/bmm/workflows/grimoire-quick-flow/quick-dev/steps/step-03-execute.md`"
- **n/adjust:** Continue gathering context, then re-present plan

---

## SUCCESS METRICS

- Files to modify identified
- Relevant patterns documented
- Dependencies noted
- Mental plan created with tasks and AC
- User confirmed readiness to proceed, or autonomous execution continued without confirmation

## FAILURE MODES

- Executing this step when Mode A (tech-spec)
- Proceeding without identifying files to modify
- Not presenting context summary before execution
- Asking for confirmation despite `{autonomous_execution}` being "true"
- Missing obvious patterns in existing code
