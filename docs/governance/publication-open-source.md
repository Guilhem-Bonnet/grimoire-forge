# Publication Open Source

## Etat actuel

Le depot cible est public.

## Checklist de publication

- Verifier la coherence du positionnement dans [README.md](../../README.md).
- Confirmer les fichiers cle: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.
- Verifier l'absence de secrets dans l'historique et dans les artefacts.
- Valider les checks qualite avant ouverture.
- Activer la visibilite publique du depot.
- Ajouter un premier lot d'issues publiques: roadmap, bug templates, ideas.

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

## Gouvernance minimale conseillee

- Definir un process clair pour les PR et les reviews.
- Tagger les issues par domaine: orchestration, docs, qualite, ux.
- Publier un changelog de release lisible.
- Maintenir un backlog priorise sur l'objectif moteur.
