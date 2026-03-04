---
description: "Audit de sécurité infrastructure — OWASP, least privilege, secrets, CVEs"
---

# Skill: Security Audit — Infrastructure & Code

Effectue un audit de sécurité complet sur `{{scope}}`.

## Mode
`[PLAN]` — lister tous les findings. Puis `[ACT]` sur validation pour les corrections automatisables.

## Scope
- **Périmètre** : `{{scope}}` (ex: "infra Terraform + API Go", "Docker + K8s", "tout")
- **Standards** : OWASP Top 10, CIS Benchmarks, principe de moindre privilège

## Checklist par Couche

### 🔴 Secrets & Credentials
- [ ] Secrets dans le code source (et l'historique git)
- [ ] Variables d'environnement exposées dans les logs
- [ ] Clés API avec permissions trop larges
- [ ] Rotation des secrets en place ?
- [ ] Vault ou solution de gestion des secrets utilisée ?

**Commandes** :
```bash
# Détecter secrets dans le code
grep -r "password\|secret\|api_key\|token" --include="*.go,*.py,*.ts,*.yaml,*.env" . | grep -v "_test\.\|\.example\|\.tpl"
# Truffledog / gitleaks si installé
trufflehog git file://. 2>/dev/null | head -50
```

### 🔴 Authentification & Autorisation
- [ ] Endpoints sans authentification (les identifier explicitement)
- [ ] JWT : algorithme vérifié, expiration courte, refresh token rotation
- [ ] RBAC : les rôles sont-ils correctement appliqués ?
- [ ] Accès admin protégé par MFA ?

### 🔴 Infrastructure
- [ ] Ports exposés non nécessaires (principe : ouvrir le minimum)
- [ ] Security Groups / Firewall rules trop permissifs (ex: 0.0.0.0/0)
- [ ] Images Docker non officielles ou non pinned
- [ ] Containers tournant en root
- [ ] Kubernetes : RBAC activé, Network Policies en place ?

### 🟡 Dépendances
- [ ] Vulnérabilités CVE connues dans les dépendances directes

```bash
# Go
govulncheck ./...
# Node
npm audit --audit-level=high
# Python
pip-audit
# Docker images
docker scout cves {{image}}
```

### 🟡 Configuration
- [ ] HTTPS/TLS partout (pas de HTTP en production)
- [ ] CORS configuré (pas wildcard en prod)
- [ ] Rate limiting présent sur les endpoints publics
- [ ] Headers sécurité HTTP (CSP, HSTS, X-Frame-Options)

### 🟢 Observabilité Sécurité
- [ ] Logs des accès et des échecs d'auth
- [ ] Alertes sur les patterns suspects (brute force, enumération)

## Output Format

```markdown
## Security Audit Report — {{scope}} — {{date}}

### Score Global : {{score}}/10

### 🔴 Critiques (corriger immédiatement)
| ID | Localisation | Problème | CVSS | Fix recommandé |
|----|-------------|----------|------|----------------|
| SEC-001 | `infra/main.tf:45` | Security group 0.0.0.0/0 sur port 22 | 9.8 | Restreindre à IP bureau |

### 🟡 Importants (corriger avant prochaine release)
| ID | Localisation | Problème | CVSS | Fix recommandé |

### 🟢 Suggestions
- [S1]

### Actions Correctives (par priorité)
- [ ] [SEC-001] Fermer port 22 public → responsable: ops → délai: aujourd'hui
- [ ] [SEC-002] Activer gitleaks en pre-commit → responsable: dev → délai: cette semaine
```

Sauvegarder dans `_bmad-output/implementation-artifacts/security-audit-{{date}}.md`
