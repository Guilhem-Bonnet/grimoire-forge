# Security checklist — patterns à détecter

Référence pour [SKILL.md](SKILL.md) Step 3. Tous les patterns ci-dessous déclenchent un blocker
ou un finding majeur. Détection par regex, mais valider toujours par lecture humaine du contexte —
un faux positif vaut moins qu'un faux négatif.

## Contents

- Injection prompt
- Exfiltration & réseau
- Commandes destructives
- Secrets & credentials
- Risques spécifiques aux hooks

## 1. Injection prompt (`BL-INJECTION`)

Une skill ne doit pas tenter de manipuler le system prompt ou les autres skills. Patterns interdits :

```text
ignore (the )?(previous|above|prior) (instructions?|prompt|system)
disregard (all )?(previous|prior) (instructions?|context)
you are now (a |an )?
forget (everything|all|the system)
new (system )?prompt
override (the )?system
act as (root|admin|developer mode|jailbreak)
DAN mode
```

Aussi suspect : injection indirecte via templating non sanitisé (`{{user_input}}` réinjecté dans un
prompt système sans escape).

**Action** : blocker `BL-INJECTION`, citer la ligne exacte.

## 2. Exfiltration & réseau (`BL-NETWORK-EXFIL`)

Détecter tout appel réseau non déclaré :

```text
curl\s+(-X\s+POST\s+)?https?://
wget\s+https?://
nc\s+-[a-z]*\s
fetch\(["']https?://
requests\.(get|post|put|delete)\(
urllib\.request\.(urlopen|Request)
http\.client\.HTTPSConnection
```

Whitelist par défaut (autorisée si déclarée explicitement) :
- `github.com`, `raw.githubusercontent.com` (lectures publiques)
- `pypi.org`, `npmjs.com` (install de paquets)
- `localhost`, `127.0.0.1` (dev local)

Tout autre domaine non listé dans la skill = finding majeur. Exfiltration vers domaine inconnu
ou IP raw = blocker.

## 3. Commandes destructives (`BL-DESTRUCTIVE-UNGUARDED`)

```text
rm\s+-[rR]f?\s+(/|~|\$HOME|\*)
rm\s+-[rR]f?\s+--no-preserve-root
git\s+(push\s+--force|reset\s+--hard|clean\s+-fdx)
git\s+commit\s+--no-verify
DROP\s+(TABLE|DATABASE|SCHEMA)
TRUNCATE\s+TABLE
sudo\s+(dd|mkfs|fdisk|parted)
chmod\s+-R\s+777
> /dev/sd[a-z]
```

Acceptable si :
- Précédé d'une confirmation utilisateur explicite documentée.
- Exécuté en dry-run par défaut avec flag `--apply` séparé.
- Limité à un sous-arbre listé (jamais `/`, `~`, `$HOME`).

## 4. Secrets & credentials (`BL-SECRET`)

```text
(?i)(api[_-]?key|token|secret|password|passwd)\s*[:=]\s*["'][A-Za-z0-9_\-]{12,}["']
gh[pousr]_[A-Za-z0-9]{36,}            # GitHub tokens
sk-[A-Za-z0-9]{20,}                    # OpenAI / Anthropic
xox[abp]-[A-Za-z0-9-]{10,}             # Slack
AKIA[0-9A-Z]{16}                       # AWS access key
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}   # JWT
```

Strings >40 chars en base64/hex pur dans un assignement = warn manuel.

Toujours préférer : variable d'environnement, fichier `.env` non commité, gestionnaire de
secrets (vault, keychain). Documenter le canal dans la skill.

## 5. Risques spécifiques aux hooks

### Eval / exec sur input user-controlled (`BL-HOOK-EVAL`)

```text
eval\s+["']?\$\{?(input|stdin|payload|prompt|user)
exec\s+["']?\$\{?(input|stdin|payload|prompt|user)
bash\s+-c\s+["']\$\{?(input|stdin|payload)
sh\s+-c\s+["']\$\{?(input|stdin|payload)
python(3)?\s+-c\s+["']?\$\{?(input|stdin|payload)
```

Le stdin d'un hook est attaquant-controlled (peut être injecté via prompt user). Toute évaluation
non sanitisée = blocker.

### Bypass du gateway (`BL-HOOK-NO-GATEWAY`)

Le `command` du hook JSON doit pointer vers `grimoire-hook-gateway.sh`, pas directement vers le
script. Le gateway gère le registre de promotion `shadow`/`canary`/`enforced`. Bypass = blocker.

```json
// Bon
{"command": ".github/hooks/scripts/grimoire-hook-gateway.sh --hook-id <id> --event <ev> ..."}

// Mauvais
{"command": ".github/hooks/scripts/grimoire-mon-hook.sh"}
```

### Absence dans le registre (`BL-HOOK-NOT-REGISTERED`)

Vérifier `_grimoire-runtime/_config/hook-safety-registry.json` :

```json
{
  "hooks": {
    "<hook-id>": {
      "mode": "shadow|canary|enforced",
      "script": ".github/hooks/scripts/<script>.sh",
      "owner": "...",
      "promoted_at": "..."
    }
  }
}
```

Hook non listé = blocker. Hook nouveau passé directement à `enforced` sans `shadow` = warn.

### Timeout manquant (`BL-HOOK-NO-TIMEOUT`)

Tout hook doit déclarer un `timeout` (en secondes). Pas de timeout = risque de blocage du runtime
agent. Recommandé : ≤5s pour PreToolUse/UserPromptSubmit, ≤30s pour PostToolUse.

### Fail-closed accidentel

Un hook qui crash sans gestion d'erreur va bloquer toute interaction agent. Préférer fail-open par
défaut (`exit 0` + `echo "{}"`), sauf gardes explicites de sécurité où fail-closed est voulu et
documenté.

## 6. Patterns suspects supplémentaires (warn, pas blocker)

- `chmod +x` sur des fichiers téléchargés.
- `curl ... | bash` ou `wget -O- | sh` (pipe-to-shell).
- Setuid binaries.
- Modification de `~/.bashrc`, `~/.zshrc`, PATH global.
- Append silencieux à des fichiers de config sensibles.

Reporter en `findings` severity `major` avec un fix proposé.
