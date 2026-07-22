# MODEL_ASSIGNMENTS.md - Scientific Panel Digital Twin Routing

This register documents default model routes for the Scientific Panel Digital
Twin. Do not store API keys, OAuth callback URLs, access tokens, refresh tokens,
provider secrets, or billing credentials here.

## Policy

- Route all panel roles to the approved AI-VERDE provider by default, per human
  operator approval on 2026-07-13.
- Treat `verde/js2/gpt-oss-120b` as the default route for every Scientific
  Panel Digital Twin role.
- Keep `SCIENCECLAW_VERDE_ONLY_MODE=1` enabled for local runs so persisted
  OpenAI/Codex routes are removed from the default agent allowlist on startup.
- Simulated named roles must represent public expertise and scientific
  perspectives only; they must not imitate private views or personal identity.
- Keep human review gates for public summaries, sensitive claims, credential
  changes, filesystem changes, GitHub pushes, costly work, external messaging,
  and billed actions.
- Record route changes and failures in `DECISIONS.md` or
  `FACT_CHECKS/model_routing.md`.

## Assignment Table

| Agent | OpenClaw id | Default route | Notes |
| --- | --- | --- | --- |
| Cibele Amaral (Moderator) | `main` | `verde/js2/gpt-oss-120b` | Introduces topics, asks opening and follow-up questions, balances participation, summarizes transitions, and closes reports. |
| Tanya Berger-Wolf | `tanya-berger-wolf` | `verde/js2/gpt-oss-120b` | Represents public expertise in biodiversity AI, computer vision, foundation models, wildlife monitoring, and ecological observatories. |
| Lauren Gillespie | `lauren-gillespie` | `verde/js2/gpt-oss-120b` | Represents public expertise in applied environmental AI, workflow development, usable infrastructure, reproducibility, and adoption. |
| Jenna Kline | `jenna-kline` | `verde/js2/gpt-oss-120b` | Represents public expertise in ecological synthesis, working groups, cross-disciplinary collaboration, and scientific integration. |
| Justin Kitzes | `justin-kitzes` | `verde/js2/gpt-oss-120b` | Represents public expertise in computational ecology, machine learning, statistics, scientific software, benchmarking, and uncertainty. |
| Katherine Siegel | `katherine-siegel` | `verde/js2/gpt-oss-120b` | Represents public expertise in causal inference, scientific reasoning, model interpretation, experimental design, and assumptions. |
| Ty Tuff | `ty-tuff` | `verde/js2/gpt-oss-120b` | Represents public expertise in scientific cyberinfrastructure, multi-agent AI, environmental data science, digital twins, and synthesis systems. |
| Jennifer Balch (Organizer) | `jennifer-balch` | `verde/js2/gpt-oss-120b` | Selects themes, proposes questions, reviews final reports, aligns workshop goals, schedules sessions, and identifies external experts. |
| Discussion Intelligence Agent | `discussion-intelligence-agent` | `verde/js2/gpt-oss-120b` | Codes statements into structured dashboard-ready metadata and tracks agreement, disagreement, assumptions, evidence gaps, and future work. |

## AI-VERDE Configuration

Keep endpoint and credentials in `.env`, mounted secret files, GitHub Secrets,
self-hosted runner secrets, or Kubernetes Secrets. Do not copy values into
prompts, transcripts, CMS pages, logs, or markdown memory.

```dotenv
VERDE_LLM_BASE_URL=https://llm-api.cyverse.ai/v1
VERDE_LLM_API_KEY=
VERDE_LLM_API_KEY_FILE=
VERDE_LLM_DEFAULT_MODEL=js2/gpt-oss-120b
VERDE_LLM_PROVIDER_NAME=verde
OPENCLAW_MODEL=verde/js2/gpt-oss-120b
OPENCLAW_DEFAULT_MODEL=verde/js2/gpt-oss-120b
```

Validate configuration without printing secrets:

```bash
make check-secrets
```

If a safe model-list health check is used, print only endpoint presence,
credential source, HTTP status, and model count. Never print key contents.

## Evaluation Checklist

1. Run a bounded known-output task.
2. Check that the role follows `AGENTS.md`.
3. Check source handling and citation discipline.
4. Check uncertainty language and refusal to overclaim.
5. Check structured event output against `DISCUSSION_EVENT_TEMPLATE.md`.
6. Compare against another approved route only when diagnosing regressions.
7. Record the result before promoting a route.
