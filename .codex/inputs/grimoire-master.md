# Codex Input - Grimoire Master

Use this file as the Codex-native input projection for Grimoire Forge. It is
an adapter into the existing Grimoire runtime, not a second instruction tree.

## Activation

1. Treat `AGENTS.md` as the root Codex entrypoint.
2. Load `.github/copilot-instructions.md`.
3. Load `.github/agents/grimoire-master.agent.md`.
4. Load `_grimoire-runtime/core/agents/grimoire-master.md`.
5. Load `_grimoire-runtime/core/config.yaml`,
   `_grimoire-runtime/bmm/config.yaml`, and
   `_grimoire-runtime/_memory/shared-context.md`.
6. If the user request is already actionable, skip menu display and execute it
   through the Grimoire Master behavior.

## Host Binding

- Host id: `host-codex`
- Host label: `OpenAI Codex CLI`
- Runtime role: secondary host bound to the single user-facing
  `grimoire-master` orchestrator
- Native entrypoint: `AGENTS.md`
- Tool adapter: `.codex/mcp/grimoire-mcp.sh`
- Host manifest: `_grimoire-runtime/_config/ides/codex.yaml`

Codex must not expose internal Grimoire sub-agents to the user. Any internal
handoff stays implicit and the final answer remains a single coherent result.

## Project Tools

Use the shared MCP projection in `.mcp.json` and the local Codex MCP registry
when available.

| Tool | Purpose | Codex entrypoint |
|---|---|---|
| `grimoire` | Project context, memory, status, preflight and Grimoire checks | `.codex/mcp/grimoire-mcp.sh` |
| `context7` | External package documentation lookup | `https://mcp.context7.com/mcp` |
| `github` | GitHub repository, issue, PR and review context | `https://api.githubcopilot.com/mcp/` |
| `playwright` | Browser interaction and visual verification | `grimoire-kit/framework/tools/playwright-mcp.sh` |

Use local shell commands for deterministic checks when an MCP tool is missing or
not authenticated.

## Memory Backend

- Current runtime memory backend: `weaviate-server`
- Runtime graph projection: `neo4j`
- Rollback/source memory backend: `qdrant-server`
- Qdrant endpoint: `http://localhost:6333`
- Docker compose file: `docker-compose.qdrant.yml`
- Collection: `grimoire_kit`
- Weaviate endpoint: `http://localhost:8080`
- Weaviate collection: `GrimoireKitMemory`
- Neo4j endpoint: `bolt://localhost:7687`
- Target Docker compose file: `docker-compose.memory-target.yml`
- Migration bundle path: `_grimoire/_memory/migration/weaviate-neo4j`
- Code graph sync: `grimoire memory graph sync-code`
- Task memory sync: `grimoire memory graph sync-tasks`
- Code vector sync: `grimoire memory vector sync-code`
- Task vector sync: `grimoire memory vector sync-tasks`
- Vector gate: `grimoire memory vector verify`
- Graph gate: `grimoire memory graph verify`
- Unified Memory OS gate: `grimoire memory gate`

Qdrant remains available as migration source and rollback while recurring
verification keeps Weaviate objects, Neo4j nodes, and bundle source ids aligned.
The `grimoire` MCP wrapper exports `GRIMOIRE_QDRANT_URL` so Codex and the
Grimoire runtime resolve the same Docker-backed Qdrant service during rollback
or re-export operations.

## Execution Contract

- Prefer `rg`, targeted reads, and the validation commands in `.vscode/tasks.json`.
- For documentation edits, load
  `_grimoire-runtime/_memory/tech-writer-sidecar/documentation-standards.md`
  first.
- Respect dirty worktrees. Do not revert unrelated user changes.
- Keep Codex-specific additions thin and point back to the runtime source of
  truth instead of duplicating Grimoire doctrine.
