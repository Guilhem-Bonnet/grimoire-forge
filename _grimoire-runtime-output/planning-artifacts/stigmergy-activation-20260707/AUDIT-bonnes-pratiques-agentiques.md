# Audit — l'atelier au crible de son propre catalogue agentique

Date : 2026-07-08. Méthode : évaluer le code livré ce cycle (serve, atelier,
hooks stigmergiques, canal de features, blueprint) contre les **52
anti-patterns** et les patterns du catalogue normatif
(`catalogue-export.json`, 78 patterns). Principe : l'outil qui prêche la
gouvernance agentique doit se l'appliquer à lui-même.

Chaque constat cite l'anti-pattern violé et le pattern qui porte le correctif.

## Constats — à corriger

### 1. `install_hooks` sans compensation — anti-pattern **effet-partiel-oublié**

`src/grimoire/tools/stigmergy_hooks.py` copie 6 fichiers puis journalise. Si
la copie échoue au 4ᵉ fichier, les 3 premiers restent en place : installation
partielle, aucun rollback. C'est exactement *« une séquence échoue en cours
sans compenser les effets déjà produits »*.

- **Pattern correctif** : RUN-14 (Compensation / rollback action).
- **Fix** : suivre les fichiers écrits, tout retirer sur exception ; ne
  journaliser dans le registre qu'après succès complet.

### 2. Journal phéromonal sans janitor — anti-pattern **tout-indexer**

`stigmergy-events.jsonl` (écrit par les hooks ET la CLI via `log_event`) est
append-only sans borne. Ironie : le board *s'évapore* (demi-vie), mais son
journal grandit indéfiniment. *« Chaque trace devient mémoire durable. »*

- **Patterns correctifs** : KNO-01 (Knowledge janitor), RUN-02 (Runtime
  output governance).
- **Fix** : rotation/plafond (garder les N derniers événements ou D jours),
  cohérent avec la philosophie de décroissance du système lui-même.

### 3. État de features non versionné — anti-pattern **save-non-versionnée**

`_grimoire/features.json` n'a **pas** de champ `version`/`schema` ; les entrées
du journal non plus. Le board l'a (`"version":"1.0.0"`), le blueprint aussi
(`blueprintVersion`). Incohérence de gouvernance des états persistés.

- **Pattern correctif** : RUN-02 + logique de migration (cf. `migration-v2-v3`).
- **Fix** : ajouter `"schemaVersion"` à `features.json` et aux événements,
  pour permettre une migration silencieuse plus tard.

### 4. Observabilité des mutations serve — anti-pattern **backend-permissif**

`grimoire serve` est silencieux (`log_message` no-op). Les endpoints
**mutants** (`/api/features/<id>` toggle, `/api/extensions/add|remove`,
`/api/blueprints/<id>/compile`) n'émettent aucune trace gouvernée. *« Les
opérations serveur ne sont ni observées ni tracées. »* (localhost atténue le
risque débit, pas le manque de traçabilité.)

- **Patterns correctifs** : QUA-08 (Agent telemetry plane), RUN-02.
- **Fix** : émettre un événement gouverné sur chaque mutation (append au
  ledger `events.jsonl` du projet), GET restant silencieux.

### 5. Drift interne « expérimental » vs « beta » — anti-pattern **drift-documentaire**

*Introduit ce cycle.* `cmd_stigmergy.py` (docstring + `--help`) annonce
« expérimental (R&D, hors contrat SemVer) », mais `features.py` classe la
stigmergie en **beta** et `cli-reference.md` dit « beta ». `rnd.md` la liste
encore comme pur expérimental. La doc affirme un canal que le registre
n'applique plus. **Corrigé inline** (docstring/help → beta ; note rnd.md).

- **Pattern correctif** : KNO-03 (Doc drift detector).

## Constats — jugement (softer)

### 6. Compilation tolère l'absence de preuve — anti-pattern **faux-done**

`blueprint_compile` ne bloque que sur les `blockers` (erreurs). Un flow sans
**aucun** pattern de preuve QUA compile quand même (simple *warning*). Pour un
brouillon c'est le bon niveau ; mais compiler un artefact **gouverné** sans la
moindre porte de preuve frôle le *« done sans preuve »*.

- **Pattern de référence** : QUA-05 (Evidence-driven transition).
- **Option** : passer « zéro pattern QUA dans un flow multi-nodes » de warning
  à blocker *au moment de la compilation* (pas de l'édition).

### 7. Métriques sans hypothèse affichée — anti-pattern **mesure-sans-hypothèse**

`/api/stigmergy.behavior` expose les bons ratios (usefulRatio…) mais sans
l'hypothèse ni le seuil de promotion. Les chiffres existent, la thèse qu'ils
testent n'est pas surfacée.

- **Pattern correctif** : QUA-13 (Eval lifecycle).
- **Fix** : joindre au bloc `behavior` la cible (`targetUsefulRatio: 0.4`) et
  l'état (`promotionReady: bool`), pour que la mesure serve une décision.

## Ce qui est bien fait (patterns correctement appliqués — à préserver)

- **hook-marteau évité** → GOV-03 (Hook lifecycle progressif) : les hooks
  stigmergiques sont non bloquants *par construction* (émettent contexte ou
  `{}`), démarrés en shadow. Modèle exemplaire.
- **validation-circulaire évitée** → QUA-15 (Independent reviewer) : la
  simulation client consulte le **verdict serveur indépendant** ; le
  producteur ne valide pas seul sa sortie critique.
- **outil-adopté-sans-accord évité** → RUN-15 : `install-hooks` est un opt-in
  explicite ; rien ne se câble sans geste utilisateur.
- **autonomie-maximale évitée** → GOV-04 (Autonomie gouvernée) : émission
  automatique désactivée par défaut, gated par flag, désactivable sans
  désinstaller.
- **parité anti-dérive** → esprit KNO-07 (Memory integrity validator) : les
  implémentations multiples de stigmergie sont tenues par un test de parité.

## Méta

Les deux constats les plus nets (rollback partiel, journal sans janitor)
correspondent à des patterns du **propre catalogue** de l'outil (RUN-14,
KNO-01). C'est le meilleur signe que l'audit vaut : le blueprint qui
imposerait ces patterns à un projet utilisateur devrait d'abord les voir
appliqués dans le kit qui le sert.

## Priorisation

1. **effet-partiel-oublié** (rollback install_hooks) — sûreté, petit, net.
2. **backend-permissif** (observer les mutations serve) — gouvernance, moyen.
3. **tout-indexer** (janitor du journal) — cohérence, petit.
4. **save-non-versionnée** (schemaVersion) — dette future, trivial.
5. **mesure-sans-hypothèse** (seuil dans behavior) — décisionnel, trivial.
6. **faux-done** (porte de preuve à la compilation) — à débattre (UX vs rigueur).
