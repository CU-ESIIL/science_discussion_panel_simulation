# OASIS Scientific Discussion Panel Workspace

This workspace is the active memory for a persistent scientific discussion panel
on AI for Ecology: Accelerating Discoveries, Reducing Uncertainties, and Scaling
Solutions.

The panel is a set of disclosed AI simulations informed by documented expertise,
published scholarship, methodological orientation, user-provided context, and
source material stored here. It does not speak for the real researchers whose
work inspired the perspectives.

## Start Here

1. Read `PANEL_BRIEF.md`.
2. Review `PANELIST_ROSTER.md` and `AGENTS.md`.
3. Check `SYSTEM_STATUS.md`.
4. Use `PANEL_INTAKE.md` if the user wants to change topic, cadence, panelists,
   or research permissions.
5. Run one deterministic local round with `make demo` from the repository root.

## Memory Files

- `PANEL_CONSTITUTION.md` - draft norms and operating rules.
- `TOPIC_QUEUE.yaml` - pending, active, parked, and completed topics.
- `DISCUSSION_ROUNDS/` - append-only round records.
- `CURRENT_POSITIONS.md` and `POSITION_HISTORY/` - current and historical views.
- `DISAGREEMENT_MAP.md` - active disagreement map.
- `EVIDENCE_LEDGER.yaml` and `LITERATURE/` - claim/source tracking.
- `EXPERIMENTS/` - bounded proposals and results.
- `FACT_CHECKS/` - claim verification records.
- `CURRENT_SYNTHESIS.md` and `DAILY_SYNTHESIS/` - compact summaries.

## Human Interface

The Interaction Agent is the default human-facing role. It summarizes from
panel memory, queues user questions, requests targeted rounds, and reports loop
status. It must not invent responses that were not produced by the panel.

## Safety Defaults

The panel is paused by default. Autonomous recurring discussion requires
explicit configuration through `PANEL_AUTORUN=1` plus cadence and budget limits.
Experiments are bounded and require approval unless configured otherwise.

Secrets belong in `.env`, mounted secret files, GitHub Secrets, runner secrets,
or Kubernetes Secrets. Never write secret values into panel prompts, logs,
transcripts, CMS pages, or markdown memory.

Powered by OpenClaw.
