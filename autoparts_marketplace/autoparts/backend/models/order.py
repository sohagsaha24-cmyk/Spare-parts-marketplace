from backend.models.db import get_db_connection, query_db

class Order:
    @staticmethod
    def get_all():
        sql = """
            SELECT o.*, p.name as product_name, p.price as product_price,
                   p.category, p.brand
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.id
            ORDER BY o.order_date DESC
        """
        return query_db(sql)

    @staticmethod
    def get_by_id(order_id):
        sql = """
            SELECT o.*, p.name as product_name, p.price as product_price,
                   p.category, p.brand, p.image_url
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.id
            WHERE o.id = %s
        """
        return query_db(sql, (order_id,), fetchone=True)

    @staticmethod
    def create(product_id, customer_name, mobile, address, quantity):
        sql = """
            INSERT INTO orders (product_id, customer_name, mobile, address, quantity)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, (product_id, customer_name, mobile, address, quantity))
            row = cur.fetchone()
            # With psycopg3 we use dict_row, so access by key.
            order_id = row["id"] if isinstance(row, dict) else row[0]
            conn.commit()
            return order_id
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_status(order_id, status):
        return query_db("UPDATE orders SET status=%s WHERE id=%s", (status, order_id), commit=True)

    @staticmethod
    def delete(order_id):
        return query_db("DELETE FROM orders WHERE id = %s", (order_id,), commit=True)

    @staticmethod
    def get_stats():
        stats = {}
        stats['total_orders'] = query_db("SELECT COUNT(*) as c FROM orders", fetchone=True)['c']
        stats['pending'] = query_db("SELECT COUNT(*) as c FROM orders WHERE status='pending'", fetchone=True)['c']
        stats['confirmed'] = query_db("SELECT COUNT(*) as c FROM orders WHERE status='confirmed'", fetchone=True)['c']
        stats['total_products'] = query_db("SELECT COUNT(*) as c FROM products", fetchone=True)['c']
        return stats
