#!/usr/bin/env bash
set -euo pipefail

# Manage extensions per VS Code profile.
# Requires profiles to exist: Dev, Cyber, Infra
# Actions:
#   ./scripts/vscode_profiles.sh purge   (uninstall ALL extensions from those profiles)
#   ./scripts/vscode_profiles.sh install (install curated sets)

ACTION="${1:-}"
if [[ -z "$ACTION" ]]; then
  echo "Usage: $0 {purge|install}"
  exit 2
fi

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing: $1"; exit 1; }; }
need code

# Curated extension sets (edit to taste)
DEV_EXT=(
  "GitHub.copilot"
  "GitHub.copilot-chat"
  "GitHub.vscode-pull-request-github"
  "dbaeumer.vscode-eslint"
  "esbenp.prettier-vscode"
  "ms-python.python"
  "ms-python.vscode-pylance"
  "ms-azuretools.vscode-docker"
  "ms-vscode-remote.remote-ssh"
  "ms-vscode-remote.remote-containers"
  "redhat.vscode-yaml"
  "yzhang.markdown-all-in-one"
)

CYBER_EXT=(
  "${DEV_EXT[@]}"
  # Add only if you truly use them:
  # "ms-kubernetes-tools.vscode-kubernetes-tools"
)

INFRA_EXT=(
  "ms-azuretools.vscode-docker"
  "ms-vscode-remote.remote-ssh"
  "redhat.vscode-yaml"
  "yzhang.markdown-all-in-one"
  # Optional:
  # "hashicorp.terraform"
)

purge_profile() {
  local profile="$1"
  echo "Purging extensions from profile: $profile"
  # list may fail if profile doesn't exist
  if ! code --list-extensions --profile "$profile" >/dev/null 2>&1; then
    echo "Profile not found: $profile (create once via UI: Profiles: Create Profile)"
    return 0
  fi
  code --list-extensions --profile "$profile" | while read -r ext; do
    [[ -z "$ext" ]] && continue
    code --profile "$profile" --uninstall-extension "$ext" || true
  done
}

install_profile() {
  local profile="$1"; shift
  local exts=("$@")
  echo "Installing extensions into profile: $profile"
  if ! code --list-extensions --profile "$profile" >/dev/null 2>&1; then
    echo "Profile not found: $profile (create once via UI: Profiles: Create Profile)"
    return 0
  fi
  for ext in "${exts[@]}"; do
    [[ "$ext" =~ ^# ]] && continue
    code --profile "$profile" --install-extension "$ext"
  done
}

case "$ACTION" in
  purge)
    purge_profile "Dev"
    purge_profile "Cyber"
    purge_profile "Infra"
    ;;
  install)
    install_profile "Dev" "${DEV_EXT[@]}"
    install_profile "Cyber" "${CYBER_EXT[@]}"
    install_profile "Infra" "${INFRA_EXT[@]}"
    ;;
  *)
    echo "Unknown action: $ACTION"
    exit 2
    ;;
esac
