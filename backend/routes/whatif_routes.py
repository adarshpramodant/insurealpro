from flask import Blueprint, request, jsonify
from backend.services.whatif_service import WhatIfSimulatorEngine
from backend.services.audit_service import AuditLoggerService
from backend.config.config import Config

whatif_bp = Blueprint('whatif', __name__)
whatif_engine = WhatIfSimulatorEngine()
audit_service = AuditLoggerService(Config.DATABASE_PATH)

@whatif_bp.route('/simulate', methods=['POST'])
def run_simulation():
    data = request.get_json() or {}
    baseline = data.get('baseline', {})
    overrides = data.get('overrides', {})
    
    if not baseline or "age" not in baseline:
        return jsonify({"success": False, "error": "Baseline payload with valid metrics required."}), 400
        
    try:
        res = whatif_engine.simulate(baseline, overrides)
        
        # Log audit event
        ip = request.remote_addr or "127.0.0.1"
        audit_service.log_event("WHATIF_SIMULATION", ip, "session-main", None, {
            "overrides": overrides,
            "annual_savings": res["annual_savings"]
        })
        
        return jsonify({"success": True, "data": res}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
