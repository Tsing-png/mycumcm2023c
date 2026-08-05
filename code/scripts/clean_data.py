"""Clean raw data for CUMCM 2023 Problem C.

Reads from workspace/data_raw/, writes to workspace/data_clean/.
Raw files are never modified. Only the visible sheet of 附件4 is used.
"""
import pandas as pd
from pathlib import Path

RAW = Path("workspace/data_raw")
CLEAN = Path("workspace/data_clean")
CLEAN.mkdir(parents=True, exist_ok=True)

# ── 附件1: Product info (pass-through) ──
df1 = pd.read_excel(RAW / "附件1.xlsx")
df1.to_csv(CLEAN / "products.csv", index=False)
print(f"[1/5] products.csv — {len(df1)} rows")

# ── 附件2: Sales — remove returns ──
df2 = pd.read_excel(RAW / "附件2.xlsx")
n_total = len(df2)
returns_mask = df2["销售类型"] == "退货"
df2_clean = df2[~returns_mask].copy()
df2_clean["extreme_qty"] = df2_clean["销量(千克)"] > df2_clean["销量(千克)"].quantile(0.999)
df2_clean.to_csv(CLEAN / "sales_clean.csv", index=False)
print(f"[2/5] sales_clean.csv — {len(df2_clean)} rows ({n_total - len(df2_clean)} returns removed)")

# ── Daily aggregated view (core modeling table) ──
daily = df2_clean.groupby(["销售日期", "单品编码"]).agg(
    total_qty=("销量(千克)", "sum"),
    avg_price=("销售单价(元/千克)", "mean"),
    discounted_ratio=("是否打折销售", lambda x: (x == "是").mean()),
    transaction_count=("销量(千克)", "count"),
).reset_index()

daily = daily.merge(df1[["单品编码", "分类编码", "分类名称"]], on="单品编码", how="left")

df3 = pd.read_excel(RAW / "附件3.xlsx")
daily = daily.merge(df3, left_on=["销售日期", "单品编码"], right_on=["日期", "单品编码"], how="left")
daily = daily.drop(columns=["日期"])

df4 = pd.read_excel(RAW / "附件4.xlsx", sheet_name="Sheet1")  # visible sheet only
daily = daily.merge(df4[["单品编码", "损耗率(%)"]], on="单品编码", how="left")

daily.to_csv(CLEAN / "daily_sales.csv", index=False)
print(f"[3/5] daily_sales.csv — {len(daily)} rows, {daily['单品编码'].nunique()} products")

# ── 附件3: Wholesale prices with flags ──
df3_clean = df3.copy()
df3_clean["near_zero_price"] = df3_clean["批发价格(元/千克)"] <= 0.01
df3_clean["extreme_price"] = df3_clean["批发价格(元/千克)"] >= 100
df3_clean.to_csv(CLEAN / "wholesale_prices.csv", index=False)
print(f"[4/5] wholesale_prices.csv — {len(df3_clean)} rows")

# ── 附件4: Visible item loss rates + computed category averages ──
df4_item = pd.read_excel(RAW / "附件4.xlsx", sheet_name="Sheet1")
df4_item.to_csv(CLEAN / "item_loss_rates.csv", index=False)

cat_avg = (
    df1.merge(df4_item, on=["单品编码", "单品名称"])
    .groupby("分类名称")["损耗率(%)"]
    .mean()
    .round(4)
)
cat_avg.to_csv(CLEAN / "category_loss_rates_computed.csv", header=["avg_loss_rate_pct"])
print(f"[5/5] item_loss_rates.csv + category_loss_rates_computed.csv (computed, NOT hidden sheet)")
print("\nDone.")
