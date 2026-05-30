# PRD — BMAD Custom Kit v2 : Le Meilleur Framework d'Agents IA Local

> **Statut** : Draft v1 — 23 février 2026  
> **Auteur** : John (PM)  
> **Projets de référence** : Anime-Sama-Downloader (Go+React), Terraform-HouseServer (Infra/K3s)

---

## 1. Problème

### Ce que l'IA locale fait mal aujourd'hui — constaté sur tes projets réels

| Frustration | Preuve concrète |
|---|---|
| **Demi-livraison** | 77 bugs trouvés en bug-hunt party-mode — ils n'auraient pas été trouvés sans forcer une vérification systématique |
| **Connaissance incohérente** | L'agent affirme "tout vu", une deuxième question fait émerger de nouveaux éléments |
| **Équipe statique** | Même setup BMAD pour un projet Go+React et pour de l'infra Terraform+K3s+Ansible |
| **Workflow cassé** | L'agent demande confirmation pour des décisions triviales, s'arrête en plein milieu |
| **Zéro preuve d'exécution** | "Terminé" sans `go test`, sans `tsc`, sans `terraform validate` |

### Ce qui fonctionne déjà bien (à conserver et amplifier)

- Le `shared-context.md` + `decisions-log.md` : la mémoire partagée fonctionne
- Le party-mode pour coordination multi-agents (bug-hunt en vagues)
- Les agents avec persona forte et domaine précis (Gopher, Sakura, Sensei...)
- Le `agent-base.md` comme protocole commun

---

## 2. Vision Produit

> **BMAD Custom Kit est l'unique framework d'agents IA local qui compose automatiquement une équipe spécialisée selon ton stack, garantit la complétion réelle avec preuves, et s'améliore à chaque cycle — sans jamais quitter ton IDE.**

### Ce qui nous différencie de tout ce qui existe

| Framework | Dépendance cloud | Auto-configuration | Completion Contract | Self-improvement |
|---|---|---|---|---|
| CrewAI | API OpenAI requis | ❌ | ❌ | ❌ |
| AutoGen | Configurable | ❌ | ❌ | ❌ |
| LangGraph | API ou local | ❌ | ❌ | ❌ |
| Cursor Rules | IDE only | ❌ | ❌ | ❌ |
| BMAD v1 | IDE only | ❌ partial | ❌ | ❌ |
| **BMAD Custom Kit v2** | **0 cloud** | **✅ auto** | **✅ built-in** | **✅ built-in** |

---

## 3. Les 4 Piliers Techniques

### Pilier 1 — Completion Contract (CC)

**Problème résolu** : L'agent dit "terminé" alors que rien ne fonctionne.

**Principe** : Chaque tâche a une **Definition of Done (DoD) objective et exécutable** vérifiée automatiquement avant de rendre la main.

**Fonctionnement** :
```
TÂCHE → IMPLÉMENTATION → VÉRIFICATION AUTOMATIQUE → RÉSULTAT
                              ↓
                     Si échec → l'agent CONTINUE, ne rend pas la main
```

**DoD par type de contexte** (détecté automatiquement) :

| Contexte détecté | Vérifications obligatoires |
|---|---|
| Go | `go build ./...` + `go test ./...` + `go vet ./...` |
| TypeScript/React | `tsc --noEmit` + `vitest run` |
| Terraform | `terraform validate` + `terraform fmt -check` + `tflint` |
| Ansible | `ansible-lint` + `yamllint` |
| Python | `pytest` + `mypy` / `ruff` |
| Docker | `docker build` + healthcheck test |
| Kubernetes | `kubectl apply --dry-run=server` + `kubeval` |

**Règle non-négociable dans agent-base.md** :
```
JAMAIS écrire "terminé", "fait", "implémenté" sans avoir exécuté
et affiché le résultat de la vérification correspondante au contexte.
Si la vérification échoue → corriger avant de rendre la main.
```

---

### Pilier 2 — Modal Team Engine (MTE)

**Problème résolu** : Même équipe générique pour tous les projets.

**Principe** : Au premier lancement dans un projet, le framework **scanne le codebase et compose l'équipe optimale**.

**Fonctionnement** :

```
bmad-init.sh --auto → SCAN → DETECT STACK → COMPOSE TEAM → GENERATE AGENTS
```

**Détection automatique** (via scan de fichiers) :

| Signal détecté | Agents activés |
|---|---|
| `*.go` + `go.mod` | Gopher (Go Expert) + Tester Go |
| `*.tsx` / `*.ts` + `package.json` | Sakura (React/TS Expert) |
| `*.tf` / `*.tfvars` | Forge (Terraform) |
| `k8s/` / `*.yaml` avec `kind:` | Helm (K8s) |
| `ansible/` / `playbook*.yml` | Ansible Expert |
| `docker-compose*.yml` / `Dockerfile` | Container Expert |
| `*.py` + `requirements.txt` | Python Expert |
| Toujours inclus | Atlas (Navigation) + Sentinel (Qualité) + Mnemo (Mémoire) |

**Recomposition dynamique** : Quand la conversation glisse vers un domaine couvert par un agent inactif, une ligne dans `shared-context.md` suggère le switch.

---

### Pilier 3 — Shared Brain (SB)

**Problème résolu** : Connaissances incohérentes, contexte perdu entre sessions.

**Architecture mémoire** (0 dépendance externe, zéro cloud) :

```
shared-context.md          ← Snapshot projet (stack, métriques, archi)
decisions-log.md           ← Décisions + raisonnement
agent-learnings/{agent}.md ← Learnings par domaine
session-state.md           ← État courant + prochaine étape
contradiction-log.md       ← Conflits détectés entre agents [NOUVEAU]
```

**Auto-scan au démarrage** : Chaque agent relit `shared-context.md` ET recalcule les métriques clés du projet (nombre de fichiers, derniers commits, tests pass/fail) pour avoir une image réelle, pas stale.

**Contradiction Detection** : Quand un agent ajoute un learning qui contredit un existant → log automatique dans `contradiction-log.md` + alerte dans le greeting de la prochaine session.

**Fallback Enterprise** : Tout fonctionne en pur fichiers Markdown/JSON. Aucun MCP, aucune API, aucun service externe requis. MCP local (filesystem) est supporté comme option si disponible.

---

### Pilier 4 — Self-Improvement Loop (SIL)

**Problème résolu** : Le framework stagne, les mêmes erreurs se répètent.

**Deux mécanismes** :

**A) Learning Loop** (par cycle de travail)
```
SESSION → LEARNINGS ajoutés → MNEMO consolide → shared-context.md enrichi
```
Les patterns récurrents (ex: "toujours vérifier les CORS en premier sur ce projet") remontent dans `shared-context.md` et deviennent du contexte partagé automatique.

**B) Agent Evolution Loop** (meta-niveau)
```
Sentinel analyse les patterns d'échec → propose des modifications dans agent-base.md
```
Sentinel a maintenant une action dédiée : **"Analyser les patterns d'échec et proposer une amélioration du framework"** — il lit les decisions-log, agent-learnings, contradiction-log, et propose des ajouts concrets à `agent-base.md`.

---

## 4. Roadmap Priorisée

### Sprint 0 — Fondations (maintenant)
**Objectif** : Stabiliser ce qui existe, poser les conventions v2.

- [ ] Refactoring `agent-base.md` : intégrer le Completion Contract
- [ ] Créer le template `DEFINITION_OF_DONE.md` par type de contexte
- [ ] Ajouter `contradiction-log.md` dans la structure mémoire
- [ ] Mettre à jour `bmad-init.sh` avec scan automatique du stack

### Sprint 1 — Completion Contract
**Objectif** : Zéro "terminé" sans preuve.

- [ ] Protocole CC dans agent-base.md (règles non-négociables)
- [ ] Scripts de vérification par contexte (`cc-verify.sh` dispatché par stack)
- [ ] Validation sur Anime-Sama-Downloader (Go + React → CC opérationnel)
- [ ] Validation sur Terraform-HouseServer (Terraform + K8s → CC opérationnel)

### Sprint 2 — Modal Team Engine
**Objectif** : `bmad-init.sh --auto` compose la bonne équipe.

- [ ] Logique de détection stack dans `bmad-init.sh`
- [ ] Bibliothèque d'agents spécialisés (Go, React/TS, Terraform, K8s, Ansible, Python, Docker)
- [ ] Chaque agent généré avec : persona forte + DoD correspondant au domaine
- [ ] Test : déployer sur les deux projets de référence

### Sprint 3 — Self-Improvement Loop
**Objectif** : Le framework s'améliore à chaque cycle.

- [ ] Action Sentinel : `Analyser patterns d'échec → proposer amélioration framework`
- [ ] `maintenance.py` : détection automatique des contradictions cross-agents
- [ ] Auto-promotion learnings récurrents → `shared-context.md`
- [ ] Changelog automatique des évolutions du framework

### Sprint 4 — Polish & Distribution
**Objectif** : Utilisable par quelqu'un d'autre que toi.

- [ ] README revu : pitch clair, comparatif vs concurrents, quick-start 5 min
- [ ] Archétype `dev-fullstack` (générique web app)
- [ ] Archétype `infra-ops` v2 (avec CC Terraform/K8s intégré)
- [ ] Documentation de contribution
- [ ] Exemples concrets avec les deux projets de référence

---

## 5. Métriques de Succès

| Métrique | Aujourd'hui | Cible v2 |
|---|---|---|
| % tâches livrées sans bug évident | ~60% | >95% |
| Temps moyen pour composer une équipe | Manuel (30 min) | Automatique (<1 min) |
| Contexte perdu entre sessions | Fréquent | Jamais |
| Contradictions non détectées | Fréquent | Auto-détectées |
| Setup sur nouveau projet | ~1h | <5 min |

---

## 6. Contraintes Non-Négociables

- **Zero cloud** : tout fonctionne hors-ligne, sans API externe
- **Zero install complexe** : `bash bmad-init.sh` suffit, Python optionnel pour la mémoire sémantique
- **Enterprise-ready** : fallback pur fichiers si MCP non autorisé
- **VS Code natif** : `.github/agents/` + `.github/prompts/` uniquement
- **Rétrocompatible** : les projets existants (Anime-Sama, Terraform) fonctionnent sans migration forcée

---

## 7. Prochaine Action Immédiate

**Commencer par Sprint 0** : Refactoring `agent-base.md` avec le Completion Contract.  
C'est le levier le plus impactant — il résout directement la frustration principale en 1 fichier.

> **Valider ce PRD ?** → On attaque Sprint 0 directement.
