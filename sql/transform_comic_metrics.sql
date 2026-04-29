INSERT INTO analytics_comic_metrics (
    comic_id,
    title,
    publish_date,
    title_length,
    cost_eur,
    views,
    customer_review
)
SELECT
    comic_id,
    title,
    publish_date,
    LENGTH(title) AS title_length,
    LENGTH(title) * 5.00 AS cost_eur,
    FLOOR(random() * 10000)::INTEGER AS views,
    ROUND((1 + random() * 9)::NUMERIC, 1) AS customer_review
FROM raw_xkcd_comics
ON CONFLICT (comic_id)
DO UPDATE SET
    title = EXCLUDED.title,
    publish_date = EXCLUDED.publish_date,
    title_length = EXCLUDED.title_length,
    cost_eur = EXCLUDED.cost_eur,
    views = EXCLUDED.views,
    customer_review = EXCLUDED.customer_review,
    transformed_at = CURRENT_TIMESTAMP;