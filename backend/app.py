import os
import sys

# Add base directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from backend.config.config import Config
from backend.models.database import init_db
from backend.routes import (
    predict_bp, history_bp, model_bp, health_bp,
    chatbot_bp, whatif_bp, admin_bp, export_bp, docs_bp
)

def create_app():
    app = Flask(__name__, 
                static_folder="static", 
                template_folder="templates")
                
    app.config.from_object(Config)
    
    # Initialize Database Schema
    init_db(Config.DATABASE_PATH)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Enable Rate Limiting
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["500 per day", "100 per hour"],
        storage_uri="memory://"
    )
    
    # Rate limit prediction & chatbot endpoints
    limiter.limit("20 per minute")(predict_bp)
    limiter.limit("30 per minute")(chatbot_bp)
    
    # Register Blueprints with /api prefix
    app.register_blueprint(predict_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")
    app.register_blueprint(model_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(chatbot_bp, url_prefix="/api")
    app.register_blueprint(whatif_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(export_bp, url_prefix="/api")
    app.register_blueprint(docs_bp, url_prefix="/api")
    
    # Serve Web Application Index
    @app.route("/")
    def index():
        return render_template("index.html")
        
    @app.route("/static/<path:filename>")
    def serve_static(filename):
        return send_from_directory(app.static_folder, filename)
        
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    print(f"[INFO] Starting InsureAI Pro Enterprise Application on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
