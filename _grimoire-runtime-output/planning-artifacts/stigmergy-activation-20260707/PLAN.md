# Plan — Activer le système stigmergique (phéromones)

Date : 2026-07-07. Cible : dépôt public `Guilhem-Bonnet/Grimoire-kit`.
Statut du concept : **R&D expérimental** (`docs/rnd.md`, hors contrat SemVer).

## État d'avancement (2026-07-08)

Branche `feat/site-atelier` (PR #64). **P0 à P3 (cœur) livrés et vérifiés E2E.**

- **P0 livré** (`7c4f90d`) — commande `grimoire stigmergy` + test de parité
  anti-dérive SDK ⧸ script autonome.
- **P1+P2+P3 cœur livrés** (`0db237f`) — hooks non bloquants (SessionStart
  sense, PostToolUse emit-renfort, Stop complete+purge) sous
  `framework/tools/stigmergy_hooks/`, câblés par
  `grimoire stigmergy install-hooks` (mode shadow). 19 tests.
  Choix d'archi : **pas** une extension marketplace (la stigmergie ne s'ancre
  honnêtement sur aucun pattern gouverné) ; hooks safe par construction.
- **Reste** : P3 *surface visuelle observatoire* (fork à trancher : snapshot
  via `gen-site-data` ⧸ live via endpoint `serve /api/stigmergy`) et **P4**
  (critères de promotion R&D → cœur, gaté sur usage réel).

## Constat vérifié

Ce qui **fonctionne déjà** (exécuté et confirmé) :

- Outil complet côté `framework/tools/stigmergy.py` (CLI argparse) :
  `emit`, `sense`, `amplify`, `resolve`, `evaporate`, `landscape`, `trails`,
  `stats`, `urgency`. Board persisté dans `_grimoire-output/pheromone-board.json`.
- Décroissance **paresseuse** : intensité `= intensité × 0.5^(âge/demi-vie)`,
  demi-vie 72 h, calculée à la lecture. **Aucun démon requis.**
- Détection de patterns émergents : hot-zone, cold-zone, convergence,
  bottleneck, relay.
- Classe SDK `grimoire.tools.Stigmergy` exportée, interface `run(action=…)`.

Ce qui **manque** pour que le système soit vivant :

1. **Aucune émission automatique.** Rien dans le cycle de vie agent ne dépose
   de signaux. Seul `dream.py` émet (en chargeant `stigmergy.py` par chemin).
   Le board reste vide tant qu'on n'émet pas manuellement.
2. **Aucune captation automatique.** Même si des signaux existaient, aucun
   agent ne lit le board au démarrage — le comportement ne s'adapte pas.
3. **Pas de commande `grimoire stigmergy`** de premier niveau. Accessible
   seulement via `grimoire-init.sh stigmergy …` (shell) ou le module direct.
   Même trou que `grimoire serve` avant son correctif.
4. **Deux implémentations divergentes** : `src/grimoire/tools/stigmergy.py`
   (528 lignes, SDK) ⧸ `framework/tools/stigmergy.py` (1011 lignes, CLI +
   `landscape`/`stats`/`trails`/`urgency`). Risque de dérive ; la version SDK
   est un sous-ensemble.
5. **Entretien manuel.** `evaporate` (purge des signaux morts) n'est jamais
   planifié — mineur, la décroissance étant déjà paresseuse.

## Décision préalable (à trancher avant tout code)

C'est une feature R&D. L'investissement dépend d'un choix :

- **Option A — Consolider sans promouvoir.** Corriger seulement les trous
  d'hygiène : dédupliquer les deux copies, exposer `grimoire stigmergy` en
  CLI, documenter honnêtement l'usage manuel. La coordination reste pilotée
  par le prompt des agents (ils appellent `stigmergy emit` quand pertinent).
  *Faible risque, faible surface, cohérent avec le statut expérimental.*
- **Option B — Rendre le système vivant.** En plus de A : câbler l'émission
  et la captation dans le cycle de vie via des hooks (mode `shadow`), pour que
  le board se remplisse et s'exploite sans geste manuel.
  *Plus de valeur démontrable, mais surface de contrôle agentique nouvelle —
  gouvernance stricte requise.*

**Recommandation** : viser B **par étapes**, en livrant A d'abord (P0) comme
socle réutilisable et sans risque, puis P1/P2 derrière un flag, avec critères
de promotion explicites. Ne pas promouvoir hors R&D tant que P4 n'est pas vert.

## Plan par phases

### P0 — Socle propre (Option A)

Objectif : une seule implémentation, une commande de premier niveau.

- Faire de `src/grimoire/tools/stigmergy.py` la **source de vérité** (fonctions
  pures + classe). Porter les fonctions manquantes depuis la copie framework
  (`landscape`, `stats`, `trails`, `urgency`) après un diff ligne à ligne.
- Réduire `framework/tools/stigmergy.py` à une **façade CLI** qui importe le
  module SDK (plus de logique dupliquée), ou la remplacer par le point 3.
- Ajouter `grimoire stigmergy <emit|sense|amplify|resolve|trails|evaporate|stats>`
  (nouveau `cmd_stigmergy.py`, même patron que `cmd_serve.py`), branché sur le
  module SDK. Marquer la commande « expérimental » dans l'aide.
- Corriger la doc d'usage (`framework/tools/README.md`, `docs/rnd.md`) pour
  pointer sur `grimoire stigmergy …` plutôt que `grimoire-init.sh …`.

Livrables : module unique, `cmd_stigmergy.py`, tests CLI, doc à jour.
Garde-fous : aucun. Aucune surface de contrôle nouvelle.
Effort : M. Risque : faible.

### P1 — Sentir (captation au démarrage)

Objectif : les agents voient les signaux actifs sans geste manuel.

- Hook `SessionStart` qui lit le board, filtre les phéromones au-dessus du
  seuil, et injecte un résumé compact via `additionalContext` (zones chaudes,
  blocages, besoins ouverts). Lecture seule — aucun effet de bord.
- Format concis (≤ quelques lignes) pour ne pas polluer le budget contexte.

Livrables : hook `grimoire-stigmergy-sense` (lecture seule), tests, capture.
Garde-fous : lecture seule, donc faible ; passe quand même par le registre de
sûreté des hooks du projet.
Effort : S. Risque : faible. Dépend de P0.

### P2 — Émettre (dépôt automatique)

Objectif : le board se remplit à partir de l'activité réelle.

- Hooks en **mode `shadow` obligatoire** (jamais bloquants), déclarés au
  registre de sûreté, dégradables :
  - `PostToolUse` : `ALERT` si un scan détecte un secret / une écriture hors
    périmètre ; `PROGRESS` sur une étape franchie.
  - `Stop` / `SubagentStop` : `COMPLETE` sur la zone travaillée.
  - `Subagent*` : `NEED` quand un agent délègue une expertise.
- Règles d'émission **conservatrices** : n'émettre que sur signaux nets, pour
  éviter le bruit qui rendrait le board inexploitable.
- Émetteur, zone (`location`), type dérivés du contexte du hook.

Livrables : hooks d'émission (shadow), entrées de registre, tests, exemple de
board rempli par une session réelle.
Garde-fous : `shadow` strict, budget d'émission (anti-bruit), pas de blocage.
Effort : L. Risque : moyen (surface de contrôle + bruit potentiel).
Dépend de P0, P1.

### P3 — Entretien + observabilité

Objectif : boucle complète, visible.

- Purge planifiée : tâche `grimoire stigmergy evaporate` (task/cron optionnel),
  ou purge opportuniste à chaque `sense` (déjà partiellement le cas).
- Surface visuelle : réutiliser la page **Observatoire** de l'atelier pour
  afficher le paysage phéromonique (zones chaudes, trails) — cohérent avec le
  reste du site branché sur données réelles.
- Exploiter la boucle `dream.py` ⇄ stigmergy déjà existante (dream lit et émet).

Livrables : task d'entretien, panneau observatoire, doc.
Effort : M. Risque : faible. Dépend de P2.

### P4 — Critères de promotion R&D → cœur

Ne promouvoir hors expérimental que si **tous** vrais :

- Usage récurrent démontré sur ≥ 1 projet réel (board non trivial, exploité).
- API stabilisée (types de signaux, contrat CLI, format board figés).
- Émission sans bruit mesurable (taux de signaux utiles vs résolus/évaporés).
- Couverture de tests des hooks + du module unique.
- Retrait de `docs/rnd.md` et entrée au contrat SemVer (voir CONTRIBUTING).

## Invariants et garde-fous

- **Pas de moteur parallèle** : on branche sur le cycle de hooks existant, on
  n'invente pas d'orchestration. Le board est un substrat de coordination, pas
  un exécutant.
- **Hooks toujours en `shadow`** à l'introduction, déclarés au registre de
  sûreté, promus manuellement seulement après validation.
- **Lecture seule d'abord** (P1) avant écriture (P2).
- **Statut expérimental** conservé jusqu'à P4 : API et format peuvent bouger.

## Ce que ce n'est pas

- Pas de « script d'entraînement » : aucune phase d'apprentissage, aucun modèle.
  La stigmergie est une coordination indirecte par signaux qui s'évaporent.
- Pas un service : le board est un fichier local, la décroissance est calculée
  à la lecture.
