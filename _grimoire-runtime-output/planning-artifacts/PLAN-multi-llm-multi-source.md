# Plan : exploitation multi-LLM et multi-source

## Contexte

Le depot dispose deja d'un canon host bridge, d'un routage de modeles cote runtime et d'un routeur LLM cote kit.
Le besoin n'est donc pas d'ajouter un nouveau centre de gravite, mais de transformer l'usage de plusieurs hotes et plusieurs providers en boucle de travail gouvernee, rejouable et verifiable.

## Decision de travail

- Copilot reste le shell principal du repo.
- Claude sert de contradicteur longue fenetre sur les sujets critiques.
- GPT Codex sert d'executant code borne.
- L'API agregee reste reservee au fallback, aux canaries et aux evals.
- Le pack de mission canonique remplace les transcripts comme unite d'echange entre hotes.

## Tranche executee dans ce tour

| Etape | Action | Resultat attendu |
| --- | --- | --- |
| 1 | Formaliser la strategie canonique | Une doc exploitation qui fixe roles, garde-fous et flux |
| 2 | Ajouter un prompt reutilisable | Une relance standard du cadrage multi-LLM sans repartir de zero |
| 3 | Relier la doc aux index | Le sujet devient visible et non orphelin |
| 4 | Aligner le template et le parser du routeur | Le schema canonique devient consommable sans casser le format legacy |
| 5 | Standardiser le review artifact externe | Une review host importee devient lisible et mappable en preuve cockpit |
| 6 | Poser le harness canari minimal | Un canari Promptfoo valide, executable localement, cable a GitHub Models via le `GITHUB_TOKEN` du workflow et via `GITHUB_TOKEN` ou `GH_MODELS_TOKEN` en local, et pilotable en workflow manuel |
| 7 | Exposer la telemetrie utile du routeur | Le dashboard Synapse lit policy, cout, distribution des regles et decisions recentes |
| 8 | Fermer la boucle pack de mission -> preuve | Les evidence packs exposent le mission pack et la couverture de preuve attendue |
| 9 | Construire un handoff host reutilisable | Le runtime expose un packet `mission pack -> canonical envelopes -> reviews/context host` pour les hotes externes |
| 10 | Brancher un premier adaptateur Mammouth et fermer la chaine review importee | Un hote HTTP externe peut consommer le packet de handoff et un review importe alimente automatiquement `verification gate -> evidence pack` |

## Prochaines taches ordonnees

### Etape 1 : enrichir le canari branche et durcir le gate compare

**Landing zone** : `grimoire-kit/evals/multi-llm/` et workflow manuel du canari.

**Action** : garder GitHub Models comme premier provider reel deja branche, puis etendre le dataset et les assertions pour produire un rapport compare plus discriminant entre modeles.

**Verification** :

- le workflow manuel peut executer `promptfoo eval` avec le `GITHUB_TOKEN` du workflow ;
- le run local peut executer `promptfoo eval` avec `GITHUB_TOKEN` ou `GH_MODELS_TOKEN` ;
- un rapport canari est publie comme artefact ;
- la comparaison inter-provider reste repo-first et bornee par le pack de mission ;
- le dataset couvre plus d'un seul pack de mission et distingue mieux les regressions reelles.

### Etape 2 : relier la telemetrie routeur a la surface web finale du cockpit

**Landing zone** : UI web finale du runtime dashboard.

**Action** : reutiliser la vue telemetry du dashboard Synapse dans la surface web finale sans recréer un modele parallele.

**Verification** :

- la politique routeur reste lisible dans le cockpit final ;
- les couts, fallback chains et dernieres decisions sont visibles sans shell Python ;
- la surface web consomme la meme source que le dashboard CLI.

## Plus petite slice executable suivante

La plus petite slice a forte valeur est :

1. enrichir le dataset du canari maintenant que GitHub Models est branche en reel ;
2. publier le rapport Promptfoo du workflow manuel comme artefact compare ;
3. relier la telemetrie routeur a la surface web finale du cockpit.

## Preuve attendue avant de dire done

- la strategie canonique est publiee et indexee ;
- le prompt reutilisable existe et pointe vers les sources canoniques ;
- le template de config du routeur reflete le canon de routage et reste compatible avec le format legacy ;
- la telemetrie routeur expose policy, cout, distribution des regles et decisions recentes ;
- une review externe peut etre reliee a une trace, un sujet canonique et une evidence ref ;
- un handoff host reutilisable peut etre produit pour une tache a partir du mission pack, des enveloppes canoniques et des reviews/context imports ;
- un premier adaptateur HTTP Mammouth peut consommer ce handoff, et un review importe peut alimenter automatiquement `verification gate -> evidence pack` sans metadonnees workflow dediees ;
- un mission pack peut etre relie a un evidence pack et a la couverture de preuve attendue ;
- une comparaison inter-modele minimale peut etre executee sans ambiguite sur la source de verite.
