from flask import Blueprint, render_template, jsonify
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.metrics_calculator import MetricsCalculator

# Main routes blueprint
main_bp = Blueprint('main', __name__)

# Initialize the metrics calculator
metrics_calculator = MetricsCalculator()

# ============================================================================
# MAIN ROUTES - TUTORIAL DASHBOARD
# ============================================================================

@main_bp.route('/')
def index():
    """Tutorial dashboard - the only page we need"""
    return render_template('tutorial-dashboard.html')

# ============================================================================
# API ROUTES - DYNAMIC DATA
# ============================================================================

@main_bp.route('/api/metrics')
def get_metrics():
    """Get all calculated metrics"""
    try:
        metrics = metrics_calculator.get_all_metrics()
        return jsonify({
            "success": True,
            "data": metrics
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/metrics/ltv')
def get_ltv():
    """Get LTV calculation"""
    try:
        ltv = metrics_calculator.calculate_ltv("stripe")
        return jsonify({
            "success": True,
            "data": ltv
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/metrics/ltv-cac-ratio')
def get_ltv_cac_ratio():
    """Get LTV:CAC ratio calculation"""
    try:
        ratio = metrics_calculator.calculate_ltv_cac_ratio()
        return jsonify({
            "success": True,
            "data": ratio
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/metrics/mrr')
def get_mrr():
    """Get MRR calculation"""
    try:
        mrr = metrics_calculator.calculate_mrr()
        return jsonify({
            "success": True,
            "data": mrr
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/metrics/arr')
def get_arr():
    """Get ARR calculation"""
    try:
        arr = metrics_calculator.calculate_arr()
        return jsonify({
            "success": True,
            "data": arr
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/metrics/payback-period')
def get_payback_period():
    """Get payback period calculation"""
    try:
        payback = metrics_calculator.calculate_payback_period()
        return jsonify({
            "success": True,
            "data": payback
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/metrics/conversion-rate')
def get_conversion_rate():
    """Get conversion rate calculation"""
    try:
        conversion = metrics_calculator.calculate_conversion_rate()
        return jsonify({
            "success": True,
            "data": conversion
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/metrics/retention')
def get_retention_metrics():
    """Get retention metrics calculation"""
    try:
        retention = metrics_calculator.calculate_retention_metrics()
        return jsonify({
            "success": True,
            "data": retention
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/metrics/nrr')
def get_nrr():
    """Get Net Revenue Retention calculation"""
    try:
        nrr = metrics_calculator.calculate_nrr()
        return jsonify({
            "success": True,
            "data": nrr
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/api/data/raw')
def get_raw_data():
    """Get raw business data"""
    try:
        return jsonify({
            "success": True,
            "data": metrics_calculator.data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500