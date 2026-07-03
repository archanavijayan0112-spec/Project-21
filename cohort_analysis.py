"""
RetailPulse — RFM Customer Segmentation
Scores every customer on Recency, Frequency, Monetary value (1-5 scale)
and assigns a human-readable segment (Champions, At Risk, Lost, etc.)
"""

import pandas as pd
import numpy as np
import os

OUT = "exports/powerbi"


def compute_rfm():
    fact = pd.read_csv("exports/powerbi/fact_sales.csv")
    dim_date = pd.read_csv("exports/powerbi/dim_date.csv", parse_dates=["date"])
    fact = fact.merge(dim_date[["date_id", "date"]], on="date_id")

    snapshot_date = fact["date"].max() + pd.Timedelta(days=1)

    rfm = fact.groupby("customer_id").agg(
        recency=("date", lambda x: (snapshot_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("net_revenue", "sum"),
    ).reset_index()

    # Score 1 (worst) - 5 (best) using quintiles
    rfm["R_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["rfm_score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)
    rfm["rfm_total"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

    def segment(row):
        r, f, m = row["R_score"], row["F_score"], row["M_score"]
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        if r >= 3 and f >= 3:
            return "Loyal Customers"
        if r >= 4 and f <= 2:
            return "New Customers"
        if r <= 2 and f >= 4:
            return "At Risk"
        if r <= 2 and f <= 2 and m <= 2:
            return "Lost"
        if r == 3 and f == 3:
            return "Needs Attention"
        return "Potential Loyalist"

    rfm["segment"] = rfm.apply(segment, axis=1)
    rfm["monetary"] = rfm["monetary"].round(2)

    rfm.to_csv(f"{OUT}/customer_rfm_segments.csv", index=False)

    summary = rfm.groupby("segment").agg(
        customers=("customer_id", "count"),
        avg_recency_days=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        total_revenue=("monetary", "sum"),
    ).sort_values("total_revenue", ascending=False).round(1)
    summary.to_csv(f"{OUT}/segment_summary.csv")

    print("=== RFM Segment Summary ===")
    print(summary.to_string())
    print(f"\nFull scores exported -> {OUT}/customer_rfm_segments.csv")
    return rfm, summary


if __name__ == "__main__":
    compute_rfm()
