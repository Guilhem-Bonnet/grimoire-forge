# Migration Terraform-HouseServer — grimoire-kit 3.38.0 → 3.44.2 (2026-09-11)

Projet : `/mnt/Travail/Projets/Dev/OPS/Terraform-HouseServer` (`$H`, pas un dépôt git).
Outil : `/mnt/Travail/Projets/Dev/Grimoire-Forge/.venv/bin/grimoire` (`$G`), toujours avec
`GRIMOIRE_NO_COCKPIT=1`.

## 1. Sauvegarde (préalable à tout)

- Tarball : `$H/_archive/2026-09-11-pre-3.44.2/grimoire-state.tar.gz` (1,8 Mo, 523 entrées
  tar — fichiers + répertoires — pour 444 fichiers réels sous `_grimoire/`,
  `_grimoire-output/`, `.claude/`, `.github/`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`,
  `.mcp.json`, `project-context.yaml`). Copié dans le scratchpad
  (`homelab-backup/grimoire-state.tar.gz`).
- Manifeste SHA-256 de `_grimoire/_memory/` (32 fichiers) :
  `homelab-backup/memory-manifest-sha256.txt`, copié aussi dans l'archive du projet.
- Vérifié : `tar -tzf ... | wc -l` (523) ≥ nombre de fichiers réels (444, y compris les
  répertoires comptés par `tar`).

**Piège d'outillage rencontré** : la commande `find` de cet environnement (RTK) renvoie une
liste erronée sur `_grimoire/overrides/agents/` (un `README.md` fantôme, le sous-dossier
`_archived/` absent). `/usr/bin/find` (ou `command find`) direct donne le résultat correct.
Tout l'inventaire ci-dessous a été refait avec `/usr/bin/find`/`command find`/`command cat`.

## 2. Inventaire avant

- `grimoire --version` : 3.44.2 (le binaire du venv Forge est déjà à jour ; c'est l'état
  *projet* qui était à 3.38.0).
- `grimoire doctor .` (avant) : **22/22 OK**.
- `grimoire host status` (avant) : **échec bloquant** — garde de distinction
  (« Agents au faisceau identique ») : tous les agents pré-migration (7 infra-ops + 4 meta +
  concierge + fix-loop-orchestrator + vectus) partagent le même triplet (outils, contexte,
  skills) — aucun n'avait de `context:`/`skills:` distinctif. Ce n'était pas un blocage
  nouveau : c'était déjà l'état avant migration, révélé seulement quand `host status`
  applique la garde en mode strict sur des agents en override.
- `grimoire memory status` (avant) : backend `qdrant-server`, 5 entrées, collection
  `grimoire_houseserver`, `sentence-transformers/all-MiniLM-L6-v2` (384d).
- Recherches `k3s` / `longhorn` / `backup` (avant) : les **5** mêmes entrées ressorties à
  chaque fois (scores quasi uniformes, collection trop petite pour discriminer) :
  `7d26ee83…`, `639b65ce…`, `999b3698…`, `432d7a13…`, `55448a59…`.

## 3. Mise à niveau (`up` + `host sync`)

- `grimoire up` (1er passage) : 28 artefacts kit régénérés, 19 fichiers projet préservés,
  identité mise à jour, profil standard `orchestrated` (4 artefacts), doctor interne 7/7.
- `grimoire host sync` : a d'abord **échoué** avec la même garde de distinction (bloquante
  cette fois car des overrides sont en cause) — les 8 agents orphelins (voir plus bas) et
  4 overrides homelab (`ops-engineer`, `monitoring-specialist`, `systems-debugger`,
  `concierge`) sont restés au format 3.37.0-3.38.0 sans `skills:`/`context:`, masquant
  entièrement la nouvelle forme du kit (voir §4).
- Orphelins retirés (le kit 3.44.2 ne livre plus que `ops-engineer`, `monitoring-specialist`,
  `systems-debugger` côté `infra-ops`, et `concierge`, `agent-optimizer`, `security-auditor`
  côté `meta`) : **24 fichiers supprimés** (8 agents × 3 emplacements) :
  `art-director`, `backup-dr-specialist`, `creative-toolsmith`, `k8s-navigator`,
  `memory-keeper`, `pipeline-architect`, `project-navigator`, `security-hardener` — sous
  `_grimoire/kit/agents/`, `.claude/agents/`, `.github/agents/*.agent.md`.
- `grimoire host sync --host all` (après nettoyage + reconstruction des overrides,
  §4) : **succès** sur les 5 hôtes (Claude Code, GitHub Copilot, Codex, Cursor, Gemini CLI).

## 4. Overrides — reconstruction nécessaire (au-delà des 2 cas anticipés)

Constat clé : `_agent_files` (dédup par nom de fichier, override prioritaire sur kit) ne
crée **qu'une seule** entrée par agent. Les overrides `ops-engineer.md`,
`monitoring-specialist.md`, `systems-debugger.md`, `concierge.md` existants (copies
complètes datant de 3.37.0/3.38.0, IP/hostnames en dur, sans `skills:`/`context:`)
masquaient donc *entièrement* la nouvelle forme livrée par le kit 3.44.2 — la migration
« généraliste + skills » n'aurait eu aucun effet réel sans les retoucher. Ce n'était pas
prévu dans les deux cas nommés (vectus, workflow-closed-loop-fix) ; j'ai appliqué le même
principe (« si la garde rejette, corriger a minima et le dire ») à l'ensemble des overrides
réellement en cause :

- **Reconstruits depuis le nouveau kit** (structure/skills 3.44.2 conservés intégralement) +
  réglages `model_affinity` homelab préexistants ré-appliqués + `context:` ajouté :
  `ops-engineer.md`, `monitoring-specialist.md`, `systems-debugger.md`, `concierge.md`.
  Les exemples à IP figées de l'ancien `ops-engineer.md` (3.37.0) ont été abandonnés — déjà
  périmés (LXC 217/219, VM 218 absents) face à `network-topology.md`, désormais chargé via
  `context:`.
- **Context ajouté** (aucune base homelab à préserver) : `agent-optimizer.md` (nouvel
  override, n'existait pas).
- **Frontmatter minimal ajouté** (`use_when`/`dont_use_when`/`tools`/`context:`), comme
  anticipé dans la consigne : `vectus.md`, `fix-loop-orchestrator.md`.
- **Déplacés, jamais supprimés**, vers `_grimoire/overrides/agents/_retired-3.44.2/`
  (avec un `README.md` explicatif) : `art-director.md`, `backup-dr-specialist.md`,
  `k8s-navigator.md`, `pipeline-architect.md`, `security-hardener.md` — leurs bases kit ont
  disparu (capacités reprises comme skills sur `ops-engineer`, ou simplement retirées côté
  meta) ; laissés en place dans `agents/` ils restaient collectés comme agents autonomes et
  faisaient échouer la garde. Le glob de collecte n'est pas récursif : les déplacer dans un
  sous-dossier les retire proprement de la collecte sans rien effacer.
- `_grimoire/overrides/README.md` mis à jour pour refléter ce nouvel état (table + section
  « Ingestion mémoire »).

**Anomalie non liée à mon travail** : `_grimoire/overrides/agents/_archived/README.md`
préexistant, dont le contenu (mentions BMAD/meta-repo Grimoire-kit) n'a aucun rapport avec ce
projet homelab — contamination antérieure (datée du 21 avril 2026), non touchée.

## 5. Ingestion mémoire dans le nouvel archétype

Chemins `context:` déclarés (frontmatter), validés à l'existence par
`grimoire.hosts.collect.collect_agents` et confirmés lus dans les fichiers émis sous
`$H/.claude/agents/*.md` :

| Agent | `context:` |
|---|---|
| `ops-engineer` (généraliste infra-ops) | `agent-learnings/{infra-ops,k8s-gitops,backup-dr,security,cicd,migration-checklist}.md`, `decisions-log.md`, `failure-museum.md`, `network-topology.md`, `shared-context.md` |
| `monitoring-specialist` | `agent-learnings/monitoring.md`, `network-topology.md`, `shared-context.md` |
| `systems-debugger` | `agent-learnings/systems-debug.md`, `failure-museum.md`, `network-topology.md`, `shared-context.md` |
| `agent-optimizer` | `agent-learnings/{memory-quality,agent-quality,project-knowledge}.md` |
| `fix-loop-orchestrator` | `agent-learnings/fix-loop-patterns.md`, `agent-learnings/meta-review/workflow-meta-improvements.md` |

Les 13 fiches `agent-learnings/*.md` sont donc toutes rattachées. `shared-context.md`
complété d'une section « Migration 2026-09-11 » (kit, archétype refait, table de
correspondance overrides retirés → skills, emplacement des fiches).

## 6. Mémoire opérationnelle

- `_grimoire/_memory/config.yaml` : en-tête mis à jour (3.38.0 → 3.44.2, date) ; les 4
  champs conservés à l'identique — ce fichier n'est régénéré qu'à `grimoire init`
  (tier "seed") et n'est lu par aucun schéma strict trouvé dans le code du kit installé
  (recherche dans `grimoire.core.scaffold` / `grimoire.memory`) : aucune perte de champ,
  comparé à un `grimoire init --archetype infra-ops` jetable (`HOME` temporaire).
- `grimoire memory reindex-lexical` : 5 entrées réindexées dans le compagnon lexical.
- Recherches `k3s` / `longhorn` / `backup` (après) : **les 5 mêmes entrées**, identiques à
  l'avant-migration — aucune régression.
- `memories.json` (4 entrées) et `palace_sidecar.sqlite3` : **inchangés** (SHA-256 identique)
  et lus avec succès par `grimoire memory recall`/`list`.

## 7. Preuve finale

- `sha256sum -c` du manifeste (32 fichiers `_grimoire/_memory/`) : **3 écarts, tous
  attendus et expliqués** — `config.yaml` (en-tête version), `grimoire_houseserver_lexical.sqlite3`
  (réindexation), `shared-context.md` (section Migration). Les 29 autres fichiers, dont
  `memories.json` et `palace_sidecar.sqlite3`, sont bit-à-bit identiques.
- `grimoire doctor .` (après) : **22/22 OK**, plus aucun FAIL (deux FAIL intermédiaires
  rencontrés et résolus, voir §8).
- Hook SessionStart rejoué (`grimoire-hook --host claude --event SessionStart`) : réponse
  JSON propre (`hookSpecificOutput.additionalContext`), aucune mention d'erreur.
- `grimoire host status` (après) : `Claude Code à jour`, plus d'erreur de garde de
  distinction, persona d'entrée `concierge`.
- `grimoire registry dispatches` : agent `concierge` (1 occurrence, issue du hook rejoué),
  aucun non-choix, agents trop récents (6 j d'historique) pour juger de leur fraîcheur.

## 8. Défauts du kit révélés (issue ouverte)

**Grimoire-kit#426** (ouverte) : `grimoire up`, étape `identity`, corrompt systématiquement
un scalaire YAML de `project-context.yaml` porteur d'un commentaire inline —
`skill_level: "expert"  # commentaire` devient `skill_level: ""expert"  # commentaire"`,
ce qui casse ensuite `grimoire doctor .` (`[GR002]` erreur de parsing). Reproduit **deux
fois** pendant cette migration (`up` lancé deux fois), et déjà consigné dans la mémoire du
projet (`failure-museum.md`, `[2026-09-05] [kit 3.38.0]`) lors d'une migration précédente —
régression non corrigée depuis au moins deux versions du kit. Corrigé manuellement à chaque
occurrence (restauration de la ligne). Contournement documenté dans l'issue : relire le
diff de `project-context.yaml` après chaque `grimoire up`.

Un second symptôme lié (non-bug, comportement attendu documenté dans le code) : la carte
`<agents>` intégrée au corps de `concierge.md` est régénérée par `grimoire up` à partir du
roster *au moment de l'exécution* — comme j'ai supprimé les orphelins **après** le premier
`up`, la carte contenait encore les 5 agents retirés et faisait échouer le check
`roster_coherent` de `doctor`. Un second `grimoire up` (après suppression des orphelins)
l'a régénérée correctement ; l'override `concierge.md` a été reconstruit une seconde fois
depuis cette version propre.

## 9. Fichiers clés

- Sauvegarde : `$H/_archive/2026-09-11-pre-3.44.2/grimoire-state.tar.gz` +
  `memory-manifest-sha256.txt` (aussi dans le scratchpad `homelab-backup/`).
- Overrides modifiés : `$H/_grimoire/overrides/agents/{ops-engineer,monitoring-specialist,
  systems-debugger,concierge,agent-optimizer,vectus,fix-loop-orchestrator}.md`,
  `$H/_grimoire/overrides/README.md`.
- Overrides retirés (déplacés) : `$H/_grimoire/overrides/agents/_retired-3.44.2/` (+ README).
- Mémoire : `$H/_grimoire/_memory/config.yaml`, `shared-context.md`.
- Config projet corrigée : `$H/project-context.yaml` (bug kit + sections commentaires
  obsolètes mises à jour).
- Issue kit : https://github.com/Guilhem-Bonnet/Grimoire-kit/issues/426
