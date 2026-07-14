#!/usr/bin/env bash
set -Eeuo pipefail

json="$(docker compose exec -T openclaw-local openclaw cron list --all --json)"
ids="$(
  printf '%s' "${json}" | python3 -c '
import json
import sys

data = json.load(sys.stdin)
for job in data.get("jobs", []):
    if job.get("enabled") is not False:
        print(job.get("id", ""))
'
)"

if [ -z "${ids}" ]; then
  echo "No enabled OpenClaw cron jobs."
  exit 0
fi

while IFS= read -r job_id; do
  [ -n "${job_id}" ] || continue
  docker compose exec -T openclaw-local openclaw cron disable "${job_id}" >/dev/null
  echo "Disabled OpenClaw cron job: ${job_id}"
done <<<"${ids}"

docker compose exec -T openclaw-local openclaw cron list --all
