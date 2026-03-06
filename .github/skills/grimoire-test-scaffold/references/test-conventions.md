# BMAD Grimoire Test Conventions

## File Structure

- Test files: `tests/test_<tool_name_underscored>.py`
- Tool name `dream.py` → test file `test_dream.py`
- Tool name `memory-lint.py` → test file `test_memory_lint.py`

## Import Pattern

All tools use hyphenated names, requiring `importlib`:

```python
import importlib
import sys
from pathlib import Path

KIT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(KIT_DIR / "framework" / "tools"))

def _import_mod():
    return importlib.import_module("tool-name")
```

## Test Class Organization

1. `TestConstants` — VERSION, config constants
2. `TestDataClasses` — dataclass/namedtuple field validation
3. `TestPureFunctions` — functions without side effects
4. `TestProjectFunctions` — functions needing temp filesystem
5. `TestCLI` — argparse parser validation
6. `TestCLIIntegration` — end-to-end subprocess tests

## Common Patterns

### Temp project setup
```python
def setUp(self):
    self.mod = _import_mod()
    self.tmpdir = Path(tempfile.mkdtemp())

def tearDown(self):
    shutil.rmtree(self.tmpdir, ignore_errors=True)
```

### Memory tree helper
```python
def _setup_memory(root, *, learnings=None, decisions=None):
    mem = root / "_bmad" / "_memory"
    mem.mkdir(parents=True, exist_ok=True)
    if learnings:
        ld = mem / "agent-learnings"
        ld.mkdir(exist_ok=True)
        for name, content in learnings.items():
            (ld / name).write_text(content, encoding="utf-8")
```

### CLI parser test
```python
def test_build_parser(self):
    parser = self.mod.build_parser()
    self.assertIsNotNone(parser)

def test_help(self):
    result = subprocess.run(
        [sys.executable, str(TOOL_PATH), "--help"],
        capture_output=True, text=True
    )
    self.assertEqual(result.returncode, 0)
```

## Rules

- Use `unittest.TestCase` (not bare pytest classes)
- Use `_import_mod()` for module import
- Use `tempfile.mkdtemp()` + `shutil.rmtree()` for temp dirs
- stdlib only — no external test dependencies except pytest runner
- Each test should be independent and idempotent
- Target 15-40 tests per tool
