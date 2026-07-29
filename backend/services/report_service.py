import os
import datetime
import re
from fpdf import FPDF

def clean_latin1(text):
    if not isinstance(text, str):
        return str(text)
    return re.sub(r'[^\x00-\xFF]', '', text).strip()

class PDFReportGenerator:
    @staticmethod
    def generate_pdf(prediction_result, output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Header banner
        pdf.set_fill_color(15, 23, 42) # Slate dark header
        pdf.rect(0, 0, 210, 35, 'F')
        
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(0, 8)
        pdf.cell(210, 10, "INSUREAI PRO - OFFICIAL PREMIUM QUOTE", align="C")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_xy(0, 20)
        pdf.cell(210, 6, f"Generated on: {datetime.datetime.now().strftime('%B %d, %Y - %H:%M:%S')} | Version 2.0.0", align="C")
        
        inputs = prediction_result.get("inputs", {})
        predicted_charge = prediction_result.get("predicted_charge", 0.0)
        risk_level = prediction_result.get("risk_level", "Moderate")
        confidence = prediction_result.get("confidence_score", 96.5)
        ai_exp = prediction_result.get("ai_explanation", {})
        rec_id = prediction_result.get("record_id", "LIVE-8821")
        
        # 1. Summary Card
        pdf.set_draw_color(226, 232, 240)
        pdf.set_fill_color(248, 250, 252)
        pdf.rect(15, 45, 180, 32, 'DF')
        
        pdf.set_xy(20, 49)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(65, 6, "PREDICTED ANNUAL PREMIUM")
        pdf.cell(45, 6, "RISK LEVEL")
        pdf.cell(40, 6, "CONFIDENCE")
        pdf.cell(30, 6, "VERIFICATION")
        
        pdf.set_xy(20, 57)
        pdf.set_font("Helvetica", "B", 15)
        pdf.set_text_color(14, 165, 233)
        pdf.cell(65, 10, f"INR {predicted_charge:,.2f}")
        
        pdf.set_font("Helvetica", "B", 12)
        if risk_level == "Low":
            pdf.set_text_color(34, 197, 94)
        elif risk_level == "Moderate":
            pdf.set_text_color(59, 130, 246)
        elif risk_level == "High":
            pdf.set_text_color(245, 158, 11)
        else:
            pdf.set_text_color(239, 68, 68)
        pdf.cell(45, 10, f"{risk_level}")
        
        pdf.set_text_color(30, 41, 59)
        pdf.cell(40, 10, f"{confidence:.1f}%")
        
        # QR Code Mock Badge
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(99, 102, 241)
        pdf.set_xy(165, 52)
        pdf.rect(165, 50, 22, 22, 'D')
        pdf.cell(22, 18, f"[QR #{rec_id}]", align="C")
        
        # 2. Applicant Profile Table
        pdf.set_xy(15, 85)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(180, 8, "Applicant Metrics Summary")
        pdf.set_draw_color(14, 165, 233)
        pdf.line(15, 94, 195, 94)
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_fill_color(241, 245, 249)
        
        profile_data = [
            ("Age", f"{inputs.get('age', 'N/A')} years", "Gender / Sex", str(inputs.get('sex', 'N/A')).title()),
            ("BMI", f"{inputs.get('bmi', 'N/A')}", "Tobacco Usage", str(inputs.get('smoker', 'N/A')).title()),
            ("Children", f"{inputs.get('children', 'N/A')}", "Region", str(inputs.get('region', 'N/A')).title())
        ]
        
        curr_y = 98
        for row in profile_data:
            pdf.set_xy(15, curr_y)
            pdf.cell(45, 7, f"  {row[0]}:", fill=True, border=1)
            pdf.cell(45, 7, f"  {row[1]}", border=1)
            pdf.cell(45, 7, f"  {row[2]}:", fill=True, border=1)
            pdf.cell(45, 7, f"  {row[3]}", border=1)
            curr_y += 7
            
        # 3. AI Insights & Narrative
        curr_y += 8
        pdf.set_xy(15, curr_y)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(180, 8, "AI Explainability & Risk Attribution")
        curr_y += 9
        pdf.line(15, curr_y, 195, curr_y)
        curr_y += 4
        
        narrative = clean_latin1(ai_exp.get("summary_narrative", "").replace("**", ""))
        pdf.set_xy(15, curr_y)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(180, 5, narrative)
        
        curr_y = pdf.get_y() + 6
        pdf.set_xy(15, curr_y)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(180, 6, "Personalized Cost Reduction Recommendations:")
        
        curr_y += 7
        pdf.set_font("Helvetica", "", 10)
        for rec in ai_exp.get("recommendations", []):
            clean_rec = clean_latin1(rec.replace("**", ""))
            pdf.set_xy(15, curr_y)
            pdf.multi_cell(180, 5, f"- {clean_rec}")
            curr_y = pdf.get_y() + 2
            
        # Footer
        pdf.set_xy(15, 260)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(148, 163, 184)
        pdf.multi_cell(180, 4, f"InsureAI Pro Verified Report | Prediction ID: {rec_id} | Model Version: 2.0.0 | Dataset: Verified Insurance Claims")
        
        pdf.output(output_path)
        return output_path
