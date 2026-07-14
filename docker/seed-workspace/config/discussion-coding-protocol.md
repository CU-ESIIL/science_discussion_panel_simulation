# Discussion Coding Protocol

Record structured minutes so the Scientific Panel Dashboard can summarize what
the panel discussed, ignored, agreed on, disagreed about, deferred, decided,
normalized, and assigned.

Every meaningful contribution must be represented as a structured event. Raw
text alone is not enough.

## Required Fields

- `id`
- `sessionId`
- `timestamp`
- `agentId`
- `agentName`
- `summary`
- `topicTags`
- `normalizedTags`
- `contributionType`
- `stance`
- `question`
- `decision`
- `evidenceRefs`
- `uncertainty`
- `confidence`
- `norm`
- `actionItems`
- `relatedEventIds`
- `relatedQuestionIds`
- `relatedDecisionIds`
- `status`

## Contribution Types

- `Question`
- `Evidence`
- `Claim`
- `Proposal`
- `Counterargument`
- `Decision`
- `Summary`
- `Norm`
- `Action Item`

## Stance Values

- `agree`
- `disagree`
- `neutral`
- `unresolved`
- `clarification`
- `mixed`

## Confidence Values

Use `low`, `medium`, `high`, or `not-assessed`. Confidence is a panel judgment,
not calibrated statistical uncertainty unless explicitly supported.

## Tagging

Use `TAG_ONTOLOGY.md` for canonical categories. Normalize similar tags. Preserve
new proposed tags separately until reviewed by the Discussion Intelligence
Agent.

## Role Duties

1. PI Liaison ensures every question has an owner.
2. Scientific Director identifies emerging themes and future directions.
3. Domain Scientist records ecological assumptions and biological implications.
4. Quantitative Modeler records model, statistics, simulation, and uncertainty
   details.
5. Data Engineer / Infrastructure Scientist records data, metadata,
   reproducibility, and infrastructure implications.
6. Citation and Evidence Curator records evidence references and unsupported
   claims.
7. Skeptical Reviewer records counterarguments, assumptions, and failure modes.
8. Team Science Facilitator records participation and adopted norms.
9. Scientific Narrative Lead records conceptual evolution and story changes.
10. Societal Impact Agent records policy, ethics, stakeholder, and
    implementation implications.
11. Decision Recorder records accepted decisions, dissent, owners, and due
    dates.
12. Discussion Intelligence Agent converts contributions into dashboard-ready
    events.
13. Cloud Infrastructure Engineer records execution and resource implications.
14. Agent Operations Manager records workload, bottlenecks, idle agents, and
    resource reallocation.

## Guidelines

1. Preserve disagreement instead of forcing consensus.
2. Mark unresolved issues explicitly.
3. Record evidence references when available.
4. Record decisions only after the panel clearly accepts them.
5. Record proposed norms separately from adopted norms.
6. Avoid counting repeated statements as new ideas.
7. Distinguish low discussion volume from low importance.
8. Identify topics that were proposed but did not stimulate conversation.
9. Keep raw private source text out of public exports unless a human approves it.
10. Never record secrets, credentials, OAuth callbacks, or private data.
