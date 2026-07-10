#!/usr/bin/env bash
set -Eeuo pipefail

workspace="${OPENCLAW_WORKSPACE:-${WORKSPACE_DIR:-/workspace}}"
command="${1:-status}"

case "${command}" in
  status|pause|resume|summary|budget-check)
    scienceclaw-panel-control "${command}" --workspace "${workspace}"
    ;;
  queue-question)
    shift
    scienceclaw-panel-control queue-question --workspace "${workspace}" --question "$*"
    ;;
  *)
    echo "Usage: panel-control.sh status|pause|resume|summary|budget-check|queue-question TEXT" >&2
    exit 2
    ;;
esac
