---
description: "Revue de code adversariale — trouver des problèmes réels, pas faire des compliments"
---

# Skill: Adversarial Code Review

Effectue une revue de code adversariale sur `{{files_or_pr}}`.

**Ton rôle** : Trouver activement des problèmes. Pas des best practices génériques — des bugs réels, des failles de sécurité, des problèmes de performance cachés dans CE code.

## Mode
`[PLAN]` d'abord — lister tous les findings. Puis `[ACT]` sur validation.

## Scope
- **Fichiers / PR** : `{{files_or_pr}}`
- **Focii** : `{{focus_areas}}` (ex: "sécurité + performances" ou "all")
- **Story de référence** : `{{story_file}}` (pour vérifier les ACs)

## Checklist de Revue (par ordre de criticité)

### 🔴 Sécurité
- [ ] Injections (SQL, NoSQL, OS command, LDAP)
- [ ] Authentification / autorisation manquante ou bypassable
- [ ] Données sensibles en clair (logs, variables, responses)
- [ ] CORS trop permissif, CSRF absent
- [ ] Rate limiting absent sur endpoints publics
- [ ] Inputs non validés / non sanitizés

### 🔴 Bugs potentiels
- [ ] Nil pointer / null reference non géré
- [ ] Race conditions et accès concurrent non protégé
- [ ] Boucles infinies possibles (condition d'arrêt manquante)
- [ ] Gestion d'erreurs incomplète (erreurs ignorées)
- [ ] Integer overflow / underflow dans les calculs critiques

### 🟡 Performances
- [ ] N+1 queries (boucle avec query SQL à chaque itération)
- [ ] Absence de pagination sur les endpoints de liste
- [ ] Objets volumineux chargés intégralement en mémoire
- [ ] Absence de cache sur les données peu volatiles

### 🟡 Maintenabilité
- [ ] Code dupliqué qui devrait être extrait
- [ ] Fonctions > 50 lignes (à décomposer)
- [ ] Nommage ambigu (variables single-letter hors scope minimal)
- [ ] TODO/FIXME laissés en place

### 🟢 Tests
- [ ] Edge cases non testés (null, empty, max values)
- [ ] Tests qui ne testent pas vraiment (tautologies)
- [ ] Mocks trop agressifs (test l'implémentation, pas le comportement)

## Output Format

```markdown
## Code Review — {{files_or_pr}} — {{date}}

### 🔴 Bloquants (à corriger avant merge)
**[SEC-001]** `src/auth.go:45` — JWT sans vérification de l'algorithme
→ Fix : ajouter `alg: "HS256"` dans les options de vérification
→ Impact : authentication bypass possible

### 🟡 Importants (à corriger avant livraison)
**[PERF-001]** `src/users.go:123` — N+1 query dans la boucle GetUserWithPosts
→ Fix : utiliser un JOIN ou chargement batch
→ Impact : {{N}} requêtes pour une page de 20 users

### 🟢 Suggestions (nice to have)
**[MAINT-001]** `src/helpers.go:34` — fonction ParseDate dupliquée 3x
→ Suggestion : extraire dans utils/date.go

## Verdict
🔴 BLOCKED — N bloquants à résoudre
/ 🟡 CONDITIONAL — Merge si [conditions]
/ ✅ APPROVED — RAS
```

Sauvegarder dans `_bmad-output/team-build/code-review-{{date}}.md`
