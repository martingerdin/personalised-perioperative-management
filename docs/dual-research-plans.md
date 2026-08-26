# Dual research plans

This project keeps **two** research plans on purpose.

| Document | Audience | Stability | File |
|----------|----------|-----------|------|
| Umbrella research plan | Etikprövningsmyndigheten / Ethix | Broad and stable; change only with ethics amendment | `docs/research-plan-umbrella.qmd` |
| Engineering research plan | Project team | Detailed and living; update as methods mature | `docs/research-plan-engineering.qmd` |

## Why two plans

Ethics review is slow to amend. Day-to-day engineering work will change prompts, model choices, evaluation metrics, and code paths. I will put the wide, ethically relevant frame in the umbrella plan. I will put operational detail in the engineering plan.

## Boundary rule

The engineering plan must stay **inside** the umbrella plan.

Allowed without ethics amendment (examples):

- Swap open-weight model versions within the approved processing setup
- Refine prompts, eval harnesses, and dashboards
- Add secondary exploratory analyses already covered by the umbrella aims
- Reorganise code and documentation

Needs ethics amendment (examples):

- New population, site, or data source not covered by the umbrella
- New purpose (for example clinical decision-making without the stated human oversight)
- New identifiable-data processing route (for example a new external API for chart text)
- Intervention in care that was not described as interventional in the umbrella plan

## Umbrella plan content (ethics)

Keep it general but not vague:

1. Aims and research questions at programme level
2. Design family (observational chart-based work under SPIROS; possible later interventional track under SPIRIT stated as contingent)
3. Population and setting in wide but bounded terms
4. Data categories (journal text, structured perioperative variables, outcomes)
5. AI processing principles: assistive only; human accountability; approved environments; logging
6. Consent / legal basis options we may use
7. Risks, mitigations, and stop rules
8. Dissemination and AI-writing transparency

Avoid locking: exact model names, prompt text, sprint schedules, package versions, dashboard layouts.

## Engineering plan content (internal)

1. Concrete workstreams and milestones
2. System architecture (agents, tools, retrieval, audit logs)
3. Model shortlist and selection criteria
4. Evaluation protocol and datasets
5. Safety tests and red-team cases
6. Reproducibility (seeds, prompt registry, env locks)
7. Mapping: each workstream → umbrella aim it serves

## Consistency check

Before each ethics-facing change, I will ask:

1. Does this stay within the umbrella population, data, aims, and processing routes?
2. If no, draft an Ethix ändringsansökan before doing the work.
