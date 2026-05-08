---
title: "ADR-006: Progressive Disclosure Memory Architecture (3-Layer Search)"
date: 2026-04-02
status: "PROPOSED"
deciders: ["Guilhem", "BMad Master"]
consulted: []
informed: ["All agents"]
---

# ADR-006: Progressive Disclosure Memory Architecture (3-Layer Search)

## Context

Grimoire's current memory system **dumps full context** when agents request memory recall. This leads to:

1. **Token waste** — Full data when only summary needed (~70% waste)
2. **Cognitive overload** — Agents distracted by irrelevant detail
3. **Hallucination** — Too much signal = more noise = more drift
4. **Latency** — Embedding + search on full data = slow (~500ms)

### Observations from claude-mem analysis

claude-mem demonstrates a **3-layer disclosure model**:

```
Layer 1 (SEARCH): 50 tokens max
├─ Show titles + dates + brief summary
├─ User scans for relevance
├─ 95% use case resolved here
└─ Time: <100ms

Layer 2 (TIMELINE): 200 tokens
├─ Add timestamps, categories
├─ Show progression/sequence
├─ 4% of cases go deeper
└─ Time: 100-200ms

Layer 3 (FETCH): 500+ tokens
├─ Full context, code samples, details
├─ Research/deep-dive mode
├─ <1% of cases need this
└─ Time: 200-500ms
```

**Real-world impact**: With aggressive compression, typical session saves **~1440 tokens** per recall (vs. 160 tokens with full context).

### Current State (Grimoire)

```
Memory Query → Full Embedding Search → Return 2000-3000 tokens
```

### Desired State

```
Memory Query
  ├─ Layer 1: SEARCH (50 tokens) ✅ [Most queries stop here]
  │   └─ User: "More details?"
  │       └─ Layer 2: TIMELINE (200 tokens) ✅ [Most deeper queries stop here]
  │           └─ User: "Full context?"
  │               └─ Layer 3: FETCH (500+ tokens) ✅ [Only deep-dive]
```

## Decision

**Implement 3-Layer Progressive Disclosure** in MemoryManager:

1. **Layer 1 (SEARCH)**: Minimum viable context (50 tokens)
2. **Layer 2 (TIMELINE)**: Extended with history/sequence (200 tokens)
3. **Layer 3 (FETCH)**: Full context (500+ tokens)

Each layer requires **explicit user/agent request** to proceed (no auto-escalation).

### Design Architecture

```python
class ProgressiveMemory:
    """3-layer memory disclosure system"""
    
    def __init__(self, memory_backend, compression_ratio=0.1):
        self.backend = memory_backend
        self.compression = compression_ratio  # Compress to 10% of original
        self.search_limit = 50     # Layer 1: max tokens
        self.timeline_limit = 200  # Layer 2: max tokens
        self.fetch_limit = 500     # Layer 3: max tokens
    
    async def search(
        self,
        query: str,
        layer: Literal["L1", "L2", "L3"] = "L1",
        limit: Optional[int] = None
    ) -> SearchResult:
        """
        Retrieve memory at specified disclosure layer.
        
        Args:
            query: Natural language search
            layer: "L1" (50 tokens) | "L2" (200) | "L3" (500+)
            limit: Override token limit if needed
        
        Returns:
            {
                "layer": str,
                "query": str,
                "results": [MemoryItem],
                "tokens_used": int,
                "truncated": bool,
                "next_layer_available": bool
            }
        """
        token_limit = {
            "L1": limit or self.search_limit,
            "L2": limit or self.timeline_limit,
            "L3": limit or self.fetch_limit,
        }[layer]
        
        # Hybrid search (keyword + vector)
        results = await self._hybrid_search(
            query=query,
            layer=layer,
            token_limit=token_limit
        )
        
        return SearchResult(
            layer=layer,
            results=results,
            tokens_used=self._estimate_tokens(results),
            truncated=len(results) >= token_limit,
            next_layer_available=(layer != "L3"),
            next_layer_suggestion=self._suggest_next_layer(results)
        )
    
    async def _hybrid_search(
        self,
        query: str,
        layer: str,
        token_limit: int
    ) -> List[MemoryItem]:
        """
        Parallel hybrid search: keyword + vector similarity
        """
        # Branch 1: Full-text search (catch exact matches)
        fts_results = await self.backend.full_text_search(
            query=query,
            limit=10
        )
        
        # Branch 2: Vector search (catch semantic similarity)
        vector_results = await self.backend.vector_search(
            query=query,
            limit=10
        )
        
        # Merge & deduplicate (prefer keyword matches)
        merged = self._merge_results(fts_results, vector_results)
        
        # Format per layer
        formatted = self._format_by_layer(
            merged,
            layer=layer,
            token_limit=token_limit
        )
        
        return formatted
    
    def _format_by_layer(
        self,
        items: List[MemoryItem],
        layer: str,
        token_limit: int
    ) -> List[MemoryItem]:
        """Format memory items for specific layer"""
        
        if layer == "L1":
            # MINIMAL: Title + date + 1-line summary
            return [
                {
                    "id": item.id,
                    "title": item.title,
                    "date": item.date,
                    "summary": self._compress(item.content, 20),  # 1 line
                    "relevance_score": item.rank
                }
                for item in items
            ][:self._count_to_token_limit(token_limit)]
        
        elif layer == "L2":
            # EXTENDED: Title + date + summary + category + sequence
            return [
                {
                    "id": item.id,
                    "title": item.title,
                    "date": item.date,
                    "summary": self._compress(item.content, 50),  # 2-3 lines
                    "category": item.category,
                    "sequence": getattr(item, "sequence", None),
                    "tags": item.tags[:3],
                    "relevance_score": item.rank
                }
                for item in items
            ][:self._count_to_token_limit(token_limit)]
        
        elif layer == "L3":
            # FULL: Everything (no compression)
            return [
                {
                    "id": item.id,
                    "title": item.title,
                    "date": item.date,
                    "content": item.content,  # Full
                    "category": item.category,
                    "tags": item.tags,
                    "context": item.full_context,
                    "related": item.related_items[:3],
                    "relevance_score": item.rank
                }
                for item in items
            ][:self._count_to_token_limit(token_limit)]
```

### Layer Specifications

#### **Layer 1 (SEARCH)** — 50 tokens
Minimal viable context for quick scans.

```
[
    {
        "id": "mem_123",
        "title": "Q3 2025 Architecture Review",
        "date": "2025-10-15",
        "summary": "Decided to migrate from monolith to microservices",
        "relevance": 0.95
    },
    {
        "id": "mem_456",
        "title": "Performance Audit Results",
        "date": "2025-10-10",
        "summary": "API latency increased 200ms, traced to N+1 queries",
        "relevance": 0.87
    }
]
```

**Use case**: "What have we decided recently?" → Done in 50 tokens.

#### **Layer 2 (TIMELINE)** — 200 tokens
Adds sequence, category, tags — useful for understanding progression.

```
[
    {
        "id": "mem_123",
        "title": "Q3 2025 Architecture Review",
        "date": "2025-10-15",
        "summary": "Decided to migrate from monolith to microservices. Key drivers: Scale, maintainability, deployment frequency",
        "category": "architecture",
        "sequence": 5,
        "tags": ["architecture", "migration", "scaling"],
        "relevance": 0.95
    },
    {
        "id": "mem_124",
        "title": "Microservices Decomposition Plan",
        "date": "2025-10-14",
        "summary": "Created 6-phase rollout starting with payments service",
        "category": "planning",
        "sequence": 4,
        "tags": ["microservices", "planning", "payments"],
        "relevance": 0.91
    }
]
```

**Use case**: "What's the sequence of decisions?" → Now clear in 200 tokens.

#### **Layer 3 (FETCH)** — 500+ tokens
Full context with related items, code samples, decisions.

```
[
    {
        "id": "mem_123",
        "title": "Q3 2025 Architecture Review",
        "date": "2025-10-15",
        "content": "[Full meeting notes, 400 tokens...]",
        "category": "architecture",
        "tags": ["architecture", "migration", "scaling"],
        "related": [
            {"id": "mem_124", "title": "Microservices Decomposition Plan"},
            {"id": "mem_50", "title": "Performance Analysis Q2 2025"}
        ],
        "decision": "APPROVED: Proceed with microservices migration",
        "owner": "architect@team"
    }
]
```

**Use case**: "I need full context on this decision" → All details in 500 tokens.

### Compression Strategy

**Key insight from claude-mem**: Aggressive compression works because humans are **good at reconstruction**.

```python
def compress(text: str, target_words: int) -> str:
    """
    Compress text to target word count while preserving facts.
    
    Strategy:
    1. Extract noun phrases (key entities)
    2. Identify action verbs (what happened)
    3. Find numbers/metrics (quantitative impact)
    4. Reconstruct in ~target_words
    """
    
    # Example
    input = """
    In our Q3 review, we analyzed the monolithic architecture's limitations.
    The system is increasingly difficult to scale. Database queries have become 
    complex with N+1 problems. The team is splitting. Deployment cycles are 
    getting slower.
    """
    
    # Output (compress to 20 words)
    output = "Monolithic system hard to scale: N+1 DB queries, slow deploys, team bottleneck"
    
    # Output (compress to 50 words)
    output = """
    Monolithic architecture showing 3 problems:
    1. Scale limitations (N+1 DB queries)
    2. Slow deployment cycles (hours → days)
    3. Team split (services loosely coupled)
    Decision: Migrate to microservices in Q4.
    """
```

### Integration with SOG

```python
# In BMad Master (SOG)
class BMadMaster:
    async def answer_with_memory(self, query: str):
        """
        Answer a question by retrieving relevant memory.
        Uses layer-by-layer disclosure.
        """
        
        # Layer 1: Initial search
        results_l1 = await self.memory.search(
            query=query,
            layer="L1"
        )
        
        agent_context = f"""
        Query: {query}
        
        Memory results (Layer 1 - Summary):
        {format_results(results_l1.results)}
        
        [If you need more detail, ask for Layer 2 or Layer 3]
        """
        
        # Ask agent if more detail needed
        agent_response = await self.agent.run(agent_context)
        
        # If agent requests deeper layer
        if agent_response.requests_layer == "L2":
            results_l2 = await self.memory.search(
                query=query,
                layer="L2"
            )
            # Merge L1 + L2
            enhanced_context = merge_layers(results_l1, results_l2)
            agent_response = await self.agent.run(enhanced_context)
        
        return agent_response
```

### Benefits

1. ✅ **~70% token savings** — 1600 tokens → 160 tokens typical
2. ✅ **Better UX** — Agents get relevant context, not noise
3. ✅ **Faster search** — Layer 1 excludes large items upfront
4. ✅ **Control** — Users/agents decide when to go deeper
5. ✅ **Learning** — Track which layers are used → optimize compression

### Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Agents ask for L3 too often (defeats savings) | Medium | Monitor usage; adjust compression if needed |
| Compression loses important details | Medium | Preserve facts explicitly; test comprehension |
| Hybrid search misses relevant items | Low | Full-text + vector catches edge cases |
| Layer 2 timestamp logic complex | Low | Simple date-based ordering initially |

### Acceptance Criteria

- [ ] ProgressiveMemory class fully implemented
- [ ] Layer 1, 2, 3 formatting working correctly
- [ ] Hybrid search (FTS + vector) working
- [ ] Token estimation accurate (within 5%)
- [ ] Compression ratio achieves 70%+ savings on real data
- [ ] Integration with SOG complete
- [ ] Tests covering all layers + edge cases
- [ ] Documentation + usage examples
- [ ] Benchmark report (before/after token usage)

### Implementation Effort

- **Estimated**: 4-6 days
- **Complexity**: Medium
- **Owner**: Memory team
- **Blocked by**: None

### References

- claude-mem: Progressive disclosure pattern
- compression research: Fact preservation techniques
- BMAD: Existing memory system
