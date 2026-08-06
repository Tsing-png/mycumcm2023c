# 论文手材料包 — CUMCM 2023 Problem C

**生成时间**: 2026-08-05
**Rigor**: submission
**覆盖**: Q1, Q2, Q3, Q4

> 本文档是论文手的唯一材料来源。所有数值结论均可溯源至具体文件。不要从散落的结果文件中猜测。

---

## Q1 — 蔬菜销售量分布规律与相互关系

### 核心结论

1. **品类间 Spearman ρ ∈ [−0.194, 0.625]**，花叶类↔花菜类最强 (ρ=0.625)，茄类↔水生根茎类唯一负相关 (ρ=−0.194)
2. **6/6 品类拒绝正态性** (p < 10⁻⁷⁵)，Pearson 相关不适用（方向一致性仅 86.7%）
3. **K-means K=2**（Silhouette=0.463）：低量高波动簇(72) vs 高量中波动簇(87)
4. 最优分布拟合：**对数正态**适用于 5/6 品类，水生根茎类拟合较弱 (KS p=0.008)
5. 跨年稳定性：2022 年茄类关联结构变化（疫情恢复效应），其余 5 品类关联增强

### 数值来源

| 数据 | 文件 |
|---|---|
| Spearman 矩阵 | `results/Q1/experiments/round1/tables/q1_spearman_corr.csv` |
| Pearson 矩阵 | `results/Q1/experiments/round1/tables/q1_pearson_corr.csv` |
| 聚类分配 | `results/Q1/experiments/round1/tables/q1_cluster_assignments.csv` |
| 分布参数 | `results/Q1/experiments/round1/tables/q1_distribution_params.csv` |
| M1 vs M2 对比 | `results/Q1/experiments/round1/metrics/q1_comparison.json` |

### 论文图表

| 图表 | 文件 | 用途 |
|---|---|---|
| Fig 1: Spearman 热力图 | `figures/q1_corr_heatmap_spearman.png` | Type 3 |
| Fig 2: 月度销售量趋势 | `figures/q1_monthly_sales_trend.png` | Type 3 |
| Table 1: 分布拟合参数 | `tables/q1_distribution_params.csv` | Type 3 |

### 方法来源

`methods/Q1/q1_final_method_explanation.md` — 完整公式、假设、求解过程

---

## Q2 — 品类级补货与定价

### 核心结论

1. **单日最优总利润：2,918 元**，七日估计：20,427 元（M1 Prophet + 报童）
2. Baseline (ARIMA+固定加成) 单日利润：723 元，M1 增益 **+304%**
3. 最优加成率范围：**103.6%–128.2%**（品类间有区分度，std=0.082）
4. 折扣回收率 k=0.66 是唯一敏感参数——利润区间 [2,362, 3,713]（k∈[0.5,0.75]）
5. 损耗率和价格弹性对利润几乎无影响（模型稳健）

### 最优策略（7月1日）

| 品类 | 加成率 | 售价 (元/kg) | 订货量 (kg) | 利润 (元) |
|---|---|---|---|---|
| 水生根茎类 | 103.6% | 24.51 | 54.7 | 287 |
| 花叶类 | 116.7% | 6.46 | 254.3 | 854 |
| 花菜类 | 104.6% | 22.82 | 79.3 | 316 |
| 茄类 | 113.2% | 20.04 | 53.3 | 162 |
| 辣椒类 | 128.2% | 18.21 | 183.5 | 699 |
| 食用菌 | 113.0% | 10.12 | 174.6 | 599 |
| **合计** | | | | **2,918** |

> 七日策略基于每日独立运行 Prophet 预测+报童优化。使用相同的加成率框架，但每日的需求预测和成本基准随新数据更新。

### 自有弹性 vs 论文对比

| 品类 | 自有 | 聂森 (2024) |
|---|---|---|
| 水生根茎类 | −1.01 | −0.03 |
| 花叶类 | −0.23 | −1.92 |
| 花菜类 | −0.73 | −0.26 |

### 数值来源

| 数据 | 文件 |
|---|---|
| M1 策略表 | `results/Q2/experiments/round1/tables/q2_m1_optimal_policy.csv` |
| M2 baseline | `results/Q2/experiments/round1/tables/q2_m2_baseline_policy.csv` |
| 弹性估计 | `results/Q2/experiments/round1/tables/q2_elasticity_estimates.csv` |
| 稳健性 | `robustness/Q2/q2_robustness_summary.json` |

### 论文图表

| 图表 | 文件 | 用途 |
|---|---|---|
| Fig 3: Prophet 分量 (花叶类) | `figures/q2_prophet_components_花叶类.png` | Type 3 |
| Fig 4: 加成率对比 | `figures/q2_markup_comparison.png` | Type 2 |
| Table 2: 最优补货定价策略 | 上表 | Type 3 |
| Table A1: k 敏感性 | 稳健性报告 | Type 4 |

### 方法来源

`methods/Q2/q2_final_method_explanation.md`

---

## Q3 — 单品级补货与定价

### 核心结论

1. **31 个单品入选**（过滤 ≥2.5kg，恰好落 [27,33]），全部 6 品类有代表
2. **单日总利润：1,327 元**（M1 单品报童），Baseline 465 元，增益 **+185%**
3. 品类需求满足率：**78.6%–190.0%**，全部 >50% fallback 阈值
4. 加成率 std=0.311（单品间有充分区分度）
5. 过滤阈值 2.3–3.0 kg 均稳定产出 30–31 个单品

### 各品类需求满足

| 品类 | 订货量 (kg) | 需求基准 (kg) | 满足率 |
|---|---|---|---|
| 水生根茎类 | 17.1 | 16.7 | 78.6% |
| 花叶类 | 142.7 | 124.8 | 178.9% |
| 花菜类 | 28.2 | 16.2 | 152.2% |
| 茄类 | 39.2 | 19.0 | 190.0% |
| 辣椒类 | 132.0 | 77.6 | 155.2% |
| 食用菌 | 77.1 | 44.2 | 187.6% |

### 数值来源

| 数据 | 文件 |
|---|---|
| M1 单品策略 | `results/Q3/experiments/round1/tables/q3_m1_sku_policy.csv` |
| M2 baseline | `results/Q3/experiments/round1/tables/q3_m2_baseline_policy.csv` |
| 稳健性 | `robustness/Q3/q3_robustness_summary.json` |

### 论文图表

| 图表 | 文件 | 用途 |
|---|---|---|
| Fig 5: 需求满足率 | `figures/q3_category_satisfaction.png` | Type 3 |
| Table 3: 单品策略（精简） | 31 行核心表 | Type 3 |
| Table A2: 阈值敏感性 | 稳健性报告 | Type 4 |

### 方法来源

`methods/Q3/q3_final_method_explanation.md`

---

## Q4 — 数据采集建议

### 核心结论

| 优先级 | 建议数据 | 对应问题 | 核心价值 |
|---|---|---|---|
| **高** | 每日库存与缺货记录 | Q2, Q3 | 区分零销量=无需求 vs 缺货 |
| **高** | 折扣原因分类码 | Q2 | 提高 k 估计精度（最敏感参数） |
| **高** | 天气数据 | Q2, Q3 | 解释 Prophet 残差结构 |
| **中** | 单品上下架时间表 | Q1, Q3 | 区分季节性 vs 零需求 |
| **中** | 促销活动日历 | Q2 | 分离促销与自然需求 |
| **中** | 竞争对手价格 | Q2 | 改善弹性估计 |
| **低** | 消费者调查/货架/产地 | Q3, Q2 | 辅助优化 |

### 方法来源

`methods/Q4/q4_data_recommendations.md`

---

## 全局数值汇总

| 指标 | 值 | 来源 |
|---|---|---|
| Q2 单日总利润 (M1) | **2,918 元** | q2_m1_optimal_policy.csv |
| Q2 七日总利润 (M1) | **~20,427 元** | run_summary (×7) |
| Q2 单日总利润 (M2) | 723 元 | q2_m2_baseline_policy.csv |
| Q3 单日总利润 (M1) | **1,327 元** | q3_m1_sku_policy.csv |
| Q3 单日总利润 (M2) | 465 元 | q3_m2_baseline_policy.csv |
| k 折扣率 | 0.66 | 数据中位数 |
| k 利润区间 (Q2) | [2,362, 3,713] | 稳健性 |
| Q3 入选单品 | 31 个 | 过滤 ≥2.5kg |

## 方法汇总

| Q | 主方法 | Baseline | Fallback |
|---|---|---|---|
| Q1 | Spearman + K-means++ | Pearson (diagnostic only) | — |
| Q2 | Prophet + Constrained Newsvendor | ARIMA + Fixed Markup | Double-log + LSTM |
| Q3 | Filter ≥2.5kg + Per-SKU Newsvendor | Fixed markup | Per-category quota |
| Q4 | Gap analysis from Q1-Q3 experience | Literature synthesis | — |

## 关键假设提醒论文手

- 单周期库存（当日未售隔日作废）— 题目原话
- 成本加成定价 — 题目要求
- 打折为被动清仓，k=0.66 — 人工确认 (`framing_discount_policy`)
- 报告 k∈{0.50, 0.75} 区间值 — 稳健性要求
- 价格弹性从自有数据估计 — 人工确认 (`assumption_Q2.3_own_elasticity`)
- 仅使用附件4可见Sheet1 — 数据审计发现
