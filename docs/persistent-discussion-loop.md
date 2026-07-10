# Persistent Discussion Loop

The loop is supervised and resource-limited. It is not an uncontrolled infinite
loop.

Default cycle:

1. Read current panel state.
2. Check user questions.
3. Select a topic.
4. Prepare evidence if needed.
5. Ask selected panelists for independent openings.
6. Conduct a moderated exchange.
7. Identify claims requiring verification.
8. Route bounded research or experiment requests.
9. Update positions, disagreement, indexes, and synthesis.
10. Sleep until the next cycle unless a user question is waiting.

Controls:

```bash
make panel-status
make panel-pause
make panel-resume
make panel-round
```

Autorun is disabled by default with `PANEL_AUTORUN=0`.
