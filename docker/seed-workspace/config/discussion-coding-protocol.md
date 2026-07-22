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

1. Cibele Amaral introduces topics, asks opening and follow-up questions,
   balances participation, summarizes transitions, and closes each discussion.
2. Tanya Berger-Wolf records biodiversity AI, observation-scale, computer
   vision, wildlife monitoring, foundation-model, and ecological observatory
   implications.
3. Lauren Gillespie records applied workflow, usable infrastructure,
   reproducibility, operational science, implementation, and adoption
   implications.
4. Jenna Kline records synthesis, cross-disciplinary collaboration, working
   group, integration, and scientific-process implications.
5. Justin Kitzes records computational ecology, benchmarking, validation,
   uncertainty, statistical rigor, and reproducibility implications.
6. Katherine Siegel records causal inference, interpretation, assumption,
   evidence-design, counterfactual, and uncertainty implications.
7. Ty Tuff records cyberinfrastructure, multi-agent AI, environmental data
   science, digital twin, synthesis-system, and future operating-system
   implications.
8. Jennifer Balch records theme selection, workshop alignment, scheduling, final
   report review, and external-expert needs between panel discussions.
9. Discussion Intelligence Agent converts contributions into dashboard-ready
   events and continuously tracks agreement, disagreement, assumptions, evidence
   gaps, competing hypotheses, future research priorities, related norms, and
   action items.

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
