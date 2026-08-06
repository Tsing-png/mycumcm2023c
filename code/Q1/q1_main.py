"""Q1 M1: Spearman correlation + K-means++ clustering + distribution fitting."""
import sys; sys.path.insert(0, "code/scripts")
from plot_config import setup_style, FIG_WIDE, FIG_SQUARE, FIG_HALF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd, numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json, time, os, warnings
warnings.filterwarnings('ignore')

setup_style()
SEED = 42
OUT = "results/Q1/experiments/round1"
for d in [f"{OUT}/figures", f"{OUT}/tables", f"{OUT}/metrics"]:
    os.makedirs(d, exist_ok=True)

daily = pd.read_csv("workspace/data_clean/daily_sales.csv", parse_dates=["销售日期"])
CAT_NAMES_CN = list(daily["分类名称"].unique())

# ── 1. Category daily aggregation ──
cat_daily = daily.groupby(["销售日期", "分类名称"])["total_qty"].sum().reset_index()
cat_pivot = cat_daily.pivot(index="销售日期", columns="分类名称", values="total_qty").dropna()

# ── 2. Spearman correlation ──
t0 = time.time()
spearman_corr = cat_pivot.corr(method="spearman")
corr_vals = spearman_corr.values[np.triu_indices_from(spearman_corr.values, k=1)]

fig, ax = plt.subplots(figsize=FIG_SQUARE)
sns.heatmap(spearman_corr, annot=True, fmt=".3f", cmap="RdBu_r", center=0,
            vmin=-1, vmax=1, ax=ax, annot_kws={"fontsize": 11})
fig.tight_layout(); fig.savefig(f"{OUT}/figures/q1_corr_heatmap_spearman.png"); plt.close()
spearman_corr.to_csv(f"{OUT}/tables/q1_spearman_corr.csv")

# ── 3. Normality test ──
norm_results = {}
for cat in cat_pivot.columns:
    _, p = stats.normaltest(cat_pivot[cat])
    norm_results[cat] = {"p_value": float(p), "is_normal": p >= 0.05}
    print(f"  {cat}: p={p:.2e} {'✓ 正态' if p>=0.05 else '✗ 非正态'}")

# ── 4. Product features + K-means++ ──
prod_stats = daily.groupby("单品编码").agg(
    mean_qty=("total_qty", "mean"), std_qty=("total_qty", "std"),
    sales_days=("total_qty", "count"), avg_price=("avg_price", "mean"),
    category=("分类名称", "first"),
).reset_index()
prod_stats["cv"] = prod_stats["std_qty"] / prod_stats["mean_qty"].replace(0, np.nan)
prod_dense = prod_stats[prod_stats["sales_days"] >= 30].copy()
print(f"聚类用单品: {len(prod_dense)} / {len(prod_stats)} (销售天数≥30)")

features = ["mean_qty", "std_qty", "cv", "avg_price"]
X = prod_dense[features].fillna(0).values
X_log = np.log1p(np.abs(X)) * np.sign(X)

sil_scores = []
for k in range(2, 8):
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=SEED)
    labels = km.fit_predict(X_log)
    sil = silhouette_score(X_log, labels)
    sil_scores.append(sil)

best_k = np.argmax(sil_scores) + 2
km_final = KMeans(n_clusters=best_k, init="k-means++", n_init=10, random_state=SEED)
labels_final = km_final.fit_predict(X_log)
prod_dense["cluster"] = labels_final
t_elapsed = time.time() - t0

# Silhouette plot
fig, ax = plt.subplots(figsize=FIG_HALF)
ax.plot(range(2, 8), sil_scores, "bo-", markersize=8, linewidth=2)
ax.set_xlabel("聚类数 K"); ax.set_ylabel("轮廓系数 (Silhouette Score)")
ax.axvline(x=best_k, color="red", linestyle="--", alpha=0.5, label=f"K={best_k}")
ax.legend(); fig.tight_layout()
fig.savefig(f"{OUT}/figures/q1_cluster_silhouette.png"); plt.close()

prod_dense[["单品编码", "category", "cluster"]].to_csv(f"{OUT}/tables/q1_cluster_assignments.csv", index=False)

for c in sorted(prod_dense["cluster"].unique()):
    comp = prod_dense[prod_dense["cluster"] == c]["category"].value_counts()
    print(f"  簇 {c}: {dict(comp)}")

# ── 5. Distribution fitting ──
dist_names = ["norm", "lognorm", "gamma"]
dist_results = {}
for cat in cat_pivot.columns:
    data = cat_pivot[cat].dropna()
    best_dist, best_ks = None, -1.0
    for dname in dist_names:
        try:
            dist = getattr(stats, dname)
            params = dist.fit(data)
            _, ks_p = stats.kstest(data, dname, args=params)
            if ks_p > best_ks:
                best_ks, best_dist = ks_p, dname
        except Exception:
            pass
    dist_results[cat] = {"best_fit": best_dist, "ks_p": round(float(best_ks), 4)}
pd.DataFrame(dist_results).T.to_csv(f"{OUT}/tables/q1_distribution_params.csv")

# ── 6. Monthly sales trend ──
cat_daily["month"] = cat_daily["销售日期"].dt.to_period("M")
monthly = cat_daily.groupby(["month", "分类名称"])["total_qty"].sum().reset_index()
monthly["month_str"] = monthly["month"].astype(str)

fig, ax = plt.subplots(figsize=FIG_WIDE)
for cat in cat_pivot.columns:
    mc = monthly[monthly["分类名称"] == cat]
    ax.plot(range(len(mc)), mc["total_qty"].values, label=cat, alpha=0.85, linewidth=1.5)
tick_positions = range(0, len(mc), 6)
tick_labels = [monthly["month_str"].iloc[i] for i in tick_positions]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha="right")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="品类")
ax.set_ylabel("月销售总量 (kg)"); ax.set_xlabel("月份")
fig.tight_layout(); fig.savefig(f"{OUT}/figures/q1_monthly_sales_trend.png"); plt.close()

# ── 7. Run summary ──
summary = {
    "schema_version": 1, "question": "Q1", "round": "round1",
    "implementation_target": "python", "random_seed": SEED,
    "approved_decision_id": "q1_method_choice",
    "methods": [{
        "method_id": "M1", "role": "main", "script": "code/Q1/q1_main.py",
        "status": "success", "execution_time_seconds": round(t_elapsed, 3),
        "input_files": ["workspace/data_clean/daily_sales.csv"],
        "output_files": ["tables/q1_spearman_corr.csv", "tables/q1_cluster_assignments.csv",
                         "tables/q1_distribution_params.csv"],
        "figure_files": ["figures/q1_corr_heatmap_spearman.png", "figures/q1_cluster_silhouette.png",
                         "figures/q1_monthly_sales_trend.png"],
        "metrics_summary": {
            "spearman_rho_range": [round(float(corr_vals.min()), 4), round(float(corr_vals.max()), 4)],
            "spearman_mean_abs_rho": round(float(np.abs(corr_vals).mean()), 4),
            "best_k": int(best_k), "silhouette_score": round(float(sil_scores[best_k-2]), 4),
            "normality_all_non_normal": all(not v["is_normal"] for v in norm_results.values()),
            "products_clustered": len(prod_dense),
            "deg_all_corr_zero": bool(np.abs(corr_vals).max() < 0.05),
            "deg_single_cluster": bool(best_k == 1 or sil_scores[best_k-2] < 0.1),
        },
        "warnings": [], "errors": []
    }],
    "comparison": {},
    "fallback_trigger": {"fallback_id": None, "condition": None, "observed": False},
    "environment": {"python": "3.10", "key_packages": "pandas scipy scikit-learn matplotlib seaborn"}
}
with open(f"{OUT}/run_summary.json", "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"\nQ1 M1 完成 ({t_elapsed:.1f}s). 输出: {OUT}/")
