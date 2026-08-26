# AI attribution summary

Per-commit AI-written share for this repository.

## Totals

- Commits scanned: **8**
- Commits with AI %: **8**
- Commits missing AI %: **0**
- Lines added (weighted base): **1216**
- Weighted AI-written share: **94.9%**
- Weighted human-written share: **5.1%**
- Unweighted mean AI %: **83.8%**

Weighted share = sum(ai_pct × lines_added) / sum(lines_added).

## Method

1. Prefer commit trailer `AI-Written-Pct: <0-100>`.
2. Else use `meta/ai-attribution-overrides.csv` if present.
3. Refresh with `python scripts/ai_attribution.py refresh`.

## Per commit

| Commit | Date | AI % | +lines | Source | Subject |
|--------|------|------|--------|--------|---------|
| `cafb674` | 2026-08-25 | 0 | 1 | override | Initial commit, add README |
| `f7fd4c8` | 2026-08-26 | 95 | 488 | override | Add plan for literature review, research plan, ethics, and bibliography |
| `dae2a25` | 2026-08-26 | 95 | 31 | override | Note Ethix has no submission API; ethics draft needs a field template |
| `960eeeb` | 2026-08-26 | 95 | 7 | override | Add Ethix field-list next step and acceptance criteria |
| `90b24b1` | 2026-08-26 | 95 | 648 | trailer | Split ethics umbrella and engineering plans; add AI attribution ledger |
| `9cccb3a` | 2026-08-26 | 100 | 8 | trailer | Refresh AI attribution summary after dual-plan commit |
| `1c2df79` | 2026-08-26 | 100 | 8 | trailer | Include prior refresh commit in AI attribution ledger |
| `8cef07c` | 2026-08-26 | 90 | 25 | trailer | Rename engineering research plan to detailed research plan |

