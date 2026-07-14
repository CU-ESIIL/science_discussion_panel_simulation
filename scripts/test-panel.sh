#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
workspace="${WORKSPACE_DIR:-}"
template_root="${TEMPLATE_ROOT:-${repo_root}/docker/seed-workspace}"
init_script="${INIT_SCRIPT:-${template_root}/scripts/init-working-group.sh}"
cleanup=0

if [ -z "${workspace}" ]; then
  workspace="$(mktemp -d)"
  cleanup=1
fi

cleanup_workspace() {
  if [ "${cleanup}" -eq 1 ]; then
    rm -rf "${workspace}"
  fi
}
trap cleanup_workspace EXIT

required_dirs=(
  NORM_PROPOSALS
  DISCUSSION_ROUNDS
  POSITION_HISTORY
  LITERATURE
  LITERATURE/evidence_packets
  EXPERIMENTS
  EXPERIMENTS/proposals
  EXPERIMENTS/results
  FACT_CHECKS
  DAILY_SYNTHESIS
  panel_sources
  documents
  config
  data
  analysis
  outputs
  logs
  runtime
  scripts
)

required_files=(
  PANEL_BRIEF.md
  PANEL_CONSTITUTION.md
  PANEL_NORMS_HISTORY.md
  DISSENTS.md
  PANELIST_ROSTER.md
  TAG_ONTOLOGY.md
  STRUCTURED_MEMORY.md
  DISCUSSION_EVENT_TEMPLATE.md
  CURRENT_POSITIONS.md
  TOPIC_QUEUE.yaml
  QUESTIONS_FROM_USER.md
  DISCUSSION_INDEX.md
  DISAGREEMENT_MAP.md
  EVIDENCE_LEDGER.yaml
  CURRENT_SYNTHESIS.md
  WHAT_WOULD_CHANGE_OUR_MINDS.md
  OPEN_QUESTIONS.md
  AUDIENCE_GUIDE.md
  SYSTEM_STATUS.md
  PANEL_INTAKE.md
  AGENTS.md
  MODEL_ASSIGNMENTS.md
  config/working_group.yaml
  prompts/interaction-agent-startup.md
  prompts/pi-liaison-startup.md
  scripts/start-interaction-agent.sh
  scripts/panel-control.sh
  scripts/check-secret-config.sh
)

if [ ! -x "${init_script}" ]; then
  echo "Init script is missing or not executable: ${init_script}" >&2
  exit 1
fi

first_output="$("${init_script}" --workspace "${workspace}" --template-root "${template_root}")"
second_output="$("${init_script}" --workspace "${workspace}" --template-root "${template_root}")"

for dir in "${required_dirs[@]}"; do
  if [ ! -d "${workspace}/${dir}" ]; then
    echo "Missing required directory: ${workspace}/${dir}" >&2
    exit 1
  fi
  if [ ! -f "${workspace}/${dir}/README.md" ] && [ "${dir}" != "runtime" ]; then
    echo "Missing directory README: ${workspace}/${dir}/README.md" >&2
    exit 1
  fi
done

for file in "${required_files[@]}"; do
  if [ ! -f "${workspace}/${file}" ]; then
    echo "Missing required file: ${workspace}/${file}" >&2
    exit 1
  fi
done

for name in \
  "PI Liaison" \
  "Scientific Director" \
  "Domain Scientist" \
  "Quantitative Modeler" \
  "Data Engineer / Infrastructure Scientist" \
  "Citation and Evidence Curator" \
  "Skeptical Reviewer" \
  "Team Science Facilitator" \
  "Scientific Narrative Lead" \
  "Societal Impact Agent" \
  "Decision Recorder" \
  "Discussion Intelligence Agent" \
  "Cloud Infrastructure Engineer" \
  "Agent Operations Manager"; do
  if ! grep -q "${name}" "${workspace}/AGENTS.md"; then
    echo "Missing Scientific Panel Digital Twin role in AGENTS.md: ${name}" >&2
    exit 1
  fi
done

grep -q "Scientific Panel Digital Twin" "${workspace}/AGENTS.md" || { echo "Digital twin architecture missing." >&2; exit 1; }
grep -q "structured event" "${workspace}/DISCUSSION_EVENT_TEMPLATE.md" || { echo "Discussion event template missing." >&2; exit 1; }
grep -q "Canonical Categories" "${workspace}/TAG_ONTOLOGY.md" || { echo "Tag ontology missing." >&2; exit 1; }
grep -q "Structured memory" "${workspace}/STRUCTURED_MEMORY.md" || grep -q "Memory Type" "${workspace}/STRUCTURED_MEMORY.md" || { echo "Structured memory map missing." >&2; exit 1; }
grep -q "Scientific Panel Digital Twin" "${workspace}/PANEL_BRIEF.md" || { echo "Panel digital twin brief missing." >&2; exit 1; }
grep -q "no_impersonation: true" "${workspace}/config/working_group.yaml" || { echo "No-impersonation config missing." >&2; exit 1; }
grep -q "VERDE_LLM_API_KEY_FILE" "${workspace}/MODEL_ASSIGNMENTS.md" || { echo "AI-VERDE secret-file support missing." >&2; exit 1; }
grep -q "max_experiments_per_day" "${workspace}/config/working_group.yaml" || { echo "Experiment bound missing." >&2; exit 1; }
grep -q "citation" "${workspace}/AGENTS.md" || { echo "Citation discipline missing." >&2; exit 1; }
grep -q "Discussion Intelligence Agent" "${workspace}/config/discussion-coding-protocol.md" || { echo "Discussion Intelligence Agent coding duty missing." >&2; exit 1; }

if ! grep -q "Files created: 0" <<< "${second_output}"; then
  echo "Init script is not idempotent; second run created files." >&2
  echo "${second_output}" >&2
  exit 1
fi

python3 "${repo_root}/scripts/panel_control.py" queue-question --workspace "${workspace}" --question "What would change each panelist's mind?" >/tmp/scienceclaw-panel-queue.log
grep -q "What would change" "${workspace}/QUESTIONS_FROM_USER.md" || { echo "Question queue failed." >&2; exit 1; }

python3 "${repo_root}/scripts/panel_control.py" pause --workspace "${workspace}" >/tmp/scienceclaw-panel-pause.log
grep -q "| Panel state | paused |" "${workspace}/SYSTEM_STATUS.md" || { echo "Pause state not recorded." >&2; exit 1; }
python3 "${repo_root}/scripts/panel_control.py" resume --workspace "${workspace}" >/tmp/scienceclaw-panel-resume.log
grep -q "| Panel state | running |" "${workspace}/SYSTEM_STATUS.md" || { echo "Resume state not recorded." >&2; exit 1; }

python3 "${repo_root}/scripts/demo_panel_discussion.py" --workspace "${workspace}" >/tmp/scienceclaw-panel-demo-1.log
python3 "${repo_root}/scripts/demo_panel_discussion.py" --workspace "${workspace}" >/tmp/scienceclaw-panel-demo-2.log

for path in \
  "${workspace}/DISCUSSION_ROUNDS/round-001/summary.md" \
  "${workspace}/DISCUSSION_ROUNDS/round-002/summary.md" \
  "${workspace}/POSITION_HISTORY/round-001.md" \
  "${workspace}/POSITION_HISTORY/round-002.md" \
  "${workspace}/EXPERIMENTS/results/round-001_calibration_demo.json" \
  "${workspace}/FACT_CHECKS/round-001.md"; do
  if [ ! -s "${path}" ]; then
    echo "Missing expected demo output: ${path}" >&2
    exit 1
  fi
done

grep -q "synthetic demonstration text" "${workspace}/DISCUSSION_ROUNDS/round-001/summary.md" || { echo "Synthetic label missing." >&2; exit 1; }
grep -q "Prediction does not equal explanation" "${workspace}/CURRENT_POSITIONS.md" || { echo "Current positions not updated." >&2; exit 1; }
grep -q "claim-round-001-001" "${workspace}/EVIDENCE_LEDGER.yaml" || { echo "Structured evidence ledger missing." >&2; exit 1; }
grep -q "Last completed round | round-002" "${workspace}/SYSTEM_STATUS.md" || { echo "Panel status not updated after demo." >&2; exit 1; }

SCIENCECLAW_SECRET_MODE=verde SECRETS_ENV_FILE=/dev/null "${repo_root}/scripts/check-secret-config.sh" >/tmp/scienceclaw-panel-secret-check.log 2>&1 && {
  echo "Secret checker should fail when Verde mode lacks required config." >&2
  exit 1
}
grep -q "VERDE_LLM_API_KEY or VERDE_LLM_API_KEY_FILE" /tmp/scienceclaw-panel-secret-check.log || {
  echo "Secret checker did not report Verde credential requirement." >&2
  exit 1
}
if grep -qE 'xoxb-|xapp-|sk-' /tmp/scienceclaw-panel-secret-check.log; then
  echo "Secret checker printed token-like content." >&2
  exit 1
fi

echo "${first_output}" >/dev/null
echo "Scientific discussion panel smoke test passed: ${workspace}"
