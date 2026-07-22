# Publishing Panel Discussions

The local `discussion-heartbeat` service makes publishing GitHub Desktop
friendly without asking agents to write directly into the website.

1. The panel writes working rounds under `workspace/DISCUSSION_ROUNDS/`.
2. That workspace folder stays local and ignored by git.
3. The heartbeat notices new or changed rounds.
4. It renders reviewable public Markdown into tracked website files:
   `docs/reports/latest-discussion.md`,
   `docs/reports/panel-discussion-log.md`, and
   `docs/dashboard/discussion-dashboard.md`.
5. It writes a local pulse note to `workspace/HEARTBEAT.md`.
6. If question automation is enabled and no question is queued, it asks Cibele
   to open the next pending topic from `workspace/TOPIC_QUEUE.yaml`.
7. A human reviews the GitHub Desktop diff for accuracy, evidence links,
   sensitive claims, and public readability.
8. The human pushes the reviewed markdown.
9. GitHub Actions rebuilds and deploys the MkDocs website.

The discussion log should link back to discussion rounds, evidence packets,
decisions, fact checks, and dashboard data where possible. It should not include
secrets, private notes, unreviewed sensitive claims, or claims that have not
been labeled as evidence, interpretation, speculation, or decision.

The heartbeat automates local rendering and question queueing only. It does not
commit, push, publish, delete, run costly work, or expose secrets; the human
review gate remains explicit.
