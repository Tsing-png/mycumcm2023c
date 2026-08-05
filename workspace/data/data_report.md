# Data Audit Report — CUMCM 2023 Problem C

**Generated**: 2026-08-05
**Rigor**: lean (compact report, no per-file Markdown appendix)

---

## 1. Attachment Summary

| Attachment | Rows | Key Fields | Quality |
|---|---|---|---|
| 附件1 | 251 | 单品编码, 分类名称 | ✅ Clean |
| 附件2 | 878,503 | 销售日期, 销量(kg), 单价, 打折 | ⚠️ Outliers present |
| 附件3 | 55,982 | 日期, 批发价 | ⚠️ 27 near-zero prices |
| 附件4 (visible) | 251 | 损耗率(%) | ⚠️ Some 0% values |

## 2. Key Quality Issues

### Must-fix (blocking for modeling)

| # | Issue | Action |
|---|---|---|
| 1 | 27 wholesale prices ≤ 0.01 yuan/kg | Flag in cleaning; impute from nearby dates or category median |
| 2 | 5 products never sold (246/251 sold) | Exclude from analysis; document in assumptions |
| 3 | 461 returns (negative quantity) | Remove before daily aggregation |

### Should-fix (improves model quality)

| # | Issue | Action |
|---|---|---|
| 4 | 10/1095 days with zero transactions | Interpolate or accept as-is (0.9% gap) |
| 5 | 1 transaction at 160kg (next highest ~2.65kg) | Cap/winsorize at 99.9th percentile |
| 6 | 16 sales prices > 100 yuan/kg | Plausible (premium fungi/herbs), keep |
| 7 | 87 products with <30 sales days | Mark as sparse; exclude from individual prediction |
| 8 | 0% loss rate products | Verify; treat as-is or flag |

### Watch (model-dependent)

| # | Issue | Relevance |
|---|---|---|
| 9 | Category imbalance (100:5) | Q1 correlation: small categories unreliable |
| 10 | Static loss rate (not time-varying) | Q2/Q3: accept as constant assumption |
| 11 | No inventory data | Cannot validate predictions |

## 3. Data Coverage

- **Time**: 1085/1095 calendar days (99.1%)
- **Products**: 246/251 sold at least once; 47/251 with ≥365 days
- **Categories**: All 6 present throughout
- **Prices**: Wholesale prices available for all 251 products
- **Loss rates**: Available for all 251 products (visible sheet only)

## 4. Category-Level Summary (computed from visible data only)

| Category | Products | Mean Loss Rate | Notes |
|---|---|---|---|
| 花叶类 | 100 | 10.28% | Largest category |
| 食用菌 | 72 | 8.13% | |
| 辣椒类 | 45 | 8.52% | |
| 水生根茎类 | 19 | 11.97% | |
| 茄类 | 10 | 7.12% | Small N |
| 花菜类 | 5 | 14.14% | Smallest, highest loss |

## 5. Per-Question Readiness

- **Q1**: `ready_with_warnings` — remove returns, exclude never-sold products, handle sparse products
- **Q2**: `ready_with_warnings` — clean wholesale prices, aggregate to daily per category, handle static loss rate
- **Q3**: `ready_with_warnings` — compute eligible product set from June 24-30, verify 2.5kg feasibility
- **Q4**: `ready` — no data dependency beyond Q1-Q3 experience

## 6. Next Skill

→ `method-selector` — data profile is sufficient for risk probe construction during method screening.
