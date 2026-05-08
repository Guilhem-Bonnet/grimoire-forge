# HOOK_TEMPLATE.md — Template de génération hook

Template pour [SKILL.md](SKILL.md) Step 3 quand `artifact_kind = hook`. Deux fichiers à générer
en parallèle : le JSON de configuration et le script bash. Tous les hooks passent par le gateway
de promotion.

## Contents

- Fichier JSON
- Script bash
- Entrée registre
- Règles de sécurité non négociables

## 1. Fichier JSON

Path : `.github/hooks/{{hook-id}}.json`

```json
{
  "hooks": {
    "{{Event}}": [
      {
        "type": "command",
        "command": ".github/hooks/scripts/grimoire-hook-gateway.sh --hook-id {{hook-id}} --event {{Event}} --control-file .github/hooks/{{hook-id}}.json",
        "timeout": {{timeout_seconds}}
      }
    ]
  }
}
```

Contraintes :

| Champ | Règle |
|---|---|
| `Event` | Parmi `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, `Stop` |
| `command` | DOIT pointer vers `grimoire-hook-gateway.sh` ; bypass = blocker |
| `timeout` | ≤5 pour Pre*, ≤30 pour Post*, jamais omis |

## 2. Script bash

Path : `.github/hooks/scripts/{{slug}}.sh`

```bash
#!/usr/bin/env bash
# {{slug}}.sh — {{Event}} hook
# {{One-line description: que valide/produit ce hook}}
#
# Contrat I/O :
#   stdin  : payload JSON du hook (event-specific)
#   stdout : JSON de réponse (continue / block / additionalContext)
#   stderr : logs (ignorés par le runtime)
#
# Fail-open par défaut : toute erreur non gérée → echo "{}"; exit 0

set -euo pipefail

project_root="$(cd "$(dirname "$0")/../../.." && pwd)"
input=$(cat)

# 1. Garde fail-open : capter toute erreur et émettre du JSON neutre
trap 'echo "{}"; exit 0' ERR

# 2. Validation minimale du stdin (JSON parseable)
if ! echo "$input" | python3 -c 'import json,sys; json.loads(sys.stdin.read())' 2>/dev/null; then
  echo "{}"
  exit 0
fi

# 3. {{Logique métier — JAMAIS d'eval/exec sur $input}}
#    Préférer : extraction de champs via jq ou python -c "..." statique.
#    Bannir : eval "$input", bash -c "$input", python -c "$input".
#
# Exemple (extraction sûre via jq) :
#   tool_name=$(echo "$input" | jq -r '.tool.name // empty')
#   if [[ "$tool_name" == "dangerous_tool" ]]; then
#     echo '{"decision":"block","reason":"Tool not allowed in this context"}'
#     exit 0
#   fi

# 4. Émission de la décision
echo "{}"
exit 0
```

Permissions : `chmod +x` à la création.

## 3. Entrée registre

Mettre à jour `_grimoire-runtime/_config/hook-safety-registry.json` :

```json
{
  "hooks": {
    "{{hook-id}}": {
      "mode": "shadow",
      "script": ".github/hooks/scripts/{{slug}}.sh",
      "config": ".github/hooks/{{hook-id}}.json",
      "owner": "{{user}}",
      "created": "{{iso_date}}",
      "promoted_at": null,
      "description": "{{one-line description}}"
    }
  }
}
```

**Règle absolue** : mode initial = `shadow`. Promotion vers `canary` puis `enforced` via la task
`grimoire: hooks-promote` après observation ≥ 3 sessions sans incident.

## 4. Règles de sécurité non négociables

| ID | Règle | Conséquence si violée |
|---|---|---|
| H-S1 | Pas de `eval`, `exec`, `bash -c`, `sh -c`, `python -c` sur stdin user-controlled | blocker `BL-HOOK-EVAL` |
| H-S2 | Le `command` du JSON DOIT être `grimoire-hook-gateway.sh` | blocker `BL-HOOK-NO-GATEWAY` |
| H-S3 | Hook DOIT être listé dans `hook-safety-registry.json` | blocker `BL-HOOK-NOT-REGISTERED` |
| H-S4 | `timeout` déclaré explicitement | blocker `BL-HOOK-NO-TIMEOUT` |
| H-S5 | `event` parmi la liste autorisée | blocker `BL-HOOK-EVENT` |
| H-S6 | Mode initial `shadow` (sauf raison documentée par owner) | warn |
| H-S7 | Pas d'appel réseau non whitelisté | blocker `BL-NETWORK-EXFIL` |
| H-S8 | Fail-open par défaut sur erreur (sauf garde sécurité explicite) | warn |
| H-S9 | Sortie JSON validée avant émission | warn |
| H-S10 | Pas de modification de fichiers hors `_grimoire-runtime-output/` | warn |

## 5. Patterns autorisés pour parser le stdin

```bash
# Avec jq (préféré si dispo)
field=$(echo "$input" | jq -r '.path.to.field // ""')

# Avec python (statique, pas eval)
field=$(echo "$input" | python3 -c '
import json, sys
data = json.loads(sys.stdin.read())
print(data.get("path", {}).get("to", {}).get("field", ""))
')

# Délégation à un script python dédié sous grimoire-kit/framework/tools/
echo "$input" | "$python_bin" "$project_root/grimoire-kit/framework/tools/{{slug}}-policy.py"
```

## 6. Checklist génération hook

- [ ] JSON conforme au schéma (`hooks.{Event}[].command`, `timeout`).
- [ ] `command` pointe vers le gateway.
- [ ] Script `chmod +x`, shebang `#!/usr/bin/env bash`, `set -euo pipefail`.
- [ ] Fail-open trap installé.
- [ ] Aucun pattern `BL-HOOK-EVAL` détecté par grep.
- [ ] Aucun appel réseau hors whitelist.
- [ ] Entrée registre avec `mode: shadow`.
- [ ] Self-test : payload nominal, payload vide, payload malformé.
- [ ] Analyzer en `mode: hook` retourne verdict `pass`.
