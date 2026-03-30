# VS Code Copilot Workflows — Quick Start Guide

Welcome! Your Grimoire project now includes **7 pre-configured VS Code Copilot workflows** to supercharge your development process.

## What Are Copilot Workflows?

They're intelligent, multi-step assistants that help you with common project tasks. Access them directly in VS Code using the `/` command in Copilot Chat.

## The 7 Workflows

### 1. 🚀 **Grimoire Session Bootstrap**
**Command**: `/grimoire-session-bootstrap`

Start a new work session with full context.

**What it does**:
- Loads your session chain and recent work
- Checks project health prerequisites
- Restores working context from memory
- Plans the work ahead

**Best for**: Starting a work day, resuming after a break, context recovery

**Usage**:
```
@Copilot /grimoire-session-bootstrap
```

---

### 2. 🏥 **Grimoire Health Check**

**Command**: `/grimoire-health-check`

Run comprehensive project diagnostics.

**What it does**:
- Verifies project structure integrity
- Checks memory system health
- Validates configuration files
- Identifies early warnings
- Generates health report

**Best for**: Pre-deployment verification, regular maintenance, troubleshooting

**Usage**:
```
@Copilot /grimoire-health-check
```

---

### 3. 💭 **Grimoire Dream**

**Command**: `/grimoire-dream`

Consolidate learnings across work sessions.

**What it does**:
- Analyzes cross-domain patterns
- Identifies emerging insights
- Deposits stigmergy signals
- Seeds incubator with actionable ideas
- Generates dream journal

**Best for**: End-of-day reflection, pattern recognition, innovation ideation

**Usage**:
```
@Copilot /grimoire-dream
```

---

### 4. ✅ **Grimoire Pre-Push**

**Command**: `/grimoire-pre-push`

Validate code before pushing to repository.

**What it does**:
- Runs all tests
- Executes linting
- Checks code harmony
- Validates preflight checklist
- Generates deployment report

**Best for**: Code quality assurance, pre-commit verification, CI/CD readiness

**Usage**:
```
@Copilot /grimoire-pre-push
```

---

### 5. 📝 **Grimoire Changelog**

**Command**: `/grimoire-changelog`

Generate release notes from git history.

**What it does**:
- Analyzes recent commits
- Loads session chain context
- Generates structured changelog
- Creates version bump summary
- Outputs release notes

**Best for**: Version releases, documentation, release communications

**Usage**:
```
@Copilot /grimoire-changelog
```

---

### 6. 📊 **Grimoire Status**

**Command**: `/grimoire-status`

Get a project status snapshot.

**What it does**:
- Lists installed agents
- Shows agent states
- Reports active processes
- Displays memory metrics
- Generates status report

**Best for**: Quick project overview, status reporting, team updates

**Usage**:
```
@Copilot /grimoire-status
```

---

### 7. 🔧 **Grimoire Self-Heal**

**Command**: `/grimoire-self-heal`

Diagnose and repair workflow failures.

**What it does**:
- Analyzes recent errors
- Runs diagnostic tests
- Generates repair suggestions
- Documents failures in failure museum
- Auto-repairs common issues

**Best for**: Incident response, error diagnosis, system recovery

**Usage**:
```
@Copilot /grimoire-self-heal
```

---

## How to Use Workflows

### In VS Code Copilot Chat

1. Open **Copilot Chat** (Cmd+Shift+I)
2. Type `/` to see available commands
3. Select the workflow you want
4. Copilot executes the workflow with full context

### Example Session

```
// Morning: Start your day
@Copilot /grimoire-session-bootstrap

// Work: Check project health
@Copilot /grimoire-health-check

// Afternoon: Quick status
@Copilot /grimoire-status

// Pre-commit: Validate before push
@Copilot /grimoire-pre-push

// Release: Generate changelog
@Copilot /grimoire-changelog

// End of day: Consolidate learnings
@Copilot /grimoire-dream

// If something breaks: Diagnose
@Copilot /grimoire-self-heal
```

## Workflow Location

All workflows are stored in:
```
.github/prompts/
├── grimoire-changelog.prompt.md
├── grimoire-dream.prompt.md
├── grimoire-health-check.prompt.md
├── grimoire-pre-push.prompt.md
├── grimoire-self-heal.prompt.md
├── grimoire-session-bootstrap.prompt.md
└── grimoire-status.prompt.md
```

## Customization

You can customize workflows by:

1. **Editing** `.github/prompts/{workflow-name}.prompt.md`
2. **Adding** project-specific instructions
3. **Adjusting** parameters and preferences
4. **Reloading** VS Code to apply changes

## Project Instructions

Additional project-specific instructions are available in:
```
.github/instructions/grimoire-project.instructions.md
```

These instructions are automatically loaded by Copilot and provide:
- Project conventions
- Code standards
- Communication preferences
- Development practices
- Memory guidelines

## Tips & Tricks

### 💡 Chain Workflows for Maximum Effect

```
// Complete morning routine
@Copilot /grimoire-session-bootstrap
@Copilot /grimoire-health-check
```

### 💡 Use Status for Decision Making

Before starting work:
```
@Copilot /grimoire-status
```

### 💡 Dream Before Sleep

End-of-day insight consolidation:
```
@Copilot /grimoire-dream
```

### 💡 Pre-Push Validation

Never commit without:
```
@Copilot /grimoire-pre-push
```

## Troubleshooting

### Workflow Not Appearing?
- Verify VS Code Copilot is enabled
- Check `.github/prompts/` directory exists
- Reload VS Code window (Cmd+R)

### Workflow Not Working?
- Run `/grimoire-health-check` to diagnose
- Check project context is loaded
- Verify memory system is operational

### Need Help?
- View this guide: **Copilot Chat** → **Question Mark** → **Workflows**
- Run health check: `/grimoire-health-check`
- Check memory: `_grimoire/_memory/`

## Next Steps

1. **Bookmark This Guide** for quick reference
2. **Try Each Workflow** to understand capabilities
3. **Customize** workflows for your project style
4. **Share** workflows with team members
5. **Integrate** into your daily development rhythm

---

**Happy coding with Grimoire! 🧙**

*Last updated: 2024 | Grimoire Kit v3.4.0+*
