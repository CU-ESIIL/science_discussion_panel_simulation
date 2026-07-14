# Changelog

## Unreleased

### Added

- Added the OASIS Scientific Discussion Panel scaffold with disclosed simulated
  panelist perspectives, a Moderator, backstage support agents, panel
  constitution files, topic queue, discussion rounds, position history,
  disagreement map, evidence ledger, fact-check records, bounded experiment
  records, current synthesis, and panel status files.
- Added panel control commands and deterministic panel demo support through
  `make init-panel`, `make panel-status`, `make panel-pause`,
  `make panel-resume`, `make panel-queue`, `make panel-round`, `make demo`,
  `scripts/panel_control.py`, and `scripts/demo_panel_discussion.py`.
- Added `docs/secret-migration.md`, `scripts/check-secret-config.sh`, and
  panel-oriented documentation for architecture, panelists, support agents,
  constitution, persistent loop, questions, evidence, experiments, memory,
  AI-VERDE, resource limits, and human oversight.
- Added clearer container-oriented onboarding across the website, including
  local URLs, service roles, 20 GiB memory configuration, no-secrets demo use,
  and the difference between GitHub Actions secrets and local Docker Compose
  secret files.
- Added the supplied Ecologists Meet AI hero/contact-sheet artwork as tracked
  site assets, cropped reusable panel tiles, a public latest-discussion brief,
  a generated discussion dashboard, structured mock minutes, a discussion-event
  schema, an agent coding protocol, CSV/JSON exports, and tests for dashboard
  aggregation.

### Fixed

- `scripts/start-instance.sh` now validates that `SCIENCECLAW_RUNTIME_ROOT` is writable before use and automatically falls back to `$RUNNER_TEMP`/`/tmp` with a warning when the configured path is unavailable. This prevents startup failures like `mkdir: cannot create directory '/private': Permission denied` on restricted runners.
- Clarified the local browser startup path in `README.md`, `docs/quick-start.md`, `docs/operations.md`, and `docs/troubleshooting.md` so the main OpenClaw chat opens from the tokenized `127.0.0.1:18789` Gateway URL rather than the `8090` CMS sidecar, and so first-run token auth plus one-time device pairing are documented explicitly.
- Added password-auth support to the local Gateway startup scripts so Docker
  Compose can run the container with `OPENCLAW_GATEWAY_AUTH_MODE=password` and a
  local `OPENCLAW_GATEWAY_PASSWORD` instead of relying on a tokenized dashboard
  URL.
- Added `OPENCLAW_GATEWAY_TOKEN` to Compose environment forwarding and documented
  a stable local token URL for no-prompt Control UI access.
- Added `make open-ui` and `scripts/open-control-ui.sh` to open the local
  Control UI with the configured token fragment.
- Changed `make up` to start Docker Compose in detached mode and added
  `make start` as the one-command local launch path.
- Disabled the extra Control UI browser/device pairing gate by default for local
  containers with `SCIENCECLAW_DISABLE_CONTROL_UI_DEVICE_PAIRING=1`; Gateway
  token or password auth still applies.
- Disabled persisted OpenClaw Gateway cron jobs by default on container startup
  with `SCIENCECLAW_DISABLE_OPENCLAW_CRON=1`, and added `make cron-off` for
  disabling any live scheduled jobs.

### Changed

- Reset the default OpenClaw agent architecture to the 14-role Scientific Panel
  Digital Twin: PI Liaison, Scientific Director, Domain Scientist, Quantitative
  Modeler, Data Engineer / Infrastructure Scientist, Citation and Evidence
  Curator, Skeptical Reviewer, Team Science Facilitator, Scientific Narrative
  Lead, Societal Impact Agent, Decision Recorder, Discussion Intelligence Agent,
  Cloud Infrastructure Engineer, and Agent Operations Manager.
- Added seed-level structured discussion infrastructure for dashboard
  integration: `TAG_ONTOLOGY.md`, `STRUCTURED_MEMORY.md`, and
  `DISCUSSION_EVENT_TEMPLATE.md`.
- Removed the old default real-person-inspired panelist source notes and
  older role reproducibility templates from the seed initializer.
- Reframed the default repository and seeded workspace from a deliverable-oriented
  scientific working group to a persistent scientific discussion panel while
  preserving Docker, Docker Compose, OpenClaw, AI-VERDE, mounted secrets, CMS,
  GitHub manager, storage, worker, Slack, MkDocs, smoke-test, and multi-instance
  infrastructure.
- Updated `.env.example`, `config/working_group.yaml`, seed model assignments,
  seed startup prompts, Makefile targets, smoke tests, and GitHub Actions labels
  for the panel model while retaining deprecated working-group aliases for
  compatibility.
- Switched the default local OpenClaw route and all panel role assignments to
  AI-VERDE `verde/js2/gpt-oss-120b` after operator approval, replacing the
  previous OpenAI/Codex-first defaults for human-facing and director roles, and
  added `SCIENCECLAW_VERDE_ONLY_MODE=1` to prune stale OpenAI/Codex routes from
  the persisted default agent allowlist.
- Updated `AGENTS.md` to identify this repository as the OASIS Scientific
  Discussion Panel container appliance and to document what users need for local
  operation, secrets, GitHub access, and Docker resource settings.
- Updated the homepage to use the supplied hero image and link directly to the
  latest discussion brief, dashboard, and discussion coding protocol.
- Reworked the MkDocs information architecture into a simpler product-style navigation with Start Here, Use OpenClaw, Working Groups, Data and Storage, and Maintainer / Advanced sections.
- Redesigned the homepage with OASIS-inspired hero, section bands, visual interludes, gallery-style card grids, and clearer calls to action for onboarding, working-group use, storage, and advanced customization.
- Added a new `docs/start-here/what-is-openclaw.md` overview page to explain the container, agent workspace, and scientific collaboration layers in plain language for new scientists.
- Ignored runtime-generated `workspace/projects/*` folders while preserving the
  tracked example project template.

## 0.1.0-alpha.1 - 2026-05-17

First alpha baseline for the OpenClaw scientific working group container.

### Added

- OASIS ScienceClaw template mode with durable Control UI branding, a current-working-group banner, canonical working-group configuration, cockpit orientation, checkpoint, consensus, and contribution files.
- Canonical seeded workspace folders for datasets, outputs, maps, reports, manuscripts, presentations, notebooks, tasks, reviews, decisions, assumptions, runtime notes, cache, and config.
- Reproducible `/workspace` seed under `docker/seed-workspace`.
- Eleven bounded working-group roles, including the PI Liaison / User Interview Agent as the default human-facing role.
- Project memory, intake, charter, team brief, initial tasks, human-review, assumption, decision, and question-queue files.
- PI Liaison startup prompt and startup script.
- Slack credential handling through local `.env` variables, with masked validation.
- Environment-backed Slack channel registration at container startup.
- Security documentation for Slack tokens and token rotation.
- Operations documentation for Slack Socket Mode, Slack user pairing, live Gateway Codex OAuth refresh, and direct agent smoke tests.
- Role-based model routing documentation and seeded `MODEL_ASSIGNMENTS.md` for open-model API experiments.
- Curated example snapshot area, including an urban wildlife corridors project capture from a live working-group run.
- Seeded template governance package: team norms, decision protocol, memory quarantine, artifact registry, societal impact checklist, meeting template, data directories, and role reproducibility notes.
- ScienceClaw `/data` layout, optional JupyterLab workspace UI, baseline scientific shell tools, document conversion examples, and brand assets.
- ScienceClaw documentation page with ESIIL-informed palette and workspace architecture notes.
- Bounded distributed spatial-temporal runtime scaffold with a local worker path, optional Kubernetes manifests, STAC/COG/Zarr examples, output indexing, and job metadata conventions.
- Three-zone repository/workspace/external-storage architecture, including `/external_storage/local` support.
- Lightweight file-backed workspace CMS for reviewing private artifacts and promoting approved pages/assets into the MkDocs public site.
- Storage registry templates, provider profiles, schema, and safe helper commands for local, STAC, COG, S3-compatible, WebDAV, iRODS, and OSN-style storage patterns.
- Public publishing workflow docs, sample promoted report, and sample metadata-only dashboard pattern.
- Continuous improvement protocol, starter log, and role review template seeded into the working group scaffold.
- Pre-remodel capture audit notes for separating reusable template changes from private workspace/project artifacts.
- Lean Pandoc PDF toolchain added to the image with LaTeX packages needed for manuscript-style PDF exports.
- Beginner-oriented MkDocs learning path with Start Here, First 10 Minutes, Concepts for Scientists, Launch and Daily Use, Troubleshooting, and Glossary pages.
- Makefile entry points and lightweight `init-working-group`, `doctor`, and `checkpoint` scripts for calm startup, validation, and session preservation.
- Stabilization docs for quick start, architecture, storage, agents, CMS/output review, Slack, Kubernetes workers, credentials, and troubleshooting.
- Deterministic environmental demo workflow and `make smoke-test` operational validation command.
- Prompt action log for preserving implementation provenance and known limitations.
- Smoke tests for working-group scaffold and secret validation.
- Pinned OpenClaw image build argument and separated service entrypoint so only the Gateway owns OpenClaw startup/state while CMS and Jupyter remain workspace services.
- Embedded Control UI sidebar tools for Files and GitHub Auth, backed by the workspace CMS instead of separate navigation-only links.
- GitHub credential setup button in the CMS, spawned-instance Docker secrets overlay support, and a manual GitHub Actions runtime workflow for self-hosted runner launches from GitHub Secrets.
- Gateway 3 GitHub authentication docs for token-file launches, sidebar credential setup, shared `/workspace/repos/` repository visibility, and OpenClaw update checks that preserve ScienceClaw branding, Files, GitHub Auth, and CMS content-security-policy access.
- CMS full-page navigation back to the matching OpenClaw Control UI from Files, GitHub, and other workspace pages.
- Project workspace routing folders under `/workspace/projects`, with manifests for GitHub repositories, external links, storage aliases, data policy, and gateway handoffs; gateway 3 now has a `fractal-corridors` project control folder linked to the gateway 1 import.
- Workspace `RESOURCE_MAP.md` instructions so agents know where to read/write files, find project manifests, use authorized GitHub clones, and route large or remote data through `/external_storage`.
- Tracked gateway 1 handoff, gateway 3 resource map, and workspace notes inside `projects/fractal_corridors` so the project-routing metadata is visible to GitHub outside the live container runtime.
- GitHub Actions runtime workflow now accepts local `.env`-style Verde and Slack secret aliases in addition to the recommended `SCIENCECLAW_...` secret names.
- Spawned instances now choose a platform-appropriate OpenClaw state directory, using `/private/tmp` on macOS, `$RUNNER_TEMP` on GitHub Actions, and `/tmp` on other Linux hosts.
- Template GitHub launch docs and workflow support for authorizing and cloning the launch repository into `/workspace/repos/<repo>` so forked repositories can act as their own ScienceClaw project memory.

### Notes

- Real Slack tokens, OpenAI keys, and local runtime state are intentionally excluded from git.
- Users should start from `.env.example`, create a local `.env`, invite the Slack bot to a channel, and use a `channel:<id>` target when possible.
