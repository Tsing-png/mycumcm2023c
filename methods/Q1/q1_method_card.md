# Q1 Method Card — Sales Distribution & Correlation

## Goal and success criteria
- **Goal**: Reveal statistical distribution characteristics of category-level and product-level sales volume, temporal patterns, and inter-category/inter-product correlation/association structures.
- **Success**: Distribution patterns supported by statistical tests; association direction and strength quantified; conclusions directly inform variable selection for Q2/Q3.

## Human constraints
- Output form: Statistical tables, correlation heatmaps, distribution plots, clustering dendrograms
- Priority: Interpretability first — every step must have clear mathematical/business meaning
- Unacceptable failure: Output degeneracy (all correlations near zero or all near 1; clusters collapse to 1)
- Experiment budget: Light (<5 min on laptop CPU)

## Shortlist

| ID | Role | Mathematical idea | Why eligible | Main risk | Implementation cost |
|---|---|---|---|---|---|
| M1 | **main_candidate** | Spearman rank correlation + K-means++ clustering + empirical distribution fitting | Literature consensus (5/5 papers). Non-parametric correlation handles non-normal sales data. K-means++ provides interpretable product groupings by sales profile (magnitude + volatility). | Sparse products (87 with <30 days) inflate noise; category imbalance (5 vs 100) weakens small-category inference | Low — scipy.stats + sklearn |
| M2 | **usable_baseline** | Pearson correlation + hierarchical clustering (Ward) + descriptive statistics (quartiles, CV) | Simpler alternative used in 杨若涵 et al. (2024). Hierarchical clustering gives dendrograms directly interpretable. Pearson assumes linearity — different assumption profile from M1. | Pearson invalid if data is non-normal (K-S test p<0.05 per 陈妙霞); hierarchical clustering sensitive to outliers | Low — scipy.stats + scipy.cluster |

## Baseline validity
- Real task completed: Yes — produces correlation matrix and clustering of categories/products
- Comparable output/metric: Yes — correlation coefficients directly comparable (Spearman ρ vs Pearson r)
- If no, classification: N/A

## Risk-probe summary
| ID | Executability | Data/assumptions | Degeneracy | Sensitivity | Scale | Verdict |
|---|---|---|---|---|---|---|
| M1 | PASS 0.11s | Non-parametric — no normality needed. Silhouette 0.34-0.46 | Spearman ρ∈[-0.19,0.63], 2 clusters balanced (72/87) | Bootstrap σ=0.026 stable | 0.2s total | **PASS** |
| M2 | PASS 0.005s | **FAIL**: all 6 categories non-normal (p<0.000001) | Pearson r∈[0.11,0.69], not degenerate | 87% directional agreement with M1 | 0.005s | **CONDITIONAL** — Pearson invalid |

## Fallback trigger
No fallback needed — Q1 is descriptive with clear literature consensus. If both M1 and M2 fail degeneracy checks, investigate data preprocessing (outlier removal, sparse-product filtering).

## Compact history
- 2026-08-05: Initial method card created. M1 = Spearman + K-means++, M2 = Pearson + hierarchical clustering.
