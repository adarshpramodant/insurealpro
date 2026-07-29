import os
from flask import Blueprint, request, jsonify, send_file
from backend.services.export_service import MultiFormatExportService
from backend.services.audit_service import AuditLoggerService
from backend.config.config import Config

export_bp = Blueprint('export', __name__)
audit_service = AuditLoggerService(Config.DATABASE_PATH)

@export_bp.route('/export', methods=['POST'])
def export_prediction():
    data = request.get_json() or {}
    fmt = str(data.get('format', 'pdf')).lower().strip()
    prediction_data = data.get('prediction', {})
    
    if not prediction_data:
        return jsonify({"success": False, "error": "Missing prediction payload."}), 400
        
    ext_map = {"pdf": ".pdf", "csv": ".csv", "excel": ".xlsx", "xlsx": ".xlsx", "json": ".json"}
    ext = ext_map.get(fmt, ".pdf")
    
    temp_file = os.path.join(Config.BASE_DIR, f"export_temp{ext}")
    mimetype_map = {
        "pdf": "application/pdf",
        "csv": "text/csv",
        "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "json": "application/json"
    }
    
    try:
        MultiFormatExportService.export_prediction(prediction_data, fmt, temp_file)
        
        # Log export action
        ip = request.remote_addr or "127.0.0.1"
        audit_service.log_event("EXPORT_GENERATED", ip, "session-main", prediction_data.get("record_id"), {
            "format": fmt
        })
        
        return send_file(
            temp_file,
            as_attachment=True,
            download_name=f"InsureAI_Pro_Quote_{prediction_data.get('record_id', 'latest')}{ext}",
            mimetype=mimetype_map.get(fmt, "application/pdf")
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
