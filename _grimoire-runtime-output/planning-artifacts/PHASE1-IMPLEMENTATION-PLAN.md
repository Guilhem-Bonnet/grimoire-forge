---
title: "PHASE 1 — Implementation Plan (Quick Wins)"
date: 2026-04-02
status: "ACTION READY"
timeline: "1-2 sprints (10-14 working days)"
owner: "Core team + Guilhem"
---

# PHASE 1 — Implementation Plan & Execution Roadmap

> **Note d'état (5 avril 2026)** : La couche SOG (auto-dispatch intent-based) est implémentée dans les instructions Copilot ([copilot-instructions.md](../../../.github/copilot-instructions.md)). Les hooks bash BMAD sont opérationnels (`.github/hooks/scripts/`). La partie **Python** (HookManager class, ProgressiveMemory, IntentClassifier) reste à implémenter selon ce plan.

## 🎯 Objective

Implement **3 Quick Wins** (Lifecycle Hooks + Progressive Disclosure + Auto-Dispatch) to achieve:
- ✅ **20-30% token savings** (immediate)
- ✅ **Cleaner UX** (fewer explicit commands)
- ✅ **Observable system** (audit trail + learning ready)
- ✅ **Foundation for Phase 2** (operational learning)

## 📊 Scope

### Work Items

#### **WI-1: Lifecycle Hooks System (ADR-005)**
- [ ] **HookManager class** (core/tasks/hooks.py)
  - [ ] `register(hook_name, listener)` — Register listener
  - [ ] `trigger(hook_name, context)` — Fire hooks synchronously
  - [ ] Audit logging to JSONL
  - [ ] Error isolation (hook failures don't crash)
  - [ ] Performance monitoring (<50ms)
  - [ ] Unit tests

- [ ] **Hook signatures** — Define 3 hooks
  - [ ] `session_start(context)` — SessionStart event
  - [ ] `post_tool_use(context)` — After tool completion
  - [ ] `session_end(context)` — Session termination
  - [ ] Context data structures (TypedDict)
  - [ ] Documentation + examples

- [ ] **Built-in listeners** (4 listeners)
  - [ ] **FailureCapturer** — Log failures to JSONL
    - [ ] Parse tool errors
    - [ ] Extract error patterns
    - [ ] Append to `_bmad/_memory/failures.jsonl`
    - [ ] Unit tests
  
  - [ ] **QualityGate** — Basic quality metrics
    - [ ] Latency threshold (warn >5s)
    - [ ] Token cost threshold (warn >2000)
    - [ ] Success rate tracking
    - [ ] Unit tests
  
  - [ ] **LearningInjector** — Inject learnings on session start
    - [ ] Read failures.jsonl
    - [ ] Extract anti-patterns
    - [ ] Inject into memory context (optional, Phase 1.5)
    - [ ] Unit tests
  
  - [ ] **SessionSummarizer** — Summarize at session end
    - [ ] Aggregate metrics
    - [ ] Generate human-readable summary
    - [ ] Append to session log
    - [ ] Unit tests

- [ ] **Integration with SOG** (bmad-master.md)
  - [ ] Hook initialization in `__init__`
  - [ ] Register built-in listeners
  - [ ] Call `trigger("session_start", ...)` at start
  - [ ] Call `trigger("post_tool_use", ...)` after tools
  - [ ] Call `trigger("session_end", ...)` at finish
  - [ ] Integration tests

- [ ] **Audit trail** (JSONL format)
  - [ ] File: `_bmad-output/test-artifacts/hooks-audit.jsonl`
  - [ ] Schema: `{"timestamp", "hook", "listeners", "results"}`
  - [ ] Rotation policy (keep last N entries)
  - [ ] Tests

- [ ] **Documentation**
  - [ ] Architecture overview (1 page)
  - [ ] API reference (hooks, context, listener pattern)
  - [ ] Example: Custom listener (3-5 lines)
  - [ ] Integration guide (for Phase 2 extensions)

**Estimated**: 3-5 days | **Owners**: Core team

---

#### **WI-2: Progressive Disclosure Memory (ADR-006)**
- [ ] **ProgressiveMemory class** (core/memory/progressive.py)
  - [ ] `search(query, layer="L1")` — Layer-aware search
  - [ ] `_hybrid_search(query, layer, token_limit)` — FTS + vector
  - [ ] `_format_by_layer(items, layer, token_limit)` — Format results
  - [ ] Compression logic (keep facts, drop verbosity)
  - [ ] Token estimation (accurate within 5%)
  - [ ] Performance (<100ms Layer 1, <300ms Layer 2, <500ms Layer 3)
  - [ ] Unit tests (all layers)

- [ ] **Layer specifications** (3 layers)
  - [ ] **Layer 1 (SEARCH)**: 50 tokens max
    - [ ] Format: title + date + 1-line summary
    - [ ] Test data sets
  
  - [ ] **Layer 2 (TIMELINE)**: 200 tokens max
    - [ ] Format: + category, sequence, tags
    - [ ] Test data sets
  
  - [ ] **Layer 3 (FETCH)**: 500+ tokens
    - [ ] Format: Full context + related items
    - [ ] Test data sets

- [ ] **Compression pipeline**
  - [ ] Fact extraction (noun phrases, verbs, metrics)
  - [ ] Summarization (1-line, 2-3 lines, full)
  - [ ] Sequence detection (for Layer 2)
  - [ ] Tests on real memory data (old sessions)

- [ ] **Hybrid search**
  - [ ] Full-text search (keyword matching)
  - [ ] Vector search (semantic similarity)
  - [ ] Result merge (dedup, prefer keyword matches)
  - [ ] Tests on diverse queries

- [ ] **Integration with Memory Manager**
  - [ ] Replace old `search()` with `search(layer="L1")`
  - [ ] Backward compatibility (default Layer 1)
  - [ ] Update all agent code calling memory
  - [ ] Integration tests

- [ ] **Integration with SOG** (optional, Phase 1.5)
  - [ ] Agent can request Layer 1 → Layer 2 → Layer 3
  - [ ] SOG tracks layer requests (for optimization)
  - [ ] Tests

- [ ] **Benchmarking**
  - [ ] Baseline: Current system token usage on 10 queries
  - [ ] New system token usage on same 10 queries
  - [ ] Target: 70% reduction
  - [ ] Report: Token savings by layer + query type

- [ ] **Documentation**
  - [ ] Architecture (3-layer model)
  - [ ] API reference (Layer 1/2/3 signatures)
  - [ ] Compression examples (before/after)
  - [ ] Integration guide (Agents calling progressive memory)
  - [ ] Benchmark results

**Estimated**: 4-6 days | **Owners**: Memory team

---

#### **WI-3: Auto-Dispatch on Intent**
- [ ] **Intent classifier** (core/orchestration/intent-classifier.py)
  - [ ] Lightweight regex-based detector (v1, no ML)
  - [ ] Patterns for: planning, architecture, coding, testing, review, docs
  - [ ] Input: User query
  - [ ] Output: `{intent: str, confidence: float, agent: str}`
  - [ ] Unit tests

- [ ] **Patterns library** (intents.yaml)
```yaml
intents:
  planning:
    patterns:
      - "plan|roadmap|strategy|timeline"
    agent: "pm"
    confidence: 0.9
  
  architecture:
    patterns:
      - "arch|design|scale|infrastructure"
    agent: "architect"
    confidence: 0.85
  
  coding:
    patterns:
      - "implement|code|feature|build"
    agent: "dev"
    confidence: 0.8
  
  review:
    patterns:
      - "review|quality|audit|improve"
    agent: "qa"
    confidence: 0.75
  # ... more intents
```

- [ ] **Integration with SOG** (bmad-master.md)
  - [ ] On user input, call `classifier.classify(query)`
  - [ ] If intent confidence > 0.7 → auto-dispatch to agent
  - [ ] Else → ask user which agent to dispatch
  - [ ] Track success (did auto-dispatch match user intent?)
  - [ ] Integration tests

- [ ] **Fallback strategy**
  - [ ] If confidence < 0.7 → show menu (don't auto-dispatch)
  - [ ] If agent not found → SOG general dispatch
  - [ ] Tests

- [ ] **Metrics collection**
  - [ ] Log intent classification per query
  - [ ] Track success rate (did agent match intent?)
  - [ ] Refine patterns based on data
  - [ ] Tests

- [ ] **Documentation**
  - [ ] Intent patterns (what triggers each agent)
  - [ ] Confidence scoring (how to read scores)
  - [ ] Integration (how to add new intent)
  - [ ] Examples (5-10 user inputs → classified correctly)

**Estimated**: 2-4 days | **Owners**: SOG team

---

## 📅 Timeline (Gantt-style)

```
Week 1
├─ Mon-Tue: WI-1 (HookManager + audit trail)
├─ Tue-Wed: WI-1 (Built-in listeners)
├─ Wed-Thu: WI-2 (ProgressiveMemory class + Layer 1)
└─ Thu-Fri: WI-2 (Layer 2 + Layer 3 + compression)

Week 2
├─ Mon: WI-3 (Intent classifier + patterns)
├─ Tue-Wed: WI-2 (Hybrid search + benchmarking)
├─ Wed-Thu: Integration tests (all 3 WIs)
├─ Thu-Fri: Documentation + demo prep
└─ Fri EOD: Phase 1 ready for review
```

## 🔄 Dependencies

```
WI-1 (Hooks)
  ↓
  └─→ WI-2 (Progressive Memory)
        ↓
        └─→ WI-3 (Auto-Dispatch)
               ↓
               └─→ SOG Integration
```

**Blocking**: None (parallel work possible)  
**Sequential**: Hooks first (needed for learning injection later), then Memory, then Dispatch

## ✅ Acceptance Criteria

### For WI-1 (Hooks)
- [ ] HookManager executes all listeners synchronously
- [ ] Hook failures isolated (don't crash)
- [ ] All hooks <50ms on average
- [ ] Audit trail JSONL appending
- [ ] 4 built-in listeners working (Failure, QualityGate, Learning, Summary)
- [ ] 95%+ test coverage
- [ ] Documentation complete

### For WI-2 (Progressive Memory)
- [ ] Layer 1 returns in <100ms
- [ ] Layer 2 returns in <300ms
- [ ] Layer 3 returns in <500ms
- [ ] Compression ratio 70%+ on real data
- [ ] Hybrid search catches 95%+ of keyword + semantic matches
- [ ] Backward compatible (existing code works)
- [ ] 95%+ test coverage
- [ ] Benchmark report (token savings by query type)
- [ ] Documentation complete

### For WI-3 (Auto-Dispatch)
- [ ] Intent classifier runs in <5ms
- [ ] 70%+ accuracy on test queries
- [ ] Fallback to menu if confidence < 0.7
- [ ] Metrics logged + tracked
- [ ] 90%+ test coverage
- [ ] Documentation complete

### Overall Phase 1
- [ ] All 3 WIs complete + tested
- [ ] Integration tests passing
- [ ] Benchmarking report (before/after)
- [ ] Demo ready (walkthrough of all 3 features)
- [ ] Release notes drafted

## 📊 Success Metrics (Target)

| Metric | Current | Target | Owner |
|--------|---------|--------|-------|
| Token usage per session | 100% | 30-40% | Memory team |
| Memory search latency | 500ms | <300ms | Memory team |
| Sub-agent clarity | ~70% | ~85% | Auto-dispatch |
| System observability | Low | High | Hook owner |
| Time to PHase 2 | - | Ready | All |

## 🚀 Execution Strategy

### Daily Standup (async in session memory)
- [ ] Completed work
- [ ] Blockers
- [ ] Next 24h plan

### Code Review Process
- [ ] Pair review (at least 1 other person)
- [ ] Test coverage check (>90%)
- [ ] Performance benchmark (if applicable)
- [ ] Documentation review

### Testing Strategy
- [ ] Unit tests (fast, isolated)
- [ ] Integration tests (hooks + memory + dispatch)
- [ ] Benchmark tests (latency + token savings)
- [ ] End-to-end tests (user workflow)

## 🔍 Risk Management

| Risk | Prob | Impact | Mitigation |
|------|------|--------|-----------|
| Hooks too slow | Low | Medium | Profile early; async fallback |
| Memory compression loses data | Medium | High | Run on real data; human review |
| Intent classifier over-confident | Medium | Low | Force menu if <0.7 confidence |
| Integration complexity | Medium | Medium | Separate branches; frequent merges |

## 📋 Definition of Done

A work item is "done" when:
1. ✅ Code written + tested (>90% coverage)
2. ✅ Integration tests passing
3. ✅ Performance benchmarks met
4. ✅ Documentation complete (API + examples)
5. ✅ Code reviewed + approved (2 reviewers)
6. ✅ Merged to main
7. ✅ Demo recorded (optional)

## 🎓 Learning & Feedback Loops

### Post-WI Reviews (after each WI)
- What went well?
- What was harder than expected?
- Any improvements to approach?

### Phase 1 Retrospective (end of week 2)
- Overall pace (on time? over?)
- Architecture decisions (correct?)
- Team morale (sustainable?)
- Recommendations for Phase 2

## 🚢 Deployment Strategy

**Phase 1** is **NOT customer-facing** by default:
- [ ] Feature flags off (`hooks_enabled: false`, `progressive_memory: false`, `auto_dispatch: false`)
- [ ] Internal testing only
- [ ] Performance baseline established
- [ ] Phase 2 decision: Enable for real?

## 📞 Contacts & Escalation

| Role | Name | Escalation Path |
|------|------|-----------------|
| WI-1 Owner | [Core team lead] | → Guilhem → BMad Master |
| WI-2 Owner | [Memory team lead] | → Guilhem → BMad Master |
| WI-3 Owner | [SOG team lead] | → Guilhem → BMad Master |
| QA | [QA lead] | → All owners |
| Docs | [Tech writer] | → All owners |

## 📚 References

- **ADR-005**: Lifecycle Hooks System
- **ADR-006**: Progressive Disclosure
- **RESEARCH Report**: Full analysis of 7 frameworks
- **claude-mem**: Reference implementation
- **gstack**: Failure capture pattern
- **superpowers**: Intent-based dispatch

---

## 🎯 Next Step After Phase 1

Once Phase 1 is complete + validated:
- [ ] **Phase 2 kickoff** → Operational Learning Pipeline + SKILL.md auto-generation
- [ ] **Phase 3 planning** → Multi-platform adapters + Marketplace

---

**Created**: 2026-04-02  
**Status**: Ready for Sprint Planning  
**Version**: 1.0
