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
- Keep human review gates for public summaries, sensitive claims, credential
  changes, filesystem changes, GitHub pushes, costly work, external messaging,
  and billed actions.
- Record route changes and failures in `DECISIONS.md` or
  `FACT_CHECKS/model_routing.md`.

## Assignment Table

| Role | Default route | Notes |
| --- | --- | --- |
| PI Liaison | `verde/js2/gpt-oss-120b` | Coordinates discussion, assigns questions, manages transitions, and summarizes for the user. |
| Scientific Director | `verde/js2/gpt-oss-120b` | Maintains scientific vision, identifies breakthroughs, and connects themes. |
| Domain Scientist | `verde/js2/gpt-oss-120b` | Evaluates ecological realism, assumptions, literature, and biological implications. |
| Quantitative Modeler | `verde/js2/gpt-oss-120b` | Develops models, evaluates statistics, uncertainty, simulations, scaling, and performance. |
| Data Engineer / Infrastructure Scientist | `verde/js2/gpt-oss-120b` | Owns data architecture, metadata, APIs, reproducibility, storage, and efficiency. |
| Citation and Evidence Curator | `verde/js2/gpt-oss-120b` | Tracks citations, verifies claims, maintains bibliography, and estimates evidence confidence. |
| Skeptical Reviewer | `verde/js2/gpt-oss-120b` | Challenges ideas constructively, identifies assumptions, and tests robustness. |
| Team Science Facilitator | `verde/js2/gpt-oss-120b` | Monitors participation, dominance, quiet voices, norms, and psychological safety. |
| Scientific Narrative Lead | `verde/js2/gpt-oss-120b` | Maintains discussion summaries, conceptual evolution, manuscript language, figures, and key messages. |
| Societal Impact Agent | `verde/js2/gpt-oss-120b` | Reviews policy, management, stakeholder, ethics, communication, and implementation implications. |
| Decision Recorder | `verde/js2/gpt-oss-120b` | Records decisions, action items, consensus, dissent, deadlines, and ownership. |
| Discussion Intelligence Agent | `verde/js2/gpt-oss-120b` | Codes every meaningful contribution into structured dashboard-ready metadata. |
| Cloud Infrastructure Engineer | `verde/js2/gpt-oss-120b` | Optimizes Kubernetes, distributed execution, GPUs, cloud, storage, orchestration, and subagents. |
| Agent Operations Manager | `verde/js2/gpt-oss-120b` | Monitors workload, idle agents, spawning, performance, resources, and efficiency. |

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
