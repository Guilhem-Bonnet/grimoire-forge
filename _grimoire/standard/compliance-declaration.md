# Agentic Compliance Declaration

## Declaration

- Project: Grimoire-Forge
- Declared profile: `governed`
- Standard reference: processus-developpement-agentique/docs/norme-structure-agentique.md
- Declaration owner: Grimoire maintainers
- Review cadence: before each profile, provider-routing, or standard-mapping change

## Profile coverage

| Requirement or capability | Status | Evidence | Gap |
|---|---|---|---|
| Workflow State Engine | partial | `_grimoire-output/evidence/bootstrap/task-envelope.md` | State is documented per task; runtime FSM enforcement remains future work. |
| Advanced Context Orchestrator | partial | `_grimoire-output/evidence/bootstrap/task-envelope.md`, `_grimoire/standard/knowledge-source-registry.yaml` | Context selection is documented; automatic ranking/budget enforcement is not implemented yet. |
| Evidence-Gated Workflow FSM | partial | `_grimoire-output/evidence/bootstrap/evidence-pack.md`, `grimoire standard verify` | Evidence is auditable; hard fail gates are not wired into CI yet. |
| Agent Telemetry Plane | deferred | `_grimoire-output/task-flow/events.jsonl` | Existing runtime events are present but not normalized into a standard telemetry plane. |
| Tool Blast-Radius Limiter | partial | `_grimoire-output/evidence/bootstrap/task-envelope.md` | Tool scopes are declared; enforcement is currently procedural. |
| Knowledge Base Indexer | partial | `_grimoire/standard/knowledge-source-registry.yaml` | Sources are declared; automated indexing/doc-to-graph pipeline is not active yet. |
| LLM Provider Abstraction | partial | `_grimoire/standard/llm-provider-registry.yaml` | Registry is provider-neutral; only GitHub Copilot is active by default. |
| Memory OS Contract | partial | `_grimoire/standard/memory-policy.yaml` | Memory OS target declared (Redis+Weaviate+Neo4j+SQLite); Redis adapter pending R8. |
| Task Board Governance | active | `_grimoire/standard/task-board.yaml` | R7/R8/R9/R10 tasks tracked with acceptance criteria and evidence refs. |

## Provider compatibility

| Provider | Status | Allowed use | Data policy |
|---|---|---|---|
| GitHub Copilot | conformant | Active default for chat, code, review, and audit workflow support | No secrets, credentials, personal data, or regulated data in prompts. |
| OpenAI Codex/OpenAI | supported-disabled | Optional chat, code, reasoning, embeddings after credentials and policy approval | Same hosted-provider restrictions as registry. |
| Anthropic Claude | supported-disabled | Optional chat, code, reasoning after credentials and policy approval | Same hosted-provider restrictions as registry. |
| Google Gemini | supported-disabled | Optional chat, code, multimodal, reasoning after credentials and policy approval | Same hosted-provider restrictions as registry. |
| Local/open-weight | supported-disabled | Optional local chat, code, embeddings for sensitive-local-only workloads | Secrets still require redaction; regulated data requires approval. |

## Environment controls

| Control | Status | Notes |
|---|---|---|
| Secret scanning | active | `.gitignore` excludes secrets; pre-commit blocks credential commits. |
| Provider data policy | active | Registry enforces non-secret data only to hosted providers. |
| Memory redaction | declared | Redaction required for all memory types before provider use. |
| Regulated data | blocked | No regulated data class is allowed in any provider interaction. |
| CI gate | partial | `grimoire standard verify` available; CI pipeline integration pending. |

## Workspace controls

| Control | Status | Notes |
|---|---|---|
| Multi-project boundary | declared | Knowledge registry separates project-local from cross-project sources. |
| Session isolation | enforced | Session memory is ephemeral and task-bound. |
| Cross-project reads | explicit-allowlist | Workspace memory type requires explicit allowlist declaration. |
| Sidecar isolation | declared | SQLite sidecar stays within project root. |

## Non-conformities

| Item | Severity | Remediation | Owner |
|---|---|---|---|
| CI release gate not enabled for `standard verify` | medium | Add standard verification to CI once branch publication strategy is settled. | Grimoire maintainers |
| Automated knowledge indexing not enabled | medium | Implement doc-to-graph or index-manifest generation from declared sources. | Grimoire maintainers |
| Provider failover is declared but not runtime-enforced | low | Bind registry routing to future runtime provider contract. | Grimoire maintainers |
| Redis hot memory adapter not yet implemented | medium | R8 planned. Short-term layer currently reports `planned`. | Grimoire maintainers |

## Statement

This declaration describes the Grimoire Kit implementation state for a selected profile. It does not replace the upstream normative corpus.
