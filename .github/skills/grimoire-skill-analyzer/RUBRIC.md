# Rubrique de notation — 100 points

Référence détaillée pour [SKILL.md](SKILL.md) Step 2. Chaque critère = 0, partiel, ou max.
Partiel = exactement la moitié des points (arrondi inférieur).

## Contents

- Axe A : Frontmatter & Discoverability (25 pts)
- Axe B : Structure & Clarity (20 pts)
- Axe C : Token Economy (15 pts)
- Axe D : Procedural Quality (15 pts)
- Axe E : Robustness & Anti-patterns (15 pts)
- Axe F : Security & Safety (10 pts)
- Mode hook : critères additionnels

## Axe A — Frontmatter & Discoverability (25 pts)

| ID | Critère | Max | Comment scorer |
|---|---|---|---|
| A1 | `name` valide (lowercase, hyphens, ≤64 chars) | 3 | Tout ou rien |
| A2 | `description` non vide, ≤1024 chars | 3 | Tout ou rien |
| A3 | `description` à la 3e personne (pas "I/you/I'll") | 3 | Tout ou rien |
| A4 | `description` contient un marqueur "Use when:" ou triggers explicites | 5 | 5 si oui, 0 sinon |
| A5 | `description` contient à la fois le QUOI (action) et le QUAND (déclencheur) | 5 | 5 si les deux, 2 si l'un, 0 sinon |
| A6 | Triggers spécifiques et discriminants (pas "helper", "tools", "general") | 4 | 4 si ≥3 mots-clés discriminants, 2 si 1-2, 0 si vague |
| A7 | Pas de chevauchement >40% avec une autre skill (description Jaccard sur n-grams) | 2 | 2 si <40%, 1 si 40-60%, 0 si >60% (>80% = blocker) |

Pénalités :
- Reserved word (`anthropic`, `claude`) dans name → blocker `BL-RESERVED`.
- Description < 30 chars → blocker `BL-DESC-EMPTY`.

## Axe B — Structure & Clarity (20 pts)

| ID | Critère | Max | Comment scorer |
|---|---|---|---|
| B1 | Body ≤ 500 lignes | 3 | 3 si ≤500, 1 si 500-800, 0 si >800 (>1000 = blocker) |
| B2 | Section "Quand utiliser" / "When to use" présente avec ≥3 cas | 4 | 4 si présente et concrète, 2 si présente mais vague, 0 si absente |
| B3 | Procédure / process steps numérotés et clairs | 4 | 4 si steps explicites, 2 si seulement bullet vague, 0 si aucun process |
| B4 | Format de sortie attendu documenté (template, schéma JSON, exemple) | 3 | 3 si schéma précis, 1 si exemple seul, 0 si rien |
| B5 | Checklist / critères de succès | 3 | 3 si checklist actionable, 1 si critères en prose, 0 si absent |
| B6 | Conditions d'arrêt / Red Flags | 3 | 3 si STOP conditions explicites, 1 si implicite, 0 si rien |

## Axe C — Token Economy (15 pts)

| ID | Critère | Max | Comment scorer |
|---|---|---|---|
| C1 | Pas d'explications inutiles (l'agent connaît déjà le concept) | 4 | 4 si concis, 2 si quelques redondances, 0 si verbeux |
| C2 | Pas de duplication interne (sections qui se répètent) | 3 | 3 si propre, 1 si 1-2 répétitions, 0 si répétitif |
| C3 | Profondeur des références ≤ 1 niveau depuis SKILL.md | 3 | 3 si tout est à 1 niveau, 0 si imbrications |
| C4 | Fichiers de référence >100 lignes ont une TOC en tête | 2 | 2 si TOC présente, 0 sinon (N/A si tout ≤100) |
| C5 | Code/exemples concrets (input/output réels), pas abstraits | 3 | 3 si concret, 1 si placeholder seul, 0 si vide |

## Axe D — Procedural Quality (15 pts)

| ID | Critère | Max | Comment scorer |
|---|---|---|---|
| D1 | Degrés de liberté adaptés à la fragilité (high/medium/low explicite) | 3 | 3 si calibré, 1 si uniforme, 0 si inadapté |
| D2 | Feedback loops / validation steps pour opérations critiques | 3 | 3 si présent, 1 si mentionné, 0 si absent quand requis |
| D3 | Workflows complexes (>5 steps) ont une checklist trackable | 3 | 3 si checklist, 1 si seulement steps numérotés, 0 si aucun |
| D4 | Decision points conditionnels clairs (si X → ..., sinon → ...) | 3 | 3 si explicite, 1 si implicite, 0 si manquant alors qu'utile |
| D5 | Terminologie cohérente (pas de mix "field/box/element") | 3 | 3 si cohérent, 1 si quelques variations, 0 si chaotique |

## Axe E — Robustness & Anti-patterns (15 pts)

| ID | Critère | Max | Comment scorer |
|---|---|---|---|
| E1 | Pas d'info time-sensitive (sauf section "Old patterns") | 3 | 3 si aucune date périssable, 0 si dépendance temporelle non isolée |
| E2 | Forward slashes uniquement dans les paths | 2 | 2 si propre, 0 si backslash trouvé |
| E3 | Pas de "too many options" (≤2 alternatives sans guidance) | 3 | 3 si défaut clair, 1 si plusieurs avec guidance, 0 si dump d'options |
| E4 | Scripts gèrent leurs erreurs (pas de "punt to LLM") | 2 | 2 si try/except ou validation, 0 si fail silencieux |
| E5 | Pas de "voodoo constants" (chaque magic number commenté) | 2 | 2 si justifié, 1 si en partie, 0 si magic numbers libres |
| E6 | MCP tools référencés en `Server:tool_name` (si applicable) | 1 | 1 si fully qualified, 0 sinon, N/A si pas de MCP |
| E7 | Dépendances externes déclarées (packages, binaires) | 2 | 2 si liste explicite, 0 si "use library X" sans install |

## Axe F — Security & Safety (10 pts)

| ID | Critère | Max | Comment scorer |
|---|---|---|---|
| F1 | Aucune instruction qui override le system prompt | 3 | 3 si propre, 0 si "ignore previous", "you are now", etc. |
| F2 | Pas d'exfiltration réseau silencieuse | 2 | 2 si pas d'appel non déclaré, 0 si curl/wget non justifié |
| F3 | Commandes destructives gardées (confirmation, dry-run, rollback) | 2 | 2 si garde, 0 si rm -rf nu |
| F4 | Pas de secrets / tokens hardcodés | 2 | 2 si propre, 0 si pattern détecté |
| F5 | Sources externes (URLs) explicites et de confiance | 1 | 1 si listées, 0 si fetch arbitraire |

## Mode hook — Critères additionnels

Quand `mode = "hook"`, les axes B et F sont étendus :

### B (hook spécifique)

| ID | Critère | Max | Comment scorer |
|---|---|---|---|
| BH1 | `event` parmi les valeurs autorisées | requis (sinon `BL-HOOK-EVENT`) |
| BH2 | `timeout` déclaré (≤30s recommandé) | requis (sinon `BL-HOOK-NO-TIMEOUT`) |
| BH3 | Hook référencé dans `hook-safety-registry.json` | requis (sinon `BL-HOOK-NOT-REGISTERED`) |
| BH4 | Mode initial = `shadow` ou `canary` (pas direct `enforced`) | warn si `enforced` direct |

### F (hook spécifique)

| ID | Critère | Comment scorer |
|---|---|---|
| FH1 | Script passe par `grimoire-hook-gateway.sh` | requis (sinon `BL-HOOK-NO-GATEWAY`) |
| FH2 | Pas de `eval`, `exec "$STDIN"`, `bash -c "$INPUT"` | requis (sinon `BL-HOOK-EVAL`) |
| FH3 | Sortie JSON validée avant émission | bonus |
| FH4 | Erreurs catchées en fail-open par défaut (`echo "{}"; exit 0`) | bonus |

## Calcul final

```
score = sum(axes_scores)
si blockers != [] → verdict = "reject"
sinon si strict ET score < 90 → "revise"
sinon si score < 60 → "reject"
sinon si score < 75 → "revise"
sinon si score < 90 → "pass" (Experimental)
sinon → "pass" (Stable-ready)
```
