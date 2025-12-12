"""Browse employees by Employee Number, Department, Job Role"""
import sys
sys.path.insert(0, r'e:\PeoplePulse\ml\pipeline')

import pandas as pd
import joblib

# Load dataset
print("Loading IBM HR Dataset...")
df = pd.read_csv(r'e:\PeoplePulse\data\raw\WA_Fn-UseC_-HR-Employee-Attrition.csv')

print("\n" + "=" * 80)
print("EMPLOYEE BROWSER - Find Employees by ID, Department, or Job Role")
print("=" * 80)

print(f"\n📊 Total Employees in Dataset: {len(df):,}")
print(f"📋 Employee Numbers Range: {df['EmployeeNumber'].min()} to {df['EmployeeNumber'].max()}")

# Show departments
print("\n" + "=" * 80)
print("🏢 DEPARTMENTS AVAILABLE:")
print("=" * 80)
for i, (dept, count) in enumerate(df['Department'].value_counts().items(), 1):
    print(f"{i}. {dept}: {count:,} employees")

# Show job roles
print("\n" + "=" * 80)
print("💼 JOB ROLES AVAILABLE:")
print("=" * 80)
for i, (role, count) in enumerate(df['JobRole'].value_counts().items(), 1):
    print(f"{i:2d}. {role}: {count:,} employees")

# Show sample employee numbers
print("\n" + "=" * 80)
print("🔢 SAMPLE EMPLOYEE NUMBERS (First 20):")
print("=" * 80)
sample_employees = df.head(20)[['EmployeeNumber', 'Department', 'JobRole', 'Age', 'Attrition']]
print(sample_employees.to_string(index=False))

# Interactive selection
print("\n" + "=" * 80)
print("SELECT EMPLOYEES TO ANALYZE:")
print("=" * 80)
print("\nOptions:")
print("1. Search by Employee Number (e.g., 1234)")
print("2. Filter by Department (e.g., Sales)")
print("3. Filter by Job Role (e.g., Sales Executive)")
print("4. Show random employees")
print("5. Show high-risk employees (those who left)")
print("6. Show specific employee numbers")

choice = input("\nEnter your choice (1-6): ").strip()

selected_df = None

if choice == "1":
    emp_num = int(input("Enter Employee Number: "))
    selected_df = df[df['EmployeeNumber'] == emp_num]
    
elif choice == "2":
    print("\nAvailable Departments:")
    for i, dept in enumerate(df['Department'].unique(), 1):
        print(f"{i}. {dept}")
    dept_name = input("Enter Department name: ").strip()
    selected_df = df[df['Department'].str.contains(dept_name, case=False)]
    
elif choice == "3":
    print("\nAvailable Job Roles:")
    for i, role in enumerate(df['JobRole'].unique(), 1):
        print(f"{i}. {role}")
    role_name = input("Enter Job Role: ").strip()
    selected_df = df[df['JobRole'].str.contains(role_name, case=False)]
    
elif choice == "4":
    num = int(input("How many random employees? (1-50): "))
    selected_df = df.sample(min(num, 50))
    
elif choice == "5":
    selected_df = df[df['Attrition'] == 'Yes']
    num = int(input(f"Found {len(selected_df)} employees who left. Show how many? (1-50): "))
    selected_df = selected_df.head(min(num, 50))
    
elif choice == "6":
    emp_nums = input("Enter Employee Numbers (comma-separated, e.g., 1234,5678,910): ").strip()
    emp_list = [int(x.strip()) for x in emp_nums.split(',')]
    selected_df = df[df['EmployeeNumber'].isin(emp_list)]

if selected_df is not None and len(selected_df) > 0:
    print(f"\n✓ Found {len(selected_df)} employee(s)")
    print("\n" + "=" * 80)
    print("EMPLOYEE DETAILS:")
    print("=" * 80)
    
    # Show key columns
    cols_to_show = ['EmployeeNumber', 'Age', 'Gender', 'Department', 'JobRole', 
                    'YearsAtCompany', 'MonthlyIncome', 'OverTime', 'JobSatisfaction', 
                    'WorkLifeBalance', 'Attrition']
    print(selected_df[cols_to_show].to_string(index=False))
    
    # Ask if user wants predictions
    predict = input("\n\nDo you want attrition predictions for these employees? (y/n): ").strip().lower()
    
    if predict == 'y':
        print("\nLoading model...")
        model_path = r'e:\PeoplePulse\ml\models\model.pkl'
        artifacts = joblib.load(model_path)
        model = artifacts['model']
        preprocessor = artifacts['preprocessor']
        
        print("\nGenerating predictions...\n")
        print("=" * 80)
        
        for idx, row in selected_df.iterrows():
            # Prepare data
            emp_data = row.to_dict()
            test_df = pd.DataFrame([emp_data])
            
            # Add required fields
            if 'EmployeeCount' not in test_df.columns:
                test_df['EmployeeCount'] = 1
            if 'StandardHours' not in test_df.columns:
                test_df['StandardHours'] = 80
            if 'Over18' not in test_df.columns:
                test_df['Over18'] = 'Y'
            
            try:
                # Preprocess and predict
                X, _ = preprocessor.prepare_data(test_df, fit=False)
                proba = model.predict_proba(X)[0]
                attrition_prob = proba[1]
                
                # Risk level
                if attrition_prob < 0.3:
                    risk = "🟢 LOW"
                elif attrition_prob < 0.6:
                    risk = "🟡 MEDIUM"
                else:
                    risk = "🔴 HIGH"
                
                print(f"\nEmployee #{row['EmployeeNumber']} - {row['JobRole']}")
                print(f"   Attrition Risk: {risk} ({attrition_prob*100:.2f}%)")
                print(f"   Details: Age {row['Age']}, {row['YearsAtCompany']} years, ${row['MonthlyIncome']:,}/mo")
                print(f"   Actual Status: {'LEFT' if row['Attrition'] == 'Yes' else 'ACTIVE'}")
                
            except Exception as e:
                print(f"   ❌ Error predicting: {str(e)}")
        
        print("\n" + "=" * 80)
else:
    print("\n❌ No employees found or invalid selection")

print("\n" + "=" * 80)
print("DONE!")
print("=" * 80)
