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

## Moderator Gateway

The user should not have to manage every agent by hand. The moderator avatar
based on the public online persona of Cibele Amaral turns a multi-agent
scientific panel into one coherent conversation.

The moderator avatar is the default human-facing role. It introduces topics,
asks the opening question, invites scientific avatars, asks follow-up questions,
summarizes transitions, and closes each discussion with a report path. The rest
of the panel communicates through structured discussion events, task
assignments, and memory files rather than competing for the user's attention.

When other agents need user input, they write questions in `QUESTIONS_FOR_USER.md`. Cibele deduplicates the queue, merges related questions, and asks only the highest-value followups. She returns milestone summaries, draft reports, and release packets to the user for review. She does not invent scientific goals or approve publication, deletion, GitHub pushes, external API use, or sensitive claims.

For Slack-connected use, the Moderator is the only Slack-facing component. Slack messages should enter queues and workspace memory before they are routed to the panel. Slack must never directly trigger arbitrary shell execution, and Slack tokens must stay in local environment variables rather than markdown, logs, screenshots, prompts, or git.

Operationally, Slack use has a few distinct gates: Socket Mode must be healthy, the Slack sender must be paired, and the running Gateway must have a fresh model login. Keep those checks separate when diagnosing failures. The reproducible command sequence is documented in the [Operations guide](operations.md).

## Role Summary

| Agent or avatar | Primary purpose | Main outputs |
| --- | --- | --- |
| Moderator avatar based on the public online persona of Cibele Amaral | Moderate discussion and human-facing flow. | Opening questions, transitions, summaries, report closure |
| Avatar based on the public online persona of Tanya Berger-Wolf | Represent biodiversity AI and scalable observation. | Biodiversity AI questions, observatory implications, data-scale challenges |
| Avatar based on the public online persona of Lauren Gillespie | Represent applied environmental AI and usable workflows. | Workflow notes, adoption risks, reproducibility needs |
| Avatar based on the public online persona of Jenna Kline | Represent ecological synthesis and cross-community integration. | Synthesis links, collaboration notes, integration gaps |
| Avatar based on the public online persona of Justin Kitzes | Represent computational ecology, validation, and reproducibility. | Benchmark critiques, uncertainty checks, validation needs |
| Avatar based on the public online persona of Katherine Siegel | Represent causal inference and scientific interpretation. | Causal assumptions, evidence designs, interpretation cautions |
| Avatar based on the public online persona of Ty Tuff | Represent cyberinfrastructure, multi-agent AI, and digital twins. | Infrastructure patterns, digital twin implications, synthesis-system notes |
| Organizer avatar based on the public online persona of Jennifer Balch | Organize themes and workshop alignment. | Topic proposals, schedule notes, report review comments |
| Discussion Intelligence Agent | Convert conversations into metadata. | Structured events, normalized tags, dashboard exports |

## Working Pattern

Start with a project charter. Identify the research question, theory of change, candidate data sources, expected outputs, and review gates. Put the charter in `documents/` and record any early assumptions in `ASSUMPTIONS.md`.

Move through the phases in `ROADMAP.md`. The phases are not a promise that the work is complete or correct; they are a checklist for what should exist before claims become stronger. A claim should not move from exploratory notes into a report or public artifact until it has evidence, citation review, skeptic review, and human review when required.

Use disagreement deliberately. Scientific avatars should respectfully challenge
assumptions, surface weak evidence, identify alternative explanations, and
preserve unresolved disagreement before it hardens into project conclusions.

Use impact translation carefully. Societal relevance is not automatic just because a result is technically interesting. Claims about communities, Tribes, Indigenous knowledge, public health, law, or policy require human review and, when appropriate, additional domain or community review.
