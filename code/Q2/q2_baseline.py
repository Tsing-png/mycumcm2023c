"""Q2 M2: ARIMA + Fixed Markup baseline."""
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import json, time, os, warnings
warnings.filterwarnings('ignore')

SEED = 42
OUT = "results/Q2/experiments/round1"
os.makedirs(f"{OUT}/tables", exist_ok=True)

daily = pd.read_csv("workspace/data_clean/daily_sales.csv", parse_dates=["销售日期"])
CATS = ["水生根茎类", "花叶类", "花菜类", "茄类", "辣椒类", "食用菌"]
CAT_LOSS = {"水生根茎类": 0.1197, "花叶类": 0.1028, "花菜类": 0.1414,
            "茄类": 0.0712, "辣椒类": 0.0852, "食用菌": 0.0813}
K_DISCOUNT = 0.66

cat_data = {}
for cat in CATS:
    cd = daily[daily["分类名称"] == cat].groupby("销售日期").agg(
        sales=("total_qty", "sum"), cost=("批发价格(元/千克)", "mean"), price=("avg_price", "mean")
    ).reset_index()
    cd = cd[cd["cost"] > 0.01]
    cat_data[cat] = cd

def expected_profit(Q, P, C, L, k, mu_d, sigma_d, n=5000):
    eff_cost = C / (1 - L)
    sigma_d = max(sigma_d, mu_d * 0.01)
    D = np.random.RandomState(SEED).normal(mu_d, sigma_d, n)
    D = np.maximum(D, 0)
    sales_reg = np.minimum(Q, D)
    excess = Q - sales_reg
    return (P * sales_reg + k * P * excess - eff_cost * Q).mean()

t0 = time.time()
results = []

for cat in CATS:
    cd = cat_data[cat]
    train = cd.iloc[:-30]
    test = cd.iloc[-30:]
    L = CAT_LOSS[cat]

    # ARIMA grid search
    ts = train["sales"].values
    best_aic, best_order = np.inf, None
    for p, d, q in [(p,d,q) for p in [1,2] for d in [0,1] for q in [1,2]]:
        try:
            model = ARIMA(ts, order=(p, d, q))
            fitted = model.fit()
            if fitted.aic < best_aic:
                best_aic, best_order = fitted.aic, (p, d, q)
        except Exception:
            pass

    # Forecast
    model = ARIMA(ts, order=best_order)
    fitted = model.fit()
    fc = fitted.forecast(steps=31)  # to July 1
    fc_30 = fitted.forecast(steps=30)
    rmse = np.sqrt(((fc_30 - test["sales"].values) ** 2).mean())
    forecast_july1 = max(1, fc[-1])

    C = cd["cost"].iloc[-1]
    hist_markup = max(0.1, (cd["price"] / cd["cost"] - 1).mean())
    P = C * (1 + hist_markup)
    Q = min(forecast_july1 / (1 - L), cd["sales"].max() * 1.5)
    demand_std = cd["sales"].std()
    profit = expected_profit(Q, P, C, L, K_DISCOUNT, forecast_july1, demand_std)

    results.append({
        "category": cat, "order": f"ARIMA{best_order}", "rmse": round(rmse, 2),
        "forecast_july1": round(forecast_july1, 1), "markup": round(hist_markup, 4),
        "P": round(P, 2), "Q": round(Q, 1), "profit": round(profit, 1)
    })
    print(f"  {cat}: ARIMA{best_order}, rmse={rmse:.1f}, fc={forecast_july1:.0f}, profit={profit:.0f}")

t_elapsed = time.time() - t0

df = pd.DataFrame(results)
df.to_csv(f"{OUT}/tables/q2_m2_baseline_policy.csv", index=False)

total_m2 = df["profit"].sum()
print(f"Q2 M2 done in {t_elapsed:.0f}s. Total profit: {total_m2:.0f} yuan/day")
