# XKCD Data Pipeline Case Study

## 1. Project Overview

This project is a data engineering case study that builds an end-to-end pipeline for ingesting XKCD comic data from the public XKCD API, loading it into a PostgreSQL database, transforming it into analytics-ready tables, and running data quality checks.

The goal is to demonstrate a basic data ingestion and modeling workflow, including:

- API extraction
- Database loading
- Data transformation
- Dimensional modeling
- Data quality validation
- Repeatable pipeline execution

## 2. Data Source

The data is extracted from the XKCD API.

Latest comic endpoint:

https://xkcd.com/info.0.json

Comic by ID endpoint:

https://xkcd.com/{comic_id}/info.0.json


The API returns comic metadata such as:

Comic ID
Title
Publish date
Image URL
Alt text
Transcript

## 3. Tech Stack

Python (3.11)
pandas
requests
psycopg2
PostgreSQL
pgAdmin
Anaconda environment
draw.io for ER diagram

## 4. Project Structure
```text
xkcd-data-pipeline/
├── ingestion/
│   ├── test_api.py
│   ├── test_db_connection.py
│   ├── load_one_comic.py
│   └── load_comics_range.py
├── quality/
│   └── run_data_quality_checks.py
├── sql/
│   ├── create_raw_table.sql
│   ├── create_analytical_table.sql
│   ├── transform_comic_metrics.sql
│   ├── create_dwh_tables.sql
│   └── transform_dwh_tables.sql
├── diagrams/
│   ├── ER.drawio
|   ├── ER.pdf
├── slides/
├── run_pipeline.py
├── requirements.txt
└── README.md
```

## 5. Database Design
```text
This project uses PostgreSQL and follows this structure:

XKCD API
   ↓
raw_xkcd_comics
   ↓
dim_comic + fact_comic_metrics
   ↓
data quality checks
```
raw_xkcd_comics stores the comic data directly extracted from the XKCD API.
The final model uses a Kimball-style dimensional structure.

dim_comic stores descriptive comic information.

fact_comic_metrics stores measurable business metrics.
check ER diagram under /diagrams for detailed column names and relation.

### Transformations

implemented using PostgreSQL SQL scripts.

The pipeline uses Python to run the SQL files in order. These SQL scripts create and populate the analytics and DWH tables, including:

analytics_comic_metrics
dim_comic
fact_comic_metrics

The derived business metrics include:

cost_eur
views
customer_review

## 6. Environment Setup

Create and activate a conda environment:

```bash
conda create -n xkcd_pipeline python=3.11
conda activate xkcd_pipeline
pip install -r requirements.txt
```

## 7. Database Setup

Create a PostgreSQL database named:

```text
xkcd_db

Create a .env file in the project root:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=xkcd_db
DB_USER=postgres
DB_PASSWORD=your_password_here

A template is provided in .env.example.
```

## 8. Run the pipeline

Run the full pipeline with:

```bash
python run_pipeline.py
```

This command will:

Create the required tables
Extract XKCD comic data from the API
Load raw data into PostgreSQL
Transform data into the DWH model
Run data quality checks


## 9. Data Quality Checks

Data quality checks are implemented in Python using pandas.

The checks validate that:

Tables are not empty
comic_id is not missing
comic_id is unique where required
Titles are not missing
Views are between 0 and 10,000
Customer reviews are between 1.0 and 10.0
Fact table rows match dimension table rows

To run checks separately:

```bash
python quality/run_data_quality_checks.py
```

## 10. Assumptions and Limitations
Comic ID is treated as the unique identifier.
Views and customer reviews are simulated because they are not provided by the XKCD API.
The project runs locally using PostgreSQL.
Airflow was considered for orchestration but not implemented in this local version.

## 11. Future Improvements
Scheduling the pipeline with Airflow
Running ingestion three times per week
Adding polling logic for newly released comics
Using dbt for transformations and tests
Adding better logging and monitoring
Containerizing the project with Docker
Storing raw API responses in cloud storage

## 12. Summary

This project demonstrates a basic end-to-end data engineering workflow:

API extraction → PostgreSQL loading → DWH modeling → data quality validation
