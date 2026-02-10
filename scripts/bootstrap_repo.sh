#!/usr/bin/env bash
set -euo pipefail

# Copy backbone files into an existing repo directory.
# Usage: ./scripts/bootstrap_repo.sh /path/to/repo

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 /path/to/repo"
  exit 2
fi

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET/.claude/agents"
mkdir -p "$TARGET/SKILLS"

# Copy minimal backbone (adjust to taste)
cp -f "$SRC_DIR/AGENTS.md" "$TARGET/AGENTS.md"
cp -f "$SRC_DIR/SKILLS.md" "$TARGET/SKILLS.md" || true
cp -rf "$SRC_DIR/SKILLS/" "$TARGET/" || true
cp -rf "$SRC_DIR/.claude/agents/" "$TARGET/.claude/agents/" || true

# Optional: CI templates
if [[ ! -f "$TARGET/.gitlab-ci.yml" && -f "$SRC_DIR/.gitlab-ci.yml" ]]; then
  cp -f "$SRC_DIR/.gitlab-ci.yml" "$TARGET/.gitlab-ci.yml"
fi
if [[ ! -d "$TARGET/.github" && -d "$SRC_DIR/.github" ]]; then
  cp -rf "$SRC_DIR/.github" "$TARGET/.github"
fi

echo "Bootstrapped repo: $TARGET"
echo "Next: wire DoD gates to your stack (npm/pip) and run scripts/dod.sh"
