# Model Routing

A scientific discussion panel does not need every role to use the same model route. In this container, the current approved local default is Verde for every panel avatar and support role.

The practical pattern is still conservative: route all agents through the approved Verde OpenAI-compatible endpoint, keep human review gates for publishing, credentials, GitHub pushes, external messaging, costly experiments, and sensitive claims, and record any future route changes before relying on them. This follows the same bounded-role idea used throughout the panel: agents get specific jobs, expected outputs, and explicit limits.

Local startup also sets `SCIENCECLAW_VERDE_ONLY_MODE=1` by default. That rewrites
the OpenClaw default agent model allowlist to the configured Verde route so
older persisted OpenAI/Codex routes do not remain available by accident.

The workspace seed includes `/workspace/MODEL_ASSIGNMENTS.md` as the role-level routing register. Update that file when a role changes model route, and record meaningful changes or reversions in `/workspace/DECISIONS.md`.

## Suggested Defaults

| Agent or avatar group | Recommended route | Why |
| --- | --- | --- |
| Moderator avatar based on the public online persona of Cibele Amaral | `verde/js2/gpt-oss-120b` | Introduces topics, asks opening and follow-up questions, balances participation, summarizes transitions, and closes reports. |
| Scientific avatars | `verde/js2/gpt-oss-120b` | Avatars based on the public online personas of Tanya Berger-Wolf, Lauren Gillespie, Jenna Kline, Justin Kitzes, Katherine Siegel, and Ty Tuff produce reviewable public-expertise perspectives. |
| Organizer avatar based on the public online persona of Jennifer Balch | `verde/js2/gpt-oss-120b` | Selects themes, proposes questions, reviews final reports, and aligns sessions with workshop goals. |
| Discussion Intelligence Agent | `verde/js2/gpt-oss-120b` | Preserves structured discussion metadata, agreement, disagreement, evidence gaps, related norms, and dashboard exports. |

## Verde-Style API Experiments

For Verde/CyVerse experiments, use the OpenAI-compatible base URL `https://llm-api.cyverse.ai/v1` and keep credentials local in `.env`. The [AI-VERDE API documentation](https://aiverde-docs.cyverse.ai/api/) explains that keys are obtained from the AI-VERDE course or team details and that available models can be listed from the API. Do not commit keys, paste them into chats, or store them in markdown:

```dotenv
VERDE_LLM_BASE_URL=https://llm-api.cyverse.ai/v1
VERDE_LLM_API_KEY=
VERDE_LLM_DEFAULT_MODEL=js2/gpt-oss-120b
VERDE_LLM_PROVIDER_NAME=verde
OPENCLAW_MODEL=verde/js2/gpt-oss-120b
OPENCLAW_DEFAULT_MODEL=verde/js2/gpt-oss-120b
```

After setting a local key, inspect the models your team can access:

```bash
curl -s -L "${VERDE_LLM_BASE_URL}/models" \
  -H "Authorization: Bearer ${VERDE_LLM_API_KEY}" \
  -H "Content-Type: application/json"
```

## Current AI-VERDE Candidate Models

The following model IDs were reported as available for the current API key context on 2026-05-18. Availability can vary by course, team, quota, and provider changes, so confirm with the `/models` endpoint before assigning a role:

| Model ID | Candidate use |
| --- | --- |
| `nrp/glm-4.7` | General specialist-agent evaluation |
| `nrp/glm-5` | General specialist-agent evaluation |
| `nrp/kimi` | Literature triage, summaries, and long-context checks |
| `nrp/gemma` | Lightweight drafts and comparison tests |
| `nrp/qwen3` | General specialist-agent evaluation |
| `nrp/qwen3-small` | Fast, low-risk smoke tests and simple routing checks |
| `nrp/minimax-m2` | General specialist-agent evaluation |
| `nrp/gpt-oss` | Open-model comparison tests |
| `Meta-Llama-3.1-70B-Instruct-quantized` | Larger-model baseline comparisons |
| `llama-3.3-70b-instruct-quantized` | Larger-model baseline comparisons |
| `phi-4` | Lightweight technical drafts and checks |
| `Llama-3.3-70B-Instruct-quantized` | Larger-model baseline comparisons |
| `phi-4-multimodal-instruct` | Multimodal experiments only when inputs and privacy are reviewed |
| `gemma-3-12b-it` | Lightweight drafts and comparison tests |
| `Llama-3.2-11B-Vision-Instruct` | Vision experiments only when images are appropriate to share |
| `esiil/GLM-4.7-Flash` | Fast ESIIL-context experiments and smoke tests |
| `js2/llama-4-scout` | Jetstream2-hosted model experiments |
| `js2/gpt-oss-120b` | Larger open-model comparison tests |

Do not treat this table as approval to use a model for sensitive claims or external actions. It is an inventory for bounded experiments.

These variables are intentionally generic placeholders. They make the container ready for local experimentation, but they do not guarantee that OpenClaw has registered a provider. Provider registration should be added only after checking the installed OpenClaw version and documenting the exact provider name, model ID, validation command, and fallback route.

## Evaluation Workflow

1. Pick one bounded role and one bounded task.
2. Run the task with the current reliable route.
3. Run the same task with the open-model candidate.
4. Compare evidence handling, citation behavior, role compliance, and uncertainty language.
5. Record the result in `/workspace/agent_reports/model_evaluations.md` or `/workspace/DECISIONS.md`.
6. Change the default route only after human approval when the role is user-facing, Slack-facing, director-level, or involved in sensitive claims.

## Scaling Pattern

The scalable unit is not "one key per agent." The scalable unit is a reviewed route assignment: role, provider, model, allowed task types, blocked actions, evaluation date, and fallback. That keeps the system reproducible as users add local keys, hosted endpoints, or future OpenClaw provider integrations.
