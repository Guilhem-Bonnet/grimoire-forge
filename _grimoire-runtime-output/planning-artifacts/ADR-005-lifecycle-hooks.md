---
title: "ADR-005: Lifecycle Hooks System for Observable Orchestration"
date: 2026-04-02
status: "PROPOSED"
deciders: ["Guilhem", "BMad Master"]
consulted: []
informed: ["All agents"]
---

# ADR-005: Lifecycle Hooks System for Observable Orchestration

## Context

The BMAD framework currently lacks a **non-invasive observation mechanism** for tracking session lifecycle events. This makes it difficult to:

1. **Capture learning** — failures/successes for future injection
2. **Debug sub-agent behavior** — understand what each agent is doing
3. **Optimize performance** — identify bottlenecks, memory hotspots
4. **Instrument workflows** — measure quality metrics per phase

Existing frameworks (claude-mem, gstack, superpowers) use **lifecycle hooks** to solve this:

- **claude-mem**: `SessionStart`, `PostToolUse`, `SessionEnd`
- **gstack**: Implicit logging + learning
- **superpowers**: Implicit state tracking

### Current State (Grimoire)

- ✅ Session-based memory exists
- ❌ No explicit observation points
- ❌ No failure capture mechanism
- ❌ No learning injection between sessions

### Desired State

```
┌─────────────────────────────────────────┐
│  BOD System (Behavior Observation Daemon) │
├─────────────────────────────────────────┤
│  SessionStart Hook                      │
│  ├─ Load memory snapshots               │
│  ├─ Inject learnings from failures      │
│  └─ Initialize agent registry           │
│                                          │
│  PostToolUse Hook                       │
│  ├─ Validate result quality             │
│  ├─ Capture outcome (success/fail)      │
│  ├─ Log metadata (latency, tokens)      │
│  └─ Detect anti-patterns                │
│                                          │
│  SessionEnd Hook                        │
│  ├─ Compress session logs → memory      │
│  ├─ Inject learning into failure museum │
│  ├─ Generate session summary            │
│  └─ Trigger optional cleanup            │
└─────────────────────────────────────────┘
```

## Decision

**Implement a Lifecycle Hooks System** (called **BOD — Behavior Observation Daemon**) with three synchronous hooks:

1. **`session_start`** — Fired when session initiates
2. **`post_tool_use`** — Fired after any tool completes
3. **`session_end`** — Fired when session closes

### Design Principles

1. **Non-invasive** — Hooks do NOT modify behavior, only observe
2. **Synchronous & Fast** — Hooks are synchronous (not async), must complete <50ms
3. **Composable** — Multiple listeners can register per hook
4. **Memory-protected** — Listeners cannot write to `_bmad/_memory/` directly
5. **Observable By Default** — All hook triggers logged to JSONL audit trail

### Architecture

```python
# Hook Manager
class HookManager:
    def __init__(self):
        self.listeners = {
            "session_start": [],
            "post_tool_use": [],
            "session_end": []
        }
    
    def register(self, hook_name: str, listener: Callable):
        """Register a listener for a hook"""
        self.listeners[hook_name].append(listener)
    
    def trigger(self, hook_name: str, context: dict) -> dict:
        """Synchronously trigger all listeners for a hook"""
        results = []
        for listener in self.listeners[hook_name]:
            try:
                result = listener(context)
                results.append({
                    "listener": listener.__name__,
                    "status": "success",
                    "data": result
                })
            except Exception as e:
                results.append({
                    "listener": listener.__name__,
                    "status": "error",
                    "error": str(e)
                })
        
        # Audit log (all triggers)
        audit_log("hook_triggered", {
            "hook": hook_name,
            "listener_count": len(self.listeners[hook_name]),
            "results": results,
            "timestamp": now()
        })
        
        return {"hook": hook_name, "results": results}

# Hook Signatures

def on_session_start(context: dict) -> dict:
    """
    Fired when session starts.
    
    Context:
    {
        "user": str,                    # Username
        "agents_available": [str],      # Loaded agent names
        "memory_budget": int,           # Token budget for this session
        "skills_loaded": [str],         # Available skills
        "session_id": str               # Unique session ID
    }
    
    Returns: observation_dict (optional)
    """
    pass

def on_post_tool_use(context: dict) -> dict:
    """
    Fired after any tool completes.
    
    Context:
    {
        "tool_name": str,               # Tool invoked
        "input": dict,                  # Tool input
        "output": str,                  # Tool output
        "status": str,                  # "success" | "timeout" | "error"
        "latency_ms": int,              # Execution time
        "tokens_used": int,             # Token cost
        "agent": str,                   # Calling agent
        "timestamp": str                # ISO timestamp
    }
    
    Returns: {
        "quality_score": float,         # 0-1, optional
        "alert": bool,                  # Flag for review
        "note": str                     # Free-form observation
    }
    """
    pass

def on_session_end(context: dict) -> dict:
    """
    Fired when session ends.
    
    Context:
    {
        "session_id": str,              # Same as session_start
        "duration_seconds": int,        # Total duration
        "tools_used": int,              # Total tools invoked
        "tokens_total": int,            # Total tokens used
        "success_rate": float,          # % of successful tools
        "critical_failures": [str],     # Failed tools
        "learnings": [str],             # Insights to capture
        "recommendations": [str]        # Improvements to recommend
    }
    
    Returns: {
        "memory_injection": dict,       # Data to inject into memory
        "cleanup": bool,                # Trigger cleanup?
        "summary": str                  # Session summary
    }
    """
    pass
```

### Built-in Listeners (Phase 1)

#### 1. **FailureCapturer** (on_post_tool_use)
```python
class FailureCapturer:
    def on_post_tool_use(context):
        if context["status"] == "error":
            # Log failure to JSONL for later injection
            failure_log = {
                "timestamp": context["timestamp"],
                "tool": context["tool_name"],
                "agent": context["agent"],
                "error": context["output"],
                "context": {
                    "input": context["input"],
                    "environment": {...}
                }
            }
            append_to_file("_bmad/_memory/failures.jsonl", failure_log)
```

#### 2. **QualityGate** (on_post_tool_use)
```python
class QualityGate:
    def on_post_tool_use(context):
        # Simple heuristics
        if context["latency_ms"] > 5000:
            return {"alert": True, "note": "Slow tool execution"}
        if context["tokens_used"] > 2000:
            return {"alert": True, "note": "High token cost"}
        return {"quality_score": 1.0}
```

#### 3. **LearningInjector** (on_session_start)
```python
class LearningInjector:
    def on_session_start(context):
        # Read failures.jsonl, inject patterns into memory
        failures = load_failures_jsonl()
        patterns = extract_patterns(failures)
        
        return {
            "injected_patterns": len(patterns),
            "memory_expanded_tokens": len(patterns) * 50
        }
```

#### 4. **SessionSummarizer** (on_session_end)
```python
class SessionSummarizer:
    def on_session_end(context):
        summary = f"""
        Session {context['session_id']}:
        - Duration: {context['duration_seconds']}s
        - Tools: {context['tools_used']}
        - Success rate: {context['success_rate']}%
        - Critical failures: {context['critical_failures']}
        - Learning: {context['learnings']}
        """
        
        return {
            "summary": summary,
            "memory_injection": {
                "type": "session_summary",
                "content": summary
            }
        }
```

### Integration Points

#### In BMad Master (SOG)
```python
class BMadMaster:
    def __init__(self):
        self.hooks = HookManager()
        # Register built-in listeners
        self.hooks.register("session_start", LearningInjector.on_session_start)
        self.hooks.register("post_tool_use", QualityGate.on_post_tool_use)
        self.hooks.register("post_tool_use", FailureCapturer.on_post_tool_use)
        self.hooks.register("session_end", SessionSummarizer.on_session_end)
    
    async def start_session(self):
        context = self._build_session_context()
        self.hooks.trigger("session_start", context)
    
    async def run_tool(self, tool_name, input):
        result = await tool_name(**input)
        context = self._build_tool_context(tool_name, input, result)
        self.hooks.trigger("post_tool_use", context)
        return result
    
    async def end_session(self):
        context = self._build_session_end_context()
        self.hooks.trigger("session_end", context)
```

### Benefits

1. ✅ **Observability** — All behavior captured by default
2. ✅ **Learning** — Failures become knowledge injection
3. ✅ **Debugging** — Understand agent behavior per hook
4. ✅ **Metrics** — Token usage, latency, quality tracked
5. ✅ **Non-invasive** — Hooks don't modify behavior
6. ✅ **Extensible** — Custom listeners can plug in

### Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Hooks too slow (<50ms enforcement) | Medium | Async option if needed, benchmarking |
| Hook failures break session | High | Try-except per listener, audit logging |
| Memory explosion (too much logging) | Medium | Compression + rotation policy |
| Listeners interfere with each other | Low | Isolation (no shared state) |

### Acceptance Criteria

- [ ] HookManager fully implemented + tested
- [ ] 4 built-in listeners working (Failure, QualityGate, Learning, Summary)
- [ ] All hooks <50ms latency on average
- [ ] Audit trail to JSONL working
- [ ] Integration with SOG complete
- [ ] Documentation + examples
- [ ] All tests passing

### Implementation Effort

- **Estimated**: 3-5 days
- **Complexity**: Low-Medium
- **Owner**: Core team
- **Blocked by**: None

### References

- claude-mem: Lifecycle hooks concept
- gstack: Failure logging + learning
- superpowers: Implicit state tracking
- BMAD: Session management + memory
