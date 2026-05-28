# Agentic Task Envelope

## Task

- Task id: bootstrap
- Request: put the agentic standard workflow in place for Grimoire-Forge and grimoire-kit, then harden and audit the baseline.
- Owner agent: Copilot CLI runtime in VS Code
- Profile: orchestrated
- Current state: `done`
- Risk level: `medium`

## Context orchestration

| Context item | Source | Reason selected | Freshness | Token budget |
|---|---|---|---|---:|
| Profile map | `grimoire-kit/framework/agentic-standard/profile-map.yaml` | Defines required artifacts and profile capabilities. | current working tree | 2000 |
| Generated Forge artifacts | `_grimoire/standard/*`, `_grimoire-output/evidence/bootstrap/*` | Declares project-specific baseline and evidence. | current working tree | 4000 |
| Standard core implementation | `grimoire-kit/src/grimoire/core/agentic_standard.py` | Defines verification semantics and warning/error rules. | current working tree | 3000 |
| Standard CLI implementation | `grimoire-kit/src/grimoire/cli/cmd_standard.py` | Defines user-facing verify and audit commands. | current working tree | 2000 |

## Knowledge base usage

| Knowledge source | Query or index | Trust level | Used as source of truth? | Notes |
|---|---|---|---:|---|
| agentic-standard-corpus | `../processus-developpement-agentique` | authoritative | yes | Upstream standard remains external and normative. |
| grimoire-forge-runtime | `.` | high | yes | Project-specific generated artifacts and wrappers. |
| grimoire-kit-framework | `grimoire-kit/framework/agentic-standard` | high | yes | Template/profile bridge consumed by Forge. |

## Memory usage

| Memory surface | Read/write | Purpose | Integrity check |
|---|---|---|---|
| session summary | read | Continue the previous implementation thread after compaction. | Cross-check against repository files before editing. |
| SQL todos | read/write | Track P0.5 baseline completion. | Mark done only after verification passes. |

## Tool boundary

| Tool | Permission | Scope | Blast-radius limit |
|---|---|---|---|
| `view`, `rg`, `bash` | read/execute | Inspect artifacts and run existing validations. | No destructive commands. |
| `apply_patch` | write | Standard baseline artifacts only. | Surgical edits to declared files. |
| `git` | read/commit if needed | Local repo metadata and targeted staging. | No reset/checkout of user changes. |

## LLM routing

| Step | Provider | Model or capability | Fallback | Data policy |
|---|---|---|---|---|
| Implementation and audit assistance | github-copilot | code, review, reasoning through CLI runtime | anthropic/openai/local when explicitly configured | No secrets, credentials, personal data, or regulated data. |

## Evidence gates

| Gate | Required evidence | Status |
|---|---|---|
| Plan accepted or autonomous assumption recorded | User approved next step with "ok go"; scope inferred from current 7 audit warnings. | complete |
| Implementation complete | Provider, knowledge, evidence, mission, task, and compliance artifacts filled. | complete |
| Validation complete | `standard:verify` and `standard:audit` outputs recorded in evidence pack. | complete |
| Deviations documented | Compliance declaration and evidence pack list current gaps. | complete |
