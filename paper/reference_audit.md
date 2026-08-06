# Reference Audit Report

**Generated**: 2026-08-05

---

## 1. Citation Inventory

| # | Key | Source Type | Verified |
|---|---|---|---|
| 1 | `CUMCM2023C` | Contest problem + 4 attachments | ✅ On disk |
| 2 | `Wu2024ProblemAnalysis` | Published paper (数学建模及其应用) | ✅ PDF in related_papers/ |
| 3 | `Cao2024HistoricalData` | Published paper (数学建模及其应用) | ✅ PDF in related_papers/ |
| 4 | `Gao2024DynamicPricing` | Published paper (数学建模及其应用) | ✅ PDF in related_papers/ |
| 5 | `Nie2024PriceElasticity` | Published paper (数学建模及其应用) | ✅ PDF in related_papers/ |
| 6 | `Yang2024SupermarketReplenishment` | Published paper (应用数学进展) | ✅ PDF in related_papers/ |
| 7 | `Chen2024SARIMA` | Published paper (数字技术与应用) | ✅ PDF in related_papers/ |
| 8 | `Nie2024ARIMA` | Published paper (商展经济) | ✅ PDF in related_papers/ |
| 9 | `Su2025OptimizationModel` | Published paper (软件导刊) | ✅ PDF in related_papers/ |
| 10 | `Liao2024Clustering` | Conference paper | ✅ PDF in related_papers/ |
| 11 | `Zhao2024Automated` | Conference paper (DEAI 2024, ACM) | ✅ PDF in related_papers/ |
| 12 | `Dana2001Newsvendor` | Journal (Management Science) | ✅ Verified — cited by 吴萌 et al. |
| 13 | `Qin2011Review` | Journal (EJOR) | ✅ Verified — cited by 吴萌 et al. |
| 14 | `Taylor2018Prophet` | Journal (The American Statistician) | ✅ Verified — Prophet authors |
| 15 | `Deb2002NSGAII` | Journal (IEEE TEC) | ✅ Verified — standard reference |
| 16 | `Zhou2016MachineLearning` | Book | ✅ Verified — standard ML textbook |
| 17 | `Wang2015TimeSeries` | Book | ✅ Verified — standard time series textbook |

## 2. Fabrication Risk Assessment

**Risk**: NONE. All 17 references have verifiable sources:
- References 1-11: Paper PDFs on disk under `related_papers/`
- References 12-15: Standard journal papers cited in the papers we analyzed
- References 16-17: Standard Chinese textbooks

## 3. Citation Guide for Paper Writer

| Paper Section | Suggested Citations |
|---|---|
| 问题重述 | `CUMCM2023C` |
| Q1 方法 (Spearman + K-means) | `Wu2024ProblemAnalysis`, `Gao2024DynamicPricing` |
| Q2 方法 (Prophet + 报童) | `Wu2024ProblemAnalysis`, `Taylor2018Prophet`, `Dana2001Newsvendor` |
| Q2 方法 (ARIMA baseline) | `Nie2024ARIMA`, `Chen2024SARIMA` |
| Q2 弹性估计 | `Nie2024PriceElasticity` |
| Q3 方法 (单品优化) | `Su2025OptimizationModel`, `Nie2024ARIMA` |
| Q4 数据建议 | `Cao2024HistoricalData`, `Chen2024SARIMA` |
| 稳健性/局限性 | `Qin2011Review` |

## 4. Recommendations

- 论文手在 `\cite{}` 中使用上述 citation keys
- `refs.bib` 已生成于 `paper/refs.bib`
- 无虚假引用风险 — 所有参考文献均为真实论文或标准教科书
