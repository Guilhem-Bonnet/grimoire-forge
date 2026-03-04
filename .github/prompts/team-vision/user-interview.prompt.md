---
description: "Interview utilisateur guidé — transformer des signaux flous en besoins précis"
---

# Skill: User Interview Protocol

Conduis un interview utilisateur structuré pour comprendre les vrais besoins derrière `{{feature_or_problem}}`.

## Contexte
- **Sujet** : `{{feature_or_problem}}`
- **Persona cible** : `{{persona}}` (ex: "CTO startup / 50 empleados" ou décrire librement)
- **Durée simulée** : 20 questions max

## Protocole d'Interview (5 phases)

### Phase 1 — Contexte (3 questions)
Comprendre la situation actuelle sans orienter.
- "Parlez-moi de comment vous gérez [domaine] aujourd'hui."
- "Qu'est-ce qui déclenche ce besoin ?"
- "Qui d'autre dans votre équipe est impacté ?"

### Phase 2 — Douleurs (4 questions)
Identifier la frustration réelle.
- "Qu'est-ce qui vous frustre le plus avec la solution actuelle ?"
- "Combien de temps perdez-vous à cause de ce problème ?"
- "Qu'avez-vous déjà essayé ? Pourquoi ça n'a pas marché ?"
- "Quel serait l'impact si ce problème disparaissait ?"

### Phase 3 — Jobs-to-be-Done (3 questions)
- "Quand [situation], je veux [motivation] pour que [résultat]."
- "Si vous aviez une baguette magique, votre solution idéale ferait quoi ?"
- "Quel est le bénéfice ultime que vous cherchez ?"

### Phase 4 — Validation Hypothèse (3 questions)
- Présenter brièvement `{{feature_or_problem}}` comme solution potentielle
- "Est-ce que ça adresse votre besoin ? Qu'est-ce qui manque ?"
- "Seriez-vous prêt à payer pour ça ? Quel prix vous semblerait juste ?"

### Phase 5 — Closing (2 questions)
- "Qu'est-ce que je n'ai pas demandé et que vous vouliez dire ?"
- "Y a-t-il quelqu'un d'autre que je devrais interviewer ?"

## Output Attendu

```markdown
## Synthèse Interview — {{persona}} — {{date}}

**Jobs-to-be-Done identifiés** :
- [JTBD 1] Quand ___ je veux ___ pour que ___
- [JTBD 2] ...

**Douleurs validées** :
- [D1] (criticité : haute/moyenne/basse)
- [D2]

**Hypothèses invalidées** :
- [H1] — raison

**Insights surprenants** :
- [I1]

**Décision produit recommandée** :
[1 phrase — ce qu'on fait/ne fait pas suite à cet interview]
```

Sauvegarder dans `_bmad-output/team-vision/user-interviews/interview-{{persona_slug}}-{{date}}.md`
