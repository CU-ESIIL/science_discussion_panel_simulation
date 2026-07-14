# TAG_ONTOLOGY.md

The Discussion Intelligence Agent maintains normalized tags for dashboard
summaries and discussion-network analysis. Agents may propose new tags, but
they should also map them to one of the canonical categories below.

## Canonical Categories

| Category | Use For |
| --- | --- |
| Scientific Domain | disciplinary framing, ecological concepts, theory |
| Methods | study design, workflows, protocols, validation |
| Data | datasets, provenance, metadata, quality, licensing |
| Infrastructure | storage, APIs, containers, cloud, reproducibility |
| AI | foundation models, agents, machine learning, automation |
| Modeling | simulations, prediction, mechanisms, scenarios |
| Statistics | uncertainty, calibration, inference, power, robustness |
| Remote Sensing | satellites, drones, cameras, acoustic sensors, edge sensing |
| Ecology | organisms, populations, communities, ecosystems, conservation |
| Policy | management, governance, decisions, regulations |
| Ethics | equity, harm, consent, privacy, sovereignty |
| Governance | approval gates, norms, accountability, auditability |
| Visualization | dashboards, figures, maps, visual summaries |
| Communication | audiences, narrative, public summaries, manuscripts |
| Future Work | follow-up studies, future rounds, missing expertise |
| Questions | open questions, clarification requests, research questions |
| Evidence | citations, evidence packets, claim support, fact checks |
| Action Items | owners, deadlines, tasks, next steps |
| Norms | collaboration rules, adopted practices, process commitments |
| Uncertainty | unknowns, confidence, caveats, limits |

## Normalization Rules

1. Use lowercase slug tags in structured events, for example `remote-sensing`
   or `evidence`.
2. Map close variants to the same canonical tag.
3. Preserve proposed new tags in `proposed_tags` until reviewed.
4. Do not create separate tags for spelling variants, singular/plural variants,
   or synonyms when a canonical tag exists.
5. Record low-engagement topics as low engagement, not low importance.
