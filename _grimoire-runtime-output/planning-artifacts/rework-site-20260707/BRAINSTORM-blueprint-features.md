# Brainstorm — features du Blueprint Studio

Date : 2026-07-07. Base : intégration complète du Studio v2 (PR kit #64),
connaissance directe de chaque module (`bp2-core`, `bp2-docs`, `bp2-cost`,
`bp2-assist`, `bp2-team`, `bp2-library`, `bp2-composer`, onboarding, tour).

## Garder tel quel — prouvé pendant l'intégration

| Feature | Pourquoi |
|---|---|
| Sous-flows C4 (⌘G, double-clic, fil d'Ariane, ports dérivés) | Différenciateur fort ; mappe naturellement la compilation en workflows imbriqués. |
| Onboarding « premier flow » en 4 gestes réels (< 2 min) | Répond exactement au problème initial (« moi-même je ne comprends pas comment on l'utilise »). Vérifié : les pins famille rendent le tutoriel connectable (QUA-04 → QUA-05 en evidence-pack). |
| Validation 3 niveaux : live client → lint serveur → simulation → compile | Architecture saine ; le serveur reste la seule autorité (E2E : un blocker serveur annule le `simulated`). |
| Nodes d'équipe concrets (agents outillés : tools, MCP, skills, hooks, modèle) | C'est la matière de la compilation v2 — à ne surtout pas retirer. |
| Docs portés par les nodes (mission-brief, system-prompt, completion-contract) | Idem : intrants directs de la compilation v2. |

## Améliorer / raffiner

1. **Curation des pins par pattern dans le catalogue** — le chantier structurel.
   Aujourd'hui : heuristique par famille, dupliquée (`FAMILY_PINS` JS /
   `STUDIO_FAMILY_PINS` Python), documentée comme provisoire. Le vrai fix :
   ajouter `contracts: {consumes: [], produces: []}` à chaque pattern dans
   `processus-developpement-agentique` et l'exporter. Effet en cascade :
   validation typée honnête, suggestions justes, plus de duplication.
   *C'est un chantier catalogue, pas éditeur.*

2. **Assist dérivé du catalogue réel** — grosse valeur, données déjà exportées.
   La map `NEXT` (adjacences suggérées) et les règles R-01…R-09 sont écrites
   à la main. Le catalogue exporte **141 relations typées** (depends,
   composes, mitigates…) et **52 anti-patterns** : les suggestions fantômes
   devraient dériver des relations, et chaque anti-pattern devrait devenir
   une règle R-xx avec fix 1-clic. L'assistant devient alors une
   matérialisation du corpus normatif au lieu d'une opinion figée.

3. **Compilation v2 : des artefacts réels par node** — le chaînon manquant.
   Le `.prompt.md` actuel est un plan descriptif. Les nodes d'équipe portent
   déjà tout (rôle, modèle, outils, hooks, prompt système) : compiler vers
   de vrais `.agent.md` par agent, hooks enregistrés en shadow dans le
   registre, skills — via des templates par pattern/kind. Le diff git reste
   la revue. C'est ce qui transforme le Studio de « schéma annoté » en
   « usine à artefacts gouvernés ».

4. **Coût tokens : du statique inventé au mesuré.**
   `NODE_COST` est une table d'hypothèses. Le kit a déjà la télémétrie
   (events.jsonl, QUA-06 LLM cost registry, ccusage en opt-in local) : un
   endpoint `/api/cost-model` calibré sur le projet remplacerait la table.
   Premier pas honnête et immédiat : étiqueter la vue COÛT « hypothèses
   statiques » tant que non calibrée.

5. **Replay branché sur le SSE réel.**
   `/api/events` (SSE) et `/api/events/log` existent côté serve ; l'onglet
   SIMU peut gagner un mode « replay » qui surligne les nodes au fil des
   événements réels du projet — la promesse « tracé, rejouable » dans
   l'éditeur lui-même.

## Manquant

1. **Multi-projets** : endpoints `/api/projects` (récents, select, init
   non-interactive) + page sélecteur réelle (la démo de composant du design
   a été supprimée ; le bouton projet de la sidebar pointe sur le hub en
   attendant).
2. **Détection de dérive visible** : le hash `compiled` est persisté (fait) ;
   l'UI doit montrer « artefact modifié à la main depuis la compilation »
   en comparant le hash au fichier réel (esprit KNO-03 Doc drift detector).
3. **Import des blueprints publiés du registry depuis l'UI** : le bouton
   « ouvrir dans l'éditeur » instancie un preset local ; il devrait passer
   par `grimoire ext add-blueprint` (checksum vérifié, provenance registry).
4. **Préparation de publication** : préparer l'archive d'un blueprint pour
   `publish-pr.sh` depuis l'UI (la PR reste manuelle — revue humaine
   non négociable).
5. **Journal de compilations honnête** : aujourd'hui en localStorage ;
   le dériver des sections `compiled` des blueprints du projet (source
   réelle), le localStorage ne gardant que les préférences UI.

## À repenser

1. **Trois chemins de création guidée qui se recouvrent** : composer
   (questionnaire), squelettes de use-cases (50 réels), templates de la
   bibliothèque. Proposition : les use-cases réels deviennent la source
   première, le composer les paramètre, les templates sont des presets du
   composer — un seul pipeline au lieu de trois.
2. **Deux tables de prix modèles** (`MODELS` de bp2-cost vs `MODEL_RATES`
   de bp2-team) : une seule source, idéalement alignée sur le routing
   modèle du projet.
3. **Budget mission par « profil »** : les profils starter/controlled du
   design n'existent pas côté kit ; ancrer les plafonds sur les archétypes
   réels ou une config projet.
4. **États sans-projet** : quand serve tourne, il y a toujours une racine ;
   « aucun projet » ne survit que hors-ligne. Simplifié pendant
   l'intégration — finir le ménage quand le multi-projets arrivera.

## À retirer

1. `CAPS` par profils morts dans bp2-cost (remplacé par le point ci-dessus).
2. Toute persistance localStorage restante qui prétend être un état projet
   (le journal de compilations, cf. Manquant §5). Préférences UI : ok.

## Priorisation proposée (impact / effort)

1. Curation des pins par pattern (catalogue) — structurel, débloque 2 et 3.
2. Compilation v2 team → artefacts réels — le chaînon manquant du produit.
3. Assist dérivé des relations + anti-patterns réels — valeur pédagogique max.
4. Multi-projets (API + sélecteur) — friction d'adoption.
5. Dérive visible + journal compilations réels — petits, forte honnêteté.
6. Coût mesuré (étiquetage immédiat, calibration ensuite).
