# Resource Limits

Defaults keep the panel bounded and manual:

```dotenv
SCIENCECLAW_CONTAINER_CPUS=2.0
SCIENCECLAW_CONTAINER_MEMORY=20g
PANEL_AUTORUN=0
PANEL_DISCUSSION_INTERVAL_MINUTES=60
PANEL_MAX_TURNS_PER_ROUND=12
PANEL_MAX_PANELISTS_PER_ROUND=4
PANEL_MAX_RESEARCH_TASKS_PER_ROUND=2
PANEL_MAX_EXPERIMENTS_PER_DAY=1
PANEL_REQUIRE_EXPERIMENT_APPROVAL=1
PANEL_DAILY_TOKEN_BUDGET=
PANEL_DAILY_COMPUTE_BUDGET_MINUTES=
PANEL_AUTO_SUMMARY_INTERVAL_ROUNDS=4
PANEL_REPETITION_THRESHOLD=0.82
PANEL_IDLE_WHEN_NO_TOPIC=1
PANEL_TIMEZONE=America/Denver
```

`SCIENCECLAW_CONTAINER_MEMORY` controls the Docker memory limit requested by
Compose for `openclaw-local`. Docker Desktop or the host Docker engine must also
be allowed that much memory. The default local example can use `20g`; larger
research or model-routing experiments should be increased deliberately.

`./data`, `./workspace`, and `./external_storage` are bind mounts on the host.
Compose does not enforce a 20 GiB disk quota for those folders; use host storage
policy or project-specific cleanup rules if you need a hard disk cap.

Enable autorun only deliberately. Use daily token and compute budgets for
unattended operation, and pause the panel when limits are reached.
