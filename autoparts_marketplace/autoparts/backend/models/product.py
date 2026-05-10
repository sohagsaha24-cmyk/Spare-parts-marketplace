from backend.models.db import query_db

class Product:
    @staticmethod
    def get_all(category=None, search=None):
        sql = "SELECT * FROM products"
        params = []
        conditions = []
        if category:
            conditions.append("category = %s")
            params.append(category)
        if search:
            conditions.append("(name ILIKE %s OR brand ILIKE %s OR description ILIKE %s)")
            params += [f'%{search}%', f'%{search}%', f'%{search}%']
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY created_at DESC"
        return query_db(sql, params)

    @staticmethod
    def get_by_id(product_id):
        return query_db("SELECT * FROM products WHERE id = %s", (product_id,), fetchone=True)

    @staticmethod
    def get_categories():
        rows = query_db("SELECT DISTINCT category FROM products ORDER BY category")
        return [r['category'] for r in rows]

    @staticmethod
    def create(name, category, brand, price, stock, image_url, description, compatibility):
        sql = """
            INSERT INTO products (name, category, brand, price, stock, image_url, description, compatibility)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return query_db(sql, (name, category, brand, price, stock, image_url, description, compatibility), commit=True)

    @staticmethod
    def update(product_id, name, category, brand, price, stock, image_url, description, compatibility):
        sql = """
            UPDATE products SET name=%s, category=%s, brand=%s, price=%s, stock=%s,
            image_url=%s, description=%s, compatibility=%s WHERE id=%s
        """
        return query_db(sql, (name, category, brand, price, stock, image_url, description, compatibility, product_id), commit=True)

    @staticmethod
    def delete(product_id):
        return query_db("DELETE FROM products WHERE id = %s", (product_id,), commit=True)
