import os
import json
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


def fetch_latest_comic():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url, timeout=10)
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


if __name__ == "__main__":
    comic = fetch_latest_comic()
    insert_comic(comic)

    print("Inserted comic successfully!")
    print("Comic ID:", comic["num"])
    print("Title:", comic["title"])