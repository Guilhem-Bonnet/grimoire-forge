# Cahier des Charges — Grimoire Game Board

> Projet : **Grimoire Game** — Board de configuration d'agents gamifié
> Version : 1.1 — Avril 2026
> Statut : Planification active
> Document produit par : BMad Master + Analyst + PM (multi-agent collaboration)

---

## 1. Vision et objectifs

### 1.1 Vision

Grimoire Game est un environnement de travail **gamifié** dans lequel des agents IA collaborent au sein d'un espace de type *openspace* en pixel art. L'utilisateur peut observer, orchestrer, configurer et interagir avec ses agents comme s'il jouait à un jeu vidéo de gestion (SimCity, The Sims, Stardew Valley rencontrent VS Code et Gather.town).

L'objectif fondamental : rendre la collaboration multi-agent **visible, compréhensible, contrôlable** et **agréable** à utiliser, en s'éloignant définitivement du paradigme du terminal/chat opaque.

### 1.2 Objectifs stratégiques

- **O1** — Centraliser toute la configuration des agents (MCP, skills, prompts, tools, hooks) dans une interface gamifiée unique.
- **O2** — Rendre le travail parallèle des agents visible en temps réel via des animations et des indicateurs d'état.
- **O3** — Faciliter la communication inter-équipes via un système de pièces dédiées avec des agents communiquants.
- **O4** — Permettre la création, le clonage et la configuration d'agents directement depuis le board.
- **O5** — Intégrer un cycle agile complet (Kanban, sprint, challenge, livraison) entièrement gamifié.
- **O6** — S'intégrer nativement dans grimoire-kit à l'installation.
- **O7** — Concevoir le bridge agents comme agnostique via une interface `AgentAdapter`, permettant la connexion future à d'autres systèmes (Claude Code, Codex, OpenCode, Gemini CLI) sans refactoring du cœur.

### 1.3 Périmètre

Le projet couvre :

1. Le moteur de jeu pixel art (renderer, cartes, personnages, animations)
2. Le système de gestion d'agents (création, configuration, état, mémoire)
3. Les espaces dédiés par teams (openspaces, salles de réunion, salle de contrôle)
4. Le gestionnaire de tâches gamifié (Kanban visuel in-world)
5. Le système de communication inter-agents (bulles, mouvements, handoffs)
6. La visualisation des workflows et chemins de décision
7. La console de debug gamifiée
8. La salle de challenge (présentation, critique, validation)
9. L'interface de configuration (MCP, skills, tools, hooks, prompts)
10. La visualisation du système mémoire (RAM, long-term, Qdrant)
11. L'orchestrateur comme agent spécial avec salle de contrôle
12. L'intégration VS Code (telemetry, debug, extensions)

---

## 2. Parties prenantes et utilisateurs

### 2.1 Utilisateurs primaires

| Persona | Description | Besoins clés |
|---|---|---|
| **Développeur AI** | Crée et orchestre des agents pour automatiser du travail | Vision globale de l'état, debug facilité, config rapide |
| **Chef de projet technique** | Supervise un workflow multi-agent | Suivi des tâches, état des équipes, qualité de sortie |
| **Chercheur AI** | Expérimente avec des architectures multi-agent | Observabilité fine, reproduction d'expériences |
| **Débutant AI** | Découvre les agents IA | Onboarding guidé, interface intuitive |

### 2.2 Agents (utilisateurs internes)

Chaque agent est un utilisateur interne du système. Ils ont des profils, des expertises, une mémoire, et interagissent avec le board via leur état observable.

---

## 3. Exigences fonctionnelles

### 3.1 F01 — Moteur de jeu pixel art

- **F01.1** Le système DOIT afficher un openspace 2D top-down en pixel art (style 16x16 ou 32x32 tiles).
- **F01.2** La carte DOIT être éditable via un éditeur intégré (furniture, floors, walls) avec : undo/redo 50 niveaux (Ctrl+Z / Ctrl+Y), grille extensible jusqu'à 64×64 tiles, et chargement d'asset packs externes via le format manifest-based (`manifest.json` par item).
- **F01.3** Le moteur DOIT supporter plusieurs salles (rooms) liées entre elles.
- **F01.4** Les personnages DOIT pouvoir se déplacer via pathfinding BFS/A*.
- **F01.5** Le moteur DOIT supporter des animations par état (idle, walk, type, think, read, talk, search, code, celebrate, confused...).
- **F01.6** Le renderer DOIT fonctionner à 60fps sur canvas HTML5.

### 3.2 F02 — Espaces dédiés par team

- **F02.1** Chaque Team DOIT avoir sa propre pièce (openspace dédié ou espace de travail séparé).
- **F02.2** Les pièces DOIVENT être visualisées avec des décorations représentant le domaine de la team (tech = screens et code, creative = tableaux, etc.).
- **F02.3** Une salle de réunion DOIT exister pour les conférences inter-teams.
- **F02.4** L'orchestrateur DOIT avoir une salle de contrôle dédiée (« war room »).
- **F02.5** Les couloirs entre pièces DOIVENT être navigables.
- **F02.6** Un agent PEUT visiter la pièce d'une autre team s'il en a l'autorisation.

### 3.3 F03 — Représentation des agents

- **F03.1** Chaque agent DOIT avoir un sprite de personnage unique (ou personnalisable).
- **F03.2** Chaque agent DOIT afficher son état actuel via une animation dédiée.
- **F03.3** Cliquer sur un agent DOIT ouvrir sa fiche détaillée (nom, rôle, modèle, prompt, tools, mémoire, workflow en cours).
- **F03.4** Chaque agent DOIT avoir une barre d'état (santé = tokens restants, stamina = latence).
- **F03.5** Les bulles de dialogue DOIVENT afficher le résumé des conversations.
- **F03.6** Les sous-agents DOIVENT apparaître liés à leur agent parent (lien visuel).
- **F03.7** L'agent orchestrateur DOIT avoir une apparence distincte et un badge « ORCH ».

### 3.4 F04 — Système de tâches Kanban gamifié

- **F04.1** Un Kanban in-world DOIT exister par team (affiché sur un tableau dans la pièce).
- **F04.2** Les colonnes DOIVENT être : Backlog → Todo → In Progress → Review → Done.
- **F04.3** Les tâches DOIVENT pouvoir être assignées à des agents via drag & drop.
- **F04.4** L'état d'une tâche DOIT se mettre à jour automatiquement en fonction de l'activité de l'agent concerné.
- **F04.5** Un tableau de bord global DOIT exister pour suivre toutes les teams.
- **F04.6** Les tâches DOIVENT pouvoir contenir : titre, description, prompt préconstruit, agent assigné, priorité, dépendances, type (bug | feature | infra | doc | research | test | refactor | security | design).
- **F04.7** Les agents DOIVENT pouvoir créer de nouvelles tâches automatiquement (discovery).

### 3.5 F05 — Communication inter-agents

- **F05.1** Chaque team DOIT avoir un agent « Team Lead/Communicant » capable de se déplacer vers d'autres teams.
- **F05.2** Les messages entre agents DOIVENT être visualisés (bulles, lignes de connexion animées).
- **F05.3** L'agent communicant DOIT pouvoir se déplacer physiquement vers une autre pièce pour transmettre un message.
- **F05.4** Les teams leads DOIVENT pouvoir déclencher une réunion inter-teams dans la salle de réunion.
- **F05.5** Les canaux de communication DOIVENT être loggés et consultables.
- **F05.6** Un système de broadcast DOIT permettre à l'orchestrateur d'envoyer un message à toutes les teams.

### 3.6 F06 — Connaissances et mémoire des agents

- **F06.1** Chaque agent DOIT avoir une mémoire visualisée (icône livre/cerveau sur son bureau).
- **F06.2** La mémoire active DOIT apparaître comme des fichiers sur le bureau de l'agent.
- **F06.3** La mémoire long-terme (Qdrant/vector store) DOIT être visible dans une bibliothèque dédiée.
- **F06.4** L'utilisation de la mémoire DOIT déclencher une animation (agent qui lit/écrit dans un livre).
- **F06.5** Le background/persona de chaque agent DOIT être configurable et visible dans sa fiche.

### 3.7 F07 — Parallélisme et exécution simultanée

- **F07.1** Le système DOIT permettre l'exécution simultanée de N agents (pas de limite artificielle).
- **F07.2** L'interface DOIT montrer visuellement quels agents travaillent en parallèle (bandes dashed visuelles).
- **F07.3** Un panel de contrôle DOIT permettre de démarrer/arrêter/mettre en pause des agents.
- **F07.4** Les conflits de ressources DOIVENT être détectés et affichés (agent bloqué = animation « wait »).

### 3.8 F08 — Visualisation des workflows

- **F08.1** Les workflows DOIVENT être représentés comme des chemins visuels sur la carte.
- **F08.2** Le chemin emprunté par un workflow DOIT être mis en évidence (couleur, animation).
- **F08.3** Cliquer sur un agent en cours de workflow DOIT afficher sa position dans le diagramme.
- **F08.4** L'historique des décisions DOIT être visible sur demande.
- **F08.5** La vue « workflow » DOIT pouvoir remonter la chaîne des agents qui ont contribué à une tâche.

### 3.9 F09 — Console de debug gamifiée

- **F09.1** Une console de debug DOIT exister sous forme d'un objet 3D en jeu (grand écran, terminal).
- **F09.2** Les logs DOIVENT être filtrables par agent, type d'événement, criticité.
- **F09.3** Les erreurs DOIVENT déclencher une animation distincte sur l'agent concerné (point d'exclamation rouge, animation panic).
- **F09.4** Les avertissements HUP (hallucinations) DOIVENT être visibles comme des alertes visuelles.
- **F09.5** Le journal de tous les tool calls DOIT être consultable avec highlighting syntaxique.

### 3.10 F10 — Salle de challenge (Review Room)

- **F10.1** Une salle dédiée au challenge DOIT exister.
- **F10.2** Un workflow de présentation DOIT orchestrer : Live demo → Questions → Critiques → Vote → Itération.
- **F10.3** Tous les agents DOIVENT pouvoir participer (même si pas directement impliqués).
- **F10.4** Les agents challengeurs DOIVENT pouvoir « prendre la parole » (animation + bulle).
- **F10.5** Les résultats du challenge DOIVENT être loggés et créer des tâches de correction.
- **F10.6** Un score de qualité DOIT être calculé après chaque challenge.

### 3.11 F11 — Créateur d'agents (Agent Factory)

- **F11.1** Une interface gamifiée DOIT permettre de créer un agent (nom, persona, tools, modèle, prompt).
- **F11.2** L'orchestrateur DOIT pouvoir cloner un agent existant.
- **F11.3** Les agents créés DOIVENT apparaître dans la room appropriée après création.
- **F11.4** Un template de personnage DOIT pouvoir être assigné à l'agent créé.

### 3.12 F12 — Interface de configuration gamifiée

- **F12.1** Tous les éléments de config (MCP, skills, prompts, tools, hooks) DOIVENT être configurables via UI.
- **F12.2** La configuration MCP DOIT être visualisée comme des « portails » ou « connexions réseau ».
- **F12.3** Les skills DOIVENT être représentés comme des cartes de compétences (RPG skill tree).
- **F12.4** Les prompts DOIVENT être éditables in-line via un modal avec highlighting.
- **F12.5** Les hooks DOIVENT apparaître comme des déclencheurs/capteurs dans la pièce.
- **F12.6** La config DOIT être persistée et synchronisée avec grimoire-kit.

### 3.13 F13 — Orchestrateur spécial

- **F13.1** L'orchestrateur DOIT avoir une interface unique pour casser le 4ème mur (dialogue direct avec l'utilisateur).
- **F13.2** L'orchestrateur DOIT pouvoir naviguer librement entre toutes les rooms.
- **F13.3** L'orchestrateur DOIT avoir sa salle de contrôle (vue globale, monitoring, dispatch).
- **F13.4** L'orchestrateur DOIT être le seul à pouvoir créer/modifier/supprimer d'autres agents.
- **F13.5** L'orchestrateur DOIT analyser le fonctionnement global et proposer des optimisations.
- **F13.6** L'orchestrateur DOIT naviguer sur le web pour veiller sur les innovations agentiques.
- **F13.7** L'orchestrateur DOIT rôle de prompt engineer (traduire les demandes utilisateur en prompts structurés).

### 3.14 F14 — Intégration grimoire-kit

- **F14.1** Le board DOIT s'installer via `grimoire.sh setup`.
- **F14.2** Le board DOIT se lancer en tant que serveur local (port configurable, défaut 8765).
- **F14.3** Le board DOIT intégrer l'observatory.html en lecture seule via iframe sandbox (bouton `[📡 Obs]` dans le header, décision ADR-GAME-005 — pas de migration de données).
- **F14.4** La config grimoire (`_bmad/bmm/config.yaml`) DOIT être lue et exposée via UI.
- **F14.5** Les agents BMAD existants DOIVENT être automatiquement importés.

### 3.15 F15 — Intégration VS Code (optionnel)

- **F15.1** Une webview panel DEVRAIT pouvoir être ouverte depuis VS Code.
- **F15.2** La télémétrie VS Code (extensions, performance, diagnostics) DEVRAIT être visible dans le board.
- **F15.3** Les commandes VS Code DEVRAIENT être accessibles depuis le board.

### 3.16 F16 — Système sonore

- **F16.1** Un système de feedback audio DOIT exister avec des sons distincts par type d'événement.
- **F16.2** Tous les sons DOIVENT être désactivables individuellement (SFX / Musique d'ambiance).
- **F16.3** Un contrôle de volume global DOIT être accessible depuis le HUD.
- **F16.4** La musique d'ambiance DOIT varier selon la room active.

### 3.17 F17 — Progression et XP gamifiés

- **F17.1** Le système DOIT attribuer automatiquement des points d'XP aux agents selon leurs actions.
- **F17.2** Une barre d'XP DOIT être visible pour chaque agent.
- **F17.3** Des achievements DOIVENT être débloquables et affichés via notification temporaire.
- **F17.4** Les données de progression DOIVENT être persistées (SQLite).

### 3.18 F18 — Tutoriel d'onboarding

- **F18.1** Un tutoriel interactif en 5 étapes DOIT s'afficher automatiquement au premier démarrage.
- **F18.2** Le tutoriel DOIT être ignorable à tout moment via un bouton [Skip].
- **F18.3** Le tutoriel NE DOIT PAS se relancer après la première complétion ou skip.
- **F18.4** Le tutoriel DOIT guider l'utilisateur vers les 5 actions fondamentales du board.

### 3.19 F19 — Mode spectateur (lecture seule partageable)

- **F19.1** Un mode spectateur DEVRAIT permettre à un utilisateur secondaire de visualiser le board en lecture seule.
- **F19.2** L'accès spectateur DEVRAIT utiliser un token distinct (read-only) généré depuis le HUD (Settings > Share).
- **F19.3** Le spectateur NE DOIT PAS pouvoir modifier les agents, tâches, ou la configuration.
- **F19.4** L'URL d'accès spectateur DEVRAIT être copiable en 1 clic depuis le HUD.

### 3.20 F20 — Vue de rétrospective gamifiée (Retro Room)

- **F20.1** Une Retro Room DOIT exister pour visualiser les métriques de sprint hebdomadaires (commits, LOC, tests, vitesse de livraison).
- **F20.2** Un tweetable summary DOIT s'afficher en tête : commits, LOC net, test ratio, shipping streak (jours consécutifs de livraison par l'équipe d'agents).
- **F20.3** Un classement par agent DOIT afficher les contributions (commits assignés, tâches terminées, XP gagné), avec éloge ancré sur les données réelles — pas de formules génériques.
- **F20.4** La Retro Room DOIT générer un JSON snapshot archivé dans `.context/retros/` pour comparaison semaine sur semaine (déltas : test ratio, LOC/sprint, focus score, shipping streak).
### 3.21 F21 — Desks as Directories et Deep Inspection

- **F21.1** Un bureau de l’openspace DOIT pouvoir être assigné à un répertoire de travail par drag-and-drop de l’agent vers le bureau. L’assignation change le `cwd` effectif de l’agent et déclenche un déplacement visuel vers ce bureau.
- **F21.2** Une icône de répertoire flottante (ex : `📁 src/server`) DOIT s'afficher au-dessus de chaque bureau assigné.
- **F21.3** Un clic sur un personnage agent DOIT ouvrir un panneau **Deep Inspection** affichant : modèle LLM, branche git active, system prompt (lecture seule + bouton copier), compteur de tokens utilisés / contexte total, outil actif en cours, historique des outils de la session. Ce panneau DOIT offrir les actions : Pause, Chat direct, Redirect, Restart.

### 3.22 F22 — Gestion des branches git (Worktree Room)

- **F22.1** Chaque branche git active DOIT générer une **Worktree Room** temporaire accessible depuis la minimap (icône 🌿).
- **F22.2** Un agent travaillant sur une branche DOIT se déplacer visuellement dans la Worktree Room correspondante.
- **F22.3** Lors de la fusion d’une branche (merge / PR validé), une animation de célébration collective (`merge_celebrate`) DOIT se déclencher dans la War Room.
- **F22.4** La Worktree Room DOIT afficher les options de clôture de branche (merge / PR / discard / keep) comme boutons in-world sur un écran mural.

### 3.23 F23 — Plugin Power Cards

- **F23.1** Les plugins Anthropic officiels (`frontend-design`, `code-review`, `security-guidance`) DOIVENT être représentés comme des **Power Cards** activables dans la Library Room (section Skills Shelf).
- **F23.2** L’activation d’une Power Card DOIT déclencher un halo de couleur distinctif + icône du plugin sur l’agent concerné.
- **F23.3** Le statut d’activation de chaque Power Card DOIT être persisté dans la config et visible en tooltip sur le sprite de l’agent.
### 3.24 F24 — Investigation Lab (debug systématique 4 phases)

- **F24.1** Un agent en état DEBUGGING DOIT suivre visuellement les 4 phases de l'Investigation Lab : Root Cause (Ph1), Pattern Analysis (Ph2), Hypothesis (Ph3), Implementation (Ph4).
- **F24.2** Un indicateur de phase (badge HUD « 🔄 Ph1 » … « 🛠️ Ph4 ») DOIT s'afficher sur le sprite de l'agent tant qu'il est en état DEBUGGING.
- **F24.3** La Loi de Fer DOIT être appliquée : si un agent émet un WS `FIX_PROPOSED` sans avoir d'abord logé un `ROOT_CAUSE_IDENTIFIED`, l'UI DOIT afficher un avertissement « ⚠️ Root cause not investigated » et bloquer la transition vers DONE.
- **F24.4** Après 3 tentatives de correctif échouées (3× `FIX_FAILED`), l'Orchestrateur DOIT être notifié avec une alerte « Architecture Review Required ».

### 3.25 F25 — Verification Gate (preuve avant complétion)

- **F25.1** Avant tout passage d'une carte Kanban en « DONE », un événement WS `VERIFICATION_GATE` DOIT être émis : l'agent doit fournir une preuve (exit code 0, test output, nombre de failures = 0).
- **F25.2** Si la preuve est absente, la carte DOIT rester en « REVIEW » et l'agent DOIT recevoir un message « Provide evidence before completion ».
- **F25.3** Un log d'audit des gates (timestamp + preuve agregée + résultat) DOIT être conservé dans `.context/verification-log.jsonl`.

### 3.26 F26 — Dispatch parallèle avec isolation de contexte

- **F26.1** Le système DOIT permettre le dispatch de ≥ 2 agents en parallèle sur des domaines indépendants (isolation de contexte complète : aucun agent n'hérite du contexte de l'agent orchestrateur).
- **F26.2** Chaque dispatch parallèle DOIT être visualisé comme un « Parallel Sprint » dans la War Room : lignes de tether colorées reliant l'orchestrateur à chaque sous-agent.
- **F26.3** Après retour de tous les sous-agents, l'Orchestrateur DOIT vérifier les conflits (fichiers édités simultanément) et afficher un résumé d'intégration avant de fermer les tether cords.

### 3.27 F27 — Cycle de revue de code (Requesting + Receiving)

- **F27.1** Après chaque tâche implémentée, le système DOIT déclencher automatiquement un sous-agent `code-reviewer` avec un contexte auto-suffisant (BASE_SHA / HEAD_SHA / description) — jamais le contexte de la session courante.
- **F27.2** Les findings du reviewer DOIVENT être classés en trois sévérités visuelles : 🔴 Critical (bloque la progression), 🟡 Important (doit être corrigé avant la prochaine tâche), ⚪ Minor (note pour plus tard).
- **F27.3** La réception d'une revue DOIT déclencher un mode « Technical Verification » : l'agent vérifie chaque point contre le codebase réel (YAGNI check, pushback raisonné si le reviewer a tort) — aucun accord performatif (interdit : « You're absolutely right! »).
- **F27.4** Un `Critical` non résolu DOIT bloquer le passage de la carte Kanban vers la colonne suivante.

### 3.28 F28 — Branch Finisher (cérémonial de fin de branche)

- **F28.1** Quand toutes les tâches d'une branche sont complètes, le système DOIT vérifier les tests (`npm test / pytest / go test`) avant de proposer les options de finalisation.
- **F28.2** Le système DOIT présenter exactement 4 options : `[1] Merge local` · `[2] Push + PR` · `[3] Keep as-is` · `[4] Discard`.
- **F28.3** L'option Discard DOIT requérir une confirmation textuelle explicite (saisie du mot `discard`) avant suppression.
- **F28.4** La suppression du worktree DOIT être automatique pour les options 1 et 4 uniquement ; les options 2 et 3 conservent le worktree.

### 3.29 F29 — Security Audit Room (CSO in-game)

- **F29.1** Une salle dédiée « Security Lab » DOIT être disponible dans le HQ, déclenchable via `/cso` (gstack) ou bouton `[🔒 Audit sécu]` dans la War Room.
- **F29.2** L'audit DOIT couvrir OWASP Top 10 + modèle de menace STRIDE, avec un seuil de confiance de 8/10 minimum avant publication d'un finding (zéro bruit : 17 exclusions de faux positifs codifiées).
- **F29.3** Chaque finding publié DOIT inclure un scénario d'exploit concret (« comment un attaquant pourrait exploiter ceci »).
- **F29.4** Les findings DOIVENT être affichés sur le tableau de la Security Lab avec badges de sévérité (CRITICAL / HIGH / MEDIUM / INFO) et créer automatiquement des cartes Kanban `[🔒 Sécu]`.

### 3.30 F30 — Design Forge (synthèse visuelle et DX)

- **F30.1** La Design Room DOIT intégrer les 3 outils gstack : `/design-consultation` (système de design complet depuis zéro), `/design-shotgun` (variantes visuelles côte-à-côte dans le navigateur), `/design-html` (HTML production avec Pretext : texte qui reflow, hauteurs auto).
- **F30.2** Le `/autoplan` DOIT être disponible comme commande one-shot qui enchaîne automatiquement CEO review → design review → eng review, présentant uniquement les décisions de « goût » pour validation humaine.
- **F30.3** Le système DOIT supporter le mode DX Review (`/devex-review`) qui teste réellement l'onboarding : navigation docs, TTHW mesuré, screenshots d'erreurs, comparaison avec les scores `/plan-devex-review`.
---

## 4. Exigences non-fonctionnelles

### 4.1 Performance

| Critère | Valeur cible |
|---|---|
| Rendu canvas | ≥ 60 fps sur hardware moderne |
| Latence message agent→UI | ≤ 200ms |
| Démarrage serveur | ≤ 5 secondes |
| Nombre d'agents simultanés | ≥ 20 sans dégradation |
| Taille bundle JS | ≤ 2 Mo (gzip) |

### 4.2 Accessibilité et compatibilité

- Support navigateurs : Chrome 120+, Firefox 120+, Safari 17+, Edge 120+
- Résolution minimale : 1280×768
- Support mobile : vue lecture seule (pas de configuration)
- Thème sombre natif (défaut), thème clair optionnel

### 4.3 Sécurité

- Toutes les communications WebSocket DOIVENT être authentifiées (token local)
- Pas d'exposition réseau sans configuration explicite
- Les clés API DOIVENT être stockées chiffrées (jamais en clair dans le config)
- Sanitisation de toutes les sorties agent avant affichage (XSS prevention)
- Rate limiting sur les endpoints WebSocket

### 4.4 Maintenabilité

- Architecture modulaire (composants remplaçables)
- Tests unitaires ≥ 80% couverture
- Tests e2e pour les flux critiques (création agent, Kanban, challenge)
- Documentation technique inline (JSDoc/TSDoc)
- Changelog automatique

### 4.5 Extensibilité

- Système de plugins pour les asset packs (sprites, themes)
- API ouverte pour les adaptateurs d'agents externes
- Système de thèmes via CSS custom properties

---

## 5. Contraintes

### 5.1 Contraintes techniques

- Langage principal : **TypeScript** (front + back)
- Rendu : **Canvas 2D** HTML5 (pas WebGL pour la compatibilité maximale)
- Serveur : **Node.js** (WebSocket via ws ou Socket.io)
- Stockage : **SQLite** (défaut) ou **PostgreSQL** (production)
- Framework front : **SvelteKit** (recommandé, voir doc technique) ou React
- Intégration existante : observatory.html supervisé en lecture seule via iframe sandbox (décision ADR-GAME-005 — pas de migration)

### 5.2 Contraintes de projet

- Environnement principal : développement local (pas de cloud natif)
- Auto-hébergeable (self-hosted)
- Open-source (MIT License)
- Compatible grimoire-kit existant (pas de breaking change)

### 5.3 Contraintes UX

- Apprenabilité : un utilisateur sans connaissance du jeu DOIT comprendre le board en < 5 minutes
- Consistency : icons et animations DOIVENT être cohérentes entre tous les états
- Direction artistique : style pixel art 16-bit cohérent sur tout le board

---

## 6. Dépendances et intégrations

### 6.1 Dépendances internes

| Composant | Rôle |
|---|---|
| `grimoire-kit` | Écosystème d'agents source |
| `observatory.html` | Monitoring existant — supervisé en lecture seule via iframe (ADR-GAME-005) |
| `_bmad/bmm/config.yaml` | Config agents BMAD |
| `_bmad/_memory/` | Mémoire agents (à visualiser) |

### 6.2 Dépendances externes

| Outil | Usage | Alternatif |
|---|---|---|
| WebSocket (ws) | Communication temps réel | Socket.io |
| SQLite (better-sqlite3) | Persistance locale | PostgreSQL |
| Canvas 2D HTML5 (custom) | Moteur de jeu | — (aucun framework jeu externe) |
| Zod | Validation de schemas | Yup |
| Vitest | Tests | Jest |
| Playwright | Tests e2e | Cypress |

### 6.3 Références inspirantes

| Projet | Aspect inspirant |
|---|---|
| pixel-agents (pablodelucca) | Animations agents, layout editor, JSONL parsing |
| DeskRPG (dandacompany) | Virtual office, AI NPCs, tasks, meetings |
| WorkAdventure | Architecture multiplayer, microservices |
| Gather.town | UX virtualspace, proximity chat |
| OpenClaw | Gateway WS, Canvas A2UI, session tools |
| superpowers (obra) | Workflow agents: TDD, subagent-driven-dev, challenge review |
| claude-mem (thedotmack) | Architecture mémoire: SQLite+Chroma, lifecycle hooks, web viewer |
| gstack (garrytan) | Design workflow: design-html, design-consultation, cso (OWASP) |

---

## 7. Critères d'acceptation globaux

- [ ] Un utilisateur peut lancer le board et voir ses agents grimoire s'animer dans un openspace
- [ ] Les agents travaillent en parallèle visible avec animations distinctes par action
- [ ] Le Kanban in-world permet de créer/assigner/déplacer des tâches
- [ ] L'orchestrateur peut dialoguer avec l'utilisateur et dispatcher vers les agents
- [ ] La salle de challenge permet une session de review complète avec critique et vote
- [ ] La configuration MCP/skills/tools est accessible et persistée depuis le board
- [ ] Le système de mémoire des agents est visualisé
- [ ] Un nouveau projet grimoire-kit installe automatiquement le board

---

## 8. Roadmap macro

| Version | Scope | Description |
|---|---|---|
| **v0.1 Alpha** | Moteur de base | Canvas, 1 room, N agents animés, WebSocket |
| **v0.2 Beta** | Multi-rooms + Kanban | Openspaces par team, Kanban mural |
| **v0.3** | Communication | Agent communicant, réunions, handoffs visuels |
| **v0.4** | Config + Mémoire | Interface config gamifiée, viz mémoire |
| **v0.5** | Challenge room | Salle de challenge, workflow de review |
| **v0.6 Polish** | Son + XP + Onboarding | Système sonore (Web Audio API), progression XP, achievements débloquables, tutoriel premier démarrage |
| **v1.0 GA** | Intégration complète | Installation grimoire-kit, VS Code optionnel |

---

*Fin du Cahier des Charges — Version 1.1*
