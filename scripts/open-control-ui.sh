#!/usr/bin/env bash
set -Eeuo pipefail

env_file="${SCIENCECLAW_ENV_FILE:-.env}"

read_env_value() {
  local key="$1"
  local default="${2:-}"
  local value=""
  if [ -f "${env_file}" ]; then
    value="$(
      awk -v key="${key}" '
        BEGIN { FS = "=" }
        $1 == key {
          sub(/^[^=]*=/, "")
          print
          exit
        }
      ' "${env_file}" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//"
    )"
  fi
  printf '%s' "${value:-${default}}"
}

port="$(read_env_value OPENCLAW_GATEWAY_PORT 18789)"
auth_mode="$(read_env_value OPENCLAW_GATEWAY_AUTH_MODE token)"
token="$(read_env_value OPENCLAW_GATEWAY_TOKEN '')"

url="http://127.0.0.1:${port}/"
if [ "${auth_mode}" = "token" ] && [ -n "${token}" ]; then
  url="${url}#token=${token}"
fi

echo "Opening OpenClaw Control UI on 127.0.0.1:${port}"

if [ "${SCIENCECLAW_OPEN_UI_DRY_RUN:-0}" = "1" ]; then
  exit 0
fi

case "$(uname -s 2>/dev/null || true)" in
  Darwin)
    open "${url}"
    ;;
  Linux)
    if command -v xdg-open >/dev/null 2>&1; then
      xdg-open "${url}" >/dev/null 2>&1 &
    else
      echo "No browser opener found. Open: http://127.0.0.1:${port}/#token=<OPENCLAW_GATEWAY_TOKEN>"
    fi
    ;;
  *)
    echo "Open: http://127.0.0.1:${port}/#token=<OPENCLAW_GATEWAY_TOKEN>"
    ;;
esac
