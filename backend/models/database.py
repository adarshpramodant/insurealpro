import sqlite3
import os

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 1. Predictions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            age INTEGER NOT NULL,
            sex TEXT NOT NULL,
            bmi REAL NOT NULL,
            children INTEGER NOT NULL,
            smoker TEXT NOT NULL,
            region TEXT NOT NULL,
            predicted_charge REAL NOT NULL,
            confidence_score REAL NOT NULL,
            risk_level TEXT NOT NULL,
            top_factors TEXT,
            ai_explanation TEXT,
            model_version TEXT,
            dataset_version TEXT DEFAULT '1.0.0',
            feature_version TEXT DEFAULT '1.0.0'
        )
    ''')
    
    # 2. Enterprise Audit Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            action_type TEXT NOT NULL,
            ip_address TEXT,
            session_id TEXT,
            prediction_id INTEGER,
            details TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
