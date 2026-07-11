# Discussion Coding Protocol

This protocol tells panel agents how to record structured minutes that can feed
the public discussion dashboard after human review.

The goal is not to count every word. The goal is to preserve the shape of the
scientific conversation: what was discussed, what was ignored, where agreement
exists, where disagreement remains useful, what questions are unresolved, and
what the panel wants to examine next.

## When To Record An Event

Record a `DiscussionEvent` for every meaningful contribution:

- a new claim, question, proposal, decision, norm, action item, evidence note, or summary
- a clear agreement, disagreement, clarification, or unresolved issue
- a topic that was proposed but did not gain traction
- a change in the panel's understanding, priorities, or public-facing synthesis

Do not record repeated statements as new ideas. Link them to the earlier event
when the repetition matters.

## Agent Responsibilities

Each agent should:

1. Record a concise minute for every meaningful contribution.
2. Assign one or more topic tags.
3. Classify the contribution type.
4. Classify the stance.
5. Link the contribution to an existing question, decision, norm, action, or event when applicable.
6. Create a new topic only when no existing topic fits.
7. Preserve disagreement rather than forcing consensus.
8. Mark unresolved issues explicitly.
9. Record evidence references where available.
10. Record decisions only after the panel clearly accepts them.
11. Record proposed norms separately from adopted norms.
12. Summarize the discussion before the panel moves to a substantially different topic.
13. Avoid counting repeated statements as new ideas.
14. Distinguish low discussion volume from low importance.
15. Identify topics that were proposed but did not stimulate conversation.

## Event Shape

Use this shape for every event:

```ts
type DiscussionEvent = {
  id: string
  sessionId: string
  timestamp: string
  agentId: string
  agentName: string
  summary: string
  sourceText?: string
  topicTags: string[]
  stance: "agree" | "disagree" | "neutral" | "unresolved" | "clarification"
  contributionType:
    | "claim"
    | "evidence"
    | "question"
    | "proposal"
    | "decision"
    | "norm"
    | "action"
    | "summary"
  relatedEventIds?: string[]
  confidence?: number
  evidenceRefs?: string[]
  actionOwner?: string
  status?: string
}
```

## Tag Taxonomy

Use controlled tags where possible and allow emergent tags when the existing
taxonomy does not fit.

| Category | Example Tags |
| --- | --- |
| Scientific domain | ecology, biodiversity, species richness, mechanisms |
| Data | data quality, dataset bias, metadata, sampling gaps |
| Methods | benchmarks, interpretability, validation, uncertainty |
| Models | foundation models, forecasting, transfer, generalization |
| Infrastructure | container, GitHub, dashboard, automation, workers |
| Ethics | data sovereignty, community review, bias, accountability |
| Governance | approval gates, publication review, benchmark governance |
| Evidence | citation, evidence packet, provenance, fact check |
| Collaboration | norms, decision protocol, minority viewpoints |
| Decisions | accepted, revisiting, completed, proposed |
| Future work | deferred, needs evidence, assigned, unassigned |

Normalize near-duplicate tags before summarizing. For example, `data bias`,
`biased data`, and `dataset bias` should roll up to `dataset bias`.

## Publication Rules

- Keep raw source text private by default unless it is explicitly approved.
- Publish summaries, stance counts, decisions, norms, and reviewed excerpts.
- Mark synthetic panel material clearly.
- Do not publish secrets, OAuth callback codes, credentials, private data, or
  unreviewed sensitive claims.
- Preserve minority views and unresolved questions in the public summary.

## File Flow

1. Agents write structured minutes in the workspace.
2. The panel or Interaction Agent updates the latest-discussion brief.
3. A human reviews the brief and dashboard output.
4. Reviewed Markdown and static dashboard files are promoted into `docs/`.
5. GitHub Pages renders the public site from the repository.
