---
description: "Architecture Decision Record — documenter un choix technique avec trade-offs"
---

# Skill: Architecture Decision Record (ADR)

Documente la décision architecturale pour `{{decision_topic}}`.

**Principe** : Un ADR capture le POURQUOI d'un choix technique. Pas ce qu'on a fait — pourquoi on l'a fait, ce qu'on a rejeté, et ce qu'on accepte comme conséquences.

## Contexte
- **Décision** : `{{decision_topic}}`
- **Contexte projet** : `{{project_context}}`
- **Contraintes** : `{{constraints}}` (budget, timeline, équipe, tech existant)
- **Mode** : `[THINK]` — délibération profonde obligatoire

## Process [THINK]

1. **Poser le problème** en une question précise (pas "quel framework ?" mais "quel framework pour une API REST haute disponibilité avec team de 2 devs Go-first ?")

2. **Lister N ≥ 3 options** réelles et sérieuses

3. **Pour chaque option** :
   - Avantages (factuel, pas marketing)
   - Inconvénients (honnêteté absolue)
   - Coût de migration si on change d'avis dans 18 mois
   - Qui dans l'équipe peut la maintenir ?

4. **Simuler les échecs** : "Si on choisit X et que le trafic x10 l'an prochain..."

5. **Décider** — une seule option, un justificatif de 2 lignes

## Template ADR Output

```markdown
# ADR-{{adr_number}} — {{decision_topic}}

**Date** : {{date}}
**Statut** : Proposé | Accepté | Déprécié | Remplacé par ADR-N
**Décideurs** : {{agents_or_humans}}

---

## Contexte

{{2-3 phrases décrivant le problème et pourquoi une décision est nécessaire maintenant}}

## Options Considérées

### Option A — {{nom}}
**Avantages** :
- [factuel]

**Inconvénients** :
- [honnête]

**Coût de migration** : [si on change d'avis]

### Option B — {{nom}}
[idem]

### Option C — {{nom}}
[idem]

---

## Décision

**Choix** : Option {{X}} — {{nom}}

**Justification** :
{{2 lignes max — pourquoi cette option vs les autres}}

## Conséquences

**Ce qu'on gagne** :
- [bénéfice concret]

**Ce qu'on accepte comme trade-off** :
- [limitation acceptée consciemment]

**Actions induites** :
- [ ] [action 1 — responsable]
- [ ] [action 2 — responsable]

---
*ADR créé par : {{agent}} | Projet : {{project_name}}*
```

Sauvegarder dans `_bmad-output/implementation-artifacts/adr-{{adr_slug}}.md`
ET référencer dans `_bmad/_memory/decisions-log.md`
