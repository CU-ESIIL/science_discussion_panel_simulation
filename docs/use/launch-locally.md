# Launch Locally

This page is for running the OASIS Scientific Discussion Panel container on your
own machine.

The local Compose stack starts three services:

| Service | Local URL | Purpose |
| --- | --- | --- |
| `openclaw-local` | `http://127.0.0.1:18789/` | OpenClaw Gateway and Control UI |
| `workspace-cms` | `http://127.0.0.1:8090/` | Workspace file review, previews, GitHub manager, public promotion |
| `workspace-ui` | `http://127.0.0.1:8888/lab?token=scienceclaw` | JupyterLab over the mounted workspace and data folders |

## Prerequisites

- Docker Desktop or a compatible Docker engine.
- Git.
- A local checkout of this repository.
- Optional model or integration credentials in `.env` or ignored files under
  `./secrets/`.

For a 20 GiB runtime, set this in `.env` before creating or recreating the
container:

```dotenv
SCIENCECLAW_CONTAINER_MEMORY=20g
```

Docker Desktop or your host Docker engine must also be configured to allow that
much memory.

## Start

```bash
cp .env.example .env
docker compose build
docker compose up -d
```

After the first build, use:

```bash
docker compose up -d
```

## Stop

```bash
docker compose down
```

This stops services. It does not automatically delete named volumes.

## Check Running Services

```bash
docker compose ps
```

## Verify The Panel

```bash
make panel-status
docker compose exec openclaw-local scienceclaw-panel-control status --workspace /data/workspace
```

If a port is already in use, start a second instance with the instance helper or adjust the port variables in `.env`.

## Local Secrets

The container can run without secrets for the browser interfaces, seeded
workspace, panel controls, and deterministic demo. Live model calls and GitHub
write operations need credentials.

GitHub organization secrets are available to GitHub Actions jobs. They are not
automatically mounted into a laptop Docker Compose run.

For local use, prefer mounted secret files:

```bash
mkdir -p secrets
printf '%s\n' 'PASTE_FINE_GRAINED_GITHUB_TOKEN' > secrets/github_token
printf '%s\n' 'PASTE_VERDE_API_KEY' > secrets/verde_llm_api_key
chmod 600 secrets/github_token secrets/verde_llm_api_key
```

Then set:

```dotenv
GITHUB_TOKEN_FILE=/run/scienceclaw-secrets/github_token
GH_TOKEN_FILE=/run/scienceclaw-secrets/github_token
VERDE_LLM_API_KEY_FILE=/run/scienceclaw-secrets/verde_llm_api_key
```

Restart after changing `.env`:

```bash
docker compose up -d --force-recreate
```

Do not commit `.env` or anything under `secrets/`.

## Start A Second Instance

Use this when one ScienceClaw container is already running and you want a
separate panel workspace for a different project.

```bash
scripts/start-instance.sh project-two 18790 8889 8091
```

Arguments are:

| Argument | Example | Meaning |
| --- | --- | --- |
| instance name | `project-two` | folder name under `instances/` and Docker Compose project suffix |
| gateway port | `18790` | OpenClaw Gateway / Control UI |
| workspace UI port | `8889` | JupyterLab file browser |
| CMS port | `8091` | workspace CMS |

The instance stores its state separately under `instances/project-two/`,
including its own `workspace`, `data`, `external_storage`, and OpenClaw state.
This lets you keep multiple panel workspaces open without mixing files.

After launching an additional instance, validate it before project work:

```bash
docker exec <gateway-container> openclaw agents list
docker exec <gateway-container> openclaw status
docker exec <gateway-container> openclaw agent \
  --agent main \
  --session-id instance-smoke-$(date +%s) \
  --message 'Reply with exactly: OK' \
  --timeout 120
```

The agent list should show the panel roles with `main` as the human-facing
liaison. Use a unique smoke-test session id so the CLI does not collide with the
browser's active chat transcript. See the [multi-instance runbook](../instance-runbook.md)
for recovery steps if the dropdown is missing or the session locks.

!!! tip "Name instances after projects"
    Use memorable names such as `wildfire-synthesis`, `urban-greenspace`, or `workshop-demo`. The title banner inside the UI can be edited after launch.

!!! warning "Mount narrowly"
    Mount only the folders the panel needs. Avoid mounting your whole home directory into an agent-accessible container.
