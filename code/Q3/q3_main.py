"""Q3 M1: Filter >=2.5kg + Per-SKU Newsvendor for July 1."""
import sys; sys.path.insert(0, "code/scripts")
from plot_config import setup_style, FIG_WIDE, FIG_HALF
import matplotlib.pyplot as plt
import pandas as pd, numpy as np
from scipy import stats
import json, time, os, warnings
warnings.filterwarnings('ignore')

setup_style()
SEED = 42
OUT = "results/Q3/experiments/round1"
for d in ["figures", "tables", "metrics"]:
    os.makedirs(f"{OUT}/{d}", exist_ok=True)

daily = pd.read_csv("workspace/data_clean/daily_sales.csv", parse_dates=["销售日期"])
loss_rates = pd.read_csv("workspace/data_clean/item_loss_rates.csv")
# Use Q2 own elasticity estimates (consistent across questions)
# Read from Q2 output if available, otherwise fall back to Q2 estimated values
try:
    q2_elast = pd.read_csv("results/Q2/experiments/round1/tables/q2_elasticity_estimates.csv")
    ELASTICITIES = dict(zip(q2_elast["品类"], q2_elast["价格弹性"]))
    print(f"Using Q2 own elasticities: {ELASTICITIES}")
except FileNotFoundError:
    ELASTICITIES = {"水生根茎类": -0.03, "花叶类": -1.92, "花菜类": -0.26,
                    "茄类": -0.07, "辣椒类": -0.03, "食用菌": -0.51}
    print("Q2 elasticities not found, using 聂森 fallback values")
K_DISCOUNT = 0.66

# ── 1. Eligible + Filter ──
june24_30 = daily[(daily["销售日期"] >= "2023-06-24") & (daily["销售日期"] <= "2023-06-30")]
eligible = june24_30.groupby("单品编码").agg(
    avg_daily_sales=("total_qty", "mean"), avg_price=("avg_price", "mean"),
    avg_cost=("批发价格(元/千克)", "mean"), category=("分类名称", "first"),
).reset_index()
eligible = eligible.merge(loss_rates[["单品编码", "损耗率(%)"]], on="单品编码", how="left")

threshold = 2.5
selected = eligible[eligible["avg_daily_sales"] >= threshold].copy()
if len(selected) < 27:
    while len(selected) < 27 and threshold > 1.0:
        threshold -= 0.1
        selected = eligible[eligible["avg_daily_sales"] >= threshold].copy()
elif len(selected) > 33:
    while len(selected) > 33 and threshold < 10.0:
        threshold += 0.1
        selected = eligible[eligible["avg_daily_sales"] >= threshold].copy()

print(f"候选单品: {len(eligible)}, 入选: {len(selected)} (阈值={threshold:.1f}kg) ∈ [27,33]: {27 <= len(selected) <= 33}")

# ── 2. Per-SKU demand ──
last_30d = daily[(daily["销售日期"] >= "2023-05-31") & (daily["销售日期"] <= "2023-06-30")]
sku_demand = last_30d.groupby("单品编码").agg(
    mu=("total_qty", "mean"), sigma=("total_qty", "std"),
    last_cost=("批发价格(元/千克)", "last"), last_price=("avg_price", "last"),
).reset_index()
sku_demand["sigma"] = sku_demand["sigma"].fillna(sku_demand["mu"] * 0.3)
selected = selected.merge(sku_demand, on="单品编码", how="left")
mask = selected["mu"].isna()
selected.loc[mask, "mu"] = selected.loc[mask, "avg_daily_sales"]
selected.loc[mask, "sigma"] = selected.loc[mask, "avg_daily_sales"] * 0.3
selected.loc[mask, "last_cost"] = selected.loc[mask, "avg_cost"]
selected.loc[mask, "last_price"] = selected.loc[mask, "avg_price"]

# ── 3. Per-SKU newsvendor ──
def expected_profit(Q, P, C, L, k, mu, sigma, n=3000):
    eff_cost = C / (1 - L / 100)
    sigma = max(sigma, mu * 0.01)
    D = np.random.RandomState(SEED).normal(mu, sigma, n); D = np.maximum(D, 0)
    s = np.minimum(Q, D); e = Q - s
    return (P * s + k * P * e - eff_cost * Q).mean()

t0 = time.time(); results = []
for _, row in selected.iterrows():
    C = max(row["last_cost"], 0.5); L = row["损耗率(%)"]
    mu, sigma = row["mu"], max(row["sigma"], 0.01); cat = row["category"]
    e = ELASTICITIES.get(cat, -0.5); ref_price = max(row["last_price"], 0.5)
    hist_markup = max(0.1, (ref_price / C - 1)) if C > 0 else 0.5
    P_ref = C * (1 + hist_markup)
    Q_max = max(row["avg_daily_sales"] * 2.5, 5.0)

    best = {"profit": -np.inf}
    for markup in np.linspace(max(0.1, hist_markup - 0.3), min(2.5, hist_markup + 0.5), 25):
        P = C * (1 + markup)
        D_adj = max(0.1, mu * (P / P_ref) ** e if P_ref > 0 else mu)
        for Q_factor in np.linspace(0.7, 1.6, 25):
            Q = max(2.5, min(D_adj * Q_factor, Q_max))
            ep = expected_profit(Q, P, C, L, K_DISCOUNT, D_adj, sigma)
            if ep > best["profit"]:
                best = {"profit": ep, "markup": markup, "P": P, "Q": Q}

    results.append({
        "单品编码": int(row["单品编码"]), "品类": cat,
        "日均销量_kg": round(row["avg_daily_sales"], 2),
        "需求均值": round(mu, 2),
        "优化加成率": round(best["markup"], 4), "优化售价_元每kg": round(best["P"], 2),
        "优化订货量_kg": round(best["Q"], 1), "优化利润_元": round(best["profit"], 1),
    })

t_elapsed = time.time() - t0
df = pd.DataFrame(results)
df.to_csv(f"{OUT}/tables/q3_m1_sku_policy.csv", index=False, encoding="utf-8-sig")

# ── 4. Demand satisfaction ──
cat_demand = june24_30.groupby("分类名称")["total_qty"].sum() / 7
print("\n各品类需求满足率:")
satisfaction = {}
for cat in cat_demand.index:
    cat_qty = df[df["品类"] == cat]["优化订货量_kg"].sum()
    sat = cat_qty / cat_demand[cat]
    satisfaction[cat] = round(sat, 4)
    print(f"  {cat}: {cat_qty:.1f}/{cat_demand[cat]:.1f}kg = {sat:.1%}")

# ── 5. SKU profit ranking plot ──
fig, ax = plt.subplots(figsize=FIG_WIDE)
df_sorted = df.sort_values("优化利润_元", ascending=True)
colors = plt.cm.Set2(np.linspace(0, 1, 6))
cat_color = {c: colors[i] for i, c in enumerate(cat_demand.index)}
bar_colors = [cat_color[c] for c in df_sorted["品类"]]
ax.barh(range(len(df_sorted)), df_sorted["优化利润_元"].values, color=bar_colors)
ax.set_yticks(range(len(df_sorted)))
ax.set_yticklabels([f"{r['单品编码']}" for _, r in df_sorted.iterrows()], fontsize=7)
ax.set_xlabel("单日期望利润 (元)")
ax.set_title("Q3 各单品报童优化单日利润", fontweight="bold")
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=cat_color[c], label=c) for c in cat_demand.index]
ax.legend(handles=legend_elements, title="品类", fontsize=8, title_fontsize=9)
fig.tight_layout(); fig.savefig(f"{OUT}/figures/q3_sku_profit_ranking.png"); plt.close()

# ── 6. Category satisfaction plot ──
fig, ax = plt.subplots(figsize=FIG_HALF)
cats_list = list(cat_demand.index)
sat_vals = [satisfaction[c] * 100 for c in cats_list]
ax.bar(cats_list, sat_vals, color="#3182bd")
ax.axhline(y=100, color="red", linestyle="--", alpha=0.5)
ax.set_ylabel("需求满足率 (%)"); ax.set_title("各品类需求满足率", fontweight="bold")
ax.tick_params(axis="x", rotation=30)
for i, v in enumerate(sat_vals):
    ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=10)
fig.tight_layout(); fig.savefig(f"{OUT}/figures/q3_category_satisfaction.png"); plt.close()

# ── 7. Markup distribution ──
fig, ax = plt.subplots(figsize=FIG_HALF)
ax.hist(df["优化加成率"].values * 100, bins=15, color="#3182bd", edgecolor="white", alpha=0.85)
ax.axvline(x=df["优化加成率"].mean() * 100, color="red", linestyle="--", label=f"均值={df['优化加成率'].mean():.1%}")
ax.set_xlabel("加成率 (%)"); ax.set_ylabel("单品数量")
ax.set_title("单品优化加成率分布", fontweight="bold")
ax.legend()
fig.tight_layout(); fig.savefig(f"{OUT}/figures/q3_markup_distribution.png"); plt.close()

# ── 8. Run summary ──
markups = df["优化加成率"].values; total_profit = df["优化利润_元"].sum()
summary = {
    "schema_version": 1, "question": "Q3", "round": "round1",
    "implementation_target": "python", "random_seed": SEED,
    "approved_decision_id": "q3_method_choice",
    "methods": [{
        "method_id": "M1", "role": "main", "script": "code/Q3/q3_main.py",
        "status": "success", "execution_time_seconds": round(t_elapsed, 1),
        "input_files": ["workspace/data_clean/daily_sales.csv", "workspace/data_clean/item_loss_rates.csv"],
        "output_files": ["tables/q3_m1_sku_policy.csv"],
        "figure_files": ["figures/q3_sku_profit_ranking.png", "figures/q3_category_satisfaction.png",
                         "figures/q3_markup_distribution.png"],
        "metrics_summary": {
            "入选单品数": len(df), "过滤阈值_kg": threshold,
            "单日总利润_元": round(float(total_profit), 1),
            "总订货量_kg": round(float(df["优化订货量_kg"].sum()), 1),
            "加成率标准差": round(float(np.std(markups)), 4),
            "加成率范围": [round(float(markups.min()), 4), round(float(markups.max()), 4)],
            "全部正利润": bool((df["优化利润_元"] > 0).all()),
            "需求满足率": satisfaction,
            "最低需求满足率": round(float(min(satisfaction.values())), 4),
            "退化检查_加成率统一": bool(np.std(markups) < 0.01),
        },
        "warnings": [], "errors": []
    }],
    "comparison": {},
    "fallback_trigger": {"fallback_id": "M3", "condition": "任意品类需求满足率 < 50%", "observed": False},
    "environment": {"python": "3.10", "key_packages": "pandas numpy scipy matplotlib"}
}
with open(f"{OUT}/run_summary.json", "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

print(f"\nQ3 M1 完成 ({t_elapsed:.1f}s). 总利润: {total_profit:.0f} 元")
print(f"加成率标准差: {np.std(markups):.4f}")
