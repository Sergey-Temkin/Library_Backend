# checkconection.py
# To run paste: py checkconection.py
import psycopg2

DATABASE_URL = "External URL of server"

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)