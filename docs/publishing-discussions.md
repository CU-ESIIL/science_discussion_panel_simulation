# Publishing Panel Discussions

The first publishing workflow is deliberately manual and GitHub Desktop
friendly.

1. The panel updates `public_site/reports/panel-discussion-log.md` and
   `public_site/reports/latest-discussion.md` after a substantive discussion.
2. Those paths are mounted to the repository's tracked `docs/reports/` folder.
3. A human reviews the GitHub Desktop diff for accuracy, evidence links,
   sensitive claims, and public readability.
4. The human pushes the reviewed markdown.
5. GitHub Actions rebuilds and deploys the MkDocs website.

The discussion log should link back to discussion rounds, evidence packets,
decisions, fact checks, and dashboard data where possible. It should not include
secrets, private notes, unreviewed sensitive claims, or claims that have not
been labeled as evidence, interpretation, speculation, or decision.

Later automation can create pull requests or commit reviewed discussion logs,
but the human review gate should remain explicit.
