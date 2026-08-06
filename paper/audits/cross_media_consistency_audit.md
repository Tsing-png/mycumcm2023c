# Cross-Media Consistency Audit (Final)

**Profile**: submission
**Date**: 2026-08-05

---

## Check 1: Numerical claims match frozen values and units

| Claim ID | Frozen | Source | Match |
|---|---|---|---|
| q1_spearman_range | [−0.1937, 0.6253] | run_summary.json | ✅ |
| q1_best_k | 2 | run_summary.json | ✅ |
| q1_silhouette | 0.4632 | run_summary.json | ✅ |
| q1_pearson_invalid | false | q1_comparison.json | ✅ |
| q2_m1_daily_profit | 2,918.2 | run_summary.json | ✅ |
| q2_m1_weekly_profit_estimate | 20,427.4 | run_summary.json | ✅ |
| q2_markup_std | 0.082 | run_summary.json | ✅ |
| q2_markup_range | [1.0361, 1.2821] | run_summary.json | ✅ |
| q2_k_sensitivity_range | [2,362, 3,713] | robustness summary | ✅ |
| q3_m1_daily_profit | 1,326.9 | run_summary.json | ✅ |
| q3_selected_skus | 31 | run_summary.json | ✅ |
| q3_min_demand_satisfaction | 0.7858 | run_summary.json | ✅ |
| q3_markup_std | 0.3108 | run_summary.json | ✅ |

**Result**: 13/13 claims verified. ✅

## Check 2: Referenced files and figures exist

All 21 referenced files in solution_package and method explanations verified on disk. 0 missing. ✅

## Check 3: Symbols match global symbol table

Solution package uses consistent notation from `planning/symbol_table.md`:
- $Q_{i,t}$, $P_{i,t}$, $\alpha_{i,t}$, $C_{i,t}$, $L_i$, $k$, $\pi$, $\rho$
- Units: kg, yuan/kg, yuan, dimensionless
- No conflicts detected. ✅

## Check 4: Human decisions resolved

| Decision ID | Status | Evidence |
|---|---|---|
| framing_profit_function | DECIDED | profit = revenue − cost − loss − discount |
| framing_discount_policy | DECIDED | passive clearance, k=0.66 |
| framing_q3_demand_satisfaction | DECIDED | penalty in objective |
| framing_q2_space_constraint | DECIDED | no space constraint |
| q1_method_choice | DECIDED | M1 Spearman+KMeans |
| q2_method_choice | DECIDED | M1 Prophet+Newsvendor |
| q3_method_choice | DECIDED | M1 Filter+Newsvendor |
| assumption_A1-A4, Q2.1-Q2.3, H1-H6 | DECIDED | all resolved in model_assumptions.md |

10/10 decisions resolved. ✅

## Check 5: Freeze not stale

All frozen values trace to `results/*/experiments/round1/` outputs generated 2026-08-05 — same date as freeze. No newer experimental results exist. ✅

## Check 6: Method roles match approved plan

| Q | Approved | Code | Match |
|---|---|---|---|
| Q1 | M1=Spearman+KMeans, M2=Pearson(diagnostic) | q1_main.py + q1_baseline.py | ✅ |
| Q2 | M1=Prophet+Newsvendor, M2=ARIMA+Fixed | q2_main.py + q2_baseline.py | ✅ |
| Q3 | M1=Filter+Newsvendor, M2=Same+Fixed | q3_main.py + q3_baseline.py | ✅ |
| Fallback M3 (Q2, Q3) | Not activated | Not implemented | ✅ |

---

## Verdict: PASSED

0 divergences found. All frozen claims verified. All references exist. All decisions logged.
