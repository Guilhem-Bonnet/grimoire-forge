---
name: grimoire-test-scaffold
description: 'Generate test scaffolding for a BMAD Grimoire tool. Use when: generate tests, create tests, scaffold tests, write tests for tool, test a tool, add test coverage, new tests needed. Inspects the tool, identifies testable functions, and generates test skeleton following project conventions.'
---

# Grimoire Test Scaffold

Generate a comprehensive test file for a BMAD Grimoire tool, following established project conventions.

## When to Use

- A new tool has been created and needs tests
- Test coverage needs to be improved for an existing tool
- When the user says "generate tests for X", "scaffold tests", or "add test coverage"

## Procedure

### Step 1 — Identify the Target Tool

The user specifies a tool name (e.g., `dream.py`, `memory-lint.py`). Locate it:

```bash
ls framework/tools/<tool-name>
```

### Step 2 — Inspect the Tool

Read the tool file and identify:

1. **Public functions** — any function without `_` prefix (the main API)
2. **Key private functions** — important internal logic worth testing
3. **Dataclasses/NamedTuples** — data structures to validate
4. **CLI interface** — argparse setup if present
5. **Constants** — version, configuration values
6. **MCP entry points** — any `mcp_*` functions

```bash
grep -n "^def \|^class \|^[A-Z_]* = \|VERSION" framework/tools/<tool-name>
```

### Step 3 — Review Existing Test Patterns

Check if tests already exist:

```bash
ls tests/test_<tool-name-with-underscores>.py 2>/dev/null
```

Review the [test conventions reference](./references/test-conventions.md) for project patterns.

### Step 4 — Generate Test File

Create `tests/test_<tool_name>.py` following these conventions:

```python
#!/usr/bin/env python3
"""Tests pour <tool-name>.py — <Tool description>."""

import importlib
import sys
import tempfile
import unittest
from pathlib import Path

# ── Import via importlib (hyphenated module names) ────────────────────────
KIT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(KIT_DIR / "framework" / "tools"))


def _import_mod():
    return importlib.import_module("<tool-name>")


# ── Test Classes ──────────────────────────────────────────────────────────

class TestConstants(unittest.TestCase):
    def setUp(self):
        self.mod = _import_mod()

    def test_version_defined(self):
        self.assertTrue(hasattr(self.mod, '<TOOL>_VERSION'))


class TestDataClasses(unittest.TestCase):
    """Test dataclass/namedtuple definitions."""
    ...


class TestPureFunctions(unittest.TestCase):
    """Test functions that don't need filesystem."""
    ...


class TestProjectFunctions(unittest.TestCase):
    """Test functions that need a temp project root."""
    def setUp(self):
        self.mod = _import_mod()
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)


class TestCLI(unittest.TestCase):
    """Test argparse and CLI integration."""
    ...


if __name__ == "__main__":
    unittest.main()
```

### Step 5 — Generate Test Bodies

For each identified function, generate meaningful tests:

- **Happy path**: Normal usage with expected inputs
- **Edge cases**: Empty inputs, missing files, boundary values
- **Error handling**: Invalid inputs, missing project root
- **Integration**: End-to-end CLI invocation

### Step 6 — Validate

```bash
python3 -m pytest tests/test_<name>.py -v --tb=short
```

All generated tests must pass. Fix any failures before presenting the result.

## Test Naming Convention

- Class: `TestFunctionGroup` (e.g., `TestDiagnose`, `TestCLI`, `TestConstants`)
- Method: `test_<what_it_tests>` (e.g., `test_empty_project_returns_clean`, `test_version_defined`)

## Notes

- Use `unittest` (not pytest classes) — this is the project convention
- Use `_import_mod()` pattern for hyphenated module names
- Use `tempfile.mkdtemp()` for filesystem tests
- Tests should be stdlib-only, matching the tools themselves
- Target: 15-40 tests per tool depending on complexity
