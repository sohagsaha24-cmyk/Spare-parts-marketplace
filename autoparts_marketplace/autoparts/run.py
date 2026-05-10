import os
from flask import Flask
from dotenv import load_dotenv
from backend.routes.products import products_bp
from backend.routes.orders import orders_bp
from backend.routes.admin import admin_bp
from backend.routes.main import main_bp
from backend.routes.api import api_bp
from backend.models.schema import ensure_schema

load_dotenv()

app = Flask(
    __name__,
    template_folder='backend/templates',
    static_folder='backend/static'
)

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    # Auto-migrate DB schema (safe to run repeatedly).
    try:
        ensure_schema()
    except Exception as e:
        # Let the app still start so the user can see errors in the console,
        # but surface a clear hint for the common "can't add product" case.
        print("WARNING: Database schema check failed. Verify Postgres is running and .env settings are correct.")
        print(f"Details: {e}")

    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
