---
description: "Runbook incident — procédure step-by-step pour les incidents les plus probables"
---

# Skill: Incident Runbook Generator

Génère un runbook opérationnel pour `{{incident_type}}` sur `{{project_name}}`.

## Contexte
- **Type d'incident** : `{{incident_type}}` (ex: "service down", "DB full", "latence élevée API", "déploiement raté")
- **Environnement** : `{{environment}}` (production / staging)
- **Stack** : `{{stack}}`
- **SLA** : `{{sla}}` (ex: "99.9% uptime, MTTR < 30min")

## Structure du Runbook

### 1. Détection
Comment savoir que cet incident se produit ?
- Alerte monitoring qui se déclenche
- Symptôme visible (erreur user, dashboard rouge)
- Commande de diagnostic première

```bash
# Commandes de diagnostic initial
{{diagnostic_commands}}
```

### 2. Escalation Matrix

| Sévérité | Critère | Action Immédiate | Escalader à |
|----------|---------|-----------------|-------------|
| P1 — Critique | Service entièrement KO | PagerDuty + War room | {{p1_contact}} |
| P2 — Majeur | Dégradation > 50% users | Slack alert | {{p2_contact}} |
| P3 — Mineur | Impact < 10% users | Ticket jira | {{p3_contact}} |

### 3. Procédure de Résolution

Pour chaque type d'incident :

```
INCIDENT: {{incident_type}}

Étape 1 — Confirmer le problème
  → Commande : {{step1_command}}
  → Expected : {{step1_expected}}
  → Si KO : continuer étape 2

Étape 2 — Isoler la cause
  → Commande : {{step2_command}}
  → Causes fréquentes :
    a) {{cause_a}} → Fix : {{fix_a}}
    b) {{cause_b}} → Fix : {{fix_b}}

Étape 3 — Appliquer le fix
  → {{fix_procedure}}
  → Vérifier : {{verification_command}}

Étape 4 — Confirmer la résolution
  → Métriques revenues à la normale
  → Alertes dégagées
  → Communication aux users (si applicable)

Étape 5 — Post-mortem
  → Durée totale de l'incident
  → Cause racine
  → Action corrective pour éviter la récurrence
```

### 4. Commandes Utiles (Quick Reference)

```bash
# Vérifier le statut des services
{{service_status_command}}

# Voir les logs en temps réel
{{log_command}}

# Redémarrer un service
{{restart_command}}

# Rollback d'un déploiement
{{rollback_command}}
```

### 5. Post-Mortem Template

Ajouter dans `_bmad-output/team-ops/incident-log.md` après résolution :
```
[{{date}}] {{incident_type}} — Durée : {{duration}} — Cause : {{root_cause}} — Fix : {{fix}} — Action : {{preventive_action}}
```

## Output

Sauvegarder dans `_bmad-output/implementation-artifacts/runbook-{{incident_slug}}-{{date}}.md`
