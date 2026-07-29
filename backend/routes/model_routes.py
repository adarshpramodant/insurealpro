import os
from flask import Blueprint, request, jsonify, send_file
from backend.services.prediction_service import PredictionService
from backend.services.report_service import PDFReportGenerator
from backend.config.config import Config

model_bp = Blueprint('model', __name__)
prediction_service = PredictionService()

@model_bp.route('/model-info', methods=['GET'])
def get_model_info():
    info = prediction_service.get_model_info()
    return jsonify({"success": True, "data": info})

@model_bp.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = prediction_service.get_metrics()
    return jsonify({"success": True, "data": metrics})

@model_bp.route('/feature-importance', methods=['GET'])
def get_feature_importance():
    importance = prediction_service.get_feature_importance()
    return jsonify({"success": True, "data": importance})

@model_bp.route('/download-report', methods=['POST'])
def download_report():
    data = request.get_json() or {}
    if "predicted_charge" not in data:
        return jsonify({"success": False, "error": "Missing prediction payload"}), 400
        
    temp_pdf_path = os.path.join(Config.BASE_DIR, "temp_report.pdf")
    try:
        PDFReportGenerator.generate_pdf(data, temp_pdf_path)
        return send_file(
            temp_pdf_path,
            as_attachment=True,
            download_name=f"Insurance_AI_Quote_{data.get('record_id', 'latest')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
