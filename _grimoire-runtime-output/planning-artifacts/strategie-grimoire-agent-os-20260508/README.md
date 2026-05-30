# Stratégie Grimoire Agent OS

Date de production : 2026-05-08

Objectif : comparer Grimoire et `grimoire-kit` aux rapports internes et aux références agentiques récentes, puis fournir une formule cible, un plan d'élévation et une revue critique des angles morts.

## Livrables

| Fichier | Rôle |
| --- | --- |
| `DOC-TECHNIQUE-strategie-grimoire-agent-os.md` | Méthode, corpus, sources locales et sources web utilisées. |
| `GUIDE-utilisation-strategie-grimoire-agent-os.md` | Mode d'emploi pour transformer le paquet en décisions et travaux. |
| `MATRICE-comparaison-grimoire-vs-references.md` | Comparaison synthétique entre Grimoire, les rapports internes et les références IA. |
| `FORMULE-agent-os-grimoire.md` | Formule cible : primitives, architecture et principes de produit. |
| `PLAN-montee-en-puissance-grimoire-kit.md` | Plan d'exécution sans estimation temporelle, avec dépendances et gates. |
| `REVUE-critique-angles-morts.md` | Revue du plan, oublis probables et corrections à intégrer. |

## Verdict court

Grimoire n'est plus au stade "mock agentique". Le code actuel montre déjà une avance depuis les anciens rapports :

- `GrimoireEvent` est présent côté Python et TypeScript.
- `activity.jsonl` existe comme ledger de hooks.
- Le Mission Board sait projeter de l'activité corrélée.
- Le runtime dashboard, l'observability surface, la timeline Office et la stigmergy ont des tests ciblés verts.
- `grimoire memory status` expose un contrat Memory OS avec Qdrant prêt et plusieurs couches partielles ou planifiées.
- Le serveur MCP local est réel et la policy MCP détecte déjà un échec sur `ollama`.

Le cap change donc : il ne faut plus refaire les anciennes vagues V1 à V4. Il faut transformer ces tranches partielles en noyau durable, interopérable, sécurisé et publiable.

## Formule synthétique

```text
Grimoire Agent OS =
  Runtime durable
+ Event ledger canonique
+ Mission graph pilotable
+ Capability registry A2A/MCP
+ Policy gate fail-closed
+ Memory OS typé
+ Eval and trace ledger
+ Cockpit opérateur IDE-native
+ Pack registry gouverné
```

Le facteur différenciant n'est pas "plus d'agents". Le facteur différenciant est le contrôle opérable : une action agentique doit être visible, reprise, prouvée, évaluée et limitée.

## Décision principale

La prochaine grande décision produit est de nommer le noyau :

`Grimoire Runtime Kernel`

Ce kernel doit devenir la source de vérité unique pour :

- runs ;
- événements ;
- checkpoints ;
- agents ;
- tools ;
- policies ;
- approvals ;
- preuves ;
- traces ;
- mémoires promues.

Le cockpit et le Mission Board doivent rester des projections du kernel, jamais une logique métier parallèle.

