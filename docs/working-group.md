# Scientific Panel Digital Twin

A good scientific agent system is not a pile of chatbots. It is a small
institution with roles, memory, evidence standards, disagreement, structured
minutes, and human review.

The Scientific Panel Digital Twin scaffold in this repository creates a
reproducible environmental data science workspace under `/workspace` inside the
OpenClaw container. It is intended for synthesis work where claims need
provenance, discussion needs dashboard-ready metadata, and autonomous
capabilities need clear boundaries. The scaffold does not make autonomy safe by
itself; it creates a better operating structure for human-supervised work.

The core files are simple Markdown registers. `MEMORY.md` holds durable institutional memory. `ROADMAP.md` organizes work from project charter through release package. `ASSUMPTIONS.md` records assumptions and their risks. `DECISIONS.md` records major decisions. `HUMAN_REVIEW.md` defines actions that require explicit human approval.

`MODEL_ASSIGNMENTS.md` records which model route each role should use. The
current approved local default routes every Scientific Panel Digital Twin role
through Verde.

The seed also includes reusable governance templates: team norms, decision
protocol, memory quarantine protocol, artifact registry, societal impact
checklist, role notes, a tag ontology, structured memory map, event template,
and a meeting template. These make the container reproducible without requiring
every new deployment to recreate panel norms from scratch.

Analyses belong in `analysis/` and reproducible utilities belong in `scripts/`. Figures belong in `figures/`, with enough provenance to trace them back to scripts and data sources. Literature, citation notes, and evidence tables belong in `literature/`. Daily working memory belongs in `daily_notes/`, while role-specific memos and skeptic reviews belong in `agent_reports/`.

The design is intentionally bounded. Each role has expected inputs, expected outputs, and limits. Third-party skills, broad filesystem mounts, autonomous shell access, external APIs, and credentials should be treated as high-trust capabilities. Human review is required before publication, destructive file operations, new mounts, new skills, external messages, expensive jobs, billed APIs, or sensitive claims.

## PI Liaison Gateway

The user should not have to manage 14 agents by hand. The PI Liaison turns a
multi-agent scientific panel into one coherent conversation.

The PI Liaison is the default human-facing role. It greets the user, asks the
configuration questions in `PANEL_INTAKE.md`, records preferences and
constraints in `USER_CONTEXT.md`, assigns question owners, and writes
`TEAM_BRIEF.md` for the scientific panel. The rest of the panel communicates
through structured discussion events, task assignments, and memory files rather
than competing for the user's attention.

When other agents need user input, they write questions in `QUESTIONS_FOR_USER.md`. The PI Liaison deduplicates the queue, merges related questions, and asks only the highest-value followups. The same role returns milestone summaries, draft reports, and release packets to the user for review. It does not invent scientific goals or approve publication, deletion, GitHub pushes, external API use, or sensitive claims.

For Slack-connected use, the Liaison is the only Slack-facing component. Slack messages should enter queues and workspace memory before they are routed to the team. Slack must never directly trigger arbitrary shell execution, and Slack tokens must stay in local environment variables rather than markdown, logs, screenshots, prompts, or git.

Operationally, Slack use has a few distinct gates: Socket Mode must be healthy, the Slack sender must be paired, and the running Gateway must have a fresh model login. Keep those checks separate when diagnosing failures. The reproducible command sequence is documented in the [Operations guide](operations.md).

## Role Summary

| Role | Primary purpose | Main outputs |
| --- | --- | --- |
| PI Liaison | Coordinate discussion and human-facing flow. | Question ownership, transitions, user summaries |
| Scientific Director | Maintain scientific vision. | Theme synthesis, future directions, claim-readiness notes |
| Domain Scientist | Ground interpretation in ecological realism. | Mechanism notes, assumptions, literature requests |
| Quantitative Modeler | Represent mathematical reasoning. | Model plans, diagnostics, uncertainty assessments |
| Data Engineer / Infrastructure Scientist | Make data and infrastructure reproducible. | Data inventories, provenance notes, storage plans |
| Citation and Evidence Curator | Maintain evidence quality. | Evidence ledger entries, citation audits, fact-check requests |
| Skeptical Reviewer | Challenge ideas constructively. | Alternative hypotheses, failure modes, robustness requirements |
| Team Science Facilitator | Improve collaboration. | Participation summaries, norm proposals, process corrections |
| Scientific Narrative Lead | Maintain the evolving story. | Synthesis drafts, conceptual timelines, figure proposals |
| Societal Impact Agent | Represent broader impacts. | Impact notes, stakeholder maps, ethics flags |
| Decision Recorder | Maintain structured records. | Decisions, action items, ownership, dissent |
| Discussion Intelligence Agent | Convert conversations into metadata. | Structured events, normalized tags, dashboard exports |
| Cloud Infrastructure Engineer | Optimize execution. | Deployment plans, resource estimates, orchestration notes |
| Agent Operations Manager | Manage panel workload. | Workload reports, queue health, resource recommendations |

## Working Pattern

Start with a project charter. Identify the research question, theory of change, candidate data sources, expected outputs, and review gates. Put the charter in `documents/` and record any early assumptions in `ASSUMPTIONS.md`.

Move through the phases in `ROADMAP.md`. The phases are not a promise that the work is complete or correct; they are a checklist for what should exist before claims become stronger. A claim should not move from exploratory notes into a report or public artifact until it has evidence, citation review, skeptic review, and human review when required.

Use disagreement deliberately. The Skeptical Reviewer is not a blocker by
default; it is a structured way to find weak evidence, hidden assumptions, and
alternative explanations before they harden into project conclusions.

Use impact translation carefully. Societal relevance is not automatic just because a result is technically interesting. Claims about communities, Tribes, Indigenous knowledge, public health, law, or policy require human review and, when appropriate, additional domain or community review.
