# Asking The Panel Questions

The PI Liaison is the human-facing coordinator. It answers from panel memory
first, assigns questions to owners, and queues absent answers in
`QUESTIONS_FROM_USER.md`.

Examples:

```bash
make panel-queue QUESTION="Ask the panel whether AI can discover ecological mechanisms."
make panel-round
make panel-summary
```

The PI Liaison must distinguish summarizing prior discussion from initiating a
new panel round. It must link answers to rounds, source notes, evidence, fact
checks, citations, decisions, action items, or experiments.
