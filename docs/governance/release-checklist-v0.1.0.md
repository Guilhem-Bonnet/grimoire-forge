# Release Checklist v0.1.0

## Pre-release

- Verifier l'etat du changelog : CHANGELOG.md
- Verifier les liens docs critiques.
- Verifier les templates de contribution.

## Checks qualite

```bash
python3 -m ruff check bmad-custom-kit/framework/tools/ bmad-custom-kit/tests/ --statistics
python3 -m pytest bmad-custom-kit/tests/ -q --tb=short -x --ignore=bmad-custom-kit/tests/test_background_tasks.py
python3 bmad-custom-kit/framework/tools/preflight-check.py --project-root .
python3 bmad-custom-kit/framework/tools/memory-lint.py --project-root .
```

## Publication repository

```bash
gh repo edit Guilhem-Bonnet/grimoire-forge --visibility public --accept-visibility-change-consequences
```

## Renommage repository

Renommage deja applique vers `Guilhem-Bonnet/grimoire-forge`.

```bash
# Commande utile uniquement si vous reproduisez le runbook depuis un depot encore nomme bmad-custom.
# gh repo rename grimoire-forge --repo Guilhem-Bonnet/bmad-custom --yes
```

## Tag et release

```bash
git tag -a v0.1.0 -m "Grimoire Forge v0.1.0"
git push origin v0.1.0

gh release create v0.1.0 \
  --repo Guilhem-Bonnet/grimoire-forge \
  --title "Grimoire Forge v0.1.0" \
  --notes-file docs/governance/release-notes-v0.1.0.md
```

## Post-release

- Verifier la page release GitHub.
- Verifier les liens de docs dans la release.
- Publier l'annonce depuis docs/governance/annonce-lancement-public.md.
