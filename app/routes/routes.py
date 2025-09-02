from flask import Blueprint, render_template

# Main routes blueprint
main_bp = Blueprint('main', __name__)

# ============================================================================
# MAIN ROUTES - TUTORIAL DASHBOARD ONLY
# ============================================================================

@main_bp.route('/')
def index():
    """Tutorial dashboard - the only page we need"""
    return render_template('tutorial-dashboard.html')