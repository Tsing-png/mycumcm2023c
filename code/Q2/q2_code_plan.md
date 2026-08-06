# Q2 Code Plan — Category-level Replenishment & Pricing

**Target**: Python 3.10+
**Round**: round1
**Approved decision**: `q2_method_choice` → M1 (Prophet + Constrained Newsvendor), M2 (ARIMA + Fixed Markup)
**Generated**: 2026-08-05

---

## 1. Input Contract

| Source | Fields | Role |
|---|---|---|
| `workspace/data_clean/daily_sales.csv` | 销售日期, 单品编码, total_qty, avg_price, 批发价格(元/千克), 损耗率(%), 分类名称 | Core data |
| Elasticity estimation | From daily_sales: regress log(sales) ~ log(price) per category | Own elasticity estimates |

## 2. Methods

### M1 (main) — Prophet + Constrained Newsvendor

**Steps**:

1. **Category daily aggregation**: $S_{i,t}, C_{i,t}, P_{i,t}$ per category per day. Filter $C_{i,t} > 0.01$.
2. **Price elasticity estimation** (H5: own data):
   - Double-log model per category: $\ln S_{i,t} = \alpha + e_i \ln P_{i,t} + \text{controls}$
   - Controls: day-of-week dummies, month dummies
   - Store $e_i$ and compare with 聂森 values as sanity check
3. **Prophet fit** (per category):
   - Train on data through 2023-05-31. Holdout: June 1-30.
   - Model: `yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False`
   - `add_country_holidays(country_name='CN')`
   - No price regressor (probe showed it worsens holdout)
   - Forecast 31 days ahead → July 1 demand forecast $\hat{D}_{i,\text{Jul1}}$
4. **Holdout evaluation**: RMSE, MAPE on June 2023 holdout. Store per-category.
5. **Residual diagnostics**: Extract $\varepsilon_{i,t} = S_{i,t} - \hat{D}_{i,t}$. Compute empirical CDF for newsvendor.
6. **Demand std estimation**: $\sigma_i^{\text{demand}} = \text{std}(S_{i,t})$ or std of recent 90-day residuals
7. **Newsvendor optimization** (per category, July 1):
   - Grid: markup $\alpha \in [\max(0.1, \bar{\alpha}-0.4), \min(2.5, \bar{\alpha}+0.5)]$, 35 steps
   - Grid: $Q$ factor $\in [0.6, 1.8]$, 35 steps
   - Demand adjustment: $D(\alpha) = \hat{D} \cdot \left(\frac{(1+\alpha)C}{(1+\bar{\alpha})C}\right)^{e_i}$
   - Expected profit via empirical quantile (H6: non-parametric):
     - Use empirical CDF of residuals: sort $\varepsilon$, find $F^{-1}(\Phi)$ by interpolation
     - Or: Monte Carlo with residual bootstrap
   - Constraint: $Q \leq 1.5 \times \max_{\tau} S_{i,\tau}$
   - Store optimal $(\alpha_i^*, Q_i^*, P_i^*, \pi_i^*)$
8. **7-day profit**: For days 2-7, repeat Prophet forecast + newsvendor with rolling forecast. Or use day-1 markup and adjust Q daily based on updated Prophet forecast.
9. **7-day profit**: For simplicity, forecast all 7 days with Prophet, then optimize each day independently.

**Key parameters**:
- $k = 0.66$ (baseline), also report $k \in \{0.5, 0.75\}$
- $Q_{\max} = 1.5 \times \text{hist\_max\_daily\_sales}$
- Empirical quantile function for $F^{-1}$

### M2 (baseline) — ARIMA + Fixed Markup

**Steps**:

1. **ARIMA fit** (per category):
   - Grid search $(p,d,q) \in \{1,2\}\times\{0,1\}\times\{1,2\}$, select by AIC
   - Train through 2023-05-31. Forecast 31 steps → July 1
2. **Fixed markup**: $\bar{\alpha}_i = \text{mean}(P_{i,t}/C_{i,t} - 1)$ over training period
3. **Order quantity**: $Q_i = \min(\hat{D}_i^{\text{ARIMA}} / (1-L_i),\ Q_{\max})$
4. **Price**: $P_i = (1+\bar{\alpha}_i) \cdot C_{i,\text{last}}$
5. **Profit**: Same expected profit formula as M1, with M2's $(Q_i, P_i)$

## 3. Comparable Outputs

| Metric | M1 | M2 |
|---|---|---|
| Per-category RMSE (June holdout) | Prophet RMSE | ARIMA RMSE |
| Per-category markup $\alpha_i$ | Optimized | Historical mean |
| Per-category order $Q_i$ (July 1) | Newsvendor optimal | $\hat{D}/(1-L)$ |
| Per-category price $P_i$ (July 1) | Cost-plus optimized | Cost-plus fixed |
| 1-day total profit | $\sum \pi_i^{\text{M1}}$ | $\sum \pi_i^{\text{M2}}$ |
| 7-day total profit | Extrapolated | Extrapolated |
| Markup diversity (std across cats) | Must be >0.01 | — |

## 4. Output Files

```
results/Q2/experiments/round1/
├── figures/
│   ├── q2_prophet_decomposition_花叶类.png
│   ├── q2_holdout_comparison.png
│   ├── q2_markup_comparison.png
│   └── q2_profit_bar.png
├── tables/
│   ├── q2_m1_optimal_policy.csv       (category, date, markup, price, Q, profit)
│   ├── q2_m2_baseline_policy.csv
│   ├── q2_holdout_metrics.csv
│   └── q2_elasticity_estimates.csv     (own vs 聂森 comparison)
├── metrics/
│   └── q2_comparison.json
└── run_summary.json
```

## 5. Risk Monitoring

| Risk | Check | Action if triggered |
|---|---|---|
| Prophet RMSE > ARIMA RMSE for 3+ categories | Per-category holdout comparison | Consider M3 fallback |
| All $\alpha_i^*$ within 1% of each other | std(optimized markups) < 0.01 | Degeneracy — investigate |
| Any $\pi_i^* < 0$ | Per-category profit check | Flag in report |
| Own elasticity $e_i$ sign ≠ 聂森 sign | Sanity check | Use own estimate, note discrepancy |
| $k$ sensitivity span >100% profit range | Report under $k\in\{0.5,0.66,0.75\}$ | Already planned |

## 6. Seed & Environment

- Random seed: 42 (Prophet has internal Stan seed; scipy.stats bootstrap)
- Expected runtime: <60s (6 categories × Prophet + ARIMA + grid search)
- Dependencies: prophet, statsmodels, pandas, numpy, scipy
