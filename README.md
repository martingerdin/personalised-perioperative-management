This repository includes documents and code for a research project on personalised perioperative management. It is primarily worked on by agents, with substantial human input of course. The project is about how "AI" agents can be used to personalise perioperative management, including assessing patients' fitness before anaesthesia and surgery through medical chart review, draft personalised management plans, and research associations between patient level variables and outcomes.

## Research documents plan

See [`docs/plan-research-documents.qmd`](docs/plan-research-documents.qmd).

Deliverables:

1. Short literature review
2. Umbrella research plan for Ethix (stable, broad)
3. Detailed research plan (specific, living)
4. Ethics application draft for Etikprövningsmyndigheten / Ethix
5. Shared BibTeX bibliography
6. AI-writing attribution ledger with running totals

Supporting paths:

- `docs/two-research-plans.md` — why two plans exist
- `docs/ai-transparency.md` — how AI % is logged
- `docs/research-plan-umbrella.qmd` — ethics-facing protocol stub
- `docs/research-plan-detailed.qmd` — internal detailed work-plan stub
- `docs/ethix/` — Ethix PDF, field map (`.md`), and YAML
- `references/project.bib` — shared bibliography
- `checklists/` — SPIROS and SPIRIT stubs
- `meta/ai-attribution-*.csv|md` — AI share ledger and summary
- `scripts/ai_attribution.py` — refresh totals
- `_quarto.yml` — Quarto project settings

## AI-writing disclosure

Every content commit should include:

```text
AI-Written-Pct: 85
```

Then run:

```bash
python scripts/ai_attribution.py refresh
```

See the current total in [`meta/ai-attribution-summary.md`](meta/ai-attribution-summary.md).
