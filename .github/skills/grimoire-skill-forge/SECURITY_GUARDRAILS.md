# SECURITY_GUARDRAILS.md — Garde-fous de génération

Référence pour [SKILL.md](SKILL.md) — patterns à refuser à la génération, indépendamment du
score qualité. Complémentaire de [../grimoire-skill-analyzer/SECURITY_CHECKLIST.md](../grimoire-skill-analyzer/SECURITY_CHECKLIST.md)
côté analyse. Ici, c'est l'auteur (la forge) qui doit refuser de générer le pattern, pas
seulement le détecter après coup.

## Contents

- Refus à la génération
- Sanitisation des inputs utilisateur
- Garde-fous pour les hooks
- Incident handling

## 1. Refus à la génération

La forge **refuse explicitement** de produire les patterns suivants, même si l'utilisateur insiste.
Réponse type : "Je ne peux pas générer ce pattern car il viole {règle}. Voici l'alternative sûre : ...".

### 1.1 Injection prompt

Bannir dans le body, dans les exemples, et dans les templates de réponse de la skill :

- "ignore previous instructions"
- "you are now {role}"
- "act as {jailbreak_persona}"
- "forget the system prompt"
- "developer mode" / "DAN mode"
- Templates qui réinjectent `{{user_input}}` dans un prompt système sans escape.

### 1.2 Exécution de code attaquant-controlled

Bannir dans tout script généré :

- `eval "$input"`, `exec "$input"`, `bash -c "$input"`, `sh -c "$input"`, `python -c "$input"`
- `subprocess.run(user_input, shell=True)` côté Python
- `os.system(user_input)` côté Python
- Templates qui construisent une commande shell par concaténation de strings utilisateur

Toujours préférer : whitelist d'opérations, parsing structuré (jq, json.loads), arguments en `argv`
(pas en `shell=True`).

### 1.3 Exfiltration

Bannir dans body, scripts, et exemples :

- `curl ... | bash`, `wget -O- | sh` (pipe-to-shell)
- `curl https://<domaine_non_whitelisté>` sans déclaration explicite
- `nc -e`, reverse shells
- Lecture systématique de `~/.ssh/`, `~/.aws/`, `~/.config/gh/`

Whitelist par défaut (autorisée si déclarée) :
- `github.com`, `raw.githubusercontent.com`
- `pypi.org`, `npmjs.com`
- `localhost`, `127.0.0.1`
- Domaines explicitement listés dans le frontmatter ou la section "External sources" de la skill.

### 1.4 Destructifs nus

Bannir sans garde :

- `rm -rf /`, `rm -rf ~`, `rm -rf $HOME`, `rm -rf *`, `rm -rf .` 
- `git push --force` sans flag explicite `--apply` séparé
- `git reset --hard` sur la branche par défaut
- `chmod -R 777`
- `> /dev/sd*`, `dd if=/dev/zero of=/dev/sd*`
- `DROP TABLE` / `TRUNCATE` sans dry-run

Pour ces opérations, exiger :
- Dry-run par défaut, flag `--apply` séparé.
- Confirmation utilisateur explicite documentée dans la procédure.
- Rollback documenté.

### 1.5 Secrets

Refuser tout assignement statique de :
- Tokens (`gh*_`, `sk-`, `xox*-`, `AKIA*`, JWT pattern)
- Clés privées (`-----BEGIN PRIVATE KEY-----`)
- Mots de passe en clair
- Strings >40 chars en base64 dans un assignement nommé `*key*`, `*token*`, `*secret*`

Toujours rediriger vers : variable d'environnement, `.env` non commité, secret manager (vault,
keychain, GitHub secrets).

## 2. Sanitisation des inputs utilisateur

Si la skill prend un input depuis l'utilisateur (chat, fichier, stdin) :

| Type d'input | Sanitisation requise |
|---|---|
| Chemin de fichier | Résoudre via `pathlib.Path(...).resolve()`, vérifier qu'il est sous le project_root |
| Slug / identifiant | Regex `^[a-z][a-z0-9-]{2,63}$` |
| URL | Schéma `https://` uniquement, hôte dans la whitelist |
| Commande shell | Refuser, utiliser argv |
| JSON | `json.loads()` avec gestion d'erreur ; pas de `eval` |
| Markdown | Pas de réinjection dans un prompt système ; échapper les triple-backticks si embarqué |

## 3. Garde-fous pour les hooks

Tout hook généré doit :

1. **Passer par le gateway** : `command` = `grimoire-hook-gateway.sh ...`. Bypass = refus génération.
2. **Démarrer en `shadow`** : la promotion `canary` → `enforced` est manuelle, observée, documentée.
3. **Avoir un timeout strict** : ≤5s pour Pre*, ≤30s pour Post*.
4. **Fail-open par défaut** : `trap 'echo "{}"; exit 0' ERR`. Une garde fail-closed doit être
   explicitement justifiée et limitée à un pattern précis.
5. **Ne jamais évaluer le stdin** : parsing structuré uniquement (jq, python statique).
6. **Émettre un JSON valide** : valider avec `python -c "import json,sys; json.loads(sys.stdin.read())"`
   avant `echo` final si la sortie est non triviale.
7. **Logger en stderr, pas stdout** : stdout est réservé au protocole hook.

## 4. Incident handling

Si pendant la forge l'utilisateur pousse vers un pattern interdit :

1. **Refuser explicitement** : nommer la règle violée (`H-S1`, `BL-INJECTION`, etc.).
2. **Proposer l'alternative sûre** dans la même réponse.
3. **Ne pas négocier** : pas de "version allégée du pattern", pas de "juste pour tester".
4. **Documenter le refus** dans le draft (section temporaire `## Refus de garde`) puis supprimer
   avant persist — l'utilisateur sait qu'il a poussé là.

Si un pattern dangereux passe la gate par erreur (faux négatif) :
- Ne pas écrire l'artefact.
- Remonter le faux négatif au prochain audit de [../grimoire-skill-analyzer/SECURITY_CHECKLIST.md](../grimoire-skill-analyzer/SECURITY_CHECKLIST.md).
- Renforcer le pattern de détection.
