import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(".env")

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
db_version = cursor.fetchone()

print("Database connection successful!")
print(db_version[0])

cursor.close()
conn.close()