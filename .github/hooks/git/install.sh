#!/usr/bin/env bash
# install.sh — installe les git hooks Grimoire dans .git/hooks/.
#
# Usage :
#   bash .github/hooks/git/install.sh          # install all hooks
#   bash .github/hooks/git/install.sh --check  # verify install state
#   bash .github/hooks/git/install.sh --uninstall

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$repo_root" ]]; then
  echo "error: pas dans un repo git" >&2
  exit 1
fi

src_dir="$repo_root/.github/hooks/git"
dst_dir="$repo_root/.git/hooks"

hooks=("pre-commit")

action="${1:-install}"

case "$action" in
  --check|check)
    missing=0
    for h in "${hooks[@]}"; do
      if [[ ! -x "$dst_dir/$h" ]]; then
        echo "[MISSING] $h"
        missing=1
        continue
      fi
      if ! cmp -s "$src_dir/$h" "$dst_dir/$h"; then
        echo "[DRIFT]   $h (installed differs from source)"
        missing=1
        continue
      fi
      echo "[OK]      $h"
    done
    exit $missing
    ;;
  --uninstall|uninstall)
    for h in "${hooks[@]}"; do
      if [[ -f "$dst_dir/$h" ]]; then
        rm -f "$dst_dir/$h"
        echo "[REMOVED] $h"
      fi
    done
    exit 0
    ;;
  install|--install|"")
    mkdir -p "$dst_dir"
    for h in "${hooks[@]}"; do
      cp "$src_dir/$h" "$dst_dir/$h"
      chmod +x "$dst_dir/$h"
      echo "[INSTALL] $h"
    done
    echo ""
    echo "Git hooks Grimoire installes."
    echo "Bypass d'urgence : git commit --no-verify"
    exit 0
    ;;
  *)
    echo "usage: $0 [install|--check|--uninstall]" >&2
    exit 2
    ;;
esac
