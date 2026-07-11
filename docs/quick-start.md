# Quick Start

Set up the OASIS Scientific Discussion Panel container locally. This starts the
OpenClaw Gateway, a seeded discussion-panel workspace, JupyterLab, and the
workspace CMS/file manager.

## Prerequisites

- Docker Desktop or another Docker engine.
- Git and a local checkout of this repository.
- Enough Docker memory for your run. For a 20 GiB runtime, set
  `SCIENCECLAW_CONTAINER_MEMORY=20g` in `.env` and allow Docker that much memory.
- Optional local secrets for live model calls or GitHub push/pull. The container
  can start without them, but model and GitHub-write workflows need them.

## Start The Stack

```bash
cp .env.example .env
docker compose build
docker compose up -d
docker compose ps
```

Open:

| Interface | URL | Purpose |
| --- | --- | --- |
| OpenClaw Control UI | `http://127.0.0.1:18789/` | Chat, sessions, agents, Gateway status |
| Workspace CMS | `http://127.0.0.1:8090/` | File review, previews, GitHub manager, public promotion |
| JupyterLab | `http://127.0.0.1:8888/lab?token=scienceclaw` | Notebooks, file browsing, workspace editing |

If ports are changed in `.env`, use `docker compose ps` to see the active
bindings.

## Panel Commands

The panel starts paused/manual by default. Use:

```bash
make panel-status
make panel-queue QUESTION="Where does the panel disagree about AI for ecological discovery?"
make panel-round
make panel-summary
```

## No-Secrets Demo

The deterministic demo does not require live API access:

```bash
make demo
```

It writes a synthetic discussion round and supporting records under
`workspace/DISCUSSION_ROUNDS/`, `workspace/EXPERIMENTS/`,
`workspace/FACT_CHECKS/`, and the current-state files in `workspace/`.

## Secrets For Full Use

GitHub organization secrets are for GitHub Actions. They do not automatically
appear inside Docker Compose on your laptop.

For local GitHub push/pull or AI-VERDE model calls, use ignored local files such
as:

- `secrets/github_token`
- `secrets/verde_llm_api_key`

Then point `.env` at the mounted paths and recreate the stack:

```dotenv
GITHUB_TOKEN_FILE=/run/scienceclaw-secrets/github_token
GH_TOKEN_FILE=/run/scienceclaw-secrets/github_token
VERDE_LLM_API_KEY_FILE=/run/scienceclaw-secrets/verde_llm_api_key
```

For AI-VERDE and secret setup, see [AI-VERDE Configuration](ai-verde-configuration.md)
and [Secret Migration](secret-migration.md).
