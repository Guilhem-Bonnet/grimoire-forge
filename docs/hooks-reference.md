# Hooks du cycle de vie agent

Référencé depuis `.github/copilot-instructions.md`. Les hooks natifs VS Code/Copilot
couvrent le cycle agent (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`,
`PreCompact`, `Subagent*`, `Stop`) mais pas `tasks.json` ; l'orchestration et la preuve
task-level restent déléguées à `.github/hooks/scripts/grimoire-task-flow.sh` et
`.vscode/tasks.json`. Voir la règle « Hook promotion guard » dans
`.github/copilot-instructions.md` pour la gouvernance shadow/canary/enforced.

| Hook | Événement | Action |
|---|---|---|
| grimoire-session-start | SessionStart | Injection d'un contexte Grimoire court via `additionalContext` |
| grimoire-prompt-submit | UserPromptSubmit | Audit du prompt, references hooks/task-flow, contraintes de session |
| grimoire-memory-guard | PreToolUse | Protection mémoire `_grimoire-runtime/_memory/` |
| grimoire-control-surface-guard | PreToolUse | Garde-fous sur surfaces de controle agentiques et patterns destructifs |
| grimoire-post-edit | PostToolUse | Validation locale deterministe (`ruff`, `bash -n`, JSON hooks, frontmatter YAML) |
| grimoire-memory-gate | PostToolUse | Gate enforced Memory OS pour bloquer les drifts Weaviate/Neo4j/code graph quand l'environnement est disponible |
| grimoire-subagent-context | SubagentStart | Injection d'un contexte concis aux sub-agents |
| grimoire-subagent-trace | SubagentStart/Stop | Tracing des transitions SOG |
| grimoire-pre-compact | PreCompact | Capsule de contexte avant compaction/summarization |
| grimoire-master-stop-hook | Stop (agent scope) | Empeche une cloture seche et force une relance utilisateur concise |
| grimoire-rtk-rewrite | PreToolUse | Reecriture des commandes shell via RTK (Rust Token Killer) — compresse les sorties verboses (git, pytest, ruff, build...) avant l'agent. `mode: enforced` (actif). Repli non bloquant via `hook-safety-gate.py set-mode shadow grimoire-rtk-rewrite` |
