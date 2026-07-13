# SKILL_TEMPLATE.md — Template de génération

Template normalisé pour [SKILL.md](SKILL.md) Step 3. Tous les placeholders `{{...}}` doivent être
substitués. Section optionnelle indiquée par `<!-- optional -->`. Body cible 200-300 lignes,
plafond strict 500.

## Contents

- Frontmatter
- Squelette body
- Règles de substitution

## Frontmatter

```yaml
---
name: {{slug}}
description: "{{quoi_action}}. Use when: {{trigger_1}}, {{trigger_2}}, {{trigger_3}}, {{trigger_4_5_optional}}."
created: "{{iso_date}}"
---
```

Contraintes :

- `slug` : lowercase, hyphens, ≤64 chars, pas `anthropic`/`claude`.
- `description` : ≤1024 chars, 3e personne, contient QUOI + "Use when:" + ≥3 triggers.
- Triggers discriminants (pas "helper", "tools", "general").

## Squelette body

```markdown
# {{Titre human-readable}}

{{Une phrase qui résume ce que fait la skill et le résultat produit.}}

## Quand utiliser

- {{Cas concret 1}}.
- {{Cas concret 2}}.
- {{Cas concret 3}}.
{{- Cas concret 4 (optional)}}

## Quand NE PAS utiliser

<!-- optional, mais recommandé si recouvrement avec autre skill -->

- {{Cas où une autre primitive est meilleure}}.
- {{Cas hors scope}}.

## Inputs

| Input | Description | Obligatoire |
|---|---|---|
| `{{input_1}}` | {{description}} | oui |
| `{{input_2}}` | {{description}} | non |

## Procédure

### Step 1 — {{Action courte}}

{{Instructions concises. L'agent connaît déjà les concepts génériques — ne pas les expliquer.}}

### Step 2 — {{Action}}

{{...}}

### Step N — {{Présenter / persister}}

{{...}}

## Format de sortie

{{Schéma JSON, template Markdown, ou exemple input → output. Choisir un seul format primaire.}}

## Conditions d'arrêt

- {{Condition 1 → action}}.
- {{Condition 2 → action}}.

## Red Flags — STOP

<!-- optional pour skills sensibles -->

- {{Pattern dangereux à refuser}}.

## Checklist de vérification

- [ ] {{Critère 1}}.
- [ ] {{Critère 2}}.
- [ ] {{Critère 3}}.

## Intégration

- {{Skill/agent en amont}}.
- {{Skill/agent en aval}}.
- {{Référence vers RUBRIC.md, EXAMPLES.md, ou autre fichier bundlé si présent}}.
```

## Règles de substitution

| Placeholder | Source | Validation |
|---|---|---|
| `{{slug}}` | Step 2 intake | regex `^[a-z][a-z0-9-]{2,63}$` |
| `{{quoi_action}}` | Step 2 intent | ≥10 chars, 3e personne, pas de "I" / "you" / "I'll" |
| `{{trigger_N}}` | Step 2 triggers | ≥3 fournis, chacun ≥2 mots, discriminant |
| `{{iso_date}}` | runtime | format `YYYY-MM-DD` |
| `{{Titre human-readable}}` | dérivé du slug | Title Case, sans tiret |
| `{{Cas concret N}}` | Step 2 ou inféré | phrase complète, déclencheur clair |
| `{{Schéma de sortie}}` | Step 2 | JSON valide ou Markdown template |

## Anti-patterns à refuser dans la génération

- `description: "Helper for X"` → trop vague, refuser.
- `description: "I help users with X"` → 1ère personne, refuser.
- `description` qui ne contient pas "Use when" → refuser.
- Body qui commence par "In this skill, we will..." → couper, l'agent sait déjà.
- Procédure d'1 seul step → suspect, soit ce n'est pas une skill, soit elle est trop fine.
- Section "When to use" en bullet uniques répétitifs → refuser, demander vrais cas.

## Bundled files (optionnel)

Si la skill nécessite des fichiers additionnels :

- Garder à 1 niveau de profondeur depuis SKILL.md (pas d'imbrication).
- Ajouter une TOC en tête si >100 lignes.
- Nommer descriptivement (`RUBRIC.md`, pas `doc1.md`).
- Référencer explicitement depuis SKILL.md.
