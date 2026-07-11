---
hide:
  - toc
---

# OASIS Scientific Discussion Panel

OASIS Scientific Discussion Panel is a local ScienceClaw/OpenClaw container for
a persistent evidence-based scientific forum about **AI for Ecology:
Accelerating Discoveries, Reducing Uncertainties, and Scaling Solutions**.

It is not just a docs site. This repository builds a runnable appliance with an
OpenClaw Gateway, a seeded panel workspace, JupyterLab, a browser file/CMS
review tool, GitHub repository management, MkDocs documentation, mounted
secrets, AI-VERDE/OpenAI-compatible model routing, optional Slack, and optional
bounded workers.

The central product is the continuing discussion. Notes, transcripts, evidence
ledgers, experiments, summaries, position histories, disagreement maps, and
public reports support that discussion without pretending that every question
has a final answer.

## What This Container Is For

- Run a disclosed simulated scientific panel focused on AI for ecology.
- Keep scientific memory in files that people can inspect, edit, review, and
  version.
- Separate active private workspace material from reviewed public website
  artifacts.
- Let humans ask questions, queue panel rounds, inspect disagreements, and
  decide what should be published or pushed to GitHub.
- Provide a repeatable local environment for model routing, evidence checks,
  small experiments, report review, and repository operations.

## Mental Model

| Layer | Role |
| --- | --- |
| GitHub | Control plane and durable public project history |
| Repository | Source for the container, website, docs, tests, scripts, and reusable seed files |
| Container | Replaceable runtime with OpenClaw, CMS, JupyterLab, tools, and agents |
| `./workspace` | Active panel memory mounted into `/workspace` and `/data/workspace` |
| `./data` | Runtime outputs, logs, notebooks, reports, and local data layout |
| `./external_storage` | Local hook for large or institutionally managed data |
| `./secrets` and `.env` | Local-only configuration and credentials; never committed |

## Start

```bash
cp .env.example .env
docker compose build
docker compose up -d
docker compose ps
make panel-status
```

Typical local URLs are:

- OpenClaw Control UI: `http://127.0.0.1:18789/`
- Workspace CMS: `http://127.0.0.1:8090/`
- JupyterLab: `http://127.0.0.1:8888/lab?token=scienceclaw`

The deterministic demo does not need live model credentials:

```bash
make demo
```

For a 20 GiB local container, set this in `.env` before recreating the stack:

```dotenv
SCIENCECLAW_CONTAINER_MEMORY=20g
```

Docker Desktop or the host Docker engine must also be allowed that much memory.

!!! warning "Secrets are local unless a runner injects them"
    GitHub organization secrets work for GitHub Actions jobs. They are not
    automatically available to Docker Compose on your laptop. For local GitHub
    push/pull or AI-VERDE model calls, provide local secret files or local
    environment variables.

## Read Next

- [Quick Start](quick-start.md)
- [Launch Locally](use/launch-locally.md)
- [Panel Architecture](panel-architecture.md)
- [Panelists](panelists.md)
- [Persistent Discussion Loop](persistent-discussion-loop.md)
- [Asking the Panel Questions](asking-the-panel.md)
- [Evidence and Citations](evidence-and-citations.md)
- [Secret Migration](secret-migration.md)

## Representation

The panelists are disclosed simulations informed by documented expertise and
source material. They do not speak for the real people whose work inspired the
perspectives, and generated statements must never be presented as private views.
