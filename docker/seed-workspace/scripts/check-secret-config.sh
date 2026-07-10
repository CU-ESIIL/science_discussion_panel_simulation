#!/usr/bin/env bash
set -Eeuo pipefail

if command -v scienceclaw-check-secret-config >/dev/null 2>&1; then
  exec scienceclaw-check-secret-config "$@"
fi

if [ -x /repo/scripts/check-secret-config.sh ]; then
  exec /repo/scripts/check-secret-config.sh "$@"
fi

echo "Secret configuration check"
echo "Values are never printed."
for name in VERDE_LLM_BASE_URL VERDE_LLM_API_KEY VERDE_LLM_API_KEY_FILE VERDE_LLM_DEFAULT_MODEL OPENCLAW_MODEL OPENCLAW_DEFAULT_MODEL GITHUB_TOKEN GITHUB_TOKEN_FILE SLACK_BOT_TOKEN SLACK_APP_TOKEN SLACK_DEFAULT_CHANNEL; do
  value="${!name:-}"
  if [ -n "${value}" ]; then
    echo "${name}: configured"
  else
    echo "${name}: missing or optional"
  fi
done
