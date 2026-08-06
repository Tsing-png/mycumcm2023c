# Symbol Table — CUMCM 2023 Problem C

**Generated**: 2026-08-05
**Scope**: Q1–Q4, global
**Status**: canonical (v1)

---

## 1. Sets and Indices

| Symbol | Name | Definition | Type | Domain | Scope |
|---|---|---|---|---|---|
| $\mathcal{I}$ | Category set | 6 vegetable categories | set | {花叶类, 辣椒类, 食用菌, 水生根茎类, 茄类, 花菜类} | Global |
| $i$ | Category index | Index into $\mathcal{I}$ | index | $i=1,\ldots,6$ | Q1–Q4 |
| $\mathcal{J}$ | Product (SKU) set | 251 products in catalog | set | 单品编码 | Global |
| $j$ | Product index | Index into $\mathcal{J}$ | index | $j=1,\ldots,251$ | Q1, Q3 |
| $\mathcal{J}_t$ | Available products at time $t$ | Products with sales on date $t$ | set | $\mathcal{J}_t \subseteq \mathcal{J}$ | Q3 |
| $t$ | Time index (day) | Calendar date | index | 2020-07-01 ~ 2023-07-07 | Global |
| $\mathcal{T}$ | Prediction horizon | Days to optimize over | set | {2023-07-01, …, 2023-07-07} (Q2); {2023-07-01} (Q3) | Q2, Q3 |
| $k$ | Cluster index | K-means cluster label | index | $k=1,\ldots,K$ | Q1 |
| $K$ | Number of clusters | Selected by silhouette/elbow | parameter | $\mathbb{N}^+$ | Q1 |

---

## 2. Input Data Variables

| Symbol | Name | Definition | Type | Unit | Scope | Source |
|---|---|---|---|---|---|---|
| $s_{j,t}$ | SKU daily sales | Total sales quantity of product $j$ on day $t$ | input | kg | Q1–Q3 | 附件2 (aggregated) |
| $p_{j,t}^{\text{sale}}$ | SKU sale price | Volume-weighted avg selling price of $j$ on $t$ | input | yuan/kg | Q2, Q3 | 附件2 |
| $c_{j,t}$ | SKU wholesale cost | Wholesale price of $j$ on $t$ | input | yuan/kg | Q2, Q3 | 附件3 |
| $\ell_j$ | SKU loss rate | Loss/wastage rate of product $j$ | input | % (dimensionless) | Q2, Q3 | 附件4 Sheet1 (visible) |
| $d_{j,t}^{\text{disc}}$ | Discount flag | Whether transaction was discounted | input | binary | Q2 | 附件2 |

---

## 3. Category-Level Aggregates

These are derived from SKU-level data by grouping on $\mathcal{I}$.

| Symbol | Name | Definition | Type | Unit | Scope |
|---|---|---|---|---|---|
| $S_{i,t}$ | Category daily sales | $S_{i,t} = \sum_{j \in \mathcal{I}_i} s_{j,t}$ | intermediate | kg | Q1, Q2 |
| $P_{i,t}$ | Category avg sale price | $P_{i,t} = \sum_{j \in \mathcal{I}_i} w_{j,t} \, p_{j,t}^{\text{sale}}$ (sales-weighted) | intermediate | yuan/kg | Q2 |
| $C_{i,t}$ | Category avg wholesale cost | $C_{i,t} = \sum_{j \in \mathcal{I}_i} w_{j,t} \, c_{j,t}$ (sales-weighted) | intermediate | yuan/kg | Q2 |
| $L_i$ | Category mean loss rate | $L_i = \frac{1}{|\mathcal{I}_i|}\sum_{j \in \mathcal{I}_i} \ell_j$ | parameter | dimensionless | Q2 |
| $\bar{S}_i$ | Category mean daily sales | $\bar{S}_i = \frac{1}{T}\sum_t S_{i,t}$ | intermediate | kg | Q1 |

---

## 4. Q1 — Statistical Analysis Symbols

| Symbol | Name | Definition | Type | Domain/Range | Unit | Source |
|---|---|---|---|---|---|---|
| $\rho_{ab}$ | Spearman rank correlation | Spearman's $\rho$ between category/product $a$ and $b$ | output | $[-1, 1]$ | dimensionless | M1 |
| $r_{ab}$ | Pearson correlation | Pearson's $r$ between $a$ and $b$ | output | $[-1, 1]$ | dimensionless | M2 (diagnostic) |
| $\mathbf{x}_j$ | Product feature vector | $( \bar{s}_j,\ \sigma(s_j),\ CV(s_j),\ \bar{p}_j )$ | intermediate | $\mathbb{R}^4$ | mixed | M1 |
| $\mu_k$ | Cluster centroid | Center of cluster $k$ in feature space | intermediate | $\mathbb{R}^4$ | mixed | M1 |
| $J(K)$ | Within-cluster distortion | $J(K) = \sum_{k=1}^{K}\sum_{\mathbf{x} \in C_k} \|\mathbf{x} - \mu_k\|^2$ | intermediate | $\mathbb{R}^+$ | — | M1 |
| $\text{Sil}(K)$ | Silhouette score | Average silhouette coefficient for $K$ clusters | output | $[-1, 1]$ | dimensionless | M1 |
| $\text{CV}_i$ | Coefficient of variation | $\text{CV}_i = \sigma(S_i)/\bar{S}_i$ | output | $\mathbb{R}^+$ | dimensionless | Q1 |
| $D_i^{\text{dist}}$ | Distribution family | Best-fit distribution for category $i$ | output | categorical | — | Q1 |
| $p_{\text{norm}}$ | Normality test p-value | D'Agostino-Pearson or Shapiro-Wilk test | intermediate | $[0, 1]$ | dimensionless | Q1 |

---

## 5. Q2 — Category Replenishment & Pricing Symbols

### 5.1 Prophet Decomposition (M1)

| Symbol | Name | Definition | Type | Unit | Source |
|---|---|---|---|---|---|
| $\hat{D}_{i,t}$ | Demand forecast (Prophet) | Point forecast for category $i$, day $t$ | intermediate | kg | M1 |
| $g_i(t)$ | Trend component | Piecewise linear or logistic growth | intermediate | kg | M1 |
| $s_i(t)$ | Seasonality component | Fourier series: weekly + yearly cycles | intermediate | kg | M1 |
| $h_i(t)$ | Holiday component | CN holiday effects with window | intermediate | kg | M1 |
| $\varepsilon_{i,t}$ | Residual | $\varepsilon_{i,t} = S_{i,t} - \hat{D}_{i,t}$ | intermediate | kg | M1 |
| $\sigma_i^{\text{demand}}$ | Demand std deviation | Std of deseasonalized demand or historical $\sigma$ | parameter | kg | M1 |

### 5.2 Cost-Plus Pricing

| Symbol | Name | Definition | Type | Domain | Unit |
|---|---|---|---|---|---|
| $\alpha_{i,t}$ | Markup rate | Decision variable: $P_{i,t} = (1 + \alpha_{i,t}) \cdot C_{i,t}$ | **decision** | $\alpha_{i,t} \geq 0$ | dimensionless |
| $P_{i,t}^{\text{opt}}$ | Optimized selling price | $P_{i,t}^{\text{opt}} = (1 + \alpha_{i,t}) \cdot C_{i,t}$ | **decision** (via $\alpha$) | yuan/kg | Q2 |
| $C_{i,t}^{\text{eff}}$ | Effective unit cost | $C_{i,t}^{\text{eff}} = C_{i,t} / (1 - L_i)$ | parameter | yuan/kg | Q2 |

### 5.3 Newsvendor Model (M1)

| Symbol | Name | Definition | Type | Unit |
|---|---|---|---|---|
| $Q_{i,t}$ | Order/replenishment quantity | Decision variable: how much to order | **decision** | kg |
| $Q_{i,t}^{\max}$ | Maximum order bound | $Q_{i,t}^{\max} = 1.5 \times \max_{\tau} S_{i,\tau}$ | parameter | kg |
| $k$ | Discount recovery rate | Discount price / regular price (empirical median) | parameter ($k=0.66$) | dimensionless |
| $c_u$ | Underage cost | $c_u = P - C^{\text{eff}}$ (profit lost per kg understocked) | intermediate | yuan/kg |
| $c_o$ | Overage cost | $c_o = C^{\text{eff}} - kP$ (net loss per kg overstocked) | intermediate | yuan/kg |
| $\Phi_i$ | Critical fractile | $\Phi_i = c_u / (c_u + c_o) = (P - C^{\text{eff}}) / (P - kP)$ | intermediate | $[0,1]$ |
| $F_i^{-1}$ | Inverse demand CDF | Quantile function of demand distribution | function | kg |

### 5.4 Profit

| Symbol | Name | Definition | Type | Unit |
|---|---|---|---|---|
| $\pi_{i,t}$ | Single-period expected profit | $\pi_{i,t} = P \cdot \mathbb{E}[\min(Q,D)] + kP \cdot \mathbb{E}[(Q-D)^+] - C^{\text{eff}} \cdot Q$ | output | yuan |
| $\Pi^{\text{Q2}}$ | Total 7-day profit (Q2) | $\Pi^{\text{Q2}} = \sum_{i \in \mathcal{I}} \sum_{t \in \mathcal{T}} \pi_{i,t}$ | **output** | yuan |
| $e_i$ | Price elasticity of demand | $\partial \ln D_i / \partial \ln P_i$ | parameter | dimensionless |

---

## 6. Q3 — SKU Replenishment & Pricing Symbols

### 6.1 Selection

| Symbol | Name | Definition | Type | Domain | Unit |
|---|---|---|---|---|---|
| $\mathcal{J}^{\text{elig}}$ | Eligible product set | Products with sales on June 24–30, 2023 | set | $\subseteq \mathcal{J}$ | — |
| $\mathcal{J}^{\text{sel}}$ | Selected product set | Products chosen for July 1 replenishment | **decision** | $\subseteq \mathcal{J}^{\text{elig}}$ | — |
| $N$ | Number of selected SKUs | $N = |\mathcal{J}^{\text{sel}}|$ | output | $[27, 33]$ | — |
| $d_{\min}$ | Minimum display quantity | 2.5 kg per selected SKU | constraint | constant | kg |
| $\delta_j$ | Selection indicator | $\delta_j = 1$ if SKU $j$ is selected, $0$ otherwise | intermediate | $\{0, 1\}$ | — |

### 6.2 Per-SKU Newsvendor (extends Q2 framework)

| Symbol | Name | Definition | Type | Unit |
|---|---|---|---|---|
| $Q_j$ | SKU order quantity | $\geq d_{\min}$ if $\delta_j = 1$, else $0$ | **decision** | kg |
| $P_j^{\text{opt}}$ | SKU optimized price | Via per-SKU newsvendor | **decision** | yuan/kg |
| $\pi_j$ | SKU expected profit | Same newsvendor formula as Q2, per-SKU | output | yuan |
| $\Pi^{\text{Q3}}$ | Total July 1 profit | $\Pi^{\text{Q3}} = \sum_{j \in \mathcal{J}^{\text{sel}}} \pi_j$ | **output** | yuan |

### 6.3 Demand Satisfaction

| Symbol | Name | Definition | Type | Unit |
|---|---|---|---|---|
| $D_i^{\text{ref}}$ | Reference demand for category $i$ | Avg daily sales June 24–30 | parameter | kg |
| $\gamma_i$ | Category demand satisfaction rate | $\gamma_i = \frac{\sum_{j \in \mathcal{I}_i \cap \mathcal{J}^{\text{sel}}} Q_j}{D_i^{\text{ref}}}$ | output | dimensionless |
| $\lambda$ | Demand shortfall penalty weight | Penalty coefficient in objective | parameter | yuan/kg |
| $\Pi_{\text{penalized}}^{\text{Q3}}$ | Penalized profit | $\Pi^{\text{Q3}} - \lambda \sum_i \max(0, \beta D_i^{\text{ref}} - \sum_{j \in \mathcal{I}_i} Q_j)$ | output | yuan |

---

## 7. Global Parameters

| Symbol | Name | Definition | Value | Unit | Scope |
|---|---|---|---|---|---|
| $k$ | Discount recovery rate | Empirical median of discount/regular price ratio | $0.66$ | dimensionless | Q2, Q3 |
| $\beta$ | Demand satisfaction threshold | Fraction of reference demand considered "satisfied" | [tunable] | dimensionless | Q3 |
| $N_{\min}$, $N_{\max}$ | SKU count bounds | 27 and 33 respectively | $27, 33$ | count | Q3 |

---

## 8. Cross-Question Handoff

| From | To | Symbol | Handoff |
|---|---|---|---|
| Q1 | Q2 | $\rho_{ab}$ (cross-category correlations) | Informs feature selection: which categories move together → joint optimization may benefit |
| Q1 | Q3 | $\mathbf{x}_j$ (product clusters) | Cluster labels may inform SKU diversity constraint |
| Q2 | Q3 | $\alpha_{i,t}$ (category markup rates) | Category-level markup as prior/reference for per-SKU pricing |
| Q2 | Q3 | $Q_{i,t}$ (category replenishment) | Category total as soft constraint: $\sum_{j \in \mathcal{I}_i} Q_j \approx Q_{i,t}$ |
| Q2 | Q3 | $e_i$ (price elasticity) | Per-category elasticity guides per-SKU demand adjustment |
| Q1–Q3 | Q4 | Data gaps encountered | Informs data collection recommendations |

---

## 9. Units Convention

| Quantity | Unit | Abbreviation |
|---|---|---|
| Mass (sales, replenishment) | kilogram | kg |
| Price, cost | yuan per kilogram | yuan/kg |
| Profit | yuan | yuan |
| Loss rate, markup rate, elasticity, correlation | — | dimensionless |
| Time granularity | 1 day | d |

---

## 10. Conflict Resolutions

| Conflict | Resolution |
|---|---|
| $k$ used both as cluster index (Q1) and discount rate (Q2) | Cluster index uses $k$ only within Q1 section; discount rate uses $\eta$ or $k$ with context. Prefer $k$ for discount rate (literature convention), $k$ as cluster index is local to Q1. |
| $D$ as demand vs. as day index | Use $D_{i,t}$ for demand, $t$ for time. No single $D$. |
| $P$ as price vs. as p-value | $P_{i,t}$ for price (always subscripted), $p$ (lowercase) for p-values. |
| $\pi$ as profit vs. as mathematical constant | Context disambiguates. Profit $\pi$ always subscripted with question ID. |
