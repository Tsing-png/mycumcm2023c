"""Q3 M2: Same 31 SKUs + Fixed Markup baseline."""
import sys; sys.path.insert(0, "code/scripts")
from plot_config import setup_style
import pandas as pd, numpy as np
import json, time, os, warnings
warnings.filterwarnings('ignore')

setup_style()
SEED = 42
OUT = "results/Q3/experiments/round1"
os.makedirs(f"{OUT}/tables", exist_ok=True)

daily = pd.read_csv("workspace/data_clean/daily_sales.csv", parse_dates=["销售日期"])
loss_rates = pd.read_csv("workspace/data_clean/item_loss_rates.csv")
K_DISCOUNT = 0.66

# ── Same eligible + filter logic as M1 ──
june24_30 = daily[(daily["销售日期"] >= "2023-06-24") & (daily["销售日期"] <= "2023-06-30")]
eligible = june24_30.groupby("单品编码").agg(
    avg_daily_sales=("total_qty", "mean"), avg_price=("avg_price", "mean"),
    avg_cost=("批发价格(元/千克)", "mean"), category=("分类名称", "first"),
).reset_index()
eligible = eligible.merge(loss_rates[["单品编码", "损耗率(%)"]], on="单品编码", how="left")

threshold = 2.5
selected = eligible[eligible["avg_daily_sales"] >= threshold].copy()

# ── Per-SKU demand ──
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

def expected_profit(Q, P, C, L, k, mu, sigma, n=3000):
    eff_cost = C / (1 - L / 100)
    sigma = max(sigma, mu * 0.01)
    D = np.random.RandomState(SEED).normal(mu, sigma, n); D = np.maximum(D, 0)
    s = np.minimum(Q, D); e = Q - s
    return (P * s + k * P * e - eff_cost * Q).mean()

t0 = time.time()
results = []

for _, row in selected.iterrows():
    C = max(row["last_cost"], 0.5); L = row["损耗率(%)"]
    mu = row["mu"]
    # Fixed markup = historical average for this SKU
    hist_markup = max(0.1, (row["last_price"] / C - 1)) if C > 0 else 0.5
    P = C * (1 + hist_markup)
    Q = max(2.5, mu / (1 - L / 100))
    profit = expected_profit(Q, P, C, L, K_DISCOUNT, mu, max(row["sigma"], 0.01))

    results.append({
        "单品编码": int(row["单品编码"]), "品类": row["category"],
        "日均销量_kg": round(row["avg_daily_sales"], 2),
        "历史加成率": round(hist_markup, 4), "售价_元每kg": round(P, 2),
        "订货量_kg": round(Q, 1), "利润_元": round(profit, 1),
    })

t_elapsed = time.time() - t0
df = pd.DataFrame(results)
df.to_csv(f"{OUT}/tables/q3_m2_baseline_policy.csv", index=False, encoding="utf-8-sig")

total_m2 = df["利润_元"].sum()

# ── Update run_summary with comparison ──
with open(f"{OUT}/run_summary.json") as f:
    summary = json.load(f)

m1_total = summary["methods"][0]["metrics_summary"]["单日总利润_元"]
summary["comparison"] = {
    "M1_单日总利润": m1_total,
    "M2_单日总利润": round(float(total_m2), 1),
    "M1_gain_vs_M2": f"{(m1_total/total_m2 - 1)*100:.1f}%"
}

# Add M2 to methods
summary["methods"].append({
    "method_id": "M2", "role": "usable_baseline",
    "script": "code/Q3/q3_baseline.py", "status": "success",
    "execution_time_seconds": round(t_elapsed, 1),
    "metrics_summary": {
        "单日总利润_元": round(float(total_m2), 1),
        "总订货量_kg": round(float(df["订货量_kg"].sum()), 1),
    }
})

with open(f"{OUT}/run_summary.json", "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

print(f"Q3 M2 完成 ({t_elapsed:.1f}s). M2 利润: {total_m2:.0f} 元")
print(f"M1 vs M2: {m1_total:.0f} vs {total_m2:.0f} ({(m1_total/total_m2 - 1)*100:.1f}%)")
