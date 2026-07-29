"""
What-If Scenario Simulator Engine for InsureAI Pro
Simulates real-time deltas for smoking cessation, weight loss, age progression, or regional relocation.
"""

from backend.services.prediction_service import PredictionService

class WhatIfSimulatorEngine:
    def __init__(self):
        self.pred_service = PredictionService()

    def simulate(self, baseline_inputs, scenario_overrides):
        sim_inputs = baseline_inputs.copy()
        
        # Apply Overrides
        if "simulated_smoker" in scenario_overrides:
            sim_inputs["smoker"] = scenario_overrides["simulated_smoker"]
            
        if "simulated_bmi" in scenario_overrides:
            sim_inputs["bmi"] = float(scenario_overrides["simulated_bmi"])
        elif "weight_loss_kg" in scenario_overrides:
            loss_kg = float(scenario_overrides["weight_loss_kg"])
            # Approx BMI reduction for standard 1.70m height
            bmi_reduction = loss_kg / (1.70**2)
            sim_inputs["bmi"] = max(18.5, float(sim_inputs["bmi"]) - bmi_reduction)

        if "simulated_age" in scenario_overrides:
            sim_inputs["age"] = int(scenario_overrides["simulated_age"])
        elif "age_delta_years" in scenario_overrides:
            sim_inputs["age"] = int(sim_inputs["age"]) + int(scenario_overrides["age_delta_years"])

        if "simulated_children" in scenario_overrides:
            sim_inputs["children"] = int(scenario_overrides["simulated_children"])

        if "simulated_region" in scenario_overrides:
            sim_inputs["region"] = str(scenario_overrides["simulated_region"])

        # Compute predictions
        base_res = self.pred_service.predict(baseline_inputs)
        sim_res = self.pred_service.predict(sim_inputs)

        base_premium = base_res["predicted_charge"]
        sim_premium = sim_res["predicted_charge"]
        
        savings_annual = round(base_premium - sim_premium, 2)
        savings_monthly = round(savings_annual / 12.0, 2)
        pct_change = round(((sim_premium - base_premium) / base_premium) * 100.0, 1)

        return {
            "baseline_inputs": baseline_inputs,
            "simulated_inputs": sim_inputs,
            "baseline_premium": base_premium,
            "simulated_premium": sim_premium,
            "annual_savings": savings_annual,
            "monthly_savings": savings_monthly,
            "percentage_change": pct_change,
            "is_savings": savings_annual > 0,
            "simulated_risk_level": sim_res["risk_level"]
        }
