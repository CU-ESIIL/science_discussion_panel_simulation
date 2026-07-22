.PHONY: help build up start down open-ui cron-off shell init-panel init-working-group panel-status panel-pause panel-resume panel-round panel-summary panel-queue publish-discussions doctor checkpoint demo demo-environmental smoke-test test-panel test-working-group test-layout check-secrets test-secrets workspace-smoke-test github-smoke-test

help:
	@echo "OASIS Scientific Discussion Panel commands"
	@echo
	@echo "  make build               Build the local container image"
	@echo "  make up                  Start the local compose stack in the background"
	@echo "  make start               Start the stack and open the Control UI"
	@echo "  make down                Stop the local compose stack"
	@echo "  make open-ui             Open the local Control UI with the configured token"
	@echo "  make cron-off            Disable all local OpenClaw cron jobs"
	@echo "  make shell               Open a shell in the OpenClaw container"
	@echo "  make init-panel          Initialize the local scientific discussion panel scaffold"
	@echo "  make panel-status        Show panel loop state and queued questions"
	@echo "  make panel-pause         Pause autonomous panel rounds"
	@echo "  make panel-resume        Resume panel rounds when autorun is enabled"
	@echo "  make panel-round         Run one deterministic local panel round"
	@echo "  make panel-summary       Print the current synthesis"
	@echo "  make panel-queue QUESTION='...'  Queue a user question"
	@echo "  make publish-discussions Render workspace rounds into website Markdown"
	@echo "  make doctor              Run safe local health checks"
	@echo "  make checkpoint          Write a local workspace checkpoint"
	@echo "  make demo                Run the deterministic panel discussion demo"
	@echo "  make smoke-test          Run lightweight operational validation"
	@echo "  make workspace-smoke-test Validate the workspace file manager"
	@echo "  make github-smoke-test   Validate the GitHub repository manager"
	@echo "  make test-panel          Validate the seeded panel scaffold"
	@echo "  make test-layout         Validate the /data layout scaffold"
	@echo "  make check-secrets       Check secret configuration without printing values"

build:
	@docker compose build

up:
	@docker compose up -d

start: up open-ui

down:
	@docker compose down

open-ui:
	@scripts/open-control-ui.sh

cron-off:
	@scripts/disable-openclaw-cron.sh

shell:
	@docker compose run --rm openclaw-local bash

init-panel:
	@scripts/init_panel.sh

init-working-group:
	@scripts/init_working_group.sh

panel-status:
	@python3 scripts/panel_control.py status --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}"

panel-pause:
	@python3 scripts/panel_control.py pause --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}"

panel-resume:
	@python3 scripts/panel_control.py resume --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}"

panel-round:
	@python3 scripts/demo_panel_discussion.py --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}"

panel-summary:
	@python3 scripts/panel_control.py summary --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}"

panel-queue:
	@python3 scripts/panel_control.py queue-question --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}" --question "$${QUESTION:?Set QUESTION='...'}"

publish-discussions:
	@python3 scripts/publish_discussion_rounds.py --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}" --site docs

doctor:
	@scripts/doctor.sh

checkpoint:
	@scripts/checkpoint.sh

demo:
	@python3 scripts/demo_panel_discussion.py --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}"

demo-environmental:
	@python3 scripts/demo_environmental_workflow.py --workspace "$${SCIENCECLAW_WORKSPACE_DIR:-$${WORKSPACE_DIR:-workspace}}"

smoke-test:
	@scripts/smoke_test.sh

workspace-smoke-test:
	@scripts/smoke_test_workspace.sh

github-smoke-test:
	@scripts/smoke_test_github_manager.sh

test-panel:
	@scripts/test-panel.sh

test-working-group:
	@scripts/test-working-group.sh

test-layout:
	@scripts/test-scienceclaw-layout.sh

check-secrets:
	@scripts/check-secret-config.sh

test-secrets:
	@scripts/test-secrets.sh
