CREATE TABLE IF NOT EXISTS dim_comic (
    comic_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    safe_title TEXT,
    publish_date DATE,
    comic_year INTEGER,
    comic_month INTEGER,
    comic_day INTEGER,
    image_url TEXT,
    alt_text TEXT,
    transcript TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_comic_metrics (
    metric_id SERIAL PRIMARY KEY,
    comic_id INTEGER NOT NULL,
    cost_eur NUMERIC(10, 2),
    views INTEGER,
    customer_review NUMERIC(3, 1),
    metric_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fact_comic
        FOREIGN KEY (comic_id)
        REFERENCES dim_comic(comic_id)
);