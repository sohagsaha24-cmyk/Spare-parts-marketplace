from flask import Blueprint, jsonify, request, session
from backend.models.product import Product

api_bp = Blueprint("api", __name__)


@api_bp.get("/categories")
def categories():
    return jsonify({"categories": Product.get_categories()})


@api_bp.get("/products")
def products_list():
    category = (request.args.get("category") or "").strip() or None
    search = (request.args.get("search") or "").strip() or None
    products = Product.get_all(category=category, search=search)
    return jsonify({"products": products})


@api_bp.post("/products")
def products_create():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Admin login required"}), 401

    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    brand = (data.get("brand") or "").strip()
    category = (data.get("category") or "").strip()
    description = (data.get("description") or "").strip()
    image_url = (data.get("image_url") or "").strip()
    compatibility = (data.get("compatibility") or "").strip()

    if not name or not brand or not category:
        return jsonify({"error": "name, brand, and category are required"}), 400

    try:
        price = float(data.get("price") or 0)
        stock = int(data.get("stock") or 0)
    except (TypeError, ValueError):
        return jsonify({"error": "price must be a number and stock must be an integer"}), 400

    Product.create(
        name=name,
        category=category,
        brand=brand,
        price=price,
        stock=stock,
        image_url=image_url,
        description=description,
        compatibility=compatibility,
    )

    return jsonify({"ok": True}), 201

