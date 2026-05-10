from backend.models.db import query_db


def ensure_schema():
    """
    Ensure required tables/columns exist.
    Safe to run multiple times; useful when DB was created with an older schema.
    """
    # products table + columns
    query_db(
        """
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
        """,
        commit=True,
    )

    query_db("ALTER TABLE products ADD COLUMN IF NOT EXISTS description TEXT DEFAULT ''", commit=True)
    query_db("ALTER TABLE products ADD COLUMN IF NOT EXISTS image_url TEXT DEFAULT ''", commit=True)
    query_db("ALTER TABLE products ADD COLUMN IF NOT EXISTS compatibility TEXT DEFAULT ''", commit=True)
    query_db("ALTER TABLE products ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP", commit=True)

    # orders table
    query_db(
        """
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
        """,
        commit=True,
    )

