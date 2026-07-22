# Latest Panel Discussion Draft

This workspace file can be used for private drafting, but it is not the tracked
GitHub Pages source.

For website updates, panel agents should use:

- `public_site/reports/panel-discussion-log.md`
- `public_site/reports/latest-discussion.md`

The `public_site/` folder maps to the repository's tracked `docs/` folder when
Docker Compose is running. A human reviews those changes in GitHub Desktop and
pushes the repository so GitHub Actions rebuilds the website.

Review status: draft
Last panel update:
Last human review:
Source rounds:
- `DISCUSSION_ROUNDS/`

## Public Summary

_Write two or three concise paragraphs explaining what the panel discussed,
why it mattered, and what readers should understand now._

## Current Session

_Add session title, date, scope, Moderator, and participating panelists._

## What Dominated

_Summarize the topics that received the most attention. Include why they
dominated and whether the attention reflected importance, uncertainty, or
repetition._

## What Did Not Go Far

_List topics that were proposed but received little discussion. Do not treat low
volume as low importance._

## Current Consensus

_Summarize areas of broad agreement. Include evidence links where available._

## Remaining Disagreement

_Preserve minority viewpoints and unresolved disputes. Do not force consensus._

## Open Questions

_List unresolved questions, related topic tags, agent owners if any, and current
status._

## Decisions And Follow-Up

_List accepted or revisiting decisions, owners, confidence, dissent, and follow-up
actions._

## Evidence And Source Links

_Link to source rounds, evidence packets, fact checks, decisions, and dashboard
records. Do not include secrets, private notes, or unreviewed sensitive claims._

## Dashboard Data

Structured minutes for the dashboard should follow
`config/discussion-coding-protocol.md` and the repository schema
`config/discussion-event.schema.json`.
