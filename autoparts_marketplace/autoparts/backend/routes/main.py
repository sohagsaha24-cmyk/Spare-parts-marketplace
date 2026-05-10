from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Single-page app: UI loads data via /api/* endpoints.
    return render_template('index.html')
