# Grimoire Workflows — Cheat Sheet

Print this! Bookmark this! Quick reference for the 7 workflows.

## Quick Access

| Workflow | Command | When | Time |
|----------|---------|------|------|
| 🚀 Bootstrap | `/grimoire-session-bootstrap` | Start day | 2min |
| 🏥 Health | `/grimoire-health-check` | Any time | 1min |
| 💭 Dream | `/grimoire-dream` | End day | 3min |
| ✅ Pre-Push | `/grimoire-pre-push` | Before commit | 5min |
| 📝 Changelog | `/grimoire-changelog` | Release | 3min |
| 📊 Status | `/grimoire-status` | Quick view | 30sec |
| 🔧 Self-Heal | `/grimoire-self-heal` | Errors | 2min |

---

## Daily Routine

```
    MORNING
    ↓
    /grimoire-session-bootstrap     (Load context)
    ↓
    /grimoire-health-check           (Verify health)
    ↓
    WORK...
    ↓
    /grimoire-status                 (Quick check)
    ↓
    WORK...
    ↓
    /grimoire-pre-push               (Before commit)
    ↓
    PUSH
    ↓
    EVENING
    ↓
    /grimoire-dream                  (Consolidate)
```

---

## By Use Case

### Starting Work
```
@Copilot /grimoire-session-bootstrap
```
✓ Loads context chain  
✓ Checks prerequisites  
✓ Plans ahead  

### Mid-Work Check
```
@Copilot /grimoire-status
```
✓ Project snapshot  
✓ Agent states  
✓ Quick metrics  

### Before Committing
```
@Copilot /grimoire-pre-push
```
✓ Runs tests  
✓ Lints code  
✓ Validates all  

### Preparing Release
```
@Copilot /grimoire-changelog
```
✓ Generates notes  
✓ Version summary  
✓ Release ready  

### Something Broke
```
@Copilot /grimoire-self-heal
```
✓ Diagnoses issue  
✓ Suggests fixes  
✓ Auto-repairs  

### Project Healthy?
```
@Copilot /grimoire-health-check
```
✓ Structure ok?  
✓ Memory ok?  
✓ Config ok?  

### End of Day
```
@Copilot /grimoire-dream
```
✓ Consolidates learning  
✓ Finds patterns  
✓ Seeds ideas  

---

## Key Files

| File | Purpose | Edit? |
|------|---------|-------|
| `_grimoire/_memory/shared-context.md` | Project truth | ✓ |
| `_grimoire/_memory/config.yaml` | Settings | ✓ |
| `.github/prompts/` | Workflows | ✓ |
| `_grimoire/_config/custom/agents/` | Custom agents | ✓ |
| `project-context.yaml` | Project config | ✓ |
| `.github/agents/` | Wrappers | ✗ Auto-generated |
| `_grimoire/_memory/decisions-log.md` | Decisions | ✓ Append |
| `_grimoire/_memory/failure-museum.md` | Errors | ✓ Append |

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Workflow not showing | Reload VS Code (Cmd+R) |
| Context not loading | Run `/grimoire-health-check` |
| Workflow slow | Check `_grimoire/_memory/` size |
| Agent confused | Load `shared-context.md` first |
| Tests failing | Run `/grimoire-self-heal` |
| Memory inconsistent | Update `shared-context.md` |

---

## Pro Tips

💡 **Chain commands** for complete workflow:
```
@Copilot /grimoire-session-bootstrap
@Copilot /grimoire-health-check
```

💡 **Use status** before major changes:
```
@Copilot /grimoire-status
```

💡 **Always pre-push** before committing:
```
@Copilot /grimoire-pre-push
```

💡 **Dream mode** finds patterns:
```
@Copilot /grimoire-dream
```

---

## Remember

| ✓ Do | ✗ Don't |
|-----|---------|
| Load shared-context.md first | Modify .github/agents/ manually |
| Update memory as you go | Guess information from context |
| Use workflows regularly | Commit without pre-push |
| Document decisions | Hardcode stack assumptions |
| Run health checks weekly | Commit secrets or tokens |

---

## Getting Help

**Stuck?** → `/grimoire-health-check`  
**Lost?** → `/grimoire-session-bootstrap`  
**Broken?** → `/grimoire-self-heal`  
**Questions?** → Check `_grimoire/_memory/shared-context.md`

---

**Last Updated**: 2024 | Grimoire Kit v3.4.0+

*Print this · Bookmark this · Share with team*
