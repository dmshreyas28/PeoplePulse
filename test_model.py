"""Test the model directly"""
import sys
sys.path.insert(0, r'e:\PeoplePulse\ml\pipeline')

import joblib
import pandas as pd

# Load the model
print("Loading model...")
model_path = r'e:\PeoplePulse\ml\models\model.pkl'
artifacts = joblib.load(model_path)

print("\n=== MODEL ARTIFACTS ===")
print(f"Keys: {list(artifacts.keys())}")

# Check feature names from training
training_features = artifacts.get('feature_names', [])
print(f"\n=== TRAINING FEATURE NAMES ({len(training_features)} features) ===")
for i, feat in enumerate(training_features, 1):
    print(f"{i:2d}. {feat}")

# Test with sample employee data
print("\n=== TESTING PREDICTION ===")
sample_employee = {
    'Age': 41,
    'Gender': 'Female',
    'Department': 'Sales',
    'JobRole': 'Sales Executive',
    'Education': 2,
    'EducationField': 'Life Sciences',
    'YearsAtCompany': 6,
    'YearsInCurrentRole': 4,
    'YearsSinceLastPromotion': 0,
    'YearsWithCurrManager': 5,
    'NumCompaniesWorked': 8,
    'MonthlyIncome': 5993,
    'PercentSalaryHike': 11,
    'StockOptionLevel': 0,
    'TrainingTimesLastYear': 0,
    'JobSatisfaction': 4,
    'WorkLifeBalance': 1,
    'EnvironmentSatisfaction': 2,
    'RelationshipSatisfaction': 1,
    'PerformanceRating': 3,
    'BusinessTravel': 'Travel_Rarely',
    'DistanceFromHome': 1,
    'MaritalStatus': 'Single',
    'OverTime': 'Yes',
    'DailyRate': 1102,
    'HourlyRate': 94,
    'MonthlyRate': 19479,
    'JobLevel': 2,
    'JobInvolvement': 3,
    'TotalWorkingYears': 8,
    'EmployeeCount': 1,
    'StandardHours': 80,
    'Over18': 'Y'
}

# Create DataFrame
df = pd.DataFrame([sample_employee])
print(f"\nInput DataFrame columns ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

# Preprocess
print("\n=== PREPROCESSING ===")
preprocessor = artifacts['preprocessor']
X, _ = preprocessor.prepare_data(df, fit=False)

print(f"\nProcessed features shape: {X.shape}")
if hasattr(X, 'columns'):
    print(f"Processed feature names ({len(X.columns)}):")
    for i, col in enumerate(X.columns, 1):
        print(f"{i:2d}. {col}")
else:
    print("X is numpy array, not DataFrame")

# Predict
print("\n=== PREDICTION ===")
model = artifacts['model']
proba = model.predict_proba(X)[0]
print(f"Attrition probability: {proba[1]:.4f}")
print(f"Risk level: {'High' if proba[1] > 0.6 else 'Medium' if proba[1] > 0.3 else 'Low'}")
