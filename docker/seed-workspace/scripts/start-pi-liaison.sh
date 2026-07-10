#!/usr/bin/env bash
set -Eeuo pipefail

workspace="${OPENCLAW_WORKSPACE:-${WORKSPACE_DIR:-/workspace}}"

echo "start-pi-liaison.sh is a deprecated compatibility alias."
echo "Starting the Scientific Discussion Panel Interaction Agent instead."

if [ -x "${workspace}/scripts/start-interaction-agent.sh" ]; then
  exec "${workspace}/scripts/start-interaction-agent.sh" "$@"
fi

exec /opt/openclaw/seed-workspace/scripts/start-interaction-agent.sh "$@"
