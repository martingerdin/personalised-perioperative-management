# AI attribution summary

Per-commit AI-written share for this repository.

## Totals

- Commits scanned: **17**
- Commits with AI %: **15**
- Commits missing AI %: **2**
- Lines added (weighted base): **3155**
- Weighted AI-written share: **93.0%**
- Weighted human-written share: **7.0%**
- Unweighted mean AI %: **88.3%**

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
| `5c43f8b` | 2026-08-26 | 100 | 10 | trailer | Refresh AI attribution after detailed-plan rename |
| `b4e9798` | 2026-09-01 | — | 0 | missing | Add ethix template |
| `073f7fd` | 2026-09-01 | 92 | 1776 | trailer | Convert Ethix PDF to field map and add GitHub issues from plan |
| `43a6b39` | 2026-09-01 | 100 | 10 | trailer | Refresh AI attribution after Ethix conversion and issues |
| `59dba40` | 2026-09-01 | 85 | 33 | trailer | Reorder plan: literature before umbrella research plan |
| `9951606` | 2026-09-01 | 100 | 10 | trailer | Refresh AI attribution after sequence reorder |
| `fb619aa` | 2026-09-01 | 90 | 1 | trailer | Fix detailed-plan issue dependency in issue script |
| `dec938b` | 2026-09-01 | — | 2917 | missing | Merge first PR with the plan |
| `22167e2` | 2026-09-01 | 88 | 99 | trailer | Add design note for issue #2 (population, data, design, outcomes) |

