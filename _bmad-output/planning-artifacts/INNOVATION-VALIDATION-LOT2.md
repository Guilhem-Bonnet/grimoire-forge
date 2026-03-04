# Validation Innovation — LOT 2 : TIER 2 R&D Moyen Terme (55 idées)

> **Même framework de scoring** : F×2 + V×3 + U×2 + S×1 + C×1 + R×1 + D×2 = max 60

---

## TOP 20 — Évaluations approfondies

---

## #2 — Mycelium Network (P2P inter-instances BMAD)

**Concept** : Protocole de partage de connaissances entre instances BMAD sur différents projets. Chaque projet qui utilise BMAD contribue à un réseau de patterns, comme le réseau mycorhizien connecte les arbres d'une forêt.

**Challenge ⚡ Victor** : "Ça ressemble à du cross-migrate mais en réseau. Le cross-migrate existe déjà."
→ Cross-migrate est un export/import MANUEL et PONCTUEL entre 2 projets. Mycelium est un protocole CONTINU et MULTI-DIRECTIONNEL. La différence : postal vs internet.

**Challenge 🔬 Dr. Quinn** : "Problèmes de sécurité ? Les données d'un projet confidentiel leakent vers un autre."
→ Risque CRITIQUE. Mitigation : seuls les patterns ANONYMISÉS sont partagés. Jamais de code, jamais de noms, jamais de données. Seulement : "Le pattern X a fonctionné pour un projet de type Y." + opt-in strict.

**Challenge 🏗️ Winston** : "Comment synchroniser sans serveur central ? Zero-cloud est la contrainte du kit."
→ Problème réel. Solutions : (1) Git-based — un repo partagé de patterns (public ou privé), (2) fichier de bundle échangé manuellement, (3) à terme, protocole P2P local (mDNS/Bonjour sur LAN). Pour la v1, le Git-based suffit.

**Challenge 📊 Mary** : "Le marché veut-il ça ? Combien d'utilisateurs BMAD sont multi-projets ?"
→ Aujourd'hui peu. Mais c'est un MOAT compétitif massif. Aucun concurrent n'a de "réseau d'apprentissage inter-projets". Et pour un solo dev avec 5+ projets, c'est précieux.

**Challenge 📋 John** : "MVP réaliste ?"
→ MVP = un repo Git `bmad-collective-patterns` où `cross-migrate export --anonymize` push automatiquement les patterns validés. Les autres projets `cross-migrate import --from-collective` pull les patterns pertinents.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 4 | 5 | 2 | 4 | 2 | 5 | **44** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale (mais potentiel moonshot si communauté croît)**
**Implémentation MVP** :
1. `cross-migrate export --anonymize` — strip les données projet-spécifiques
2. Format de "pattern card" standardisé (type, contexte, outcome, confidence)
3. Repo Git `bmad-patterns` comme hub d'échange
4. `cross-migrate import --from-patterns` avec matching contextuel
**Effort estimé** : 5-7 jours
**Dépendances** : cross-migrate existant

---

## #3 — Essaimage / Swarm Intelligence (consensus émergent)

**Concept** : Au lieu d'un consensus formel (adversarial), les agents votent par "danse" — chaque agent contribue son évaluation indépendamment, et le consensus ÉMERGE de l'agrégation.

**Challenge ⚡ Victor** : "C'est la sagesse des foules (#38). Doublon."
→ Partiellement. #38 = estimation NUMÉRIQUE agrégée (combien de jours ?). #3 = DÉCISION agrégée (quelle architecture ?). Les mécanismes sont différents : vote pondéré par expertise vs moyenne de nombres.

**Challenge 🔬 Dr. Quinn** : "Comment pondérer les votes sans replay le adversarial consensus ?"
→ Pondération statique par expertise déclarée dans le manifest. L'architect a poids 3x sur les décisions arch, le QA poids 3x sur les décisions qualité, le PM poids 3x sur les décisions produit. Simple, transparent.

**Challenge 🏗️ Winston** : "Concrètement, quand utilise-t-on le swarm vs le adversarial consensus ?"
→ Swarm = décisions routinières (choix de lib, priorité de stories). Adversarial = décisions critiques irréversibles (choix de stack, architecture fondamentale). Le seuil est l'irréversibilité.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 3 | 3 | 3 | 5 | 3 | 4 | **41** 🟡 |

**Verdict : 🟡 VALIDÉ — Fusionner avec adversarial-consensus comme mode "light"**
**Implémentation** : `consensus --mode swarm` (léger) vs `consensus --mode adversarial` (formel)
**Effort estimé** : 2 jours
**Dépendances** : adversarial-consensus existant

---

## #12 — Plasticité synaptique (workflows auto-optimisés)

**Concept** : Les workflows les plus utilisés se "renforcent" — les étapes qui marchent toujours sont accélérées (auto-approve), celles qui échouent souvent sont renforcées (checks supplémentaires). Auto-adaptation basée sur l'historique.

**Challenge ⚡ Victor** : "C'est du machine learning sur les workflows. On a les données ?"
→ Oui — BMAD_TRACE + desire paths (#175) fournissent les données. Et pas besoin de ML : des règles simples suffisent. "Si l'étape X a échoué 3 fois sur les 5 dernières = ajouter un pre-check." "Si l'étape Y a toujours réussi sans intervention = auto-approve."

**Challenge 🔬 Dr. Quinn** : "Risque : auto-approve d'étapes qui devraient être vérifiées juste parce qu'elles n'ont jamais échoué. Le cygne noir."
→ Risque réel. Mitigation : (1) jamais auto-approve les étapes de sécurité ou CC final, (2) audit régulier des auto-approves, (3) seuil conservateur (10 succès consécutifs minimum).

**Challenge 🏗️ Winston** : "Les workflows sont en YAML/MD statiques. Comment les rendre dynamiques ?"
→ On ne modifie pas les fichiers. On ajoute un "overlay" dynamique : `workflow-adaptations.yaml` qui override des comportements spécifiques. Le workflow source reste intact.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 4 | 5 | 3 | 4 | 2 | 5 | **45** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. `workflow-adaptations.yaml` — overlay dynamique par workflow
2. Analyse BMAD_TRACE → génération d'adaptations recommandées
3. `bmad-init.sh adapt --review` — review et approve les adaptations
4. Seuils conservateurs, never auto-approve security/CC
**Effort estimé** : 5-7 jours
**Dépendances** : BMAD_TRACE, #175 (desire paths)

---

## #16 — Biais cognitifs comme features

**Concept** : Au lieu de combattre les biais, les utiliser intentionnellement. Biais d'ancrage pour fixer les priorités (montrer la solution recommandée EN PREMIER). Biais de confirmation pour la validation (chercher activement les preuves que ça marche avant de chercher les contre-preuves). Biais de récence pour prioriser les patterns récents.

**Challenge ⚡ Victor** : "C'est de la MANIPULATION."
→ Manipulation ≠ design intentionnel. Un bon UX designer utilise DÉJÀ les biais (defaults intelligents = biais du statu quo). La question est l'INTENTION : aider le dev à prendre de meilleures décisions = éthique.

**Challenge 🔬 Dr. Quinn** : "Et si un bias amplifie une mauvaise décision ?"
→ C'est pourquoi chaque biais utilisé est DOCUMENTÉ et TRANSPARENT. L'agent dit : "Je recommande X en premier (ancrage intentionnel). Les alternatives sont Y, Z." La transparence neutralise le risque.

**Challenge 📋 John** : "Exemples concrets dans le kit ?"
→ (1) Ancrage : les estimations de story commencent par la médiane historique. (2) Disponibilité : le failure museum montre les erreurs RÉCENTES en premier. (3) Framing : "95% des tests passent" vs "27 tests en échec" — choisir le framing adapté. (4) Engagement : commencer par un petit changement, puis étendre (foot-in-the-door technique).

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 5 | 3 | 4 | 3 | 5 | **49** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute — Innovation UNIQUE**
**Implémentation** :
1. Catalogue de biais exploitables avec guidelines éthiques
2. Intégration dans agent-base.md : quand/comment utiliser chaque biais
3. Transparence obligatoire ("[Anchoring: showing recommended option first]")
4. "Bias audit" dans le workflow de review
**Effort estimé** : 2-3 jours
**Dépendances** : Aucune

---

## #25 — Digital Twin (simulation d'impact)

**Concept** : Avant d'implémenter un changement architectural, simuler son impact sur le système. "Et si on ajoutait Redis ? Voici les modules impactés, les tests à mettre à jour, l'estimation d'effort, les risques."

**Challenge ⚡ Victor** : "Un 'digital twin' est un concept industriel lourd. Ce n'est pas réaliste pour un framework local."
→ Correct si on parle d'un vrai digital twin. Mais la VERSION BMAD est plus simple : c'est une analyse d'impact statique. On a le graphe de dépendances, on a l'historique des changements, on a les patterns — on peut SIMULER l'impact sans exécuter.

**Challenge 🔬 Dr. Quinn** : "L'analyse d'impact n'est fiable que si le graphe de dépendances est complet."
→ Bon point. Prérequis : le context-router (#17) doit avoir mappé les dépendances du projet. Sinon, l'analyse est partielle et le dit explicitement.

**Challenge 🏗️ Winston** : "Ça existe déjà dans les IDE — IntelliJ fait du refactoring preview."
→ IntelliJ fait du refactoring CODE. Ici on simule l'impact BUSINESS + TECHNIQUE + EQUIPE. "Ajouter Redis impacte : architecture (nouveau service), tests (18 tests à adapter), documentation (3 docs à update), skills (personne dans l'équipe ne connaît Redis), coûts (infra + licence)."

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 5 | 4 | 2 | 4 | 3 | 5 | **46** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. `impact-sim.py` — analyse statique multi-dimension (code, tests, docs, skills, cost)
2. Input : description du changement proposé
3. Output : rapport d'impact avec score de risque et recommandations
4. Intégration dans le workflow architecture (avant toute décision)
**Effort estimé** : 5-7 jours
**Dépendances** : #17 (context-router), #78 (théorie des graphes)

---

## #27 — Federated Learning (apprentissage distribué)

**Concept** : Plusieurs instances BMAD apprennent ensemble sans partager de données sensibles. Chaque instance fait son analyse locale, seuls les "gradients" (patterns abstraits) sont partagés.

**Challenge ⚡ Victor** : "C'est le mycelium network (#2) avec un nom fancy."
→ Non. Mycelium = partage de patterns FINIS et EXPLICITES ("pattern X fonctionne pour contexte Y"). Federated learning = les instances apprennent ENSEMBLE de manière continue, les modèles s'enrichissent mutuellement sans échange de données raw.

**Challenge 🔬 Dr. Quinn** : "Il n'y a pas de 'modèle' à entraîner dans BMAD. Les agents sont des prompts."
→ Point fatal. Les LLM ne s'entraînent pas localement. Le "federated learning" ici se réduit à : partager des prompts améliorés et des patterns validés. C'est du mycelium avec un algorithme de sélection des meilleurs patterns. Pas besoin d'un concept séparé.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 2 | 3 | 3 | 1 | 3 | 2 | 3 | **30** 🟠 |

**Verdict : 🟠 EN SURSIS — Fusionner avec #2 (Mycelium). Le concept de sélection des meilleurs patterns enrichit Mycelium mais ne justifie pas un outil séparé.**

---

## #38 — Sagesse des foules (estimation agrégée)

**Concept** : Tous les agents estiment indépendamment (effort, risque, impact), puis agrégation pondérée = meilleure prédiction qu'aucun agent individuel.

**Challenge ⚡ Victor** : "On peut pas demander 5 estimations à 5 agents séparément dans un seul chat."
→ Correct avec le LLM actuel. Mais : (1) un agent peut SIMULER les perspectives de plusieurs agents (déjà fait en party mode), (2) avec le swarm mode (#3), chaque "vote" est généré indépendamment, (3) on peut séquentialiser sur des décisions clés.

**Challenge 🔬 Dr. Quinn** : "L'indépendance est la clé. Si les agents partagent le même contexte, ils sont corrélés."
→ Vrai. Solution : chaque agent reçoit un SUBSET différent du contexte pour estimer. L'architecte voit le graphe de dépendances, le dev voit la complexité code, le QA voit les risques test. Perspectives différentes = indépendance.

**Challenge 📋 John** : "Le planning poker agile fait exactement ça."
→ Oui, c'est du planning poker automatisé avec des agents. La valeur = pas besoin d'une vraie équipe, un dev solo a accès à multiple perspectives.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 3 | 3 | 4 | 4 | 3 | **43** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : `consensus --mode estimate` — chaque agent estime, médiane pondérée + écart-type
**Effort estimé** : 2 jours
**Dépendances** : #3 (swarm mode)

---

## #42 — Théorie des jeux (allocation de ressources)

**Concept** : Les agents négocient les ressources (context window, priorité, temps d'exécution) via des mécanismes de théorie des jeux : enchères, allocation Nash.

**Challenge ⚡ Victor** : "Trop académique. Quel est le problème concret résolu ?"
→ Le problème : le context window est LIMITÉ. Si 3 agents veulent tous charger leurs fichiers de référence, qui a la priorité ? Actuellement : premier arrivé, premier servi. Avec la théorie des jeux : allocation proportionnelle à l'importance de la tâche.

**Challenge 🔬 Dr. Quinn** : "Les agents ne sont pas des agents autonomes rationnels — c'est le même LLM."
→ Point valide. Implémenter ça comme un ALLOCATEUR de ressources qui utilise les métriques d'importance, pas comme une vraie négociation. Plus simple, même résultat.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 2 | 3 | 4 | 2 | 3 | 2 | 3 | **33** 🟠 |

**Verdict : 🟠 EN SURSIS — Le concept est intéressant mais l'implémentation réaliste est un allocateur de ressources simple, pas de la théorie des jeux. Fusionner avec #17 (Context Router) comme module d'allocation.**

---

## #48 — Effet papillon (détection d'anomalies précoces)

**Concept** : Détecter les petits signaux dans BMAD_TRACE avant qu'ils deviennent des crises. Exemples : temps de story qui augmente progressivement, taux d'échec CC qui monte, learnings contradictoires qui s'accumulent.

**Challenge ⚡ Victor** : "Le NSO fait déjà du monitoring."
→ Le NSO fait du monitoring PONCTUEL (on le lance, il analyse). L'effet papillon est du monitoring CONTINU avec des alertes PRÉCOCES. Le NSO dit "tu as un problème". L'effet papillon dit "tu VAS AVOIR un problème dans 2 sprints si cette tendance continue."

**Challenge 🔬 Dr. Quinn** : "Comment prédire avec peu de données ?"
→ Pas de prédiction ML. Des tendances simples : régression linéaire sur 5 data points. Si la pente est négative → alerte. Si 3 indicateurs sont simultanément en dégradation → alerte rouge. Heuristiques simples, pas de magie.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 5 | 4 | 3 | 5 | 3 | 5 | **50** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. `early-warning.py` — analyse de tendances sur BMAD_TRACE
2. 5 métriques clés : temps/story, taux CC pass, contradictions, scope creep, entropie mémoire
3. Alertes 3 niveaux : watch / warning / critical
4. Intégration NSO : `nso run` inclut early-warning
**Effort estimé** : 3-4 jours
**Dépendances** : BMAD_TRACE, NSO existant

---

## #52 — Sérendipité programmée

**Concept** : Le système injecte aléatoirement des connexions entre domaines éloignés. "Pendant que tu travailles sur l'authentification, le failure museum d'un autre module a eu un pattern similaire avec le caching — potentielle connexion."

**Challenge ⚡ Victor** : "Les connexions forcées sont du spam si elles ne sont pas pertinentes."
→ D'accord. Mitigation : (1) algo de pertinence minimum (au moins 1 concept commun), (2) max 1 "sérendipité" par session, (3) opt-out facile, (4) le nudge engine (#97) est le véhicule — la sérendipité est un TYPE de nudge.

**Challenge 🎨 Maya** : "C'est le dream mode qui croise les sources."
→ Dream mode croise les sources HORS session. Sérendipité croise les sources EN session, au moment où c'est potentiellement utile. Complémentaires.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 3 | 4 | 3 | 4 | 3 | 4 | **41** 🟡 |

**Verdict : 🟡 VALIDÉ — Comme sous-feature du nudge-engine (#97)**
**Implémentation** : Type "serendipity" dans nudge-engine, basé sur les connexions cross-module
**Effort estimé** : 1 jour (extension nudge-engine)
**Dépendances** : #97 (nudge-engine)

---

## #54 — Incubation d'idées (parking lot intelligent)

**Concept** : Les idées rejetées ou déprioritisées ne sont pas supprimées — elles entrent en "incubation" et sont re-proposées quand le contexte change. "Une feature rejetée il y a 3 mois car trop complexe est maintenant faisable car on a ajouté le module X."

**Challenge ⚡ Victor** : "C'est un backlog. Rien de nouveau."
→ Un backlog est passif. L'incubateur est ACTIF : il réévalue les idées incubées à chaque changement de contexte (nouveau module ajouté, nouvelle lib disponible, nouvelle compétence acquise). C'est un backlog avec un brain.

**Challenge 🔬 Dr. Quinn** : "Comment savoir que le contexte a changé de manière pertinente pour une idée spécifique ?"
→ Chaque idée incubée a un champ "conditions de viabilité" (ex: "nécessite Redis", "nécessite expertise ML"). Le system check ces conditions périodiquement.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 3 | 4 | 3 | 4 | 4 | 4 | **43** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale**
**Implémentation** : `incubator.yaml` avec conditions de viabilité + check dans `nso run`
**Effort estimé** : 2 jours
**Dépendances** : NSO existant

---

## #55 — Fractales (architecture auto-similaire)

**Concept** : Le même pattern à chaque échelle : un agent est une mini-team, une team est un mini-module, un module est un mini-projet. Les interfaces sont identiques à chaque niveau.

**Challenge 🏗️ Winston** : "L'architecture team-of-teams est DÉJÀ fractale par design."
→ Partiellement. Mais les interfaces ne sont PAS identiques : un agent a un menu, une team a un manifest, un module a un config.yaml. L'idée est d'UNIFIER l'interface : chaque niveau expose les mêmes primitives (activate, execute, report, learn).

**Challenge 🔬 Dr. Quinn** : "L'uniformité force peut contraindre des besoins différents."
→ L'interface est uniforme, l'implémentation est spécifique. Comme HTTP : tout est GET/POST/PUT/DELETE, mais les backends sont tous différents.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 3 | 4 | 3 | 4 | 3 | 4 | **41** 🟡 |

**Verdict : 🟡 VALIDÉ — Priorité normale. Définir les "primitives universelles" pour chaque niveau.**
**Implémentation** : Spec "BMAD Universal Interface" : activate, execute, report, learn pour agent/team/module
**Effort estimé** : 3 jours
**Dépendances** : Refactoring des manifests

---

## #56 — Bioluminescence (dashboard temps réel)

**Concept** : Visualisation en temps réel de tout ce qui se passe dans BMAD : flux de données, décisions, interactions entre agents, phéromones stigmergiques, scores de fitness, alertes early-warning.

**Challenge ⚡ Victor** : "Un dashboard nécessite un front-end. Le kit est CLI/markdown."
→ Options : (1) ASCII dashboard dans le terminal (comme htop), (2) Markdown dashboard généré et ouvert dans l'IDE, (3) Simple HTML statique généré, ouvert dans le navigateur, (4) Excalidraw/Mermaid dans l'IDE.

**Challenge 🔬 Dr. Quinn** : "Le temps réel est impossible sans processus serveur."
→ Pas du vrai temps réel. Un "dashboard" généré à la demande qui montre l'état courant. `bmad-init.sh dashboard` → génère un HTML/MD avec l'état complet.

**Challenge 🎨 Maya** : "Un dashboard qui n'est pas en temps réel, c'est un rapport."
→ Fair point. On peut faire du pseudo-temps-réel : le dashboard est un fichier Markdown dans l'IDE qui est régénéré à chaque changement d'état (via hooks). VS Code auto-refresh le preview.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 5 | 4 | 2 | 5 | 3 | 5 | **47** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute — Killer feature UX**
**Implémentation** :
1. `bmad-init.sh dashboard` — génère `_bmad-output/dashboard.md` 
2. Sections : état projet, agents actifs, phéromones, fitness, early-warning, stories en cours
3. Mermaid diagrams pour les graphes de dépendances
4. Mode watch : régénération auto quand `_bmad-output/` change
**Effort estimé** : 5-7 jours
**Dépendances** : Toutes les métriques existantes (bench, antifragile, stigmergy, etc.)

---

## #58 — Quorum sensing (changement de comportement collectif)

**Concept** : Les agents changent de mode collectivement quand un seuil est atteint. Ex: 3 agents signalent un risque sécurité → auto-activation mode security-first. 2 agents détectent une deadline à risque → mode crunch.

**Challenge ⚡ Victor** : "C'est de la stigmergie + des triggers."
→ Exact — c'est une EXTENSION de stigmergy. La stigmergie pose les phéromones, le quorum sensing INTERPRÈTE la densité de phéromones pour déclencher des changements de mode collectifs. L'un ne fonctionne pas bien sans l'autre.

**Challenge 🏗️ Winston** : "Comment définir les seuils ?"
→ Seuils par défaut + configurables dans project-context. Ex: `quorum_security: 2` (2 signaux sécurité → mode security-first), `quorum_deadline: 3` (3 signaux retard → mode crunch).

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 4 | 3 | 5 | 3 | 4 | **46** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute — Extension naturelle de stigmergy**
**Implémentation** :
1. `stigmergy quorum` — analyse les phéromones actives pour détecter les seuils
2. Modes collectifs : normal, security-first, crunch, quality-focus
3. Seuils configurables dans project-context
4. Intégration NSO : `nso run` inclut quorum check
**Effort estimé** : 2-3 jours
**Dépendances** : stigmergy existant

---

## #78 — Théorie des graphes (modélisation graphe)

**Concept** : Modéliser tout l'écosystème BMAD comme un graphe : agents = nœuds, interactions = arêtes, workflows = chemins, dépendances = arêtes pondérées. Utiliser les algorithmes de graphe pour : centralité (quel agent est le plus connecté ?), clustering (quels modules forment des groupes naturels ?), plus court chemin (quelle est la route optimale entre deux artefacts ?).

**Challenge ⚡ Victor** : "Joli en théorie. En pratique, qui regarde un graphe ?"
→ Le DASHBOARD (#56). Le graphe est la structure de données sous-jacente, le dashboard est la visualisation. Sans le graphe, le dashboard est une liste. Avec le graphe, c'est une MAP interactive.

**Challenge 🔬 Dr. Quinn** : "Construire et maintenir le graphe a un coût."
→ Le graphe est construit AUTOMATIQUEMENT à partir des manifests, workflows, et BMAD_TRACE. Pas de maintenance manuelle. `import` dans les workflows + `dependencies` dans les manifests = arêtes auto-détectées.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 3 | 3 | 3 | 5 | 3 | 4 | **40** 🟡 |

**Verdict : 🟡 VALIDÉ — Infrastructure technique pour #56, #48, #116**
**Implémentation** : `project-graph.py` — construit et requête le graphe du projet
**Effort estimé** : 4-5 jours
**Dépendances** : Enabling pour #56, #48, #25

---

## #136 — Système immunitaire (security à 2 niveaux)

**Concept** : Réponse INNÉE (règles toujours actives : no secrets in code, no SQL injection patterns, dependency audit) + réponse ADAPTATIVE (apprend des incidents passés : "ce type de config a causé une faille sur le projet X, flag automatique").

**Challenge ⚡ Victor** : "CC verify fait déjà des checks sécurité."
→ CC verify fait des checks STATIQUES prédéfinis. Le système immunitaire APPREND des incidents. La première fois qu'une XSS est trouvée, elle va dans le failure museum. La fois suivante, l'agent la détecte AVANT.

**Challenge 🔬 Dr. Quinn** : "L'adaptatif nécessite des incidents pour apprendre. Chicken-and-egg."
→ On boot avec une "bibliothèque d'anticorps" : OWASP Top 10, CWE communs, patterns de vulnérabilités connus. L'adaptatif enrichit cette base avec les incidents projet-spécifiques.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 4 | 4 | 3 | 5 | 3 | 4 | **46** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. `security-innate.yaml` — règles statiques toujours actives (OWASP, etc.)
2. `security-adaptive.yaml` — auto-alimenté par failure museum incidents sécurité
3. Check intégré dans CC verify : `cc-verify.sh --security`
4. Learning loop : incident → pattern extrait → ajouté à adaptive
**Effort estimé** : 4-5 jours
**Dépendances** : CC verify existant, failure museum

---

## #176 — Oracle introspectif (auto-SWOT du projet)

**Concept** : Un agent qui analyse le projet lui-même : forces (stack solide, bonne couverture test), faiblesses (documentation manquante, single point of failure), opportunités (nouvelle lib disponible, pattern cross-projet utile), menaces (dépendance EOL, dette technique croissante).

**Challenge ⚡ Victor** : "Le NSO + antifragile score font déjà de l'introspection."
→ Ils font de l'introspection QUANTITATIVE (scores, métriques). L'Oracle fait de l'introspection QUALITATIVE et STRATÉGIQUE. Le NSO dit "score antifragile = 72%". L'Oracle dit "Ta force principale est la couverture test à 95%, mais ta dépendance à Redis sans fallback est un single point of failure stratégique."

**Challenge 📋 John** : "C'est du consulting automatisé. Utile ?"
→ TRÈS utile pour un solo dev qui n'a pas de CTO/tech lead pour prendre du recul. L'Oracle est le CTO virtuel qui fait la review stratégique que personne ne fait sur les petits projets.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 5 | 5 | 3 | 5 | 3 | 5 | **52** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute — Unique sur le marché**
**Implémentation** :
1. `bmad-init.sh oracle` — analyse stratégique complète
2. Inputs : project-context, BMAD_TRACE, failure museum, bench scores, dependency audit
3. Output : rapport SWOT structuré avec recommandations priorisées
4. Intégration NSO : `nso retro` inclut Oracle summary
**Effort estimé** : 4-5 jours
**Dépendances** : Toutes les données existantes

---

## #191 — Autocatalyse (workflows auto-améliorants)

**Concept** : Chaque exécution de workflow rafine le workflow lui-même pour la suivante. Les timings sont collectés, les étapes problématiques identifiées, les defaults ajustés.

**Challenge ⚡ Victor** : "C'est #12 (plasticité synaptique) reformulé."
→ Oui, c'est très proche. La nuance : #12 = adaptation des CHEMINS (quelles étapes). #191 = adaptation des PARAMÈTRES (quels defaults, quels seuils, quels prompts). Mais en pratique, fusionnables.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 4 | 4 | 3 | 4 | 3 | 4 | **43** 🟡 |

**Verdict : 🟡 VALIDÉ — Fusionner avec #12 (Plasticité synaptique). Un seul système "Adaptive Workflows".**

---

## #197 — Algorithme de recommandation

**Concept** : "Les devs qui ont utilisé ce workflow ont aussi aimé..." Suggestions basées sur les patterns d'usage similaires cross-projets.

**Challenge ⚡ Victor** : "Ça nécessite une base d'utilisateurs. On l'a pas."
→ Correct pour du collaborative filtering. Mais on peut faire du content-based : "Ce workflow est similaire à ceux que tu utilises souvent (même tags, même complexité, même domain)." Pas besoin d'autres utilisateurs.

**Challenge 🔬 Dr. Quinn** : "Avec Mycelium (#2), on AURAIT la base d'utilisateurs à terme."
→ Exact. C'est un use case naturel du Mycelium Network. En standalone, c'est du content-based. En réseau, c'est du collaborative.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 3 | 3 | 3 | 3 | 4 | 4 | 3 | **38** 🟡 |

**Verdict : 🟡 VALIDÉ — Phase 2 de Mycelium Network**
**Implémentation** : Extension de `cross-migrate` + Mycelium avec matching de patterns similaires
**Effort estimé** : 3 jours
**Dépendances** : #2 (Mycelium)

---

## #209 — New Game+ (héritage complet cross-projets)

**Concept** : Quand on démarre un projet similaire à un précédent, hériter de TOUT : learnings, patterns validés, workflows adaptés, DNA évoluée, agents optimisés.

**Challenge ⚡ Victor** : "C'est cross-migrate + un archetype enrichi. Pas nouveau."
→ Cross-migrate exporte des bundles génériques. New Game+ est spécifique : il identifie le projet SOURCE le plus similaire et crée un archetype personnalisé basé sur sa DNA évoluée. C'est un archetype DYNAMIQUE, pas statique.

**Challenge 🏗️ Winston** : "Comment déterminer 'similaire' ?"
→ Stack matching + domain matching. Un projet Go+API est similaire à un autre Go+API. Un projet Terraform infra est similaire à un autre Terraform infra. Le stack détecté par MTE + les tags du project-context.

| F | V | U | C | S | R | D | **Score** |
|---|---|---|---|---|---|---|-----------|
| 4 | 5 | 4 | 3 | 5 | 3 | 5 | **50** ✅ |

**Verdict : ✅ VALIDÉ — Priorité haute**
**Implémentation** :
1. `bmad-init.sh --from-project /path/to/previous-project`
2. Auto-détection stack similarity
3. Import sélectif : DNA, learnings validés, workflow adaptations, agents performants
4. Customization post-import pour les spécificités du nouveau projet
**Effort estimé** : 4-5 jours
**Dépendances** : cross-migrate, dna-evolve existants

---

## TIER 2 — Reste (35 idées) — Évaluation batch

### ✅ VALIDÉES — Priorité haute

| # | Concept | Score | Note clé | Effort |
|---|---------|-------|----------|--------|
| 26 | **Self-healing workflows** | **46** | Quand un workflow échoue, tente auto-correction (retry, alternative path, rollback) avant de reporter l'échec humain. Unique. | 5j |
| 77 | **Réverbération** | **45** | Tracer l'impact d'un changement sur TOUS les artefacts connectés. Étend #116. Graphe de propagation. | 3j |
| 91 | **Matière noire** | **47** | Détecter et documenter les conventions non-écrites, le savoir tribal, les décisions implicites. Agent "dark matter detector". | 3j |

### 🟡 VALIDÉES — Priorité normale

| # | Concept | Score | Note clé | Effort |
|---|---------|-------|----------|--------|
| 8 | Biomimétisme structurel | 37 | Workflows minimalistes, renforcés aux points de stress identifiés par BMAD_TRACE | 2j |
| 9 | Rhizome | 38 | Tout agent = point d'entrée valide. Pas de hiérarchie rigide. | 1j |
| 19 | Neurones miroirs | 36 | Détection ton/frustration dans les messages user. Adaptation empathique. | 2j |
| 21 | Hémisphères | 39 | Phases divergentes (brainstorm) puis convergentes (décision) explicites dans chaque workflow | 1j |
| 24 | Blockchain décisions | 38 | Ledger immuable de décisions architecturales. Extension ADR avec hash + chaînage. | 2j |
| 29 | Hot-swapping | 40 | Remplacer un agent mid-workflow via state serialization. | 3j |
| 33 | Time-travel debugging | 41 | Replay d'un workflow passé step-by-step pour comprendre une décision. Via BMAD_TRACE. | 3j |
| 35 | JIT workflows | 39 | Workflows qui se compilent/optimisent basé sur le contexte. Overlay dynamique (#12). | Fusionné #12 |
| 37 | Mèmes viraux | 36 | Patterns réussis se répliquent automatiquement. Extension Mycelium (#2). | Fusionné #2 |
| 41 | Effet réseau | 35 | Interopérabilité croît la valeur. Spec d'interface universelle (#55 Fractales). | Fusionné #55 |
| 45 | Économie attention | 40 | Score de pertinence pour chaque info chargée dans le context window. | 2j |
| 53 | Mémoire sensorielle | 37 | Buffer ultra-court qui capture tout avant filtrage. Étend state-checkpoint. | 2j |
| 60 | Tectonique | 36 | Modules qui "collisionnent" = nouvelles features. Sérendipité planifiée. | Fusionné #52 |
| 61 | Voyage du Héros | 37 | Structure narrative du projet comme framework motivationnel. | 1j |
| 62 | Inconscient collectif | 35 | Patterns archétypaux partagés entre agents. Base de "maximes universelles". | 1j |
| 67 | Catalyse | 38 | Agents catalyseurs qui accélèrent les interactions. Le SM existant est un catalyseur. | 1j |
| 68 | Cristallisation | 40 | Process structuré : idée floue → draft → review → spec solide. Étapes explicites. | 1j |
| 69 | Osmose | 36 | Savoir circule depuis les agents riches en contexte vers les pauvres. Auto-share. | 2j |
| 70 | Résonance | 37 | Détection paires d'agents performantes. Extension #6 (Symbiose). | Fusionné #6 |
| 79 | Fractales Mandelbrot | 36 | Templates qui scale. Un workflow fonctionne pour 1 story ou 100. | 1j |
| 82 | Fourier | 37 | Décomposer problème complexe en composantes. Framework de problem decomposition. | 2j |
| 83 | Attracteurs | 38 | Identifier vers quoi le projet tend naturellement. Extension Oracle (#176). | Fusionné #176 |
| 92 | Moindre action | 39 | Optimiser workflow pour le chemin de moindre effort. Extension #12 (plasticité). | Fusionné #12 |
| 112 | Fermentation | 38 | Cool-down obligatoire entre brainstorm et implémentation. Configurable. | 0.5j |
| 121 | Multivers | 39 | Session branching étendu. Explorer N architectures en parallèle et comparer. | 2j |
| 137 | CRISPR | 39 | Édition chirurgicale d'un workflow. `workflow-edit` tool précis. | 2j |
| 139 | Succession écologique | 37 | Phases projet : pioneer → growth → mature. Adaptation workflows par phase. | 1j |
| 141 | Dormance | 38 | Features/agents en veille, réactivation contextuelle. Extension incubator (#54). | Fusionné #54 |
| 166 | Bulle spéculative | 40 | Détection hype autour d'une techno/feature. Contrarian agent. | 1j |
| 179 | Hydre de Lerne | 41 | Root cause analysis formalisé. Bugs qui se multiplient quand traités en surface. | 2j |
| 213 | Criticalité | 42 | Détection accumulation critique. Extension #48 (early warning). | Fusionné #48 |
| 221 | Épidémiologie | 39 | Contact tracing pour bugs. Propagation analysis dans le graphe. | 2j |

### 🟠 EN SURSIS / FUSIONNÉES

| # | Concept | Décision |
|---|---------|----------|
| 27 | Federated Learning | Fusionné avec #2 (Mycelium) |
| 42 | Théorie des jeux | Fusionné avec #17 (Context Router) |
| 191 | Autocatalyse | Fusionné avec #12 (Plasticité) |
| 35 | JIT workflows | Fusionné avec #12 |
| 37 | Mèmes viraux | Fusionné avec #2 |
| 41 | Effet réseau | Fusionné avec #55 |
| 60 | Tectonique | Fusionné avec #52 |
| 70 | Résonance | Fusionné avec #6 |
| 83 | Attracteurs | Fusionné avec #176 |
| 92 | Moindre action | Fusionné avec #12 |
| 141 | Dormance | Fusionné avec #54 |
| 213 | Criticalité | Fusionné avec #48 |

