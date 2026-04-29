import os
import subprocess
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


load_dotenv(".env")

PROJECT_ROOT = Path(__file__).parent


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def run_sql_file(file_path):
    print(f"\nRunning SQL file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        sql = file.read()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    print(f"Finished SQL file: {file_path}")


def run_python_script(script_path):
    print(f"\nRunning Python script: {script_path}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        check=True,
    )

    print(f"Finished Python script: {script_path}")
    return result


def main():
    print("Starting XKCD data pipeline...")

    # Create raw table
    run_sql_file(PROJECT_ROOT / "sql" / "create_raw_table.sql")

    # Load XKCD comic data into table
    run_python_script(PROJECT_ROOT / "ingestion" / "load_comics_range.py")

    # Create simple analytics table
    run_sql_file(PROJECT_ROOT / "sql" / "create_analytical_table.sql")

    # Transform raw data into simple analytics table
    run_sql_file(PROJECT_ROOT / "sql" / "transform_comic_metrics.sql")

    # Create DWH dimension and fact tables
    run_sql_file(PROJECT_ROOT / "sql" / "create_dwh_tables.sql")

    # Transform raw data into DWH tables
    run_sql_file(PROJECT_ROOT / "sql" / "transform_dwh_tables.sql")

    # Run data quality checks
    run_python_script(PROJECT_ROOT / "quality" / "run_data_quality_checks.py")

    print("\nPipeline finished successfully!")


if __name__ == "__main__":
    main()