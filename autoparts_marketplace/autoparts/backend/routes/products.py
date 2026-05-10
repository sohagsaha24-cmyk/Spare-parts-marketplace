from flask import Blueprint, render_template, abort
from backend.models.product import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/<int:product_id>')
def detail(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product)
