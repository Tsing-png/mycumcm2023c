# Model Assumptions — CUMCM 2023 Problem C

**Generated**: 2026-08-05
**Status**: pending human review (necessary/simplifying labels)

---

## A. Global Assumptions (All Questions)

### A1. Single-Period Perishability
- **Statement**: 蔬菜当日未售出，隔日无法再售。Each day is an independent inventory cycle.
- **Scope**: Q2, Q3 (not Q1 — descriptive only)
- **Source**: Problem statement
- **Modeling need**: Justifies newsvendor (single-period) framework for Q2/Q3
- **Type**: **necessary** (decided by human, H1)
- **Validation**: Descriptive; matches problem statement
- **Impact if violated**: Would require multi-period dynamic programming instead of single-period newsvendor
- **Mitigation**: None needed — this is the problem's core constraint
- **Decision ID**: `assumption_A1_single_period`

### A2. Cost-Plus Pricing
- **Statement**: 定价采用成本加成定价方法：$P = (1 + \alpha) \cdot C$
- **Scope**: Q2, Q3
- **Source**: Problem statement ("一般采用成本加成定价方法")
- **Modeling need**: Defines the pricing decision variable ($\alpha$) and links cost to price
- **Type**: **necessary** (decided by human, H2)
- **Validation**: Verified from data — markup rates are positive and vary across categories
- **Impact if violated**: Pricing model would need alternative formulation (e.g., value-based pricing)

### A3. Passive Discount Clearance
- **Statement**: 打折销售是被动清仓行为，未售出商品以折扣价 $k \cdot P$ 清仓，$k=0.66$ (数据中位数)
- **Scope**: Q2, Q3
- **Source**: Problem statement ("对运损和品相变差的商品通常进行打折销售") + Human decision (`framing_discount_policy`)
- **Modeling need**: Defines overage cost in newsvendor model
- **Type**: simplifying (decided by human)
- **Decision ID**: `framing_discount_policy`
- **Validation**: $k$ empirically estimated from data. Sensitive — probe shows profit varies ±50% for $k \in [0.3, 0.9]$
- **Impact if violated**: If discounting is strategic (not passive clearance), the single-period profit function changes
- **Mitigation**: Report results under $k \in \{0.5, 0.66, 0.75\}$

### A4. Historical Data Representativeness
- **Statement**: 2020-07 ~ 2023-06 历史销售数据可以代表 2023年7月的需求模式
- **Scope**: Q1, Q2, Q3
- **Source**: Modeling necessity
- **Modeling need**: All time-series models (Prophet, ARIMA) assume past patterns continue
- **Type**: **necessary** (decided by human, H3)
- **Validation**: Cannot fully validate — July 2023 actual data unavailable. Holdout test on June 2023 shows reasonable RMSE
- **Impact if violated**: Predictions systematically biased
- **Mitigation**: Use 30-day holdout evaluation; report prediction intervals
- **Decision ID**: `assumption_A4_representativeness`

### A5. COVID Period Inclusion
- **Statement**: 2020-2023数据包含疫情期间，但不单独处理疫情效应
- **Scope**: Q1, Q2
- **Source**: Data coverage
- **Modeling need**: Prophets' yearly seasonality averages over all 3 years including COVID
- **Type**: simplifying
- **Validation**: Cannot isolate COVID effect without external data
- **Impact if violated**: 2020-2021 demand patterns may differ from 2023; Prophet may learn distorted seasonality
- **Mitigation**: Prophet's flexibility with changepoints partially adapts; noted as limitation

---

## B. Data Assumptions

### D1. Visible Sheet Only for 附件4
- **Statement**: 仅使用附件4可见Sheet1（单品级损耗率），品类级损耗率自行计算。隐藏sheet不可用
- **Scope**: Q2, Q3
- **Source**: Data audit discovery
- **Modeling need**: Loss rate input for cost calculation
- **Type**: necessary
- **Validation**: Verified that visible data + 附件1 join produces category-level loss rates
- **Impact if violated**: Using hidden sheet would give different (possibly more accurate) category-level rates

### D2. Static Loss Rate
- **Statement**: 损耗率为近期盘点值，假设在预测期内恒定
- **Scope**: Q2, Q3
- **Source**: 附件4 documentation ("近期盘点周期的数据")
- **Modeling need**: Simplifies cost calculation — avoids modeling time-varying spoilage
- **Type**: simplifying
- **Validation**: Probe shows CF insensitive to ±20% loss rate variation
- **Impact if violated**: If loss rate varies significantly day-to-day, optimal order quantities would shift

### D3. Returns Negligible
- **Statement**: 退货 461/878,503 (0.05%) 忽略不计
- **Scope**: Q1, Q2, Q3
- **Source**: Data audit
- **Modeling need**: Simplifies data processing
- **Type**: simplifying
- **Validation**: 0.05% — negligible by any standard
- **Impact if violated**: None meaningful

### D4. Near-Zero Wholesale Prices
- **Statement**: 27条批发价≤0.01元/kg的记录排除于加成率计算
- **Scope**: Q2, Q3
- **Source**: Data audit
- **Modeling need**: Prevents division-by-zero and nonsensical markup rates
- **Type**: necessary (data cleaning)
- **Validation**: 27/55,982 = 0.05%
- **Impact if violated**: Distorted markup statistics

### D5. Never-Sold Products Excluded
- **Statement**: 5个从未销售的单品排除出所有分析
- **Scope**: Q1, Q2, Q3
- **Source**: Data audit
- **Modeling need**: No data → no analysis possible
- **Type**: necessary
- **Validation**: 5/251 = 2%

---

## C. Q1 Assumptions

### Q1.1. Non-Normal Sales Distribution
- **Statement**: 各品类日销售量不服从正态分布（全部6品类p<0.000001）
- **Scope**: Q1
- **Source**: Risk probe
- **Modeling need**: Justifies Spearman over Pearson correlation
- **Type**: necessary (verified by data)
- **Validation**: D'Agostino-Pearson test on all 6 categories
- **Impact if violated**: If data were normal, Pearson would be valid and more efficient

### Q1.2. Sparse-Product Filtering
- **Statement**: 单品聚类分析仅使用销售天数≥30的单品（159/246），稀疏单品标记但不纳入聚类
- **Scope**: Q1
- **Source**: Method design
- **Modeling need**: Clustering requires stable feature estimates
- **Type**: simplifying
- **Validation**: 159 products retained; 87 sparse products with unreliable statistics excluded
- **Impact if violated**: Noisy features would degrade cluster quality

### Q1.3. Correlation ≠ Causation Boundary
- **Statement**: 关联分析仅揭示统计相关性，不做因果推断
- **Scope**: Q1
- **Source**: Problem classification
- **Modeling need**: Defines the scope of Q1 conclusions
- **Type**: necessary (inferential boundary)
- **Validation**: N/A — this is a scope constraint, not a testable claim

---

## D. Q2 Assumptions

### Q2.1. Prophet Decomposition Adequacy
- **Statement**: 销量时间序列可分解为 $y(t) = g(t) + s(t) + h(t) + \varepsilon$，其中 $g$ 为趋势，$s$ 为周+年季节性，$h$ 为中国节假日效应
- **Scope**: Q2 M1
- **Source**: Prophet model specification; 吴萌 et al. (2024)
- **Modeling need**: Core model structure
- **Type**: **simplifying** (decided by human, H4)
- **Validation**: Components are meaningful amplitudes (trend:145, weekly:75, yearly:145 for 花叶类). Holdout RMSE acceptable.
- **Impact if violated**: If additional factors (e.g., weather, promotions) dominate, Prophet underfits
- **Mitigation**: Compare with ARIMA baseline (M2); if ARIMA significantly better, trigger fallback
- **Decision ID**: `assumption_Q2.1_prophet_decomposition`

### Q2.2. Demand Distribution After Decomposition
- **Statement**: Prophet残差用经验分位数（非参数）估计报童模型的分位数 $F^{-1}(\Phi)$
- **Scope**: Q2 M1
- **Source**: 吴萌 et al. (2024); risk probe finding
- **Modeling need**: Newsvendor requires demand CDF $F^{-1}(\Phi)$
- **Type**: **simplifying** (decided by human, H6 — use empirical quantiles)
- **Validation**: Residuals are NOT normal (p<0.000001) — parametric fit would be invalid
- **Impact if violated**: N/A — this is the more robust choice
- **Mitigation**: Empirical quantiles are assumption-free; bootstrap CI for robustness
- **Decision ID**: `assumption_Q2.2_empirical_quantiles`

### Q2.3. Price Elasticity Estimates
- **Statement**: 品类价格弹性 $e_i$ 需从自己的数据重新估计（Double-log模型或Prophet价格回归），不照搬聂森 et al.
- **Scope**: Q2 M1, Q3 M1
- **Source**: Human decision (H5)
- **Modeling need**: Demand-price adjustment in newsvendor optimization
- **Type**: **simplifying** (decided by human, H5 — estimate from own data)
- **Validation**: Will be estimated during implementation and compared with 聂森's values as sanity check
- **Impact if violated**: Using others' elasticity estimates may not fit our data
- **Mitigation**: Compare own estimates with 聂森's; flag large discrepancies
- **Decision ID**: `assumption_Q2.3_own_elasticity`

### Q2.4. Constrained Order Quantity
- **Statement**: $Q_{i,t} \leq 1.5 \times \max_{\tau} S_{i,\tau}$（订货量不超过历史最大日销量的1.5倍）
- **Scope**: Q2 M1
- **Source**: Risk probe mitigation (CF>1 for some categories with k=0.7)
- **Modeling need**: Prevents unbounded orders when effective cost < discount price
- **Type**: simplifying (practical bound)
- **Validation**: Reasonable business constraint — supermarket cannot store >1.5× historical peak
- **Impact if violated**: Without bound, optimizer may recommend unreasonably large orders for high-margin categories

### Q2.5. No Space Constraint in Q2
- **Statement**: Q2不考虑销售空间约束（题目仅在Q3提出）
- **Scope**: Q2
- **Source**: Human decision (`framing_q2_space_constraint`)
- **Type**: simplifying (decided by human)
- **Decision ID**: `framing_q2_space_constraint`
- **Impact if violated**: If space IS binding, Q2 optimal quantities may be infeasible; Q3 would need to reconcile

---

## E. Q3 Assumptions

### Q3.1. Filter-Based Selection
- **Statement**: 日均销量≥2.5kg的单品全部入选（31个），无需组合优化选品
- **Scope**: Q3 M1
- **Source**: Risk probe finding
- **Modeling need**: Eliminates combinatorial selection problem
- **Type**: simplifying (data-driven)
- **Validation**: Filter threshold 2.3-3.0kg all yield 30-31 products within [27,33]
- **Impact if violated**: If threshold sensitivity were high, would need explicit selection algorithm
- **Mitigation**: If filtered count falls outside [27,33], adjust threshold or activate M3 fallback

### Q3.2. Demand Satisfaction as Penalty
- **Statement**: 品类需求满足作为惩罚项而非硬约束：$\Pi_{\text{penalized}} = \Pi - \lambda \sum_i \max(0, \beta D_i^{\text{ref}} - \sum Q_j)$
- **Scope**: Q3 M1
- **Source**: Human decision (`framing_q3_demand_satisfaction`)
- **Type**: simplifying (decided by human)
- **Decision ID**: `framing_q3_demand_satisfaction`
- **Validation**: With filter-based selection, all categories satisfy >100% — penalty term may be inactive
- **Impact if violated**: Different formulation (e.g., hard constraint) would change the optimization structure

### Q3.3. June 24-30 Representative of July 1 Demand
- **Statement**: 6月24-30日销售模式代表7月1日需求
- **Scope**: Q3
- **Source**: Problem statement ("根据2023年6月24-30日的可售品种")
- **Modeling need**: Defines candidate product set and reference demand
- **Type**: necessary (directed by problem)
- **Validation**: One-week gap — reasonable for stable product assortment
- **Impact if violated**: Relevant products or demand levels could change in one week

---

## F. Profit Function

### F1. Profit Definition
- **Statement**: $\pi = P \cdot \mathbb{E}[\min(Q,D)] + kP \cdot \mathbb{E}[(Q-D)^+] - \frac{C}{1-L} \cdot Q$
- **Scope**: Q2, Q3
- **Source**: Human decision (`framing_profit_function`)
- **Modeling need**: Objective function
- **Type**: necessary (decided by human)
- **Decision ID**: `framing_profit_function`
- **Components**: Revenue from regular sales + revenue from discounted clearance − effective cost (including loss)
- **Impact if violated**: Alternative definitions change optimal decisions

---

## G. Resolved Human Decisions

| # | Decision | Choice | Decision ID |
|---|---|---|---|
| H1 | A1 single-period | necessary | `assumption_A1_single_period` |
| H2 | A2 cost-plus pricing | necessary | `assumption_A2_cost_plus` |
| H3 | A4 historical representativeness | necessary | `assumption_A4_representativeness` |
| H4 | Q2.1 Prophet decomposition | simplifying | `assumption_Q2.1_prophet_decomposition` |
| H5 | Q2.3 price elasticity source | estimate from own data | `assumption_Q2.3_own_elasticity` |
| H6 | Q2.2 demand distribution | empirical quantiles (non-parametric) | `assumption_Q2.2_empirical_quantiles` |

---

## Compact History
- 2026-08-05: Initial assumptions built from problem parse, method cards, risk probes, and human framing decisions.
