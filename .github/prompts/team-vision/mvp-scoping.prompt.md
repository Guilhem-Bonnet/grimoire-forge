---
description: "Priorisation MoSCoW rapide — décider en 10 minutes ce qui entre dans le MVP"
---

# Skill: MVP Scoping — MoSCoW Prioritization

Aide à définir le scope exact du MVP pour `{{project_or_feature}}` en utilisant le framework MoSCoW.

## Inputs
- **Projet/Feature** : `{{project_or_feature}}`
- **Contrainte temps** : `{{time_constraint}}` (ex: "2 sprints = 4 semaines")
- **Contrainte équipe** : `{{team_constraint}}` (ex: "1 dev + 1 designer, 50% de leur temps")
- **Objectif business MVP** : `{{business_goal}}` (ex: "valider que les users paient pour X")

## Framework MoSCoW Strict

### Must Have (in — MVP cassé sans ça)
> Critère : sans cette feature, le MVP ne peut pas être testé.

Pour chaque feature proposée, poser : **"Le MVP peut-il être testé sans cette feature ?"**
- Si NON → Must Have
- Si OUI → bloquer à Should ou Could

### Should Have (important mais pas bloquant pour le test)
### Could Have (nice to have si temps restant)
### Won't Have (hors scope — à documenter pour éviter le scope creep)

## Process

1. **Lister toutes les features envisagées** (brainstorm libre, 5-10 items)
2. **Appliquer le critère Must Have** rigoureusement — pas plus de 3-4 must haves
3. **Estimer chaque Must Have** : S/M/L (S = 1-2j, M = 3-5j, L = 1-2 semaines)
4. **Vérifier la faisabilité** : total Must Haves ≤ 80% de la capacité disponible
5. **Décider** : si too big → couper un Must Have ou réduire sa scope

## Output Attendu

```markdown
## MVP Scope — {{project_or_feature}} — {{date}}

**Contraintes** : {{time_constraint}} | {{team_constraint}}
**Hypothèse à valider** : {{business_goal}}

### Must Have (MVP core)
| Feature | Pourquoi critique | Estimation | Owner |
|---------|------------------|------------|-------|
| [F1]    | [raison]         | M (3j)     | dev   |

### Should Have (Sprint 2)
| Feature | Valeur | Estimation |
|---------|--------|------------|

### Could Have (si temps)
- [F5]
- [F6]

### Won't Have (v2 ou jamais)
- [F7] — raison explicite

**Capacité utilisée** : X/Y jours (Z%)
**Risque principal** : [1 phrase]
**Décision** : ✅ Scope validé / 🔴 Trop large — couper [F2]
```

Sauvegarder dans `_bmad-output/team-vision/mvp-scope-{{project_slug}}-{{date}}.md`
