from flask import Blueprint, request, jsonify
from backend.utils.validators import validate_predict_input
from backend.services.prediction_service import PredictionService
from backend.services.database_service import DatabaseService
from backend.services.audit_service import AuditLoggerService
from backend.config.config import Config

predict_bp = Blueprint('predict', __name__)
prediction_service = PredictionService()
db_service = DatabaseService(Config.DATABASE_PATH)
audit_service = AuditLoggerService(Config.DATABASE_PATH)

@predict_bp.route('/predict', methods=['POST'])
def predict_insurance():
    data = request.get_json() or {}
    
    is_valid, errors = validate_predict_input(data)
    if not is_valid:
        return jsonify({"success": False, "errors": errors}), 400
        
    try:
        result = prediction_service.predict(data)
        
        # Save prediction record to SQLite
        record_id = db_service.insert_prediction({
            "age": int(data["age"]),
            "sex": str(data["sex"]).lower(),
            "bmi": float(data["bmi"]),
            "children": int(data["children"]),
            "smoker": str(data["smoker"]).lower(),
            "region": str(data["region"]).lower(),
            "predicted_charge": result["predicted_charge"],
            "confidence_score": result["confidence_score"],
            "risk_level": result["risk_level"],
            "top_factors": result["feature_contributions"],
            "ai_explanation": result["ai_explanation"],
            "model_version": result["model_version"]
        })
        
        result["record_id"] = record_id
        
        # Audit Log
        ip = request.remote_addr or "127.0.0.1"
        audit_service.log_event("PREDICTION_GENERATED", ip, "session-main", record_id, {
            "inputs": data,
            "predicted_premium": result["predicted_charge"],
            "risk_level": result["risk_level"]
        })
        
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
