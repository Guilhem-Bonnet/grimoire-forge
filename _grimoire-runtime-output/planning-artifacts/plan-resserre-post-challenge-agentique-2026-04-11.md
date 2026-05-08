---
title: Plan resserre post-challenge agentique
description: Plan revise apres contradiction croisee du diagnostic et du plan post-audit, centre sur le contrat canonique, la preuve et le cockpit minimal.
date: 2026-04-11
---

## Plan resserre post-challenge agentique

## But

Remplacer le premier plan post-audit par une version plus dure, plus courte et plus testable.

Le changement central est le suivant : le projet ne doit pas avancer en mode `cleanup first` ni `event first`. Il doit avancer en mode **contrat canonique -> preuve -> cockpit minimal -> extensions**.

## Verdict apres contradiction croisee

La contradiction sur quatre angles distincts fait ressortir cinq corrections de cap.

- Le pivot n'est pas l'evenement runtime. Le pivot est le **contrat d'execution canonique**.
- Le wedge n'est pas le runtime seul. Le wedge est le **cockpit agentique visible, explicable et verifiable**.
- La consolidation interne est necessaire, mais seulement jusqu'au niveau qui rend une preuve produit defendable.
- La chaine de preuve doit arriver avant les surfaces riches, pas apres.
- Les extensions `multi-host`, `multi-PC`, `rooms`, `catalogue d'agents`, `memoire riche` et `policy MCP exhaustive` doivent suivre la preuve, pas la preceder.

## Ce qui change par rapport au premier plan

Le premier plan post-audit etait juste sur le diagnostic, mais trop large sur le sequencing.

- `Canoniser l'evenement runtime` devient `geler le contrat d'execution canonique`.
- `Operationaliser le cockpit` remonte beaucoup plus tot, mais sur un scope minimal strict.
- `Rationaliser le catalogue d'agents` ne disparait pas, mais cesse d'etre un prerequis dur.
- `Governance MCP exhaustive` devient une extension tardive ; seul le **contrat host fail-closed minimal** remonte tot.
- Le plan est redecoupe pour limiter les fronts de validation ouverts en parallele.

## Axe 1 - Geler le contrat canonique

### Axe 1 Intention

Fermer une spine runtime utilisable avant toute extension de surface.

Le livrable n'est pas un format d'evenement de plus. Le livrable est un **contrat canonique v1** qui couvre trois niveaux :

- contrat de run ;
- contrat host ;
- contrat de preuve.

### Axe 1 Scope minimal

- Identites stables : `runId`, `taskId`, `workerId`, `hostId`, `traceId`, `requestId`, `idempotencyKey`.
- Transitions autorisees et ownership des mutations.
- Regles fail-closed pour `preview -> validation -> commit borne`.
- Idempotence, causalite et replay pour un panier critique de mutations.
- Source de verite explicite pour runtime, trace, verification et projection.

### Axe 1 Sortie attendue

- Un run critique mono-host et mono-projet se reconstruit sans inference fragile.
- Une mutation critique est refusee si provenance, policy ou verification sont incompletes.
- La trace, la verification et le replay pointent vers les memes identites canoniques.

### Axe 1 Gate de sortie

- Un scenario critique de reference passe de bout en bout sur les tests de contrat et d'integration.
- Le scenario miroir en entree incomplete ou non autorisee est refuse explicitement.
- Les nouvelles traces critiques n'introduisent plus de `unknown -> unknown` sur les champs causaux.

### Axe 1 Ce qu'il faut geler

- Extension large du catalogue d'agents.
- Surfaces UI riches non branchees sur ce contrat.
- Claims `Agent OS` ou `control plane` plus ambitieux que la preuve produite.

## Axe 2 - Prouver le cockpit minimal

### Axe 2 Intention

Prouver rapidement pourquoi Grimoire existe comme produit, sans ouvrir un second systeme.

Le cockpit minimal doit battre le workflow actuel sur une boucle courte :

`observer -> inspecter -> expliquer -> verifier -> challenger`

### Axe 2 Scope minimal

- Une vue operateur experte unique, pas encore un ensemble complet de rooms.
- Inspection d'un run critique unique issu du contrat canonique.
- Lecture de la provenance, de la decision, de la verification et du replay depuis les memes read models.
- Un seul flux utile `preview -> validation -> commit borne` visible dans la surface.

### Axe 2 Sortie attendue

- Un operateur peut comprendre pourquoi une action a ete acceptee ou refusee.
- Une preuve exploitable est visible sans transcript brut complet.
- Le replay du run critique est lisible dans la meme surface que l'inspection.

### Axe 2 Gate de sortie

- Une demo borne de bout en bout existe sur un flux critique unique.
- Cette demo montre au minimum : origine host, decision, preuve, refus ou validation, replay.
- Le cockpit n'introduit aucune logique metier parallele au runtime.

### Axe 2 Ce qu'il faut geler

- Rooms riches, office view et habillage spatial etendu.
- Gamification, audio, assets non necessaires a la preuve produit.
- Tout read model qui ne sert pas directement la boucle operateur minimale.

## Axe 3 - Ouvrir les extensions sous preuve

### Axe 3 Intention

N'ouvrir le reste du programme qu'apres validation de la spine et du wedge.

### Axe 3 Extensions autorisees ensuite

- Rationalisation profonde du catalogue d'agents.
- Governance MCP exhaustive et allowlists completees.
- Host bridges additionnels.
- Multi-PC et distribution plus large.
- Memoire multi-session enrichie.
- Rooms specialisees, office view et contenu spatial additionnel.

### Axe 3 Regle d'entree

Chaque extension doit consommer le meme contrat de run, le meme contrat host et le meme contrat de preuve.

Elle ne peut pas introduire :

- un nouveau format canonique concurrent ;
- une nouvelle source de verite ;
- une preuve reconstruite a posteriori hors spine principale.

### Axe 3 Gate de sortie

- L'extension demontre sa valeur sur la boucle operateur ou sur la robustesse de la spine.
- L'extension ne force ni re-ecriture du contrat canonique ni duplication des read models.

## Ordre d'execution dur

1. Fermer la topologie active uniquement au niveau necessaire pour supporter le contrat canonique.
2. Geler le contrat de run, le contrat host minimal et le contrat de preuve minimal.
3. Prouver un flux critique mono-host, mono-projet, replayable et verifiable.
4. Exposer ce flux dans un cockpit minimal expert.
5. Seulement ensuite, et sur preuve, ouvrir rationalisation profonde, MCP exhaustif, multi-host, multi-PC, rooms et extensions memoire.

## Premier paquet a lancer

Si un seul paquet part maintenant, il doit contenir uniquement ceci :

- alignement des sources de verite runtime, trace et verification ;
- gel du contrat canonique sur un panier critique borne ;
- refus fail-closed et replay fiable sur ce panier ;
- projection cockpit minimale sur ces memes read models.

Tout le reste doit attendre que ce paquet soit prouve.

## Claims autorises apres ce resserrement

Une fois ce paquet ferme, le projet peut defendre honnetement la proposition suivante :

- Grimoire est un **workbench agentique IDE-native** ;
- avec un **cockpit operatoire verifiable** sur un flux critique borne ;
- et une trajectoire credible vers un Agent OS, mais sans revendiquer encore cette maturite comme acquise.

## Claims a ne pas faire avant preuve supplementaire

- `runtime durable de reference` ;
- `control plane complet` ;
- `Agent OS stabilise` ;
- `interop multi-host generalisee` ;
- `gouvernance MCP pleinement operee a grande echelle`.
