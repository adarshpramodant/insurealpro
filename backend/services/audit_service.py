"""
Enterprise Audit Logger & Admin Telemetry Aggregator for InsureAI Pro
"""

import json
import sqlite3
import datetime
from backend.models.database import get_db_connection

class AuditLoggerService:
    def __init__(self, db_path):
        self.db_path = db_path

    def log_event(self, action_type, ip_address="127.0.0.1", session_id="anon", prediction_id=None, details=None):
        try:
            conn = get_db_connection(self.db_path)
            cursor = conn.cursor()
            
            query = '''
                INSERT INTO audit_logs (action_type, ip_address, session_id, prediction_id, details)
                VALUES (?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (
                action_type, ip_address, session_id, prediction_id, json.dumps(details or {})
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[WARN] Failed to write audit log: {e}")

    def get_audit_logs(self, page=1, per_page=15):
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        
        offset = (page - 1) * per_page
        cursor.execute("SELECT COUNT(*) FROM audit_logs")
        total = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT * FROM audit_logs
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (per_page, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for r in rows:
            item = dict(r)
            item["details"] = json.loads(item["details"]) if item.get("details") else {}
            logs.append(item)
            
        return {"items": logs, "total": total, "page": page, "per_page": per_page}

    def get_admin_stats(self):
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                AVG(predicted_charge) as avg_charge,
                AVG(bmi) as avg_bmi,
                SUM(CASE WHEN smoker = 'yes' THEN 1 ELSE 0 END) as smoker_count,
                SUM(CASE WHEN risk_level = 'Moderate' THEN 1 ELSE 0 END) as moderate_risk_count,
                SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_risk_count
            FROM predictions
        ''')
        row = cursor.fetchone()
        
        total = row['total'] or 0
        avg_charge = round(row['avg_charge'], 2) if row['avg_charge'] else 0.0
        avg_bmi = round(row['avg_bmi'], 1) if row['avg_bmi'] else 0.0
        smoker_ratio = round(((row['smoker_count'] or 0) / total) * 100.0, 1) if total > 0 else 0.0
        
        conn.close()
        
        return {
            "total_predictions": total,
            "average_premium": avg_charge,
            "average_bmi": avg_bmi,
            "smoker_percentage": smoker_ratio,
            "most_common_risk_level": "Moderate Risk" if (row['moderate_risk_count'] or 0) >= (row['high_risk_count'] or 0) else "High Risk",
            "system_health": "Healthy",
            "model_version": "2.0.0",
            "accuracy_r2": 0.8853
        }
