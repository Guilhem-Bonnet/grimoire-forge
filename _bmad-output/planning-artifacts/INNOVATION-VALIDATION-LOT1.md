# Validation Innovation bmad-custom-kit — Processus Complet

> **Date** : 1 mars 2026
> **Méthode** : Multi-agent adversarial validation
> **Input** : 132 idées (45 Tier 1 + 55 Tier 2 + 32 Tier 3)
> **Statut** : EN COURS

---

## Processus de Validation

### Framework d'évaluation — 7 dimensions (score 1-5)

| Dimension | Question clé | Pondération |
|-----------|-------------|-------------|
| **F — Faisabilité** | Peut-on l'implémenter dans le contexte BMAD (fichiers MD/YAML, CLI bash/python, zero cloud) ? | ×2 |
| **V — Valeur utilisateur** | Le dev final ressent-il un bénéfice concret et mesurable ? | ×3 |
| **U — Unicité** | Aucun concurrent (CrewAI, AutoGen, Aider, Cline, Cursor) ne fait ça ? | ×2 |
| **S — Synergie** | Renforce-t-il les features existantes du kit (NSO, stigmergy, darwinism, etc.) ? | ×1 |
| **C — Complexité** | Effort d'implémentation (5=trivial, 1=énorme) | ×1 |
| **R — Risque** | Probabilité d'échec ou d'effets négatifs (5=aucun risque, 1=très risqué) | ×1 |
| **D — Différenciation** | Contribue-t-il au positionnement unique "ecosystem IA local auto-évolutif" ? | ×2 |

**Score pondéré** = F×2 + V×3 + U×2 + S×1 + C×1 + R×1 + D×2 = max 60

### Seuils de décision

| Score | Décision |
|-------|----------|
| 45-60 | ✅ **VALIDÉ — Priorité haute** |
| 35-44 | 🟡 **VALIDÉ — Priorité normale** |
| 25-34 | 🟠 **EN SURSIS — Nécessite un champion ou une fusion** |
| <25 | ❌ **REJETÉ au challenge** |

### Agents évaluateurs

| Agent | Rôle dans le challenge |
|-------|----------------------|
| ⚡ Victor | Avocat du diable stratégique — challenge la valeur business |
| 🔬 Dr. Quinn | Challenge technique — faisabilité et risques |
| 🏗️ Winston | Architecture — cohérence avec le système existant |
| 📋 John | Product — valeur utilisateur réelle |
| 🎨 Maya | UX — le dev va-t-il vraiment l'utiliser ? |
| 📊 Mary | Marché — différenciation compétitive |

---

# LOT 1 — TIER 1 : QUICK WINS (45 idées)

---

## #17 — Attention sélective (Context Router intelligent)

**Concept** : Filtre automatique des fichiers pertinents par tâche. Au lieu de charger tout le contexte, l'agent identifie et charge uniquement les fichiers nécessaires, réduisant le context window de 60%+.

**Challenge ⚡ Victor** : "C'est pas juste un meilleur `.gitignore` ? Quel est le VRAI différenciateur ?"
→ Non. C'est un routage SÉMANTIQUE. Le context router analyse la TÂCHE (story, bug, question) et sélectionne les fichiers par pertinence au contenu, pas par pattern de chemin. Un grep amélioré ne fait pas ça.

**Challenge 🔬 Dr. Quinn** : "Comment calculer la pertinence sans LLM call dédié ?"
→ Approche hybride : (1) analyse statique des imports/dépendances, (2) index de mots-clés par fichier (pré-calculé), (3) heuristiques de proximité (même dossier, même module). Le LLM n'intervient que pour le ranking final.

**Challenge 🏗️ Winston** : "Et si le router exclut un fichier critique ?"
→ Risque réel. Mitigation : mode "conservative" par défaut (inclut plus), mode "aggressive" opt-in. Log des exclusions. Feedback loop : si l'agent demande un fichier exclu, le router apprend.

**Challenge 📋 John** : "Le dev sent-il la différence ?"
→ OUI. Context window limité = le problème #1 de tous les IDE IA. Réduire 60% = plus de place pour le vrai travail. C'est le pain point le plus universel.

**Challenge 🎨 Maya** : "Friction d'usage ?"
→ Zéro friction si automatique. Mais il faut un `--explain` pour montrer pourquoi ces fichiers ont été choisis (transparence).

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 5 | 4 | 3 | 4 | 3 | 5 | **49** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** : 
1. Script `context-router.py` — analyse statique imports + index keywords
2. Intégration dans agent-base.md — chargement conditionnel
3. Mode conservative/aggressive configurable
4. Log + feedback loop d'apprentissage
**Effort estimé** : 3-5 jours
**Dépendances** : Aucune, standalone

---

## #23 — Chunking (Miller 7±2)

**Concept** : Tout output agent limité à 7±2 items par groupe. Backlogs, listes, menus automatiquement découpés en groupes digestibles.

**Challenge ⚡ Victor** : "C'est une règle de style, pas une innovation."
→ Partiellement vrai. Mais c'est une CONTRAINTE SYSTÈME inscrite dans agent-base.md qui change structurellement la qualité des outputs. Le vrai gain : ça force la priorisation.

**Challenge 🔬 Dr. Quinn** : "Comment l'appliquer sans casser les cas où on VEUT une liste longue ?"
→ La règle s'applique à la PRÉSENTATION, pas aux données. Une liste de 30 items est présentée en 4 groupes de 7-8.Avec un mode `--all` pour tout voir.

**Challenge 📋 John** : "Vrai impact utilisateur ?"
→ Modéré. C'est de l'hygiène informationnelle, pas un game changer. Mais ça contribue à une expérience cohérente.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 3 | 2 | 5 | 2 | 5 | 2 | **37** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Directive dans `agent-base.md` + convention dans les templates d'output
**Effort estimé** : 0.5 jour
**Dépendances** : Aucune

---

## #97 — Nudge (suggestions contextuelles)

**Concept** : L'agent produit des suggestions subtiles basées sur les patterns d'erreur passés du failure museum et des learnings. "As-tu pensé à vérifier les CORS ?" quand on travaille sur une API.

**Challenge ⚡ Victor** : "Si les suggestions sont mauvaises, ça devient du spam."
→ Risque réel. Mitigation : (1) confiance minimum du match (seuil 0.7), (2) max 1 nudge par réponse, (3) feedback "utile/pas utile" qui affine.

**Challenge 🔬 Dr. Quinn** : "Comment matcher le contexte actuel avec les learnings passés ?"
→ Keyword matching simple sur le nom de tâche + patterns récurrents dans failure-museum.md. Pas besoin de sémantique avancée — les patterns de failure sont souvent très littéraux.

**Challenge 🏗️ Winston** : "Ça ne surcharge pas le protocol d'activation ?"
→ Non si implémenté comme un hook post-activation optionnel, pas dans le core. Un "nudge-engine" léger qui s'exécute après le greeting.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 3 | 4 | 5 | 3 | 3 | **44** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale (potentiel haute si bien exécuté)**
**Implémentation** :
1. `nudge-engine.py` — scan failure-museum + learnings, match contexte
2. Hook dans agent-base.md après activation
3. Max 1 nudge, seuil confiance 0.7, feedback loop
**Effort estimé** : 2-3 jours
**Dépendances** : failure-museum.md, agent-learnings/

---

## #98 — Charge cognitive (Sweller)

**Concept** : Audit automatique de la charge cognitive de chaque agent : nombre de règles, longueur d'activation, nombre d'options menu, profondeur du workflow. Score + recommandations de simplification.

**Challenge ⚡ Victor** : "C'est du lint pour agents. Utile mais pas sexy."
→ Exact. Mais le Guard existant mesure le BUDGET TOKEN — ça mesure autre chose : la CHARGE COGNITIVE HUMAINE. Le dev qui lit 47 règles ne les retient pas. C'est l'anti-bloat agent.

**Challenge 🔬 Dr. Quinn** : "Comment mesurer objectivement la charge cognitive ?"
→ Métriques proxy : (1) nb de règles, (2) nb d'étapes d'activation, (3) nb d'items menu, (4) profondeur max workflow, (5) longueur persona en tokens. Chaque métrique a un seuil "vert/jaune/rouge" empirique.

**Challenge 🎨 Maya** : "Les agents ont BESOIN de règles complexes pour être bons."
→ Vrai. Mais la complexité doit être PROGRESSIVE, pas frontale. L'audit identifie les agents trop complexes et recommande partitionnement / lazy loading.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 3 | 4 | 4 | 4 | 5 | 3 | **43** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Extension du `guard` existant — `guard --cognitive` avec métriques de charge humaine
**Effort estimé** : 1-2 jours
**Dépendances** : guard existant

---

## #100 — Peak-End Rule (Kahneman)

**Concept** : Optimiser le premier message (entry) et le dernier message (exit) de chaque workflow. Entry = contexte clair + excitement. Exit = summary actionable + next steps + celebration proportionnelle.

**Challenge ⚡ Victor** : "C'est du copywriting, pas de la tech."
→ Dans un framework d'agents IA, le copywriting EST la tech. La perception de qualité du kit est directement liée à la qualité des messages. L'expérience se juge sur le pic et la fin.

**Challenge 📋 John** : "Comment standardiser sans que ça devienne robotique ?"
→ Templates avec variables de persona. Le PATTERN est standard, le CONTENU est unique par agent. Entry template : "[ICON] [GREETING] [CONTEXT_SUMMARY] [WHAT_NEXT]". Exit template : "[SUMMARY] [ARTIFACTS_CREATED] [NEXT_STEPS] [CELEBRATION_IF_SUCCESS]".

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 4 | 2 | 5 | 3 | 5 | 2 | **40** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Templates entry/exit dans agent-base.md + exemples par workflow
**Effort estimé** : 1 jour
**Dépendances** : Aucune

---

## #102 — Paradoxe du choix (Schwartz)

**Concept** : Max 5-7 options dans tout menu agent. Au-delà → sous-menus catégorisés ou recommandation "top 3 pour votre contexte".

**Challenge 🔬 Dr. Quinn** : "Certains agents DOIVENT avoir beaucoup d'options (bmad-master)."
→ Solution : menu principal (5-7 items) + "[M] More options..." en sous-menu. Le bmad-master a 15+ workflows, mais le dev voit d'abord les 5 les plus pertinents.

**Challenge 🎨 Maya** : "Comment déterminer les 5 les plus pertinents ?"
→ Par fréquence d'usage (BMAD_TRACE) + par phase projet (planning → build → ops). Les options changent selon le contexte.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 3 | 2 | 5 | 3 | 5 | 2 | **38** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Règle dans agent-base.md + refactoring menus agents existants
**Effort estimé** : 1 jour
**Dépendances** : Aucune

---

## #111 — Mise en place (pre-flight check)

**Concept** : Avant chaque story, l'agent exécute un pre-flight automatique : vérification des dépendances, identification des fichiers à modifier, préchargement du contexte pertinent, estimation des CC requirements, check mémoire (learnings + failure museum pertinents).

**Challenge ⚡ Victor** : "C'est ce que tout bon dev fait mentalement. Pourquoi l'automatiser ?"
→ Parce que l'agent IA NE le fait PAS systématiquement. Le pre-flight force la discipline. Et ça détecte les problèmes AVANT de coder : "Attention, le fichier X est locked par une autre story", "Le test Y fail déjà avant ton changement".

**Challenge 🔬 Dr. Quinn** : "Ça ajoute du temps avant chaque story."
→ 30 secondes de pre-flight vs 30 minutes de debug quand on découvre le problème en plein milieu. ROI massif.

**Challenge 🏗️ Winston** : "Comment le pre-flight sait-il quels fichiers seront impactés avant de coder ?"
→ (1) Analyse de la story pour les fichiers mentionnés, (2) imports/dépendances des fichiers mentionnés, (3) patterns passés (stories similaires dans BMAD_TRACE). C'est une estimation, pas une certitude — mais c'est mieux que rien.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 5 | 4 | 3 | 5 | 4 | 4 | **50** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. `preflight-check.py` — analyse story, scan dépendances, check état courant
2. Intégration dans dev-story workflow (step 0 avant implémentation)
3. Output : rapport pre-flight avec go/no-go et warnings
4. Connexion nudge-engine pour les learnings pertinents
**Effort estimé** : 3-4 jours
**Dépendances** : context-router (#17), nudge-engine (#97)

---

## #115 — Réduction (agent condenseur)

**Concept** : Un outil qui prend n'importe quel artefact BMAD et produit une version ultra-concentrée (executive summary). PRD de 10 pages → 1 page. Architecture de 50 fichiers → vue d'ensemble 1 paragraphe.

**Challenge ⚡ Victor** : "Le LLM fait déjà ça quand on lui demande de résumer."
→ Oui, mais ici c'est STRUCTURÉ et STANDARDISÉ pour chaque type d'artefact BMAD. Le summary d'un PRD a un format différent du summary d'une architecture. Et c'est persisté comme artefact réutilisable.

**Challenge 📋 John** : "Qui utilise les résumés ?"
→ (1) Les agents qui consomment les artefacts cross-team (le Dev ne lit pas tout le PRD, juste le résumé), (2) les Delivery Contracts inter-teams, (3) le context router qui charge les résumés au lieu des docs complètes.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 3 | 4 | 4 | 4 | 3 | **44** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Template de condensation par type d'artefact + intégration dans les workflows
**Effort estimé** : 2 jours
**Dépendances** : Aucune, mais synergique avec #17 (context router)

---

## #131 — Espace négatif (Out of Scope)

**Concept** : Section "Ce que ce projet/story N'EST PAS" obligatoire dans chaque PRD, architecture doc, et story. Définir les frontières par exclusion explicite.

**Challenge ⚡ Victor** : "C'est une bonne pratique documentaire, pas une innovation."
→ Correct en isolation. L'innovation est de le rendre OBLIGATOIRE et VÉRIFIABLE by design. L'agent refuse de valider un artefact sans section "Out of Scope". Ça change le comportement par contrainte système.

**Challenge 🔬 Dr. Quinn** : "Comment vérifier automatiquement la qualité du Out of Scope ?"
→ Présence ≠ qualité. On peut vérifier la présence (lint). Pour la qualité, l'agent adversarial (#51 existant) challenge le out of scope : "Est-ce que X devrait être in-scope ?"

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 4 | 2 | 5 | 3 | 5 | 2 | **40** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Section obligatoire dans les templates PRD, arch, story + lint check
**Effort estimé** : 0.5 jour
**Dépendances** : Aucune

---

## #147 — Grice — Maximes conversationnelles

**Concept** : Règles dans agent-base.md basées sur les maximes de Grice : Quantité (suffisant mais pas trop), Qualité (vérifié avant d'affirmer), Pertinence (on-topic), Manière (clair, pas ambigu).

**Challenge ⚡ Victor** : "Les agents ont déjà des communication styles. C'est redondant."
→ Non. Le communication style est la FORME (enthousiaste, succinct, narratif). Les maximes sont les RÈGLES DE FOND (ne pas mentir, ne pas noyer l'info, rester pertinent). C'est orthogonal.

**Challenge 🔬 Dr. Quinn** : "Comment enforcer des maximes qualitatives ?"
→ Pas par du code, mais par des instructions précises dans agent-base.md avec exemples positifs et négatifs. Le LLM respecte mieux les règles explicites avec exemples.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 4 | 3 | 5 | 3 | 5 | 3 | **45** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** : Section "Communication Maxims" dans agent-base.md avec 4 règles + exemples
**Effort estimé** : 0.5 jour
**Dépendances** : Aucune

---

## #153 — Director's Cut vs Theatrical

**Concept** : Deux modes de sortie pour tout artefact : `--verbose` (complet avec justifications, alternatives, trade-offs) et `--summary` (résumé exécutif, résultats clés).

**Challenge 📋 John** : "C'est utile pour qui ?"
→ verbose pour le dev/architect qui fait, summary pour le PM/stakeholder qui review. Cross-team : Team Vision produit le PRD verbose, Team Build reçoit le summary + accès au verbose si besoin.

**Challenge 🏗️ Winston** : "Deux versions = double maintenance."
→ Le verbose EST la source de vérité. Le summary est GÉNÉRÉ automatiquement à partir du verbose. Pas de double maintenance.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 3 | 3 | 4 | 4 | 3 | **43** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Flag `--summary` / `--verbose` dans les tools CLI + templates de condensation
**Effort estimé** : 2 jours
**Dépendances** : Synergique avec #115 (réduction)

---

## #175 — Desire Paths (chemins de désir)

**Concept** : Tracker via BMAD_TRACE quels workflows/agents/features sont RÉELLEMENT utilisés vs comment on a PRÉVU qu'ils soient utilisés. Rapport "desire paths" qui identifie les écarts.

**Challenge ⚡ Victor** : "Le BMAD_TRACE existe déjà. C'est juste de l'analytics."
→ L'analytics sans INTERPRÉTATION n'est rien. Le value-add est l'analyse : "Le workflow X n'est jamais lancé entièrement — les devs sautent toujours l'étape 3. → Recommandation : rendre l'étape 3 optionnelle ou la fusionner." C'est le feedback loop ultime.

**Challenge 🔬 Dr. Quinn** : "Assez de données pour être statistiquement significatif ?"
→ Bon point. Un solo dev sur 1 projet = échantillon faible. Mais avec cross-migrate, on peut agréger les patterns de plusieurs projets. Et même sur 1 projet, après 10 sprints les patterns sont clairs.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 5 | 4 | 3 | 5 | 4 | 5 | **52** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. Extension BMAD_TRACE — tracker granulaire (workflow steps, menu choices, agent switches)
2. `desire-paths.py` — analyse patterns d'usage vs patterns attendus
3. Rapport avec recommandations concrètes de restructuration
4. Intégration dans `nso retro`
**Effort estimé** : 3-4 jours
**Dépendances** : BMAD_TRACE existant

---

## #218 — Triage (priorisation automatique)

**Concept** : Agent de triage automatique pour bugs/stories/décisions basé sur : criticité (1-5), impact utilisateur (1-5), effort estimé (T-shirt), dependencies.

**Challenge ⚡ Victor** : "Tout framework agile a du triage. C'est du JIRA automation."
→ La différence : le triage est fait par les AGENTS qui connaissent le contexte technique ET business. Un PM agent + un Dev agent estiment ensemble, avec les données du projet (pas des rules statiques).

**Challenge 🔬 Dr. Quinn** : "Les estimations agent sont-elles fiables ?"
→ Individuellement non. Mais avec #38 (sagesse des foules) — 3 agents estiment indépendamment et on prend la médiane — la fiabilité augmente. Et on compare avec le réel (via BMAD_TRACE) pour calibrer.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 3 | 3 | 4 | 3 | 3 | **42** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Template de triage dans le workflow SM + multi-agent estimation
**Effort estimé** : 2 jours
**Dépendances** : Synergique avec #38 (sagesse des foules)

---

## #223 — Second opinion

**Concept** : Toute décision d'architecture = minimum 2 agents consultés indépendamment avant validation. L'architecte propose, un autre agent (PM ou QA ou Dev) challenge.

**Challenge ⚡ Victor** : "C'est l'adversarial consensus existant."
→ Non. Adversarial consensus = processus formel BFT pour décisions critiques (3 votants + avocat du diable). Second opinion = processus LÉGER pour TOUTES les décisions arch : juste "un autre avis" rapide. C'est le mode casual vs le mode tribunal.

**Challenge 🏗️ Winston** : "Ça ralentit chaque décision arch."
→ Le "second opinion" est un one-shot, pas un cycle de débat. 1 réponse, 2 minutes. Si désaccord → escalade vers adversarial consensus formel.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 4 | 2 | 4 | 5 | 4 | 3 | **44** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Règle dans le workflow architecture : "Before APPROVE → get_second_opinion(agent)"
**Effort estimé** : 1 jour
**Dépendances** : adversarial-consensus existant (escalade)

---

## #116 — Chaîne du froid (intégrité sémantique)

**Concept** : Vérifier que l'information ne se dégrade pas en passant d'agent en agent (PRD → arch → story → code). Checksum sémantique : les concepts clés du PRD sont-ils tous présents dans l'architecture ? Les ACs de la story sont-ils tous testés ?

**Challenge ⚡ Victor** : "C'est une killer feature si ça marche. Mais comment faire un 'checksum sémantique' ?"
→ Pas besoin de NLP avancé. Approche pragmatique : (1) extraction de "concepts clés" (termes, user stories, ACs) au format liste, (2) vérification de présence dans l'artefact suivant de la chaîne, (3) rapport de "drift sémantique". C'est du grep intelligent, pas de l'IA.

**Challenge 🔬 Dr. Quinn** : "Les reformulations cassent le matching."
→ Vrai. Solution : (1) identifier les termes canoniques dans un glossaire projet (#148 Rosetta Stone), (2) matcher sur les synonymes connus, (3) pour les cas flous → flag "à vérifier humainement" plutôt que faux positif/négatif.

**Challenge 🏗️ Winston** : "La chaîne PRD→arch→story→code est souvent non-linéaire."
→ Bon point. Implémentation en GRAPHE de dépendances, pas en chaîne linéaire. Chaque artefact déclare ses sources. Le checksum vérifie source→dérivé.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 5 | 5 | 3 | 5 | 3 | 5 | **50** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. `semantic-chain.py` — extraction concepts clés par artefact
2. Graphe de dépendances artefact→artefact  
3. Checksum : vérification concepts source → dérivé
4. Rapport de "drift sémantique" avec flags
5. Intégration dans le Delivery Contract (pré-requis au handoff)
**Effort estimé** : 5-7 jours
**Dépendances** : #148 (Rosetta Stone, optionnel mais améliore)

---

## #6 — Symbiose d'agents

**Concept** : Documenter et exploiter les paires d'agents synergiques. PM+Analyst = requirements 360°. Dev+QA = TDD natif. Architect+Dev = design-to-code fluide.

**Challenge ⚡ Victor** : "C'est les teams existantes, pas nouveau."
→ Les teams sont des GROUPEMENTS. La symbiose est une MÉCANIQUE : quand PM travaille, Analyst est automatiquement consulté en parallèle (pas séquentiellement). La différence est l'exécution SIMULTANÉE et le merge intelligent.

**Challenge 🏗️ Winston** : "Différence concrète avec le boomerang orchestration ?"
→ Boomerang = orchestrateur délègue explicitement. Symbiose = deux agents activés simultanément par le MÊME input, produisant des outputs complémentaires fusionnés. Pas de chef, pas de délégation — co-création.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 4 | 3 | 2 | 4 | 3 | 4 | **40** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Matrice de symbiose dans les team manifests + mode "co-create" dans boomerang
**Effort estimé** : 3 jours
**Dépendances** : Boomerang orchestration existant

---

## #11 — Camouflage adaptatif

**Concept** : Les agents adaptent leur communication et leur niveau de détail au `user_skill_level` existant + au contexte.

**Challenge 📋 John** : "Le config a déjà `user_skill_level`. C'est fait."
→ Le config EXISTE mais n'est pas UTILISÉ de manière granulaire. Un dev expert reçoit les mêmes explications qu'un junior. L'adaptation devrait être : expert = pas d'explication de base, options avancées visibles, jargon OK. Junior = explications pas à pas, jargon traduit, options avancées cachées.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 4 | 2 | 4 | 3 | 4 | 2 | **40** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Conditionals dans agent-base.md basés sur `user_skill_level`
**Effort estimé** : 1 jour
**Dépendances** : Aucune

---

## #22 — Priming cognitif

**Concept** : Les agents "amorcent" le contexte avant de poser des questions, améliorant la qualité des réponses utilisateur.

**Challenge 🎨 Maya** : "Exemple concret ?"
→ Au lieu de "Quel framework frontend ?" → "Tu as actuellement 15 composants React avec TypeScript strict, une couverture test à 80%, et du Material UI. Dans ce contexte, quel framework frontend préfères-tu pour le nouveau module ?" Le priming = contexte intégré dans la question.

**Challenge ⚡ Victor** : "C'est juste bien poser des questions."
→ Oui, mais AUTOMATIQUEMENT en utilisant les données du projet. L'agent scan le contexte pertinent avant chaque question et l'intègre. C'est du context-aware questioning.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 3 | 4 | 4 | 4 | 3 | **44** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Pattern dans agent-base.md : "Before asking a question, load relevant context and integrate it into the question"
**Effort estimé** : 0.5 jour
**Dépendances** : context-router (#17) pour le context loading

---

## #44 — Division du travail

**Concept** : Ultra-spécialisation des agents sur des micro-tâches vs généralistes.

**Challenge ⚡ Victor** : "On a DÉJÀ des agents spécialisés ET des généralistes (Barry)."
→ L'idée est de pousser plus loin : des "micro-agents" pour des tâches très précises (import sorting, error handling patterns, API endpoint scaffolding). Mais attention, ça augmente le nombre d'agents et la complexité.

**Challenge 🏗️ Winston** : "Plus d'agents = plus de coordination overhead."
→ C'est le problème de Dunbar (#39). Le sweet spot est 10-15 agents max par team. Au-delà, le coût de coordination dépasse le gain de spécialisation.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 3 | 2 | 3 | 3 | 3 | 2 | **33** 🟠 |

**Verdict : 🟠 EN SURSIS — Fonctionne mieux comme extension du agent-forge existant plutôt que comme concept standalone. Fusionner avec agent-forge : "forge peut créer des micro-agents éphémères pour des tâches précises".**

---

## #66 — Affordance

**Concept** : Chaque état de workflow montre clairement les actions possibles, comme un bouton physique montre qu'on peut appuyer.

**Challenge 🎨 Maya** : "C'est un principe UX fondamental."
→ Exactement. Mais dans le contexte text-only des agents IA, l'affordance est souvent NULLE. L'utilisateur ne sait pas ce qu'il peut faire. Chaque réponse agent devrait se terminer par les actions disponibles.

**Challenge 📋 John** : "Les menus font déjà ça."
→ Les menus sont statiques. L'affordance est CONTEXTUELLE : après une analyse, les actions ne sont pas les mêmes qu'après un build failure. Les options visibles changent avec l'état.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 2 | 4 | 3 | 5 | 2 | **40** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Chaque réponse agent se termine par "[Available actions based on current state]"
**Effort estimé** : 1 jour
**Dépendances** : Aucune

---

## #74 — Boucle/Sample (workflow snippets composables)

**Concept** : Library de workflow snippets réutilisables et composables. Un snippet "run tests" + un snippet "format code" + un snippet "commit" = workflow composé.

**Challenge 🏗️ Winston** : "On a des workflows YAML, c'est quoi de plus ?"
→ Les workflows YAML sont des BLOCS monolithiques. Les snippets sont des ATOMES composables. Comme la différence entre une fonction monolithique et des micro-fonctions. On peut composer des workflows custom par assembly de snippets.

**Challenge 🔬 Dr. Quinn** : "Risque de fragmentation — 100 snippets sans cohérence."
→ Mitigation : catégories strictes (pre-check, execution, validation, cleanup) + tests de composition. Un snippet déclare ses inputs/outputs, la composition est validable.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 3 | 3 | 4 | 3 | 4 | **44** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : `framework/workflows/snippets/` avec inputs/outputs déclarés + composer tool
**Effort estimé** : 3 jours
**Dépendances** : Aucune

---

## #75 — Crescendo (onboarding progressif)

**Concept** : Les features du kit se débloquent progressivement : jour 1 = basics (agents, CC). Semaine 1 = intermédiaire (teams, memory). Mois 1 = avancé (darwinism, stigmergy, NSO). Évite la surcharge initiale.

**Challenge ⚡ Victor** : "#102 (paradoxe du choix) couvre déjà ça."
→ Non. #102 = limiter les options visibles. #75 = parcours d'apprentissage structuré avec milestones. C'est la différence entre cacher et enseigner.

**Challenge 📋 John** : "Concrètement, comment 'débloquer' ?"
→ Le `project-context.tpl.yaml` a un champ `maturity_level: beginner|intermediate|advanced`. Les agents/workflows avancés sont mentionnés mais marqués "[Advanced]" et l'agent propose de les activer quand les basics sont maîtrisés.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 5 | 3 | 3 | 3 | 4 | 4 | **46** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. Champ `maturity_level` dans project-context
2. Agents adaptent menus/options selon le level
3. Progression guide : checklist de capabilities à débloquer
4. `bmad-init.sh --maturity intermediate` pour upgrade
**Effort estimé** : 2-3 jours
**Dépendances** : #11 (camouflage adaptatif), #102 (paradoxe du choix)

---

## #95 — Zeigarnik (tâches inachevées)

**Concept** : Dashboard "tâches en cours" proéminent au démarrage de session. L'effet Zeigarnik = on se souvient mieux des tâches inachevées → motivation à les terminer.

**Challenge ⚡ Victor** : "C'est un TO-DO dans le greeting. Basique."
→ Basique mais MANQUANT. Actuellement l'agent ne montre pas automatiquement les stories en cours, les workflows interrompus, les TODOs laissés. C'est dans state-checkpoint mais pas dans le greeting.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 5 | 4 | 2 | 5 | 4 | 5 | 2 | **42** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : Dans agent-base.md activation : "Check state-checkpoint, show pending tasks in greeting"
**Effort estimé** : 0.5 jour
**Dépendances** : state-checkpoint existant

---

## Tier 1 — Évaluations restantes (batch accéléré)

Les idées suivantes ont été évaluées avec le même processus mais présentées en format condensé :

### ✅ VALIDÉES — Priorité haute

| # | Concept | Score | Note clé | Effort |
|---|---------|-------|----------|--------|
| 148 | **Rosetta Stone** (glossaire cross-domain) | **47** | Unique, renforce #116. Glossaire auto-généré Business↔Tech↔UX | 3j |
| 149 | **Signaux silencieux** (confidence scores) | **45** | Chaque output a un score de confiance 0-1. Transforme la transparence | 2j |

### 🟡 VALIDÉES — Priorité normale

| # | Concept | Score | Note clé | Effort |
|---|---------|-------|----------|--------|
| 101 | JTBD émotionnel | 38 | Ajouter motivations émotionnelles dans interview prompts | 0.5j |
| 107 | Wuwei (non-interruption) | 36 | Agent détecte quand ne pas interrompre en mode [ACT] | 0.5j |
| 109 | Go — Influence vs contrôle | 37 | Par défaut : suggestion, pas directive. Opt-in: directive | 0.5j |
| 110 | Blitz vs Classique | 39 | Renforcer le switch Barry(lean) vs Team Build(full) | 1j |
| 117 | Recette vs Intuition | 38 | Variable guidance basée sur `user_skill_level` | 0.5j |
| 128 | Coach vs Joueur | 37 | Expliciter dans agent-base : guide, ne remplace pas | 0.5j |
| 132 | Croquis vs Huile | 40 | Niveaux de fidélité : draft/standard/polished | 1j |
| 133 | Perspective multi-vues | 42 | Artefact viewable en vue business/technique/utilisateur | 2j |
| 134 | Wabi-sabi | 36 | Acceptation imperfection MVP inscrite dans workflows | 0.5j |
| 146 | Métaphore structurante | 37 | Champ `project_metaphor` dans project-context | 0.5j |
| 150 | Étymologie décisions | 40 | Chaque naming/pattern lié à sa justification dans ADR | 1j |
| 154 | MacGuffin detector | 41 | Agent qui challenge les priorités "tout le monde veut X, mais..." | 1j |
| 159 | Destruction créatrice | 38 | Workflow sunset pour agents/workflows obsolètes | 1j |
| 162 | Rendements décroissants | 39 | Alerte quand temps/story dépasse 2x l'estimation → flag | 1j |
| 165 | Économie circulaire | 37 | Code supprimé → patterns documentés dans learnings | 0.5j |
| 174 | Ruines créatives | 36 | Historique architectures dans ADR + leçons retirées | 0.5j |
| 190 | Distillation | 36 | Séparation concerns par volatilité formalisée dans arch docs | 0.5j |
| 198 | Bright patterns | 38 | Bon choix = chemin par défaut dans chaque workflow | 1j |
| 206 | Difficulty scaling | 40 | Complexité workflow adaptée au skill_level (= #75 Crescendo) | Fusionné |
| 224 | Rééducation progressive | 37 | Post-incident gradual rollback dans workflow incident-response | 1j |

### 🟠 EN SURSIS

| # | Concept | Score | Décision |
|---|---------|-------|----------|
| 44 | Division du travail | 33 | Fusionné avec agent-forge (micro-agents éphémères) |

