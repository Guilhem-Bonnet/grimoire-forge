# Plan directeur unifie Grimoire x Gastownhall

Ce paquet remplace la lecture dispersee des anciens plans par une source de pilotage unique pour le nouveau projet Grimoire Agent OS.

Il corrige un manque du rapport precedent : Gastownhall n'est plus traite seulement par le paquet `adaptation-gastownhall-grimoire`, mais comme ecosysteme complet :

- `gastown` : workspace manager, Mayor, rigs, hooks, convoys, provider integration ;
- `beads` : ledger de travail distribue, dependances, ids sans collision, multi-repo ;
- `gascity` : SDK d'orchestration, providers runtime, supervisor, orders, formulas, packs ;
- `gascity-packs` : modele concret de distribution par packs, commandes, doctor checks et services ;
- `gascity-otel` : stack d'observabilite et modeles de metriques ;
- `community` et `docs` : strategie de documentation, adoption et ecosysteme.

## Documents

| Document | Role |
| --- | --- |
| [../cahier-des-charges-projet-cible-grimoire-agent-os-20260508/README.md](../cahier-des-charges-projet-cible-grimoire-agent-os-20260508/README.md) | Cahier des charges cible ideal, architecture, schemas, exigences et lots d'execution agents. |
| [DOC-TECHNIQUE-plan-directeur-grimoire-gastown-unifie.md](./DOC-TECHNIQUE-plan-directeur-grimoire-gastown-unifie.md) | Sources, diagnostic, comparaison Grimoire x Gastownhall x references externes. |
| [GUIDE-utilisation-plan-directeur-grimoire-gastown-unifie.md](./GUIDE-utilisation-plan-directeur-grimoire-gastown-unifie.md) | Comment utiliser ce plan comme source de verite pour agents et humains. |
| [PLAN-DIRECTEUR-nouveau-projet-grimoire-agent-os.md](./PLAN-DIRECTEUR-nouveau-projet-grimoire-agent-os.md) | Grand plan unifie pour Grimoire Forge et grimoire-kit. |
| [MATRICE-fusion-projets-agentiques.md](./MATRICE-fusion-projets-agentiques.md) | Quels projets fusionner, quoi absorber, quoi rejeter, comment faire. |
| [ADDENDUM-REFERENCES-AGENTIQUES-comparaison-fusion.md](./ADDENDUM-REFERENCES-AGENTIQUES-comparaison-fusion.md) | Fiches de decision pour chaque projet du corpus `Référence-Agentique`. |
| [ADDENDUM-CREWAI-comparaison-fusion.md](./ADDENDUM-CREWAI-comparaison-fusion.md) | Analyse ciblee de CrewAI, decisions de fusion et backlog associe. |
| [CONTRAT-hooks-guardrails-agents.md](./CONTRAT-hooks-guardrails-agents.md) | Contrat d'execution agentique adapte aux hooks, guardrails et gates fail-closed. |
| [BACKLOG-agentique-unifie.md](./BACKLOG-agentique-unifie.md) | Backlog unique en lots agent-executable sans notion de calendrier. |
| [REGISTRE-nettoyage-plans-deprecies.md](./REGISTRE-nettoyage-plans-deprecies.md) | Nettoyage non destructif des anciens plans, statuts et regles de migration. |

## Decision

La nouvelle source de verite est :

```text
Grimoire Agent OS =
  Grimoire Forge comme chantier, cockpit et bootstrap natif
+ grimoire-kit comme SDK, CLI, runtime kernel et produit distribuable
+ Mission Ledger comme source causale
+ Workflow Instances comme execution reprenable
+ Pack Registry comme distribution gouvernee
+ Memory OS comme rappel et code graph
+ Hook and Guardrail Plane comme surface de securite
+ Mission Board comme cockpit operateur
```

Les anciens plans ne sont pas supprimes. Ils sont classes comme `source`, `absorbed`, `superseded`, `incubator` ou `archive`. Toute nouvelle tache doit se rattacher au plan directeur et non rouvrir une roadmap parallele.

## Principe de fusion

On ne fusionne pas les repos par copie brute. On fusionne les primitives utiles par contrat :

- schema canonique ;
- adaptateur de lecture ou d'import ;
- pack experimental ;
- gate de securite ;
- preuve d'execution ;
- promotion seulement si le comportement est repetable et gouverne.
