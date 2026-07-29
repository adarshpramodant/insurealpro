from flask import Blueprint, request, jsonify
from backend.services.database_service import DatabaseService
from backend.config.config import Config

history_bp = Blueprint('history', __name__)
db_service = DatabaseService(Config.DATABASE_PATH)

@history_bp.route('/history', methods=['GET'])
def get_history():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search = request.args.get('search', '')
    smoker = request.args.get('smoker', 'all')
    risk = request.args.get('risk', 'all')
    sort_by = request.args.get('sort_by', 'timestamp')
    order = request.args.get('order', 'DESC')
    
    data = db_service.get_history(page, per_page, search, smoker, risk, sort_by, order)
    return jsonify({"success": True, "data": data})

@history_bp.route('/history/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    success = db_service.delete_prediction(record_id)
    if success:
        return jsonify({"success": True, "message": f"Record {record_id} deleted."})
    return jsonify({"success": False, "message": "Record not found."}), 404

@history_bp.route('/history', methods=['DELETE'])
def clear_history():
    db_service.clear_history()
    return jsonify({"success": True, "message": "History database cleared."})
