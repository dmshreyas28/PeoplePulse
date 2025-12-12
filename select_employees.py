"""Interactive employee selection and prediction tool"""
import sys
sys.path.insert(0, r'e:\PeoplePulse\ml\pipeline')

import joblib
import pandas as pd

print("=" * 70)
print("PEOPLEPULSE - INTERACTIVE EMPLOYEE ATTRITION PREDICTION")
print("=" * 70)

# Load the dataset
print("\nLoading dataset...")
df = pd.read_csv(r'e:\PeoplePulse\data\raw\WA_Fn-UseC_-HR-Employee-Attrition.csv')
print(f"✓ Loaded {len(df):,} employees")

# Load the model
print("Loading model...")
model_path = r'e:\PeoplePulse\ml\models\model.pkl'
artifacts = joblib.load(model_path)
model = artifacts['model']
preprocessor = artifacts['preprocessor']
print("✓ Model loaded successfully!")

def predict_employee(employee_data, emp_id):
    """Make prediction for an employee"""
    try:
        # Create DataFrame
        df_pred = pd.DataFrame([employee_data])
        
        # Preprocess
        X, _ = preprocessor.prepare_data(df_pred, fit=False)
        
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
        
        return attrition_prob, risk, color
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None, None, None

def show_employee_details(emp):
    """Display employee details"""
    print("\n" + "=" * 70)
    print(f"EMPLOYEE #{emp.get('EmployeeNumber', 'N/A')}")
    print("=" * 70)
    print(f"👤 Personal:")
    print(f"   Age: {emp['Age']} years")
    print(f"   Gender: {emp['Gender']}")
    print(f"   Marital Status: {emp['MaritalStatus']}")
    print(f"   Distance from Home: {emp['DistanceFromHome']} miles")
    
    print(f"\n💼 Job Information:")
    print(f"   Department: {emp['Department']}")
    print(f"   Job Role: {emp['JobRole']}")
    print(f"   Job Level: {emp['JobLevel']}")
    print(f"   Business Travel: {emp['BusinessTravel']}")
    print(f"   Overtime: {emp['OverTime']}")
    
    print(f"\n📚 Education:")
    print(f"   Education Level: {emp['Education']} (1=Below College, 2=College, 3=Bachelor, 4=Master, 5=Doctor)")
    print(f"   Education Field: {emp['EducationField']}")
    
    print(f"\n⏱️ Tenure:")
    print(f"   Years at Company: {emp['YearsAtCompany']}")
    print(f"   Years in Current Role: {emp['YearsInCurrentRole']}")
    print(f"   Years Since Last Promotion: {emp['YearsSinceLastPromotion']}")
    print(f"   Years with Current Manager: {emp['YearsWithCurrManager']}")
    print(f"   Total Working Years: {emp['TotalWorkingYears']}")
    print(f"   Number of Companies Worked: {emp['NumCompaniesWorked']}")
    
    print(f"\n💰 Compensation:")
    print(f"   Monthly Income: ${emp['MonthlyIncome']:,}")
    print(f"   Hourly Rate: ${emp['HourlyRate']}")
    print(f"   Percent Salary Hike: {emp['PercentSalaryHike']}%")
    print(f"   Stock Option Level: {emp['StockOptionLevel']}")
    
    print(f"\n😊 Satisfaction (1-4):")
    print(f"   Job Satisfaction: {emp['JobSatisfaction']}/4")
    print(f"   Environment Satisfaction: {emp['EnvironmentSatisfaction']}/4")
    print(f"   Relationship Satisfaction: {emp['RelationshipSatisfaction']}/4")
    print(f"   Work Life Balance: {emp['WorkLifeBalance']}/4")
    
    print(f"\n📊 Performance:")
    print(f"   Performance Rating: {emp['PerformanceRating']}")
    print(f"   Job Involvement: {emp['JobInvolvement']}")
    print(f"   Training Times Last Year: {emp['TrainingTimesLastYear']}")

# Main menu
while True:
    print("\n" + "=" * 70)
    print("SELECTION OPTIONS")
    print("=" * 70)
    print("1. Search by Employee Number")
    print("2. Filter by Department")
    print("3. Filter by Job Role")
    print("4. Filter by Risk (predict all and filter)")
    print("5. Random Sample (10 employees)")
    print("6. Predict Specific Employee Number(s)")
    print("7. Exit")
    print("=" * 70)
    
    choice = input("\nEnter your choice (1-7): ").strip()
    
    if choice == '1':
        emp_num = input("Enter Employee Number: ").strip()
        try:
            emp_num = int(emp_num)
            emp = df[df['EmployeeNumber'] == emp_num]
            if len(emp) == 0:
                print(f"❌ Employee #{emp_num} not found!")
                continue
            emp = emp.iloc[0].to_dict()
            show_employee_details(emp)
            
            prob, risk, color = predict_employee(emp, emp_num)
            if prob is not None:
                print(f"\n{color} PREDICTION:")
                print(f"   Attrition Probability: {prob*100:.2f}%")
                print(f"   Risk Level: {risk}")
        except ValueError:
            print("❌ Invalid employee number!")
    
    elif choice == '2':
        print("\nDepartments:")
        for i, dept in enumerate(df['Department'].unique(), 1):
            count = len(df[df['Department'] == dept])
            print(f"  {i}. {dept} ({count} employees)")
        
        dept_choice = input("\nEnter department number: ").strip()
        try:
            dept = df['Department'].unique()[int(dept_choice) - 1]
            dept_df = df[df['Department'] == dept]
            print(f"\n{len(dept_df)} employees in {dept}")
            
            num = input(f"How many to predict? (1-{min(50, len(dept_df))}): ").strip()
            num = min(int(num), len(dept_df))
            
            print(f"\nPredicting {num} employees from {dept}...\n")
            for idx, (_, emp) in enumerate(dept_df.head(num).iterrows(), 1):
                emp_dict = emp.to_dict()
                prob, risk, color = predict_employee(emp_dict, emp['EmployeeNumber'])
                if prob is not None:
                    print(f"{idx:2d}. {color} #{emp['EmployeeNumber']:4d} | {emp['JobRole']:30s} | {prob*100:5.2f}% | {risk}")
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
    
    elif choice == '3':
        print("\nJob Roles:")
        roles = df['JobRole'].value_counts()
        for i, (role, count) in enumerate(roles.items(), 1):
            print(f"  {i:2d}. {role} ({count})")
        
        role_choice = input("\nEnter role number: ").strip()
        try:
            role = list(roles.index)[int(role_choice) - 1]
            role_df = df[df['JobRole'] == role]
            print(f"\n{len(role_df)} employees as {role}")
            
            num = input(f"How many to predict? (1-{min(50, len(role_df))}): ").strip()
            num = min(int(num), len(role_df))
            
            print(f"\nPredicting {num} {role}s...\n")
            for idx, (_, emp) in enumerate(role_df.head(num).iterrows(), 1):
                emp_dict = emp.to_dict()
                prob, risk, color = predict_employee(emp_dict, emp['EmployeeNumber'])
                if prob is not None:
                    print(f"{idx:2d}. {color} #{emp['EmployeeNumber']:4d} | Age:{emp['Age']:2d} | YrsCompany:{emp['YearsAtCompany']:2d} | {prob*100:5.2f}% | {risk}")
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
    
    elif choice == '4':
        print("\nThis will predict ALL employees and show by risk level...")
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm == 'y':
            print(f"\nPredicting {len(df)} employees...")
            results = []
            for idx, (_, emp) in enumerate(df.iterrows(), 1):
                emp_dict = emp.to_dict()
                prob, risk, color = predict_employee(emp_dict, emp['EmployeeNumber'])
                if prob is not None:
                    results.append({
                        'emp_num': emp['EmployeeNumber'],
                        'name': f"{emp['JobRole']}-{emp['Department'][:3]}",
                        'prob': prob,
                        'risk': risk,
                        'color': color
                    })
                if idx % 100 == 0:
                    print(f"  Processed {idx}/{len(df)}...")
            
            # Sort by probability
            results.sort(key=lambda x: x['prob'], reverse=True)
            
            print("\n" + "=" * 70)
            print("TOP 20 HIGHEST RISK EMPLOYEES:")
            print("=" * 70)
            for i, r in enumerate(results[:20], 1):
                print(f"{i:2d}. {r['color']} #{r['emp_num']:4d} | {r['name']:40s} | {r['prob']*100:5.2f}%")
            
            print("\n" + "=" * 70)
            print("BOTTOM 20 LOWEST RISK EMPLOYEES:")
            print("=" * 70)
            for i, r in enumerate(results[-20:], 1):
                print(f"{i:2d}. {r['color']} #{r['emp_num']:4d} | {r['name']:40s} | {r['prob']*100:5.2f}%")
    
    elif choice == '5':
        print("\nSelecting 10 random employees...")
        sample = df.sample(10)
        print("\n")
        for idx, (_, emp) in enumerate(sample.iterrows(), 1):
            emp_dict = emp.to_dict()
            prob, risk, color = predict_employee(emp_dict, emp['EmployeeNumber'])
            if prob is not None:
                print(f"{idx:2d}. {color} #{emp['EmployeeNumber']:4d} | {emp['JobRole']:30s} | {prob*100:5.2f}% | {risk}")
    
    elif choice == '6':
        emp_nums = input("Enter Employee Number(s) (comma-separated): ").strip()
        try:
            emp_list = [int(x.strip()) for x in emp_nums.split(',')]
            print("\n")
            for emp_num in emp_list:
                emp = df[df['EmployeeNumber'] == emp_num]
                if len(emp) == 0:
                    print(f"❌ Employee #{emp_num} not found!")
                    continue
                emp = emp.iloc[0].to_dict()
                prob, risk, color = predict_employee(emp, emp_num)
                if prob is not None:
                    print(f"{color} #{emp_num:4d} | {emp['JobRole']:30s} | {prob*100:5.2f}% | {risk}")
        except ValueError:
            print("❌ Invalid input!")
    
    elif choice == '7':
        print("\n👋 Goodbye!")
        break
    
    else:
        print("❌ Invalid choice!")
    
    input("\nPress Enter to continue...")
