# Spec — Ingénierie de contexte dans le blueprint

Date : 2026-07-12. Portée : spécifier les composants dédiés au management de
contexte (raffinement section 4.C, chantiers P2.3 et P3.2), troisième pièce de
la série ouverte par `SPEC-failure-edges-et-evals.md` et
`SPEC-gate-universel.md`. Rétro-compatible : tout est additif au format v2
Studio et au schéma v1 (`blueprintVersion` inchangé).

Constat d'écart : le catalogue possède déjà la théorie (famille ORC
« Orchestration et contexte », patterns ORC-03 à ORC-09, contrats
`context-pack` et `handoff-packet`) et le kit possède déjà les moteurs
(dormants `token-budget.py`, `context-summarizer.py`, `context-merge.py`,
testés, non wirés). Mais l'éditeur blueprint ne connaît qu'une dimension : le
coût statique `NODE_COST`. Le budget de contexte, la compaction et
l'isolation — les trois décisions de design centrales — sont invisibles dans
le graphe. Cette spec les rend déclarables, lintables, simulables et
compilables.

---

## 0. Principe — le contexte est une politique, pas un node

Même discipline que le Gate universel : pas de nouveau bestiaire. Le
management de contexte s'exprime en **politique par node**
(`config.context`), en **gates** (enforcement via `Gate(budget)` déjà
spécifié) et, quand P0.3 livrera les classes sémantiques, en **frontière de
région** (`Boundary(isolation)`). Aucun `kind` nouveau.

> Un node « qui fait » (`Unit`) déclare *ce qu'il reçoit* (budget), *comment
> son amont est compressé* (compaction) et *dans quelle fenêtre il tourne*
> (isolation). Le graphe montre enfin la décision architecturale la plus
> coûteuse d'un système agentique : ce qui entre dans chaque fenêtre.

Les tiers de budget réutilisent le vocabulaire du contrat `context-pack` du
catalogue : `tiny | small | medium | deep` (ORC-08, escalade justifiée et
retour au tier inférieur).

---

## 1. Delta de schéma — `config.context`

Sous-schéma nommé, additif, sur tout node. L'absence de `config.context`
équivaut aux défauts (comportement actuel : rien ne change pour les
blueprints existants).

```json
"$defs": {
  "contextPolicy": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "budget": {
        "type": "object",
        "properties": {
          "tier": { "enum": ["tiny", "small", "medium", "deep"], "default": "medium" },
          "maxTokens": { "type": "integer", "minimum": 1 },
          "justification": { "type": "string" }
        }
      },
      "compaction": {
        "type": "object",
        "properties": {
          "strategy": { "enum": ["digest", "selective", "index-guided", "full"], "default": "full" },
          "digestContract": { "enum": ["handoff-packet", "context-pack"], "default": "handoff-packet" }
        }
      },
      "isolation": { "enum": ["shared", "isolated"], "default": "shared" }
    }
  }
}
```

Sémantique des trois axes :

| Axe | Valeurs | Décision qu'il rend visible |
|---|---|---|
| `budget.tier` | `tiny → deep` | Combien de contexte ce node reçoit ; `deep` exige `justification` (R-C3) |
| `compaction.strategy` | `digest`, `selective`, `index-guided`, `full` | Comment l'amont est compressé avant d'entrer dans la fenêtre |
| `isolation` | `shared`, `isolated` | Fenêtre partagée avec l'orchestrateur, ou sous-agent quarantiné qui ne rend qu'un digest |

Point clé de compilation : ces valeurs mappent **une pour une** sur des
mécanismes que le runtime exécute déjà — les stratégies `discover_inputs` du
moteur de workflow (`FULL_LOAD`, `SELECTIVE_LOAD`, `INDEX_GUIDED`) et la
capsule minimale d'injection subagent. Le blueprint ne déclare rien que
l'hôte ne sache pas honorer (section 5).

---

## 2. Enforcement — délégué au Gate universel

Cette spec n'ajoute **aucun mécanisme d'enforcement propre**.
`config.context.budget` est déclaratif (design + simulation) ; le blocage
runtime est `Gate(mode: budget)` de `SPEC-gate-universel.md`, dont on précise
ici le branchement :

- Le moteur d'enforcement est le dormant `framework/tools/token-budget.py`
  (BM-41), réveillé comme chantier P2.3 : CLI + endpoint `/api/cost-model`
  remplaçant la table statique `NODE_COST` (la vue COÛT passe de
  « hypothèses » à « calibré »).
- Un dépassement émet un `error-envelope` de classe `budget-exceeded`
  (`SPEC-failure-edges-et-evals.md`) et route selon `onReject` — le fallback
  naturel est un edge `failure` vers un `Unit` sur modèle moins cher.
- L'assertion d'éval `cost-under` devient vérifiable contre le même modèle de
  coût : une seule source de vérité pour design, gate et éval.

---

## 3. Isolation — node d'abord, région ensuite

Deux temps, pour ne pas dépendre de P0.3 :

1. **Maintenant (additif)** : `config.context.isolation: "isolated"` par
   node. L'éditeur dessine un halo sur le node ; la compilation émet la
   directive de dispatch en sous-agent isolé (section 5).
2. **Après P0.3 (classes sémantiques)** : `Boundary(isolation)` marque une
   *région* — plusieurs nodes partageant une même fenêtre quarantinée
   (patron orchestrateur-worker). Le viewer dessine la zone. La sémantique
   par node reste valide et devient le cas dégénéré d'une région à un node.

Règle de cohérence : un node `isolated` ne peut exporter vers l'aval qu'un
contrat de digest (`handoff-packet` ou `context-pack`) — c'est la définition
même de la quarantaine. Lint R-C5.

---

## 4. Pression de contexte — la simulation gagne une dimension

`blueprint_simulate` estime aujourd'hui l'ordre topologique et les prérequis.
Ajout : une estimation de **pression de fenêtre par node**, calculée pendant
le parcours topologique.

Modèle (volontairement simple, calibrable par P2.3) :

- `charge(node) = coût d'entrée du node + report d'amont`.
- Le report d'amont dépend de la compaction du node :
  `full` reporte la charge cumulée des prédécesseurs ; `digest` la réduit à
  la taille du digest ; `selective` et `index-guided` à une fraction
  intermédiaire. Un node `isolated` **remet le report à zéro** pour son aval
  (seul le digest sort).
- Verdict par node contre la fenêtre du modèle cible :
  `ok` (sous 60 %), `warn` (60 à 85 %), `critical` (au-delà).

Sortie : `contextPressure: [{ nodeId, estimatedTokens, windowPct, verdict }]`
dans la réponse de `/api/blueprints/<id>/simulate`. L'éditeur colore les
nodes en conséquence. C'est le signal « ça cassera en prod » **avant**
compilation — la simulation teste enfin autre chose que la forme.

---

## 5. Compilation — section « Contexte » du mission pack

`blueprint_compile` émet, pour chaque step dont le node porte un
`config.context`, une sous-section normative :

| Déclaration blueprint | Directive compilée (exécutée par l'hôte existant) |
|---|---|
| `budget.tier` | Tier annoncé au step + plafond `maxTokens` si présent |
| `compaction: digest` | Produire un `handoff-packet` (ORC-03) avant de passer la main |
| `compaction: selective` | Chargement `SELECTIVE_LOAD` (variables ciblées) du moteur de workflow |
| `compaction: index-guided` | Chargement `INDEX_GUIDED` (index puis shards pertinents) |
| `isolation: isolated` | Dispatch en sous-agent à capsule minimale ; retour exclusivement via le contrat de digest déclaré |

La compilation reste déterministe (P0.1) : la politique de contexte est du
texte stable dans le mission pack, pas un appel runtime.

---

## 6. Règles de lint ajoutées

| Règle | Sévérité | Déclencheur | Fix |
|---|---|---|---|
| R-C1 | avertissement | Node alimenté par `extension-node` ou référence MCP avec `isolation: "shared"` | Passer le node en `isolated` (quarantaine du contenu externe) |
| R-C2 | avertissement | Chaîne de 4 `Unit` ou plus sans aucune compaction `digest` ni node ORC-03 | Insérer un handoff digest |
| R-C3 | avertissement | `budget.tier: "deep"` sans `justification` | Justifier ou redescendre de tier (discipline ORC-08) |
| R-C4 | bloquant | `budget.maxTokens` supérieur à la fenêtre du modèle cible | Corriger le plafond |
| R-C5 | bloquant | Node `isolated` avec un pin de sortie dont le contrat n'est pas un digest (`handoff-packet`, `context-pack`) | Sortir via digest ou lever l'isolation |
| R-C6 | information | Verdict de pression `critical` sur au moins un node | Ajouter compaction ou isolation en amont |

R-C1 rejoint R-G2 du Gate universel : les deux traitent la frontière de
confiance, l'un côté filtrage, l'autre côté fenêtre.

---

## 7. Réveil des dormants — décision par outil

Un réveil = une PR gated (discipline du raffinement, section 4.J).

| Dormant | Décision | Chantier |
|---|---|---|
| `token-budget.py` | **Réveil prioritaire** — moteur du coût calibré et du `Gate(budget)` | P2.3 |
| `context-summarizer.py` | Réveil — moteur hôte de `compaction: digest` | avec la tranche compile |
| `context-merge.py` | Réveil — fusion de digests au fan-in (`Gather`) | après P0.3 |
| `semantic-cache.py` | Différé — utile mais sans ancre blueprint ; candidat Labs | — |
| `sensory-buffer.py` | **Refusé** — pas de thèse produit (raffinement section 7) | — |

---

## 8. Volet runtime — aligner les flows existants sur le catalogue

Les composants blueprint ci-dessus déclarent des politiques ; les flows qui
tournent aujourd'hui dans la Forge doivent converger vers les mêmes contrats.
Quatre chantiers d'hygiène, indépendants de l'éditeur :

1. **Capsule pre-compact au contrat `context-pack`** : la capsule runtime
   (`precompact/latest.json`) est un format ad hoc. L'aligner sur le contrat
   du catalogue : `schemaVersion`, provenance des sources incluses/exclues
   avec statut et confiance, scorecard de suffisance, `expiry`. La capsule
   subagent (200 caractères) devient le profil `tiny` du même contrat.
2. **Bornage des ledgers de contexte** : `activity.jsonl` et
   `precompact/events.jsonl` sont append-only sans borne — exactement le
   constat « tout-indexer » de l'audit. Appliquer KNO-01/RUN-02 : rotation
   par nombre d'événements ou fenêtre glissante, `schemaVersion` sur chaque
   ligne.
3. **`repo-contexts/` exploité** : le répertoire mémoire prévu pour le
   contexte de repo persistant est vide. Y matérialiser un `context-pack`
   durable par repo, sous l'ordre d'autorité ORC-06 (source active avant
   preuve vérifiée avant mémoire durable avant similarité).
4. **Handoff inter-agents** : le seul handoff runtime effectif est la trace
   subagent. Produire un `handoff-packet` conforme (ORC-03) à chaque
   SubagentStop, en réutilisant `context-summarizer.py` réveillé.

---

## 9. Découpage, dépendances, preuve

| Tranche | Contenu | Dépend de | Preuve |
|---|---|---|---|
| C1 — surface déclarative | `config.context` (éditeur + validation), lint R-C1 à R-C6, pression de contexte en simulation, section « Contexte » compilée | rien (additif) | Un blueprint annoté compile avec sa politique visible ; un node `isolated` à sortie non-digest refuse de compiler (R-C5) |
| C2 — enforcement calibré | Réveil `token-budget`, `/api/cost-model`, branchement `Gate(budget)` et `cost-under` | P2.1, C1 | Vue COÛT étiquetée « calibré » ; un dépassement injecté suit le failure-edge (`budget-exceeded`) |
| C3 — régions d'isolation | `Boundary(isolation)` en zone, `context-merge` au fan-in | P0.3, C1 | Une région multi-nodes compile en un seul dispatch quarantiné |
| C4 — runtime aligné | Capsule `context-pack`, ledgers bornés, `repo-contexts`, handoff ORC-03 | rien (parallèle) | La capsule valide contre le contrat du catalogue ; les ledgers ont une borne effective |

C1 est volontairement libre de toute dépendance : c'est la tranche qui rend
le contexte *visible et décidable* dans le graphe. L'enforcement (C2) et les
régions (C3) suivent l'ordre du raffinement (P2.1 puis P0.3).

Contrainte de gouvernance : le catalogue amont vit dans le dépôt
`processus-developpement-agentique` — tout nouveau contrat ou pattern (il n'y
en a **aucun** dans cette spec : elle réutilise `context-pack`,
`handoff-packet`, ORC-03, ORC-06, ORC-08) passerait par une PR là-bas, pas
par une édition locale de l'export.
