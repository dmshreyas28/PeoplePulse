"""Interactive model testing script"""
import sys
sys.path.insert(0, r'e:\PeoplePulse\ml\pipeline')

import joblib
import pandas as pd

print("=" * 60)
print("PEOPLEPULSE - EMPLOYEE ATTRITION PREDICTION TEST")
print("=" * 60)

# Load the model
print("\nLoading model...")
model_path = r'e:\PeoplePulse\ml\models\model.pkl'
artifacts = joblib.load(model_path)
model = artifacts['model']
preprocessor = artifacts['preprocessor']

print("✓ Model loaded successfully!")
print(f"✓ Model type: {type(model).__name__}")
print(f"✓ Features expected: {len(artifacts['feature_names'])}")

# Sample employees to test
employees = [
    {
        'name': 'High Risk Employee',
        'data': {
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
    },
    {
        'name': 'Low Risk Employee',
        'data': {
            'Age': 49,
            'Gender': 'Male',
            'Department': 'Research & Development',
            'JobRole': 'Research Scientist',
            'Education': 1,
            'EducationField': 'Life Sciences',
            'YearsAtCompany': 10,
            'YearsInCurrentRole': 7,
            'YearsSinceLastPromotion': 1,
            'YearsWithCurrManager': 7,
            'NumCompaniesWorked': 1,
            'MonthlyIncome': 5130,
            'PercentSalaryHike': 11,
            'StockOptionLevel': 1,
            'TrainingTimesLastYear': 3,
            'JobSatisfaction': 2,
            'WorkLifeBalance': 3,
            'EnvironmentSatisfaction': 3,
            'RelationshipSatisfaction': 4,
            'PerformanceRating': 3,
            'BusinessTravel': 'Travel_Frequently',
            'DistanceFromHome': 8,
            'MaritalStatus': 'Married',
            'OverTime': 'No',
            'DailyRate': 279,
            'HourlyRate': 61,
            'MonthlyRate': 9362,
            'JobLevel': 2,
            'JobInvolvement': 2,
            'TotalWorkingYears': 10,
            'EmployeeCount': 1,
            'StandardHours': 80,
            'Over18': 'Y'
        }
    },
    {
        'name': 'Medium Risk Employee',
        'data': {
            'Age': 37,
            'Gender': 'Male',
            'Department': 'Research & Development',
            'JobRole': 'Laboratory Technician',
            'Education': 2,
            'EducationField': 'Medical',
            'YearsAtCompany': 7,
            'YearsInCurrentRole': 0,
            'YearsSinceLastPromotion': 0,
            'YearsWithCurrManager': 0,
            'NumCompaniesWorked': 6,
            'MonthlyIncome': 2090,
            'PercentSalaryHike': 13,
            'StockOptionLevel': 0,
            'TrainingTimesLastYear': 3,
            'JobSatisfaction': 2,
            'WorkLifeBalance': 3,
            'EnvironmentSatisfaction': 4,
            'RelationshipSatisfaction': 1,
            'PerformanceRating': 3,
            'BusinessTravel': 'Travel_Rarely',
            'DistanceFromHome': 2,
            'MaritalStatus': 'Single',
            'OverTime': 'Yes',
            'DailyRate': 1373,
            'HourlyRate': 92,
            'MonthlyRate': 2396,
            'JobLevel': 1,
            'JobInvolvement': 2,
            'TotalWorkingYears': 7,
            'EmployeeCount': 1,
            'StandardHours': 80,
            'Over18': 'Y'
        }
    }
]

def predict_employee(employee_data, employee_name="Employee"):
    """Make prediction for an employee"""
    try:
        # Create DataFrame
        df = pd.DataFrame([employee_data])
        
        # Preprocess
        X, _ = preprocessor.prepare_data(df, fit=False)
        
        # Predict
        proba = model.predict_proba(X)[0]
        attrition_prob = proba[1]
        
        # Determine risk level
        if attrition_prob < 0.3:
            risk = "LOW"
            color = "🟢"
        elif attrition_prob < 0.6:
            risk = "MEDIUM"
            color = "🟡"
        else:
            risk = "HIGH"
            color = "🔴"
        
        # Print results
        print(f"\n{color} {employee_name}")
        print(f"   Attrition Probability: {attrition_prob*100:.2f}%")
        print(f"   Risk Level: {risk}")
        print(f"   Age: {employee_data['Age']}, Role: {employee_data['JobRole']}")
        print(f"   Years at Company: {employee_data['YearsAtCompany']}, Income: ${employee_data['MonthlyIncome']:,}")
        print(f"   Overtime: {employee_data['OverTime']}, Job Satisfaction: {employee_data['JobSatisfaction']}/4")
        
        return attrition_prob, risk
        
    except Exception as e:
        print(f"\n❌ Error predicting for {employee_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

# Test all sample employees
print("\n" + "=" * 60)
print("TESTING SAMPLE EMPLOYEES")
print("=" * 60)

for emp in employees:
    predict_employee(emp['data'], emp['name'])

# Summary
print("\n" + "=" * 60)
print("MODEL TEST COMPLETE!")
print("=" * 60)
print("\nKey Factors for Attrition:")
print("  🔴 High Risk: Low satisfaction, overtime, frequent job changes")
print("  🟡 Medium Risk: Mixed indicators")
print("  🟢 Low Risk: High satisfaction, stable tenure, no overtime")
print("\n" + "=" * 60)
