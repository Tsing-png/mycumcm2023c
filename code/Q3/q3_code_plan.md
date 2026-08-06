# Q3 Code Plan — SKU-level Replenishment & Pricing

**Target**: Python 3.10+
**Round**: round1
**Approved decision**: `q3_method_choice` → M1 (Filter ≥2.5kg + Per-SKU Newsvendor), M2 (Same SKUs + Fixed Markup)
**Generated**: 2026-08-05

---

## 1. Input Contract

| Source | Fields | Role |
|---|---|---|
| `workspace/data_clean/daily_sales.csv` | 销售日期, 单品编码, total_qty, avg_price, 批发价格(元/千克), 损耗率(%), 分类名称 | Core data |
| Q2 output: elasticity estimates | Per-category $e_i$ from Q2 M1 | Price sensitivity |
| Q2 output: category markup | Per-category $\alpha_i^*$ (reference only) | Pricing prior |

## 2. Methods

### M1 (main) — Filter ≥2.5kg + Per-SKU Newsvendor

**Steps**:

1. **Eligible product identification**: Products with sales on June 24-30, 2023 (~49 products).
2. **Filter**: Keep products with `avg_daily_sales ≥ 2.5kg` during June 24-30.
   - Expected: 31 products → in [27, 33] range.
   - If count outside [27, 33]: adjust threshold ±0.1kg until count in range. Log adjustment.
3. **Per-SKU demand estimation**:
   - Last 30 days (June 2023): per-SKU daily demand mean $\mu_j$ and std $\sigma_j$
   - If <30 days of data: use June 24-30 week stats as fallback
4. **Per-SKU cost**: Last known wholesale price $C_j$ (from June 30 or nearest date)
5. **Per-SKU loss rate**: From `item_loss_rates.csv` — $\ell_j$
6. **Per-SKU newsvendor optimization** (same structure as Q2 M1, per-SKU):
   - Grid: markup $\alpha_j \in [\max(0.1, \bar{\alpha}_{\text{cat}}-0.3), \min(2.5, \bar{\alpha}_{\text{cat}}+0.5)]$, 25 steps
   - Grid: $Q$ factor $\in [0.7, 1.6]$, 25 steps
   - Demand adjustment: $D_j(\alpha) = \mu_j \cdot \left(\frac{(1+\alpha_j)C_j}{(1+\bar{\alpha}_{\text{cat}})C_j}\right)^{e_{\text{cat}}}$
   - Constraint: $Q_j \geq 2.5$ kg (minimum display). $Q_j \leq 1.5 \times \max_{\text{June}} s_{j,t}$
   - Expected profit via empirical quantile or normal approximation
   - Store $(\alpha_j^*, Q_j^*, P_j^*, \pi_j^*)$
7. **Demand satisfaction**: 
   - Per category: $\gamma_i = \sum_{j \in \mathcal{I}_i} Q_j^* / D_i^{\text{ref}}$
   - $D_i^{\text{ref}}$ = avg daily category sales June 24-30
   - Penalized profit not needed if all $\gamma_i \geq 100\%$ (probe suggests they will be)
   - If any $\gamma_i < 100\%$: compute penalized profit with $\lambda$ tuned so penalty ~10% of profit at $\gamma_i=50\%$
8. **Total**: $\Pi^{\text{Q3}} = \sum_{j \in \mathcal{J}^{\text{sel}}} \pi_j^*$

**Key parameters**:
- $k = 0.66$ (baseline), report $k \in \{0.5, 0.75\}$
- $d_{\min} = 2.5$ kg
- $N \in [27, 33]$ (satisfied by filter)
- $e_i$: from Q2 own estimation

### M2 (baseline) — Same 31 SKUs + Fixed Markup

**Steps**:

1. Same 31 products as M1
2. **Fixed markup**: Per-SKU $\bar{\alpha}_j = \text{mean}(p_{j,t}/c_{j,t} - 1)$ over June 2023
3. **Order quantity**: $Q_j = \max(2.5, \mu_j / (1 - \ell_j/100))$
4. **Price**: $P_j = (1+\bar{\alpha}_j) \cdot C_j$
5. **Profit**: Same expected profit formula as M1, with M2's $(Q_j, P_j)$

## 3. Comparable Outputs

| Metric | M1 | M2 |
|---|---|---|
| SKUs selected | 31 (filtered) | 31 (same) |
| Per-category demand satisfaction $\gamma_i$ | From optimized Q | From fixed Q |
| Total order quantity | $\sum Q_j^*$ | $\sum Q_j^{\text{fixed}}$ |
| Total 1-day profit | $\sum \pi_j^*$ | $\sum \pi_j^{\text{fixed}}$ |
| Markup diversity (std across SKUs) | Must be >0.01 | Fixed per SKU history |

## 4. Output Files

```
results/Q3/experiments/round1/
├── figures/
│   ├── q3_sku_profit_ranking.png
│   ├── q3_category_satisfaction.png
│   └── q3_markup_distribution.png
├── tables/
│   ├── q3_m1_sku_policy.csv        (单品编码, category, Q, P, markup, profit)
│   ├── q3_m2_baseline_policy.csv
│   └── q3_demand_satisfaction.csv  (per-category γ_i)
├── metrics/
│   └── q3_comparison.json
└── run_summary.json
```

## 5. Risk Monitoring

| Risk | Check | Action if triggered |
|---|---|---|
| Filter count ∉ [27, 33] | Count qualifying products | Adjust threshold, log change |
| Any $\pi_j^* < 0$ | Per-SKU profit check | Flag; may indicate data error |
| All $\alpha_j^*$ equal | std(markups) < 0.01 | Degeneracy |
| Any $\gamma_i < 50\%$ | Demand satisfaction per category | Activate M3 fallback (per-category quota) |
| $k$ sensitivity >100% profit range | Report under multiple k values | Already planned |

## 6. Seed & Environment

- Random seed: 42
- Expected runtime: <10s (31 SKUs × grid search)
- Dependencies: pandas, numpy, scipy
