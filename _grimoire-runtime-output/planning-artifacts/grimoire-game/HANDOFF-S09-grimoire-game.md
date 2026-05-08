---
title: Handoff Sprint S9 - Grimoire Game
description: Passation operationnelle par role pour le Sprint S9.
author: GitHub Copilot
date: 2026-04-09
---

## But

Aligner `@ux`, `@dev`, `@qa` et `@arch` sur une execution S9 borne, verifiable et sans glissement de scope. Ce handoff ne remplace ni le backlog ni le board tickets. Il sert a rendre chaque role directement actionnable a partir du brief sprint et du paquet S9.

## Statut post-challenge

Ce handoff devient un handoff de readiness tant que `GAME-TKT-054` n'est pas prouve.

Regle immediate:

- `@ux` peut continuer la preparation de `GAME-S09-001` ;
- `@dev`, `@qa` et `@arch` ne lancent pas les lots mutationnels S9 tant que la gate post-challenge reste ouverte.

Mise a jour runtime locale du 2026-04-11 :

- La tranche runtime bornee de `GAME-TKT-030` est deja couverte et validee dans `grimoire-kit/apps/grimoire-game`.
- `GAME-TKT-038` est deja prouve localement et doit etre traite comme dependance satisfaite.
- Toute reactivation de `GAME-S09-001` ou `GAME-S09-002` doit donc cibler un reliquat UI, UX ou produit explicite, et non la reimplementation d'un coeur runtime deja livre.

## Sources operatoires

- [KICKOFF-S09-grimoire-game.md](KICKOFF-S09-grimoire-game.md)
- [SPRINT-S09-grimoire-game.md](SPRINT-S09-grimoire-game.md)
- [TICKETS-web-gaming.md](TICKETS-web-gaming.md)
- [GO-NO-GO-S09-004-grimoire-game.md](GO-NO-GO-S09-004-grimoire-game.md)
- [EPICS-grimoire-game.md](EPICS-grimoire-game.md)
- [GDD-grimoire-game.md](GDD-grimoire-game.md)
- [TECH-grimoire-game.md](TECH-grimoire-game.md)
- [PAQUET-execution-agentic-guardrails-runtime.md](PAQUET-execution-agentic-guardrails-runtime.md)
- [CONTRAT-runtime-agentic-guardrails.md](CONTRAT-runtime-agentic-guardrails.md)
- [PAQUET-execution-front-prioritaire-post-challenge.md](PAQUET-execution-front-prioritaire-post-challenge.md)

```mermaid
flowchart LR
    UX[@ux] -->|Contrats UI figes| DEV[@dev]
    DEV -->|Builds + mutations + traces| QA[@qa]
    QA -->|Verdict evidence| ARCH[@arch]
    ARCH -->|Go/No-Go TASK-055| DEV
```

## Regles d'engagement

- Aucun elargissement de scope apres gel des contrats UI S9.
- Aucune ouverture effective de S9 avant fermeture de `GAME-TKT-054`.
- `GAME-S09-005` ferme toute activation du scope configuration qui manque provenance, trust status ou policy minimale.
- `GAME-S09-004` n'ouvre jamais sans verdict go/no-go explicite.
- Aucun ticket ne change de statut vers `Review` ou `Done` sans evidence exploitable.

## Handoff @ux

Mission:

Figer les contrats UI du sprint pour permettre l'integration Svelte sans reouverture de decisions structurelles.

Note de cadrage:

- La mission ne vaut plus, a date, comme rattrapage du coeur runtime de `GAME-TKT-030`, deja couvert localement.

Tickets pilotes:

- `GAME-S09-001`

Entrees attendues:

- Brief sprint S9
- Requirements critiques des panels et modals
- Contraintes de reflow et d'affichage securise du contenu agentique

Sorties attendues:

- Direction visuelle retenue pour S9
- Liste des composants critiques a integrer
- Contrats UI figes pour le skill tree, ses badges de governance et la modal de challenge

Gate de sortie du role:

- Les surfaces skill tree et challenge modal sont assez figees pour que `@dev` implemente sans reinterpretation produit.

## Handoff @dev

Mission:

Transformer les contrats UI gelees en surfaces fonctionnelles, connecter la configuration reelle, puis ouvrir les variantes de challenge sans absorber la tranche suivante du backlog.

Note de cadrage:

- `GAME-S09-002` ne doit plus etre lu comme ticket runtime manquant dans le package courant ; toute reprise doit viser un reliquat explicite au-dela de la tranche deja livree.

Tickets pilotes:

- `GAME-S09-001`
- `GAME-S09-002`
- `GAME-S09-005`
- `GAME-S09-003`
- `GAME-S09-004` si go/no-go positif

Entrees attendues:

- Contrats UI gelees issus de `GAME-S09-001`
- Ticket parent `GAME-TKT-030` pour la config gamifiee
- Ticket parent `GAME-TKT-037` pour les garde-fous OWASP Agentic Skills
- Ticket parent `GAME-TKT-015` pour la challenge room
- Gate `GAME-TKT-054` fermee avant toute implementation mutationnelle

Sorties attendues:

- Composants Svelte integres et reutilisables
- Skill tree branche a la vraie configuration
- Badges de provenance, trust status et policy minimale visibles sur le scope S9
- Selecteur de challenge et variantes nominales tracees
- Investigation Lab tranche S9 si le sprint ouvre le conditionnel

Gate de sortie du role:

- Les mutations de configuration et les variantes de challenge sont testables, tracees et sans regression nominale visible.

## Handoff @qa

Mission:

Construire et faire respecter la preuve minimale du sprint avant tout passage en review ou ouverture du conditionnel.

Tickets pilotes:

- `GAME-S09-001`
- `GAME-S09-002`
- `GAME-S09-005`
- `GAME-S09-003`
- `GAME-S09-004` si ouvert

Entrees attendues:

- Composants integres et contrats UI figes
- Flux de configuration persistants
- Pipelines des variantes de challenge
- Gate `GAME-TKT-054` fermee et preuves du front prioritaire disponibles

Sorties attendues:

- Tests integration UI -> config -> reload
- Tests activation autorisee/refusee sur le scope skill tree S9
- Tests d'activation des variantes Investigation, DX Review et Auto-Challenge
- Verdict de go/no-go pour l'ouverture de `GAME-S09-004`

Gate de sortie du role:

- La preuve permet de distinguer clairement un ticket pret pour `Review`, un ticket a maintenir `In Progress`, et un ticket conditionnel qui doit rester ferme.

## Handoff @arch

Mission:

Proteger la coherence contractuelle du sprint et arbitrer l'ouverture du conditionnel sans laisser entrer de dette structurelle silencieuse.

Tickets pilotes:

- Validation transverse sur `GAME-S09-001` a `GAME-S09-005`

Entrees attendues:

- Contrats UI orientes WebSocket
- Gardes-fous de gouvernance issus de `GAME-TKT-037`
- Preuves QA sur persistence, challenge et audit trail
- Points de friction eventuelle avec auth spectateur ou socle debug

Sorties attendues:

- Validation des interfaces et de la synchro config
- Verdict go/no-go pour `GAME-S09-004`
- Liste courte des contraintes non negociables a conserver jusqu'en fin de sprint

Gate de sortie du role:

- Aucun contournement n'est accepte sur root cause, verification gate, ou blocages contractuels lies a la configuration.

## Synchronisations obligatoires

1. Verification de la gate `GAME-TKT-054` avant toute ouverture effective de S9.
2. Revue de gel apres `GAME-S09-001` pour ouvrir `GAME-S09-002`.
3. Revue de gouvernance apres `GAME-S09-002` pour ouvrir `GAME-S09-005`.
4. Revue de coherence apres `GAME-S09-005` pour ouvrir `GAME-S09-003` sans extension de scope.
5. Revue go/no-go avant toute ouverture de `GAME-S09-004`.

## Resultat attendu en fin de sprint

- Le board dispose d'un socle UI stable pour la configuration gamifiee, sans avoir contourne la gate post-challenge.
- Le skill tree MCP/skills modifie et recharge la vraie configuration.
- Les activations du scope S9 restent bloquees sans provenance, trust status et policy minimale.
- Les variantes de challenge prevues par S9 existent sans regression du flux nominal.
- L'Investigation Lab ne s'ouvre que si les preuves permettent de le faire sans fragiliser le sprint.
