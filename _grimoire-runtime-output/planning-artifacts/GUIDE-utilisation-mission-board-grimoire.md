---
title: Guide d'utilisation - Mission Board Grimoire
description: Guide d'usage cible du Mission Board pour creer, qualifier, router, suivre, verifier et cloturer une task sans perdre la causalite.
author: GitHub Copilot
date: 2026-04-16
---

## Guide d'utilisation — Mission Board Grimoire

## 1. Portee

Ce document decrit **l'usage cible** du `Mission Board` tel qu'il est specifie dans le package Mission Board.

Il documente comment un operateur doit lire et piloter le board. Il ne doit pas etre lu comme une promesse que chaque ecran existe deja dans le runtime code.

## 2. Ce que le board permet

Le board permet de :

- creer une task dans un backlog natif ;
- qualifier cette task avec ses criteres d'acceptation et son niveau de preuve ;
- comprendre pourquoi elle est routee vers une lane et une recipe ;
- suivre son execution sans la sortir de son contexte causal ;
- demander et lire la verification ;
- detecter un stall, une escalation ou une quarantine ;
- cloturer seulement quand les conditions canoniques sont reunies.

## 3. Parcours principal

### Etape 1 - Creer une task depuis `Intake Desk`

Vous renseignez :

- un titre clair ;
- une description ;
- des labels ;
- des criteres d'acceptation ;
- les options de ticket utiles : severite, dependances, `flowHint`, `evidenceProfile`, `policyPack`.

Avant confirmation, le board doit vous montrer un apercu de qualification et de routage. Vous devez pouvoir lire :

- la complexite estimee ;
- la lane cible ;
- la recipe cible ;
- la rationale courte de cette decision.

### Etape 2 - Qualifier et accepter le routage

Une task n'entre pas dans l'execution comme un simple post-it de kanban.

Vous verifiez :

- que les criteres d'acceptation sont suffisants ;
- que le niveau de preuve est correct ;
- que le routage est coherent ;
- qu'aucune dependance bloquante n'est oubliee.

Si le routage est mauvais, vous n'editez pas directement la colonne: vous passez par un override explicite et causal.

### Etape 3 - Suivre l'execution dans `War Room` et `Workshop`

Dans `War Room`, vous lisez la mission a l'echelle tactique :

- quelles tasks sont en `Intake`, `Qualified`, `Assigned`, `Running`, `Review`, `Verified`, `Blocked`, `Done` ;
- quelles dependances relient les cartes ;
- quelles cartes manquent de preuve ou de checkpoint.

Dans `Workshop`, vous regardez l'execution active :

- run courant ;
- checkpoint attendu ;
- step en cours ;
- prochaine action utile.

## 4. Lire une carte correctement

Une carte sert a piloter, pas a tout afficher.

Vous devez y trouver :

- le titre et le sous-titre ;
- l'etat operatoire ;
- la lane ;
- les compteurs de dependances, criteres et preuves ;
- les badges utiles ;
- l'action primaire conseillee.

Vous ne devez pas y trouver :

- un transcript brut ;
- un historique detaille complet ;
- une source de verite concurrente du ledger.

## 5. Ouvrir le drawer au bon moment

Le drawer donne le niveau `L2` de contexte.

Vous l'ouvrez pour :

- relire les criteres d'acceptation ;
- comprendre la rationale de routage ;
- verifier l'evidence gap ;
- lire le prochain checkpoint ;
- lancer les commandes autorisees.

Le drawer n'est pas fait pour remplacer `Seance Archive` ni les vues profondes de lineage.

## 6. Passer par `Branch Finisher`

Quand une task doit etre verifiee, vous passez par `Branch Finisher`.

Vous y regardez :

- le statut de verification ;
- les preuves rattachees ;
- les cas manquants ;
- le verdict courant.

Regle dure :

- pas de `close_task` sans verification acceptee ;
- pas de `close_mission` si une task enfant requise reste ouverte ;
- un rejet de verification doit rouvrir le travail de facon causale.

## 7. Utiliser `Seance Archive`

`Seance Archive` sert a comprendre :

- qui a decide quoi ;
- quand la task a ete reroutee ;
- pourquoi une cloture a ete refusee ;
- quelles preuves ou sessions soutiennent l'etat courant.

Utilisez cette room quand la carte et le drawer ne suffisent plus.

## 8. Utiliser `Watchtower`

`Watchtower` sert a traiter les incidents de progression :

- `stale` ;
- `escalated` ;
- `quarantined`.

Quand une task devient stale, vous devez voir :

- la cause ;
- le signal de supervision ;
- la `nextAction` attendue.

Le bon invariant n'est pas "le flow ne s'arrete jamais". Le bon invariant est : **aucune task critique ne meurt silencieusement**.

## 9. Bonnes pratiques d'usage

- Ecrivez des criteres d'acceptation observables.
- Gardez la rationale de routage courte et lisible.
- Utilisez le `preview` avant les actions sensibles.
- Ouvrez le deep fetch seulement quand la carte et le drawer ne suffisent plus.
- Considerez la verification comme une condition d'existence du `done`, pas comme une formalite finale.

## 10. Anti-usages

- Deplacer une carte comme si cela validait l'etat metier.
- Cloturer une task parce que la UI "a l'air verte".
- Utiliser la carte comme stockage d'un transcript.
- Masquer un stall au lieu de l'escalader.
- Override un routage sans rationale traçable.

## 11. Lecture minimale par profil

### Operateur

- `Intake Desk`
- `War Room`
- drawer de task

### Reviewer ou verificateur

- `Branch Finisher`
- `Seance Archive`

### Supervision

- `Watchtower`
- `War Room`

## 12. References de package

- [SPEC-mission-board-grimoire.md](./SPEC-mission-board-grimoire.md)
- [CONTRAT-mission-board-grimoire.md](./CONTRAT-mission-board-grimoire.md)
- [UX-MAP-mission-board-grimoire.md](./UX-MAP-mission-board-grimoire.md)
- [WIREFRAMES-mission-board-grimoire.md](./WIREFRAMES-mission-board-grimoire.md)
- [LIVRABLE-FINAL-mission-board-grimoire.md](./LIVRABLE-FINAL-mission-board-grimoire.md)
