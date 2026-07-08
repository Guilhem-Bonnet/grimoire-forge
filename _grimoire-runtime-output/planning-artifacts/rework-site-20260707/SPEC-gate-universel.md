# Spec — Gate universel paramétré

Date : 2026-07-08. Portée : spécifier la primitive `Gate` (raffinement
section 2, chantier P2.1) qui unifie toute la famille gouvernance/preuve en un
seul type de node paramétré. Rétro-compatible avec `schemas/blueprint.schema.json`
(`blueprintVersion` reste `1`). Enchaîne sur `SPEC-failure-edges-et-evals.md` :
le **rejet** d'un gate réutilise les edges typés (`channel`).

Livre au passage le human-in-the-loop riche (raffinement 4.F) et la couche
guardrails (4.E), sans node neuf.

---

## 0. Principe — une primitive, N modes

La proposition XXL éparpille les nodes de gouvernance : porte humaine, garde de
budget, checkpoint de preuve, contrat de sortie, MCP trust, guardrail… Ce sont
tous la **même mécanique** : inspecter les contrats entrants et *laisser
passer* (plan happy) ou *bloquer / router* (plan failure/escalation). La
variation est dans un paramètre, pas dans le type de node.

> Un `Gate` n'a **jamais** de sémantique de transformation (ça, c'est un
> `Unit`). Il **assère une précondition** et gouverne le flux. Son
> comportement de rejet réutilise les failure-edges du spec précédent.

Bénéfice : un seul compilateur, un seul visuel, une seule famille de lint, et
côté canal Labs on teste une *config* de Gate, pas un nouveau bestiaire.

---

## 1. Delta de schéma — `config.gate`

`node.config` est ouvert dans le schéma réel ; on lui donne un sous-schéma
nommé pour le lint. La présence de `config.gate` **dérive** `role: "gate"`.

```json
"$defs": {
  "gatePolicy": {
    "type": "object",
    "required": ["mode"],
    "additionalProperties": false,
    "properties": {
      "mode": {
        "enum": ["human", "budget", "evidence", "output-contract", "guardrail", "mcp-trust"]
      },
      "onReject": {
        "enum": ["escalation", "failure", "block"],
        "default": "block",
        "description": "Comment le rejet se propage : edge escalation, edge failure, ou arrêt dur"
      },
      "params": { "type": "object", "description": "Paramètres propres au mode (voir §2)" }
    }
  }
}
```

Un node Gate reste un node normal : `kind` = `pattern` le plus souvent (il
ancre un pattern GOV/QUA du catalogue via `ref`), `pins` d'entrée = ce qu'il
inspecte, `pins` de sortie = le plan happy s'il passe.

---

## 2. Les six modes

Un seul type, six paramétrages. Chaque mode ancre un pattern du catalogue et
compile vers une section différente.

| `mode` | `params` | Ancre | Compile vers | Bloque quand |
|---|---|---|---|---|
| `human` | `action`, `approvers?`, `confidenceThreshold?` | GOV-15 | Checkpoint d'escalade humaine documenté | Non approuvé / incertitude sous seuil |
| `budget` | `maxTokens?`, `maxUsd?`, `scope` | (token-budget) | Enforcement de budget sur node/segment/flow | Plafond dépassé |
| `evidence` | `require: []`, `format?` | QUA-04 | Entrée d'evidence-pack exigée | Evidence manquante |
| `output-contract` | `schema` | QUA-14 | Validateur de schéma de sortie | Schéma invalide |
| `guardrail` | `direction`, `checks: []` | (bias-toolkit) | Étape de filtre I/O | Flag PII / injection / secret / contenu |
| `mcp-trust` | `server`, `allowedTools: []`, `permissions: []` | GOV-09 | MCP Trust Gate | Serveur non fiable / sur-permissionné |

### Détail des params par mode

```json
{ "mode": "human",
  "params": { "action": "approve", "approvers": ["maintainer"], "confidenceThreshold": 0.7 } }

{ "mode": "budget",
  "params": { "maxUsd": 2.5, "scope": "segment" } }

{ "mode": "evidence",
  "params": { "require": ["test-run", "verdict"], "format": "evidence-pack" } }

{ "mode": "output-contract",
  "params": { "schema": "contracts/deploy-report.schema.json" } }

{ "mode": "guardrail",
  "params": { "direction": "in", "checks": ["injection", "pii", "secret"] } }

{ "mode": "mcp-trust",
  "params": { "server": "github", "allowedTools": ["list_prs"], "permissions": ["read"] } }
```

---

## 3. Human-in-the-loop riche (livre 4.F)

« Porte humaine » n'est pas un point mais un spectre, exprimé par
`params.action` :

| `action` | Sémantique | Compile vers |
|---|---|---|
| `approve` | Approbation avant de continuer | Checkpoint bloquant GOV-15 |
| `edit` | L'humain corrige la sortie avant transmission | Checkpoint + point d'édition du handoff |
| `input` | L'humain fournit un input manquant | Checkpoint + attente d'input typé |
| `sample` | Revue de `pct` % des runs (échantillonnage) | Checkpoint probabiliste (`params.pct`) |
| `escalate-on-uncertainty` | Ne bloque que si le verdict de confiance < `confidenceThreshold` | Checkpoint conditionnel |

Corollaire d'état durable (4.F) : tout `Gate(human)` qui suspend exige un
`Boundary(checkpoint)` en amont (spec à venir) pour que le flow soit
*reprenable* après décision — sinon l'approbation n'a nulle part où reprendre.

---

## 4. Le rejet réutilise les failure-edges (continuité)

Point de design central : un gate qui bloque **route via un edge typé** du spec
précédent, il ne réinvente rien.

- `onReject: "escalation"` → edge `channel:"escalation"` du pin de rejet du gate
  vers un `Gate(human)` ou un `Reference(signal ALERT)`. Naturel pour `human`,
  `mcp-trust`.
- `onReject: "failure"` → edge `channel:"failure"` vers un `Unit` de secours.
  Naturel pour `budget` (basculer sur modèle moins cher) et `output-contract`
  (re-tenter avec contrainte renforcée).
- `onReject: "block"` → arrêt dur, aucun edge sortant de rejet. Le flow se
  termine sur ce gate (dead-letter implicite).

Le pin de rejet est synthétisé (contract `error-envelope`, comme le pin `error`
d'un Unit) : le gate a donc jusqu'à trois sorties — happy (passe), rejet
(failure/escalation), rien (block).

---

## 5. Compilation — un seul compilateur

```text
compileGate(node):
    switch node.config.gate.mode:
      human           -> section GOV-15 (action, approvers, seuil)
      budget          -> directive d'enforcement (token-budget, scope)
      evidence        -> exigence QUA-04 (types requis)
      output-contract -> validateur QUA-14 (schéma)
      guardrail       -> étape de filtre (direction, checks)
      mcp-trust       -> GOV-09 (serveur, outils, permissions)
    emit reject-path from node.config.gate.onReject
```

Un point d'entrée, un `switch`, un émetteur de chemin de rejet commun. Ajouter
un mode = ajouter une branche, pas un compilateur.

---

## 6. Règles de lint ajoutées

| Règle | Sévérité | Déclencheur | Fix |
|---|---|---|---|
| R-G1 | bloquant | `Reference(mcp)` ou `extension-node` à accès outil **sans** `Gate(mcp-trust)` en amont | Insérer un gate mcp-trust |
| R-G2 | bloquant | Entrée externe (mcp/ext) qui alimente un `Unit` effectful ou une sortie **sans** `Gate(guardrail, in)` intermédiaire | Insérer un guardrail entrée |
| R-G3 | avertissement | `Gate(human\|budget\|mcp-trust)` avec `onReject:"block"` et aucune alternative | Suggérer un edge escalation |
| R-G4 | bloquant | `Gate(output-contract)` dont `params.schema` ne résout pas | — |
| R-G5 | information | Sortie réseau (`Unit` notification) **sans** `Gate(guardrail, out)` en amont | Suggérer un guardrail sortie |

R-G1 et R-G2 sont l'application directe du verdict de sécurité (4.E) : la
surface d'attaque ne peut plus exister sans point de filtrage déclaré.

---

## 7. Exemple — le policy-gate durci

Reprise de `onboarding-crew` : le `policy-gate` devient un `Gate(mcp-trust)`
explicite, et on ajoute un `Gate(guardrail, out)` avant toute notification.

```json
{
  "id": "policy-gate",
  "kind": "pattern",
  "ref": "GOV-09",
  "label": "MCP Trust Gate",
  "config": {
    "gate": {
      "mode": "mcp-trust",
      "onReject": "escalation",
      "params": { "server": "github", "allowedTools": ["list_prs", "read_issue"], "permissions": ["read"] }
    }
  },
  "pins": [
    { "id": "task-in", "direction": "in", "contract": "task-envelope" },
    { "id": "task-out", "direction": "out", "contract": "task-envelope" },
    { "id": "reject", "direction": "out", "contract": "error-envelope" }
  ]
}
```

Edge de rejet, réutilisant le canal escalation du spec précédent :

```json
{ "from": "policy-gate.reject", "to": "escalade.err-in", "contract": "error-envelope", "channel": "escalation" }
```

---

## 8. Impact sur le plan

- Livre **P2.1** (Gate universel), et par ricochet **4.E** (guardrails) et
  **4.F** (HITL riche) du raffinement.
- Construit sur **P0.2** (typage d'edge) : le rejet est un failure-edge.
- Prépare **P3.2** : `Gate(human)` a besoin de `Boundary(checkpoint)` pour la
  reprise.

Preuve de complétion :

1. Les six modes compilent via le `switch` unique ; ajout d'un mode = une
   branche + un cas de test.
2. `onboarding-crew` avec `Gate(mcp-trust)` refuse de compiler si le
   `crew-recherche` accède à un outil hors `allowedTools` (R-G1).
3. Un flow avec entrée externe → sortie sans guardrail refuse de compiler (R-G2).
