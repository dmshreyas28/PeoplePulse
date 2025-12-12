import pandas as pd

df = pd.read_csv(r'e:\PeoplePulse\data\raw\WA_Fn-UseC_-HR-Employee-Attrition.csv')

print("=" * 60)
print("IBM HR ANALYTICS DATASET - SUMMARY")
print("=" * 60)

print(f"\n📊 Total Employees: {len(df):,}")
print(f"📋 Total Features: {len(df.columns)}")

print(f"\n🚪 ATTRITION BREAKDOWN:")
print(df['Attrition'].value_counts())
attrition_rate = (df["Attrition"] == "Yes").sum() / len(df) * 100
print(f"\n📈 Attrition Rate: {attrition_rate:.2f}%")
print(f"   - Left Company: {(df['Attrition'] == 'Yes').sum():,} employees")
print(f"   - Still Working: {(df['Attrition'] == 'No').sum():,} employees")

print(f"\n🏢 DEPARTMENTS:")
for dept, count in df['Department'].value_counts().items():
    pct = count / len(df) * 100
    print(f"   {dept}: {count:,} ({pct:.1f}%)")

print(f"\n💼 JOB ROLES (Top 10):")
for i, (role, count) in enumerate(df['JobRole'].value_counts().head(10).items(), 1):
    pct = count / len(df) * 100
    print(f"   {i:2d}. {role}: {count:,} ({pct:.1f}%)")

print(f"\n👥 DEMOGRAPHICS:")
print(f"   Gender: {df['Gender'].value_counts().to_dict()}")
print(f"   Age Range: {df['Age'].min()} - {df['Age'].max()} years")
print(f"   Avg Age: {df['Age'].mean():.1f} years")

print(f"\n💰 INCOME:")
print(f"   Min: ${df['MonthlyIncome'].min():,}")
print(f"   Max: ${df['MonthlyIncome'].max():,}")
print(f"   Avg: ${df['MonthlyIncome'].mean():,.2f}")

print(f"\n⏱️ TENURE:")
print(f"   Avg Years at Company: {df['YearsAtCompany'].mean():.1f}")
print(f"   Max Years at Company: {df['YearsAtCompany'].max()}")

print("\n" + "=" * 60)
