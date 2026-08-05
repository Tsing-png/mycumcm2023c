# Q2 Method Card — Category-level Replenishment & Pricing

## Goal and success criteria
- **Goal**: Model the quantitative relationship between category daily sales and cost-plus pricing; determine daily replenishment quantity and pricing for each of 6 categories for 2023-07-01~07 to maximize total profit.
- **Success**: Replenishment quantities and prices within historically reasonable ranges; profit exceeds naive baseline (historical-mean replenishment + fixed markup); model shows reasonable sensitivity to price elasticity and loss rate assumptions.

## Human constraints
- Output form: Per-category per-day replenishment table (kg), pricing table (yuan/kg), estimated 7-day profit
- Priority: Interpretability first — Prophet components must be visualizable, newsvendor logic auditable
- Unacceptable failure: Output degeneracy (all categories get same markup, all days same replenishment)
- Experiment budget: Light (<5 min per full fit+optimize cycle on laptop CPU)

## Shortlist

| ID | Role | Mathematical idea | Why eligible | Main risk | Implementation cost |
|---|---|---|---|---|---|
| M1 | **main_candidate** | Prophet time-series decomposition + newsvendor (报童) model + nonlinear programming for joint markup-quantity optimization | 吴萌 et al. (2024) official solution. Prophet separates trend/season/holiday transparently. Newsvendor is the canonical single-period perishable inventory framework. Markup rate α_i(t) as continuous decision variable. | Prophet may overfit with only 3 years of daily data; newsvendor assumes known demand distribution — residuals from Prophet may not be i.i.d. | Medium — prophet (pypi) + scipy.optimize |
| M2 | **usable_baseline** | ARIMA/SARIMA time-series prediction + historical-average markup + safety-stock heuristic (mean + z·σ replenishment) | Classic method used in 聂宇旋, 陈妙霞, 杨若涵. ARIMA is well-understood and fast. Fixed markup is the simplest cost-plus implementation. Directly comparable on total profit. | ARIMA does not natively handle multiple seasonalities (weekly+annual); fixed markup ignores price-demand relationship | Low — statsmodels ARIMA + numpy |
| M3 | **conditional_fallback** | Double-log price-elasticity model + LSTM prediction + nonlinear optimization | 聂森 et al. (2024). Price elasticity explicitly models demand-price coupling. Different mathematical structure from M1 (elasticity-based vs decomposition-based). | LSTM violates light-compute budget; elasticity estimates may be unstable with 6 categories | High — keras/torch + longer runtime |

## Baseline validity
- Real task completed: Yes — M2 produces per-category per-day replenishment and pricing
- Comparable output/metric: Yes — total 7-day profit directly comparable between M1 and M2
- If no, classification: N/A

## Risk-probe summary
| ID | Executability | Data/assumptions | Degeneracy | Sensitivity | Scale | Verdict |
|---|---|---|---|---|---|---|
| M1 | PASS 1.8s | Prophet components meaningful (trend:145, weekly:75, yearly:145). **CF>1 for 5/6 categories** — mitigation: bound Q ≤ 1.5×hist_max | RMSE 34.1kg, MAPE 18.9%, forecast varies | CF>1 structural (high markup + k=0.7), robust to ±20% loss | ~11s all 6 | **CONDITIONAL** — needs Q-bounding |
| M2 | PASS 2.1s | ARIMA(2,1,2) by AIC. Residual structure remains (expected). Fixed markup ignores daily variance (σ²: 4.8-42.6) | RMSE 45.0kg, MAPE 27.1%, CV 0.47-0.84 per category | Fixed markup stable by design | ~13s all 6 | **PASS** |
| M3 | — | — | — | — | Exceeds budget | CONDITIONAL (trigger only) |

## Fallback trigger
- **Trigger**: M1 Prophet residual ACF shows significant remaining structure (Ljung-Box p<0.01) AND M2 ARIMA produces lower holdout RMSE
- **Evidence to evaluate**: Prophet residual diagnostics, ARIMA vs Prophet holdout RMSE comparison

## Compact history
- 2026-08-05: Initial method card. M1=Prophet+Newsvendor, M2=ARIMA+fixed markup, M3=elasticity+LSTM (fallback only).
