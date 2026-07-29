from flask import Blueprint, jsonify
import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Insurance Price Prediction AI Engine",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "2.0.0"
    }), 200
