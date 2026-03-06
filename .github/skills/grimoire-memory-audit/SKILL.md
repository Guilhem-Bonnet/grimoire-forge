---
name: grimoire-memory-audit
description: 'Deep audit of BMAD Grimoire memory system. Use when: memory audit, check memory, memory issues, stale memories, memory cleanup, memory health, contradictions in memory, duplicate learnings, memory freshness, session chain review. Combines memory-lint, freshness scoring, and session chain analysis.'
---

# Grimoire Memory Audit

Deep audit of the BMAD memory subsystem: coherence, freshness, contradictions, and session continuity.

## When to Use

- Memory feels inconsistent or outdated
- Before archiving or pruning memory files
- After a long period without maintenance
- When the user asks about "memory health", "stale entries", or "contradictions"
- Periodic memory hygiene review

## Procedure

### Step 1 — Memory Lint (Coherence)

```bash
python3 framework/tools/memory-lint.py --project-root .
```

Checks:
- **Contradictions** between learnings and decisions
- **Duplicates** across memory files  
- **Orphan decisions** not traced to any artifact
- **Failures without lessons** in the failure museum
- **Chronological consistency** of dated entries
- **Freshness/staleness** scoring (decay halflife = 30 days)

### Step 2 — Session Chain Review

Read the session chain file to understand recent session continuity:

```bash
cat _bmad/_memory/session-chain.jsonl 2>/dev/null | python3 -m json.tool --no-ensure-ascii 2>/dev/null | tail -100
```

If the file exists, analyze:
- Number of sessions recorded
- Time gaps between sessions
- Consistency of context passing
- Any sessions that ended without proper closure

### Step 3 — Memory File Inventory

```bash
find _bmad/_memory/ -type f -name "*.md" -o -name "*.json" -o -name "*.jsonl" | sort
```

List all memory files with their last modification dates:

```bash
find _bmad/_memory/ -type f \( -name "*.md" -o -name "*.json" \) -exec ls -la --time-style=long-iso {} \;
```

### Step 4 — Memory Bridge Status

Check if the bridge sync is up to date:

```bash
diff -rq _bmad/_memory/ .github/memories/repo/ 2>/dev/null || echo "Bridge not synced or target missing"
```

### Step 5 — Aggregate Report

```
## 🧠 Memory Audit Report

### Coherence
| Check              | Result | Count |
|--------------------|--------|-------|
| Contradictions     | ✅/⚠️  | N     |
| Duplicates         | ✅/⚠️  | N     |
| Orphan decisions   | ✅/⚠️  | N     |
| Missing lessons    | ✅/⚠️  | N     |
| Chronological      | ✅/⚠️  | N     |
| Staleness          | ✅/⚠️  | N     |

### Freshness
- Total entries: N
- Fresh (< 30 days): N
- Aging (30-90 days): N  
- Stale (> 90 days): N → candidates for archival

### Session Chain
- Sessions recorded: N
- Last session: YYYY-MM-DD
- Average gap: N days

### Recommendations
- Archive entries older than 90 days
- Resolve contradictions before they propagate
- ...
```

## Memory Structure Reference

```
_bmad/_memory/
├── agent-learnings/     # Per-agent learnings (dated entries)
│   ├── dev.md
│   ├── architect.md
│   └── ...
├── decisions-log.md     # Architectural decisions
├── failure-museum.md    # Catalogued failures + lessons
├── shared-context.md    # Cross-agent shared knowledge
├── contradiction-log.md # Known contradictions
├── session-chain.jsonl  # Session continuity chain (QW1)
└── daemon/              # Daemon state files
```
