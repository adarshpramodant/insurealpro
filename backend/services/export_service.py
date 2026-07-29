"""
Multi-Format Exporter for InsureAI Pro (PDF, CSV, Excel, JSON)
"""

import os
import json
import pandas as pd
from backend.services.report_service import PDFReportGenerator

class MultiFormatExportService:
    @staticmethod
    def export_prediction(prediction_data, format_type, output_path):
        fmt = str(format_type).lower().strip()
        
        if fmt == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(prediction_data, f, indent=2)
            return output_path
            
        elif fmt in ["csv", "excel", "xlsx"]:
            flat_record = {
                "Prediction ID": prediction_data.get("record_id", "N/A"),
                "Timestamp": prediction_data.get("timestamp", "N/A"),
                "Age": prediction_data.get("inputs", {}).get("age"),
                "Sex": prediction_data.get("inputs", {}).get("sex"),
                "BMI": prediction_data.get("inputs", {}).get("bmi"),
                "Children": prediction_data.get("inputs", {}).get("children"),
                "Smoker": prediction_data.get("inputs", {}).get("smoker"),
                "Region": prediction_data.get("inputs", {}).get("region"),
                "Predicted Premium (INR)": prediction_data.get("predicted_charge"),
                "Risk Level": prediction_data.get("risk_level"),
                "Confidence Score": prediction_data.get("confidence_score"),
                "Model Version": prediction_data.get("model_version", "2.0.0")
            }
            df = pd.DataFrame([flat_record])
            if fmt == "csv":
                df.to_csv(output_path, index=False)
            else:
                try:
                    df.to_excel(output_path, index=False)
                except Exception:
                    # Fallback to CSV if openpyxl not installed
                    df.to_csv(output_path, index=False)
            return output_path
            
        else: # Default PDF
            PDFReportGenerator.generate_pdf(prediction_data, output_path)
            return output_path
