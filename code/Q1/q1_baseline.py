"""Q1 M2 (diagnostic): Pearson correlation + hierarchical clustering."""
import sys; sys.path.insert(0, "code/scripts")
from plot_config import setup_style, FIG_SQUARE, FIG_HALF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd, numpy as np
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage
import json, time, os, warnings
warnings.filterwarnings('ignore')

setup_style()
SEED = 42
OUT = "results/Q1/experiments/round1"
os.makedirs(f"{OUT}/figures", exist_ok=True)
os.makedirs(f"{OUT}/tables", exist_ok=True)

daily = pd.read_csv("workspace/data_clean/daily_sales.csv", parse_dates=["销售日期"])
cat_daily = daily.groupby(["销售日期", "分类名称"])["total_qty"].sum().reset_index()
cat_pivot = cat_daily.pivot(index="销售日期", columns="分类名称", values="total_qty").dropna()

t0 = time.time()

# ── Pearson correlation ──
pearson_corr = cat_pivot.corr(method="pearson")

fig, ax = plt.subplots(figsize=FIG_SQUARE)
sns.heatmap(pearson_corr, annot=True, fmt=".3f", cmap="RdBu_r", center=0,
            vmin=-1, vmax=1, ax=ax, annot_kws={"fontsize": 11})
ax.set_title("各品类日销售量 Pearson 相关系数矩阵", fontsize=15, fontweight="bold")
fig.tight_layout(); fig.savefig(f"{OUT}/figures/q1_corr_heatmap_pearson.png"); plt.close()
pearson_corr.to_csv(f"{OUT}/tables/q1_pearson_corr.csv")

# ── Hierarchical clustering ──
Z = linkage(cat_pivot.T, method="ward")
fig, ax = plt.subplots(figsize=FIG_HALF)
dendrogram(Z, labels=list(cat_pivot.columns), ax=ax, leaf_font_size=12)
ax.set_title("品类销售量层次聚类 (Ward 方法)", fontweight="bold")
ax.set_ylabel("距离")
fig.tight_layout(); fig.savefig(f"{OUT}/figures/q1_dendrogram.png"); plt.close()

# ── Normality + comparison ──
all_normal = all(stats.normaltest(cat_pivot[c]).pvalue >= 0.05 for c in cat_pivot.columns)
spearman_corr = pd.read_csv(f"{OUT}/tables/q1_spearman_corr.csv", index_col=0)
diff = (spearman_corr - pearson_corr).abs()
p_pearson = pearson_corr.values[np.triu_indices_from(pearson_corr.values, k=1)]
dir_agree = (np.sign(spearman_corr.values[np.triu_indices_from(spearman_corr.values, k=1)]) ==
             np.sign(p_pearson)).mean()

comparison = {
    "pearson_range": [round(float(p_pearson.min()), 4), round(float(p_pearson.max()), 4)],
    "spearman_vs_pearson_max_diff": round(float(diff.max().max()), 4),
    "directional_agreement": round(float(dir_agree), 4),
    "normality_all_pass": bool(all_normal),
    "pearson_valid": bool(all_normal),
}
with open(f"{OUT}/metrics/q1_comparison.json", "w") as f:
    json.dump(comparison, f, indent=2)

t_elapsed = time.time() - t0
print(f"Q1 M2 完成 ({t_elapsed:.1f}s)")
print(f"  Pearson r ∈ [{p_pearson.min():.3f}, {p_pearson.max():.3f}]")
print(f"  全部正态: {all_normal} → Pearson {'有效' if all_normal else '无效 (应使用 Spearman)'}")
print(f"  Spearman vs Pearson 方向一致性: {dir_agree:.1%}")
