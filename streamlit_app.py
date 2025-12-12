"""
PeoplePulse - Employee Attrition Prediction Dashboard
Streamlit Frontend
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
DATASET_PATH = Path("data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv")

# Page config
st.set_page_config(
    page_title="PeoplePulse - Attrition Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def load_employees_from_csv():
    """Load all employees from the dataset CSV file"""
    try:
        df = pd.read_csv(DATASET_PATH)
        employees = []
        
        for _, row in df.iterrows():
            emp = {
                "employee_id": f"EMP{int(row['EmployeeNumber']):04d}",
                "age": int(row['Age']),
                "gender": str(row['Gender']),
                "department": str(row['Department']),
                "job_role": str(row['JobRole']),
                "education": int(row['Education']),
                "education_field": str(row['EducationField']),
                "years_at_company": int(row['YearsAtCompany']),
                "years_in_current_role": int(row['YearsInCurrentRole']),
                "years_since_last_promotion": int(row['YearsSinceLastPromotion']),
                "years_with_curr_manager": int(row['YearsWithCurrManager']),
                "num_companies_worked": int(row['NumCompaniesWorked']),
                "monthly_income": int(row['MonthlyIncome']),
                "percent_salary_hike": int(row['PercentSalaryHike']),
                "stock_option_level": int(row['StockOptionLevel']),
                "training_times_last_year": int(row['TrainingTimesLastYear']),
                "job_satisfaction": int(row['JobSatisfaction']),
                "work_life_balance": int(row['WorkLifeBalance']),
                "environment_satisfaction": int(row['EnvironmentSatisfaction']),
                "relationship_satisfaction": int(row['RelationshipSatisfaction']),
                "performance_rating": int(row['PerformanceRating']),
                "business_travel": str(row['BusinessTravel']),
                "distance_from_home": int(row['DistanceFromHome']),
                "marital_status": str(row['MaritalStatus']),
                "overtime": str(row['OverTime']),
                "daily_rate": int(row['DailyRate']),
                "hourly_rate": int(row['HourlyRate']),
                "monthly_rate": int(row['MonthlyRate']),
                "job_level": int(row['JobLevel']),
                "job_involvement": int(row['JobInvolvement']),
                "total_working_years": int(row['TotalWorkingYears'])
            }
            employees.append(emp)
        
        return employees
    except Exception as e:
        st.error(f"Error loading employee data: {str(e)}")
        return []

# Load all employees from CSV
@st.cache_data
def get_all_employees():
    return load_employees_from_csv()

# Fallback sample data if CSV not found
SAMPLE_EMPLOYEES_FALLBACK = [
    {
        "employee_id": "EMP001", "age": 41, "gender": "Female", "department": "Sales",
        "job_role": "Sales Executive", "education": 2, "education_field": "Life Sciences",
        "years_at_company": 6, "years_in_current_role": 4, "years_since_last_promotion": 0,
        "years_with_curr_manager": 5, "num_companies_worked": 8, "monthly_income": 5993,
        "percent_salary_hike": 11, "stock_option_level": 0, "training_times_last_year": 0,
        "job_satisfaction": 4, "work_life_balance": 1, "environment_satisfaction": 2,
        "relationship_satisfaction": 1, "performance_rating": 3, "business_travel": "Travel_Rarely",
        "distance_from_home": 1, "marital_status": "Single", "overtime": "Yes",
        "daily_rate": 1102, "hourly_rate": 94, "monthly_rate": 19479,
        "job_level": 2, "job_involvement": 3, "total_working_years": 8
    },
    {
        "employee_id": "EMP002", "age": 49, "gender": "Male", "department": "Research & Development",
        "job_role": "Research Scientist", "education": 1, "education_field": "Life Sciences",
        "years_at_company": 10, "years_in_current_role": 7, "years_since_last_promotion": 1,
        "years_with_curr_manager": 7, "num_companies_worked": 1, "monthly_income": 5130,
        "percent_salary_hike": 23, "stock_option_level": 1, "training_times_last_year": 3,
        "job_satisfaction": 2, "work_life_balance": 3, "environment_satisfaction": 3,
        "relationship_satisfaction": 4, "performance_rating": 4, "business_travel": "Travel_Frequently",
        "distance_from_home": 8, "marital_status": "Married", "overtime": "No",
        "daily_rate": 279, "hourly_rate": 61, "monthly_rate": 24907,
        "job_level": 2, "job_involvement": 2, "total_working_years": 10
    },
    {
        "employee_id": "EMP003", "age": 37, "gender": "Male", "department": "Research & Development",
        "job_role": "Laboratory Technician", "education": 2, "education_field": "Other",
        "years_at_company": 0, "years_in_current_role": 0, "years_since_last_promotion": 0,
        "years_with_curr_manager": 0, "num_companies_worked": 6, "monthly_income": 2090,
        "percent_salary_hike": 15, "stock_option_level": 0, "training_times_last_year": 3,
        "job_satisfaction": 2, "work_life_balance": 3, "environment_satisfaction": 4,
        "relationship_satisfaction": 2, "performance_rating": 3, "business_travel": "Travel_Rarely",
        "distance_from_home": 2, "marital_status": "Single", "overtime": "Yes",
        "daily_rate": 1373, "hourly_rate": 56, "monthly_rate": 2396,
        "job_level": 1, "job_involvement": 2, "total_working_years": 7
    },
    {
        "employee_id": "EMP004", "age": 33, "gender": "Female", "department": "Research & Development",
        "job_role": "Research Scientist", "education": 4, "education_field": "Life Sciences",
        "years_at_company": 8, "years_in_current_role": 7, "years_since_last_promotion": 3,
        "years_with_curr_manager": 0, "num_companies_worked": 1, "monthly_income": 2909,
        "percent_salary_hike": 11, "stock_option_level": 0, "training_times_last_year": 3,
        "job_satisfaction": 3, "work_life_balance": 3, "environment_satisfaction": 4,
        "relationship_satisfaction": 3, "performance_rating": 3, "business_travel": "Travel_Frequently",
        "distance_from_home": 3, "marital_status": "Married", "overtime": "Yes",
        "daily_rate": 1392, "hourly_rate": 40, "monthly_rate": 23159,
        "job_level": 1, "job_involvement": 3, "total_working_years": 8
    },
    {
        "employee_id": "EMP005", "age": 27, "gender": "Male", "department": "Research & Development",
        "job_role": "Laboratory Technician", "education": 1, "education_field": "Medical",
        "years_at_company": 2, "years_in_current_role": 2, "years_since_last_promotion": 2,
        "years_with_curr_manager": 2, "num_companies_worked": 9, "monthly_income": 3468,
        "percent_salary_hike": 12, "stock_option_level": 1, "training_times_last_year": 3,
        "job_satisfaction": 2, "work_life_balance": 3, "environment_satisfaction": 1,
        "relationship_satisfaction": 4, "performance_rating": 4, "business_travel": "Travel_Rarely",
        "distance_from_home": 24, "marital_status": "Single", "overtime": "No",
        "daily_rate": 591, "hourly_rate": 79, "monthly_rate": 16632,
        "job_level": 1, "job_involvement": 3, "total_working_years": 6
    },
    {
        "employee_id": "EMP006", "age": 32, "gender": "Male", "department": "Research & Development",
        "job_role": "Laboratory Technician", "education": 2, "education_field": "Life Sciences",
        "years_at_company": 7, "years_in_current_role": 7, "years_since_last_promotion": 3,
        "years_with_curr_manager": 6, "num_companies_worked": 0, "monthly_income": 2571,
        "percent_salary_hike": 13, "stock_option_level": 0, "training_times_last_year": 3,
        "job_satisfaction": 4, "work_life_balance": 3, "environment_satisfaction": 2,
        "relationship_satisfaction": 3, "performance_rating": 3, "business_travel": "Travel_Rarely",
        "distance_from_home": 15, "marital_status": "Divorced", "overtime": "No",
        "daily_rate": 1005, "hourly_rate": 81, "monthly_rate": 17357,
        "job_level": 1, "job_involvement": 2, "total_working_years": 7
    },
    {
        "employee_id": "EMP007", "age": 59, "gender": "Female", "department": "Research & Development",
        "job_role": "Laboratory Technician", "education": 3, "education_field": "Medical",
        "years_at_company": 1, "years_in_current_role": 0, "years_since_last_promotion": 0,
        "years_with_curr_manager": 0, "num_companies_worked": 4, "monthly_income": 2083,
        "percent_salary_hike": 11, "stock_option_level": 0, "training_times_last_year": 2,
        "job_satisfaction": 3, "work_life_balance": 4, "environment_satisfaction": 3,
        "relationship_satisfaction": 1, "performance_rating": 3, "business_travel": "Travel_Rarely",
        "distance_from_home": 26, "marital_status": "Married", "overtime": "Yes",
        "daily_rate": 1324, "hourly_rate": 44, "monthly_rate": 26999,
        "job_level": 1, "job_involvement": 1, "total_working_years": 12
    },
    {
        "employee_id": "EMP008", "age": 30, "gender": "Male", "department": "Research & Development",
        "job_role": "Laboratory Technician", "education": 1, "education_field": "Life Sciences",
        "years_at_company": 1, "years_in_current_role": 0, "years_since_last_promotion": 0,
        "years_with_curr_manager": 0, "num_companies_worked": 1, "monthly_income": 2028,
        "percent_salary_hike": 22, "stock_option_level": 1, "training_times_last_year": 6,
        "job_satisfaction": 4, "work_life_balance": 2, "environment_satisfaction": 2,
        "relationship_satisfaction": 2, "performance_rating": 4, "business_travel": "Travel_Rarely",
        "distance_from_home": 19, "marital_status": "Single", "overtime": "No",
        "daily_rate": 1551, "hourly_rate": 67, "monthly_rate": 17552,
        "job_level": 1, "job_involvement": 3, "total_working_years": 5
    }
]

def check_backend_health():
    """Check if backend is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def predict_batch(employees: List[Dict]):
    """Call batch prediction API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/predict/batch",
            json={"employees": employees},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def predict_single(employee: Dict):
    """Call single employee prediction API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/predict/employee",
            json=employee,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def display_shap_chart(shap_values: Dict):
    """Display SHAP values as horizontal bar chart"""
    if not shap_values:
        st.info("No SHAP data available")
        return
    
    # Convert to list and sort by absolute value
    items = [(k, float(v)) for k, v in shap_values.items()]
    items.sort(key=lambda x: abs(x[1]), reverse=True)
    items = items[:10]  # Top 10
    
    features = [item[0] for item in items]
    values = [item[1] for item in items]
    colors = ['red' if v > 0 else 'green' for v in values]
    
    fig = go.Figure(data=[
        go.Bar(
            y=features,
            x=values,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{v:.4f}" for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Feature Impact Analysis (SHAP Values)",
        xaxis_title="SHAP Impact",
        yaxis_title="Features",
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("🔴 Red bars increase attrition risk | 🟢 Green bars decrease attrition risk")

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">📊 PeoplePulse</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Employee Attrition Analytics</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check backend health
    health = check_backend_health()
    
    if health.get("status") == "healthy":
        if health.get("model_loaded"):
            st.success("✅ Backend Connected | Model Loaded")
        else:
            st.warning("⚠️ Backend Connected | Model NOT Loaded")
    else:
        st.error(f"❌ Backend Not Available: {health.get('message', 'Unknown error')}")
        st.stop()
    
    # Sidebar Navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio("Go to", ["📈 Dashboard", "🔍 Employee Search"])
    
    if page == "📈 Dashboard":
        show_dashboard()
    else:
        show_employee_search()

def show_dashboard():
    """Dashboard page with batch predictions"""
    st.header("📈 Employee Attrition Dashboard")
    
    # Load employees
    all_employees = get_all_employees()
    
    if not all_employees:
        st.error("Unable to load employee data from CSV file")
        return
    
    st.info(f"""
    **About this dashboard:**
    - Analyzes up to 50 employees from the dataset ({len(all_employees)} total available)
    - Trained on 1,470 IBM HR Analytics records
    - 87% accuracy with XGBoost algorithm
    - 35+ employee factors analyzed
    """)
    
    # Let user select how many employees to analyze
    num_to_analyze = st.slider("Number of employees to analyze", min_value=5, max_value=50, value=20, step=5)
    
    if st.button("🎯 Run Attrition Predictions", type="primary"):
        with st.spinner(f"Analyzing {num_to_analyze} employees with AI..."):
            # Take first N employees for batch prediction
            employees_to_predict = all_employees[:num_to_analyze]
            result = predict_batch(employees_to_predict)
            
            if result and result.get("predictions"):
                predictions = result["predictions"]
                
                # Store in session state
                st.session_state["predictions"] = predictions
                st.success(f"✅ Successfully analyzed {len(predictions)} employees!")
    
    # Display results if available
    if "predictions" in st.session_state:
        predictions = st.session_state["predictions"]
        
        # KPI Metrics
        st.subheader("📊 Key Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total = len(predictions)
        high_risk = sum(1 for p in predictions if p["risk_level"] == "High")
        medium_risk = sum(1 for p in predictions if p["risk_level"] == "Medium")
        avg_prob = sum(p["attrition_probability"] for p in predictions) / total * 100
        avg_conf = sum(p["confidence"] for p in predictions) / total * 100
        
        with col1:
            st.metric("👥 Total Employees", total)
        with col2:
            st.metric("⚠️ High Risk", high_risk, delta=f"{high_risk/total*100:.1f}%")
        with col3:
            st.metric("⚡ Medium Risk", medium_risk, delta=f"{medium_risk/total*100:.1f}%")
        with col4:
            st.metric("📊 Avg Risk", f"{avg_prob:.1f}%")
        with col5:
            st.metric("✨ Confidence", f"{avg_conf:.1f}%")
        
        st.markdown("---")
        
        # Results Table
        st.subheader("📋 Prediction Results")
        
        # Prepare data for table
        table_data = []
        for pred in predictions:
            risk_emoji = {"High": "⚠️", "Medium": "⚡", "Low": "✅"}.get(pred["risk_level"], "")
            table_data.append({
                "Employee ID": pred["employee_id"],
                "Risk": f"{risk_emoji} {pred['risk_level']}",
                "Probability": f"{pred['attrition_probability']*100:.1f}%",
                "Confidence": f"{pred['confidence']*100:.1f}%",
                "Top Factor": pred["top_factors"][0] if pred["top_factors"] else "N/A",
                "Recommendation": pred["recommendation"]
            })
        
        df = pd.DataFrame(table_data)
        
        # Color code by risk
        def highlight_risk(row):
            if "⚠️" in row["Risk"]:
                return ['background-color: #fee2e2'] * len(row)
            elif "⚡" in row["Risk"]:
                return ['background-color: #fef3c7'] * len(row)
            else:
                return ['background-color: #d1fae5'] * len(row)
        
        st.dataframe(df.style.apply(highlight_risk, axis=1), use_container_width=True, height=400)
        
        # Risk Distribution Chart
        st.subheader("📊 Risk Distribution")
        risk_counts = pd.DataFrame([
            {"Risk Level": "High", "Count": high_risk},
            {"Risk Level": "Medium", "Count": medium_risk},
            {"Risk Level": "Low", "Count": total - high_risk - medium_risk}
        ])
        
        fig = px.pie(risk_counts, values='Count', names='Risk Level', 
                     color='Risk Level',
                     color_discrete_map={'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'})
        st.plotly_chart(fig, use_container_width=True)

def show_employee_search():
    """Employee search page"""
    st.header("🔍 Employee Search")
    
    # Load all employees
    all_employees = get_all_employees()
    
    if not all_employees:
        st.error("Unable to load employee data from CSV file")
        return
    
    st.info(f"Search through **{len(all_employees)} employees** and get individual attrition risk predictions")
    
    # Get unique values for dropdowns
    departments = sorted(list(set(emp["department"] for emp in all_employees)))
    job_roles = sorted(list(set(emp["job_role"] for emp in all_employees)))
    
    # Search controls
    col1, col2 = st.columns([1, 2])
    
    with col1:
        search_type = st.selectbox("Search By", ["Employee ID", "Department", "Job Role", "Age Range"])
    
    with col2:
        if search_type == "Employee ID":
            search_value = st.text_input("Enter Employee ID", placeholder="e.g., EMP0001, EMP0100")
        elif search_type == "Department":
            search_value = st.selectbox("Select Department", [""] + departments)
        elif search_type == "Job Role":
            search_value = st.selectbox("Select Job Role", [""] + job_roles)
        else:  # Age Range
            age_range = st.slider("Select Age Range", 18, 65, (25, 45))
            search_value = age_range
    
    if st.button("🔍 Search", type="primary"):
        # Filter employees
        filtered = []
        
        if search_type == "Employee ID" and search_value:
            filtered = [emp for emp in all_employees if search_value.upper() in emp["employee_id"].upper()]
        elif search_type == "Department" and search_value:
            filtered = [emp for emp in all_employees if emp["department"] == search_value]
        elif search_type == "Job Role" and search_value:
            filtered = [emp for emp in all_employees if emp["job_role"] == search_value]
        elif search_type == "Age Range":
            filtered = [emp for emp in all_employees if age_range[0] <= emp["age"] <= age_range[1]]
        
        if filtered:
            # Limit to first 20 results for display
            filtered = filtered[:20]
            st.session_state["search_results"] = filtered
            st.success(f"Found {len(filtered)} employee(s) (showing first 20)")
        else:
            st.warning(f"No employees found. Try different search criteria.")
    
    # Display search results
    if "search_results" in st.session_state:
        st.markdown("---")
        st.subheader("Search Results")
        
        for emp in st.session_state["search_results"]:
            with st.expander(f"👤 {emp['employee_id']} - {emp['job_role']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Age:** {emp['age']}")
                    st.write(f"**Department:** {emp['department']}")
                    st.write(f"**Role:** {emp['job_role']}")
                
                with col2:
                    st.write(f"**Tenure:** {emp['years_at_company']} years")
                    st.write(f"**Income:** ${emp['monthly_income']:,}")
                    st.write(f"**Overtime:** {emp['overtime']}")
                
                with col3:
                    st.write(f"**Job Satisfaction:** {emp['job_satisfaction']}/4")
                    st.write(f"**Work-Life Balance:** {emp['work_life_balance']}/4")
                    st.write(f"**Performance:** {emp['performance_rating']}/4")
                
                if st.button(f"🎯 Predict Risk for {emp['employee_id']}", key=emp['employee_id']):
                    with st.spinner("Analyzing..."):
                        prediction = predict_single(emp)
                        
                        if prediction:
                            st.markdown("---")
                            
                            # Risk metrics
                            risk_col1, risk_col2, risk_col3 = st.columns(3)
                            
                            risk_emoji = {"High": "⚠️", "Medium": "⚡", "Low": "✅"}.get(prediction["risk_level"], "")
                            risk_color = {"High": "red", "Medium": "orange", "Low": "green"}.get(prediction["risk_level"], "gray")
                            
                            with risk_col1:
                                st.metric("Attrition Risk", 
                                         f"{prediction['attrition_probability']*100:.1f}%")
                            
                            with risk_col2:
                                st.markdown(f"**Risk Level:** :{risk_color}[{risk_emoji} {prediction['risk_level']}]")
                            
                            with risk_col3:
                                st.metric("Confidence", 
                                         f"{prediction['confidence']*100:.1f}%")
                            
                            # Recommendation
                            st.info(f"💡 **Recommendation:** {prediction['recommendation']}")
                            
                            # Top factors
                            st.write("**📊 Top Risk Factors:**")
                            for i, factor in enumerate(prediction['top_factors'][:5], 1):
                                st.write(f"{i}. {factor}")
                            
                            # SHAP chart
                            if prediction.get("shap_values"):
                                st.markdown("---")
                                display_shap_chart(prediction["shap_values"])

if __name__ == "__main__":
    main()
