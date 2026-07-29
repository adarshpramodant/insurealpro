"""
Personalized Advisory, Savings Optimization & Health Timeline Engine for InsureAI Pro
"""

class InsuranceAdvisorEngine:
    @staticmethod
    def generate_advisory_package(inputs, final_premium):
        age = int(inputs.get("age", 30))
        bmi = float(inputs.get("bmi", 25.0))
        smoker = str(inputs.get("smoker", "no")).lower().strip() == "yes"
        children = int(inputs.get("children", 0))
        sex = str(inputs.get("sex", "female")).lower().strip()
        region = str(inputs.get("region", "southeast")).lower().strip()

        # 1. Multi-frequency Rates
        multi_freq = {
            "annual": round(final_premium, 2),
            "monthly": round(final_premium / 12.0, 2),
            "quarterly": round(final_premium / 4.0, 2),
            "daily": round(final_premium / 365.0, 2)
        }

        # 2. Percentage Contribution Breakdown
        contributions = []
        if smoker:
            contributions.append({"factor": "Smoking Status", "percentage": "+35%", "impact": "positive", "amount": round(final_premium * 0.35, 2)})
        else:
            contributions.append({"factor": "Non-Smoker Status", "percentage": "-25%", "impact": "negative", "amount": round(final_premium * -0.25, 2)})

        age_pct = min(40, max(5, int((age - 18) * 0.8)))
        contributions.append({"factor": f"Age ({age} yrs)", "percentage": f"+{age_pct}%", "impact": "positive", "amount": round(final_premium * (age_pct / 100.0), 2)})

        bmi_pct = min(30, max(0, int((bmi - 22.5) * 1.5))) if bmi > 22.5 else -5
        bmi_sign = "+" if bmi_pct >= 0 else ""
        contributions.append({"factor": f"BMI ({bmi:.1f})", "percentage": f"{bmi_sign}{bmi_pct}%", "impact": "positive" if bmi_pct >= 0 else "negative", "amount": round(final_premium * (bmi_pct / 100.0), 2)})

        if children > 0:
            contributions.append({"factor": f"Dependents ({children} kids)", "percentage": f"+{children * 5}%", "impact": "positive", "amount": round(final_premium * (children * 0.05), 2)})
        
        contributions.append({"factor": "Region Adjustment", "percentage": "-2%", "impact": "negative", "amount": round(final_premium * -0.02, 2)})
        contributions.append({"factor": "Gender Schedule", "percentage": "-1%", "impact": "negative", "amount": round(final_premium * -0.01, 2)})

        # 3. Premium Optimization Savings Advisor
        optimization_options = []
        if smoker:
            quit_savings = round(final_premium * 0.52, 2)
            optimization_options.append({
                "action": "Quit Smoking",
                "target": "Tobacco-free lifestyle",
                "estimated_savings_annual": quit_savings,
                "estimated_savings_monthly": round(quit_savings / 12.0, 2),
                "badge": "Highest Impact"
            })

        if bmi >= 27.0:
            lose_wt_savings = round(final_premium * 0.16, 2)
            optimization_options.append({
                "action": "Lose 10 kg",
                "target": "Target BMI 25.0",
                "estimated_savings_annual": lose_wt_savings,
                "estimated_savings_monthly": round(lose_wt_savings / 12.0, 2),
                "badge": "Health Bonus"
            })

        if bmi >= 25.0:
            optimal_bmi_savings = round(final_premium * 0.12, 2)
            optimization_options.append({
                "action": "Target Healthy BMI 24",
                "target": "Optimal Weight Tier",
                "estimated_savings_annual": optimal_bmi_savings,
                "estimated_savings_monthly": round(optimal_bmi_savings / 12.0, 2),
                "badge": "Long-term Savings"
            })

        # 4. Projected Health Risk Timeline
        timeline = [
            {"year": "Today", "age": age, "estimated_premium": round(final_premium, 2)},
            {"year": "1 Year", "age": age + 1, "estimated_premium": round(final_premium * 1.035, 2)},
            {"year": "3 Years", "age": age + 3, "estimated_premium": round(final_premium * 1.11, 2)},
            {"year": "5 Years", "age": age + 5, "estimated_premium": round(final_premium * 1.20, 2)}
        ]

        # 5. National Average Comparison
        national_avg = 36000.0
        diff = final_premium - national_avg
        diff_pct = round((diff / national_avg) * 100.0, 1)
        
        comparison = {
            "national_average": national_avg,
            "user_premium": round(final_premium, 2),
            "difference_amount": round(diff, 2),
            "difference_percentage": diff_pct,
            "status": "above" if diff > 0 else "below",
            "explanation": (
                f"Your premium is {abs(diff_pct)}% {'above' if diff > 0 else 'below'} the national average of ₹{national_avg:,.2f}, "
                f"primarily driven by your {'tobacco status and ' if smoker else ''}age bracket."
            )
        }

        # 6. Health & Affordability Scores
        health_score = 100
        if smoker: health_score -= 35
        if bmi >= 30: health_score -= 25
        elif bmi >= 25: health_score -= 10
        if age > 50: health_score -= 10
        health_score = max(30, health_score)

        lifestyle_score = 95 if not smoker and 18.5 <= bmi <= 24.9 else 65 if not smoker else 40
        affordability_score = max(40, min(98, int(100 - (final_premium / 800))))

        # Plain English Narrative
        plain_english = (
            f"Your annual premium is estimated at ₹{final_premium:,.2f}. "
            f"This is mainly because {'you are a smoker, ' if smoker else 'you maintain a non-smoker status, '}"
            f"have a BMI of {bmi:.1f}, and are {age} years old. "
            f"Your region ({region.title()}) and gender have minimal adjustments."
        )

        # 7. 3-Tier Policy Options
        tier_plans = [
            {
                "tier": "Basic Plan",
                "annual_premium": round(final_premium * 0.75, 2),
                "monthly_premium": round((final_premium * 0.75) / 12.0, 2),
                "coverage": "₹5,00,000 Sum Insured",
                "benefits": ["Hospitalization Coverage", "Emergency Ambulance Rider", "20% Co-pay Requirement"],
                "recommended_for": "Budget-conscious policyholders seeking core hospital coverage."
            },
            {
                "tier": "Standard Plan (Recommended)",
                "annual_premium": round(final_premium, 2),
                "monthly_premium": round(final_premium / 12.0, 2),
                "coverage": "₹15,00,000 Sum Insured",
                "benefits": ["Zero Co-pay", "Day Care Procedures", "Annual Health Checkup", "Pre & Post Hospitalization"],
                "recommended_for": "Most popular choice offering comprehensive balance of price and coverage."
            },
            {
                "tier": "Premium Executive Plan",
                "annual_premium": round(final_premium * 1.35, 2),
                "monthly_premium": round((final_premium * 1.35) / 12.0, 2),
                "coverage": "₹50,00,000 Sum Insured",
                "benefits": ["Global Cover", "No Room Rent Capping", "Organ Donor Cover", "International Concierge"],
                "recommended_for": "High-net-worth individuals requiring zero-limit international health cover."
            }
        ]

        return {
            "multi_frequency": multi_freq,
            "percentage_breakdown": contributions,
            "optimization_options": optimization_options,
            "timeline": timeline,
            "national_comparison": comparison,
            "scores": {
                "health_score": health_score,
                "lifestyle_score": lifestyle_score,
                "affordability_score": affordability_score
            },
            "plain_english_explanation": plain_english,
            "tier_plans": tier_plans
        }
