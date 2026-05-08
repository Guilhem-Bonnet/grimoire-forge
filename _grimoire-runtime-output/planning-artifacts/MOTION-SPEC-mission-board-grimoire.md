# Motion Spec — Mission Board Grimoire

> Projet : **Grimoire**
> Sources : [VISUAL-BRIEF-mission-board-grimoire.md](./VISUAL-BRIEF-mission-board-grimoire.md), [UX-MAP-mission-board-grimoire.md](./UX-MAP-mission-board-grimoire.md), [grimoire-game-assets/STYLE_GUIDE.md](../../grimoire-game-assets/STYLE_GUIDE.md)

---

## 1. Objet

Definir une grammaire de motion semantique pour le `Mission Board` : chaque mouvement doit porter une information operatoire. Rien ne doit bouger sans raconter une transition metier ou un changement causal.

## 2. Principes de motion

- **Motion supports comprehension** : l'animation explique, elle ne distrait pas.
- **Locality first** : la motion reste locale a la carte, a la lane ou a la relation concernees.
- **No endless loops** : aucune animation d'ambiance ne doit monopoliser l'attention.
- **Edge-led runtime** : les signaux runtime vivent sur les bords, les scelles ou les tethers, jamais au centre de la carte.
- **Reduced motion parity** : chaque animation a un equivalent statique ou quasi-statique.

## 3. Vocabulaire de motion

| Token | Usage | Forme |
| --- | --- | --- |
| `stamp` | qualification, decision, readiness | impact court et centralise |
| `dock` | entree en verification ou en archive | glisse courte vers une zone cible |
| `tether` | handoff, dependance, reroute | lien directionnel source -> cible |
| `edge-pulse` | run actif, heartbeat, checkpoint | pulse discret sur tranche |
| `tight-flash` | reject, blocage, alerte critique | flash serre local, jamais plein ecran |
| `desaturate` | stale ou attente | perte de saturation locale |
| `seal-reveal` | verdict ou policy | apparition de sceau ou cachet |

## 4. Evenements et motions associees

| Evenement canonique | Motion | Sens |
| --- | --- | --- |
| `task.created` | `dock` vers `Intake` | une fiche entre dans le systeme |
| `task.qualified` | `stamp` `Verdigris` ou `Brass` | le contrat devient lisible |
| `task.routed` | `tether` vers la lane cible | le systeme choisit une route |
| `task.assignment.confirmed` | `seal-reveal` discret sur le badge de lane | la prise en charge devient explicite |
| `workflow.instance.started` | `edge-pulse` `Storm` | un run vit |
| `workflow.checkpoint.recorded` | `edge-pulse` court sur le socle | le run progresse |
| `workflow.stale.detected` | `desaturate` + marqueur `Memory` | la fraicheur devient un signal |
| `verification.requested` | `dock` vers `Branch Finisher` | la task entre en gate |
| `verification.accepted` | `seal-reveal` `Brass` | le verdict autorise la cloture |
| `verification.rejected` | `tight-flash` `Ember` puis retour lane | la task revient avec cause |
| `task.blocked` | encoche `Ember` qui se fige | l'arret est explicite |
| `task.unblocked` | retrait de l'encoche et retour d'`Ink` et `Paper` | la task retrouve un chemin |
| `task.closed` | `dock` leger vers archive ou done | la task quitte l'actif proprement |

## 5. Motion par room

### 5.1 Intake Desk

- motion de creation et de qualification ;
- aucune ambience continue ;
- preview de routage par `tether` bref vers la lane candidate.

### 5.2 War Room

- dependances revelees au focus ;
- reroute et handoff lisibles par tether ;
- pas de glissement libre de carte comme mutation canonique.

### 5.3 Workshop

- `edge-pulse` `Storm` sur runs actifs ;
- checkpoint visible en bas de carte ;
- pause ou reprise sans spinner central.

### 5.4 Branch Finisher

- `dock` et `seal-reveal` dominants ;
- `tight-flash` `Ember` sur reject ;
- aucun triomphe confetti sur acceptation.

### 5.5 Seance Archive

- transitions calmes, presque documentaires ;
- onglets `Memory` et highlights discrets ;
- pas de motion hero.

### 5.6 Watchtower

- alertes par `tight-flash` localise ;
- stale par `desaturate` ;
- escalade par `tether` vers la lane ou le role de destination.

## 6. Etats interactifs

| Etat interactif | Reponse motion |
| --- | --- |
| hover | soulievement minimal et accent de contour |
| focus | double contour et rappel d'ancrage au dossier lateral |
| selection | tether visuel carte -> dossier |
| disabled | scelle visible, pas de disparition de l'action |
| denied | `tight-flash` local + raison de refus |

## 7. Reduced Motion

Quand `reduced motion` est actif :

- `dock` devient un changement de placement sans transition visible ;
- `tether` devient une ligne statique temporaire ;
- `edge-pulse` devient une variation de contour ou d'opacite ;
- `tight-flash` devient un changement bref de bordure et de badge ;
- `desaturate` reste autorise car il ne depend pas du mouvement.

## 8. Prohibitions absolues

- spinner central de carte ;
- glow diffus permanent ;
- pluie de particules ;
- tremblement de surface complet ;
- plein ecran rouge pour incident ;
- anneaux radiaux generiques sans direction ni sens.

## 9. Regles d'implementation

- toute motion doit se mapper a un evenement canonique ou a un etat interactif explicite ;
- une motion doit rester lisible en densite de board elevee ;
- aucune motion n'a le droit de masquer une information essentielle ;
- la motion doit survivre a une lecture a 1x sans ressembler a un bruit.
