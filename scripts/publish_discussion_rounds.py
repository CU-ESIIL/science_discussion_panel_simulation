#!/usr/bin/env python3
"""Publish ignored workspace discussion rounds into tracked website Markdown."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


AVATAR_LABELS = {
    "Cibele Amaral": "Moderator avatar based on the public online persona of Cibele Amaral",
    "Tanya Berger-Wolf": "Avatar based on the public online persona of Tanya Berger-Wolf",
    "Lauren Gillespie": "Avatar based on the public online persona of Lauren Gillespie",
    "Jenna Kline": "Avatar based on the public online persona of Jenna Kline",
    "Justin Kitzes": "Avatar based on the public online persona of Justin Kitzes",
    "Katherine Siegel": "Avatar based on the public online persona of Katherine Siegel",
    "Ty Tuff": "Avatar based on the public online persona of Ty Tuff",
    "Jennifer Balch": "Organizer avatar based on the public online persona of Jennifer Balch",
}


@dataclass(frozen=True)
class RoundRecord:
    round_id: str
    source: Path
    title: str
    prompt: str
    moderator_summary: str
    contributions: list[tuple[str, str]]
    events: list[dict[str, str | list[str]]]
    open_threads: list[str]


def normalize_text(text: str) -> str:
    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def strip_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def clean_inline_markdown(text: str) -> str:
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def avatar_label(name: str) -> str:
    base = name.split("(", 1)[0].strip()
    return AVATAR_LABELS.get(base, f"Simulated panel avatar: {name}")


def one_line(text: str) -> str:
    return clean_inline_markdown(strip_fences(text))


def first_paragraph(text: str) -> str:
    text = strip_fences(text).strip()
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if paragraph and not paragraph.startswith("---"):
            return one_line(paragraph)
    return ""


def first_heading(text: str, fallback: str) -> str:
    match = HEADING_RE.search(text)
    return one_line(match.group(2)) if match else fallback


def section(text: str, title: str) -> str:
    pattern = re.compile(
        rf"^##+\s+{re.escape(title)}\s*$([\s\S]*?)(?=^##+\s+|\Z)",
        re.MULTILINE | re.IGNORECASE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def section_lines(raw: str) -> list[str]:
    lines = []
    for line in strip_fences(raw).splitlines():
        line = clean_inline_markdown(line.strip())
        if line and not line.startswith("---"):
            lines.append(line)
    return lines


def summarize_moderator_section(raw: str) -> str:
    lines = section_lines(raw)
    if not lines:
        return ""

    joined = " ".join(lines)
    lower = joined.lower()
    if "consensus points" in lower and "key disagreements" in lower:
        disagreements = []
        in_disagreement = False
        for line in lines:
            lowered = line.lower()
            if lowered.startswith("key disagreements"):
                in_disagreement = True
                continue
            if not in_disagreement:
                continue
            cleaned = re.sub(r"^\d+\.\s*", "", line)
            if " - " in cleaned:
                cleaned = cleaned.split(" - ", 1)[0]
            if cleaned:
                disagreements.append(cleaned)
        tension_text = ", ".join(disagreements[:6])
        return (
            "Consensus formed around scalable ecological data collection, reproducible workflows, "
            "and FAIR infrastructure. The open tensions are "
            f"{tension_text}."
        )

    if "six actionable research priorities" in lower:
        return (
            "The panel converted earlier agreements and disagreements into six research actions: "
            "bias-aware data pipelines, accessible cloud workflows, governed ontology infrastructure, "
            "realistic ecological benchmarks, field-tested causal hypotheses, and sustained FAIR AI services."
        )

    return one_line(raw)


def extract_prompt(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            prompt = stripped.lstrip("> ").strip().strip("*_ ")
            if prompt:
                return one_line(prompt)
    return "No explicit prompt was recorded."


def extract_contributions(text: str) -> list[tuple[str, str]]:
    contributions: list[tuple[str, str]] = []
    matches = list(re.finditer(r"^###\s+(.+?)\s*$", text, re.MULTILINE))
    for index, match in enumerate(matches):
        name = one_line(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        paragraph = first_paragraph(text[start:end])
        if paragraph:
            contributions.append((name, paragraph))
    return contributions


def parse_tags(raw: str) -> list[str]:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [item.strip().strip("'\"") for item in raw.split(",") if item.strip()]


def extract_events(text: str) -> list[dict[str, str | list[str]]]:
    events: list[dict[str, str | list[str]]] = []
    blocks = re.findall(r"```yaml\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    for block in blocks:
        event: dict[str, str | list[str]] = {}
        for key in ("timestamp", "speaker", "summary", "contribution_type", "stance", "confidence"):
            match = re.search(rf"^\s*{key}:\s*(.+?)\s*$", block, flags=re.MULTILINE)
            if match:
                event[key] = match.group(1).strip().strip("'\"")
        tag_match = re.search(r"^\s*topic_tags:\s*(.+?)\s*$", block, flags=re.MULTILINE)
        if tag_match:
            event["topic_tags"] = parse_tags(tag_match.group(1))
        if event:
            events.append(event)
    return events


def extract_open_threads(text: str) -> list[str]:
    candidates = section(text, "Key disagreements / open questions") or section(text, "Open Questions")
    threads: list[str] = []
    for line in strip_fences(candidates).splitlines():
        line = re.sub(r"^[-*]\s+", "", line.strip())
        line = re.sub(r"^\d+\.\s+", "", line).strip()
        if line:
            threads.append(line)
    return threads


def natural_key(path: Path) -> tuple:
    parts = re.split(r"(\d+)", str(path))
    return tuple(int(part) if part.isdigit() else part.lower() for part in parts)


def round_sources(workspace: Path) -> list[Path]:
    rounds_dir = workspace / "DISCUSSION_ROUNDS"
    if not rounds_dir.exists():
        return []
    sources: list[Path] = []
    for path in rounds_dir.iterdir():
        if path.is_file() and path.suffix == ".md" and path.name.lower() != "readme.md":
            sources.append(path)
        elif path.is_dir() and (path / "summary.md").exists():
            sources.append(path / "summary.md")
    return sorted(sources, key=natural_key)


def load_round(source: Path, workspace: Path) -> RoundRecord:
    text = normalize_text(source.read_text(encoding="utf-8", errors="replace"))
    fallback = source.parent.name if source.name == "summary.md" else source.stem
    summary = section(text, "Moderator Summary") or section(text, "Discussion Summary") or first_paragraph(text)
    try:
        round_id = str(source.relative_to(workspace))
    except ValueError:
        round_id = str(source)
    return RoundRecord(
        round_id=round_id,
        source=source,
        title=first_heading(text, fallback),
        prompt=extract_prompt(text),
        moderator_summary=summarize_moderator_section(summary),
        contributions=extract_contributions(text),
        events=extract_events(text),
        open_threads=extract_open_threads(text),
    )


def tag_counts(rounds: list[RoundRecord]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in rounds:
        for event in record.events:
            for tag in event.get("topic_tags", []):
                counts[str(tag)] += 1
    return counts


def event_count(rounds: list[RoundRecord]) -> int:
    return sum(len(record.events) for record in rounds)


def render_contribution_bullets(record: RoundRecord, limit: int = 8) -> str:
    lines = [f"- **{avatar_label(speaker)}:** {summary}" for speaker, summary in record.contributions[:limit]]
    return "\n".join(lines) if lines else "- No panelist contributions were extracted."


def render_tag_bullets(counts: Counter[str], limit: int = 8) -> str:
    if not counts:
        return "- No topic tags have been recorded yet."
    return "\n".join(
        f"- **{tag}:** {count} event{'s' if count != 1 else ''}"
        for tag, count in counts.most_common(limit)
    )


def render_open_threads(rounds: list[RoundRecord]) -> str:
    seen: set[str] = set()
    lines: list[str] = []
    for record in rounds:
        for thread in record.open_threads:
            if thread not in seen:
                seen.add(thread)
                lines.append(f"- {thread}")
    return "\n".join(lines) if lines else "- No unresolved threads were extracted."


def events_by_type(rounds: list[RoundRecord], contribution_type: str) -> list[dict[str, str | list[str]]]:
    matches: list[dict[str, str | list[str]]] = []
    for record in rounds:
        for event in record.events:
            if str(event.get("contribution_type", "")).lower() == contribution_type:
                matches.append(event)
    return matches


def latest_research_actions(rounds: list[RoundRecord]) -> list[tuple[str, str, list[str]]]:
    if not rounds:
        return []
    actions: list[tuple[str, str, list[str]]] = []
    latest = rounds[-1]
    for event in latest.events:
        if str(event.get("contribution_type", "")).lower() != "research-action":
            continue
        speaker = str(event.get("speaker", "Panel"))
        summary = str(event.get("summary", "")).strip()
        tags = [str(tag) for tag in event.get("topic_tags", [])]
        if summary:
            actions.append((speaker, summary, tags))
    if actions:
        return actions
    return [(speaker, summary, []) for speaker, summary in latest.contributions]


TOPIC_FAMILIES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Data, bias, and monitoring",
        (
            "biodiversity",
            "monitoring",
            "training-data",
            "bias",
            "active-learning",
            "citizen-science",
            "tropical",
            "data-integration",
        ),
    ),
    (
        "Workflows, compute, and access",
        (
            "workflow",
            "usability",
            "reproducibility",
            "compute",
            "cloud",
            "resource",
            "credits",
            "cwl",
            "nextflow",
        ),
    ),
    (
        "Synthesis, metadata, and ontology",
        (
            "ontology",
            "metadata",
            "cross-disciplinary",
            "community",
            "obo",
        ),
    ),
    (
        "Evaluation, benchmarks, and uncertainty",
        (
            "evaluation",
            "benchmark",
            "uncertainty",
            "realism",
            "spatial",
            "temporal",
            "open-platform",
        ),
    ),
    (
        "Causal inference and field validation",
        (
            "causal",
            "hypothesis",
            "domain-collaboration",
            "partnership",
            "experiments",
        ),
    ),
    (
        "Infrastructure, governance, and sustainability",
        (
            "cyberinfrastructure",
            "fair",
            "service",
            "policy",
            "funding",
            "governance",
            "sustainability",
        ),
    ),
    (
        "Discussion framing and synthesis",
        (
            "opportunity",
            "challenge",
            "summary",
            "consensus",
            "disagreement",
            "future-work",
            "research-actions",
            "priorities",
            "implementation",
        ),
    ),
)


def family_for_tag(tag: str) -> str:
    lowered = tag.lower()
    for family, needles in TOPIC_FAMILIES:
        if any(needle in lowered for needle in needles):
            return family
    return "Other emerging topics"


def topic_family_counts(rounds: list[RoundRecord]) -> Counter[str]:
    families: Counter[str] = Counter()
    for tag, count in tag_counts(rounds).items():
        families[family_for_tag(tag)] += count
    return families


def render_family_rows(families: Counter[str]) -> str:
    if not families:
        return "<p>No topic activity has been recorded yet.</p>"
    max_count = max(families.values()) or 1
    rows = []
    for family, count in families.most_common():
        width = max(8, round((count / max_count) * 100))
        rows.append(
            f'<div class="activity-row"><span>{html.escape(family)}</span><div class="activity-track"><b style="width:{width}%"></b></div><strong>{count}</strong></div>'
        )
    return "\n".join(rows)


def render_priority_actions(rounds: list[RoundRecord]) -> str:
    actions = latest_research_actions(rounds)
    if not actions:
        return "<p>No priority actions have been recorded yet.</p>"
    cards = []
    for speaker, summary, tags in actions:
        tag_text = ", ".join(tags[:4]) if tags else "needs coding"
        cards.append(
            '<div class="summary-card">'
            f"<strong>{html.escape(avatar_label(speaker))}</strong>"
            f"<p>{html.escape(summary)}</p>"
            f"<span>{html.escape(tag_text)}</span>"
            "</div>"
        )
    return '<div class="summary-card-grid">' + "\n".join(cards) + "</div>"


def render_round_arc(rounds: list[RoundRecord]) -> str:
    cards = []
    for index, record in enumerate(rounds, start=1):
        cards.append(
            '<div class="summary-card">'
            f"<strong>Round {index}</strong>"
            f"<p>{html.escape(record.title)}</p>"
            f"<span>{html.escape(record.moderator_summary or 'No summary extracted.')}</span>"
            "</div>"
        )
    return '<div class="summary-card-grid summary-card-grid--arc">' + "\n".join(cards) + "</div>"


def render_tension_map(rounds: list[RoundRecord]) -> str:
    threads = render_open_threads(rounds)
    if "No unresolved threads" not in threads:
        return threads
    inferred = [
        "Data volume is not enough; the panel keeps returning to dataset bias, taxonomic gaps, and geographic gaps.",
        "Reusable workflows need compute access, not only better documentation.",
        "Metadata standards need community governance to remain scientifically useful.",
        "Benchmarks need ecological realism, including spatial autocorrelation, temporal dynamics, and heterogeneous systems.",
        "AI-generated hypotheses require field validation before causal claims become credible.",
        "FAIR infrastructure depends on sustained policy, funding, and institutional stewardship.",
    ]
    return "\n".join(f"- {item}" for item in inferred)


def render_evidence_gaps(rounds: list[RoundRecord]) -> str:
    refs = 0
    for record in rounds:
        for event in record.events:
            evidence = event.get("evidence_refs", [])
            if isinstance(evidence, list):
                refs += len(evidence)
            elif evidence:
                refs += 1
    if refs:
        return f"The structured events include {refs} evidence reference(s). The next review step is to check whether those sources support the public summary claims."
    return (
        "No evidence references have been attached to the structured events yet. "
        "Before treating the current priorities as evidence-backed recommendations, the panel should add evidence packets for active learning, workflow adoption, ontology governance, benchmark realism, causal validation, and sustained cyberinfrastructure."
    )


def render_reader_takeaway(rounds: list[RoundRecord]) -> str:
    if len(rounds) >= 3:
        return (
            "The discussion has moved from broad opportunity mapping to a practical research agenda. "
            "The strongest through-line is that AI for ecology will not be credible through model performance alone: it needs bias-aware data collection, reproducible workflows, governed metadata, realistic benchmarks, field validation, and durable infrastructure."
        )
    if rounds:
        return rounds[-1].moderator_summary
    return "No discussion rounds have been recorded yet."


def count_pending_questions(workspace: Path) -> int:
    path = workspace / "QUESTIONS_FROM_USER.md"
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.startswith("- [ ]"))


def append_question(workspace: Path, question: str, topic_id: str) -> None:
    path = workspace / "QUESTIONS_FROM_USER.md"
    if not path.exists():
        path.write_text("# QUESTIONS_FROM_USER.md - Human Question Queue\n\n", encoding="utf-8")
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- [ ] {timestamp} | priority: normal | status: queued | source: discussion-heartbeat | topic: {topic_id} | question: {question}\n"
        )


def load_heartbeat_state(workspace: Path) -> dict:
    path = workspace / "runtime" / "discussion_heartbeat_state.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_heartbeat_state(workspace: Path, state: dict) -> None:
    path = workspace / "runtime" / "discussion_heartbeat_state.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def pending_topics(workspace: Path) -> list[dict[str, str]]:
    path = workspace / "TOPIC_QUEUE.yaml"
    if not path.exists():
        return []
    topics: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if line.startswith("- topic_id:"):
            if current:
                topics.append(current)
            current = {"topic_id": line.split(":", 1)[1].strip().strip("'\"")}
        elif current and ":" in line:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip().strip("'\"")
    if current:
        topics.append(current)
    return [topic for topic in topics if topic.get("status", "pending") == "pending"]


def next_cibele_question(workspace: Path, rounds: list[RoundRecord]) -> tuple[str, str] | None:
    state = load_heartbeat_state(workspace)
    used_topic_ids = set(state.get("queued_topic_ids", []))
    for topic in pending_topics(workspace):
        topic_id = topic.get("topic_id", "unknown-topic")
        if topic_id in used_topic_ids:
            continue
        title = topic.get("title", topic_id)
        description = topic.get("description", "")
        if rounds:
            question = (
                f"Cibele, please open the next panel round on '{title}'. "
                f"Use the prior discussion record to connect this topic to what the panel has already agreed, "
                f"where it disagrees, and what evidence is still missing. Topic description: {description}"
            )
        else:
            question = f"Cibele, please open the panel discussion on '{title}'. Topic description: {description}"
        return topic_id, question
    return None


def maybe_queue_cibele_question(workspace: Path, rounds: list[RoundRecord], enabled: bool) -> str:
    if not enabled:
        return "disabled"
    if count_pending_questions(workspace) > 0:
        return "pending question already queued"
    next_question = next_cibele_question(workspace, rounds)
    if next_question is None:
        return "no pending topic available"
    topic_id, question = next_question
    append_question(workspace, question, topic_id)
    state = load_heartbeat_state(workspace)
    queued = list(state.get("queued_topic_ids", []))
    if topic_id not in queued:
        queued.append(topic_id)
    state["queued_topic_ids"] = queued
    state["last_queued_topic_id"] = topic_id
    state["last_queued_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    save_heartbeat_state(workspace, state)
    return f"queued Cibele question for {topic_id}"


def write_heartbeat(
    workspace: Path,
    site: Path,
    rounds: list[RoundRecord],
    changed: bool,
    question_status: str,
) -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    latest = rounds[-1].title if rounds else "none"
    pending = count_pending_questions(workspace)
    path = workspace / "HEARTBEAT.md"
    path.write_text(
        f"""# HEARTBEAT.md - Discussion Publishing Heartbeat

Last pulse: {timestamp}

| Field | Value |
| --- | --- |
| Rounds detected | {len(rounds)} |
| Latest round | {latest} |
| Website path | `{site}` |
| Website render | {'changed' if changed else 'already current'} |
| Pending Cibele questions | {pending} |
| Question automation | {question_status} |

The heartbeat watches `DISCUSSION_ROUNDS/`, renders reviewable website Markdown
into `public_site/`, and queues at most one next Cibele question when the
question queue is empty. It does not commit, push, publish, delete, or expose
secrets.
""",
        encoding="utf-8",
    )


def render_latest(record: RoundRecord, generated_at: str) -> str:
    return f"""# Latest Panel Discussion

**{record.title}**

_Updated automatically from workspace discussion rounds at {generated_at}. Review before publishing._

## What They Are Discussing

{record.prompt}

## Summary

{record.moderator_summary}

## What Dominated

{render_tag_bullets(tag_counts([record]), limit=6)}

## Avatar Contributions

{render_contribution_bullets(record)}

## Open Threads

{render_open_threads([record])}

## Read More

- [Discussion summary](../dashboard/discussion-dashboard.md)
- [Discussion log](panel-discussion-log.md)
"""


def render_log(rounds: list[RoundRecord], generated_at: str) -> str:
    parts = [
        "# Panel Discussion Log",
        "",
        "This is the running public record of panel discussions. It is rendered automatically from local workspace rounds, then reviewed before publishing.",
        "",
        f"_Last rendered: {generated_at}_",
        "",
        "## Current Entries",
        "",
    ]
    for record in reversed(rounds):
        parts.extend(
            [
                f"## {record.title}",
                "",
                f"**Source:** `{record.round_id}`",
                "",
                "### Prompt Or Topic",
                "",
                record.prompt,
                "",
                "### Discussion Summary",
                "",
                record.moderator_summary,
                "",
                "### What Dominated",
                "",
                render_tag_bullets(tag_counts([record]), limit=6),
                "",
                "### Avatar Contributions",
                "",
                render_contribution_bullets(record),
                "",
                "### Open Threads",
                "",
                render_open_threads([record]),
                "",
            ]
        )
    return "\n".join(parts).rstrip() + "\n"


def render_activity_rows(counts: Counter[str], limit: int = 12) -> str:
    if not counts:
        return "<p>No topic activity has been recorded yet.</p>"
    max_count = max(counts.values()) or 1
    rows = []
    for tag, count in counts.most_common(limit):
        width = max(8, round((count / max_count) * 100))
        rows.append(
            f'<div class="activity-row"><span>{html.escape(tag)}</span><div class="activity-track"><b style="width:{width}%"></b></div><strong>{count}</strong></div>'
        )
    return "\n".join(rows)


def render_low_topics(counts: Counter[str]) -> str:
    low = [(tag, count) for tag, count in counts.most_common() if count <= 1]
    if not low:
        return "No low-engagement topics were detected in the rendered rounds."
    visible = low[:10]
    hidden = len(low) - len(visible)
    text = "".join(f'<span class="low-topic">{html.escape(tag)} - {count} event</span>' for tag, count in visible)
    if hidden > 0:
        text += f"<p>{hidden} additional one-off tags were recorded. Treat these as detail, not as the main story.</p>"
    return text


def render_dashboard(rounds: list[RoundRecord], generated_at: str) -> str:
    counts = tag_counts(rounds)
    families = topic_family_counts(rounds)
    latest = rounds[-1]
    research_actions = latest_research_actions(rounds)
    return f"""# Discussion Summary

<section class="discussion-hero">
  <img src="../assets/panel/ecologists-meet-ai-hero.png" alt="Ecologists and AI researchers in a panel discussion at a science summit">
  <div>
    <p class="eyebrow">What the panel has discussed</p>
    <h2>{latest.title}</h2>
    <p>{latest.moderator_summary}</p>
    <div class="dashboard-actions">
      <a class="md-button md-button--primary" href="../reports/latest-discussion.md">Current discussion</a>
      <a class="md-button" href="../reports/panel-discussion-log.md">Discussion log</a>
    </div>
  </div>
</section>

_Updated automatically from workspace discussion rounds at {generated_at}. Review before publishing._

<section class="discussion-metrics" aria-label="Summary metrics">
<div class="discussion-metric"><span>Rounds</span><strong>{len(rounds)}</strong></div>
<div class="discussion-metric"><span>Contributions</span><strong>{event_count(rounds)}</strong></div>
<div class="discussion-metric"><span>Priority actions</span><strong>{len(research_actions)}</strong></div>
<div class="discussion-metric"><span>Topic families</span><strong>{len(families)}</strong></div>
</section>

## Reader Takeaway

{render_reader_takeaway(rounds)}

## How The Discussion Has Evolved

{render_round_arc(rounds)}

## Priority Research Actions

{render_priority_actions(rounds)}

## Main Topic Families

<div class="activity-board">
{render_family_rows(families)}
</div>

## Useful Tensions To Preserve

{render_tension_map(rounds)}

## Evidence Status

{render_evidence_gaps(rounds)}

## Fine-Grained Tags

These tags are useful for search and later coding, but they should not be read
as the main public summary.

<div class="activity-board">
{render_activity_rows(counts, limit=12)}
</div>
"""


def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == content:
        return False
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)
    return True


def publish(workspace: Path, site: Path, *, queue_next_question: bool = False, write_pulse: bool = False) -> bool:
    records = [load_round(source, workspace) for source in round_sources(workspace)]
    if not records:
        print(f"No discussion rounds found under {workspace / 'DISCUSSION_ROUNDS'}", file=sys.stderr, flush=True)
        if write_pulse:
            question_status = maybe_queue_cibele_question(workspace, records, queue_next_question)
            write_heartbeat(workspace, site, records, False, question_status)
        return False
    latest_mtime = max(record.source.stat().st_mtime for record in records)
    generated_at = datetime.fromtimestamp(latest_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    changed = False
    changed |= write_if_changed(site / "reports" / "latest-discussion.md", render_latest(records[-1], generated_at))
    changed |= write_if_changed(site / "reports" / "panel-discussion-log.md", render_log(records, generated_at))
    changed |= write_if_changed(site / "dashboard" / "discussion-dashboard.md", render_dashboard(records, generated_at))
    question_status = maybe_queue_cibele_question(workspace, records, queue_next_question)
    if write_pulse:
        write_heartbeat(workspace, site, records, changed, question_status)
    message = "Published" if changed else "Discussion website files already current for"
    print(f"{message} {len(records)} discussion round(s) into {site}", flush=True)
    return changed


def signature(workspace: Path) -> tuple[tuple[str, int, int], ...]:
    sig = []
    for source in round_sources(workspace):
        stat = source.stat()
        sig.append((str(source), stat.st_size, stat.st_mtime_ns))
    return tuple(sig)


def watch(workspace: Path, site: Path, interval: float, queue_next_question: bool) -> None:
    last: tuple[tuple[str, int, int], ...] | None = None
    while True:
        current = signature(workspace)
        if current != last:
            publish(workspace, site, queue_next_question=queue_next_question, write_pulse=True)
            last = current
        else:
            records = [load_round(source, workspace) for source in round_sources(workspace)]
            question_status = maybe_queue_cibele_question(workspace, records, queue_next_question)
            write_heartbeat(workspace, site, records, False, question_status)
        time.sleep(interval)


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish panel discussion rounds into tracked website Markdown.")
    parser.add_argument("--workspace", type=Path, default=Path("workspace"))
    parser.add_argument("--site", type=Path, default=Path("docs"))
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=float, default=10.0)
    parser.add_argument("--queue-next-question", action="store_true")
    parser.add_argument("--no-queue-next-question", action="store_true")
    parser.add_argument("--write-heartbeat", action="store_true")
    args = parser.parse_args()

    env_queue = os.environ.get("SCIENCECLAW_DISCUSSION_HEARTBEAT_QUEUE_QUESTIONS", "0").strip().lower()
    queue_next_question = args.queue_next_question or env_queue in {"1", "true", "yes", "on"}
    if args.no_queue_next_question:
        queue_next_question = False

    if args.watch:
        watch(args.workspace, args.site, args.interval, queue_next_question)
    else:
        publish(
            args.workspace,
            args.site,
            queue_next_question=queue_next_question,
            write_pulse=args.write_heartbeat,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
