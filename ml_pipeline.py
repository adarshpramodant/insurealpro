"""
Comprehensive Machine Learning Training Pipeline for Insurance Price Prediction
Includes 16 model benchmarks, hyperparameter optimization, feature engineering, SHAP explainability,
and artifact packaging.
"""

import os
import sys
import json
import joblib
import time
import datetime
import numpy as np
import pandas as pd
import warnings

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

# Regression algorithms
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor, AdaBoostRegressor, StackingRegressor, VotingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import shap

warnings.filterwarnings('ignore')

from backend.services.feature_engineer import InsuranceFeatureEngineer


def run_ml_pipeline():
    print("=" * 70)
    print("🚀 STARTING PRODUCTION ML PIPELINE FOR INSURANCE PRICE PREDICTION")
    print("=" * 70)
    
    # 1. Load Data
    csv_path = "insurance.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
        
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    
    # 2. Preprocessing & Feature Engineering
    fe = InsuranceFeatureEngineer()
    df_engineered = fe.transform(df)
    
    # Target variable and log transformation for right-skewed target
    y_raw = df_engineered['charges'].values
    y_log = np.log1p(y_raw)
    
    # Define features
    feature_cols = [c for c in df_engineered.columns if c != 'charges']
    X = df_engineered[feature_cols]
    
    # Categorical and numerical columns
    cat_cols = ['sex', 'smoker', 'region']
    num_cols = [c for c in feature_cols if c not in cat_cols]
    
    # Pipeline preprocessor
    num_transformer = Pipeline(steps=[
        ('scaler', RobustScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_cols),
            ('cat', cat_transformer, cat_cols)
        ]
    )
    
    # Fit preprocessor & get feature names
    preprocessor.fit(X)
    
    # Obtain expanded feature names after one-hot encoding
    cat_feature_names = preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(cat_cols)
    all_feature_names = num_cols + list(cat_feature_names)
    
    X_trans = preprocessor.transform(X)
    X_trans_df = pd.DataFrame(X_trans, columns=all_feature_names)
    
    print(f"✅ Preprocessing completed. Total engineered features: {len(all_feature_names)}")
    print(f"Features: {all_feature_names}")
    
    # 3. Train/Test Split
    X_train, X_test, y_train_log, y_test_log, y_train_raw, y_test_raw = train_test_split(
        X_trans, y_log, y_raw, test_size=0.2, random_state=42
    )
    
    # 4. Model Benchmarking (16 Algorithms)
    print("\n" + "=" * 70)
    print("📊 BENCHMARKING 16 REGRESSION ALGORITHMS (5-FOLD CROSS VALIDATION)")
    print("=" * 70)
    
    base_models = {
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Lasso": Lasso(alpha=0.1),
        "ElasticNet": ElasticNet(alpha=0.1, l1_ratio=0.5),
        "Decision Tree": DecisionTreeRegressor(random_state=42, max_depth=6),
        "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
        "Extra Trees": ExtraTreesRegressor(n_estimators=200, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=200, random_state=42),
        "AdaBoost": AdaBoostRegressor(n_estimators=100, random_state=42),
        "XGBoost": xgb.XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42),
        "LightGBM": lgb.LGBMRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42, verbose=-1),
        "CatBoost": cb.CatBoostRegressor(iterations=300, learning_rate=0.05, depth=5, verbose=0, random_seed=42),
        "Support Vector Regression": SVR(C=1.0, epsilon=0.1),
        "KNN Regressor": KNeighborsRegressor(n_neighbors=7)
    }
    
    # Add Stacking & Voting Regressor using top estimators
    estimators = [
        ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
        ('xgb', xgb.XGBRegressor(n_estimators=100, max_depth=4, random_state=42)),
        ('lgb', lgb.LGBMRegressor(n_estimators=100, max_depth=4, random_state=42, verbose=-1)),
        ('cat', cb.CatBoostRegressor(iterations=200, verbose=0, random_seed=42))
    ]
    
    base_models["Stacking Regressor"] = StackingRegressor(
        estimators=estimators,
        final_estimator=Ridge()
    )
    
    base_models["Voting Regressor"] = VotingRegressor(
        estimators=estimators
    )
    
    benchmark_results = []
    trained_estimators = {}
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    n = len(X_test)
    p = X_trans.shape[1]
    
    for name, model in base_models.items():
        start_t = time.time()
        
        # Train on y_log
        model.fit(X_train, y_train_log)
        elapsed = time.time() - start_t
        
        # Predict & convert back from log space
        y_pred_log = model.predict(X_test)
        y_pred = np.expm1(y_pred_log)
        
        mae = mean_absolute_error(y_test_raw, y_pred)
        mse = mean_squared_error(y_test_raw, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test_raw, y_pred)
        adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
        
        # Cross validation R2
        cv_scores = cross_val_score(model, X_trans, y_log, cv=kf, scoring='r2')
        cv_mean = np.mean(cv_scores)
        cv_std = np.std(cv_scores)
        
        benchmark_results.append({
            "model": name,
            "mae": round(float(mae), 2),
            "mse": round(float(mse), 2),
            "rmse": round(float(rmse), 2),
            "r2": round(float(r2), 4),
            "adjusted_r2": round(float(adj_r2), 4),
            "cv_mean_r2": round(float(cv_mean), 4),
            "cv_std_r2": round(float(cv_std), 4),
            "training_time_sec": round(float(elapsed), 4)
        })
        
        trained_estimators[name] = model
        print(f"  {name:<28} | R²: {r2:.4f} | Adj R²: {adj_r2:.4f} | MAE: ₹{mae:,.2f} | RMSE: ₹{rmse:,.2f} | CV R²: {cv_mean:.4f}")

    # Convert results to DataFrame and sort by R²
    results_df = pd.DataFrame(benchmark_results).sort_values(by="r2", ascending=False)
    
    top_model_name = results_df.iloc[0]["model"]
    print(f"\n🏆 TOP PERFORMING BASE MODEL: {top_model_name} (R² = {results_df.iloc[0]['r2']})")
    
    # 5. Hyperparameter Tuning on Top Models
    print("\n" + "=" * 70)
    print(f"🎯 HYPERPARAMETER OPTIMIZATION (GRIDSEARCH / RANDOMIZEDSEARCH) FOR {top_model_name}")
    print("=" * 70)
    
    param_grids = {
        "CatBoost": {
            "depth": [4, 5, 6, 7],
            "learning_rate": [0.03, 0.05, 0.08, 0.1],
            "iterations": [200, 350, 500],
            "l2_leaf_reg": [1, 3, 5, 7]
        },
        "LightGBM": {
            "max_depth": [3, 4, 5, 6],
            "learning_rate": [0.02, 0.04, 0.06, 0.1],
            "n_estimators": [150, 250, 400],
            "num_leaves": [15, 31, 63],
            "subsample": [0.7, 0.85, 1.0]
        },
        "XGBoost": {
            "max_depth": [3, 4, 5, 6],
            "learning_rate": [0.02, 0.05, 0.08, 0.1],
            "n_estimators": [150, 250, 400],
            "subsample": [0.7, 0.85, 1.0],
            "colsample_bytree": [0.7, 0.85, 1.0]
        },
        "Random Forest": {
            "n_estimators": [150, 250, 400],
            "max_depth": [6, 10, 15, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4]
        },
        "Gradient Boosting": {
            "n_estimators": [150, 250, 400],
            "learning_rate": [0.03, 0.05, 0.1],
            "max_depth": [3, 4, 5],
            "subsample": [0.7, 0.85, 1.0]
        }
    }
    
    # Pick tuning model (default to CatBoost / LightGBM if top is not in grid)
    tune_target = top_model_name if top_model_name in param_grids else "CatBoost"
    
    if tune_target == "CatBoost":
        base_tune_estimator = cb.CatBoostRegressor(verbose=0, random_seed=42)
    elif tune_target == "LightGBM":
        base_tune_estimator = lgb.LGBMRegressor(random_state=42, verbose=-1)
    elif tune_target == "XGBoost":
        base_tune_estimator = xgb.XGBRegressor(random_state=42)
    elif tune_target == "Gradient Boosting":
        base_tune_estimator = GradientBoostingRegressor(random_state=42)
    else:
        base_tune_estimator = RandomForestRegressor(random_state=42)
        
    search = RandomizedSearchCV(
        estimator=base_tune_estimator,
        param_distributions=param_grids[tune_target],
        n_iter=25,
        scoring='r2',
        cv=kf,
        random_state=42,
        n_jobs=-1
    )
    
    search.fit(X_train, y_train_log)
    best_tuned_model = search.best_estimator_
    
    # Evaluate tuned model
    y_pred_tuned_log = best_tuned_model.predict(X_test)
    y_pred_tuned = np.expm1(y_pred_tuned_log)
    
    tuned_mae = mean_absolute_error(y_test_raw, y_pred_tuned)
    tuned_mse = mean_squared_error(y_test_raw, y_pred_tuned)
    tuned_rmse = np.sqrt(tuned_mse)
    tuned_r2 = r2_score(y_test_raw, y_pred_tuned)
    tuned_adj_r2 = 1 - (1 - tuned_r2) * (n - 1) / (n - p - 1)
    
    print(f"✅ Tuned Model ({tune_target}): Best Params = {search.best_params_}")
    print(f"✅ Tuned Metrics: R² = {tuned_r2:.4f} | Adj R² = {tuned_adj_r2:.4f} | MAE = ₹{tuned_mae:,.2f} | RMSE = ₹{tuned_rmse:,.2f}")
    
    # Build complete End-to-End Pipeline object
    full_pipeline = Pipeline([
        ('feature_engineer', fe),
        ('preprocessor', preprocessor),
        ('regressor', best_tuned_model)
    ])
    
    # 6. SHAP & Model Explainability
    print("\n" + "=" * 70)
    print("💡 CALCULATING SHAP FEATURE EXPLAINABILITY")
    print("=" * 70)
    
    try:
        explainer = shap.TreeExplainer(best_tuned_model)
        shap_values = explainer.shap_values(X_trans)
    except Exception as e:
        print(f"Using KernelExplainer fallback: {e}")
        explainer = shap.KernelExplainer(best_tuned_model.predict, shap.sample(X_trans, 50))
        shap_values = explainer.shap_values(X_trans)
        
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    feature_importance_dict = {
        feat: float(val) for feat, val in zip(all_feature_names, mean_abs_shap)
    }
    # Sort feature importance
    sorted_feature_importance = dict(sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True))
    
    # 7. Save Artifacts to backend/saved_models/
    save_dir = os.path.join("backend", "saved_models")
    os.makedirs(save_dir, exist_ok=True)
    
    joblib.dump(best_tuned_model, os.path.join(save_dir, "trained_model.pkl"))
    joblib.dump(preprocessor, os.path.join(save_dir, "preprocessor.pkl"))
    joblib.dump(cat_transformer, os.path.join(save_dir, "encoder.pkl"))
    joblib.dump(full_pipeline, os.path.join(save_dir, "pipeline.pkl"))
    
    with open(os.path.join(save_dir, "feature_names.json"), "w") as f:
        json.dump(all_feature_names, f, indent=2)
        
    metadata = {
        "model_name": f"Tuned {tune_target}",
        "r2_score": round(float(tuned_r2), 4),
        "adjusted_r2": round(float(tuned_adj_r2), 4),
        "mae": round(float(tuned_mae), 2),
        "mse": round(float(tuned_mse), 2),
        "rmse": round(float(tuned_rmse), 2),
        "best_hyperparameters": search.best_params_,
        "num_features": len(all_feature_names),
        "feature_names": all_feature_names,
        "feature_importance": sorted_feature_importance,
        "benchmark_summary": benchmark_results,
        "target_log_transformed": True,
        "trained_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(os.path.join(save_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
        
    version_info = {
        "version": "2.0.0",
        "release_name": "Enterprise Production Insurance AI Engine",
        "author": "Deepmind Agentic AI",
        "created_at": datetime.datetime.now().isoformat()
    }
    
    with open(os.path.join(save_dir, "version.json"), "w") as f:
        json.dump(version_info, f, indent=2)
        
    print("\n" + "=" * 70)
    print("🎉 ALL 7 MODEL ARTIFACTS SAVED SUCCESSFULLY TO backend/saved_models/")
    print("=" * 70)

if __name__ == "__main__":
    run_ml_pipeline()
