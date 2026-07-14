# Setup Guide

ScienceClaw is the local container appliance behind the OASIS Scientific
Discussion Panel. It builds and runs an OpenClaw-based scientific discussion
workspace on your laptop in Docker.

It persists OpenClaw state in `~/.openclaw`, exposes that state inside the
container at `/data/.openclaw`, mounts a narrow `./workspace` into
`/data/workspace` and `/workspace`, mounts `./data` for runtime outputs, and
mounts `./external_storage` for larger local or externally managed data.

The image also bootstraps local defaults before each command runs: local Gateway
mode, Docker-friendly Gateway bind settings, token auth, Control UI origins for
local browser use, a default model route, the `/data` runtime layout, and starter
panel workspace files from `docker/seed-workspace`.

The default workspace is a Scientific Panel Digital Twin scaffold. It includes
14 functional scientific roles, shared memory files, structured discussion
events, a tag ontology, evidence ledgers, disagreement maps, bounded experiment
records, decision records, action items, collaboration norms, dashboard-ready
metadata, and human approval rules.

The appliance is intended to be reproducible from the repository: build the
image, provide local `.env` settings and optional local secrets, and the
container seeds the discussion-panel setup automatically.

## Quick Start

```bash
cp .env.example .env
docker compose build
docker compose up -d
docker compose ps
make panel-status
```

Open:

- OpenClaw Control UI: `http://127.0.0.1:18789/`
- Workspace CMS: `http://127.0.0.1:8090/`
- JupyterLab: `http://127.0.0.1:8888/lab?token=scienceclaw`

If OpenClaw opens a login URL from inside Docker, copy it into your laptop
browser. If the CLI asks for a callback URL, paste the full browser redirect URL
back into the terminal.

For Slack-connected Gateway operation, use the operations runbook:

```bash
scripts/start-gateway.sh
docker exec <container-id> openclaw channels status --channel slack --probe --timeout 20000
docker exec -it <container-id> openclaw models auth login --provider openai-codex --set-default
docker exec <container-id> openclaw agent --session-id slack-ready-check --message 'Reply with exactly: PI Liaison ready' --timeout 120
```

If Slack returns an access pairing code, approve the specific user:

```bash
docker exec -it <container-id> openclaw pairing approve slack <PAIRING_CODE>
```

Generated discussion records, heartbeat notes, memory files, and working drafts
should be written under `/workspace` inside the container. They appear on the
host under `./workspace`.

To inspect or edit files through the browser workspace UI, open JupyterLab at
`http://127.0.0.1:8888/lab?token=scienceclaw`, or use the `WORKSPACE_UI_TOKEN`
value from `.env` if you changed it.

## Auth Options

ChatGPT/Codex OAuth can be convenient when your OpenClaw version, account entitlement, quota, and provider policy support it. It is not guaranteed and may require periodic re-login.

OpenAI API-key mode uses `OPENAI_API_KEY` from `.env` and bills through your OpenAI API account. It is optional for OAuth mode, but it is usually more predictable for automation.

AI-VERDE and other OpenAI-compatible providers can be configured through
`VERDE_LLM_BASE_URL`, `VERDE_LLM_API_KEY_FILE`, `VERDE_LLM_DEFAULT_MODEL`, and
the role-level routing files in the workspace.

GitHub push/pull from inside the container needs a local token file or injected
environment token. Organization secrets in GitHub are for Actions runners; they
do not appear automatically in local Docker Compose runs.

## Safety

Keep `./workspace` small and task-specific. Do not mount your whole home directory, browser profile, SSH keys, password manager exports, or other sensitive folders.

Read the full root-level `README.md` in the repository for troubleshooting details and verified OpenClaw documentation links.
