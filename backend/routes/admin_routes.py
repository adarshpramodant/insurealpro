from flask import Blueprint, request, jsonify
from backend.services.audit_service import AuditLoggerService
from backend.config.config import Config

admin_bp = Blueprint('admin', __name__)
audit_service = AuditLoggerService(Config.DATABASE_PATH)

@admin_bp.route('/admin/stats', methods=['GET'])
def get_admin_stats():
    stats = audit_service.get_admin_stats()
    return jsonify({"success": True, "data": stats})

@admin_bp.route('/admin/audit-logs', methods=['GET'])
def get_audit_logs():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 15))
    logs = audit_service.get_audit_logs(page, per_page)
    return jsonify({"success": True, "data": logs})
