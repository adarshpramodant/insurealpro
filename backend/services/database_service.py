import json
import sqlite3
from backend.models.database import get_db_connection

class DatabaseService:
    def __init__(self, db_path):
        self.db_path = db_path

    def insert_prediction(self, data):
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            INSERT INTO predictions (
                age, sex, bmi, children, smoker, region,
                predicted_charge, confidence_score, risk_level,
                top_factors, ai_explanation, model_version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        top_factors_str = json.dumps(data.get('top_factors', []))
        ai_explanation_str = json.dumps(data.get('ai_explanation', {}))
        
        cursor.execute(query, (
            data['age'], data['sex'], data['bmi'], data['children'], data['smoker'], data['region'],
            data['predicted_charge'], data.get('confidence_score', 95.0), data.get('risk_level', 'Moderate'),
            top_factors_str, ai_explanation_str, data.get('model_version', '2.0.0')
        ))
        
        inserted_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return inserted_id

    def get_history(self, page=1, per_page=10, search="", smoker_filter="all", risk_filter="all", sort_by="timestamp", order="DESC"):
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        
        where_clauses = []
        params = []
        
        if search:
            where_clauses.append("(region LIKE ? OR sex LIKE ? OR smoker LIKE ?)")
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
            
        if smoker_filter and smoker_filter != "all":
            where_clauses.append("smoker = ?")
            params.append(smoker_filter)
            
        if risk_filter and risk_filter != "all":
            where_clauses.append("risk_level = ?")
            params.append(risk_filter)
            
        where_str = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Validate sort field
        valid_sorts = ["id", "timestamp", "age", "bmi", "predicted_charge", "risk_level"]
        if sort_by not in valid_sorts:
            sort_by = "timestamp"
            
        order_str = "ASC" if order.upper() == "ASC" else "DESC"
        
        # Count query
        count_query = f"SELECT COUNT(*) FROM predictions{where_str}"
        cursor.execute(count_query, params)
        total_records = cursor.fetchone()[0]
        
        # Data query
        offset = (page - 1) * per_page
        data_query = f'''
            SELECT * FROM predictions{where_str}
            ORDER BY {sort_by} {order_str}
            LIMIT ? OFFSET ?
        '''
        
        data_params = params + [per_page, offset]
        cursor.execute(data_query, data_params)
        rows = cursor.fetchall()
        
        items = []
        for r in rows:
            item = dict(r)
            item['top_factors'] = json.loads(item['top_factors']) if item.get('top_factors') else []
            item['ai_explanation'] = json.loads(item['ai_explanation']) if item.get('ai_explanation') else {}
            items.append(item)
            
        conn.close()
        
        total_pages = (total_records + per_page - 1) // per_page if per_page > 0 else 1
        
        return {
            "items": items,
            "total": total_records,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }

    def delete_prediction(self, record_id):
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions WHERE id = ?", (record_id,))
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted_count > 0

    def clear_history(self):
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()
        conn.close()
        return True

    def get_stats(self):
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*), AVG(predicted_charge), MIN(predicted_charge), MAX(predicted_charge) FROM predictions")
        row = cursor.fetchone()
        
        conn.close()
        return {
            "total_predictions": row[0] or 0,
            "avg_charge": round(row[1], 2) if row[1] else 0.0,
            "min_charge": round(row[2], 2) if row[2] else 0.0,
            "max_charge": round(row[3], 2) if row[3] else 0.0
        }
