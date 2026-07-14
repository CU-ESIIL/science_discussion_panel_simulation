# Agent Team

ScienceClaw now seeds a Scientific Panel Digital Twin: a living scientific
organization designed to reason, document, critique, remember, and improve
shared understanding.

## Why This Structure Exists

Scientific synthesis needs memory, disagreement, provenance, structured
minutes, and review. A flat chat full of assistants can become noisy and hard
to trust. The digital twin gives each role a bounded purpose, expected outputs,
review requirements, and dashboard-compatible event metadata.

## Human-Facing Flow

1. The user talks to the PI Liaison.
2. The PI Liaison assigns each question to an owner or marks it unassigned.
3. Scientific roles contribute claims, counterarguments, evidence, uncertainty,
   norms, decisions, and action items.
4. The Discussion Intelligence Agent normalizes events for the dashboard.
5. The Decision Recorder updates decisions, dissent, owners, and deadlines.
6. Humans approve risky or public actions.

## Stable Principle

Agents may recommend. Humans approve.

This is especially important for publication, deletion, GitHub pushes, new
tools, new mounts, paid APIs, sensitive data, policy claims, public health
claims, or claims involving communities, Tribes, or Indigenous knowledge.

Routine Python package installs inside the running container do not need the
same approval ritual when they are needed for active analysis and are logged.
Durable dependency changes still belong in the repository so future containers
can reproduce the work.
