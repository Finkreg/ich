import os
import time
import MySQLdb

DB_HOST = os.environ.get("DATABASE_HOST", "db")
DB_PORT = int(os.environ.get("DATABASE_PORT", 3306))
DB_USER = os.environ.get("DATABASE_USER")
DB_PASS = os.environ.get("DATABASE_PASSWORD")
DB_NAME = os.environ.get("DATABASE_NAME")

while True:
    try:
        conn = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            db=DB_NAME,
            port=DB_PORT
        )
        conn.close()
        print("✅ Database is ready!")
        break
    except MySQLdb.OperationalError:
        print("⏳ Waiting for database...")
        time.sleep(2)
