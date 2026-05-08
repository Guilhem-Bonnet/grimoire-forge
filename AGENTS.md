# Grimoire Forge - AGENTS Bridge

Use this file as the Codex / AGENTS.md-compatible entrypoint for the same
project instructions already exposed through `CLAUDE.md` and GitHub Copilot.

## Bootstrap

1. Read `.github/copilot-instructions.md`.
2. Read `.github/agents/grimoire-master.agent.md`.
3. From that agent file, load `_grimoire-runtime/core/agents/grimoire-master.md`
   and follow its activation instructions exactly.
4. When running inside Codex, read `.codex/inputs/grimoire-master.md` as the
   Codex-native host/tool adapter. It must not override the Grimoire runtime.
5. Treat `grimoire-master` as the single user-facing orchestrator. All other
   agents are internal sub-agents and should stay invisible to the user.
6. If the first user message is already actionable, skip any menu/bootstrap and
   execute the request directly.

## Project Defaults

- Communication language: Francais
- Document output language: Francais
- Primary project instructions: `.github/copilot-instructions.md`
- Primary orchestrator agent: `.github/agents/grimoire-master.agent.md`
- Runtime source of truth: `_grimoire-runtime/`
- Codex native input: `.codex/inputs/grimoire-master.md`
- Shared MCP projection: `.mcp.json`

## Codex Tooling

- Mirror project MCP servers from `.mcp.json` into the local Codex MCP config
  when the host supports it.
- The Grimoire MCP stdio entrypoint for Codex is `.codex/mcp/grimoire-mcp.sh`.
- Treat Codex as host `host-codex`, configured in
  `_grimoire-runtime/_config/ides/codex.yaml`.
- Use the same safety model as the runtime: preview/read first, validation
  before durable writes, and explicit proof for risky changes.

## Workspace Conventions

- Respect the instruction files in `.github/instructions/` when they apply.
- When workspace MCP servers are supported, use `.vscode/mcp.json`.
- Prefer the validation commands documented in `README.md` and the tasks in
  `.vscode/tasks.json`.
- Do not invent an alternate agent tree when the existing Grimoire runtime
  already covers the request.
