import os
import sys

import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv(".env")


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def run_check(check_name, condition):
    """
    Prints PASS or FAIL for a data quality check.
    If condition is True, the check passes.
    If condition is False, the check fails.
    """
    if condition:
        print(f"PASS: {check_name}")
        return True
    else:
        print(f"FAIL: {check_name}")
        return False


def main():
    conn = get_db_connection()

    raw_df = pd.read_sql("SELECT * FROM raw_xkcd_comics", conn)
    analytics_df = pd.read_sql("SELECT * FROM analytics_comic_metrics", conn)
    dim_comic_df = pd.read_sql("SELECT * FROM dim_comic", conn)
    fact_metrics_df = pd.read_sql("SELECT * FROM fact_comic_metrics", conn)

    conn.close()

    print("Running data quality checks...\n")

    results = []

    # Raw table checks
    results.append(
        run_check(
            "raw_xkcd_comics has rows",
            len(raw_df) > 0,
        )
    )

    results.append(
        run_check(
            "comic_id has no missing values",
            raw_df["comic_id"].notna().all(),
        )
    )

    results.append(
        run_check(
            "comic_id is unique",
            raw_df["comic_id"].is_unique,
        )
    )

    results.append(
        run_check(
            "title has no missing or empty values",
            raw_df["title"].notna().all()
            and (raw_df["title"].astype(str).str.strip() != "").all(),
        )
    )

    results.append(
        run_check(
            "publish_date has no missing values",
            raw_df["publish_date"].notna().all(),
        )
    )

    # Analytics table checks
    results.append(
        run_check(
            "analytics_comic_metrics has rows",
            len(analytics_df) > 0,
        )
    )

    results.append(
        run_check(
            "cost_eur is not negative",
            (analytics_df["cost_eur"] >= 0).all(),
        )
    )

    results.append(
        run_check(
            "views are between 0 and 10000",
            analytics_df["views"].between(0, 10000).all(),
        )
    )

    results.append(
        run_check(
            "customer_review is between 1.0 and 10.0",
            analytics_df["customer_review"].between(1.0, 10.0).all(),
        )
    )

    results.append(
        run_check(
            "each analytics row has a matching raw comic",
            analytics_df["comic_id"].isin(raw_df["comic_id"]).all(),
        )
    )
        # DWH dimension table checks
    results.append(
        run_check(
            "dim_comic has rows",
            len(dim_comic_df) > 0,
        )
    )

    results.append(
        run_check(
            "dim_comic comic_id has no missing values",
            dim_comic_df["comic_id"].notna().all(),
        )
    )

    results.append(
        run_check(
            "dim_comic comic_id is unique",
            dim_comic_df["comic_id"].is_unique,
        )
    )

    results.append(
        run_check(
            "dim_comic title has no missing or empty values",
            dim_comic_df["title"].notna().all()
            and (dim_comic_df["title"].astype(str).str.strip() != "").all(),
        )
    )

    # DWH fact table checks
    results.append(
        run_check(
            "fact_comic_metrics has rows",
            len(fact_metrics_df) > 0,
        )
    )

    results.append(
        run_check(
            "fact_comic_metrics comic_id has no missing values",
            fact_metrics_df["comic_id"].notna().all(),
        )
    )

    results.append(
        run_check(
            "each fact row has a matching dim_comic row",
            fact_metrics_df["comic_id"].isin(dim_comic_df["comic_id"]).all(),
        )
    )

    results.append(
        run_check(
            "fact_comic_metrics cost_eur is not negative",
            (fact_metrics_df["cost_eur"] >= 0).all(),
        )
    )

    results.append(
        run_check(
            "fact_comic_metrics views are between 0 and 10000",
            fact_metrics_df["views"].between(0, 10000).all(),
        )
    )

    results.append(
        run_check(
            "fact_comic_metrics customer_review is between 1.0 and 10.0",
            fact_metrics_df["customer_review"].between(1.0, 10.0).all(),
        )
    )

    print("\nSummary:")
    print(f"Passed checks: {sum(results)} / {len(results)}")

    if all(results):
        print("All data quality checks passed.")
        sys.exit(0)
    else:
        print("Some data quality checks failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()