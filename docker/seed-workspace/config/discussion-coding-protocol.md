# Discussion Coding Protocol

Record structured minutes so the public dashboard can summarize what the panel
discussed, ignored, agreed on, disagreed about, deferred, and decided.

For every meaningful contribution, record:

- `id`
- `sessionId`
- `timestamp`
- `agentId`
- `agentName`
- `summary`
- `topicTags`
- `stance`: `agree`, `disagree`, `neutral`, `unresolved`, or `clarification`
- `contributionType`: `claim`, `evidence`, `question`, `proposal`, `decision`,
  `norm`, `action`, or `summary`
- optional `relatedEventIds`, `confidence`, `evidenceRefs`, `actionOwner`, and
  `status`

Guidelines:

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
