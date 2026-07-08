# Brainstorm P4 — Promouvoir la stigmergie (R&D → cœur)

Date : 2026-07-08. Contexte : P0-P3 livrés (CLI `grimoire stigmergy`, hooks
non bloquants `install-hooks`, vue live `/api/stigmergy` + observatoire). La
feature est **vivante et observable** mais toujours estampillée **R&D**
(`docs/rnd.md`, hors contrat SemVer).

Ce document n'implémente rien : il pose la décision « faut-il, et comment,
sortir la stigmergie du R&D ? » avec options, critères et verdicts.

## 1. Ce que « promouvoir » signifie concrètement

Sortir une feature du R&D, ce n'est pas cosmétique — c'est un engagement :

- **Contrat SemVer** : le format du board, les types de signaux et le contrat
  CLI deviennent stables. Un changement cassant impose un bump majeur.
- **Retrait de `docs/rnd.md`** + entrée dans le README/guides comme capacité
  de première classe, documentée et supportée.
- **Dette de maintenance assumée** : la duplication SDK ⧸ script autonome ⧸
  logique de hook devient une responsabilité de stabilité, plus un détail.
- **Promesse d'utilité** : on affirme que ça aide vraiment, pas que « ça marche ».

Corollaire : promouvoir trop tôt fige des choix qu'on regrettera ; ne jamais
promouvoir laisse une capacité utile dans un statut qui décourage l'adoption.

## 2. La question qui précède tout : est-ce utile ?

Aujourd'hui on sait que le système **fonctionne** (signaux émis, captés,
renforcés, évaporés, observés). On ne sait pas encore s'il **change le
comportement** des agents — c'est la seule chose qui justifie la promotion.

Il faut de la preuve d'usage, pas une intuition. Trois questions mesurables :

1. **Le signal mène-t-il à l'action ?** Un `NEED`/`ALERT`/`BLOCK` est-il suivi
   d'un travail dans la même zone par un autre agent (relais), ou meurt-il par
   évaporation sans effet ?
2. **Le bruit est-il maîtrisé ?** Ratio signaux utiles (résolus / relayés) vs
   signaux évaporés sans interaction. Un board que personne ne lit = bruit.
3. **Le contexte injecté est-il lu ?** Le résumé `SessionStart` change-t-il
   une décision d'agent, ou est-il ignoré ?

**Verdict** : sans instrumentation de ces trois ratios, la promotion est un
pari. La première étape de P4 n'est pas de promouvoir — c'est de **mesurer**.

## 3. Métriques à instrumenter (avant toute promotion)

Réutiliser le ledger d'événements existant (`events.jsonl`) plutôt qu'un
système parallèle :

| Métrique | Ce qu'elle prouve |
|---|---|
| Taux de relais (COMPLETE→NEED/PROGRESS zone, agent ≠) | Le board coordonne réellement |
| Taux de résolution vs évaporation | Les signaux servent, ou pourrissent |
| Profondeur de renfort moyenne | Les pistes convergent (utile) ou restent plates |
| Signaux actifs par session | Densité exploitable vs désert/déluge |
| Corrélation sense→action | Le contexte injecté influence le comportement |

Sans ces chiffres, on ne saura pas distinguer « feature cool » de « feature
utile ». Avec, la décision de promotion devient factuelle.

## 4. Questions de conception à trancher AVANT de figer l'API

Promouvoir = figer. Donc résoudre d'abord :

1. **Portée de l'émission automatique.** Aujourd'hui les hooks n'émettent que
   `PROGRESS` (édition) et `COMPLETE` (stop) — les signaux les plus sûrs.
   Faut-il auto-émettre `ALERT` (échec de commande, secret détecté), `NEED`
   (délégation d'agent), `BLOCK` (erreur bloquante) ? Chacun ajoute de la
   valeur *et* du risque de bruit/faux positifs. À décider signal par signal.
2. **La dualité d'implémentation.** SDK (paquet) + script autonome + logique de
   hook = trois copies parité-testées. Acceptable en R&D ; en cœur stable,
   c'est une dette. Faut-il un générateur (une source → les copies) avant de
   promettre la stabilité ? Ou assumer les trois avec le test de parité comme
   garde ?
3. **Portée de la captation.** `SessionStart` seulement, ou aussi injection en
   cours de session (UserPromptSubmit) quand un signal chaud apparaît ?
4. **Rétention / GC du board.** L'évaporation est paresseuse + purge au Stop.
   Suffisant, ou faut-il une politique de rétention explicite (taille max,
   archivage) pour un usage long ?
5. **Sémantique multi-agents.** `emitter` est libre aujourd'hui. Pour de la
   vraie coordination inter-agents, faut-il un registre d'émetteurs, des
   permissions par type de signal ?

## 5. Options de trajectoire

- **Option A — Statu quo (rester R&D).** Zéro engagement, zéro dette de
  stabilité. La feature vit, s'améliore, s'observe. Coût : reste « niche »,
  peu découverte, peu adoptée.
- **Option B — Promotion graduée (recommandée).** Promouvoir par **couches de
  maturité** différentes, pas en bloc :
  - *Stable maintenant* : le **format de board** + la **CLI** (`emit/sense/
    trails/...`). Ils sont simples, testés, sans effet de bord. Peu de risque
    à figer.
  - *Reste expérimental* : l'**auto-émission par hooks** (les règles d'émission
    sont des heuristiques v1, à valider par les métriques du §3).
  Ainsi un utilisateur peut s'appuyer sur la CLI/board stables tout en sachant
  que le câblage automatique bouge encore.
- **Option C — Promotion complète.** Tout stable, retrait de rnd.md. Prématuré
  tant que §2/§3 ne sont pas verts.
- **Option D — Découplage en paquet optionnel.** Sortir la stigmergie dans un
  extra (`grimoire-kit[stigmergy]`) : isole la dette, signale le caractère
  optionnel, permet un cycle de version propre. Utile si ça reste niche.
- **Option E — Déprécation.** Si les métriques montrent que personne n'exploite
  le board, retirer proprement plutôt que maintenir une capacité morte.

## 6. Chemin de promotion proposé (si on y va)

1. **Instrumenter** les métriques du §3 (réutiliser `events.jsonl`).
2. **Collecter** sur un usage réel (≥ un projet, board non trivial exploité).
3. **Geler l'API stable** : format board + contrat CLI → SemVer. Retrait
   partiel de rnd.md (la CLI/board sortent ; les hooks restent marqués R&D).
4. **Itérer les règles d'émission** derrière le flag expérimental jusqu'à un
   ratio bruit acceptable, puis promouvoir les hooks.
5. **Décider la dualité** : générateur ou parité-test assumée, documenté.

## 7. Critères de sortie (la barre à franchir)

Promotion d'une couche seulement si **tous** vrais pour cette couche :

- Usage récurrent démontré sur ≥ 1 projet réel (données du §3, pas anecdote).
- Ratio signaux utiles / évaporés au-dessus d'un seuil décidé (ex. > 40 %).
- API/format figés et couverts par tests (déjà le cas pour board + CLI).
- Documentation de première classe prête (hors rnd.md).
- Dette de duplication tranchée (générateur ou parité assumée).

## 8. Recommandation

**Ne pas promouvoir maintenant. Instrumenter d'abord (Option B, étape 1).**

La feature est vivante mais on manque la seule preuve qui compte : qu'elle
change le comportement des agents. Le prochain incrément à faible risque et à
forte valeur décisionnelle est d'ajouter les métriques du §3 (elles se
branchent sur le ledger existant, sans nouvel engagement). Une fois les
chiffres en main, la **promotion graduée** (CLI/board stables d'abord, hooks
ensuite) est la trajectoire honnête : elle donne de la stabilité là où le
risque est faible, sans figer prématurément les heuristiques d'émission.

Si, à la mesure, le board reste désert, **Option E (déprécation)** est un
résultat acceptable — mieux qu'une capacité morte maintenue par principe.
