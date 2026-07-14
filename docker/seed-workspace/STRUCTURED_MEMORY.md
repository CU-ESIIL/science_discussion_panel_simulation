# STRUCTURED_MEMORY.md

This file defines the durable memory surfaces for the Scientific Panel Digital
Twin. Agents should update the narrowest appropriate memory file instead of
burying durable state in raw transcripts.

| Memory Type | Canonical Location | Owner |
| --- | --- | --- |
| Topics | `TOPIC_QUEUE.yaml`, `DISCUSSION_INDEX.md` | PI Liaison, Discussion Intelligence Agent |
| Questions | `OPEN_QUESTIONS.md`, `QUESTIONS_FROM_USER.md`, `QUESTIONS_FOR_USER.md` | PI Liaison, Decision Recorder |
| Decisions | `DECISIONS.md` | Decision Recorder |
| Norms | `PANEL_NORMS_HISTORY.md`, `NORM_PROPOSALS/` | Team Science Facilitator |
| Evidence | `EVIDENCE_LEDGER.yaml`, `LITERATURE/evidence_packets/`, `FACT_CHECKS/` | Citation and Evidence Curator |
| Action Items | `INITIAL_TASKS.md`, `DECISIONS.md`, `tasks/` | Decision Recorder, Agent Operations Manager |
| Discussion Timeline | `DISCUSSION_INDEX.md`, `DISCUSSION_ROUNDS/` | Discussion Intelligence Agent |
| Agent Contributions | structured event records in each round | Discussion Intelligence Agent |
| Consensus Scores | `CONSENSUS_STATE.md` | Decision Recorder, Team Science Facilitator |
| Open Questions | `OPEN_QUESTIONS.md` | PI Liaison |
| Future Discussion Queue | `TOPIC_QUEUE.yaml` | PI Liaison, Scientific Director |
| Discussion History | `DISCUSSION_ROUNDS/`, `POSITION_HISTORY/` | Scientific Narrative Lead |

## Memory Rule

Raw transcripts are evidence of conversation, not structured memory by
themselves. Every meaningful change in understanding should be reflected in at
least one structured memory file and linked back to the source round.
