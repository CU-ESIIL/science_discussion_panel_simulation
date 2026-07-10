# Secret Migration

GitHub forks do not inherit Actions secrets from the source repository.
Repository secrets must be recreated in the new repository, or organization
secrets must allow access from the new repository.

## Secrets And Variables To Audit

- `SCIENCECLAW_VERDE_LLM_API_KEY`
- `VERDE_LLM_API_KEY`
- `SCIENCECLAW_VERDE_LLM_BASE_URL`
- `VERDE_LLM_BASE_URL`
- `SCIENCECLAW_VERDE_LLM_DEFAULT_MODEL`
- `VERDE_LLM_DEFAULT_MODEL`
- `SCIENCECLAW_GITHUB_TOKEN`
- `SCIENCECLAW_SLACK_BOT_TOKEN`
- `SLACK_BOT_TOKEN`
- `SCIENCECLAW_SLACK_APP_TOKEN`
- `SLACK_APP_TOKEN`
- `SCIENCECLAW_SLACK_DEFAULT_CHANNEL`
- `SLACK_DEFAULT_CHANNEL`
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `DOCKERHUB_IMAGE`

Secrets and variables are different in GitHub. Secrets hide values; variables
are plain configuration. Do not store credentials as variables.

## Local Migration

Copy `.env.example` to `.env` and fill values locally. For mounted secret files,
write values outside git, set paths such as `VERDE_LLM_API_KEY_FILE` or
`GITHUB_TOKEN_FILE`, and start Compose with the secrets override when needed.

## Validation

```bash
make check-secrets
```

The checker reports configured, missing, optional, or required. It never prints
secret values.

## Rotation

If a key is exposed, revoke or rotate it with the provider, remove it from git
history or screenshots where possible, update local secret files and GitHub
Secrets, and run the checker again.

You may run with AI-VERDE and no Slack. You may also run locally without GitHub
Actions.
