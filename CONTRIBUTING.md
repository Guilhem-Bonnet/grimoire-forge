# Guide de contribution

Merci de votre intérêt pour contribuer à Grimoire Forge ! Ce document décrit le processus de contribution et les standards à respecter.

## Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
- [Workflow de développement](#workflow-de-développement)
- [Standards de qualité](#standards-de-qualité)
- [Process de revue](#process-de-revue)
- [Documentation](#documentation)

## Code de conduite

Ce projet adhère au [Code de conduite Contributor Covenant](CODE_OF_CONDUCT.md). En participant, vous êtes tenu de respecter ce code. Veuillez signaler tout comportement inacceptable via les issues GitHub.

## Comment contribuer

### Signaler un bug

Avant de créer un nouveau bug report :

1. Vérifiez que le bug n'a pas déjà été signalé dans les [issues](https://github.com/Guilhem-Bonnet/grimoire-forge/issues)
2. Utilisez le template **bug-report** disponible dans `.github/ISSUE_TEMPLATE/bug-report.md`
3. Incluez toutes les informations requises : description, étapes de reproduction, comportement attendu vs observé

### Proposer une fonctionnalité

Pour proposer une nouvelle fonctionnalité :

1. Consultez d'abord la [roadmap publique](docs/roadmap/roadmap-v1-publique.md) et le [backlog](docs/roadmap/backlog-initial.md)
2. Utilisez le template **feature-request** dans `.github/ISSUE_TEMPLATE/feature-request.md`
3. Décrivez clairement la proposition de valeur et les critères d'acceptation
4. Attendez l'approbation d'un mainteneur avant de commencer l'implémentation

### Améliorer la documentation

Les contributions à la documentation sont toujours bienvenues :

1. Utilisez le template **docs-improvement** dans `.github/ISSUE_TEMPLATE/docs-improvement.md`
2. Suivez les standards Markdown définis dans `.github/instructions/markdown-standards.instructions.md`
3. Assurez-vous que tous les liens fonctionnent et que les exemples sont exécutables

## Workflow de développement

### 1. Fork et clone

```bash
# Fork le dépôt via l'interface GitHub
git clone https://github.com/VOTRE-USERNAME/grimoire-forge.git
cd grimoire-forge
```

### 2. Créer une branche

```bash
git checkout -b feature/ma-fonctionnalite
# ou
git checkout -b fix/mon-correctif
```

Conventions de nommage des branches :

- `feature/` pour les nouvelles fonctionnalités
- `fix/` pour les corrections de bugs
- `docs/` pour les modifications de documentation
- `refactor/` pour les refactorisations
- `test/` pour l'ajout ou la modification de tests

### 3. Faire vos modifications

- Respectez les conventions de code du projet
- Ajoutez ou mettez à jour les tests si nécessaire
- Mettez à jour la documentation si applicable
- Suivez les instructions spécifiques aux types de fichiers dans `.github/instructions/`

### 4. Valider localement

Avant de pousser vos modifications, exécutez les vérifications de qualité :

```bash
# Vérification Python (si applicable)
python3 -m ruff check grimoire-kit/framework/tools/ grimoire-kit/tests/ --statistics

# Tests unitaires (si applicable)
python3 -m pytest grimoire-kit/tests/ -q --tb=short -x

# Vérifications BMAD
python3 grimoire-kit/framework/tools/preflight-check.py --project-root .
python3 grimoire-kit/framework/tools/memory-lint.py --project-root .
```

### 5. Commit

Suivez les conventions de commit :

```bash
git add .
git commit -m "type(scope): description courte

Description plus détaillée si nécessaire.

Resolves #123"
```

Types de commit :

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Modifications de documentation
- `style`: Changements de formatage (pas de changement de code)
- `refactor`: Refactorisation de code
- `test`: Ajout ou modification de tests
- `chore`: Tâches de maintenance

### 6. Push et Pull Request

```bash
git push origin feature/ma-fonctionnalite
```

Ensuite, créez une Pull Request via l'interface GitHub en utilisant le template fourni (`.github/pull_request_template.md`).

## Standards de qualité

### Code

- **Python** : Suivre les conventions dans `.github/instructions/python-conventions.instructions.md`
  - Python 3.12+
  - Type hints obligatoires
  - f-strings exclusivement
  - Longueur de ligne max : 120 caractères

- **Markdown** : Suivre `.github/instructions/markdown-standards.instructions.md`
  - CommonMark strict
  - Headers ATX uniquement (`# Title`)
  - Blocs de code fencés avec langage
  - Pas d'estimations temporelles

### Tests

- Couverture minimale : 90% pour le nouveau code
- Tests unitaires obligatoires pour les fonctionnalités critiques
- Noms de tests descriptifs : `test_<fonction>_<scénario>_<résultat_attendu>`

### Documentation

- Toute nouvelle fonctionnalité doit être documentée
- Les README doivent rester à jour
- Les exemples de code doivent être testés et fonctionnels
- Liens internes relatifs : `[voir config](../config.yaml)`

## Process de revue

### Checklist PR

Votre Pull Request doit :

- [ ] Être liée à une issue existante
- [ ] Passer tous les checks de qualité (lint, tests)
- [ ] Inclure des tests pour les nouvelles fonctionnalités
- [ ] Mettre à jour la documentation si nécessaire
- [ ] Respecter les conventions de code du projet
- [ ] Avoir une description claire suivant le template
- [ ] Ne pas contenir de secrets ou d'informations sensibles

### Timeline de revue

- **Accusé de réception** : Dans les 48 heures
- **Première revue** : Sous 7 jours pour les contributions externes
- **Itérations** : Les mainteneurs peuvent demander des modifications
- **Merge** : Une fois tous les commentaires résolus et les checks passés

### Critères de merge

1. Approbation d'au moins un mainteneur
2. Tous les checks CI/CD passent
3. Pas de conflits de merge
4. Documentation à jour
5. Respect du scope défini

## Documentation

### Structure

- `docs/vision/` : Vision produit et objectifs stratégiques
- `docs/roadmap/` : Roadmap publique et backlog
- `docs/governance/` : Processus de publication et gouvernance
- `.github/ISSUE_TEMPLATE/` : Templates d'issues
- `.github/instructions/` : Instructions spécifiques par type de fichier

### Références importantes

- [Vision produit](docs/vision/objectif-moteur-agentique.md)
- [Roadmap publique](docs/roadmap/roadmap-v1-publique.md)
- [Plan d'exécution](docs/roadmap/plan-vers-objectif.md)
- [Publication open source](docs/governance/publication-open-source.md)

## Questions ?

Si vous avez des questions :

1. Consultez d'abord la [documentation](docs/)
2. Cherchez dans les [issues existantes](https://github.com/Guilhem-Bonnet/grimoire-forge/issues)
3. Créez une nouvelle issue avec le tag `question`

## Remerciements

Merci de contribuer à Grimoire Forge ! Chaque contribution, qu'elle soit grande ou petite, aide à améliorer le projet pour toute la communauté.
