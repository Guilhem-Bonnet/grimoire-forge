# Documentation externe

Référencé depuis `.github/copilot-instructions.md`. Documentation approfondie des
dépendances et frameworks utilisés par le projet.

| Ressource | URL | Usage |
|---|---|---|
| VS Code Copilot Hooks (official) | `https://code.visualstudio.com/docs/copilot/customization/hooks` | Contrat JSON stdin/stdout, evenements, `permissionDecision`, `decision: block`, securite |
| VS Code Copilot Chat System | `https://deepwiki.com/microsoft/vscode-copilot-chat` | Vue d'ensemble custom agents, prompts, skills, hooks, instructions |
| VS Code Copilot Tool Calling Loop | `https://deepwiki.com/microsoft/vscode-copilot-chat/5.4-tool-calling-loop-and-execution` | Ordre d'execution des hooks, accumulation de `additionalHookContext`, boucle autopilot |
| VS Code Copilot Chat Hooks | `https://deepwiki.com/microsoft/vscode-copilot-chat/5.5-chat-hooks-and-extensibility` | Execution source-level des hooks, result processing, telemetry, output channel |
| VS Code Copilot Conversation Summarization | `https://deepwiki.com/microsoft/vscode-copilot-chat/5.6-conversation-summarization` | Integration `PreCompact`, compaction et preservation du contexte |
| Ruff Linter | `https://deepwiki.com/astral-sh/ruff` | Règles, configuration, per-file-ignores |
| Pytest | `https://deepwiki.com/pytest-dev/pytest` | Fixtures, markers, plugins |
| Typer CLI | `https://deepwiki.com/fastapi/typer` | CLI framework utilisé par grimoire |
| Mermaid | `https://deepwiki.com/mermaid-js/mermaid` | Syntaxe diagrammes v10+ |

Les URLs DeepWiki sont disponibles via MCP `deepwiki` si configuré, ou via navigateur.
Pour consulter en session : utiliser `fetch` MCP ou demander une recherche ciblée.
