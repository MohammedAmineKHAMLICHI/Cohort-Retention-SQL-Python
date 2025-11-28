# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Outils de calcul de rétention par cohorte et CLI associée.

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {"order_id", "user_id", "order_date"}


@dataclass
class RetentionSummary:
    """Regroupe la table produite et les phrases d’insight générées."""

    table: pd.DataFrame
    insights: list[str]


def _validate_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Valide le jeu de commandes : colonnes requises et dates converties."""
    if orders.empty:
        raise ValueError("Cannot compute retention: the orders dataframe is empty.")

    missing = REQUIRED_COLUMNS - set(orders.columns)
    if missing:
        raise ValueError(f"Missing columns for retention: {', '.join(sorted(missing))}.")

    df = orders.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if df["order_date"].isna().any():
        raise ValueError("Invalid dates detected in order_date; retention cannot be computed.")

    return df


def _to_month_index(period_series: pd.Series) -> pd.Series:
    """Convertit une série Period[M] en index de mois absolu (année*12 + mois)."""
    return period_series.dt.year * 12 + period_series.dt.month


def build_retention(orders: pd.DataFrame) -> pd.DataFrame:
    """Construit la table de rétention par cohorte (cohort_size + M+0..n en pourcentage)."""
    df = _validate_orders(orders)
    df["cohort_month"] = df.groupby("user_id")["order_date"].transform("min").dt.to_period("M")
    df["order_month"] = df["order_date"].dt.to_period("M")
    df["month_index"] = _to_month_index(df["order_month"]) - _to_month_index(df["cohort_month"])

    cohort_counts = (
        df.groupby(["cohort_month", "month_index"], observed=True)["user_id"]
        .nunique()
        .unstack(fill_value=0)
        .sort_index(axis=1)
    )

    if 0 not in cohort_counts.columns:
        raise ValueError("Cannot compute cohort sizes because month index 0 is missing.")

    cohort_size = cohort_counts[0].replace(0, pd.NA)
    retention = (cohort_counts.div(cohort_size, axis=0) * 100).round(1)
    retention.insert(0, "cohort_size", cohort_size.astype("Int64"))
    retention.index = retention.index.astype(str)
    return retention


def build_insights(retention: pd.DataFrame, limit: int = 3) -> List[str]:
    """Génère quelques phrases d’insight à partir de la table de rétention."""
    messages: List[str] = []
    if retention.empty:
        return ["Not enough data to compute cohort retention."]

    numeric_months = [col for col in retention.columns if isinstance(col, (int, np.integer))]
    numeric_months.sort()

    if not numeric_months:
        return ["Orders do not cover any follow-up months (M+1, M+3, etc.)."]

    cohort_sizes = retention["cohort_size"].dropna()
    if not cohort_sizes.empty:
        median_size = int(cohort_sizes.median())
        messages.append(f"Median cohort size: {median_size} customers.")

    def fmt_pct(value: float) -> str:
        return f"{value:.1f}%"

    if 1 in retention.columns:
        month_one = retention[1].dropna()
        if not month_one.empty:
            messages.append(
                f"Average M+1 retention: {fmt_pct(month_one.mean())} "
                f"(best cohort {month_one.idxmax()} at {fmt_pct(month_one.max())})."
            )

    horizon = max((m for m in numeric_months if m >= 1), default=None)
    if horizon is not None and horizon != 1:
        horizon_data = retention[horizon].dropna()
        if not horizon_data.empty:
            messages.append(
                f"Median retention at M+{horizon}: {fmt_pct(horizon_data.median())} "
                f"(max/min {fmt_pct(horizon_data.max())} / {fmt_pct(horizon_data.min())})."
            )

    decay_months = [m for m in numeric_months if m >= 1]
    if len(decay_months) >= 2:
        first, last = decay_months[0], decay_months[-1]
        first_mean = retention[first].dropna().mean()
        last_mean = retention[last].dropna().mean()
        if pd.notna(first_mean) and pd.notna(last_mean):
            messages.append(
                f"Retention decays from {fmt_pct(first_mean)} (M+{first}) "
                f"to {fmt_pct(last_mean)} (M+{last})."
            )

    return messages[:limit]


def run_cli(input_path: Path, output_path: Path, insight_count: int) -> RetentionSummary:
    data = pd.read_csv(input_path, parse_dates=["order_date"])
    retention = build_retention(data)
    output_path.parent.mkdir(exist_ok=True, parents=True)
    retention.to_csv(output_path)
    insights = build_insights(retention, limit=insight_count)
    return RetentionSummary(table=retention, insights=insights)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Construit une table de rétention par cohorte à partir d’un CSV de commandes."
    )
    parser.add_argument(
        "--input",
        default="data/orders.csv",
        help="Path to the orders CSV.",
    )
    parser.add_argument(
        "--output",
        default="outputs/retention.csv",
        help="Path for the retention CSV output.",
    )
    parser.add_argument(
        "--insights",
        type=int,
        default=3,
        help="Number of insight sentences to print after writing the table.",
    )
    args = parser.parse_args()

    summary = run_cli(Path(args.input), Path(args.output), args.insights)
    print(f"Wrote {args.output} with shape {summary.table.shape}")
    if summary.insights:
        print("Key insights:")
        for line in summary.insights:
            print(f"- {line}")


if __name__ == "__main__":
    main()
