#!/usr/bin/env python3
"""Generate public discussion dashboard pages from structured panel minutes."""

from __future__ import annotations

import csv
import html
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Literal, TypedDict


Stance = Literal["agree", "disagree", "neutral", "unresolved", "clarification"]
ContributionType = Literal[
    "claim",
    "evidence",
    "question",
    "proposal",
    "decision",
    "norm",
    "action",
    "summary",
]


class DiscussionEvent(TypedDict, total=False):
    id: str
    sessionId: str
    timestamp: str
    agentId: str
    agentName: str
    summary: str
    sourceText: str
    topicTags: list[str]
    stance: Stance
    contributionType: ContributionType
    relatedEventIds: list[str]
    confidence: float
    evidenceRefs: list[str]
    actionOwner: str
    status: str


class TopicSummary(TypedDict):
    id: str
    label: str
    count: int
    stanceCounts: dict[str, int]
    agents: list[str]
    status: str


def load_minutes(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def session_minutes(data: dict[str, Any]) -> int:
    total = 0
    for session in data.get("sessions", []):
        if not session.get("endedAt"):
            continue
        total += int((parse_dt(session["endedAt"]) - parse_dt(session["startedAt"])).total_seconds() / 60)
    return total


def topic_lookup(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {topic["id"]: topic for topic in data.get("topics", [])}


def agent_lookup(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {agent["id"]: agent for agent in data.get("agents", [])}


def topic_summaries(data: dict[str, Any]) -> list[TopicSummary]:
    topics = topic_lookup(data)
    counts: Counter[str] = Counter()
    stances: dict[str, Counter[str]] = defaultdict(Counter)
    agents: dict[str, set[str]] = defaultdict(set)

    for event in data.get("events", []):
        for tag in event.get("topicTags", []):
            if tag not in topics:
                continue
            counts[tag] += 1
            stances[tag][event.get("stance", "neutral")] += 1
            agents[tag].add(event.get("agentName", event.get("agentId", "unknown")))

    summaries: list[TopicSummary] = []
    for topic_id, topic in topics.items():
        summaries.append(
            {
                "id": topic_id,
                "label": topic["label"],
                "count": counts[topic_id],
                "stanceCounts": dict(stances[topic_id]),
                "agents": sorted(agents[topic_id]),
                "status": topic.get("status", "unclassified"),
            }
        )
    return sorted(summaries, key=lambda item: (-item["count"], item["label"]))


def low_engagement_topics(data: dict[str, Any], threshold: int = 2) -> list[TopicSummary]:
    return [
        topic
        for topic in topic_summaries(data)
        if topic["count"] <= threshold or topic["status"] == "low engagement"
    ]


def participation_by_agent(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for agent in data.get("agents", []):
        rows[agent["id"]] = {
            "agentId": agent["id"],
            "agentName": agent["name"],
            "role": agent["role"],
            "contributions": 0,
            "questions": 0,
            "evidence": 0,
            "agreements": 0,
            "disagreements": 0,
            "decisions": 0,
            "actions": 0,
        }

    for event in data.get("events", []):
        row = rows.setdefault(
            event["agentId"],
            {
                "agentId": event["agentId"],
                "agentName": event.get("agentName", event["agentId"]),
                "role": "Unregistered",
                "contributions": 0,
                "questions": 0,
                "evidence": 0,
                "agreements": 0,
                "disagreements": 0,
                "decisions": 0,
                "actions": 0,
            },
        )
        row["contributions"] += 1
        if event.get("contributionType") == "question":
            row["questions"] += 1
        if event.get("contributionType") == "evidence":
            row["evidence"] += 1
        if event.get("stance") == "agree":
            row["agreements"] += 1
        if event.get("stance") == "disagree":
            row["disagreements"] += 1
        if event.get("contributionType") == "decision":
            row["decisions"] += 1
        if event.get("contributionType") == "action":
            row["actions"] += 1

    return sorted(rows.values(), key=lambda item: (-item["contributions"], item["agentName"]))


def metrics(data: dict[str, Any]) -> dict[str, Any]:
    events = data.get("events", [])
    active_topics = [topic for topic in topic_summaries(data) if topic["count"] > 0]
    stance_counts = Counter(event.get("stance", "neutral") for event in events)
    total = max(len(events), 1)
    return {
        "discussion_minutes": session_minutes(data),
        "contributions": len(events),
        "active_topics": len(active_topics),
        "low_engagement_topics": len(low_engagement_topics(data)),
        "unresolved_questions": len([q for q in data.get("openQuestions", []) if q.get("status") != "resolved"]),
        "decisions_made": len(data.get("decisions", [])),
        "agreement_rate": round(stance_counts["agree"] / total * 100),
        "disagreement_rate": round(stance_counts["disagree"] / total * 100),
    }


def stance_distribution_for_topic(data: dict[str, Any], topic_id: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for event in data.get("events", []):
        if topic_id in event.get("topicTags", []):
            counts[event.get("stance", "neutral")] += 1
    return counts


def events_for_topic(data: dict[str, Any], topic_id: str) -> list[DiscussionEvent]:
    return [event for event in data.get("events", []) if topic_id in event.get("topicTags", [])]


def pct(part: int, whole: int) -> int:
    if whole <= 0:
        return 0
    return round(part / whole * 100)


def md_escape(value: str) -> str:
    return value.replace("|", "\\|")


def metric_card(label: str, value: Any, note: str) -> str:
    return (
        '<div class="discussion-metric" title="'
        + html.escape(note)
        + '"><span>'
        + html.escape(str(label))
        + "</span><strong>"
        + html.escape(str(value))
        + "</strong></div>"
    )


def stance_bar(counts: Counter[str]) -> str:
    order = ["agree", "disagree", "neutral", "unresolved", "clarification"]
    total = sum(counts.values())
    if total == 0:
        return '<div class="stance-bar stance-bar--empty" aria-label="No recorded stances"></div>'
    segments = []
    for stance in order:
        width = pct(counts[stance], total)
        if width == 0:
            continue
        segments.append(
            f'<span class="stance-segment stance-{stance}" style="width:{width}%" title="{stance}: {counts[stance]}"></span>'
        )
    return '<div class="stance-bar" aria-label="Stance distribution">' + "".join(segments) + "</div>"


def render_topic_network(data: dict[str, Any]) -> str:
    summaries = topic_summaries(data)
    max_count = max((topic["count"] for topic in summaries), default=1)
    nodes = []
    for idx, topic in enumerate(summaries):
        status = topic["status"].replace(" ", "-")
        size = 0.86 + (topic["count"] / max_count) * 1.1
        nodes.append(
            '<a class="topic-node topic-node--'
            + html.escape(status)
            + '" href="#topic-'
            + html.escape(topic["id"])
            + '" style="--node-size:'
            + f"{size:.2f}"
            + '; --node-index:'
            + str(idx)
            + '"><strong>'
            + html.escape(topic["label"])
            + "</strong><span>"
            + str(topic["count"])
            + " events</span></a>"
        )
    return '<div class="topic-network" role="list">' + "".join(nodes) + "</div>"


def render_dashboard(data: dict[str, Any]) -> str:
    m = metrics(data)
    sessions = data.get("sessions", [])
    session = sessions[0] if sessions else {"title": "Discussion session", "summary": ""}
    topics = topic_summaries(data)
    low_topics = low_engagement_topics(data)
    future = data.get("futureQueue", [])

    metric_html = "\n".join(
        [
            metric_card("Discussion time", f"{m['discussion_minutes']} min", "Total elapsed session time"),
            metric_card("Contributions", m["contributions"], "Recorded structured discussion events"),
            metric_card("Active topics", m["active_topics"], "Topics with at least one event"),
            metric_card("Low engagement", m["low_engagement_topics"], "Topics with two or fewer events"),
            metric_card("Open questions", m["unresolved_questions"], "Questions not marked resolved"),
            metric_card("Decisions", m["decisions_made"], "Recorded decision register entries"),
            metric_card("Agreement", f"{m['agreement_rate']}%", "Share of events tagged as agreement"),
            metric_card("Disagreement", f"{m['disagreement_rate']}%", "Share of events tagged as disagreement"),
        ]
    )

    topic_rows = []
    max_topic_count = max((topic["count"] for topic in topics), default=1)
    for topic in topics:
        width = pct(topic["count"], max_topic_count)
        topic_rows.append(
            f'<div class="activity-row"><span>{html.escape(topic["label"])}</span>'
            f'<div class="activity-track"><b style="width:{width}%"></b></div>'
            f'<strong>{topic["count"]}</strong></div>'
        )

    topic_detail = []
    for topic in topics:
        counts = Counter(topic["stanceCounts"])
        events = events_for_topic(data, topic["id"])
        strongest = events[:3]
        topic_detail.append(
            f'<details class="topic-detail" id="topic-{html.escape(topic["id"])}">'
            f'<summary><strong>{html.escape(topic["label"])}</strong><span>{topic["count"]} events · {html.escape(topic["status"])}</span></summary>'
            + stance_bar(counts)
            + "<ul>"
            + "".join(f"<li>{html.escape(event['summary'])}</li>" for event in strongest)
            + "</ul>"
            + "<p><strong>Agents involved:</strong> "
            + html.escape(", ".join(topic["agents"]) or "No recorded agents")
            + "</p></details>"
        )

    question_rows = []
    topic_labels = {topic["id"]: topic["label"] for topic in data.get("topics", [])}
    agent_names = {agent["id"]: agent["name"] for agent in data.get("agents", [])}
    for question in data.get("openQuestions", []):
        involved = ", ".join(agent_names.get(agent_id, agent_id) for agent_id in question.get("agentIds", []))
        question_rows.append(
            "| "
            + md_escape(question["text"])
            + " | "
            + md_escape(topic_labels.get(question["topicId"], question["topicId"]))
            + " | "
            + str(question["mentions"])
            + " | "
            + question["priority"]
            + " | "
            + question["status"]
            + " | "
            + md_escape(involved)
            + " |"
        )

    decision_rows = []
    for decision in data.get("decisions", []):
        decision_rows.append(
            "| "
            + md_escape(decision["statement"])
            + " | "
            + md_escape(topic_labels.get(decision["topicId"], decision["topicId"]))
            + " | "
            + str(round(decision["confidence"] * 100))
            + "% | "
            + decision["status"]
            + " | "
            + md_escape(decision["owner"])
            + " | "
            + md_escape(decision["followUpAction"])
            + " |"
        )

    norm_cards = []
    for norm in data.get("norms", []):
        norm_cards.append(
            '<div class="norm-card"><strong>'
            + html.escape(norm["text"])
            + "</strong><span>"
            + html.escape(norm["status"])
            + " · "
            + html.escape(norm["adoptedAt"][:10])
            + "</span></div>"
        )

    future_cards = []
    for item in future:
        supporters = ", ".join(agent_names.get(agent_id, agent_id) for agent_id in item.get("supportingAgentIds", []))
        future_cards.append(
            '<div class="future-card"><strong>'
            + html.escape(item["title"])
            + "</strong><p>Raised by "
            + html.escape(item["raisedBy"])
            + "; supported by "
            + html.escape(supporters or "no additional agents")
            + ".</p><span>"
            + html.escape(item.get("owner") or "unassigned")
            + " · "
            + html.escape(item["status"])
            + "</span></div>"
        )

    participation_rows = []
    for row in participation_by_agent(data):
        participation_rows.append(
            "| "
            + md_escape(row["agentName"])
            + " | "
            + str(row["contributions"])
            + " | "
            + str(row["questions"])
            + " | "
            + str(row["evidence"])
            + " | "
            + str(row["agreements"])
            + " | "
            + str(row["disagreements"])
            + " | "
            + str(row["actions"])
            + " |"
        )

    timeline = []
    for event in sorted(data.get("events", []), key=lambda item: item["timestamp"]):
        timeline.append(
            '<div class="timeline-event"><time>'
            + html.escape(event["timestamp"][11:16])
            + "</time><strong>"
            + html.escape(event["agentName"])
            + "</strong><p>"
            + html.escape(event["summary"])
            + '</p><span class="event-pill">'
            + html.escape(event["stance"])
            + "</span><span class=\"event-pill\">"
            + html.escape(event["contributionType"])
            + "</span></div>"
        )

    return f"""# Discussion Dashboard

<section class="discussion-hero">
  <img src="../assets/panel/ecologists-meet-ai-hero.png" alt="Ecologists and AI researchers in a panel discussion at a science summit">
  <div>
    <p class="eyebrow">Conversation intelligence for the panel</p>
    <h2>{html.escape(session["title"])}</h2>
    <p>{html.escape(session.get("summary", ""))}</p>
    <div class="dashboard-actions">
      <a class="md-button md-button--primary" href="../data/discussion-minutes.mock.json">Export JSON</a>
      <a class="md-button" href="../data/discussion-events.csv">Export CSV</a>
      <a class="md-button" href="../reports/latest-discussion/">Latest brief</a>
      <a class="md-button" href="../discussion-coding-protocol/">Coding protocol</a>
    </div>
  </div>
</section>

<section class="discussion-filters" aria-label="Dashboard filters">
  <label>Session <select><option>{html.escape(session["title"])}</option></select></label>
  <label>Agent <select><option>All agents</option></select></label>
  <label>Topic <select><option>All topics</option></select></label>
  <label>Stance <select><option>All stances</option></select></label>
  <label>Event type <select><option>All event types</option></select></label>
</section>

<section class="discussion-metrics" aria-label="Summary metrics">
{metric_html}
</section>

## Discussion Landscape

Each topic node is sized by event volume. Color marks broad agreement, disagreement, unresolved status, or low engagement.

{render_topic_network(data)}

## Topic Activity

<div class="activity-board">
{''.join(topic_rows)}
</div>

### Topics That Did Not Gain Traction

{''.join(f'<span class="low-topic">{html.escape(topic["label"])} · {topic["count"]} events</span>' for topic in low_topics) or '<p class="empty-state">No low-engagement topics were recorded.</p>'}

## Agreement And Disagreement

{''.join(topic_detail)}

## Open Questions

| Question | Topic | Mentions | Priority | Status | Agents |
| --- | ---: | ---: | --- | --- | --- |
{chr(10).join(question_rows)}

## What The Panel Still Wants To Discuss

<div class="future-grid">
{''.join(future_cards)}
</div>

## Decisions Register

| Decision | Topic | Confidence | Status | Owner | Follow-up |
| --- | --- | ---: | --- | --- | --- |
{chr(10).join(decision_rows)}

## Group Norms

<div class="norm-grid">
{''.join(norm_cards)}
</div>

## Conversation Timeline

<div class="timeline-list">
{''.join(timeline)}
</div>

## Participation Overview

High volume is not automatically better participation. This table shows how the
work was distributed so the panel can see gaps and rebalance future rounds.

| Agent | Contributions | Questions | Evidence | Agreements | Disagreements | Actions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(participation_rows)}

## Architecture

This page is generated from `docs/data/discussion-minutes.mock.json` by
`scripts/discussion_dashboard.py`. Replace the mock data with reviewed panel
minutes that follow `config/discussion-event.schema.json`, run the generator,
review the Markdown, then publish through the normal docs workflow.
"""


def render_latest_discussion(data: dict[str, Any]) -> str:
    m = metrics(data)
    topics = topic_summaries(data)
    dominant = topics[0] if topics else {"label": "None", "count": 0}
    low = low_engagement_topics(data)
    questions = data.get("openQuestions", [])
    decisions = data.get("decisions", [])
    session = data.get("sessions", [{}])[0]

    return f"""# Latest Panel Discussion

!!! note "Reviewed public brief"
    This page is the public copy of the panel-updated latest-discussion brief.
    Agents should update the workspace source first; humans review before this
    page is promoted to the website.

## Session

**{session.get("title", "Discussion session")}**

{session.get("summary", "")}

## What Dominated

The most active topic was **{dominant["label"]}** with {dominant["count"]}
recorded events. Across the session, the panel recorded {m["contributions"]}
structured contributions over {m["discussion_minutes"]} minutes.

## What Did Not Go Far

{chr(10).join(f'- **{topic["label"]}**: {topic["count"]} recorded events' for topic in low) or 'No low-engagement topics were recorded.'}

## Current Consensus

- Evidence traceability should be a first-class norm for public summaries.
- Benchmark performance is useful evidence, but not a standalone definition of ecological discovery.
- Low discussion volume should not be interpreted as low importance.

## Remaining Disagreement

- The panel disagreed about how much benchmark performance can tell us about ecological mechanism.
- The panel has not resolved how to evaluate foundation-model claims against mechanistic baselines.
- Ethical and sovereignty concerns need to be represented in benchmark governance rather than handled after model evaluation.

## Open Questions

{chr(10).join(f'- **{q["priority"]}**: {q["text"]} ({q["status"]})' for q in questions)}

## Decisions And Follow-Up

{chr(10).join(f'- **{d["status"]}**: {d["statement"]} Follow-up: {d["followUpAction"]}' for d in decisions)}

## Dashboard

See the [discussion dashboard](../dashboard/discussion-dashboard.md) for topic
activity, stance distributions, open questions, future queue, decisions, group
norms, timeline, and participation overview.
"""


def write_csv(data: dict[str, Any], path: Path) -> None:
    fields = ["id", "sessionId", "timestamp", "agentId", "agentName", "summary", "topicTags", "stance", "contributionType", "status"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for event in data.get("events", []):
            writer.writerow({field: ",".join(event[field]) if field == "topicTags" else event.get(field, "") for field in fields})


def generate(
    data_path: Path = Path("docs/data/discussion-minutes.mock.json"),
    dashboard_path: Path = Path("docs/dashboard/discussion-dashboard.md"),
    latest_path: Path = Path("docs/reports/latest-discussion.md"),
    csv_path: Path = Path("docs/data/discussion-events.csv"),
) -> None:
    data = load_minutes(data_path)
    dashboard_path.write_text(render_dashboard(data), encoding="utf-8")
    latest_path.write_text(render_latest_discussion(data), encoding="utf-8")
    write_csv(data, csv_path)


def main() -> None:
    generate()


if __name__ == "__main__":
    main()
