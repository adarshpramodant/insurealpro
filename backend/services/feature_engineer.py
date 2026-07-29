import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class InsuranceFeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_out = X.copy()
        
        # Ensure standard column naming
        if 'sex' in X_out.columns:
            X_out['is_female'] = (X_out['sex'].astype(str).str.strip().str.lower() == 'female').astype(int)
        
        if 'smoker' in X_out.columns:
            X_out['is_smoker'] = (X_out['smoker'].astype(str).str.strip().str.lower() == 'yes').astype(int)
        
        # BMI Categories
        if 'bmi' in X_out.columns:
            bmi = X_out['bmi']
            X_out['is_obese'] = (bmi >= 30.0).astype(int)
            X_out['bmi_squared'] = bmi ** 2
            
        if 'age' in X_out.columns:
            X_out['age_squared'] = X_out['age'] ** 2
            
        # High impact interaction terms
        if 'bmi' in X_out.columns and 'is_smoker' in X_out.columns:
            X_out['smoker_bmi'] = X_out['is_smoker'] * X_out['bmi']
            X_out['smoker_obese'] = X_out['is_smoker'] * X_out['is_obese']
            
        if 'age' in X_out.columns and 'is_smoker' in X_out.columns:
            X_out['smoker_age'] = X_out['is_smoker'] * X_out['age']
            
        if 'age' in X_out.columns and 'bmi' in X_out.columns:
            X_out['age_bmi'] = X_out['age'] * X_out['bmi']
            
        return X_out
