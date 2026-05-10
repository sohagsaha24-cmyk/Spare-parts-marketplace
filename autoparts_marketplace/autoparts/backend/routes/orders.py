import os
import traceback
from flask import Blueprint, render_template, request, redirect, url_for, abort
from backend.models.order import Order
from backend.models.product import Product

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/checkout/<int:product_id>', methods=['GET'])
def checkout(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template('checkout.html', product=product)

@orders_bp.route('/place', methods=['POST'])
def place_order():
    try:
        product_id = int(request.form.get('product_id'))
        customer_name = request.form.get('customer_name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        address = request.form.get('address', '').strip()
        quantity = int(request.form.get('quantity', 1))

        # Basic validation
        if not all([customer_name, mobile, address]) or quantity < 1:
            return render_template('checkout.html',
                                   product=Product.get_by_id(product_id),
                                   error="Please fill all required fields.")

        product = Product.get_by_id(product_id)
        if not product:
            abort(404)

        if quantity > product['stock']:
            return render_template('checkout.html',
                                   product=product,
                                   error=f"Only {product['stock']} units available.")

        order_id = Order.create(product_id, customer_name, mobile, address, quantity)
        return redirect(url_for('orders.success', order_id=order_id))

    except Exception as e:
        # Don't hide the root cause during development.
        debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
        if debug:
            print("Order placement failed:")
            print(traceback.format_exc())
        return render_template('checkout.html',
                               product=Product.get_by_id(int(request.form.get('product_id', 0))),
                               error=("Something went wrong. Please try again."
                                      if not debug else f"Order failed: {type(e).__name__}"))

@orders_bp.route('/success/<int:order_id>')
def success(order_id):
    order = Order.get_by_id(order_id)
    if not order:
        abort(404)
    return render_template('order_success.html', order=order)
