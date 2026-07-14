# AI-VERDE Configuration

AI-VERDE remains a first-class OpenAI-compatible provider.

```dotenv
VERDE_LLM_BASE_URL=https://llm-api.cyverse.ai/v1
VERDE_LLM_API_KEY=
VERDE_LLM_API_KEY_FILE=
VERDE_LLM_DEFAULT_MODEL=js2/gpt-oss-120b
VERDE_LLM_PROVIDER_NAME=verde
OPENCLAW_MODEL=verde/js2/gpt-oss-120b
OPENCLAW_DEFAULT_MODEL=verde/js2/gpt-oss-120b
```

Keep credentials in local `.env`, mounted secret files, GitHub Secrets,
self-hosted runner secrets, or Kubernetes Secrets. Do not copy secrets into
prompts, logs, transcripts, CMS pages, screenshots, or markdown memory.

Validate without printing values:

```bash
make check-secrets
```
