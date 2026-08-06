# Cross-Media Consistency Audit (Final)

**Profile**: submission | **Date**: 2026-08-05 | **Re-run**: post paper-polish

---

## Check 1: Paper numbers vs frozen_numbers.json

| Claim ID | Frozen Value | In Paper | Match |
|---|---|---|---|
| q1_spearman_range | [−0.1937, 0.6253] | ✅ section 04 | ✅ |
| q1_best_k | 2 | ✅ | ✅ |
| q1_silhouette | 0.4632 | ✅ | ✅ |
| q2_m1_daily_profit | 2,918.2 | ✅ section 05 | ✅ |
| q2_m1_weekly_profit_estimate | 20,427.4 | ✅ | ✅ |
| q2_markup_range | [1.0361, 1.2821] | ✅ | ✅ |
| q2_k_sensitivity_range | [2,362, 3,713] | ✅ | ✅ |
| q3_m1_daily_profit | 1,326.9 | ✅ section 06 | ✅ |
| q3_selected_skus | 31 | ✅ | ✅ |
| q3_min_demand_satisfaction | 0.7858 | ✅ | ✅ |

**Result**: 10/10 paper claims verified against frozen_numbers.json. ✅

## Check 2: Figure references

| Paper Ref | File | Exists |
|---|---|---|
| fig1_spearman_corr.png | paper/figures/fig1_spearman_corr.png | ✅ |
| fig2_monthly_trend.png | paper/figures/fig2_monthly_trend.png | ✅ |
| fig3_prophet_components.png | paper/figures/fig3_prophet_components.png | ✅ |
| fig4_markup_comparison.png | paper/figures/fig4_markup_comparison.png | ✅ |
| fig5_demand_satisfaction.png | paper/figures/fig5_demand_satisfaction.png | ✅ |

**Result**: 5/5 figure references resolve. ✅

## Check 3: Symbols match symbol_table.md

Paper uses $S_{i,t}$, $P_{i,t}$, $\alpha_{i,t}$, $C_{i,t}$, $L_i$, $k$, $e_i$, $\pi$, $\rho$, $\gamma_i$, $d_{\min}$, $N$ — all consistent with `planning/symbol_table.md`. Notation $S_i(t)$ was corrected to $S_{i,t}$ during polish. ✅

## Check 4: Human decisions resolved

10 decisions in `planning/framing_decisions.jsonl`. Methods, profit function, discount policy, demand satisfaction, space constraint — all referenced in paper. ✅

## Check 5: Freeze not stale

Frozen 2026-08-05. No newer experimental results. code re-run at 300dpi on same date — outputs identical. ✅

## Check 6: Method roles match approved plan

Paper describes M1 for Q1-Q3 as main methods, M2 as baselines. No fallback methods mentioned (correct — not triggered). ✅

---

## Verdict: PASSED

0 divergences. All 10 frozen claims in paper. All 5 figures present. Notation consistent. Decisions traced.
