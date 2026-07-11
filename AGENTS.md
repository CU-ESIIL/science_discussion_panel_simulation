# AGENTS.md

## Project Identity
- This repository builds the OASIS Scientific Discussion Panel container.
- Treat the repo as a reusable ScienceClaw/OpenClaw appliance, not only a static website or one-off analysis folder.
- The container is for a persistent, evidence-based AI-for-ecology discussion panel with disclosed simulated panelists, a Moderator, an Interaction Agent, support agents, durable workspace memory, and human review gates.
- The core runtime is Docker Compose: `openclaw-local` serves the OpenClaw Gateway, `workspace-ui` serves JupyterLab, and `workspace-cms` serves file review, previews, public promotion, and GitHub repository management.
- The common local interfaces are:
  - OpenClaw Control UI: `http://127.0.0.1:18789/`
  - Workspace CMS: `http://127.0.0.1:8090/`
  - JupyterLab: `http://127.0.0.1:8888/lab?token=scienceclaw`
- GitHub is the control plane, the repository is durable public memory, the container is replaceable runtime, `./workspace` is active panel memory, `./data` is runtime/output storage, and `./external_storage` is for large or externally managed data.
- Local `.env`, `./secrets/`, OpenClaw state, OAuth state, tokens, logs, generated runtime workspace files, and large private data are not repository content.

## User Requirements And Local Use
- Users need Docker Desktop or a compatible Docker engine, a local git checkout, and enough Docker resources for the selected workload.
- For a 20 GiB local runtime, set `SCIENCECLAW_CONTAINER_MEMORY=20g` in `.env`; Docker must also be allowed that much memory in Docker Desktop or the host engine.
- A no-secrets local run can start the Gateway, CMS, JupyterLab, deterministic demo, seeded workspace, and panel control commands.
- Live model calls require a configured model route such as Codex OAuth, OpenAI API key, or AI-VERDE-compatible endpoint credentials.
- GitHub push/pull from inside the container requires a local mounted token file or environment-provided token. GitHub organization secrets are available to GitHub Actions runners only; they are not automatically visible to Docker Compose on a laptop.
- Prefer mounted local secret files such as `./secrets/github_token` and `./secrets/verde_llm_api_key` over literal token values in `.env`. Never print or document token contents.
- The intended first local path is `cp .env.example .env`, adjust resource and secret settings, `docker compose build`, `docker compose up -d`, then verify with `docker compose ps`, `make panel-status`, and the local URLs above.

## Core Operating Contract
- Treat this repository as the source of truth.
- Treat the website as a rendered view of repository state.
- Prefer small, additive, traceable edits.
- Keep documentation synchronized with code and project structure.
- Keep the repository minimalist by default.

## Default Workflow
- Inspect repository structure before editing.
- Make the smallest diff that solves the request.
- Update related docs when behavior, workflows, or outputs change.
- Update changelog, dev log, or equivalent history files for meaningful changes.
- Preserve existing structure and historical context.
- Do not perform destructive rewrites unless explicitly requested.

## Documentation and Website Policy
- Treat `docs/` as project-level documentation and website source.
- Update docs whenever code, workflows, or outputs change.
- Amend existing docs when possible; do not replace whole files without need.
- Preserve navigation, readability, and consistency in website changes.
- Keep default website behavior clean and minimal unless the user asks for more expressive design.

## Testing Policy
- Assume `tests/` may exist before a full testing framework is defined.
- Do not invent domain-specific tests when expected behavior is unclear.
- Add the smallest meaningful tests when behavior is known.
- Prefer early-stage checks such as smoke tests, import tests, CLI tests, schema checks, or example-based checks.
- If tests are deferred, document the gap; do not imply coverage that does not exist.

## Package and Structure Separation Policy
- Keep website structure and package structure clearly separated.
- Do not automatically repurpose `docs/` for package-native docs or build artifacts.
- For Python packaging requests, prefer standard Python layout, typically `src/`.
- For R packaging requests, follow standard R conventions (`R/`, `man/`, `DESCRIPTION`, `NAMESPACE`, optional `vignettes/`).
- For other ecosystems, follow ecosystem conventions.
- If structural conflicts arise, choose a durable long-term structure and document the decision.

## Data Discovery and Data Use Policy
- Prefer open and FAIR data when possible.
- Prefer streaming or lazy-access workflows over bulk downloads when feasible.
- Use standards-based discovery systems (for example STAC) when relevant.
- When relevant, consider streaming-friendly tooling such as xarray, zarr, GDAL, rasterio, pystac-client, stackstac, gdalcubes, terra, stars, cubo, or equivalent tools.
- When introducing data, document source, access method, format, license, and citation requirements.
- Do not silently ingest external data into the project.

## Data Sovereignty and Intellectual Property Policy
- Consider licensing, copyright, privacy, Indigenous data sovereignty, and related restrictions for all data and content.
- If rights or permissions are unclear, document uncertainty and avoid assuming open reuse.

## Design and Usability Policy
- Keep the website simple, readable, and easy to extend by default.
- When design improvements are requested, prioritize system-level improvements (layout, spacing, typography, hierarchy, navigation, consistency).
- Do not use scattered one-off styling hacks.
- If direct site inspection is possible, verify readability, navigation, link integrity, and that docs still reflect repository state.

## Decision Logging
- Reflect meaningful structural, architectural, documentation, data-source, or design decisions in changelog, dev log, roadmap, or equivalent history files when appropriate.

## OpenClaw Slack/Gateway Operations
- Keep the reproducible Slack path documented in `docs/operations.md` whenever scripts, Docker behavior, auth setup, Slack setup, or pairing behavior changes.
- Treat Gateway startup, Slack Socket Mode, Slack user pairing, and model OAuth as four separate gates. Do not collapse them into one vague "Slack is broken" diagnosis.
- For Codex OAuth troubleshooting, prefer re-authenticating inside the live Gateway container with `openclaw models auth login --provider openai-codex --set-default`, then verify with `openclaw models status` and a direct `openclaw agent` smoke test.
- Never document or print full OAuth callback codes, Slack tokens, OpenAI API keys, gateway tokens, or credential file contents. Use masked previews only.
- Keep Slack-facing behavior routed through the PI Liaison. Do not add documentation or code paths that let Slack directly trigger arbitrary shell execution or bypass human approval gates.

## Model Routing Policy
- Keep role-level model routing explicit in `docs/model-routing.md` and seeded workspace files such as `MODEL_ASSIGNMENTS.md`.
- Preserve OpenAI/Codex OAuth, or another explicitly approved high-reliability route, for the PI Liaison and Scientific Director unless the user approves a change.
- Treat open-model API routes, including Verde-style OpenAI-compatible endpoints, as experiments until their role behavior, citation handling, and safety boundaries are evaluated.
- Do not store provider API keys, endpoint secrets, OAuth callbacks, or token values in tracked docs, prompts, logs, screenshots, or markdown memory files.
- When adding provider automation, verify behavior against the installed OpenClaw version and update the setup docs plus smoke tests.
