# Discussion Coding Protocol

This public page mirrors the reusable protocol in
`config/discussion-coding-protocol.md`. The config file is the source agents can
include in their prompts; this page explains the same expectations for people
reviewing the dashboard.

## Purpose

The panel records structured minutes so the website can show what the
conversation is about: dominant topics, low-engagement topics, agreement,
disagreement, unresolved questions, decisions, adopted norms, and future work.

## Event Rules

Each meaningful contribution should become one discussion event with:

- a concise summary
- one or more topic tags
- a stance: `agree`, `disagree`, `neutral`, `unresolved`, or `clarification`
- a contribution type: `claim`, `evidence`, `question`, `proposal`, `decision`,
  `norm`, `action`, or `summary`
- links to related events, evidence, questions, decisions, norms, or actions
  when applicable

Repeated statements should link back to an existing event instead of inflating
topic volume.

## Publication Rules

- Publish reviewed summaries and dashboards, not raw private source text by default.
- Label synthetic panel material clearly.
- Preserve minority viewpoints and unresolved questions.
- Do not publish secrets, OAuth callback codes, credentials, private data, or
  unreviewed sensitive claims.

## Source Files

- Agent protocol: `config/discussion-coding-protocol.md`
- Machine-readable schema: `config/discussion-event.schema.json`
- Mock data: `docs/data/discussion-minutes.mock.json`
- Dashboard generator: `scripts/discussion_dashboard.py`
