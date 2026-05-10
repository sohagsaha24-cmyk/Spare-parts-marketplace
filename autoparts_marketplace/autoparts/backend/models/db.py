import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Load .env properly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def get_db_connection():
    """Create and return a database connection."""
    conn = psycopg.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),   # ✅ FIXED (no fallback wrong DB)
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', ''),
        row_factory=dict_row,
    )
    return conn


def query_db(sql, params=None, fetchone=False, commit=False):
    """Execute SQL safely and return results."""
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(sql, params or ())

        if commit:
            conn.commit()
            return cur.rowcount

        if fetchone:
            return cur.fetchone()

        return cur.fetchall()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()