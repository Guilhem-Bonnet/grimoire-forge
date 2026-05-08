# Maturation Agentique — Pack de planification (2026-04-21)

> **Cadrage** : Audit + consolidation. Rationaliser l'existant, finir l'inachevé, durcir les hooks, extraire le meilleur de Pixel Agents. Pas de net-new.
>
> **Livrable** : planning-artifact, aucune modification de code dans ce tour.
>
> **Mandat utilisateur (21 avril 2026)** :
> > *Je veux un projet mature avec une gestion comme pixel-agent, avec le même principe de kanban que nos ref. Utiliser toutes nos ref en extraire le meilleur et les utiliser. Avec des systèmes de hook super bien agencé. Avec un projet agentique très moderne et innovant avec tous les concepts qu'on propose fonctionnel (si ils sont toujours jugés bons). Je veux une base solide.*

## Index du pack

| Fichier | Objet |
|---|---|
| [01-AUDIT-etat-existant.md](01-AUDIT-etat-existant.md) | Inventaire mesuré des surfaces, runtime, hooks, concepts |
| [02-EXTRACTIONS-refs.md](02-EXTRACTIONS-refs.md) | Pixel Agents + Switchboard — ce qu'on garde, ce qu'on adapte |
| [03-GAP-ANALYSIS-hooks.md](03-GAP-ANALYSIS-hooks.md) | Audit des 9 hooks installés + trous identifiés |
| [04-CARTOGRAPHIE-concepts.md](04-CARTOGRAPHIE-concepts.md) | Les 42 BM-* référencés — statut fonctionnel / partiel / mort |
| [05-DECISIONS-rationalisation.md](05-DECISIONS-rationalisation.md) | ADR synthèse : garder / durcir / archiver |
| [06-PLAN-execution-phases.md](06-PLAN-execution-phases.md) | Roadmap phasée en vagues |
| [07-METRIQUES-baseline.md](07-METRIQUES-baseline.md) | Baseline mesurable pour tracker la progression |
| [DOC-TECHNIQUE-maturation-agentique.md](DOC-TECHNIQUE-maturation-agentique.md) | Contrat technique du pack |
| [GUIDE-utilisation-maturation-agentique.md](GUIDE-utilisation-maturation-agentique.md) | Comment consommer ce pack |

## Synthèse en 30 secondes

**État actuel** (avril 2026) :

- 3 surfaces déjà livrées : `cockpit`, `mission-board` (Kanban in-world), `observatory` via `grimoire-game`
- 13 hooks scripts + 9 déclarations JSON + registry de sécurité + gateway (`enforced` mode validé `2026-04-16`)
- 23 agents + 41 skills + 7 instructions + 6 prompts user-facing
- 42 concepts BM-* référencés dans le codebase (dont SOG BM-53, HUP BM-50, QEC BM-51, CVTL BM-52, ARG BM-57 pleinement implémentés)
- Score harmony : **96/100 (A)** — 1389 fichiers scannés
- 2 forks de référence intégrés : `apps/pixel-agents-fork/` et `apps/switchboard-fork/`

**Diagnostic** :

- Le projet n'est **pas immature**. Il est **trop riche pour ce qui est actuellement exploitable par l'utilisateur**.
- Le cockpit live est publié, mais la chaîne d'événements agent → Kanban → observatory n'est pas bouclée : le Kanban n'a pas de producteur d'événements réels, c'est un mock rendu.
- Les hooks sont présents et gatés, mais ne produisent pas de signaux consommables par les surfaces (pas de pont `hook → mission-board`).
- Les BM-* sont massivement référencés mais ~40% sont théoriques (documentés, non exécutables).
- Pixel Agents et Switchboard sont forkés mais **non intégrés** — ils dorment sous `apps/`.

**Objectif du pack** : transformer 4 à 6 semaines de travail en 4 vagues courtes qui livrent **une base agentique solide, mesurable, et cohérente**.

## Vagues proposées (voir `06-PLAN-execution-phases.md`)

| Vague | Durée indicative | Objectif livré |
|---|---|---|
| **V1 — Vérité** | 1 semaine | Bus d'événements unifié `hook → GameState → surfaces`. Tout signal agent devient visible dans le même ledger. |
| **V2 — Kanban vivant** | 1 semaine | Mission-board piloté par de vrais événements hooks + pattern `drag → trigger` emprunté à Switchboard. |
| **V3 — Office view** | 1-2 semaines | Agents = personnages dans `observatory` (pattern Pixel Agents). Event → animation branché sur V1. |
| **V4 — Rationalisation concepts** | 1 semaine | Tri des 42 BM-* : garder les 24 actifs, archiver 10 théoriques, durcir 8. Registry de capacités à jour. |

Chaque vague produit son propre pack planning-artifact d'exécution au moment du go.

## Mandat utilisateur résolu ✓

| Demande | Comment ce pack y répond |
|---|---|
| *Projet mature* | V1+V2+V3 transforment les signaux agent en surface visible. V4 supprime la dette conceptuelle. |
| *Gestion comme Pixel Agents* | V3 extrait l'office view agent-agnostic (voir `02-EXTRACTIONS-refs.md`). |
| *Même Kanban que nos refs* | V2 adopte le pattern Switchboard drag→trigger + reste branché sur le ledger GameState (pas de divergence). |
| *Utiliser toutes nos refs* | `02-EXTRACTIONS-refs.md` consolide les 2 forks + docs `benchmark-github-agent-os-game-ui.md` + `plan-maitre-agent-os-game-ui.md`. |
| *Hooks super bien agencés* | V1 branche les hooks sur le bus d'événements, V2/V3 les consomment. `03-GAP-ANALYSIS-hooks.md` décrit les trous. |
| *Concepts fonctionnels (si jugés bons)* | V4 tranche concept par concept via grille "garder/durcir/archiver". |
| *Base solide* | `07-METRIQUES-baseline.md` définit ce qui doit rester vert après chaque vague. |

## Statut

- **Type** : planning-artifact durable
- **Version** : 1.0 (2026-04-21)
- **Auteur orchestrateur** : grimoire-master (SOG BM-53)
- **Compagnons obligatoires** : `DOC-TECHNIQUE-maturation-agentique.md` + `GUIDE-utilisation-maturation-agentique.md` (voir règle dans `.github/copilot-instructions.md`)
- **Prochain artefact attendu** : `_grimoire-runtime-output/planning-artifacts/V1-verite-bus-evenements-20260422/` au go utilisateur
