---
hide:
  - toc
---

<section class="site-photo-hero">
  <img src="assets/panel/ecologists-meet-ai-hero.png" alt="Ecologists and AI researchers discussing ecosystem science on a conference panel">
  <div class="site-photo-hero__copy">
    <p class="eyebrow">OASIS Scientific Discussion Panel</p>
    <h1>Ecologists meet AI in a container built for durable scientific memory.</h1>
    <p>Run a disclosed simulated panel, preserve evidence and disagreement, and publish reviewed discussion summaries to the website.</p>
    <div class="cta-buttons">
      <a class="md-button md-button--primary" href="quick-start/">Start locally</a>
      <a class="md-button" href="dashboard/discussion-dashboard/">View dashboard</a>
      <a class="md-button" href="reports/latest-discussion/">Latest discussion</a>
    </div>
  </div>
</section>

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

<div class="panel-image-strip">
  <img src="assets/panel/panel-tile-01-speaker.png" alt="Panel participant speaking with a microphone">
  <img src="assets/panel/panel-tile-05-key-questions.png" alt="Participant writing key questions about ecological AI on a board">
  <img src="assets/panel/panel-tile-07-breakout.png" alt="Small group discussing notes around a laptop">
  <img src="assets/panel/panel-tile-08-voting.png" alt="Audience members voting with colored cards">
  <img src="assets/panel/panel-tile-10-map-talk.png" alt="Presenter pointing to a species richness map">
</div>

- Run a disclosed simulated scientific panel focused on AI for ecology.
- Keep scientific memory in files that people can inspect, edit, review, and
  version.
- Separate active private workspace material from reviewed public website
  artifacts.
- Let humans ask questions, queue panel rounds, inspect disagreements, and
  decide what should be published or pushed to GitHub.
- Provide a repeatable local environment for model routing, evidence checks,
  small experiments, report review, and repository operations.

## Public Discussion Outputs

The panel maintains a tracked public discussion log and latest-discussion brief
in the website source. After human review in GitHub Desktop, pushing the
repository lets GitHub Actions rebuild the site so readers can see what the
panel most recently discussed, what dominated, what stalled, what remains
unresolved, and what should happen next.

The dashboard turns structured minutes into a visual summary of conversation
activity: topic volume, stance distributions, open questions, decisions, adopted
norms, future queue, timeline, and agent participation.

<div class="homepage-card-grid">
  <a class="homepage-card" href="reports/latest-discussion/">
    <strong>Latest discussion</strong>
    <p>Reviewed public brief of the most recent panel round.</p>
    <span>Read the brief</span>
  </a>
  <a class="homepage-card" href="reports/panel-discussion-log/">
    <strong>Discussion log</strong>
    <p>Append-only markdown record of substantive panel discussions.</p>
    <span>Open the log</span>
  </a>
  <a class="homepage-card" href="dashboard/discussion-dashboard/">
    <strong>Conversation dashboard</strong>
    <p>See which topics dominated, stalled, resolved, or remained contested.</p>
    <span>Open dashboard</span>
  </a>
  <a class="homepage-card" href="discussion-coding-protocol/">
    <strong>Coding protocol</strong>
    <p>Structured minute-taking rules for panel agents and reviewers.</p>
    <span>See the model</span>
  </a>
</div>

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
