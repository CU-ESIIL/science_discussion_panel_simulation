#!/usr/bin/env python3
"""File-backed controls for the ScienceClaw scientific discussion panel."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STATE = {
    "status": "paused",
    "last_completed_round": None,
    "next_planned_round": None,
    "pending_user_questions": 0,
    "pending_research_tasks": 0,
    "pending_experiments": 0,
    "autorun": False,
    "budget_status": "not_configured",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def workspace_path(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def ensure_runtime(workspace: Path) -> Path:
    runtime = workspace / "runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    return runtime


def state_path(workspace: Path) -> Path:
    return ensure_runtime(workspace) / "panel_state.json"


def load_state(workspace: Path) -> dict:
    path = state_path(workspace)
    if not path.exists():
        return DEFAULT_STATE.copy()
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        state = DEFAULT_STATE.copy()
        state["state_warning"] = f"Invalid JSON in {path}; using safe defaults."
    merged = DEFAULT_STATE.copy()
    merged.update(state)
    return merged


def save_state(workspace: Path, state: dict) -> None:
    path = state_path(workspace)
    state["updated_at"] = now()
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_system_status(workspace, state)


def count_pending_questions(workspace: Path) -> int:
    questions = workspace / "QUESTIONS_FROM_USER.md"
    if not questions.exists():
        return 0
    return sum(1 for line in questions.read_text(encoding="utf-8").splitlines() if line.startswith("- [ ]"))


def write_system_status(workspace: Path, state: dict) -> None:
    path = workspace / "SYSTEM_STATUS.md"
    path.write_text(
        f"""# SYSTEM_STATUS.md - Panel Runtime Status

Last updated: {state.get('updated_at', now())}

| Field | Value |
| --- | --- |
| Panel state | {state.get('status', 'paused')} |
| Autorun enabled | {str(state.get('autorun', False)).lower()} |
| Last completed round | {state.get('last_completed_round') or 'none'} |
| Next planned round | {state.get('next_planned_round') or 'manual'} |
| Pending user questions | {state.get('pending_user_questions', 0)} |
| Pending research tasks | {state.get('pending_research_tasks', 0)} |
| Pending experiments | {state.get('pending_experiments', 0)} |
| Budget status | {state.get('budget_status', 'not_configured')} |

Use `make panel-pause`, `make panel-resume`, `make panel-round`, and
`make panel-queue QUESTION='...'` to control the local panel loop.
""",
        encoding="utf-8",
    )


def append_question(workspace: Path, question: str) -> None:
    path = workspace / "QUESTIONS_FROM_USER.md"
    if not path.exists():
        path.write_text("# QUESTIONS_FROM_USER.md - Human Question Queue\n\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- [ ] {now()} | priority: normal | status: queued | question: {question.strip()}\n"
        )


def status(workspace: Path) -> int:
    state = load_state(workspace)
    state["pending_user_questions"] = count_pending_questions(workspace)
    save_state(workspace, state)
    print(f"Panel state: {state['status']}")
    print(f"Pending user questions: {state['pending_user_questions']}")
    print(f"Last completed round: {state.get('last_completed_round') or 'none'}")
    print(f"Budget status: {state.get('budget_status', 'not_configured')}")
    return 0


def set_status(workspace: Path, value: str) -> int:
    state = load_state(workspace)
    state["status"] = value
    state["pending_user_questions"] = count_pending_questions(workspace)
    if value == "paused":
        state["pause_reason"] = "manual"
    save_state(workspace, state)
    print(f"Panel state set to {value}.")
    return 0


def queue_question(workspace: Path, question: str) -> int:
    if not question.strip():
        raise SystemExit("Question cannot be empty.")
    append_question(workspace, question)
    state = load_state(workspace)
    state["pending_user_questions"] = count_pending_questions(workspace)
    save_state(workspace, state)
    print("Queued question for the Interaction Agent and Moderator.")
    return 0


def summary(workspace: Path) -> int:
    path = workspace / "CURRENT_SYNTHESIS.md"
    if not path.exists():
        print("No current synthesis exists yet. Run `make demo` or `make panel-round`.")
        return 1
    print(path.read_text(encoding="utf-8").strip())
    return 0


def budget_check(workspace: Path) -> int:
    state = load_state(workspace)
    token_budget = os.environ.get("PANEL_DAILY_TOKEN_BUDGET", "").strip()
    compute_budget = os.environ.get("PANEL_DAILY_COMPUTE_BUDGET_MINUTES", "").strip()
    if not token_budget and not compute_budget:
        state["budget_status"] = "not_configured"
    else:
        state["budget_status"] = "configured"
    state["pending_user_questions"] = count_pending_questions(workspace)
    save_state(workspace, state)
    print(f"Budget status: {state['budget_status']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Control the local scientific discussion panel state.")
    parser.add_argument("command", choices=["status", "pause", "resume", "queue-question", "summary", "budget-check"])
    parser.add_argument("--workspace", default=os.environ.get("WORKSPACE_DIR", "workspace"))
    parser.add_argument("--question", default="")
    args = parser.parse_args()

    workspace = workspace_path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    if args.command == "status":
        return status(workspace)
    if args.command == "pause":
        return set_status(workspace, "paused")
    if args.command == "resume":
        return set_status(workspace, "running")
    if args.command == "queue-question":
        return queue_question(workspace, args.question)
    if args.command == "summary":
        return summary(workspace)
    if args.command == "budget-check":
        return budget_check(workspace)
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
