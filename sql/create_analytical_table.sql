CREATE TABLE IF NOT EXISTS analytics_comic_metrics (
    comic_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    publish_date DATE,
    title_length INTEGER,
    cost_eur NUMERIC(10, 2),
    views INTEGER,
    customer_review NUMERIC(3, 1),
    transformed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);