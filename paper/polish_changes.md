# Paper Polish — Change Summary

**Date**: 2026-08-05
**Sections reviewed**: 8/8

---

## Changes Applied

| Section | Change | Reason |
|---|---|---|
| 01_abstract L3 | 拆分超长句（127字→两句），首句新增"商超需每日做出补货与定价决策"的背景锚点 | 句子长度，可读性 |
| 01_abstract L13 | "所有数值结论均经过稳健性检验" → "关键数值结论均经过参数扰动和敏感性检验" | 降级过度声明；并非所有数值都有稳健性检验（如Q1分布拟合参数） |
| 05_q2 L7 | $S_i(t)$ → $S_{i,t}$ | 符号一致性：全文统一使用 $S_{i,t}$ |
| 05_q2 L9 | "三个分量均有显著的实际意义" → 具体数值描述 | 去除AI-味空泛表达，替换为具体数据 |
| 05_q2 L77-79 | 扩充"七日策略"段（1句→4句），补充七日总利润和k区间 | 原文过薄，补充关键数值 |
| 08_evaluation L5 | "具有明确的业务含义" → "可直接对应商超的经营决策变量" | 去除空泛套话，替换为具体表述 |

## 12-Point Checklist Summary

| # | Check | Status |
|---|---|---|
| 1 | Sentence length | ✅ 超长句已拆分 |
| 2 | Paragraph structure | ✅ 每段一个主题句 |
| 3 | Tense consistency | ✅ 中文论文，时态一致 |
| 4 | Hedging calibration | ✅ 降级一处过度声明 |
| 5 | Overclaim detection | ✅ 未发现虚假声称；"最优"仅用于优化问题上下文中（即网格搜索最优解） |
| 6 | Formula formatting | ✅ 显示/行内公式分离正确 |
| 7 | Notation consistency | ✅ $S_{i,t}$ 全文统一 |
| 8 | Figure/table references | ✅ 5图1表，顺序正确 |
| 9 | Transition and flow | ✅ 节间有桥接句 |
| 10 | Word choice | ✅ 去除"显著的实际意义""明确的业务含义"等空泛表述 |
| 11 | Voice | ✅ 中文论文，"本文"一致性使用 |
| 12 | Formatting compliance | ✅ 标题层级、公式编号一致 |

## AI-味表达清除

| 位置 | 原表述 | 问题 | 修改 |
|---|---|---|---|
| Q2 | "三个分量均有显著的实际意义" | 空泛声明，无数据支撑 | 替换为具体振幅数值 |
| 评价 | "具有明确的业务含义" | 套话 | "可直接对应商超的经营决策变量" |
| 摘要 | "所有数值结论均经过稳健性检验" | 过度声明 | 降级为"关键数值结论" |

## No Blocking Issues

所有数值声明均溯源至 frozen_numbers.json。所有图表引用对应已存在的 paper/figures/ 文件。无虚假引用。
