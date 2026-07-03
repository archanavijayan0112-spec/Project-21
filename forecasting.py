"""
RetailPulse — Monthly Cohort Retention Analysis
Groups customers by signup month and tracks what % of each cohort
remains active in each subsequent month.
"""

import pandas as pd
import numpy as np

OUT = "exports/powerbi"


def compute_cohorts():
    fact = pd.read_csv("exports/powerbi/fact_sales.csv")
    dim_date = pd.read_csv("exports/powerbi/dim_date.csv", parse_dates=["date"])
    dim_customer = pd.read_csv("exports/powerbi/dim_customer.csv", parse_dates=["signup_date"])

    fact = fact.merge(dim_date[["date_id", "date"]], on="date_id")

    # Anchor cohorts on each customer's FIRST PURCHASE (not signup), since
    # signup can predate the transaction window and would misalign cohorts.
    first_purchase = fact.groupby("customer_id")["date"].min().rename("cohort_date")
    fact = fact.merge(first_purchase, on="customer_id")

    fact["order_month"] = fact["date"].dt.to_period("M")
    fact["cohort_month"] = fact["cohort_date"].dt.to_period("M")
    fact["cohort_index"] = (
        (fact["order_month"].dt.year - fact["cohort_month"].dt.year) * 12
        + (fact["order_month"].dt.month - fact["cohort_month"].dt.month)
    )

    cohort_data = fact.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
    cohort_pivot = cohort_data.pivot(index="cohort_month", columns="cohort_index", values="customer_id")

    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_sizes, axis=0).round(3)

    retention.to_csv(f"{OUT}/cohort_retention_matrix.csv")

    # Long format, easier for Power BI / Tableau to plot
    long_format = retention.reset_index().melt(id_vars="cohort_month", var_name="months_since_signup",
                                                 value_name="retention_rate").dropna()
    long_format["cohort_month"] = long_format["cohort_month"].astype(str)
    long_format.to_csv(f"{OUT}/cohort_retention_long.csv", index=False)

    print("=== Retention rate by cohort (first 6 months since signup) ===")
    print((retention.iloc[:, :6] * 100).round(1).to_string())
    print(f"\nExported -> {OUT}/cohort_retention_matrix.csv and cohort_retention_long.csv")
    return retention


if __name__ == "__main__":
    compute_cohorts()
