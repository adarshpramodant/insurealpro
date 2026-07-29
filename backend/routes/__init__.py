from .predict_routes import predict_bp
from .history_routes import history_bp
from .model_routes import model_bp
from .health_routes import health_bp
from .chatbot_routes import chatbot_bp
from .whatif_routes import whatif_bp
from .admin_routes import admin_bp
from .export_routes import export_bp
from .docs_routes import docs_bp

__all__ = [
    "predict_bp", "history_bp", "model_bp", "health_bp",
    "chatbot_bp", "whatif_bp", "admin_bp", "export_bp", "docs_bp"
]
