-- Load descriptive comic data into dimension table
INSERT INTO dim_comic (
    comic_id,
    title,
    safe_title,
    publish_date,
    comic_year,
    comic_month,
    comic_day,
    image_url,
    alt_text,
    transcript,
    updated_at
)
SELECT
    comic_id,
    title,
    safe_title,
    publish_date,
    comic_year,
    comic_month,
    comic_day,
    image_url,
    alt_text,
    transcript,
    CURRENT_TIMESTAMP
FROM raw_xkcd_comics
ON CONFLICT (comic_id)
DO UPDATE SET
    title = EXCLUDED.title,
    safe_title = EXCLUDED.safe_title,
    publish_date = EXCLUDED.publish_date,
    comic_year = EXCLUDED.comic_year,
    comic_month = EXCLUDED.comic_month,
    comic_day = EXCLUDED.comic_day,
    image_url = EXCLUDED.image_url,
    alt_text = EXCLUDED.alt_text,
    transcript = EXCLUDED.transcript,
    updated_at = CURRENT_TIMESTAMP;


-- Load measurements into fact table, one fact row per comid
INSERT INTO fact_comic_metrics (
    comic_id,
    cost_eur,
    views,
    customer_review
)
SELECT
    comic_id,
    LENGTH(title) * 5.00 AS cost_eur,
    FLOOR(random() * 10000)::INTEGER AS views,
    ROUND((1 + random() * 9)::NUMERIC, 1) AS customer_review
FROM raw_xkcd_comics r
WHERE NOT EXISTS (
    SELECT 1
    FROM fact_comic_metrics f
    WHERE f.comic_id = r.comic_id
);