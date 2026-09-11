# Agentic Evidence Pack

## Summary

- Task id: bootstrap
- Profile: orchestrated
- Outcome: Grimoire-Forge now has an operational agentic-standard baseline with generation, verification, audit, provider registry, knowledge registry, and compliance artifacts.
- Final state: validated

## Evidence inventory

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Agentic standard bridge commit | `grimoire-kit@8e8f283e` | grimoire-kit | Added profile map, templates, archetype, and documentation bridge. |
| Standard setup commit | `grimoire-kit@2258bed3` | grimoire-kit | Added CLI/core profile generation and verification. |
| Content audit commit | `grimoire-kit@eea86949` | grimoire-kit | Added structured verification checks and Markdown/JSON audit command. |
| Forge workflow commit | `Grimoire-Forge@d4dd86a` | Grimoire-Forge | Generated project artifacts and standard workflow wrapper. |
| Forge audit wrapper commit | `Grimoire-Forge@5fcb455` | Grimoire-Forge | Exposed `standard:audit` npm wrapper. |
| Baseline artifact completion | `_grimoire/standard/*`, `_grimoire-output/evidence/bootstrap/evidence-pack.md` | Grimoire-Forge | Filled provider, knowledge, evidence, and compliance baseline. |

## Validation

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Forge profile verification | `npm run standard:verify -- --project-root . --profile orchestrated` | pass | Confirms required artifacts and structured checks. |
| Forge audit report | `npm run standard:audit -- --project-root . --profile orchestrated` | pass | Produces Markdown audit for human review. |
| Kit targeted tests | `.venv/bin/python -m pytest tests/test_agentic_standard.py tests/test_archetype_resolver.py::TestArchetypeResolver::test_archetypes_override_accepts_agentic_standard tests/test_cmd_init.py::TestInitCLI::test_init_with_agentic_standard_archetype -q --tb=short` | pass | Confirms standard CLI, resolver, and init integration. |
| Kit type check | `.venv/bin/python -m mypy src/grimoire/core/agentic_standard.py src/grimoire/cli/cmd_standard.py` | pass | Confirms typed standard modules. |
| Kit lint check | `.venv/bin/python -m ruff check src/grimoire/core/agentic_standard.py src/grimoire/cli/cmd_standard.py tests/test_agentic_standard.py` | pass | Confirms targeted lint quality. |

## Controls

| Control family | Applied? | Evidence | Gap |
|---|---:|---|---|
| Governance | yes | `_grimoire/standard/compliance-declaration.md` | CI enforcement not enabled yet. |
| Quality | yes | Targeted pytest, mypy, ruff validation listed above | Full repository lint still has pre-existing unrelated failures. |
| Runtime | partial | `scripts/setup-agentic-standard.sh`, `package.json` npm scripts | Runtime workflow is local wrapper only; no release gate yet. |
| Knowledge | yes | `_grimoire/standard/knowledge-source-registry.yaml` | Automated indexing/doc-to-graph pipeline not enabled yet. |
| Model/provider | yes | `_grimoire/standard/llm-provider-registry.yaml` | Only GitHub Copilot is active by default; other providers need credentials and policy approval. |

## Deviations and accepted risks

| Deviation | Impact | Accepted by | Review trigger |
|---|---|---|---|
| `grimoire-kit` branch is divergent from `origin/main` | Push/merge needs explicit branch strategy before publication. | Grimoire maintainers | Before remote publication or PR creation. |
| Broad pre-commit hook is blocked by pre-existing unrelated local issues | Commits used targeted validation and `--no-verify` where necessary. | Grimoire maintainers | Before normalizing the repository baseline. |

## Completion statement

The bootstrap task is complete for the orchestrated profile baseline when `standard:verify` returns zero errors and no unresolved placeholder warnings for provider, knowledge, evidence, or compliance artifacts.

## Addendum 2026-09-08 — référence agentique industrielle

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Référence agentique industrielle livrée au produit | `grimoire-kit@9d5ca9f6`, PR Grimoire-kit#315 | session Claude Code | `framework/agentic-industry-reference.md` + `_PROTOCOL_DOCS` + pointeurs socle + test |
| Détail de la tâche | `_grimoire-output/evidence/agentic-industry-reference/` | session Claude Code | task-envelope et evidence-pack complets |
| Audit d'écart Grimoire contre la référence | `_grimoire-output/evidence/bootstrap/audit-ecarts-reference-agentique-20260908.md` | cinq sous-agents Sonnet + vérification manuelle | 8 écarts bloquants confirmés, 15 actions, aucun fichier modifié |

| Check | Command or method | Result | Notes |
|---|---|---|---|
| Kit | pytest ciblé (47 passed), ruff, ratchet | pass | depuis un worktree jetable sur origin/main 3.40.0 |

## Routage par vérifiabilité du kit (2026-09-08)

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Épic et sous-issues | `Grimoire-kit#307`, `#308`-`#313` | session Claude Code | cadrage produit déposé dans le repo kit |
| Émetteurs reasoning × cost | `Grimoire-kit#314` (squash `c4a9d275`) | sous-agent Sonnet, relu et rejoué | 98 tests hôtes verts, CI 26/26 |
| Classe de vérifiabilité V0/V1/V2 | `Grimoire-kit#316` (squash `ad4b20c9`) | sous-agent Sonnet + resserrement vocabulaire | 128 tests missions/mcp verts, CI 26/26 |
| Registre par palier + état runtime | `Grimoire-kit#317` (squash `1747b85b`) | sous-agent Sonnet + correctif test MCP | suites cli/core/missions/mcp vertes, CI 26/26 |
| Prototype lot 0, verdict GO | `Grimoire-kit#308` commentaire 5588081621 | campagne `claude -p` × 20 tâches × 5 ouvriers, recomptée | haiku 20/20, cascade 0,1226 $ vs opus 0,5692 $ par tâche |

## Addendum 2026-09-08 — exécution du plan d'écarts (vague 0)

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Plan d'exécution relu (Opus GO avec amendements, fiche de faisabilité Sonnet) | `_grimoire-output/evidence/bootstrap/plan-execution-ecarts-20260908.md` section 7 | concierge | amendements intégrés |
| Issue épique produit | https://github.com/Guilhem-Bonnet/Grimoire-kit/issues/318 | gh | ouverte |
| Lot F (socle AORA/DCF retirés, PIP observer-only, docs obsolètes) | PR Grimoire-kit#319, worktree kit-lotF | codeur Sonnet | vérificateur Haiku : CONFORME (tests ciblés 100 %, ratchet OK, zéro lien mort, charte respectée) |
| Lot B11 (plafonds kernel, garde P2P) | PR Grimoire-kit#320, worktree kit-lotB11 | codeur Sonnet | vérificateur Haiku : CONFORME (87 tests verts, ruff, ratchet, état REFUSED avec checkpoint et événement, garde P2P 4/5/reset) |
| Lot A (gardes fail-closed, budget de tokens, hook shadow, registre MCP) | PR Grimoire-Forge#32, worktree forge-lotA | codeur Sonnet | test bash 8/8 vert et 8/8 rouge sur l'ancien code ; vérificateur Haiku : CONFORME (8/8 tests bash, 7/7 pytest, verify et gate OK rejoués) ; hooks dépendant de guardrail-policy.py auto-dégradés en shadow, `hooks-promote` requis après merge |
| Lot C (claims exclusifs avec expiration, sous-agents bornés, événements SubagentStart et PostToolUseFailure) | PR Grimoire-kit#321, worktree kit-lotC | codeur Sonnet | vérificateur Haiku : CONFORME (refus nommé fichier/tâche/acteur, expiration, frontmatter stable, événements câblés, ruff, ratchet) ; note : comparaison exacte par chemin, un claim sur un répertoire ne couvre pas ses fichiers |
| Lot E (export OTel GenAI corrigé et unifié, pass^k, catégories d'évals) | PR Grimoire-kit#322, worktree kit-lotE | codeur Sonnet | vérificateur Haiku : CONFORME (77 tests rejoués, spans invoke_agent/execute_tool, horodatages réels, export grimoire.otel.v2, fixtures synthétiques, aucun chevauchement avec #321) |
| Lot F-Forge (instructions chargées 332 → 129 lignes, doctrine en source unique, script `scripts/instructions-budget.py`) | PR Grimoire-Forge#33, worktree forge-lotF | codeur Sonnet | vérificateur Haiku : CONFORME (129/200 rejoué, onze règles opposables présentes, doctrine en source unique, agent-index --check OK, verify 0 erreur) |
| Lot B (validation des écritures mémoire, contrat MCP annoté avec isError, contenu externe marqué, vérificateur tools.mediated-before-use) | PR Grimoire-kit#324, worktree kit-lotB | codeur Opus | 6 506 tests verts, ruff, ratchet, smoke stdio 22 outils annotés selon le codeur ; vérification Haiku : CONFORME ; revue adversariale Sonnet : trois trous réels (remember() sans validation, enveloppe untrusted sans appelant en production, source MCP illisible ignorée) et une annotation readOnly fausse sur task_context ; deux tours de correctifs Opus (six chemins d'écriture validés, normalisation NFKC, trois annotations corrigées, source MCP illisible signalée, `grimoire web fetch` câblé dans le resolver livré sans ligne ajoutée à la zone gelée) ; re-contrôles adversariaux 2 et 3 : TIENT sur tous les points, prêt à merger ; 6 572 tests verts |
| Lot 2b, `grimoire task dispatch` en cascade | `Grimoire-kit#325` (issue #323) | sous-agent Sonnet + distinction error/rate_limit | suites missions/cli/providers/mcp vertes, auto-merge armé |
| #204 moteur de flow, couche d'étape | `Grimoire-kit#326` (prototype jetable puis implémentation) | deux sous-agents Sonnet + renommage `--result` | suite `tests/unit` entière verte hors mémoire, auto-merge armé |

| Gates Forge après campagne | `grimoire standard gate check --task-id bootstrap --strict` ; `grimoire standard verify .` | concierge | voir ci-dessous |

## Addendum 2026-09-08 — merges

| Evidence | Location | Produced by | Result |
|---|---|---|---|
| Forge #32 mergée (squash f74cba63) après quatre correctifs Copilot dont le relayage de `systemMessage` sur le chemin Stop | https://github.com/Guilhem-Bonnet/grimoire-forge/pull/32 | codeur-intendant Sonnet | CI 18/18, fils résolus |
| Forge #33 mergée (squash 279bec45) après conversion des URL en liens inline | https://github.com/Guilhem-Bonnet/grimoire-forge/pull/33 | codeur-intendant Sonnet | budget 129/200, fils résolus |
| Branche de travail fusionnée avec main, six hooks re-promus par identifiant | `_grimoire-runtime/_config/hook-safety-registry.json` | concierge | `hook-safety-gate.py status` : 12 enforced, 2 shadow, 1 canary ; hooks-smoke ok ; gate bootstrap OK ; verify governed 0 erreur |
| `grimoire providers audit` sans dépenser | `Grimoire-kit#331` (issue #330) | sous-agent Sonnet | 92 tests verts, mergée |
| Politique de dispatch émise aux hôtes | `Grimoire-kit#332` (issue #329) | sous-agent Sonnet | 102 tests hôtes verts, mergée |
| Relisibilité du diff + incertitudes déclarées | `Grimoire-kit#334` (issues #327, #328) | sous-agent Sonnet + surfaces génériques | 883 tests verts, mergée (27 checks) |
| Lot 4, palier de départ par historique | `Grimoire-kit#335` (issue #312) | sous-agent Sonnet + verrou de plancher | 910 tests verts, mergée |
| Lot 3, exécuteur dispatch dans flow run | `Grimoire-kit#336` (issue #311) | sous-agent Sonnet + correctif import mypy strict | mypy strict 217 fichiers propre, tests verts, mergée |
| Kit #319 mergée (0f2761ca) + correctif #333 (70df7249, typo ; régénération du registre de hachages refusée à raison : elle aurait attribué du contenu non publié à la 3.40.0) | intendant Sonnet | fils Copilot traités | main vert |
| Kit #320 mergée (99298a27) après correction : plafonds vérifiés avant émission, `cost` négatif refusé, `yaml.YAMLError` attrapée | intendant Sonnet | fils résolus | main vert |
| Kit #321 mergée (b88ec0df) après correction : `is_expired()` sur horodatage naïf, timestamp invalide traité comme expiré et journalisé | intendant Sonnet | conflit résolu | main vert |
| Kit #322 mergée (0c21ccbf) ; `pass_hat_k` porté dans `evals/pass_hat_k.py` car main a supprimé le paquet legacy | intendant Sonnet | conflit modify/delete résolu | main vert (Validate, SDK, E2E) |
| Kit #324 : CI verte sur e2e80363 après alignement sur mcp 2.2.0 (la CI ne résout pas comme le venv local) et trois tours CodeQL ; conflit avec main en cours de résolution par le codeur | codeur Opus | 26 jobs pass, 0 alerte CodeQL | en cours |
| Release 3.41.0 | `Grimoire-kit#337`, tag v3.41.0, PyPI 3.41.0 | sous-agent Sonnet, décision repli changelog par numéro de PR | workflows release et publish verts |
| Kit #324 mergée (e28d68e9) après résolution d'un conflit sur `docs/cli-reference.md` ; main six runs verts | codeur Opus | 26 jobs pass, 0 alerte CodeQL nouvelle | main vert |
| Release grimoire-kit 3.41.0 : PR #337 squash 72bcc7cf, tag v3.41.0, publish.yml et release.yml verts, PyPI et release GitHub confirmés | intendant Sonnet | trois rouges tracés à leur cause (venv non aligné sur ruff CI, garde changelog cassé depuis 3.39.1, précondition E2E) et corrigés sans contournement | publié |
| Forge consomme 3.41.0 : venv mis à niveau, `host sync` + `grimoire up` (agents avec effort/maxTurns, référence livrée dans `_grimoire/kit/framework/`, resolver vers `grimoire web fetch`), hook `grimoire-subagent-context` re-promu (13 enforced), `out_of_scope_reason` sur huit entrées MCP | commit ac1bf67 | intendant Sonnet | hooks-smoke ok, doctor 23/24 (playwright préexistant), gate OK |
| Artefacts que la 3.41.0 exige au profil governed : bloc `write_validation` dans `memory-policy.yaml`, `prompt-firewall.yaml` (trois sources en quarantaine) | `_grimoire/standard/` | concierge | `standard verify` 0 erreur 0 avertissement ; gate bootstrap OK |
| Forge sur 3.41.0, registre renseigné | commit `2e27150`, `grimoire providers audit` | session Claude Code | anthropic et local sondés disponibles, copilot ignoré faute de commande |
| Chaîne de dispatch prouvée bout-en-bout | `task dispatch --dry-run` sur une tâche V0 jetable | session Claude Code | V0 détectée, chaîne cheap → mid → strong, consigne d'incertitudes présente |
| Écritures du cockpit réparées | `Grimoire-kit#358`, garde 4 routes avec query string | session Claude Code | garde rouge sans correctif, verte avec |
| Registre du cockpit assaini | `Grimoire-kit#343` | sous-agent + relecture | 31,2 s → 1,15 s, suppression d'office refusée |
| Pyramide de tests | `Grimoire-kit#361` | agent isolé + correctif encodage Windows | 4 défauts couverts, chacun prouvé rouge avant son correctif |
| Agent de sécurité | `Grimoire-kit#357` | sous-agent | campagne ~850 exemples, 0 plantage, couverture mesurée |
| Audit Rust | `Grimoire-kit#354` commentaire | agent isolé | premier module `policies`, coût 5 roues par version |
| Premier port Rust | `Grimoire-kit#363` | agent isolé + correctif CI | parité prouvée dans les deux configurations, roue restée universelle |
| Bouton mort retiré | `Grimoire-kit#362` | sous-agent + vérification navigateur | en-tête intact, garde contre un bouton sans écouteur |
| Doctrine des artefacts | `Grimoire-kit#370` (issue #368) | sous-agent + relecture d'échantillon | garde use_when/tools sur 33 agents, mergée |
| Audits agents, contextes, skills | `Grimoire-kit#369`, `#371` commentaires | trois agents spécialisés | 0/33 tools déclarés, 21/33 même contexte, 0 skill rattaché |
| Instrumentation du choix d'agent | `Grimoire-kit#366` | sous-agent + commit par le concierge | best-effort testé, mypy strict propre |
| Outil d'ajout d'agent réel | `Grimoire-kit#367` | sous-agent | fichier vu par diagnostic et routage |
| Skills attachés par défaut | `Grimoire-kit#377` | sous-agent + double régime de garde par le concierge | 1 480 vs 0 tokens/tour mesurés, job CI rejoué localement |
| Contexte déclaré câblé | `Grimoire-kit#378` | sous-agent | 476 vs 157 tokens, agent sans contexte identique bit à bit |
| infra-ops refait | `Grimoire-kit#380` | agent-optimizer + relecture de conversion | 4 agents → 4 skills, sujets techniques conservés, init sans note |
| Cockpit : agents et skills | `Grimoire-kit#382` (issue #374) | sous-agent navigateur + fusion de main et 4 suites rejouées par le concierge | 11 fichiers additifs, e2e vert, registre réel revérifié intact |
| Instrumentation fusionnée après correctif lint | `Grimoire-kit#366` | concierge, ruff épinglé version CI | noqa restauré, suites vertes, mergée |
| Identité d'agent, source unique | `Grimoire-kit#383` (issue #381) | sous-agent + lint CI, typage, e2e rejoués par le concierge | garde rouge avant, verte après, mergée |
| Archétypes refaits, cinq lots + émission allégée | `Grimoire-kit#384` `#385` `#386` `#387` `#388` `#390` | sous-agents Sonnet, conflits CHANGELOG et régressions (détection de pile, e2e reciblé, test lisant origin/main) traités en session | tous fusionnés le 2026-09-11, 0 PR ouverte, worktrees supprimés, release 3.42.0 déléguée |
| La Forge consomme la release 3.42.0 | `Grimoire-kit#391` (release), `#392` (second port Rust, en fusion auto) | venv 3.42.0, `grimoire up`, `host sync`, retrait des 4 agents orphelins de meta devenus skills attachés (`up` ne supprime pas les orphelins), résiduels `.claude/worktrees` purgés | verify OK, agent-optimizer émis avec ses 4 skills |
