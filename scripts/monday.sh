#!/usr/bin/env bash
set -euo pipefail

# Monday Overhaul Runner (safe by default)
# Usage:
#   ./scripts/monday.sh status
#   ./scripts/monday.sh vscode-purge   (requires CONFIRM=YES)
#   ./scripts/monday.sh vscode-install
#   ./scripts/monday.sh repo-bootstrap /path/to/repo
#
# Notes:
# - VS Code profile creation is easiest once via UI (Profiles: Create Profile).
#   This script assumes profiles exist: Dev, Cyber, Infra.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== Dev Backbone Monday Runner =="
echo "Repo: $ROOT_DIR"
echo

cmd="${1:-status}"
shift || true

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1"; exit 1; }
}

case "$cmd" in
  status)
    echo "[1] VS Code CLI: $(command -v code || echo 'NOT FOUND')"
    echo "[2] Git:       $(command -v git || echo 'NOT FOUND')"
    echo "[3] Docker:    $(command -v docker || echo 'NOT FOUND')"
    echo
    echo "Profiles expected: Dev, Cyber, Infra"
    echo "Try: code --list-extensions --profile Dev"
    ;;

  vscode-purge)
    need_cmd code
    if [[ "${CONFIRM:-NO}" != "YES" ]]; then
      echo "Refusing to uninstall extensions without CONFIRM=YES"
      echo "Run: CONFIRM=YES ./scripts/monday.sh vscode-purge"
      exit 2
    fi
    bash "$ROOT_DIR/scripts/vscode_profiles.sh" purge
    ;;

  vscode-install)
    need_cmd code
    bash "$ROOT_DIR/scripts/vscode_profiles.sh" install
    ;;

  repo-bootstrap)
    repo_path="${1:-}"
    if [[ -z "$repo_path" ]]; then
      echo "Usage: ./scripts/monday.sh repo-bootstrap /path/to/repo"
      exit 2
    fi
    bash "$ROOT_DIR/scripts/bootstrap_repo.sh" "$repo_path"
    ;;

  *)
    echo "Unknown command: $cmd"
    exit 2
    ;;
esac
