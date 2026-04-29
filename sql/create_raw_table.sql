CREATE TABLE IF NOT EXISTS raw_xkcd_comics (
    comic_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    safe_title TEXT,
    comic_year INTEGER,
    comic_month INTEGER,
    comic_day INTEGER,
    publish_date DATE,
    image_url TEXT,
    alt_text TEXT,
    transcript TEXT,
    raw_json JSONB,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);