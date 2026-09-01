# AI writing transparency

I will log how much of each commit was AI-written, and keep a running total.

## Rule

Every commit that changes project material must declare an AI share.

Prefer a commit message trailer:

```text
AI-Written-Pct: 85
```

Meaning: about 85% of the new or changed material in that commit was produced by AI (agents or other generative tools). The rest was typed or substantially rewritten by a human.

## Ledger

| File | Role |
|------|------|
| `meta/ai-attribution.csv` | Per-commit ledger (regenerated) |
| `meta/ai-attribution-summary.md` | Totals and table (regenerated) |
| `meta/ai-attribution-overrides.csv` | Manual backfill when a trailer was missing |

## How to refresh

```bash
python scripts/ai_attribution.py refresh
python scripts/ai_attribution.py show
```

## Totals

- **Weighted AI %** = sum(ai_pct × lines_added) / sum(lines_added)
- **Weighted human %** = 100 − weighted AI %
- Unweighted mean is also reported, but weighted is the primary figure for disclosure

## Judgement guide

| Situation | Typical AI % |
|-----------|--------------|
| Human wrote almost all text; AI only fixed typos | 0–10 |
| Human outline; AI first draft; human heavy edit | 40–70 |
| AI draft; light human edit | 80–95 |
| AI-only generated content with human prompt only | 95–100 |

Be honest. Round to the nearest 5 if unsure.

## Ethics and protocol disclosure

The umbrella ethics research plan and Ethix answers will cite this ledger and the current weighted total. I will update the disclosure when the total moves in a material way before submission.
