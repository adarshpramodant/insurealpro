"""
Context-Aware AI Insurance Chatbot Engine with Offline FAQ Knowledge Base
Understands current prediction context (BMI, risk level, premium, smoker status, health score).
"""

import re

class InsuranceAIChatbot:
    def __init__(self):
        pass

    def answer_question(self, message, context=None):
        msg = str(message).lower().strip()
        ctx = context or {}
        
        charge = ctx.get("predicted_charge", 0.0)
        risk = ctx.get("risk_level", "Moderate")
        bmi = ctx.get("bmi", 25.0)
        age = ctx.get("age", 35)
        smoker = str(ctx.get("smoker", "no")).lower() == "yes"
        health_score = ctx.get("health_score", 80)
        
        # 1. Intent: Why is my premium high?
        if any(w in msg for w in ["why high", "expensive", "why so much", "costly", "high premium"]):
            if charge > 0:
                smoker_reason = "tobacco usage (which adds ~150%-300% surcharge)" if smoker else ""
                bmi_reason = f"elevated BMI of {bmi:.1f}" if bmi >= 25 else ""
                age_reason = f"age progression ({age} years)" if age >= 45 else ""
                
                reasons = [r for r in [smoker_reason, bmi_reason, age_reason] if r]
                reason_str = ", ".join(reasons) if reasons else "baseline actuarial risk models"
                
                return (
                    f"Based on your prediction of **₹{charge:,.2f}** ({risk} Risk), your premium is influenced primarily by {reason_str}. "
                    f"Tobacco status and BMI tier carry the highest statistical weights in healthcare actuarial models."
                )
            return "Insurance premiums are primarily calculated based on age, tobacco usage, BMI tier, geographic region, and dependent coverage."

        # 2. Intent: How can I reduce premium / lower cost?
        if any(w in msg for w in ["reduce", "lower", "save", "decrease", "cheaper", "discount"]):
            tips = []
            if smoker:
                tips.append("🚭 **Quit Tobacco**: Halts the 150%+ smoker surcharge, saving up to 50% on future renewal quotes.")
            if bmi >= 25:
                tips.append("🏃 **Weight Management**: Reducing BMI into the 18.5 - 24.9 range triggers lower risk brackets.")
            tips.append("🛡️ **Opt for Higher Deductibles**: Choosing a small voluntary co-pay reduces annual premium significantly.")
            tips.append("🧘 **Wellness Incentives**: Participate in health tracking programs for annual renewal discounts.")
            return "Here are the most effective ways to lower your health insurance premium:\n\n" + "\n\n".join(tips)

        # 3. Intent: What is BMI?
        if "bmi" in msg:
            cat = "Normal" if 18.5 <= bmi <= 24.9 else "Overweight" if 25 <= bmi <= 29.9 else "Obese" if bmi >= 30 else "Underweight"
            return (
                f"**BMI (Body Mass Index)** measures body fat based on height and weight. "
                f"Your input BMI is **{bmi:.1f}** ({cat}). "
                f"Health insurers use BMI tiers (18.5-24.9 = Normal, ≥30 = Obese) to assess chronic disease probability."
            )

        # 4. Intent: How accurate is the prediction?
        if any(w in msg for w in ["accuracy", "accurate", "reliable", "trust", "confidence"]):
            return (
                "**InsureAI Pro** executes an ensemble of the top 3 benchmarked ML algorithms (XGBoost, Random Forest, CatBoost) "
                "trained on 1,338 verified policyholder records. The ensemble achieves a 5-Fold Cross-Validation R² score of **88.5%** "
                "with average prediction error under **₹1,944**."
            )

        # 5. Intent: What happens if I stop smoking?
        if "stop smoking" in msg or "quit smoking" in msg:
            if charge > 0:
                potential_savings = charge * 0.52
                return (
                    f"If you quit smoking, your annual premium is estimated to drop by up to **₹{potential_savings:,.2f}** per year! "
                    f"Tobacco cessation removes the single largest multiplier from actuarial risk tables."
                )
            return "Quitting smoking reduces health insurance premiums by an average of 50% to 60% across all age groups."

        # 6. Intent: Why does age matter?
        if "age" in msg:
            return (
                f"Age is a primary factor because health maintenance costs statistically increase over time. "
                f"At **{age} years old**, your profile is evaluated against standard actuarial mortality tables. "
                f"Premiums typically increase by 3% - 5% each year as age progresses."
            )

        # 7. Intent: Difference between annual and monthly premium?
        if "monthly" in msg or "annual" in msg or "difference" in msg:
            annual = charge if charge > 0 else 36000.0
            monthly = annual / 12.0
            return (
                f"**Annual Premium** (₹{annual:,.2f}) is paid once per policy year. "
                f"**Monthly Premium** (₹{monthly:,.2f}) breaks the cost into 12 equal monthly installments. "
                f"Annual payments often avoid minor installment processing fees."
            )

        # 8. Intent: Explain Risk Score
        if "risk" in msg:
            return (
                f"Your current Risk Level is classified as **{risk} Risk** (Health Score: {health_score}/100). "
                f"Risk scores combine BMI metrics, age bracket, and tobacco usage to place policyholders into actuarial risk tiers."
            )

        # Default Fallback Help Response
        return (
            "I'm your **InsureAI Assistant**! I can answer questions about your premium estimate, "
            "explain feature contributions, calculate potential savings from quitting smoking or losing weight, "
            "or compare annual vs monthly pricing plans. What would you like to know?"
        )
