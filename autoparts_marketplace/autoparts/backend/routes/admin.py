import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from backend.models.product import Product
from backend.models.order import Order
from dotenv import load_dotenv

load_dotenv()

admin_bp = Blueprint('admin', __name__)

ADMIN_USER = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASSWORD', 'admin123')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    stats = Order.get_stats()
    recent_orders = Order.get_all()[:5]
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

@admin_bp.route('/products')
@login_required
def products():
    all_products = Product.get_all()
    return render_template('admin/products.html', products=all_products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        Product.create(
            name=request.form.get('name'),
            category=request.form.get('category'),
            brand=request.form.get('brand'),
            price=float(request.form.get('price', 0)),
            stock=int(request.form.get('stock', 0)),
            image_url=request.form.get('image_url', ''),
            description=request.form.get('description', ''),
            compatibility=request.form.get('compatibility', '')
        )
        flash('Product added successfully!')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', product=None, action='Add')

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found')
        return redirect(url_for('admin.products'))
    if request.method == 'POST':
        Product.update(
            product_id=product_id,
            name=request.form.get('name'),
            category=request.form.get('category'),
            brand=request.form.get('brand'),
            price=float(request.form.get('price', 0)),
            stock=int(request.form.get('stock', 0)),
            image_url=request.form.get('image_url', ''),
            description=request.form.get('description', ''),
            compatibility=request.form.get('compatibility', '')
        )
        flash('Product updated successfully!')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', product=product, action='Edit')

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    Product.delete(product_id)
    flash('Product deleted.')
    return redirect(url_for('admin.products'))

@admin_bp.route('/orders')
@login_required
def orders():
    all_orders = Order.get_all()
    return render_template('admin/orders.html', orders=all_orders)

@admin_bp.route('/orders/status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    status = request.form.get('status')
    Order.update_status(order_id, status)
    flash('Order status updated.')
    return redirect(url_for('admin.orders'))

@admin_bp.route('/orders/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    Order.delete(order_id)
    flash('Order deleted.')
    return redirect(url_for('admin.orders'))
