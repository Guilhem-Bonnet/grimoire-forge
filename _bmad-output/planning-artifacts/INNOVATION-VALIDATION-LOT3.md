# Validation Innovation — LOT 3 : TIER 3 MOONSHOTS (32 idées)

> **Même framework de scoring** : F×2 + V×3 + U×2 + S×1 + C×1 + R×1 + D×2 = max 60
> **Note** : Les moonshots sont évalués avec une tolérance plus haute sur la faisabilité (vision long terme) mais exigence plus haute sur l'unicité et la différenciation.

---

## Évaluation complète des 32 Moonshots

---

## #30 — Quantum superposition (branches parallèles)

**Concept** : Explorer N branches d'implémentation simultanément et "collapser" sur la meilleure au moment de la décision.

**Challenge** : Le session branching existant fait déjà ça. La "superposition" implique que les branches sont évaluées SIMULTANÉMENT par des critères objectifs et la meilleure est sélectionnée automatiquement. La différence : session branching = choix humain. Quantum = choix algorithmique.

**Challenge technique** : Pour comparer N implémentations, il faut des métriques objectives comparables (perf, coverage, complexity). Faisable pour du code, difficile pour des artefacts de design.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 2 | 4 | 4 | 1 | 4 | 2 | 4 | **38** 🟡 |

**Verdict : 🟡 Extension avancée de Session Branching — `session-branch --compare --auto-select`**
**Effort** : 5-7j | **Dépendances** : Session Branching, métriques de comparaison

---

## #31 — Edge AI / Fog Computing

**Concept** : Agents légers locaux (décisions rapides, lint, pre-checks) + agents lourds cloud/puissants (analyse profonde, review complète).

**Challenge** : Intéressant mais viole la contrainte zero-cloud du kit. En version locale-only : "agents légers" = prompts courts pour System 1, "agents lourds" = prompts complexes avec [THINK] pour System 2. C'est #15 reformulé.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 2 | 3 | 2 | 1 | 2 | 2 | 2 | **25** ❌ |

**Verdict : ❌ REJETÉ — Redondant avec Plan/Act/Think existant, viole zero-cloud**

---

## #36 — WebAssembly agents

**Concept** : Agents sandboxés, portables, cross-platform via Wasm.

**Challenge** : Les agents BMAD sont des fichiers MD, pas des programmes exécutables. Wasm est pour l'exécution de code, pas pour des prompts. Mauvaise correspondance paradigme.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 1 | 2 | 3 | 1 | 1 | 2 | 2 | **21** ❌ |

**Verdict : ❌ REJETÉ — Paradigme incompatible**

---

## #39 — Nombre de Dunbar

**Concept** : Limiter la taille des modules/agents interconnectés à un nombre cognitif optimal.

**Challenge** : C'est une bonne RÈGLE mais pas une feature. Inscrite comme guideline dans la documentation architecture.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 2 | 2 | 5 | 3 | 5 | 2 | **35** 🟡 |

**Verdict : 🟡 Guideline dans la documentation — "Max 15 agents par team, max 7 modules par projet"**
**Effort** : 0.5j (documentation)

---

## #46 — Open Source Governance

**Concept** : Gouvernance méritocratique des contributions aux modules BMAD.

**Challenge** : Nécessite une communauté qui n'existe pas encore. Prématuré. Mais utile de PRÉPARER les mécanismes (voting, proposals, contribution guidelines) pour le jour où la communauté émerge.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 2 | 3 | 2 | 2 | 3 | 3 | **30** 🟠 |

**Verdict : 🟠 EN SURSIS — Préparer CONTRIBUTING.md avancé pour future communauté**
**Effort** : 1j

---

## #47 — Guildes inter-projets

**Concept** : Des guildes d'agents spécialisés qui partagent des standards de qualité entre projets.

**Challenge** : Extension naturelle du Mycelium (#2). Les guildes sont des "channels" thématiques dans le réseau Mycelium. Pas un concept séparé.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 2 | 3 | 3 | 1 | 3 | 3 | 3 | **31** 🟠 |

**Verdict : 🟠 Fusionné avec #2 (Mycelium) — feature "channels/guilds" dans le réseau**

---

## #49 — Rogers — Diffusion d'innovations

**Concept** : Rollout features par catégorie d'adopteurs (innovators → early adopters → majority).

**Challenge** : Utile quand on a des utilisateurs. C'est du product management, pas une feature technique. Le Crescendo (#75) adresse le même besoin côté individu.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 2 | 2 | 3 | 2 | 4 | 2 | **28** 🟠 |

**Verdict : 🟠 Fusionné avec #75 (Crescendo) pour l'onboarding progressif**

---

## #64 — Synesthésie (visualisation multi-modale)

**Concept** : Voir le code comme de la musique, entendre l'architecture. Visualisations qui croisent les sens.

**Challenge technique** : Fascinant conceptuellement mais impraticable dans un terminal CLI. Seul aspect faisable : des visualisations ALTERNATIVES du même artefact (graphe, tableau, narration, Mermaid).

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 2 | 3 | 4 | 1 | 2 | 3 | 3 | **31** 🟠 |

**Verdict : 🟠 Le sous-concept "multi-modal views" est fusionné avec #133 (Perspective) et #56 (Dashboard)**

---

## #65 — Kinesthésie

**Concept** : "Sentir" la structure du code. Retour haptique sur la santé du projet.

**Challenge** : Même problème que #64. Sans hardware, on ne peut pas faire du haptique. Mais on peut faire des INDICATEURS VISUELS (couleurs, emojis) qui créent des réactions émotionnelles similaires.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 2 | 2 | 3 | 1 | 2 | 3 | 2 | **25** ❌ |

**Verdict : ❌ REJETÉ — Impraticable dans le contexte actuel. L'aspect émoji/couleurs est déjà dans le dashboard.**

---

## #71 — Harmonie/Dissonance

**Concept** : Détecter les "dissonances" architecturales — décisions contradictoires, patterns incompatibles, coupling incohérent.

**Challenge** : Le memory-lint détecte certaines contradictions. L'extension serait un "architecture harmony check" qui vérifie la cohérence entre patterns utilisés. Ex: "Tu utilises Repository Pattern pour le module A mais Active Record pour le module B — dissonance ?".

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 4 | 4 | 2 | 4 | 3 | 4 | **42** 🟡 |

**Verdict : 🟡 VALIDÉ — "Architecture Harmony Check" intégré au code-review workflow**
**Effort** : 3j | **Dépendances** : memory-lint, code-review workflow

---

## #72 — Improvisation Jazz

**Concept** : Agents qui improvisent intelligemment hors script quand le contexte l'exige.

**Challenge** : C'est essentiellement un agent avec des guardrails assouplis pour les cas non couverts. Risqué — un agent "jazz" pourrait diverger dangereusement. Mais avec les bons guardrails (jamais improviser sur la sécurité, le CC, les tests), ça pourrait accélérer les cas edge.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 3 | 3 | 2 | 3 | 2 | 3 | **34** 🟠 |

**Verdict : 🟠 EN SURSIS — Concept intéressant mais risqué. Pourrait être un mode `--experimental` opt-in.**

---

## #76 — Contrepoint (Bach)

**Concept** : Threads d'agents parallèles qui convergent harmonieusement.

**Challenge** : C'est le boomerang orchestration reformulé avec de la poésie. Pas de valeur additionnelle vs l'existant.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 2 | 1 | 3 | 3 | 3 | 1 | **26** ❌ |

**Verdict : ❌ REJETÉ — Redondant avec boomerang orchestration**

---

## #80 — Gödel (Incomplétude)

**Concept** : Le système ne peut pas se valider lui-même de l'intérieur. Méta-agents externes.

**Challenge** : Philosophiquement vrai. En pratique : c'est l'adversarial review existant + le second opinion (#223). Un agent dédié "external validator" qui reviewe les outputs du système entier. Mais c'est le MÊME LLM, donc techniquement pas externe.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 2 | 3 | 4 | 1 | 3 | 2 | 4 | **34** 🟠 |

**Verdict : 🟠 Le concept renforce l'idée de faire le code-review avec un AUTRE LLM. Guideline plutôt que feature.**

---

## #84 — Topologie (invariants)

**Concept** : Identifier les propriétés qui ne changent pas sous déformation — les invariants du projet.

**Challenge** : Concrètement, c'est le "Out of Scope" (#131) + les contraintes non-négociables du PRD. Les invariants sont les PRINCIPES qui survivent aux pivots. Déjà couvert.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 2 | 2 | 4 | 3 | 4 | 2 | **30** 🟠 |

**Verdict : 🟠 Fusionné avec #131 (Espace négatif) — section "Project Invariants" dans project-context**

---

## #85 — Nombre d'or (ratios optimaux)

**Concept** : Ratios optimaux entre code/tests, features/tech-debt, planning/exécution.

**Challenge** : Intéressant mais les ratios optimaux dépendent du contexte (startup ≠ enterprise ≠ OSS). Des GUIDELINES avec des ranges plutôt que des ratios fixes.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 3 | 3 | 3 | 3 | 3 | 3 | **36** 🟡 |

**Verdict : 🟡 Guidelines "ratio santé" dans le dashboard (#56). Ex: code/test ratio, feature/debt ratio.**
**Effort** : 1j (métriques dans dashboard)

---

## #86 — Intrication quantique (sync instantanée)

**Concept** : Quand un agent apprend quelque chose, tous les autres le savent instantanément.

**Challenge** : C'est le shared-context.md existant. La "sync instantanée" est ce que le shared-context fait DÉJÀ — c'est la source de vérité commune. Le challenge est la FRAÎCHEUR (est-il à jour ?), pas la sync.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 3 | 1 | 4 | 4 | 4 | 1 | **33** 🟠 |

**Verdict : 🟠 Amélioration du shared-context : auto-update systématique à chaque changement d'état.**

---

## #87 — Heisenberg (trade-off quoi/quand)

**Concept** : Formaliser le trade-off : plus on détaille le "quoi", moins on contrôle le "quand".

**Challenge** : C'est une vérité de project management, pas une feature implémentable. Guideline dans la documentation.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 2 | 2 | 5 | 2 | 4 | 2 | **30** 🟠 |

**Verdict : 🟠 Guideline dans documentation PM. Pas de feature technique.**

---

## #88 — Relativité du temps (pondération temporelle)

**Concept** : Une heure de dette technique "pèse" plus qu'une heure de feature en termes d'impact futur.

**Challenge** : Le concept est juste. Implémentation pratique : dans les estimations, appliquer un multiplicateur pour la dette technique. "1h de dette = 3h d'impact futur." Intégrable dans le triage (#218).

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 3 | 3 | 4 | 3 | 4 | 3 | **39** 🟡 |

**Verdict : 🟡 Multiplicateur de dette technique dans les estimations. Extension du triage.**
**Effort** : 0.5j

---

## #89 — Trou noir informationnel

**Concept** : Préserver TOUTE l'information critique pour qu'elle ne disparaisse jamais.

**Challenge** : C'est l'objectif du système de mémoire existant (shared-context + learnings + failure museum + BMAD_TRACE). L'amélioration : un audit de "risque de perte d'information" dans le NSO.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 3 | 2 | 3 | 4 | 4 | 2 | **35** 🟡 |

**Verdict : 🟡 Audit "information loss risk" dans NSO. Détecte : docs manquantes, décisions non loguées, savoir tribal non capturé (#91).**
**Effort** : 1j | Fusionné avec #91 (Matière noire)

---

## #90 — Big Bang cosmique

**Concept** : Les projets passent par des ères : naissance (idée), inflation (prototype), expansion (scale).

**Challenge** : C'est la succession écologique (#139) avec un autre nom. Fusionner.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 2 | 1 | 4 | 3 | 4 | 1 | **28** ❌ |

**Verdict : ❌ REJETÉ — Redondant avec #139 (Succession écologique)**

---

## #93 — Dualité onde-particule

**Concept** : Le code comme artefact ET comme processus simultanément.

**Challenge** : Trop abstrait. Pas d'implémentation concrète identifiable.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 1 | 2 | 3 | 1 | 2 | 3 | 2 | **23** ❌ |

**Verdict : ❌ REJETÉ — Trop abstrait**

---

## #94 — Entropie thermodynamique

**Concept** : Mesurer l'entropie croissante du codebase et appliquer de l'énergie (refactoring) AVANT le point critique.

**Challenge** : Excellent concept. L'entropie peut être mesurée par : (1) complexité cyclomatique croissante, (2) couplage inter-modules en hausse, (3) ratio de code commenté, (4) divergence entre docs et réalité. Le early-warning (#48) peut inclure cette métrique.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 4 | 3 | 2 | 4 | 3 | 4 | **40** 🟡 |

**Verdict : 🟡 "Entropy score" comme métrique dans early-warning (#48) et dashboard (#56)**
**Effort** : 2j | Part de #48

---

## #157-#170 — Batch restant

| # | Concept | Score | Verdict |
|---|---------|-------|---------|
| 157 | Bande-son adaptative | 28 | ❌ Impraticable en CLI. Aspect "ton adaptatif" couvert par #11 (Camouflage). |
| 160 | Main invisible | 32 | 🟠 Concept philosophique. Le kit est déjà designé pour ça (agents indépendants → optimum collectif). |
| 161 | Externalités | 38 | 🟡 "Side-effect analysis" intégré dans impact-sim (#25). Chaque décision évaluée pour ses externalités. |
| 163 | Arbitrage | 36 | 🟡 Transfert cross-domain via Mycelium (#2). Pattern qui fonctionne en Go transféré à Python. |
| 170 | Feng Shui | 27 | ❌ Trop métaphorique. L'aspect "flow sans blocage" est la bonne architecture, pas une feature. |
| 211 | Boids (Reynolds) | 40 | 🟡 3 règles simples pour agents : (1) cohésion projet, (2) séparation de concerns, (3) alignement sur la vision. Extension de #55 (Fractales). |
| 212 | Automates cellulaires | 34 | 🟠 Paradigme de workflow intéressant mais trop expérimental. R&D pure. |
| 215 | Phase transition | 39 | 🟡 Détection des seuils qualitatifs. Extension early-warning (#48). Ex: "Le projet vient de passer de 'petit' à 'moyen' → recommandations structurelles." |
| 216 | Small-world networks | 35 | 🟡 Architecture max 3 hops. Guideline + vérification dans le graphe (#78). |
| 217 | Loi de puissance | 36 | 🟡 Analytics : identifier les 20% d'agents/workflows qui font 80%. Dashboard (#56). |

---

## Synthèse Tier 3

| Verdict | Nombre |
|---------|--------|
| ✅ Priorité haute | 0 |
| 🟡 Priorité normale | 14 |
| 🟠 En sursis/fusionnées | 9 |
| ❌ Rejetées | 9 |
| **Total** | **32** |

**Conclusion Tier 3** : Aucun moonshot ne justifie un développement standalone immédiat. La majorité des concepts viables sont des EXTENSIONS des features Tier 1 et Tier 2 (dashboard, early-warning, graphe, mycelium). Les concepts purement moonshot (Wasm, haptique, federated ML) sont rejetés comme impraticables.

