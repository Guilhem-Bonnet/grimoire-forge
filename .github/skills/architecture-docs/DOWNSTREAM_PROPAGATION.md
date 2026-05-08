# Downstream Documentation Propagation (Step 5.5)

Companion to `architecture-docs/SKILL.md` — full procedure for the Step 5.5 propagation workflow that runs after the Post-Write Alignment Audit.

Runs immediately after the Post-Write Alignment Audit passes. Detects downstream files whose content may be stale due to the edit and offers to update them.

## Trigger Gate

**Run when**: The edit changed substantive content — metrics, technology names, component names, architectural patterns, constraints, requirements, or interface definitions.

**Skip silently when**: The edit was cosmetic — typo fixes, formatting, grammar, markdown structure, comment updates, `<!-- TODO -->` markers, or source attribution links. Heuristic: if the diff contains only whitespace/punctuation/link/formatting changes with no word-level changes to technical terms, skip entirely.

**Anti-recursion rule**: Propagation updates (Phase 3 edits) do NOT re-trigger Step 5.5.

## Reverse Dependency Table

| Edited Section | File | Downstream Section Files |
| --- | --- | --- |
| S1+S2 (System Overview) | `docs/01-system-overview.md` | ALL sections (S4–S11) + `docs/components/*` |
| S3 (Principles) | `docs/02-architecture-principles.md` | ALL sections (S4–S11) + `docs/components/*` |
| S4 (Layers) | `docs/03-architecture-layers.md` | S5 (`docs/components/*`), S8 (`docs/06-technology-stack.md`) |
| S5 (Components) | `docs/components/*.md` | S6 (`docs/04-data-flow-patterns.md`), S7 (`docs/05-integration-points.md`), S8 (`docs/06-technology-stack.md`), S9 (`docs/07-security-architecture.md`), S10 (`docs/08-scalability-and-performance.md`), S11 (`docs/09-operational-considerations.md`), Refs (`docs/10-references.md`), **+ S3 semantic re-check** (Phase 1.5 — invoke `principle-quality-reviewer` in `mode: downstream-impact` with `downstream_file = docs/02-architecture-principles.md`; flag any principle whose Implementation/Trade-offs the new component contradicts) |
| S6 (Data Flow) | `docs/04-data-flow-patterns.md` | *(leaf — no downstream sections)* |
| S7 (Integration) | `docs/05-integration-points.md` | S9 (`docs/07-security-architecture.md`) |
| S8 (Tech Stack) | `docs/06-technology-stack.md` | S9 (`docs/07-security-architecture.md`), S10 (`docs/08-scalability-and-performance.md`), S11 (`docs/09-operational-considerations.md`), Refs (`docs/10-references.md`) |
| S9 (Security) | `docs/07-security-architecture.md` | *(leaf)* |
| S10 (Scalability) | `docs/08-scalability-and-performance.md` | S11 (`docs/09-operational-considerations.md`) |
| S11 (Operations) | `docs/09-operational-considerations.md` | *(leaf)* |
| S12 (ADRs) | `ARCHITECTURE.md` (navigation table) | `adr/` directory → delegate to `/skill architecture-definition-record`, Refs (`docs/10-references.md`) |

**Cross-cutting** (always scanned regardless of table): `docs/components/`, `handoffs/`, `docs/10-references.md`

### References file (`docs/10-references.md`) propagation

`docs/10-references.md` is a cross-cutting file that aggregates links from multiple sections. It MUST be included in the downstream scan when **any** of these change:

| Change Type | What to update in `10-references.md` |
| --- | --- |
| ADR added, removed, renamed, or status changed (`adr/*.md`) | ADR index table — add/remove/rename row, update status |
| New technology in S5 components or S8 tech stack | Technology documentation links — add official doc URL |
| Technology removed or replaced | Technology documentation links — remove or replace entry |
| New glossary-worthy term introduced in any section | Glossary — add definition |

When `10-references.md` is flagged for update during Phase 2 (Generate Checklist), present specific sub-items showing which table(s) need updating (ADR index, technology links, glossary).

## S12 ADR Table Propagation (Special Rule)

When the edited file is `ARCHITECTURE.md` **and** the edit added or modified rows in the Section 12 ADR table:

1. **Detect new ADR rows**: Compare the ADR table before and after the edit. Extract any new rows matching `| [ADR-NNN](...) | ... |`
2. **Check for existing files**: For each new ADR row, check if `adr/ADR-NNN-slug.md` already exists
3. **Delegate creation**: For ADR rows where the file does NOT exist, invoke `/skill architecture-definition-record` with context:
   - Trigger reason: "Section 12 ADR table updated — generate ADR files for new entries"
   - Pass the ADR metadata (number, title, status, date, impact) from the table row
   - The architecture-definition-record skill runs Workflow 1 Steps 1.3–1.5 (extract → load template → generate)
4. **Skip if file exists**: If the ADR file already exists, do not overwrite — report: `adr/ADR-NNN-slug.md already exists — skipped`

After ADR file creation (or skip), **always update `docs/10-references.md`**:

- Add new ADRs to the ADR index table
- Update ADR titles or status if changed
- Remove entries for deleted ADRs

This rule runs **instead of** the standard Phase 1–3 propagation for S12 changes. ADR table changes do not trigger downstream section updates — they trigger ADR file creation and references update.

## Phase 1: Impact Discovery

**1a. Fact-delta extraction** — Compare the file content before and after the edit. Produce a concrete bullet list of what changed (e.g., "Database: PostgreSQL → CockroachDB", "Added: Redis caching layer", "Removed: legacy SOAP endpoint"). If zero substantive deltas → skip propagation entirely.

**1b. Structural dependency scan** — Look up the edited section in the reverse dependency table above. Collect all downstream section files.

**1c. Cross-reference scan** — Grep across `docs/`, `docs/components/`, `handoffs/` for explicit references to the edited filename (links, section anchors, `(see [...](...))`).

```bash
grep -rl "{edited_filename}" docs/ docs/components/ handoffs/ 2>/dev/null
```

**1d. Handoff scan** — For each fact-delta keyword (component names, technology names, pattern names), grep `handoffs/` for matching terms.

**1e. Merge and deduplicate** — Combine results from 1b+1c+1d. Remove duplicates and remove the edited file itself.

## Phase 1.5: Principle Alignment Audit (S3 edits only)

Runs **only** when the edited file is `docs/02-architecture-principles.md` AND Phase 1a's fact-delta extraction reported substantive word-level changes in any of {Description, Implementation, Trade-offs} subsections.

**Trigger gate** — skip Phase 1.5 silently when:

- The diff contains only whitespace, punctuation, link reformatting, or markdown structure changes (no word-level changes inside D/I/T blocks).
- The Section 3 Enforcement Gate above failed and the principles file was regenerated wholesale (the regenerated file is treated as a first-write, not an edit, and the orchestrator already re-ran the gate).
- Phase 1a's diff is empty (no substantive changes detected).

**Audit procedure** when the gate fires:

1. **Extract per-principle deltas** from the diff. For each principle that changed, capture:
   - `principleNumber`, `principleName`
   - Which subsection(s) changed (Description / Implementation / Trade-offs)
   - A 1-line summary of the change (what was added, removed, or rephrased)
   - **Token set for pruning** — derived from the *raw* added/removed lines of the changed subsections (not from the 1-line summary). Build a single de-duplicated set containing:
     - **Principle names** — the `principleName` of every changed principle.
     - **ADR IDs** — every `ADR-NNN` token (regex `ADR-\d{3}`) that appears in either the before-text or the after-text of changed Description / Implementation / Trade-offs subsections.
     - **Affected tech tokens** — every named tech term that appears on an added or removed diff line AND is enumerated in `docs/06-technology-stack.md` (i.e., a tech this system actually uses). Intersecting with the tech stack avoids matching English words that happen to be tech-name-shaped. Compare case-insensitive on whole-token boundaries.

   This token set powers the pruning step below; if the set ends up empty (e.g., the diff only rephrased Description prose with no concrete principle names, ADR IDs, or system-tech tokens) the fall-back is conservative — fan out to all candidates without pruning.

2. **Pre-fan-out pruning** — Token-grep each candidate downstream file against the token set from step 1 to drop files with zero references to anything that changed. The reviewer is Opus and the median S3 edit touches one principle's Implementation, so most downstream files don't even mention the changed content. Skipping them on the basis of a cheap structural grep avoids spending Opus on guaranteed `NO_IMPACT` verdicts.

   **Candidate set** = the reverse dependency files for S3 (S4–S11 + every `docs/components/**/*.md` listed in `docs/components/README.md`).

   **Pruning rule (per candidate file):**
   - If the token set from step 1 is empty → KEEP the file (conservative: nothing concrete to grep against; fall through to fan-out).
   - Else, run a single composite case-insensitive grep over the file using a regex alternation of every token in the set (escape regex metacharacters in principle names; whole-line match is fine — we only need a hit/no-hit signal). Examples:

     ```bash
     grep -liE 'Principle Name 1|Principle Name 4|ADR-005|ADR-012|Spring Boot|PostgreSQL|Redis' \
       docs/03-architecture-layers.md docs/04-data-flow-patterns.md \
       docs/05-integration-points.md docs/06-technology-stack.md \
       docs/07-security-architecture.md docs/08-scalability-and-performance.md \
       docs/09-operational-considerations.md docs/components/*.md
     ```

   - File path emitted by grep → KEEP for the fan-out in step 3.
   - File NOT emitted → SKIP. Record one Phase 2 note for the user:

     ```text
     ℹ️  {file} — no token references to changed principles, cited ADRs, or affected tech; semantic review skipped (Phase 1.5 pruning).
     ```

   **Empty kept-set after pruning** — when zero candidate files token-match (and the token set was non-empty, so the prune was real), emit one consolidated Phase 2 note ("Principle Alignment Audit: no downstream files reference any of the changed principles, cited ADRs, or affected tech — nothing to review.") and skip steps 3–6 of this Audit procedure. Phase 2 still runs with the structural impact list from Phase 1b–1d.

   **Fail-open** — if `grep` is unavailable or returns an unexpected error, emit a one-line Phase 2 warning ("Phase 1.5 pruning unavailable; fanned out to the full candidate set") and fall through to step 3 with all candidates kept. Pruning is an optimization, not a gate.

   **Why this is recall-safe** — the token set includes principle names AND cited ADR IDs AND affected tech, all three. Most "implicit contradiction" cases (a downstream file paraphrases a principle without naming it) still surface because the file usually mentions either the cited ADR or the affected tech. The conservative empty-set fallback covers the long tail (pure prose changes with no concrete tokens).

3. **Fan out to `principle-quality-reviewer`** in `mode: downstream-impact`. The orchestrator MUST construct the sub-agent prompt using the **stable-prefix → dynamic-suffix template** below so parallel calls in the same batch share the maximum cacheable prefix (Anthropic prompt cache hits on byte-identical prefixes within the 5-min TTL).

   **Read-once foundational context.** Before dispatching any sub-agent in this fan-out, read the four foundational files **once** in the orchestrator's session and capture their content. The five blocks below are byte-identical across every sub-agent call in the fan-out, so inlining them lets calls 2..N hit the prompt cache for the entire prefix instead of each agent re-Reading the same files independently:

   - `docs/02-architecture-principles.md` (post-edit) → `<principles>` block
   - `docs/01-system-overview.md` → `<system_overview>` block
   - `docs/03-architecture-layers.md` → `<arch_layers>` block
   - `docs/06-technology-stack.md` → `<tech_stack>` block
   - `Glob('adr/*.md')` ID list (one `ADR-NNN` per line, sorted) → `<adr_index>` block (the IDs alone — bodies are not needed for existence checks)

   **Prompt template** — positional, order must not change. Lines above the marker are stable across the batch; only `downstream_file` (last line) differs per call:

   ```text
   mode: downstream-impact
   round: <int>
   arch_type: <MICROSERVICES|META|BIAN|3-TIER|N-LAYER|unknown>
   principles_file: docs/02-architecture-principles.md
   principles_diff: |
     <per-principle deltas from step 1, identical for every call in this batch>

   <principles>
   {full content of docs/02-architecture-principles.md (post-edit)}
   </principles>

   <system_overview>
   {full content of docs/01-system-overview.md}
   </system_overview>

   <arch_layers>
   {full content of docs/03-architecture-layers.md}
   </arch_layers>

   <tech_stack>
   {full content of docs/06-technology-stack.md}
   </tech_stack>

   <adr_index>
   {one ADR-NNN id per line, sorted}
   </adr_index>

   # === Stable prefix ends here. Only the line below differs per call. ===

   downstream_file: {absolute path to the specific downstream file under audit}
   ```

   The agent's Step 1 consumes the five inlined blocks directly — it does NOT re-Read the four foundational files when the blocks are present. See `agents/reviewers/principle-quality-reviewer.md` Step 1 (Inlined-blocks fast path) for the consumption contract.

   **Why the order matters**: Anthropic's prompt cache is a prefix matcher. Any per-call discriminator above the marker would split the cache and force every parallel call to be a cache miss. Keep `downstream_file` as the LAST line; keep `principles_diff` and the five inlined blocks above it; keep them in the order shown so all calls in the batch share a byte-identical prefix.

   **Backward compatibility**: when running the reviewer outside this orchestrator (e.g., direct invocation, older callers), the agent still accepts path-only inputs and falls back to `Read` / `Glob`. The path parameters (`system_overview_file`, `arch_layers_file`, `tech_stack_file`, `adr_index_glob`) remain in the prompt as fallback values; they are ignored when the inlined blocks are present.

   **Parallelism**: dispatch in batches of 4 (mirrors v3.16.0 explorer fan-out pattern). Wait for each batch before starting the next.

   **Cache-warm sequencing (first batch only)**: in the FIRST batch of any Phase 1.5 fan-out, fire **one** sub-agent call first and wait for its response to settle before firing the remaining 1–3 calls in parallel. The first call's response writes the byte-identical stable prefix (the five inlined blocks above) into Anthropic's prompt cache; the remaining calls in that batch — and every call in every subsequent batch within the 5-min cache TTL — read the prefix from cache instead of re-paying it. After the first batch completes, dispatch subsequent batches normally (full parallel of 4); the cache is already warm.

   The latency cost is one extra serialized call (~30–60s) paid only on the first batch of each Phase 1.5 fan-out. For typical S3 edits where step 2 pruning leaves 2–4 candidate files, this adds < 1 minute of wall-clock time. For wider fan-outs (8+ files post-pruning) the savings compound across batches because each non-first batch hits cache for the full prefix instead of re-writing it.

4. **Aggregate results** — each sub-agent returns one of:
   - `status: PASS` with `findings: []` and a finding `checkType: downstream-impact, severity: NO_IMPACT` → file unaffected; no action.
   - `status: PASS` with `WARNING` findings → surface in Phase 2 checklist as `[principle-impact]` items but don't block.
   - `status: FAIL` with `BLOCKING` findings → file contradicts a changed principle; surface in Phase 2 checklist as `[principle-impact-BLOCKING]` items requiring user review.

5. **Fail-open clauses**:
   - Sub-agent timeout / empty / error on any single file: skip that file with a Phase 2 warning ("`{file}` — principle alignment review unavailable; manual review required"). Do not block.
   - All sub-agents fail (e.g., system-wide tool outage): emit one warning at the top of Phase 2 ("Principle Alignment Audit unavailable; downstream files not semantically re-checked. Run `/skill architecture-peer-review` after edits land if reliability matters for this change.") and proceed to standard Phase 2 with structural impacts only.

6. **Inject findings into Phase 2 checklist** — semantic findings appear as a dedicated subsection labeled "Principle Alignment Findings" between the structural impact list and the "Approve all?" prompt. Pruning notes from step 2 (skipped files) appear in the same subsection under a "Skipped (no token references)" sub-heading so the user retains visibility into what was deliberately not reviewed. User can approve / deselect / skip per file (same UX as structural impacts).

**Anti-recursion**: Phase 1.5 sub-agent calls do NOT trigger another Phase 1.5 invocation when their findings translate into Phase 3 edits.

## Phase 2: Generate Checklist

Present a structured checklist grouped by file type:

```text
═══════════════════════════════════════════════════════════
DOWNSTREAM UPDATES REQUIRED — {edited_file} ({section_name})
═══════════════════════════════════════════════════════════

Changes detected:
- {bullet list from Phase 1a}

─── Downstream Sections ──────────────────────────────────
[ ] 1. docs/07-security-architecture.md — references {changed_tech}; security controls may need updating
[ ] 2. docs/09-operational-considerations.md — mentions {old_value}; align with new value

─── Component Files ──────────────────────────────────────
[ ] 3. docs/components/03-payment-service.md — uses {changed_component}; integration details may be stale

─── Handoff Docs ─────────────────────────────────────────
[ ] 4. handoffs/03-payment-service-handoff.md — Section 4 references {old_tech}

─── No Updates Required ──────────────────────────────────
ℹ️  docs/04-data-flow-patterns.md — no references to changed content
═══════════════════════════════════════════════════════════
Approve all? ('all', comma-separated numbers to deselect, or 'skip')
```

Wait for user response before proceeding.

## Phase 3: Execute Updates

Process approved files **in tier order** (lower tiers first → higher tiers last) so each updated file is available as context for files that depend on it.

For each approved `docs/*.md` or `docs/components/*.md` file:

1. Load Context Anchor (universal foundation + section-specific parents per the dependency table)
2. Read the target file in full
3. Identify passages affected by the fact-deltas
4. Apply updates, maintaining Source Attribution links (`per [Section X](../...)`)
5. Run the 5-check Post-Write Alignment Audit on the updated file
6. Mark as `[x]`

For approved `handoffs/*.md` files: Read, locate affected passages, update following the dev-handoff Documentation Fidelity Policy. Mark as `[x]`.

If user selected `skip`: Add `<!-- PROPAGATION PENDING: upstream {edited_file} changed ({date}) — downstream not yet updated -->` comment at the top of the edited file.

### Component File Edit Handling

When the edited file is `docs/components/*.md` (not a section file):

- Cascade through S5's row in the table (S6, S7, S8, S9, S10, S11)
- Additionally grep for the **component name** (not just filename) across all `docs/` files
- Always include the matching `handoffs/{component}-handoff.md` if it exists
- If `docs/components/README.md` needs updating, delegate to the `architecture-component-guardian` skill

## Phase 4: Propagation Report

```text
═══════════════════════════════════════════════════════════
DOWNSTREAM PROPAGATION — COMPLETION REPORT
═══════════════════════════════════════════════════════════

Source: {edited_file} ({section_name})
Changes: {summary from Phase 1a}

Completed:
[x] docs/07-security-architecture.md — {what was updated}
[x] docs/components/03-payment-service.md — {what was updated}

Verified (no change needed):
✓  docs/08-scalability-and-performance.md — content still accurate

Deselected (manual update required):
[ ] docs/09-operational-considerations.md — user chose manual update

Failed (require manual review):
⚠️  {any files where edit could not be applied cleanly}
═══════════════════════════════════════════════════════════
```

## Phase 5: Asset Regeneration Advisory

**Runs after**: Phase 4 report is displayed.
**Also runs when**: User selected `skip` in Phase 2 and handoff files exist in `handoffs/` — in this case, note that handoff text was also not updated.

**Skip silently when**: No `handoffs/*.md` files appeared in the Phase 3 update list (completed, deselected, or failed) AND propagation was not skipped.

**Step 5a — Detect asset-impacting changes**: Scan the fact-deltas from Phase 1a for asset-impact keywords (case-insensitive):

| Keywords | Potentially Stale Asset |
| ---------- | ------------------------ |
| API, endpoint, REST, GraphQL, gRPC, route, path, method, request, response, header, status code | `openapi.yaml` |
| database, table, column, schema, index, constraint, migration, DDL, SQL | `ddl.sql` |
| Redis, cache, key, TTL, expiration, eviction | `redis-key-schema.md` |
| deployment, container, pod, replica, port, resource, limit, CPU, memory, image, Kubernetes, K8s | `deployment.yaml` |
| message, event, topic, queue, consumer, producer, Kafka, RabbitMQ, stream | `asyncapi.yaml` |
| Avro, schema registry | `schema.avsc` |
| Protobuf, proto | `schema.proto` |
| cron, schedule, batch, job, CronJob | `cronjob.yaml` |

If no keywords match → skip this phase silently.

**Step 5b — Identify affected components**: For each `handoffs/*-handoff.md` file that was touched in Phase 3 (or would have been if propagation was skipped/deselected), check whether `handoffs/assets/NN-<component-name>/` exists and contains any of the matched asset types. Exclude components with no asset directory or no matching asset files on disk.

If zero components remain after filtering → skip silently.

**Step 5c — Present advisory**:

```text
───────────────────────────────────────────────────────────
ASSET REGENERATION ADVISORY
───────────────────────────────────────────────────────────

The propagation above updated handoff document text, but
the following scaffolded assets may now be stale:

  Component: {component-name}
    → openapi.yaml  (changes mention: endpoint, API)
    → ddl.sql       (changes mention: table, column)

  Component: {component-name-2}
    → deployment.yaml  (changes mention: container, port)

These assets were generated by the dev-handoff skill and
contain structured specs derived from architecture docs.
In-place text patches do not regenerate them.

Would you like to regenerate handoff documents and assets
for the affected components?

  [Yes] → I will provide the commands to run
  [No]  → No action needed right now

Note: You can regenerate all handoffs at any time with:
  /skill architecture-dev-handoff
───────────────────────────────────────────────────────────
```

If propagation was **skipped**: prepend to the advisory:
> `Note: Propagation was skipped — handoff document text was also not updated. Full regeneration is recommended.`

**Wait for user response.**

- **Yes** → Display one line per affected component: `Run: /skill architecture-dev-handoff` (for each affected component by name). Do NOT invoke the skill automatically.
- **No** → Acknowledge and proceed with no further action.
