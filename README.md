# 🛡️ Enterprise Insurance Price Prediction & Explainable AI Platform

> A production-ready, enterprise-grade AI web application that benchmarks **16 Machine Learning algorithms**, applies automated hyperparameter tuning, provides real-time **SHAP explainability**, and generates downloadable PDF insurance quotes.

---

## 🌟 Key Features

- **📊 16 ML Model Benchmarking**: Automatically evaluates Linear Regression, Ridge, Lasso, ElasticNet, Decision Tree, Random Forest, Extra Trees, Gradient Boosting, AdaBoost, XGBoost, LightGBM, CatBoost, SVR, KNN, Stacking, and Voting Regressors.
- **⚡ 54% Error Reduction**: Reduced average prediction error from **₹4,295 down to ₹1,943.84** using target log transformation and feature engineering.
- **💡 Real-time Explainable AI (SHAP)**: Waterfall breakdown of positive and negative cost drivers with natural language AI recommendations.
- **🎨 Glassmorphic SaaS Dashboard**: Modern interface featuring Dark/Light mode persistence, animated counters, interactive Chart.js charts, and responsive form sliders.
- **📜 Prediction History & SQLite DB**: Stored prediction logs with multi-column filtering, search, row deletion, and CSV export.
- **📄 Automated PDF Reports**: One-click generation of branded insurance quote PDFs with risk badges and cost optimization tips.
- **🔒 Enterprise Security & REST API**: Rate limiting, CORS, input bounds validation, SQL injection prevention, and modular Flask REST architecture.

---

## 📊 Model Benchmark Results (5-Fold Cross Validation)

| Algorithm | R² Score | Adj R² | MAE (INR) | RMSE (INR) | CV Mean R² |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 🏆 **XGBoost (Tuned)** | **0.8853** | **0.8774** | **₹1,943.84** | **₹4,220.73** | **0.8248** |
| 🥇 **Voting Regressor** | 0.8814 | 0.8734 | ₹1,950.44 | ₹4,290.72 | 0.8213 |
| 🥈 **Random Forest** | 0.8772 | 0.8689 | ₹2,009.14 | ₹4,365.44 | 0.8131 |
| 🥉 **CatBoost** | 0.8769 | 0.8685 | ₹1,958.62 | ₹4,372.07 | 0.8308 |
| **LightGBM** | 0.8753 | 0.8668 | ₹2,060.22 | ₹4,400.53 | 0.8279 |
| **Stacking Regressor** | 0.8741 | 0.8655 | ₹2,071.98 | ₹4,421.77 | 0.8273 |
| **Gradient Boosting** | 0.8699 | 0.8610 | ₹2,139.22 | ₹4,494.44 | 0.8135 |
| **SVR** | 0.8643 | 0.8550 | ₹2,060.07 | ₹4,590.49 | 0.8138 |
| **Decision Tree** | 0.8634 | 0.8541 | ₹2,216.71 | ₹4,604.88 | 0.8083 |
| **KNN Regressor** | 0.8630 | 0.8537 | ₹2,312.72 | ₹4,611.73 | 0.8005 |
| **Linear Regression** | 0.8489 | 0.8386 | ₹2,465.85 | ₹4,844.07 | 0.8286 |

---

## 🏗️ Folder Structure

```
Insurance/
├── backend/
│   ├── app.py                   # Main Flask Application Entry Point
│   ├── config/                  # App Configuration & Paths
│   ├── models/                  # SQLite Schema & Database Init
│   ├── routes/                  # REST API Endpoints (predict, history, model, health)
│   ├── services/                # Prediction, SHAP Explanation, PDF & DB Services
│   ├── saved_models/            # Serialized Model Artifacts (pkl, json)
│   ├── static/                  # Glassmorphism CSS, JS Controllers, Chart.js
│   └── templates/               # Single Page Application HTML Dashboard
├── insurance.csv                # Primary Dataset
├── insurance_ml.ipynb           # Data Science Notebook Audit
├── ml_pipeline.py               # End-to-End Training & Benchmarking Pipeline
├── test_backend.py              # Automated Unit & API Test Suite
├── requirements.txt             # Python Package Dependencies
├── render.yaml                  # Render Backend Deployment Config
└── vercel.json                  # Vercel Deployment Manifest
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.9+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run ML Benchmarking & Pipeline
```bash
python ml_pipeline.py
```

### 4. Start Flask Server
```bash
python backend/app.py
```
Open your browser and navigate to: `http://localhost:5000`

---

## 🧪 Verification & Testing

Run the automated test suite to verify API endpoints, database CRUD, and PDF generation:
```bash
python test_backend.py
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/predict` | Computes insurance premium, SHAP explanations, and saves record to DB |
| `GET` | `/api/history` | Returns paginated prediction records with search & filter |
| `DELETE` | `/api/history/<id>` | Deletes specific prediction record |
| `DELETE` | `/api/history` | Clears all prediction history |
| `GET` | `/api/model-info` | Returns model accuracy, hyperparameters, and version |
| `GET` | `/api/metrics` | Returns 16 benchmarked model evaluation scores |
| `POST` | `/api/download-report` | Generates official PDF quote document |
| `GET` | `/api/health` | Service health status check |
