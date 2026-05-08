---
title: Continue — Configuration Partagée Projet
---

# Configuration Continue — Guide Équipe

## Fichiers de référence

- **Config partagée repo**: `.github/continue-config.yaml` — source de vérité du projet
- **Config utilisateur**: `~/.continue/config.yaml` — ta config locale Continue
- **Guide complet**: `docs/exploitation/continue-setup-guide.md` — dépannage, avancé

## Installation (pour toute l'équipe)

```bash
# 1. Cloner le repo ou mettre à jour
git pull origin main

# 2. Copier la config partagée
cp .github/continue-config.yaml ~/.continue/config.yaml

# 3. Redémarrer Continue dans VS Code
# Ctrl+Maj+P → "Continue: Restart Continue"
```

## Points clés

✅ **Modèles supportés**:
- grimoire-coder (par défaut, optimisé pour le projet)
- qwen3-coder:30b (brut, pour override)
- qwen3-coder-next:79B (gros modèle)
- ollama-remote (serveur 192.168.2.81:11434)

✅ **Rôles activés sur tous les modèles**:
- chat: conversation, clarification
- edit: modification de code
- apply: application de changements
- autocomplete: complétion clavier

✅ **Agents Grimoire intégrés**:
- grimoire-master: orchestrateur unique (visible)
- Sub-agents: analyst, architect, dev, qa, tech-writer, etc. (invisibles, dispatch auto)

## Usage quotidien

```
# Lancer Continue
Ctrl+L (ou Cmd+L)

# Basculer de modèle (session)
/set-model dev qwen3-coder:30b

# Générer un test
/test

# Review code
Ctrl+Maj+L → "Review"

# Utiliser les agents Grimoire
/grimoire-help
```

## Troubleshooting rapide

| Problème | Commande |
|---|---|
| Continue ne démarre pas | `Ctrl+Maj+P` → "Continue: Restart Continue" |
| Modèles non détectés | `curl http://localhost:11434/api/tags` |
| Ollama offline | `systemctl status ollama` → `systemctl start ollama` |
| Modèle lent | `/set-model all auto` ou passer à grimoire-coder |

## Pour les mainteneurs

Si tu dois mettre à jour la config:

1. Édite `.github/continue-config.yaml`
2. Valide le YAML: `yamllint .github/continue-config.yaml`
3. Committe + push
4. Notifie l'équipe: `cp .github/continue-config.yaml ~/.continue/config.yaml`

---

**Question?** Voir `docs/exploitation/continue-setup-guide.md` pour plus de détails.
