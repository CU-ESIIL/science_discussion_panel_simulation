#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "scripts/test-working-group.sh is a deprecated alias; running scripts/test-panel.sh."
exec "${repo_root}/scripts/test-panel.sh" "$@"
