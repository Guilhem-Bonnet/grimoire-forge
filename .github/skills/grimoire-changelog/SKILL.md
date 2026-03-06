---
name: grimoire-changelog
description: 'Generate a structured CHANGELOG from git history and session chain. Use when: changelog, release notes, what changed, version bump, prepare release, summarize changes, diff since last release, release prep. Combines git log analysis with session chain context for rich changelogs.'
---

# Grimoire Changelog

Generate a structured CHANGELOG entry from git commits and session chain context.

## When to Use

- Preparing a release or version bump
- When the user asks "what changed?", "generate changelog", or "release notes"
- Before tagging a new version
- Periodic summary of recent work

## Procedure

### Step 1 — Identify Scope

Determine the range of changes to cover:

```bash
git tag --sort=-version:refname | head -5
```

If tags exist, use the last tag as baseline. Otherwise, use a date or commit range.

```bash
git log --oneline <last-tag>..HEAD
```

Or by date:

```bash
git log --oneline --since="2 weeks ago"
```

### Step 2 — Categorize Commits

```bash
git log --pretty=format:"%h %s" <range> | sort -t: -k1
```

Group by conventional commit prefix:
- **feat:** — New features
- **fix:** — Bug fixes
- **docs:** — Documentation
- **refactor:** — Code restructuring
- **test:** — Test additions/changes
- **chore:** — Maintenance, dependencies

### Step 3 — Enrich with Session Chain

```bash
cat _bmad/_memory/session-chain.jsonl 2>/dev/null | tail -10
```

Cross-reference session summaries with commits to add context:
- What was the intent behind each change?
- What decisions drove the implementation?
- Any notable trade-offs or design choices?

### Step 4 — Check File Impact

```bash
git diff --stat <range>
```

Quantify the changes:
- Files changed
- Lines added/removed
- Key files affected

### Step 5 — Read Current CHANGELOG

```bash
head -30 CHANGELOG.md 2>/dev/null
```

Understand the existing format and continue with the same style.

### Step 6 — Generate Entry

Format following [Keep a Changelog](https://keepachangelog.com/) convention:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Feature description (#commit-ref)

### Changed
- Change description

### Fixed
- Bug fix description

### Stats
- N files changed, +N insertions, -N deletions
- N commits by N contributors
```

### Step 7 — Update CHANGELOG.md

Prepend the new entry at the top of `CHANGELOG.md` (after the header), preserving all existing entries.

### Step 8 — Suggest Version Bump

Based on changes:
- **PATCH** (X.Y.Z+1) — only fixes and minor changes
- **MINOR** (X.Y+1.0) — new features, backward compatible
- **MAJOR** (X+1.0.0) — breaking changes

Check current version:

```bash
cat version.txt 2>/dev/null
```

## Quick Mode

For a rapid summary without full formatting:

```bash
git log --oneline --since="1 week ago" | head -20
```

Present as a bullet list without full CHANGELOG structure.

## Notes

- Always preserve existing CHANGELOG entries — prepend, never overwrite
- Use commit hashes as references for traceability
- Session chain provides the "why" behind the "what" from git
- If no conventional commit prefixes are used, categorize by file path patterns
