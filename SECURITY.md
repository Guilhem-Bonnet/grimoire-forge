# Politique de sécurité

## Versions supportées

Seule la version la plus récente de Grimoire Forge est activement supportée avec des mises à jour de sécurité.

| Version | Supportée          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < main  | :x:                |

## Signaler une vulnérabilité

La sécurité de Grimoire Forge est prise très au sérieux. Si vous découvrez une vulnérabilité de sécurité, nous vous prions de bien vouloir nous en informer de manière responsable.

### Comment signaler

**NE PAS créer d'issue publique pour les vulnérabilités de sécurité.**

À la place, veuillez :

1. Créer une **Security Advisory** privée via l'onglet Security du dépôt GitHub
2. Ou envoyer un email à l'équipe de maintenance (voir les informations de contact dans les issues GitHub)

### Informations à inclure

Pour nous aider à mieux comprendre et résoudre le problème, veuillez inclure autant d'informations que possible :

- Type de vulnérabilité (par exemple : injection de code, XSS, CSRF, etc.)
- Chemins complets des fichiers source concernés
- Emplacement du code source affecté (tag/branche/commit ou URL directe)
- Configuration spéciale requise pour reproduire le problème
- Instructions étape par étape pour reproduire le problème
- Preuve de concept ou code d'exploitation (si possible)
- Impact potentiel du problème, y compris comment un attaquant pourrait l'exploiter

### Processus de réponse

1. **Accusé de réception** : Nous accuserons réception de votre rapport dans les 48 heures
2. **Évaluation** : Nous évaluerons la vulnérabilité et déterminerons sa gravité
3. **Correction** : Nous travaillerons sur un correctif et vous tiendrons informé de l'avancement
4. **Publication** : Une fois le correctif déployé, nous publierons un avis de sécurité
5. **Crédit** : Avec votre permission, nous vous créditerons pour la découverte

## Bonnes pratiques de sécurité

Lors de l'utilisation de Grimoire Forge :

- Ne jamais committer de secrets, clés API ou credentials dans le code source
- Utiliser des variables d'environnement pour les informations sensibles
- Maintenir vos dépendances à jour
- Suivre le principe du moindre privilège pour les permissions
- Valider et sanitiser toutes les entrées utilisateur
- Utiliser les outils de sécurité intégrés (ruff avec bandit)

## Outils de sécurité intégrés

Le projet utilise plusieurs outils pour maintenir un haut niveau de sécurité :

- **ruff** avec extension **bandit** pour la détection de vulnérabilités Python
- **preflight-check** pour les vérifications de sécurité avant commit
- **memory-lint** pour éviter les fuites d'informations sensibles

## Remerciements

Nous remercions tous les chercheurs en sécurité qui contribuent à garder Grimoire Forge sûr pour tous.
