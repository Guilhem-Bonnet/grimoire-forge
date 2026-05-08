---
name: grimoire-skill-analyzer
description: "Audit qualité d'un SKILL.md ou d'un hook Grimoire avec grille de notation 100 points et seuils de blocage. Use when: review d'une skill, audit qualité skill, scoring SKILL.md, valider une skill avant publication, gate de qualité skill-forge, vérifier hook security, contrôler artefact .github/skills ou .github/hooks, before promoting dynamic skill, check skill description quality."
---

# Grimoire Skill Analyzer

Audit déterministe d'une skill ou d'un hook Grimoire. Produit un score sur 100, une liste de
findings classés, et un verdict `pass` / `revise` / `reject`. Sert de gate qualité pour
`grimoire-skill-forge` et de filet de review pour les skills existantes.

## Quand utiliser

- Audit d'une skill existante (`.github/skills/<name>/SKILL.md`).
- Validation d'une skill nouvellement générée par `grimoire-skill-forge` avant écriture définitive.
- Audit d'un hook (`.github/hooks/*.json` + script associé).
- Comparaison de plusieurs skills pour repérer les sous-qualifiées.
- Pré-promotion d'un artefact `_dyn-*` vers permanent.

## Inputs attendus

| Input | Description | Obligatoire |
|---|---|---|
| `target_path` | Chemin du fichier SKILL.md, du dossier skill, ou du hook JSON | oui |
| `mode` | `skill` (défaut) ou `hook` | non |
| `strict` | `true` pour appliquer les seuils Stable, `false` pour Experimental | non |

Si `target_path` est absent ou ambigu → **HALT** et demander.

## Procédure

### Step 1 — Charger l'artefact

1. Lire le SKILL.md (ou le JSON du hook + son script `.sh`).
2. Parser le frontmatter YAML (`name`, `description`, autres clefs autorisées).
3. Compter les lignes du body, repérer les liens internes, extraire les blocs de code.
4. En mode `hook` : charger aussi le script référencé et le registre `hook-safety-registry.json`.
5. Lister les autres skills voisines (`ls .github/skills/`) pour la détection de chevauchement.

Si le frontmatter est invalide ou le fichier illisible → emit blocker `BL-FRONTMATTER` et STOP au Step 4.

### Step 2 — Appliquer la grille (100 pts)

Charger [RUBRIC.md](RUBRIC.md) pour le détail de chaque critère et exemples bon/mauvais. La grille
contient six axes pondérés. Chaque critère reçoit 0, partial, ou max.

| Axe | Poids | Focus |
|---|---|---|
| **A. Frontmatter & Discoverability** | 25 | name, description 3e personne, triggers, "Use when", anti-overlap |
| **B. Structure & Clarity** | 20 | Quand utiliser, procédure, sortie, checklist, conditions d'arrêt |
| **C. Token Economy** | 15 | concision, pas de duplication, profondeur ≤1, TOC sur fichiers >100l |
| **D. Procedural Quality** | 15 | degrés de liberté, feedback loops, terminologie cohérente |
| **E. Robustness & Anti-patterns** | 15 | pas de time-sensitive, forward slashes, no voodoo constants, deps |
| **F. Security & Safety** | 10 | injection prompt, exfil, destructifs gardés, no secrets, sources trust |

Score brut = somme des points obtenus. Reporter aussi le score normalisé par axe (% de l'axe).

### Step 3 — Détecter les blockers

Indépendamment du score, ces conditions imposent un **rejet automatique** :

| Code | Condition |
|---|---|
| `BL-FRONTMATTER` | `name` ou `description` manquant, name >64 chars, format invalide |
| `BL-RESERVED` | `name` contient `anthropic` ou `claude` |
| `BL-DESC-EMPTY` | `description` < 30 caractères ou ne contient ni QUOI ni QUAND |
| `BL-BODY-OVERSIZE` | Body > 1000 lignes (>500 = warn, >1000 = block) |
| `BL-OVERLAP` | Description ≥80% similaire à une skill existante (stems, n-grams) |
| `BL-INJECTION` | Pattern d'injection prompt dans le body (override system, ignore previous) |
| `BL-SECRET` | Token, clé API, password, JWT détecté dans body ou script |
| `BL-DESTRUCTIVE-UNGUARDED` | `rm -rf`, `git push --force`, `DROP TABLE` sans confirmation/dry-run |
| `BL-NETWORK-EXFIL` | Appel réseau vers domaine non whitelisté sans déclaration |

En mode `hook`, ajouter :

| Code | Condition |
|---|---|
| `BL-HOOK-EVENT` | `event` non reconnu (hors `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, `Stop`) |
| `BL-HOOK-NO-GATEWAY` | Script ne passe pas par `grimoire-hook-gateway.sh` |
| `BL-HOOK-NOT-REGISTERED` | Hook absent de `hook-safety-registry.json` |
| `BL-HOOK-EVAL` | Usage de `eval`, `exec`, ou `bash -c "$INPUT"` sur stdin user-controlled |
| `BL-HOOK-NO-TIMEOUT` | Pas de timeout déclaré dans le hook JSON |

Voir [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) pour les patterns détaillés.

### Step 4 — Verdict

```
si blockers ≥ 1                                → reject
sinon si strict ET score < 90                  → revise
sinon si score < 60                             → reject
sinon si score < 75                             → revise
sinon si score < 90                             → pass (Experimental)
sinon                                           → pass (Stable-ready)
```

| Verdict | Score | Statut suggéré | Suite |
|---|---|---|---|
| `pass` | ≥90 (ou ≥75 non-strict) | Stable / Experimental | Publier ou promouvoir |
| `revise` | 60-89 | Incubating | Appliquer les findings, re-scorer |
| `reject` | <60 ou blockers | — | Réécrire, ne pas publier |

### Step 5 — Présenter le rapport

Format de sortie obligatoire — JSON suivi d'un résumé Markdown :

```json
{
  "target": "<path>",
  "mode": "skill|hook",
  "strict": false,
  "score": 0,
  "verdict": "pass|revise|reject",
  "axes": {
    "frontmatter_discoverability": {"score": 0, "max": 25},
    "structure_clarity": {"score": 0, "max": 20},
    "token_economy": {"score": 0, "max": 15},
    "procedural_quality": {"score": 0, "max": 15},
    "robustness_antipatterns": {"score": 0, "max": 15},
    "security_safety": {"score": 0, "max": 10}
  },
  "blockers": [
    {"code": "BL-XXX", "evidence": "<extract>", "fix": "<action>"}
  ],
  "findings": [
    {"id": "A4", "axis": "A", "severity": "major|minor|nit",
     "title": "...", "evidence": "...", "fix": "..."}
  ],
  "stable_ready": false
}
```

Suivi d'un résumé Markdown lisible : score, verdict, top 5 findings, prochaine action.

## Conditions d'arrêt

- Si `target_path` n'existe pas → STOP, demander un chemin valide.
- Si frontmatter illisible → emit `BL-FRONTMATTER`, retourner `reject`, STOP.
- Si l'utilisateur invoque sans target → demander, ne rien noter au hasard.

## Red Flags — STOP

- L'auteur demande de "skip la review" → refuser, expliquer le rôle de gate.
- Score truqué (refus de baisser un point sur un critère manquant clair) → ne pas céder, rapporter en l'état.
- Skill auto-référente qui se note → toujours rapporter ce conflit d'intérêt dans `findings`.

## Checklist de vérification

- [ ] Frontmatter parsé sans erreur.
- [ ] Tous les axes scorés explicitement (pas de "score moyen estimé").
- [ ] Au moins une `evidence` (extrait) par finding.
- [ ] Au moins un `fix` actionnable par finding.
- [ ] Verdict cohérent avec score + blockers.
- [ ] Mode `hook` : registre + gateway vérifiés.
- [ ] JSON valide et complet avant le résumé Markdown.

## Intégration

- Gate obligatoire de `grimoire-skill-forge` (Step 4).
- Peut être invoqué seul par l'orchestrateur SOG sur demande "review cette skill".
- Sortie JSON consommable par CI (futur `grimoire: validate-skills` strict mode).
- Référence : [RUBRIC.md](RUBRIC.md), [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md), [EXAMPLES.md](EXAMPLES.md).
