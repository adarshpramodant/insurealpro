import os

class Config:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
    DATABASE_PATH = os.path.join(BASE_DIR, "insurance_history.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", "enterprise-insurance-ai-secret-key-2026")
    
    # Model Artifact Paths
    MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "trained_model.pkl")
    PREPROCESSOR_PATH = os.path.join(SAVED_MODELS_DIR, "preprocessor.pkl")
    ENCODER_PATH = os.path.join(SAVED_MODELS_DIR, "encoder.pkl")
    PIPELINE_PATH = os.path.join(SAVED_MODELS_DIR, "pipeline.pkl")
    FEATURE_NAMES_PATH = os.path.join(SAVED_MODELS_DIR, "feature_names.json")
    METADATA_PATH = os.path.join(SAVED_MODELS_DIR, "metadata.json")
    VERSION_PATH = os.path.join(SAVED_MODELS_DIR, "version.json")
    
    # Risk Level Thresholds (charges in INR/USD equivalent)
    LOW_RISK_MAX = 5000.0
    MODERATE_RISK_MAX = 15000.0
    HIGH_RISK_MAX = 30000.0
