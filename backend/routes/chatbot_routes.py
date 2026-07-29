from flask import Blueprint, request, jsonify
from backend.services.chatbot_service import InsuranceAIChatbot
from backend.services.audit_service import AuditLoggerService
from backend.config.config import Config

chatbot_bp = Blueprint('chatbot', __name__)
chatbot_engine = InsuranceAIChatbot()
audit_service = AuditLoggerService(Config.DATABASE_PATH)

@chatbot_bp.route('/chatbot', methods=['POST'])
def handle_chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    context = data.get('context', {})
    
    if not message.strip():
        return jsonify({"success": False, "error": "Message body cannot be empty."}), 400
        
    try:
        reply = chatbot_engine.answer_question(message, context)
        
        # Log chatbot query
        ip = request.remote_addr or "127.0.0.1"
        audit_service.log_event("CHATBOT_QUERY", ip, "session-main", None, {
            "user_message": message,
            "response": reply[:100]
        })
        
        return jsonify({"success": True, "reply": reply}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
