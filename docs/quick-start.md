# Quick Start

Set up the OASIS Scientific Discussion Panel locally:

```bash
cp .env.example .env
make init-panel
make doctor
make build
make up
```

The panel starts paused/manual by default. Use:

```bash
make panel-status
make panel-queue QUESTION="Where does the panel disagree about AI for ecological discovery?"
make panel-round
make panel-summary
```

The deterministic demo does not require live API access:

```bash
make demo
```

It writes a synthetic discussion round and supporting records under
`workspace/DISCUSSION_ROUNDS/`, `workspace/EXPERIMENTS/`,
`workspace/FACT_CHECKS/`, and the current-state files in `workspace/`.

Open the file manager at `http://127.0.0.1:8090/files?path=/workspace` after
the Compose stack is running. OpenClaw dashboard links are printed by:

```bash
docker compose exec openclaw-local openclaw dashboard --no-open
```

For AI-VERDE and secret setup, see [AI-VERDE Configuration](ai-verde-configuration.md)
and [Secret Migration](secret-migration.md).
