# Changelog - InsureAI Pro

All notable changes to the **InsureAI Pro** platform are documented in this file.

## [2.0.0] - 2026-07-29
### Added
- **Multi-Model Confidence Ensemble**: 3-model confidence prediction engine executing XGBoost, Random Forest, and CatBoost simultaneously.
- **Explainable AI (SHAP & Plain English)**: Technical SHAP feature contributions + natural language narrative explanations.
- **Premium Optimization Advisor**: Savings calculation cards for quitting smoking, weight reduction, and healthy BMI targets.
- **Smart Live BMI Calculator**: Dual unit system (`cm/kg` & `in/lbs`), category badges, health gauge, and target range.
- **Interactive What-If Simulator**: Real-time delta scenario engine for lifestyle and age changes.
- **Admin Analytics Dashboard**: Telemetry overview (`/admin`) displaying predictions, smoker ratio, risk level distribution, and real-time audit logs.
- **Swagger / OpenAPI Documentation**: Interactive API documentation rendered at `/api/docs`.
- **Enterprise Audit Logging**: Action logging into SQLite `audit_logs` table.
- **Multi-Format Export**: One-click exports to PDF (with QR verification code), CSV, Excel, and JSON.
- **Accessibility System**: High contrast, large font, reduced motion, dark/light themes.

### Improved
- **Model Accuracy**: Reduced MAE from ₹4,295 to ₹1,943.84 (>54% error reduction) using target log transformation and feature engineering.
- **UI/UX Aesthetics**: Glassmorphism design system inspired by Stripe, Vercel, Linear, and PolicyBazaar.
- **Verification Test Suite**: Comprehensive 8-test unit and API integration test suite.
