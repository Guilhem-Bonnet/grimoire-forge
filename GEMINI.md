<!-- grimoire:managed — régénéré par `grimoire host sync`; éditez la source, pas ce fichier. -->

# Grimoire-Forge — Gemini CLI

Projet **Grimoire Kit**. Instructions canoniques : [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

Cet hôte lit des instructions et parle MCP ; il n'exécute ni sous-agents, ni
compétences chargées à la demande, ni hooks de cycle de vie. Ce fichier tient
donc lieu de catalogue : tout ce qui suit s'active en lisant un fichier ou en
lançant une commande.

## Personas

| Persona | Rôle | Définition | Outils |
|---|---|---|---|
| `agent-optimizer` | Agent Quality Assurance & Optimizer — Sentinel — généraliste meta : arbitrage d'agents/workflows, plus les skills attachés meta-art-direction, meta-toolsmithing, meta-memory-quality, meta-project-navigation | `_grimoire/kit/agents/agent-optimizer.md` | read, search, edit |
| `concierge` (entrée) | Concierge — Triage, clarification, routage intelligent vers l'agent adapté | `_grimoire/kit/agents/concierge.md` | read, search |
| `security-auditor` | Security Auditor — cartographie des surfaces d'entrée, fuzzing, triage de plantages, analyse binaire cadrée | `_grimoire/kit/agents/security-auditor.md` | read, execute |

Activer une persona = lire sa définition en entier et l'appliquer, sans la
résumer. Aucun contexte n'est isolé sur cet hôte : la persona s'ajoute à la
conversation courante au lieu de s'exécuter à part.

## Compétences

| Compétence | Quand l'utiliser | Contenu |
|---|---|---|
| `grimoire-agent-dispatch` | Choisir et activer la bonne persona Grimoire du projet. À utiliser quand une demande relève clairement d'un rôle (architecture, tests, documentation, sécurité, produit) plutôt que d'une exécution directe, ou quand l'utilisateur demande un avis spécialisé. | `_grimoire/hosts/skills/grimoire-agent-dispatch.md` |
| `grimoire-evidence` | Protocole de preuve du standard agentique Grimoire. À utiliser dans un projet enrôlé (présence de _grimoire/standard/) dès qu'une tâche modifie du code, de la configuration ou de l'infrastructure : avant la première modification, pendant le travail, et avant toute conclusion. | `_grimoire/hosts/skills/grimoire-evidence.md` |
| `grimoire-memory` | Mémoire projet Grimoire : retrouver une décision passée, un incident ou une convention, et consigner ce qui doit survivre à la session. À utiliser avant de reprendre un sujet déjà traité, et après toute décision non déductible du code. | `_grimoire/hosts/skills/grimoire-memory.md` |
| `meta-art-direction` | Concevoir une identité visuelle d'agent (persona, ton, icône), un template de sortie (rapport/dashboard/checklist) ou une palette d'icônes cohérente pour le projet. À utiliser quand une nouvelle persona doit être créée ou qu'un format de sortie manque de cohérence — pas pour de la relecture qualité ordinaire d'un agent (voir l'arbitrage d'agent-optimizer). | `_grimoire/hosts/skills/meta-art-direction.md` |
| `meta-memory-quality` | Auditer à la demande la qualité de la mémoire du projet : contradictions, doublons de learnings, fraîcheur, drift. À utiliser pour un audit ponctuel avec enjeu de qualité — la maintenance de routine (pruning, archivage) tourne déjà sans agent, via les hooks du cercle vertueux. | `_grimoire/hosts/skills/meta-memory-quality.md` |
| `meta-project-navigation` | Cartographier ou retrouver une connaissance dispersée du projet (services, ports, configs, ADRs) et arbitrer `shared-context.md` quand deux sources se contredisent. À utiliser quand la connaissance cherchée n'est pas déjà indexée et nommée — sinon une recherche directe suffit. | `_grimoire/hosts/skills/meta-project-navigation.md` |
| `meta-toolsmithing` | Créer, auditer ou refactorer un outil framework Grimoire (CLI, module, pattern d'automatisation sous framework/tools/). À utiliser dès qu'un outil doit être forgé, testé triple-interface (CLI/MCP/module) ou découpé — pas pour créer un agent (arbitrage d'agent-optimizer) ni un workflow métier. | `_grimoire/hosts/skills/meta-toolsmithing.md` |

Aucun chargement automatique ici : lire le fichier quand la situation décrite se présente.

## Commandes

| Commande | Effet |
|---|---|
| `grimoire host run grimoire-changelog` | Génère un CHANGELOG structuré depuis git history et les décisions Grimoire |
| `grimoire host run grimoire-doctor [--fix]` | Diagnostiquer et réparer l'installation Grimoire du projet |
| `grimoire host run grimoire-dream` | Dream Mode — consolidation hors-session, patterns cross-domaine, insights émergents |
| `grimoire host run grimoire-gate [task-id]` | Vérifier les gates de preuve de la tâche courante |
| `grimoire host run grimoire-health-check` | Health check complet du projet Grimoire — agents, mémoire, config, intégrité |
| `grimoire host run grimoire-pre-push` | Validation pre-push — intégrité agents, qualité code, mémoire, tests si disponibles |
| `grimoire host run grimoire-proof [task-id]` | Compléter le pack de preuve de la tâche courante |
| `grimoire host run grimoire-recall <sujet>` | Chercher une décision, un incident ou une convention en mémoire projet |
| `grimoire host run grimoire-self-heal` | Auto-diagnostic et réparation Grimoire — identifie et corrige les problèmes courants |
| `grimoire host run grimoire-session-bootstrap` | Bootstrap une nouvelle session Grimoire — contexte projet, historique, état git, santé |
| `grimoire host run grimoire-status` | Tableau de bord Grimoire — agents actifs, mémoire, activité récente, état projet |
| `grimoire host run grimoire-verify` | Vérification complète du standard agentique et score de conformité |

## MCP

Serveurs déclarés dans `.mcp.json` : `context7`, `github`, `playwright`, `grimoire`.

## Gouvernance

- **session_start** — Directive de session — mécanisme mesuré 40/40 contre 0/40 sans lui (campagne 2026-07-09).
- **pre_tool_use** — Refus des mutations destructrices et des accès secrets, selon le profil de risque.
- **user_prompt_submit** — Nomme la tâche courante avant que le modèle ne choisisse où écrire ses preuves.
- **post_tool_use** — Rappelle qu'une écriture doit laisser une ligne de preuve.
- **pre_compact** — Sauvegarde la tâche et les gates ouverts avant une remise à zéro du contexte.
- **subagent_stop** — Remonte l'état des gates sans bloquer un sous-agent qui ne clôt pas la tâche.
- **stop** — Une clôture sans gates verts est une tâche non terminée — la règle devient contrainte ici.

Sur cet hôte, ces règles ne sont pas opposables : rien n'intercepte un appel
d'outil ni une fin de tour. Elles tiennent par discipline, et par la CI.

Avant toute conclusion de tâche :

```bash
grimoire standard gate check --strict
grimoire standard verify .
```

Une clôture sans gates verts est une tâche non terminée.
