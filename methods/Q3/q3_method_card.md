# Q3 Method Card — SKU-level Replenishment & Pricing

## Goal and success criteria
- **Goal**: Select 27-33 SKUs from June 24-30 available products, determine per-SKU replenishment (≥2.5kg) and pricing for July 1, maximizing single-day profit while satisfying category-level market demand (penalty in objective).
- **Success**: SKU selection explainable (historical sales, profit margin, demand complementarity); quantities and prices in reasonable ranges; category demand satisfaction vs profit trade-off quantifiable.

## Human constraints
- Output form: Selected SKU list (27-33) with per-SKU quantity (kg) and price (yuan/kg); expected profit; per-category demand satisfaction rate
- Priority: Interpretability first — selection criteria must be auditable
- Unacceptable failure: Output degeneracy (all selected SKUs from one category, all same quantity)
- Experiment budget: Light (<5 min for selection + optimization)

## Shortlist

| ID | Role | Mathematical idea | Why eligible | Main risk | Implementation cost |
|---|---|---|---|---|---|
| M1 | **main_candidate** | Knapsack formulation + greedy selection by profit-density + per-SKU newsvendor pricing (extending Q2 framework) | Literature consensus (苏茜, 聂宇旋). Knapsack is the natural formulation for subset selection under space constraint. Greedy is fast, interpretable, and provably near-optimal for fractional relaxation. Per-SKU newsvendor extends Q2 M1 consistently. | Greedy may miss globally optimal combination (complementary products); 2.5kg minimum may exclude some high-margin low-volume products | Low — numpy + custom greedy |
| M2 | **usable_baseline** | Top-N by historical revenue + historical-mean replenishment + per-SKU historical-average markup | Simplest implementable strategy. No optimization — purely data-driven selection. Directly comparable on profit and demand satisfaction. | No optimization at all — purely backward-looking; may select products with declining trends | Low — pandas aggregation |
| M3 | **conditional_fallback** | VIKOR multi-criteria ranking (demand + frequency) + NSGA-II multi-objective optimization (profit + demand satisfaction Pareto) | 聂森 et al. (2024). VIKOR provides principled multi-criteria ranking. NSGA-II generates Pareto frontier for profit-demand trade-off. | NSGA-II exceeds light-compute budget; VIKOR weights require human judgment | High — custom evolutionary algorithm |

## Baseline validity
- Real task completed: Yes — M2 produces SKU selection, quantities, and pricing
- Comparable output/metric: Yes — single-day profit and demand satisfaction rate directly comparable
- If no, classification: N/A

## Fallback trigger
- **Trigger**: M1 greedy solution shows demand satisfaction <50% for any single category
- **Evidence to evaluate**: Per-category demand satisfaction rates from M1 solution

## Risk-probe summary
| ID | Executability | Data/assumptions | Degeneracy | Sensitivity | Scale | Verdict |
|---|---|---|---|---|---|---|
| M1 | Pending probe | Pending probe | Pending probe | Pending probe | Pending probe | — |
| M2 | Pending probe | Pending probe | Pending probe | Pending probe | Pending probe | — |
| M3 | — | — | — | — | Exceeds compute budget | CONDITIONAL (trigger only) |

## Compact history
- 2026-08-05: Initial method card. M1=Knapsack+greedy+Newsvendor, M2=Top-N by revenue+historical mean, M3=VIKOR+NSGA-II (fallback only). Probe deferred until Q2 framework is built.
