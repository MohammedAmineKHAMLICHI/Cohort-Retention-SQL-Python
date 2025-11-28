import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from src.retention import build_retention


def sample_orders() -> pd.DataFrame:
    data = [
        (1, 1, "2024-01-10", 10.0),
        (2, 1, "2024-02-05", 12.0),
        (3, 2, "2024-01-12", 10.0),
        (4, 3, "2024-02-02", 11.0),
        (5, 3, "2024-04-02", 11.0),
        (6, 4, "2024-03-15", 19.0),
    ]
    df = pd.DataFrame(data, columns=["order_id", "user_id", "order_date", "amount"])
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def test_retention_handles_multi_month_churn():
    df = sample_orders()
    retention = build_retention(df)

    assert retention.loc["2024-01", "cohort_size"] == 2
    assert retention.loc["2024-01", 1] == 50.0
    assert retention.loc["2024-02", 0] == 100.0
    assert retention.loc["2024-02", 1] == 0.0
    assert retention.loc["2024-02", 2] == 100.0


def test_build_retention_empty_input():
    empty = pd.DataFrame(columns=["order_id", "user_id", "order_date", "amount"])
    with pytest.raises(ValueError):
        build_retention(empty)


def test_cli_round_trip(tmp_path: Path):
    input_path = tmp_path / "orders.csv"
    output_path = tmp_path / "retention.csv"
    sample_orders().to_csv(input_path, index=False)

    result = subprocess.run(
        [
            sys.executable,
            "src/retention.py",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--insights",
            "2",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert output_path.exists()
    csv = pd.read_csv(output_path)
    assert "cohort_size" in csv.columns
    assert "Key insights" in result.stdout


def test_sql_query_retention(tmp_path: Path):
    orders = sample_orders()
    con = duckdb.connect()
    con.register("orders_df", orders)
    con.execute("CREATE OR REPLACE TABLE orders AS SELECT * FROM orders_df")

    sql_path = Path(__file__).resolve().parents[1] / "sql" / "queries.sql"
    sql_retention = con.sql(sql_path.read_text()).df()
    sql_retention["cohort_month"] = (
        pd.to_datetime(sql_retention["cohort_month"])
        .dt.to_period("M")
        .astype(str)
    )

    python_retention = build_retention(orders)
    january_sql = sql_retention[
        (sql_retention["cohort_month"] == "2024-01") & (sql_retention["month_index"] == 1)
    ]["retention_pct"].iloc[0]
    assert january_sql == pytest.approx(python_retention.loc["2024-01", 1])

    february_sizes = sql_retention[sql_retention["cohort_month"] == "2024-02"][
        "cohort_size"
    ].unique()
    assert len(february_sizes) == 1
    assert february_sizes[0] == python_retention.loc["2024-02", "cohort_size"]
