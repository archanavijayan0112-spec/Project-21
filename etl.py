"""
RetailPulse — Executive KPI Report
Computes headline business metrics and writes a JSON + printed summary,
used by the dashboard and README.
"""

import pandas as pd
import json

OUT = "exports/powerbi"


def main():
    fact = pd.read_csv("exports/powerbi/fact_sales.csv")
    dim_date = pd.read_csv("exports/powerbi/dim_date.csv", parse_dates=["date"])
    dim_customer = pd.read_csv("exports/powerbi/dim_customer.csv")
    dim_product = pd.read_csv("exports/powerbi/dim_product.csv")
    dim_store = pd.read_csv("exports/powerbi/dim_store.csv")

    fact = fact.merge(dim_date[["date_id", "date", "year"]], on="date_id")
    fact = fact.merge(dim_product[["product_id", "category"]], on="product_id")
    fact = fact.merge(dim_store[["store_id", "city", "region"]], on="store_id")

    kpis = {
        "total_revenue": round(fact["net_revenue"].sum(), 2),
        "total_profit": round(fact["profit"].sum(), 2),
        "avg_margin_pct": round(fact["profit"].sum() / fact["net_revenue"].sum() * 100, 2),
        "total_orders": int(fact["order_id"].nunique()),
        "total_customers": int(fact["customer_id"].nunique()),
        "avg_order_value": round(fact.groupby("order_id")["net_revenue"].sum().mean(), 2),
        "yoy_growth_pct": None,
        "top_category": fact.groupby("category")["net_revenue"].sum().idxmax(),
        "top_region": fact.groupby("region")["net_revenue"].sum().idxmax(),
        "top_city": fact.groupby("city")["net_revenue"].sum().idxmax(),
    }

    yearly = fact.groupby("year")["net_revenue"].sum()
    if len(yearly) >= 2:
        y = yearly.sort_index()
        kpis["yoy_growth_pct"] = round((y.iloc[-1] / y.iloc[-2] - 1) * 100, 2)

    with open(f"{OUT}/kpi_summary.json", "w") as f:
        json.dump(kpis, f, indent=2)

    print("=== RetailPulse KPI Summary ===")
    for k, v in kpis.items():
        print(f"{k:20s}: {v}")


if __name__ == "__main__":
    main()
