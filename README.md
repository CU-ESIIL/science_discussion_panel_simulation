# OASIS Scientific Discussion Panel

OASIS Scientific Discussion Panel is a ScienceClaw/OpenClaw appliance for a
persistent evidence-based conversation about:

**AI for Ecology: Accelerating Discoveries, Reducing Uncertainties, and Scaling
Solutions**

Powered by OpenClaw.

The system is not a generic chatbot and not an impersonation engine. Its
on-stage panelists are clearly disclosed AI simulations informed by documented
expertise, published scholarship, methodological orientation, user-provided
context, and source material stored in the workspace. Generated statements do
not represent the real panelists' private views.

## What It Does

- Maintains a durable scientific discussion rather than forcing a final report.
- Tracks current and historical panelist positions.
- Preserves disagreement and uncertainty without fabricating consensus.
- Lets a user ask what has been discussed, where panelists disagree, what
  evidence exists, and what would change each perspective's mind.
- Queues user questions for targeted panel rounds.
- Supports bounded literature checks, fact checks, and small reproducible
  experiments.
- Keeps GitHub as the control plane, the repository as durable public memory,
  the container as replaceable runtime, and the workspace as active panel memory.

## Quick Start

```bash
cp .env.example .env
make init-panel
make doctor
make build
make up
```

Open the main OpenClaw dashboard URL printed by:

```bash
docker compose exec openclaw-local openclaw dashboard --no-open
```

The CMS/file-review sidecar remains available at
`http://127.0.0.1:8090/files?path=/workspace`.

## Panel Controls

```bash
make panel-status
make panel-pause
make panel-resume
make panel-queue QUESTION="Ask the panel whether AI can discover ecological mechanisms."
make panel-round
make panel-summary
```

The deprecated `make init-working-group` target remains as a compatibility
alias, but the default scaffold is now panel-centered.

## Deterministic Demo

The demo requires no API keys or network access. It writes a synthetic panel
round on "Does predictive accuracy constitute ecological discovery?"

```bash
make demo
```

Expected outputs include `workspace/DISCUSSION_ROUNDS/round-001/`,
`CURRENT_POSITIONS.md`, `DISAGREEMENT_MAP.md`, `EVIDENCE_LEDGER.yaml`,
`FACT_CHECKS/`, `EXPERIMENTS/results/`, and `CURRENT_SYNTHESIS.md`.

Fixture text is labeled synthetic and must not be treated as a real panel
response.

## Resource Limits

The panel is paused/manual by default. Autonomous recurring rounds require
explicit configuration:

```dotenv
PANEL_AUTORUN=1
PANEL_DISCUSSION_INTERVAL_MINUTES=60
PANEL_MAX_TURNS_PER_ROUND=12
PANEL_MAX_PANELISTS_PER_ROUND=4
PANEL_MAX_RESEARCH_TASKS_PER_ROUND=2
PANEL_MAX_EXPERIMENTS_PER_DAY=1
PANEL_REQUIRE_EXPERIMENT_APPROVAL=1
```

Use `PANEL_DAILY_TOKEN_BUDGET` and
`PANEL_DAILY_COMPUTE_BUDGET_MINUTES` when running unattended. The system should
pause at configured budget limits rather than burn credits indefinitely.

## AI-VERDE And Model Routing

AI-VERDE remains a first-class OpenAI-compatible provider. Keep provider
configuration centralized in `.env`, mounted secret files, GitHub Secrets,
self-hosted runner secrets, or Kubernetes Secrets:

```dotenv
VERDE_LLM_BASE_URL=https://llm-api.cyverse.ai/v1
VERDE_LLM_API_KEY=
VERDE_LLM_API_KEY_FILE=
VERDE_LLM_DEFAULT_MODEL=
VERDE_LLM_PROVIDER_NAME=verde
OPENCLAW_MODEL=
OPENCLAW_DEFAULT_MODEL=
```

Role-level assignments live in `docker/seed-workspace/MODEL_ASSIGNMENTS.md` and
the spawned workspace copy. Do not hard-code a commercial provider as the only
route.

## Secrets

GitHub forks do not inherit repository or Actions secrets. Recreate required
secrets and variables for this repository or add it to organization-level secret
allowlists. Validate local configuration without printing values:

```bash
make check-secrets
```

See [Secret Migration](docs/secret-migration.md).

## Safety Model

- The Interaction Agent is the default human-facing agent.
- On-stage panelists are simulated perspectives, not real people.
- The Moderator manages agenda and disagreement without forcing consensus.
- Evidence, fact checks, experiments, and position changes are traceable files.
- Human approval is required for secrets, publishing, deletion, GitHub pushes,
  new mounts, third-party tools, expensive jobs, billed APIs, and sensitive
  public claims.
- Slack, when enabled, should route through the Interaction Agent only.
- Kubernetes workers remain bounded execution mechanisms, not autonomous
  unbounded agents.

## Core Commands

| Command | Purpose |
| --- | --- |
| `make init-panel` | Create or refresh the panel workspace scaffold |
| `make panel-status` | Show panel state and pending questions |
| `make panel-pause` / `make panel-resume` | Control recurring discussion state |
| `make panel-round` | Run one deterministic local panel round |
| `make demo` | Run the deterministic synthetic panel demo |
| `make smoke-test` | Run lightweight validation |
| `make test-panel` | Validate the seeded panel scaffold |
| `make check-secrets` | Validate secret configuration without values |
| `make workspace-smoke-test` | Validate the workspace file manager |
| `make github-smoke-test` | Validate the GitHub repository manager |

## Existing Infrastructure Preserved

The Dockerfile, Docker Compose stack, OpenClaw runtime, AI-VERDE configuration,
mounted secret-file support, GitHub Actions, workspace persistence, CMS/file
review sidecar, GitHub repository manager, MkDocs documentation, local/cloud
launch paths, smoke tests, storage zones, optional Slack, optional Kubernetes
workers, and multi-instance support remain part of the appliance.

## Documentation

Start with:

- [Quick Start](docs/quick-start.md)
- [Panel Architecture](docs/panel-architecture.md)
- [Panelists](docs/panelists.md)
- [Persistent Discussion Loop](docs/persistent-discussion-loop.md)
- [Asking the Panel Questions](docs/asking-the-panel.md)
- [Evidence and Citations](docs/evidence-and-citations.md)
- [Experiments](docs/experiments.md)
- [Memory and Discussion Records](docs/memory-and-discussion-records.md)
- [AI-VERDE Configuration](docs/ai-verde-configuration.md)
- [Secret Migration](docs/secret-migration.md)
- [Resource Limits](docs/resource-limits.md)
- [Security and Human Oversight](docs/security-and-human-oversight.md)
