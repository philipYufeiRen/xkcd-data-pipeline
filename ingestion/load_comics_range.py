import argparse
import os
import json
import time
from datetime import date

import requests
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


def fetch_latest_comic_id():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["num"]


def fetch_comic_by_id(comic_id):
    url = f"https://xkcd.com/{comic_id}/info.0.json"

    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        print(f"[INGESTION] Comic {comic_id} not found. Skipping.")
        return None

    response.raise_for_status()
    return response.json()


def insert_comic(comic):
    publish_date = date(
        int(comic["year"]),
        int(comic["month"]),
        int(comic["day"]),
    )

    sql = """
        INSERT INTO raw_xkcd_comics (
            comic_id,
            title,
            safe_title,
            comic_year,
            comic_month,
            comic_day,
            publish_date,
            image_url,
            alt_text,
            transcript,
            raw_json
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (comic_id)
        DO UPDATE SET
            title = EXCLUDED.title,
            safe_title = EXCLUDED.safe_title,
            comic_year = EXCLUDED.comic_year,
            comic_month = EXCLUDED.comic_month,
            comic_day = EXCLUDED.comic_day,
            publish_date = EXCLUDED.publish_date,
            image_url = EXCLUDED.image_url,
            alt_text = EXCLUDED.alt_text,
            transcript = EXCLUDED.transcript,
            raw_json = EXCLUDED.raw_json;
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        sql,
        (
            comic["num"],
            comic["title"],
            comic.get("safe_title"),
            int(comic["year"]),
            int(comic["month"]),
            int(comic["day"]),
            publish_date,
            comic.get("img"),
            comic.get("alt"),
            comic.get("transcript"),
            json.dumps(comic),
        ),
    )

    conn.commit()
    cursor.close()
    conn.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Load XKCD comics from the public API into PostgreSQL."
    )

    parser.add_argument(
        "--start-id",
        type=int,
        default=1,
        help="First XKCD comic ID to load. Default is 1.",
    )

    parser.add_argument(
        "--end-id",
        type=int,
        default=None,
        help="Last XKCD comic ID to load. If not provided, the latest comic ID is used.",
    )

    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.5,
        help="Pause between API requests. Default is 0.5 seconds.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    start_id = args.start_id
    end_id = args.end_id

    if end_id is None:
        print("[INGESTION] No end ID provided. Fetching latest XKCD comic ID...")
        end_id = fetch_latest_comic_id()

    if start_id > end_id:
        raise ValueError("start-id cannot be greater than end-id.")

    print(f"[INGESTION] Loading comics from ID {start_id} to {end_id}.")

    inserted_count = 0
    skipped_count = 0

    for comic_id in range(start_id, end_id + 1):
        print(f"[INGESTION] Fetching comic {comic_id}...")

        comic = fetch_comic_by_id(comic_id)

        if comic:
            insert_comic(comic)
            inserted_count += 1
            print(f"[LOAD] Inserted or updated comic {comic_id}: {comic['title']}")
        else:
            skipped_count += 1

        time.sleep(args.sleep_seconds)

    print("[INGESTION] Finished loading comics.")
    print(f"[INGESTION] Inserted/updated: {inserted_count}")
    print(f"[INGESTION] Skipped: {skipped_count}")


if __name__ == "__main__":
    main()