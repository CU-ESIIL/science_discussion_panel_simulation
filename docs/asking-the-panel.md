# Asking The Panel Questions

The Interaction Agent is the human-facing agent. It answers from panel memory
first and queues absent answers in `QUESTIONS_FROM_USER.md`.

Examples:

```bash
make panel-queue QUESTION="Ask the panel whether AI can discover ecological mechanisms."
make panel-round
make panel-summary
```

The Interaction Agent must distinguish summarizing prior discussion from
initiating a new panel round. It must link answers to rounds, source notes,
evidence, fact checks, citations, or experiments.
