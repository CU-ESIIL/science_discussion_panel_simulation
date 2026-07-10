#!/usr/bin/env python3
"""Run a deterministic synthetic panel discussion demo.

The fixture text is synthetic and does not represent the private views of any
real person. It is designed to prove that panel memory, disagreement tracking,
fact-check requests, experiment records, and summaries can be written without
network access or live model credentials.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import panel_control


TOPIC_ID = "esa-q2-prediction-vs-discovery"
TOPIC_TITLE = "Does predictive accuracy constitute ecological discovery?"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def next_round_id(rounds_dir: Path) -> str:
    rounds_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(path.name for path in rounds_dir.iterdir() if path.is_dir() and path.name.startswith("round-"))
    return f"round-{len(existing) + 1:03d}"


def ensure_dirs(workspace: Path) -> None:
    for rel in [
        "DISCUSSION_ROUNDS",
        "POSITION_HISTORY",
        "LITERATURE/evidence_packets",
        "EXPERIMENTS/proposals",
        "EXPERIMENTS/results",
        "FACT_CHECKS",
        "DAILY_SYNTHESIS",
        "logs",
        "runtime",
    ]:
        (workspace / rel).mkdir(parents=True, exist_ok=True)


def calibration_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for i in range(1, 11):
        confidence = i / 10
        observed = max(0.0, min(1.0, 0.08 + 0.78 * confidence + 0.07 * math.sin(i)))
        rows.append(
            {
                "bin": i,
                "mean_confidence": round(confidence, 2),
                "observed_frequency": round(observed, 3),
                "absolute_gap": round(abs(confidence - observed), 3),
            }
        )
    return rows


def write_seed_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def write_demo(workspace: Path) -> str:
    ensure_dirs(workspace)
    round_id = next_round_id(workspace / "DISCUSSION_ROUNDS")
    round_dir = workspace / "DISCUSSION_ROUNDS" / round_id
    round_dir.mkdir(parents=True, exist_ok=False)

    evidence_packet = f"""# Evidence Packet - {TOPIC_TITLE}

Fixture status: synthetic demonstration packet.
Search date: not applicable; no network or live literature search was used.

## Structured Claims

| Claim | Evidence type | Status |
| --- | --- | --- |
| Predictive accuracy can reveal useful ecological regularities. | Panel interpretation from fixture text | unverified |
| Accuracy alone does not identify mechanism or causality. | Methodological principle represented in fixture text | requires citation before external use |
| Benchmark success may not transfer across taxa, regions, sensors, or social contexts. | Panel interpretation from fixture text | requires literature review |

## Citation Placeholder

- id: synthetic-demo-methods-note
  type: fixture
  title: Synthetic demonstration of panel evidence structure
  evidence_strength: demonstration only
"""
    (round_dir / "evidence_packet.md").write_text(evidence_packet, encoding="utf-8")
    (workspace / "LITERATURE" / "evidence_packets" / f"{round_id}.md").write_text(evidence_packet, encoding="utf-8")

    openings = """# Opening Positions

All statements below are synthetic fixture text for an operational demo.

## Tanya Berger-Wolf Simulated Perspective

Predictive accuracy can matter when it connects observations to individuals,
populations, traits, or conservation action. I would not call a leaderboard
score discovery unless it changes the ecological question we can answer.

## Lauren Gillespie Simulated Perspective

Accuracy needs a missing-data audit. If the benchmark overrepresents a few
places, seasons, or image styles, the result may be a brittle shortcut rather
than transferable ecological knowledge.

## Jenna Kline Simulated Perspective

The sensing process is part of the claim. A model can look accurate because the
drone, camera, microphone, or edge filter sampled only easy contexts.

## Justin Kitzes Simulated Perspective

A detector is not an ecological inference pipeline by itself. False positives,
false negatives, annotation burden, and reproducible workflows decide whether a
prediction supports discovery.

## Katherine Siegel Simulated Perspective

Prediction is not explanation. Accuracy can motivate hypotheses, but causal or
mechanistic claims need explicit assumptions, study design, and falsification.

## Ty Tuff Simulated Perspective

Discovery also depends on the system around the model: provenance, training,
open workflows, infrastructure access, and whether ecologists can reproduce the
result outside one lab.
"""
    (round_dir / "opening_positions.md").write_text(openings, encoding="utf-8")

    transcript = """# Moderated Exchange

Fixture status: synthetic.

Moderator: The panel agrees that accuracy can be useful, but not sufficient. I
want Katherine to respond directly to Tanya: when does prediction become a
scientific lead rather than merely a tool?

Katherine Siegel simulated perspective: It becomes a lead when the prediction
is tied to a testable contrast. If the model says traits, places, or behaviors
matter, the next step is a design that could show the apparent relationship is
not just confounding or selection.

Tanya Berger-Wolf simulated perspective: I agree on the need for tests. I would
add that individual-level recognition and imageomics can create variables that
were previously unavailable, which may make those tests possible.

Justin Kitzes simulated perspective: The same caution applies in acoustics. A
bird-call classifier can create scale, but occupancy or abundance still depends
on the detection process and sampling design.

Lauren Gillespie simulated perspective: And scale may amplify bias. If volunteer
observations are unevenly distributed, the model may learn visibility and access
patterns alongside biology.

Jenna Kline simulated perspective: Hardware choices can create the same problem.
Edge AI that filters observations before storage must be audited, or the missing
data become invisible.

Ty Tuff simulated perspective: The operational answer is to preserve the
pipeline: data provenance, model version, prompt or code, uncertainty, and the
human decision that promoted a claim.
"""
    (round_dir / "exchange_transcript.md").write_text(transcript, encoding="utf-8")

    fact_check = f"""# Fact Check Request - {round_id}

Date: {now()}
Requester: Moderator
Claim: Accuracy alone does not establish ecological mechanism or causality.
Status: unverified
Needed: Add methodological citations distinguishing prediction, explanation,
causal identification, and external validity before using this in public copy.
"""
    (round_dir / "fact_checks.md").write_text(fact_check, encoding="utf-8")
    (workspace / "FACT_CHECKS" / f"{round_id}.md").write_text(fact_check, encoding="utf-8")

    rows = calibration_rows()
    result_json = {
        "title": "Synthetic uncertainty calibration demonstration",
        "question": "Can high accuracy still hide calibration error?",
        "hypothesis": "A model can rank cases well while confidence remains miscalibrated.",
        "proposer": "Experiment Steward",
        "reviewer": "Katherine Siegel simulated perspective",
        "data_source": "Synthetic fixture generated by scripts/demo_panel_discussion.py",
        "code_path": "scripts/demo_panel_discussion.py",
        "environment": "local Python, no network access",
        "compute_estimate": "less than 1 second CPU",
        "approval_status": "pre-approved deterministic smoke-test fixture",
        "stopping_rule": "write ten synthetic bins and stop",
        "result": rows,
        "uncertainty": "demonstration only",
        "limitations": "Not ecological data; illustrates record structure only.",
        "discussion_impact": "Panel keeps the distinction between prediction quality and inference validity explicit.",
        "reproducibility_command": "make demo",
    }
    result_path = workspace / "EXPERIMENTS" / "results" / f"{round_id}_calibration_demo.json"
    result_path.write_text(json.dumps(result_json, indent=2) + "\n", encoding="utf-8")
    (round_dir / "experiment_result.json").write_text(json.dumps(result_json, indent=2) + "\n", encoding="utf-8")

    summary = f"""# Round Summary - {TOPIC_TITLE}

Round: {round_id}
Date: {now()}
Fixture status: synthetic demonstration text.

## Agreements

- Predictive accuracy can be useful evidence, especially when it enables new observations or scale.
- Accuracy alone is not sufficient for ecological discovery, explanation, or causal claims.
- Sampling design, sensor behavior, dataset bias, and reproducibility determine how much confidence the panel should place in a model result.

## Disagreement Preserved

Tanya's simulated perspective gives more weight to AI systems that create new
biological observables, while Katherine's simulated perspective keeps the bar
for explanation and causality higher. The panel did not force consensus.

## Unresolved Questions

- What evidence distinguishes ecological discovery from automated pattern recognition?
- Which benchmark designs best test transfer across ecosystems, taxa, sensors, and social contexts?
- When does a simple baseline outperform a complex AI model?

## Position Changes

No prior position was overwritten. This round creates an initial append-only
position history entry.
"""
    (round_dir / "summary.md").write_text(summary, encoding="utf-8")
    (workspace / "CURRENT_SYNTHESIS.md").write_text(summary, encoding="utf-8")
    (workspace / "DAILY_SYNTHESIS" / f"{round_id}.md").write_text(summary, encoding="utf-8")

    current_positions = f"""# CURRENT_POSITIONS.md - Current Panel Positions

Last updated: {now()}

| Panelist | Topic | Current position | Confidence | Evidence basis | History |
| --- | --- | --- | --- | --- | --- |
| Tanya Berger-Wolf simulated perspective | {TOPIC_TITLE} | Accuracy matters when it creates biologically meaningful observables linked to individuals, populations, traits, or conservation outcomes. | medium | synthetic fixture round | POSITION_HISTORY/{round_id}.md |
| Lauren Gillespie simulated perspective | {TOPIC_TITLE} | Accuracy must be interpreted through representativeness, transfer, and hidden dataset bias. | medium | synthetic fixture round | POSITION_HISTORY/{round_id}.md |
| Jenna Kline simulated perspective | {TOPIC_TITLE} | Sensing design and edge filtering shape what accuracy means. | medium | synthetic fixture round | POSITION_HISTORY/{round_id}.md |
| Justin Kitzes simulated perspective | {TOPIC_TITLE} | Detection accuracy is only one component of ecological inference. | medium | synthetic fixture round | POSITION_HISTORY/{round_id}.md |
| Katherine Siegel simulated perspective | {TOPIC_TITLE} | Prediction does not equal explanation or causal identification. | high | synthetic fixture round | POSITION_HISTORY/{round_id}.md |
| Ty Tuff simulated perspective | {TOPIC_TITLE} | Reproducible infrastructure and transparent provenance are part of whether AI can support discovery. | medium | synthetic fixture round | POSITION_HISTORY/{round_id}.md |
"""
    (workspace / "CURRENT_POSITIONS.md").write_text(current_positions, encoding="utf-8")
    (workspace / "POSITION_HISTORY" / f"{round_id}.md").write_text(current_positions, encoding="utf-8")

    disagreement = f"""# DISAGREEMENT_MAP.md - Current Disagreements

Last updated: {now()}

## Predictive Accuracy Versus Ecological Discovery

| Position | Panelists | Strongest current support | What could resolve it |
| --- | --- | --- | --- |
| Accuracy can create new ecological observables and therefore seed discovery. | Tanya, Ty | Individual recognition, imageomics, scalable monitoring workflows. | Case studies linking predictions to validated ecological mechanisms or decisions. |
| Accuracy is not discovery without design, transfer checks, and explicit assumptions. | Katherine, Lauren, Justin, Jenna | Confounding, distribution shift, detection error, and sensor-selection concerns. | Benchmarks and studies that test mechanism, transportability, and uncertainty calibration. |

Minority positions are preserved until evidence changes them.
"""
    (workspace / "DISAGREEMENT_MAP.md").write_text(disagreement, encoding="utf-8")

    evidence_ledger_path = workspace / "EVIDENCE_LEDGER.yaml"
    evidence_ledger_entry = f"""  - id: claim-{round_id}-001
    claim: "Predictive accuracy can reveal useful ecological regularities."
    source: "DISCUSSION_ROUNDS/{round_id}/opening_positions.md"
    evidence_strength: "panel interpretation; demonstration only"
    verification_status: "unverified"
    topics: ["{TOPIC_ID}"]
    relevant_panelists: ["tanya_berger_wolf", "ty_tuff"]
  - id: claim-{round_id}-002
    claim: "Accuracy alone does not identify mechanism or causality."
    source: "DISCUSSION_ROUNDS/{round_id}/fact_checks.md"
    evidence_strength: "methodological principle; citation needed"
    verification_status: "fact_check_requested"
    topics: ["{TOPIC_ID}"]
    relevant_panelists: ["katherine_siegel", "lauren_gillespie", "justin_kitzes"]
"""
    if not evidence_ledger_path.exists() or evidence_ledger_path.read_text(encoding="utf-8").strip() in {"", "claims: []"}:
        evidence_ledger_path.write_text("# EVIDENCE_LEDGER.yaml\nclaims:\n" + evidence_ledger_entry, encoding="utf-8")
    else:
        with evidence_ledger_path.open("a", encoding="utf-8") as handle:
            handle.write(evidence_ledger_entry)

    index = workspace / "DISCUSSION_INDEX.md"
    if not index.exists():
        index.write_text("# DISCUSSION_INDEX.md - Discussion Index\n\n", encoding="utf-8")
    with index.open("a", encoding="utf-8") as handle:
        handle.write(f"- {now()} | {round_id} | {TOPIC_ID} | {TOPIC_TITLE}\n")

    interaction_summary = f"""# Interaction Agent Summary

Fixture status: synthetic.

The panel discussed whether predictive accuracy constitutes ecological
discovery. The strongest shared conclusion is that accuracy can support
discovery when it enables new ecological observations or hypotheses, but it
does not by itself establish mechanism, causality, transferability, or validity.

Source round: `DISCUSSION_ROUNDS/{round_id}/summary.md`
"""
    (round_dir / "interaction_agent_summary.md").write_text(interaction_summary, encoding="utf-8")

    state = panel_control.load_state(workspace)
    state["last_completed_round"] = round_id
    state["pending_user_questions"] = panel_control.count_pending_questions(workspace)
    state["pending_experiments"] = 0
    state["pending_research_tasks"] = 1
    panel_control.save_state(workspace, state)
    return round_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the deterministic panel discussion demo.")
    parser.add_argument("--workspace", default="workspace")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    write_seed_if_missing(
        workspace / "PANEL_BRIEF.md",
        "# PANEL_BRIEF.md - Scientific Discussion Panel Brief\n\n"
        "Purpose: Maintain an ongoing evidence-based conversation about AI for Ecology.\n",
    )
    round_id = write_demo(workspace)
    print(f"Deterministic panel demo wrote synthetic round {round_id} to {workspace / 'DISCUSSION_ROUNDS' / round_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
