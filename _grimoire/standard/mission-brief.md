# Agentic Mission Brief

## Identity

- Project: Grimoire-Forge
- Owner: Grimoire maintainers
- Selected profile: `governed`
- Upstream standard reference: processus-developpement-agentique/docs/norme-structure-agentique.md
- Date: 2026-05-29

## Scope

- In scope: generate, verify, audit, and maintain standard-aware Grimoire project artifacts from grimoire-kit.
- Out of scope: redefining the upstream normative corpus; storing provider secrets; enforcing production release gates before branch strategy is settled.
- Critical assets: `_grimoire/standard/*`, `_grimoire-output/evidence/bootstrap/*`, `grimoire-kit/framework/agentic-standard/*`, `grimoire-kit/src/grimoire/core/agentic_standard.py`, `grimoire-kit/src/grimoire/cli/cmd_standard.py`.
- Risk level: `medium`

## Flow objectives

| Objective | Expected outcome | Evidence required |
|---|---|---|
| Operable standard profile | Forge can initialize, verify, and audit the `orchestrated` profile. | `npm run standard:verify`, `npm run standard:audit` |
| Provider-neutral compatibility | LLM provider usage is declared through a registry before execution. | `_grimoire/standard/llm-provider-registry.yaml` |
| External knowledge separation | Knowledge sources are declared separately from memory and session context. | `_grimoire/standard/knowledge-source-registry.yaml` |
| Evidence-gated completion | Bootstrap work is traceable to commits and validation commands. | `_grimoire-output/evidence/bootstrap/evidence-pack.md` |

## Mandatory capabilities

| Capability | Required? | Grimoire artifact | Notes |
|---|---:|---|---|
| Workflow State Engine | yes | Task envelope | Declared per task; runtime enforcement is a follow-up. |
| Advanced Context Orchestrator | profile-dependent | Task envelope, context policy | Context source, freshness, and reason are documented. |
| Knowledge Base Indexer | profile-dependent | Knowledge source registry | Not memory, not session context |
| LLM Provider Registry | profile-dependent | Provider registry | Provider-first routing |
| Evidence-Gated Workflow | yes | Evidence pack | Required validation evidence is recorded. |

## Governance assumptions

- Approved tools: local shell validation, grimoire-kit CLI, npm wrappers, git metadata reads.
- Writable paths: `_grimoire/standard/**`, `_grimoire-output/evidence/bootstrap/**`, Forge wrapper/docs files, grimoire-kit standard implementation files.
- External services: GitHub Copilot as active default provider; other hosted providers disabled until explicit configuration.
- Data classes allowed in prompts: public docs, project source, generated artifacts, non-secret metadata.
- Data classes forbidden in prompts: secrets, credentials, personal data, regulated data.

## Known deviations

| Deviation | Reason | Expiry or review trigger |
|---|---|---|
| CI enforcement not enabled yet | Branch and publication strategy is not settled. | Before remote publication or PR creation. |
| Automated knowledge indexing not enabled yet | Current milestone establishes registry and auditability first. | Before moving from `orchestrated` to `governed`. |
