#!/usr/bin/env bash
set -Eeuo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
env_file="${SECRETS_ENV_FILE:-${repo_root}/.env}"
mode="${SCIENCECLAW_SECRET_MODE:-local}"

load_env_file() {
  local file="$1"
  local line key value
  [ -f "${file}" ] || return 0
  while IFS= read -r line || [ -n "${line}" ]; do
    line="${line%$'\r'}"
    case "${line}" in ""|\#*) continue ;; esac
    line="${line#export }"
    case "${line}" in *=*) ;; *) continue ;; esac
    key="${line%%=*}"
    value="${line#*=}"
    [[ "${key}" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue
    if [[ "${value}" == \"*\" && "${value}" == *\" ]]; then
      value="${value:1:${#value}-2}"
    elif [[ "${value}" == \'*\' && "${value}" == *\' ]]; then
      value="${value:1:${#value}-2}"
    fi
    export "${key}=${value}"
  done < "${file}"
}

has_value() {
  local name="$1"
  local value="${!name:-}"
  [ -n "${value}" ]
}

has_file_value() {
  local name="$1"
  local file="${!name:-}"
  [ -n "${file}" ] && [ -s "${file}" ]
}

report() {
  local name="$1"
  local requirement="$2"
  local configured="$3"
  printf '%-38s %-12s %s\n' "${name}" "${requirement}" "${configured}"
}

load_env_file "${env_file}"

status=0

echo "ScienceClaw secret configuration check"
echo "Mode: ${mode}"
echo "Values are never printed."
printf '%-38s %-12s %s\n' "Name" "Requirement" "State"
printf '%-38s %-12s %s\n' "----" "-----------" "-----"

check_required() {
  local name="$1"
  local required="$2"
  local configured="missing"
  if has_value "${name}"; then
    configured="configured"
  fi
  report "${name}" "${required}" "${configured}"
  if [ "${required}" = "required" ] && [ "${configured}" = "missing" ]; then
    status=1
  fi
}

check_pair() {
  local env_name="$1"
  local file_name="$2"
  local required="$3"
  local configured="missing"
  if has_value "${env_name}" || has_file_value "${file_name}"; then
    configured="configured"
  fi
  report "${env_name} or ${file_name}" "${required}" "${configured}"
  if [ "${required}" = "required" ] && [ "${configured}" = "missing" ]; then
    status=1
  fi
}

verde_required="optional"
if [ "${mode}" = "verde" ] || [ -n "${VERDE_LLM_BASE_URL:-}" ] || [ -n "${VERDE_LLM_DEFAULT_MODEL:-}" ]; then
  verde_required="required"
fi

slack_required="optional"
if [ "${SCIENCECLAW_ENABLE_SLACK:-0}" = "1" ] || [ "${mode}" = "slack" ]; then
  slack_required="required"
fi

github_required="optional"
if [ "${SCIENCECLAW_CONFIGURE_GITHUB:-0}" = "1" ] || [ "${mode}" = "github" ]; then
  github_required="required"
fi

check_required "VERDE_LLM_BASE_URL" "${verde_required}"
check_pair "VERDE_LLM_API_KEY" "VERDE_LLM_API_KEY_FILE" "${verde_required}"
check_required "VERDE_LLM_DEFAULT_MODEL" "optional"
check_required "VERDE_LLM_PROVIDER_NAME" "optional"
check_required "OPENCLAW_MODEL" "optional"
check_required "OPENCLAW_DEFAULT_MODEL" "optional"
check_pair "GITHUB_TOKEN" "GITHUB_TOKEN_FILE" "${github_required}"
check_required "SLACK_BOT_TOKEN" "${slack_required}"
check_required "SLACK_APP_TOKEN" "${slack_required}"
check_required "SLACK_DEFAULT_CHANNEL" "${slack_required}"
check_required "DOCKERHUB_USERNAME" "optional"
check_required "DOCKERHUB_TOKEN" "optional"
check_required "DOCKERHUB_IMAGE" "optional"

if git -C "${repo_root}" ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "ERROR: .env is tracked by git."
  status=1
else
  echo ".env tracking: not tracked"
fi

if [ "${status}" -eq 0 ]; then
  echo "Secret configuration check passed."
else
  echo "Secret configuration check found missing required configuration." >&2
fi

exit "${status}"
