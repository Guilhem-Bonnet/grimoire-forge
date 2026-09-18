# Audit du parcours d'onboarding — grimoire-kit 3.57.0

Date : 2026-09-18
Portée : lecture seule, aucune PR, aucune modification de dépôt. Projets jetables sous
`_scratch/onboarding-audit/` (jamais `/tmp`), `GRIMOIRE_NO_COCKPIT=1` exporté pour tous
les `init`/`up`. Binaire testé : `/mnt/Travail/Projets/Dev/Grimoire-Forge/.venv/bin/grimoire`
(`grimoire-kit 3.57.0`). Code lu via `git -C grimoire-kit fetch origin` puis
`git show origin/main:<chemin>` (HEAD `ecda0fe` — release 3.57.0, #612).

Registre cockpit vérifié en fin d'audit (`grimoire cockpit list`) : aucun des projets
jetables de cet audit (`python-project*`, `node-project*`, `empty-repo*`) n'y figure —
`GRIMOIRE_NO_COCKPIT=1` a fonctionné comme attendu, rien à retirer. Une entrée
`serve-check` (chemin sous `/tmp/.../scratchpad`, marquée `○` = chemin disparu) est
préexistante, sans rapport avec cet audit ; non touchée.

---

## 1. Parcours vécu sur trois projets jetables

### Constat transversal n°1 — `grimoire init` sans option n'est interactif QUE sous un vrai TTY

Premier test, stdin `/dev/null` (script/CI-like) : le wizard **ne s'affiche pas du
tout**, `init` exécute silencieusement le chemin express (comme `-y`) et rend un rapport
identique à `-y`. Aucun message n'indique que l'assistant interactif a été sauté. Ce
n'est qu'en rejouant sous pseudo-TTY (harnais `pty` maison, boutons "Entrée" simulés)
que le wizard 5 étapes apparaît réellement. Un agent, un hook, ou tout terminal qui ne
présente pas un TTY plein (beaucoup d'environnements agentiques) tombe donc **toujours**
dans le chemin express sans le savoir.

### Constat transversal n°2 — le chemin par défaut (Entrée partout) ne choisit jamais de pattern

Wizard interactif, sur le projet Node (`package.json` + jest), toutes réponses par
défaut (Entrée) :

```
[####-] 4/5 · Archetypes
  1) Web App  2) Infra & DevOps  3) Platform Eng.  4) Agentic Standard
  5) Creative Studio  6) Fix Loop   0) Not sure — help me choose
  Choice (ex: 1,3,5 or all) (none):        <- défaut = "none"
```

Défaut = `none` → archétype `minimal` (3 méta-agents, aucun agent métier). Le menu
affiche 6 spécialisations avec une phrase chacune, plus une option explicite « 0) Not
sure — help me choose » (guided discovery) — mais il faut taper quelque chose pour en
profiter. Confirmé en rejouant le wizard avec `0` : 3 questions oui/non
(frontend ? infra ? fix-loop certifié ?) → recommandation correcte `web-app` pour ce
projet Node. Le mécanisme existe et fonctionne, il n'est simplement jamais le défaut.

### Constat transversal n°3 — `-y` (et donc `grimoire up` sans `-a`) donne `minimal` sur les trois projets, sans exception

```
PYTHON  -y  → Archetype: minimal (No specific stack pattern matched)
NODE    -y  → Archetype: minimal (No specific stack pattern matched)
EMPTY   -y  → Archetype: minimal (No specific stack pattern matched)
```

Lecture du code (`src/grimoire/core/archetype_resolver.py`, `_ARCHETYPE_RULES`) : la
détection automatique ne reconnaît que `terraform`/`kubernetes`/`ansible` → `infra-ops`,
et `react`/`vue`/`django`/`fastapi` (seuls ou combinés à python/go) → `web-app`. Un
`package.json` + `jest` nu (sans React/Vue) ou un `pyproject.toml` + `pytest` nu
(sans Django/FastAPI) ne correspondent à **aucune règle** → `minimal` par construction,
quel que soit le contenu réel du projet. C'est la cause racine, dans le code, du
problème posé par Guilhem : la majorité des projets réels (backend Python simple,
script Node, lib) tombent systématiquement sur l'archétype le plus pauvre, par le
chemin le plus emprunté (`-y`, ou `up` sans flag, tous deux documentés comme
« recommandés » dans le README/getting-started).

### Ce qui est installé (identique sur les trois projets, seul l'archétype varie)

`_grimoire/kit/` (agents, framework, tools, memory, teams), `_grimoire/_memory/`
(shared-context, decisions-log, contradiction-log, dependency-graph, etc.),
`_grimoire/overrides/`, `_grimoire-output/` (contracts, runs, team-build/ops/vision),
`.claude/{agents,commands,skills,settings.json}`, `.mcp.json`, `project-context.yaml`,
`CLAUDE.md`. Sur `minimal` : 18 dirs · 62 fichiers · 14 configs, 4 agents (meta ×3 +
stack-engineer). Sur `web-app` (guided discovery) : 63 fichiers, +1 agent
(`fullstack-dev` + skill `web-frontend-ux`). Mémoire : toujours `lexical` par défaut
(politique « jamais d'attache silencieuse », confirmée y compris quand un Weaviate est
détecté sur `localhost:8080` — le rapport le signale mais n'attache pas).

### Sortie « Next Steps » — identique dans les 6 runs (`init` plain, `init -y`, `up`), quel que soit le stack ou l'archétype

```
Your project is alive!
  Step 1: Open your project in VS Code        code <dir>
  Step 2: Talk to your AI concierge           Open Copilot Chat → type @concierge
                                               Marcel will guide you through your first session.
  Optional:
  Health check:   grimoire doctor
  Agent registry: grimoire status
```

Source : `_display_report()` dans `src/grimoire/cli/cmd_init.py` (~ligne 810) — panneau
**statique**, ne varie ni avec l'archétype choisi, ni avec le backend mémoire, ni avec le
profil. Suivi à la lettre : `grimoire doctor` (22/22 checks OK sur le projet Python,
aucune mention de cockpit/standard/hosts) et `grimoire status` (tableau projet + un seul
axe "Archetype: minimal" / "Backend: lexical", pas de piste vers autre chose). VS Code
et Copilot Chat n'étant pas disponibles dans ce terminal, l'étape 2 n'a pu être rejouée
littéralement ; le fichier `.claude/agents/concierge.md` existe (persona Marcel) mais son
contenu n'a pas été exécuté pour rester strictement dans les indications affichées.

### `grimoire up` (chemin « recommandé » du README/Quick Start) — plus riche, même angle mort

Sur le même projet Node, `grimoire up` (sans `-a`) ajoute un tableau récapitulatif que
`init` seul n'a pas :

```
init              done      project initialized (express)
standard          done      profile 'starter' — 7 artifact(s) written
task_unification  done      Mission Ledger already covers the board
host_sync         done      43 host artifact(s) written, 45 unchanged, across 5 host(s)
doctor            done      7/7 env checks OK, 0 warning(s)

Needs suggérés pour ce projet :
  --needs hooks-skills-governance   hooks/skills présents — les gouverner évite la dérive
  --needs tool-mediation-security   configuration MCP détectée — médiation des appels outils
```

Ce bloc « Needs suggérés » est la seule sortie CLI, sur tout l'audit, qui recommande
activement une suite d'action personnalisée — mais il s'affiche **après** le panneau
« Next Steps » encadré, dans un texte brut sans encadré, donc visuellement second plan.
L'archétype reste `minimal` : `up` sans `-a` a exactement le même angle mort que `init -y`
(`up --help` le confirme : « Express mode by default (equivalent to `grimoire init -y`) »).

---

## 2. Ce que le kit sait faire et qu'on ne découvre pas à l'init

`grimoire --help` n'affiche que 5 commandes (« Commandes pour commencer ») ; `--help --all`
en révèle 52. Pour chaque capacité : commande, mention à l'init/`--help`/docs, où
l'apprendre en pratique.

| Capacité | Commande d'accès | Mentionnée à l'init ? | Mentionnée dans `--help` (5) ? | Dans `docs/` ? |
|---|---|---|---|---|
| Archétypes/patterns | `grimoire registry list`, `init -a` | Oui mais seulement en option `1..6/0` du wizard interactif, jamais en `-y` | Non | Oui — `docs/archetype-guide.md`, `getting-started.md` |
| Guided discovery (3 questions) | intégré au wizard, taper `0` | Oui, mais pas par défaut | Non | Non documenté séparément |
| Profils standard (starter→governed→production) | `grimoire standard needs/init/verify/audit/score/gate` | **Non**, jamais cité dans le rapport `init`/`up` (`up` l'exécute mais ne l'explique pas) | Non (standard est dans les 47 « autres ») | Oui, en détail — `docs/standard/*.md`, README |
| Profils mémoire (lexical/standard/graphe/complet) | `--memory-profile`, question du wizard étape 3 | Oui dans le wizard interactif seulement | Non | Oui — `docs/memory-system.md` |
| Backends mémoire (Weaviate/Qdrant/Ollama) | `--backend`, `grimoire memory up` | Détection signalée en texte (jamais attachée) | Non | Oui |
| Hôtes (5 réels : Claude Code, Copilot, Codex, Cursor, Gemini CLI — **pas 177**, `177` est le n° de l'issue produit qui a introduit `hosts.enabled`) | `grimoire host list/surface/sync/status` | Non | Non | Oui — `docs/hosts.md` |
| Cockpit multi-projets | `grimoire cockpit` (add/list/scan/serve/start) | Non (sauf si `--lite`, qui l'exclut explicitement) | Oui (1 des 5) | Oui |
| Flows/blueprints gouvernés | `grimoire flow run`, `grimoire blueprint new/validate/compile/evals` | Non | Oui (`flow`, 1 des 5) | Oui — `getting-started.md`, `docs/nodal/*` |
| Skills | livrés avec l'archétype (`.claude/skills/`), pas de commande de navigation dédiée | Listés dans le rapport `init` (« Agents deployed » avec sous-chemins `skills/...`) | Non | Peu — mentionnés en passant |
| Agents/propositions (non-choix répétés) | `grimoire registry dispatches`, `grimoire proposals` | Non | Non | Non trouvé dans `getting-started.md`/`onboarding.md` |
| `grimoire up` | — | N/A (c'est la commande elle-même) | Oui (1 des 5) | Oui, mise en avant comme chemin recommandé |
| `doctor` / `status` | — | Oui, dans « Optional » du panneau final | Oui (1 des 5, doctor) | Oui |
| `context-pack` (le plus proche de « context build » — cette commande exacte n'existe pas) | `grimoire context-pack` | Non | Non | Non trouvé de doc dédiée |
| MCP | `.mcp.json` généré automatiquement, `grimoire-mcp` serveur | Vérifié silencieusement par `doctor` (« .mcp.json server 'grimoire' resolves ») jamais expliqué | Non | Oui — `docs/mcp-integration.md` |

Conclusion de section : **tout existe et est documenté quelque part dans `docs/`**, mais
rien de ce tableau (à l'exception d'un doctor/status en option, et du bloc `needs` de
`up` en texte secondaire) n'est jamais montré par la commande elle-même au moment où
l'utilisateur vient de taper `init`. L'écart n'est pas un manque de fonctionnalité, c'est
un manque de **surface** au moment zéro.

---

## 3. Documentation — où le parcours « premier quart d'heure » rompt

- `docs/index.md` → `getting-started.md` : parcours cohérent et à jour (archétypes,
  `up`, standard, cockpit, MCP, blueprints tous couverts, avec les bonnes commandes
  3.57.0). C'est une bonne doc — mais **rien dans la sortie CLI n'y renvoie**.
- `docs/onboarding.md` (« Guide de Démarrage Progressif », J1/S1/M1) est référencé dans
  `mkdocs.yml` (`nav: Onboarding: onboarding.md`, ligne 99) donc publié sur le site
  officiel, mais **daté du 2026-08-26** et rompt sur des éléments qui n'existent plus
  dans le produit livré : `bash grimoire.sh doctor` (pas de `grimoire.sh` scaffoldé),
  menu `/grimoire-master` avec personas BMM Mary/John/Winston/Amelia/Quinn/Bob (le
  concierge réel installé s'appelle Marcel, sans ce menu), archétypes cités
  `features`/`meta` (absents de `_ARCHETYPE_KEYS` actuel — les 7 valides sont `minimal`,
  `web-app`, `infra-ops`, `platform-engineering`, `agentic-standard`, `creative-studio`,
  `fix-loop`), `python3 framework/tools/nso.py` (NSO). Un utilisateur qui suit ce guide
  officiel — le seul à porter explicitement l'intention « premier quart d'heure » —
  échoue à la première commande non triviale de S1. C'est le point de rupture le plus
  net trouvé dans cet audit.
- `web/` existe dans le clone (`git ls-tree origin/main -- web`) mais n'a pas été
  investigué en détail (hors périmètre CLI de cet audit ; à creuser séparément si
  Guilhem le juge utile).
- Aucun document ne porte, pour l'instant, un contrat explicite « en 60 secondes,
  vous devez avoir X » — le contrat implicite le plus proche est le Quick Start du
  README (`grimoire up my-project --archetype web-app`), qui **suppose déjà connu**
  l'archétype à choisir.

---

## 4. Comparaison au marché (connaissances générales, non revérifiées par recherche web dans cet audit)

Motif commun aux outils agentiques CLI de référence (Claude Code `/init`, règles Cursor,
Aider, Continue, `npm create mastra@latest`) :

1. **Le chemin rapide fait quand même un choix visible et expliqué**, jamais un
   défaut « rien ». Mastra `create` demande un template avec une phrase par choix avant
   toute installation ; Continue demande un provider dès l'extension installée.
   Grimoire fait l'inverse sur son chemin le plus emprunté (`-y`/`up`) : défaut = rien.
2. **Un artefact concret et lisible apparaît immédiatement** (CLAUDE.md pour Claude
   Code, fichier de règles pour Cursor, playground local pour Mastra) — la valeur se
   voit sans lire de doc. Grimoire produit un `project-context.yaml` + une arborescence
   `_grimoire/`, mais rien de comparable à un artefact « à lire tout de suite » n'est mis
   en avant dans le rapport (le premier flow/preuve gouvernée n'est jamais montré).
3. **Le résumé post-install est personnalisé** à ce qui a été choisi/détecté, pas un
   texte fixe. Le panneau « Next Steps » de Grimoire est identique sur les 6 runs de cet
   audit, quel que soit stack, archétype ou profil mémoire.
4. **Les prochaines actions sont actionnables immédiatement**, pas juste « optionnel :
   voir X ». Le bloc `Needs suggérés` de `grimoire up` va dans ce sens mais est
   sous-visible (texte brut après le panneau encadré).
5. **Une visite guidée du produit** existe souvent en un geste (playground Mastra,
   tutoriel épinglé Continue). Grimoire a un cockpit et des flows gouvernés qui
   rempliraient ce rôle, mais rien ne les déclenche depuis `init`/`up`.

---

## 5. Constats chiffrés — les 5 manques majeurs

1. **`-y` et `up` sans `-a` produisent `minimal` pour 100 % des stacks hors
   React/Vue/Django/FastAPI/Terraform/K8s/Ansible** — vérifié sur Python nu, Node nu et
   dépôt vide (3/3). C'est le chemin documenté comme « recommandé » (README, `up`).
2. **Le wizard interactif a un défaut « aucune spécialisation »** à l'étape la plus
   importante (4/5 Archetypes) alors qu'un mécanisme de recommandation guidée
   (3 questions, `0`) existe et fonctionne correctement (testé : recommande `web-app`
   pour le projet Node) — mais n'est jamais le chemin par défaut.
3. **Le panneau « Next Steps » est 100 % statique** (identique sur 6 runs testés,
   3 stacks × plain/express) : aucune mention de cockpit, standard, hosts, flows,
   skills, MCP, alors que ces 7 capacités existent et sont documentées ailleurs.
4. **Le seul document officiellement dédié au « premier quart d'heure » (`docs/onboarding.md`,
   publié dans la nav mkdocs) est obsolète** de façon vérifiable — 3 références à des
   commandes/agents/archétypes qui n'existent plus dans le produit livré (`grimoire.sh`,
   menu `/grimoire-master`, personas BMM, `nso.py`, archétypes `features`/`meta`).
5. **Le wizard interactif ne se déclenche que sous TTY réel** ; en environnement non-TTY
   (script, beaucoup d'agents), `init` sans option se comporte silencieusement comme
   `-y`, sans le signaler — l'utilisateur ne sait même pas qu'un choix lui a été retiré.

Correction factuelle sur le brief : les « 177 hôtes » évoqués dans le cadrage sont en
réalité l'**issue #177** (déclaration `hosts.enabled`) ; le nombre réel de hôtes
supportés est **5** (Claude Code, GitHub Copilot, Codex, Cursor, Gemini CLI), confirmé
par `grimoire host list` et `docs/hosts.md`.

---

## 6. Expérience cible en trois niveaux

### Niveau 1 — « 60 secondes » (dans `grimoire init` / `grimoire up`)

| Action | Fichier(s) à modifier | Effort | Test d'acceptation |
|---|---|---|---|
| Rendre la guided discovery (3 questions oui/non) **le défaut** de l'étape Archétypes du wizard interactif, au lieu de `none` — l'option numérique reste disponible pour qui sait déjà ce qu'il veut | `src/grimoire/cli/cmd_init.py` (prompt de l'étape 4/5, `_parse_archetype_selection`) | S | Un utilisateur qui répond uniquement aux 3 questions oui/non du wizard (jamais un numéro) obtient un archétype spécialisé cohérent avec son projet, sur Python nu et Node nu, en moins de 2 minutes |
| Sur le chemin express (`-y`, `up` sans `-a`) : ne pas changer le défaut mémoire (doctrine « jamais silencieux » à garder), mais ajouter dans le rapport une ligne visible « Stack détecté : ce projet ressemble à web-app/infra-ops — relancez avec `-a <archétype>` » quand un signal faible existe (tests+CI, Dockerfile, package.json avec scripts front) | `src/grimoire/core/archetype_resolver.py` (nouvelle fonction de suggestion faible, séparée de la résolution silencieuse), `cmd_init.py::_display_report` | M | `grimoire init -y` sur un projet Node avec `webpack`/`vite` dans `package.json` affiche une suggestion nommée, jamais une attache silencieuse |
| Rendre le panneau « Next Steps » dynamique : nommer l'archétype installé et pourquoi, ajouter une ligne « ce projet a aussi : cockpit, standard, flows, mémoire — `grimoire status` pour tout voir » | `cmd_init.py::_display_report`, panneau `Panel(...)` en fin de fonction | S | Deux runs avec des archétypes différents produisent des panneaux « Next Steps » visiblement différents |
| Ajouter un pied de page à `grimoire doctor`/`status` : « Découvrir : `grimoire registry list` · `grimoire standard needs` · `grimoire cockpit` » | `src/grimoire/cli/cmd_doctor.py`, `cmd_status.py` | S | `grimoire status` sur un projet fraîchement initié affiche au moins une commande de découverte que l'utilisateur n'a pas encore tapée |

### Niveau 2 — « premier quart d'heure » (tour guidé)

| Action | Fichier(s)/mécanisme | Effort | Test d'acceptation |
|---|---|---|---|
| Réécrire `docs/onboarding.md` contre le CLI 3.57.0 réel (Marcel/concierge, 7 archétypes réels, commandes `grimoire` actuelles, retrait des références `grimoire.sh`/BMM/NSO) | `docs/onboarding.md` | M | Chaque commande citée dans le document s'exécute sans erreur sur un projet fraîchement initié |
| Ajouter une visite guidée déclenchée en fin de `up` (première exécution seulement) : ouvre le cockpit une fois, lance un flow de démonstration bundlé (`grimoire flow run <demo>.blueprint.json`) pour montrer un reçu de preuve réel, fait un aller-retour `memory remember`/`recall` | Nouvelle logique dans `cmd_up.py` + un blueprint de démo dans `registry/blueprints/` (déjà `minimal`/`web-pipeline` existants à réutiliser) | L | Sans lire aucune doc, un nouvel utilisateur peut, à partir de la seule sortie de `up`, ouvrir le cockpit, exécuter un flow gouverné et voir un reçu de preuve, et faire un aller-retour mémoire, en 15 minutes |
| Le concierge Marcel envoie un premier message proactif (via le hook SessionStart déjà utilisé pour l'auto-activation de persona, cf. mémoire `project_forge_persona_entree_autostart`) plutôt que d'attendre que l'utilisateur tape `@concierge` | Mécanisme SessionStart existant, contenu du prompt Marcel | M | Un nouvel hôte Claude Code affiche un message d'accueil de Marcel sans action de l'utilisateur au premier tour |

### Niveau 3 — « montée en puissance » (propositions, `up`, flows, skills)

| Action | Fichier(s)/mécanisme | Effort | Test d'acceptation |
|---|---|---|---|
| Donner au bloc « Needs suggérés » de `up` la même mise en forme (encadré) que « Next Steps », ou le fusionner dedans, pour qu'il ne soit plus en texte brut secondaire | `cmd_up.py` (affichage post-résumé) | S | Le bloc needs suggérés est visuellement au même niveau que Next Steps dans une capture d'écran |
| Surfacer `grimoire proposals`/`registry dispatches` (non-choix répétés déjà tracés, doctrine « artefact = différenciateur vérifiable ») dans `grimoire doctor`/`status` dès qu'un seuil de non-choix est atteint | `cmd_doctor.py`/`cmd_status.py`, lecture du registre de non-choix existant | S | Après reproduction artificielle de 3 non-choix identiques, `grimoire status` affiche une proposition concrète sans commande supplémentaire |
| Bannière de première visite dans le cockpit web listant les capacités non exploitées du projet enrôlé (archétype non spécialisé, profil standard sous la cible, mémoire encore lexicale) | UI cockpit (`web/`), déjà objet d'un audit UX antérieur (mémoire `project_kit_cockpit_interface`) | L | Un projet `minimal`/`lexical` fraîchement enrôlé affiche au moins une suggestion d'upgrade au premier chargement du cockpit |

---

## Annexe — commandes exactes rejouées (traces complètes disponibles dans ce dossier de scratch si besoin de re-preuve)

```
grimoire init <python-project>                 (stdin /dev/null → chemin express silencieux)
grimoire init <node-project>                   (pty réel → wizard 5 étapes, défauts partout)
grimoire init <node-project-guided>             (pty réel → wizard, "0" à l'étape archétype)
grimoire init <python-project-yes> -y
grimoire init <node-project-yes> -y
grimoire init <empty-repo-yes> -y
grimoire up <node-project-up>                   (stdin /dev/null → express + standard + host_sync + doctor)
grimoire doctor / grimoire status               (sur python-project)
grimoire registry list / grimoire host list
grimoire cockpit list                           (vérification finale de non-inscription)
```
