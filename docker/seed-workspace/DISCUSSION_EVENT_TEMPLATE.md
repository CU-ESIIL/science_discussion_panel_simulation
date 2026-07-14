# DISCUSSION_EVENT_TEMPLATE.md

Use this template for each dashboard-ready structured event. The Discussion
Intelligence Agent may emit JSON, YAML, CSV, or another structured form, but the
fields below are required for meaningful contributions.

```yaml
id:
session_id:
timestamp:
speaker:
agent_id:
summary:
topic_tags: []
normalized_tags: []
proposed_tags: []
contribution_type:
stance:
question:
decision:
evidence_refs: []
uncertainty:
confidence:
norm:
action_items:
  - owner:
    task:
    due:
    status:
related_questions: []
related_decisions: []
related_events: []
dashboard_visibility: internal
```

Allowed `contribution_type` values:

- Question
- Evidence
- Claim
- Proposal
- Counterargument
- Decision
- Summary
- Norm
- Action Item

Allowed `stance` values:

- agree
- disagree
- neutral
- unresolved
- clarification
- mixed

Use `dashboard_visibility: public` only after human review.
