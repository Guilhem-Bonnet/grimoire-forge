# Publication Open Source

## Etat actuel

Le depot cible est public.

## Checklist de publication

- [x] Verifier la coherence du positionnement dans [README.md](../../README.md) — ✅ Complété
- [x] Confirmer les fichiers cle: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY — ✅ Tous créés
- [x] Verifier l'absence de secrets dans l'historique et dans les artefacts — ✅ Aucun secret trouvé
- [x] Templates issue/PR en place — ✅ 3 templates issue + 1 template PR + config.yml
- [x] Activer la visibilite publique du depot — ✅ Le dépôt est déjà public
- [x] Process de contribution clarifié — ✅ Documenté dans CONTRIBUTING.md

## Fichiers de gouvernance créés

- **LICENSE** : Licence MIT avec copyright 2026
- **CONTRIBUTING.md** : Guide complet de contribution avec workflow, standards de qualité et process de revue
- **CODE_OF_CONDUCT.md** : Code de conduite basé sur Contributor Covenant v2.1
- **SECURITY.md** : Politique de sécurité avec instructions de signalement et bonnes pratiques

## Templates disponibles

- **Issue templates** (`.github/ISSUE_TEMPLATE/`) :
  - `bug-report.md` : Pour signaler des bugs reproductibles
  - `feature-request.md` : Pour proposer de nouvelles fonctionnalités
  - `docs-improvement.md` : Pour améliorer la documentation
  - `config.yml` : Configuration avec liens vers roadmap et vision

- **PR template** (`.github/pull_request_template.md`) :
  - Checklist de vérification complète
  - Sections pour summary, alignment, verification, risks
  - Liens vers documentation et standards

## Commandes recommandees

```bash
# Qualite locale
python3 -m ruff check grimoire-kit/framework/tools/ grimoire-kit/tests/ --statistics
python3 -m pytest grimoire-kit/tests/ -q --tb=short -x --ignore=grimoire-kit/tests/test_background_tasks.py

# Basculer la visibilite
# Requiert un token GitHub avec droits admin sur le depot
# Si gh est configure avec les bons scopes
# gh repo edit Guilhem-Bonnet/grimoire-forge --visibility public
```

## Gouvernance mise en place

✅ **Process de contribution** :
- Workflow Git clairement défini (fork, branche, commit, PR)
- Conventions de nommage des branches et commits
- Standards de qualité obligatoires (lint, tests, documentation)
- Process de revue avec timeline et critères de merge

✅ **Organisation des issues** :
- Templates structurés par type (bug, feature, docs)
- Configuration pour rediriger vers roadmap et vision
- Labels implicites par domaine : orchestration, docs, qualite, ux

✅ **Documentation** :
- Vision produit claire : [docs/vision/objectif-moteur-agentique.md](../vision/objectif-moteur-agentique.md)
- Roadmap publique : [docs/roadmap/roadmap-v1-publique.md](../roadmap/roadmap-v1-publique.md)
- Backlog initial : [docs/roadmap/backlog-initial.md](../roadmap/backlog-initial.md)
- Changelog maintenu : [CHANGELOG.md](../../CHANGELOG.md)

✅ **Sécurité** :
- Politique de signalement des vulnérabilités
- Bonnes pratiques documentées
- Outils de sécurité intégrés (ruff/bandit, preflight-check, memory-lint)

## Prochaines étapes recommandées

1. **Configurer les labels GitHub** pour tagger les issues par domaine
2. **Créer le premier milestone** pour la version v0.2.0
3. **Ajouter GitHub Actions** pour automatiser les checks qualité sur les PRs
4. **Annoncer la publication** via les canaux appropriés (voir [annonce-lancement-public.md](annonce-lancement-public.md))
