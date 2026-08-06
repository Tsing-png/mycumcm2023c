# Q1 Code Plan — Sales Distribution & Correlation

**Target**: Python 3.10+
**Round**: round1 (first and only planned round)
**Approved decision**: `q1_method_choice` → M1 (Spearman + K-means++)
**Generated**: 2026-08-05

---

## 1. Input Contract

| Source | Fields | Role |
|---|---|---|
| `workspace/data_clean/daily_sales.csv` | 销售日期, 单品编码, total_qty, avg_price, 分类名称 | Core sales data |
| `workspace/data_clean/products.csv` | 单品编码, 分类名称 | Product-category mapping |

## 2. Methods

### M1 (main) — Spearman + K-means++ + Distribution Fitting

**Steps**:

1. **Daily category aggregation**: Pivot `daily_sales` to category×date matrix $S_{i,t}$
2. **Spearman correlation**: Compute $\rho_{ab}$ for all 15 category pairs. Output heatmap + matrix.
3. **Normality verification**: D'Agostino-Pearson test on each category's daily sales → confirm non-normal (justifies Spearman over Pearson)
4. **Product feature construction**: Per-product $\bar{s}_j$, $\sigma(s_j)$, $\text{CV}(s_j)$, $\bar{p}_j$. Filter to products with ≥30 sales days (159 products expected).
5. **K-means++ clustering**: $K=2..7$ grid. Select best $K$ by silhouette score. Output cluster assignments + silhouette plot.
6. **Cluster interpretation**: Category composition per cluster, centroid profiles.
7. **Distribution fitting**: Per-category: fit candidate distributions (normal, lognormal, gamma). Select best by KS statistic or AIC. Output fit parameters + Q-Q plots.
8. **Temporal analysis**: Monthly aggregate line plots per category. Identify seasonal peaks/troughs.

**Data filter**: Exclude 5 never-sold products and 461 returns (already removed in cleaning). Sparse products (<30 days) excluded from clustering but included in category-level correlation.

### M2 (diagnostic reference) — Pearson + Hierarchical Clustering

**Steps**:

1. Pearson correlation on same $S_{i,t}$ matrix
2. Report normality test failures (all 6 categories fail)
3. Ward hierarchical clustering on category sales vectors → dendrogram
4. Compare M1 vs M2 correlation matrices (Spearman Δ vs Pearson)

## 3. Comparable Outputs

| Metric | M1 | M2 |
|---|---|---|
| Correlation matrix | Spearman $\rho$ (15 values) | Pearson $r$ (15 values) |
| Clustering | K-means++ with silhouette | Hierarchical dendrogram |
| Cluster K | Selected by silhouette | Visual from dendrogram |
| Distribution fit | Best-fit per category | N/A (M1 only) |
| Directional agreement | % of $\text{sign}(\rho) = \text{sign}(r)$ | — |

## 4. Output Files

```
results/Q1/experiments/round1/
├── figures/
│   ├── q1_corr_heatmap_spearman.png
│   ├── q1_corr_heatmap_pearson.png
│   ├── q1_cluster_silhouette.png
│   ├── q1_monthly_sales_trend.png
│   └── q1_distribution_fits.png
├── tables/
│   ├── q1_spearman_corr.csv
│   ├── q1_pearson_corr.csv
│   ├── q1_cluster_assignments.csv
│   └── q1_distribution_params.csv
├── metrics/
│   └── q1_comparison.json
└── run_summary.json
```

## 5. Risk Monitoring

| Risk | Check |
|---|---|
| All $\rho \approx 0$ (degeneracy) | $\max|\rho| > 0.1$ |
| All $\rho \approx 1$ (degeneracy) | $\max|\rho| < 0.95$ |
| Single cluster (degeneracy) | Silhouette > 0.1 for $K \geq 2$ |
| Normality (M2 validity) | All 6 categories p < 0.05 → M2 invalid (expected) |

## 6. Seed & Environment

- Random seed: 42 (sklearn KMeans, scipy bootstrap)
- Expected runtime: <5s
- Dependencies: pandas, numpy, scipy, scikit-learn, matplotlib, seaborn
