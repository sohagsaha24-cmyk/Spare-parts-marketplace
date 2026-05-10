import os
import re
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def _connect(**kwargs):
    """
    Prefer psycopg v3 (binary wheels) but fall back to psycopg2 if needed.
    This keeps setup_db.py runnable on more Windows Python versions.
    """
    try:
        import psycopg  # type: ignore
        return psycopg.connect(**kwargs)
    except ModuleNotFoundError:
        import psycopg2  # type: ignore
        return psycopg2.connect(**kwargs)


def create_db():
    if not DB_NAME:
        raise RuntimeError("DB_NAME is not set. Create a .env file based on .env.example")
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]{0,62}", DB_NAME):
        raise RuntimeError("DB_NAME contains invalid characters. Use letters/numbers/underscore only.")

    conn = _connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,))
    exists = cur.fetchone() is not None

    if not exists:
        cur.execute(f'CREATE DATABASE "{DB_NAME}"')
        print("Database created")
    else:
        print("Database already exists")

    conn.commit()
    cur.close()
    conn.close()


def create_tables():
    conn = _connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        brand VARCHAR(100) NOT NULL,
        category VARCHAR(100) NOT NULL,
        price NUMERIC(10,2) NOT NULL DEFAULT 0,
        stock INTEGER NOT NULL DEFAULT 0,
        description TEXT DEFAULT '',
        image_url TEXT DEFAULT '',
        compatibility TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Migrations for older databases (safe to run repeatedly)
    cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS description TEXT DEFAULT ''")
    cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS image_url TEXT DEFAULT ''")
    cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS compatibility TEXT DEFAULT ''")
    cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
        customer_name VARCHAR(255) NOT NULL,
        mobile VARCHAR(32) NOT NULL,
        address TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 1),
        status VARCHAR(20) NOT NULL DEFAULT 'pending',
        order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables created")


def insert_sample_data():
    conn = _connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM products")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("""
        INSERT INTO products (name, brand, category, price, stock, description, image_url)
        VALUES
        ('Brake Pad', 'Bosch', 'Brakes', 50, 10, 'Premium brake pad', 'https://via.placeholder.com/150'),
        ('Engine Oil', 'Shell', 'Oil', 30, 20, 'Synthetic oil', 'https://via.placeholder.com/150'),
        ('Air Filter', 'Toyota', 'Filter', 25, 15, 'High quality air filter', 'https://via.placeholder.com/150');
        """)
        conn.commit()
        print("Sample data inserted")
    else:
        print("Data already exists")

    cur.close()
    conn.close()


if __name__ == "__main__":
    print("Auto Setup Starting...")

    create_db()
    create_tables()
    insert_sample_data()

    print("Setup Complete! Run your Flask app now.")