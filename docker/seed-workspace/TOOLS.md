# TOOLS.md - Panel Tool Boundaries

| Tool or surface | Purpose | Boundary |
| --- | --- | --- |
| OpenClaw Gateway | Human-facing Moderator and panel runtime | Respect role prompts, approval gates, and model routing |
| Workspace files | Durable panel memory | Preserve append-only rounds and position history |
| CMS/file manager | Inspect panel memory and outputs | Do not expose secrets or blocked paths |
| GitHub manager | Authorized repository work | Use selected repos only; avoid direct pushes to protected branches |
| Slack | Optional Moderator intake and review surface | No arbitrary shell execution; approval gates still apply |
| AI-VERDE | First-class model provider | Configure via env or secret file; do not print keys |
| Kubernetes/worker jobs | Bounded experiments | Approval required for costly or long-running work |
