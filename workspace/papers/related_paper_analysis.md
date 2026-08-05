# Related Paper Analysis — CUMCM 2023 Problem C

**Source**: `related_papers/` (17 papers across Q1-Q4)
**Generated**: 2026-08-05
**Next skill**: `method-selector`

---

## 1. Reviewed Paper Inventory

### Most Authoritative (published in 数学建模及其应用, 2024 Vol.13 No.2 — official contest solution collection)

| # | Paper | Authors | Covers | Key Method |
|---|---|---|---|---|
| 1 | "蔬菜类商品的自动定价与补货决策" 问题解析 | 吴萌, 张驰, 王志勇 (四川大学/电子科技大学) | Q1-Q4 full | **Prophet + Newsvendor + 分布拟合** |
| 2 | 基于历史数据的蔬菜类商品定价与补货决策模型 | 曹宇轩, 黄瑞, 秦一天 (复旦大学) | Q1-Q4 full | Prophet + 模拟退火 + 遗传算法 |
| 3 | 蔬菜类商品动态定价与补货决策研究 | 高佳楠, 台明浪, 崔思雨, 李明涛 (太原理工大学) | Q1-Q4 full | K-means++ + 模拟退火 + 灰色关联分析 |
| 4 | 基于价格弹性的蔬菜类商品自动定价与补货决策 | 聂森, 潘萱颖, 曲浩栋 (武汉大学) | Q1-Q4 full | Double-log需求弹性 + LSTM + GBest-PSO + NSGA-II |

### Other Published Papers

| # | Paper | Authors | Source | Covers |
|---|---|---|---|---|
| 5 | 基于SARIMA模型的生鲜类商品自动定价与补货决策 | 陈妙霞 et al. (韩山师范学院) | 数字技术与应用 2024 | Q1-Q4 full |
| 6 | 基于ARIMA预测优化模型的生鲜类商品自动定价与补货策略研究 | 聂宇旋 (云南大学) | 商展经济 2024 | Q1-Q4 full |
| 7 | 基于优化模型的蔬菜类商品定价与补货决策 | 苏茜 et al. (云南大学) | 软件导刊 2025 | Q1-Q4 full |
| 8 | 基于超市商品补货策略的分析 | 杨若涵 et al. (北京工商大学) | 应用数学进展 2024 | Q1-Q2 partial |
| 9 | Clustering Model-based Analysis of Sales in Vegetable Categories | Liao et al. (广东工业大学/UESTC) | Conference 2024 | Q1 only |
| 10 | Automated pricing and replenishment decision model based on single-objective optimization | Zhao et al. (郑州航院) | DEAI 2024 (ACM) | Q2-Q3 partial |

---

## 2. Transferable Method Cues by Subquestion

### Q1 — Sales Distribution & Correlation

**Consensus approach across all papers:**

1. **Distribution analysis**: Aggregate sales to daily per category → visualize with line charts → remove time effects (optional but recommended) → fit distributions
2. **Correlation**: Spearman (data is non-normal per K-S test) or Pearson. Heatmap visualization.
3. **Clustering**: K-means++ to group products/items by sales patterns (magnitude + fluctuation). Elbow method for K.

**Key finding from 吴萌 et al. (authoritative)**: 
- After removing Prophet time components, best-fit distributions: 花菜类/茄类→Lognormal, 花叶类/辣椒类→Generalized Gamma, 食用菌→Normal, 水生根茎类→Cauchy
- Correlation should consider price as confounding variable, not just raw sales correlation

**Data preprocessing consensus**:
- Aggregate to daily level (not transaction-level)
- Remove returns (退货 0.05%, negligible)
- Discount data: either exclude or treat as regular sales (吴萌 uses option 2 — treat as regular)
- Filter products with sufficient sales continuity (avoid sparse products)

### Q2 — Category-level Replenishment & Pricing

**Two main method families:**

| Family | Papers | Demand Model | Optimization |
|---|---|---|---|
| **Prophet + Newsvendor** | 吴萌, 曹宇轩 | Prophet分解+价格外生变量 | 报童模型/非线性规划 + 模拟退火/遗传算法 |
| **ARIMA/LSTM + NLP** | 聂森, 陈妙霞, 聂宇旋, Zhao | ARIMA/LSTM预测 + 价格弹性修正 | 非线性规划 + PSO/贪心 |

**Core framework (吴萌 — most transferable)**:
1. Decompose sales time series with Prophet → extract trend, season, holiday effects
2. Fit demand distribution on residuals
3. Build newsvendor model: profit = revenue − cost − loss
4. Cost-plus pricing: `price = wholesale × (1 + markup)`, with markup as decision variable
5. Actual cost: `wholesale / (1 − loss_rate)` to account for wastage
6. Optimize markup + order quantity jointly

**Demand-price relationship**:
- 聂森: Double-log model `ln(Q) = α + Σe·ln(P) + ...` → price elasticity estimates (all negative, confirming law of demand)
- 聂宇旋: Fit linear/log/power functions per category, pick best by R²
- 曹宇轩: Prophet with price as exogenous regressor

### Q3 — SKU-level Replenishment

**Key methods across papers:**

| Paper | SKU Selection | Optimization |
|---|---|---|
| 苏茜 | Knapsack formulation | Greedy + solver |
| 聂森 | VIKOR multi-criteria ranking (sales volume + frequency) | NSGA-II multi-objective (profit + demand satisfaction) |
| 曹宇轩 | Dynamic programming | DP with space constraint |
| 聂宇旋 | Greedy by unit profit | Per-category knapsack (6 backpacks) |
| 高佳楠 | Based on K-means clusters | Simulated annealing |

**Common pattern**:
1. Filter: products appearing in June 24-30 sales data (~45-49 products)
2. Rank: by profit margin, demand, or VIKOR score
3. Select: top 27-33 products satisfying ≥2.5kg display minimum
4. Optimize: per-SKU quantity + pricing

### Q4 — Additional Data Recommendations

**Common suggestions across papers**:
1. **Weather data** (temperature, humidity, precipitation) — affects demand and spoilage
2. **Holiday/event calendar** — Prophet already handles, but granular local events matter
3. **Competitor pricing and promotions** — competitive intelligence
4. **Consumer feedback/surveys** — preference and satisfaction
5. **Origin/supply chain data** — supply stability, brand effects (曹宇轩 notes product names encode origin codes)
6. **Inventory/stockout records** — distinguish zero-sales-due-to-no-demand vs. zero-sales-due-to-stockout
7. **Promotional campaign data** — planned discounts vs. clearance

---

## 3. Useful Assumptions, Variables & Validation Ideas

### Assumptions worth adopting:
- Historical sales represent future demand trends (all papers)
- Loss rate is constant over the prediction horizon (all papers)
- Supply is stable (no disruption events)
- Single-period inventory (perishable — today's stock can't sell tomorrow)

### Variable definitions worth standardizing:
- `α_i`: markup rate for category i (decision variable)
- `C_i(t)`: wholesale price for category i at time t
- `P_i(t) = (1+α_i(t)) × C_i(t)`: selling price
- `L_i`: loss rate for category i
- `Q_i`: order/replenishment quantity
- `D_i`: realized demand/sales
- Profit = `Σ[P_i × min(Q_i, D_i) + k × P_i × max(0, Q_i-D_i) − C_i × Q_i/(1−L_i)]` where k≈0.7 is discount recovery rate (聂森)

### Validation ideas:
- Compare Prophet vs. ARIMA vs. LSTM for time series prediction (R², RMSE, MAE)
- Compare optimized profit vs. naive baseline (historical mean order + fixed markup)
- Sensitivity: vary loss rate ±20%, price elasticity ±20%
- Robustness: compare different optimization algorithms on same formulation

---

## 4. Risks of Direct Reuse

| Risk | Details |
|---|---|
| **Hidden sheet in 附件4** | Multiple papers likely used the hidden category-level loss rates directly. We must compute from visible item-level data only. |
| **Prophet model complexity** | 吴萌 and 曹宇轩 use Prophet — effective but requires careful tuning. ARIMA is a simpler fallback. |
| **Pandemic-period data** | 2020-2023 includes COVID. Demand patterns may be distorted. Papers don't address this. |
| **Overfitting demand functions** | Some papers overfit polynomial demand functions (苏茜 uses up to degree-6 polynomials on monthly data). Prefer simpler forms. |
| **Discount rate k=0.7** | 聂森 estimates k≈0.7 for discount recovery. This is an empirical estimate from the data — verify independently. |
| **Neural network overkill** | LSTM (聂森) adds complexity without guaranteed improvement over ARIMA/Prophet for 3-year daily data. |
| **Missing inventory data** | No paper can verify predictions against actual 2023 July data — all validation is on historical holdout. |

---

## 5. Missing Evidence

- No paper provides code or reproducible experiments
- No paper validates Q2 results against actual July 2023 data (unavailable)
- Category-level loss rate computation method is inconsistent (hidden vs. computed)
- No consensus on whether to use 品类级 or 单品级 for loss rate in Q2 optimization
- Q3 space constraint is qualitative — no paper quantifies it

---

## 6. Recommended Next Skill

→ **`method-selector`**

Before method selection, ensure:
- [ ] Data audit (`data-auditor-cleaner`) is complete
- [ ] Choice card for method priorities (interpretability vs. performance, experiment budget) is presented to human

### Key handoff messages for method-selector:

**Q1**: Spearman correlation + K-means++ clustering is the dominant approach. Prophet-based time decomposition (吴萌) is the most rigorous but optional for Q1 alone — it becomes critical for Q2.

**Q2**: Newsvendor framework (吴萌) is the most principled. ARIMA + nonlinear optimization is the simpler alternative. Simulated annealing or PSO for solving the nonlinear program.

**Q3**: Knapsack + greedy (苏茜, 聂宇旋) is simplest. VIKOR + NSGA-II (聂森) is most sophisticated. The choice depends on how we handle the multi-objective nature.

**Q4**: Qualitative — informed by Q1-Q3 experience. Grey relational analysis (高佳楠) provides a quantitative angle but is optional.
