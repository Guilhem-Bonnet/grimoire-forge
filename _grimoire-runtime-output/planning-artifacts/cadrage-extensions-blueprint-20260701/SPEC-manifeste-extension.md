---
description: Contrat extension.json, du CLI H1 au marketplace H3 et aux node packs H4
author: Guilhem (via Grimoire Forge)
date: 2026-07-01
---

# Spécification — Manifeste d'extension

Chaque extension déclare un fichier `extension.json` à sa racine, validé par
[schemas/extension.schema.json](schemas/extension.schema.json). Exemple réel :
[exemples/crewai.extension.json](exemples/crewai.extension.json).

## Rôle du manifeste par horizon

| Horizon | Usage |
| --- | --- |
| H1 | `grimoire ext add` lit `install`, la page extensions lit `id`, `name`, `description`, `patterns` |
| H2 | Le wizard filtre par `patterns` et `permissions` |
| H3 | La CI du registry valide le schéma, les permissions et le mode shadow des hooks |
| H4 | `provides.nodes` expose des node packs au blueprint |

## Champs

### Identité et provenance

| Champ | Obligation | Rôle |
| --- | --- | --- |
| `manifestVersion` | required | Version du schéma de manifeste (entier, `1` aujourd'hui) |
| `id` | required | Slug unique kebab-case, clé dans le registry |
| `name` | required | Nom affiché |
| `version` | required | Semver de l'extension |
| `description` | required | Une phrase, affichée sur la page extensions |
| `license` | required | Identifiant SPDX |
| `authors` | required | Liste de contributeurs |
| `upstream` | optional | Projet amont encapsulé : `repository`, `kind` (`framework`, `observability`, `memory`, `tooling`), `pinnedVersion` |

### Compatibilité

| Champ | Obligation | Rôle |
| --- | --- | --- |
| `compat.kit` | required | Contrainte semver sur la version de grimoire-kit |
| `compat.manifest` | required | Version de schéma de manifeste supportée |

### Contributions (`provides`)

Chaque entrée pointe vers des fichiers relatifs à la racine de l'extension,
copiés vers les surfaces gouvernées du projet cible à l'installation.

| Champ | Cible dans le projet | Note |
| --- | --- | --- |
| `provides.agents` | `.github/agents/` | Frontmatter validé à l'installation |
| `provides.skills` | `.github/skills/` | Passent par `grimoire-skill-analyzer` |
| `provides.hooks` | `.github/hooks/` + registre de sécurité | Toujours enregistrés en mode `shadow` |
| `provides.workflows` | `.github/prompts/` | — |
| `provides.instructions` | `.github/instructions/` | — |
| `provides.nodes` | Blueprint (H4) | Déclaré dès la v1, liste vide acceptée |

Un node déclare : `id`, `label`, `patterns` (patterns du catalogue qu'il
implémente), `pins` (entrées/sorties avec contrat associé), `compilesTo`
(artefacts générés quand le node est utilisé dans un blueprint).

### Ancrage normatif (`patterns`)

| Champ | Obligation | Rôle |
| --- | --- | --- |
| `patterns.implements` | required | IDs de patterns du catalogue que l'extension matérialise (ex. `ORC-01`, `ORC-03`) |
| `patterns.requires` | optional | Patterns qui doivent déjà être en place dans le projet cible |

C'est le champ qui distingue ce marketplace d'un annuaire générique : la CI H3
rejette un manifeste sans mapping, et le viewer affiche chaque extension sur la
carte des patterns.

### Permissions (`permissions`)

Modèle déclaratif inspiré des extensions VS Code. La CI H3 vérifie la
cohérence entre permissions déclarées et contenu réel.

| Champ | Valeurs | Rôle |
| --- | --- | --- |
| `permissions.filesystem` | `none`, `artifacts`, `workspace` | Surfaces d'écriture à l'installation et à l'exécution |
| `permissions.network` | booléen | Accès réseau des scripts d'installation |
| `permissions.hooks` | Liste d'événements (`PreToolUse`, `PostToolUse`...) | Événements interceptés |
| `permissions.memory` | `none`, `read`, `readwrite` | Accès à `_grimoire-runtime/_memory/` |

### Installation

| Champ | Obligation | Rôle |
| --- | --- | --- |
| `install.steps` | required | Liste ordonnée d'étapes : `kind` (`copy`, `script`, `pip`, `npm`), champs propres au kind |
| `install.verify` | recommended | Script de vérification post-installation, exécuté par `grimoire ext verify` |
| `uninstall.steps` | recommended | Réversibilité ; à défaut, le CLI inverse les `copy` |

## Règles de validation (CI registry, H3)

1. Le manifeste valide le JSON Schema.
2. `patterns.implements` est non vide et chaque ID existe dans l'export catalogue courant.
3. Chaque hook fourni est déclaré `shadow` dans son fichier de registre.
4. Les chemins de `provides.*` existent dans l'archive et ne sortent pas de la racine de l'extension.
5. `permissions` couvre ce que font réellement les scripts (revue manuelle pour les tiers).
6. Le score `grimoire-skill-analyzer` des skills fournies atteint le seuil (75/100).

## Évolution du schéma

- Ajout de champ optionnel : incrément mineur, pas de migration.
- Changement structurel : incrément de `manifestVersion`, le CLI supporte n et n-1 pendant une fenêtre de dépréciation.
