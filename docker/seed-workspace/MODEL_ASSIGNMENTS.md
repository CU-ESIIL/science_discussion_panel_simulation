# MODEL_ASSIGNMENTS.md - Panel Model Routing

This register documents default model routes for the scientific discussion
panel. Do not store API keys, OAuth callback URLs, access tokens, refresh
tokens, provider secrets, or billing credentials here.

## Policy

- Preserve AI-VERDE as a first-class OpenAI-compatible provider.
- Keep the Interaction Agent, Moderator, and sensitive public summaries on a
  high-reliability route unless the human operator approves a change.
- Use open-model routes for bounded panelist, memory, literature, and experiment
  work after the route is evaluated for citations, uncertainty, and role limits.
- Never use an unevaluated model route for credential changes, external
  messaging, irreversible filesystem actions, public claims, or sensitive
  community, policy, health, legal, or sovereignty claims.
- Record route changes and failures in `DECISIONS.md` or
  `FACT_CHECKS/model_routing.md`.

## Assignment Table

| Role | Default route | AI-VERDE/open-model use | Notes |
| --- | --- | --- | --- |
| Interaction Agent | OpenAI/Codex OAuth or approved high-reliability route | Limited after approval | Human-facing memory retrieval and question queueing. Must not invent panel responses. |
| Moderator | Strong reasoning and long-context route | Limited after approval | Balances discussion, preserves disagreement, requests evidence. |
| Tanya Berger-Wolf simulated perspective | Strong reasoning route | Yes, after evaluation | Biodiversity observation and imageomics perspective. |
| Lauren Gillespie simulated perspective | Strong reasoning route | Yes, after evaluation | Dataset bias, multimodal models, transfer. |
| Jenna Kline simulated perspective | Strong reasoning route | Yes, after evaluation | Autonomous sensing and edge AI. |
| Justin Kitzes simulated perspective | Strong reasoning route | Yes, after evaluation | Acoustic monitoring and ecological inference pipeline. |
| Katherine Siegel simulated perspective | Strong reasoning route | Yes, after evaluation | Causal language, validity, and uncertainty scrutiny. |
| Ty Tuff simulated perspective | Strong reasoning route | Yes, after evaluation | Infrastructure, reproducibility, access, and open science. |
| Discussion Producer | Efficient planning route | Yes | Topic selection, balance, and cadence. |
| Evidence and Literature Curator | Citation-disciplined route | Yes, with source verification | Must not cite unverifiable sources. |
| Fact Checker | Strong verification route | Yes, with source verification | Labels claim status and appends corrections. |
| Experiment Steward | Coding-capable route | Yes | Bounded scripts only; approval for costly work. |
| Memory and Transcript Curator | Efficient summarization route | Yes | Summaries must link to original rounds. |
| Bias and Balance Reviewer | Strong review route | Yes | Flags false balance and missing perspectives. |

## AI-VERDE Configuration

Keep endpoint and credentials in `.env`, mounted secret files, GitHub Secrets,
self-hosted runner secrets, or Kubernetes Secrets. Do not copy values into
prompts, transcripts, CMS pages, logs, or markdown memory.

```dotenv
VERDE_LLM_BASE_URL=https://llm-api.cyverse.ai/v1
VERDE_LLM_API_KEY=
VERDE_LLM_API_KEY_FILE=
VERDE_LLM_DEFAULT_MODEL=
VERDE_LLM_PROVIDER_NAME=verde
OPENCLAW_MODEL=
OPENCLAW_DEFAULT_MODEL=
```

Validate configuration without printing secrets:

```bash
make check-secrets
```

If a safe model-list health check is used, print only endpoint presence,
credential source, HTTP status, and model count. Never print key contents.

## Evaluation Checklist

1. Run a bounded known-output task.
2. Check the role follows `AGENTS.md`.
3. Check source handling and citation discipline.
4. Check uncertainty language and refusal to impersonate real people.
5. Compare against the high-reliability route.
6. Record the result before promoting a route.

## Failure Modes

- Inventing citations, datasets, approvals, sources, or panel responses.
- Converting panel interpretation into evidence.
- Treating confidence text as calibrated uncertainty.
- Ignoring pause, budget, or approval controls.
- Using commercial providers as a silent fallback when AI-VERDE is configured.
