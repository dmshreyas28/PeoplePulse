"""
PeoplePulse - Employee Attrition Prediction Dashboard
Streamlit Frontend
"""
import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DATASET_PATH = Path(os.getenv("DATASET_PATH", "data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv"))

# Page config
st.set_page_config(
    page_title="PeoplePulse - Attrition Analytics",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background-color: #f5f7fa;
    }

    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        letter-spacing: -0.5px;
    }

    .sub-header {
        text-align: center;
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* Card styling */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }

    /* Button styling */
    .stButton>button {
        width: 100%;
        background: #1e40af;
        color: white;
        font-weight: 500;
        padding: 0.65rem 1.5rem;
        border-radius: 6px;
        border: none;
        transition: background 0.2s ease;
    }

    .stButton>button:hover {
        background: #1d4ed8;
    }

    /* Section headers */
    .section-header {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1e293b;
        border-left: 3px solid #1e40af;
        padding-left: 0.75rem;
        margin: 1.5rem 0 1rem 0;
        letter-spacing: -0.3px;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff;
    }

    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 600;
    }

    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
    }

    /* Table styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        font-weight: 500;
    }

    /* Info/Success/Warning/Error boxes */
    .stAlert {
        border-radius: 6px;
    }

    /* Slider styling */
    .stSlider label {
        color: #374151;
    }

    /* Input styling */
    .stTextInput input, .stSelectbox select {
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }

    /* Divider */
    hr {
        border-color: #e5e7eb;
        margin: 1.5rem 0;
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
    colors = ['#dc2626' if v > 0 else '#16a34a' for v in values]

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
        title=dict(text="Feature Impact Analysis (SHAP Values)", font=dict(size=16, color="#1e293b")),
        xaxis_title="SHAP Impact",
        yaxis_title="Features",
        height=500,
        showlegend=False,
        font=dict(family="Inter, Arial, sans-serif", size=12, color="#374151"),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff'
    )

    fig.update_xaxes(gridcolor='#f1f5f9', zerolinecolor='#94a3b8')
    fig.update_yaxes(gridcolor='#f1f5f9')

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Red bars:** Increase attrition risk")
    with col2:
        st.markdown("**Green bars:** Decrease attrition risk")

def get_risk_label(risk_level: str) -> str:
    """Return formatted risk label"""
    labels = {
        "High": "[HIGH]",
        "Medium": "[MEDIUM]",
        "Low": "[LOW]"
    }
    return labels.get(risk_level, risk_level)

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">PeoplePulse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Employee Attrition Analytics Platform</p>', unsafe_allow_html=True)

    # Check backend health
    health = check_backend_health()

    if health.get("status") == "healthy":
        if health.get("model_loaded"):
            st.success("System Status: Online | ML Model: Loaded")
        else:
            st.warning("System Status: Online | ML Model: Not Loaded")
    else:
        st.error(f"System Status: Offline - {health.get('message', 'Unknown error')}")
        st.stop()

    st.markdown("---")

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Select Page", ["Dashboard", "Employee Search"])

    st.sidebar.markdown("---")
    st.sidebar.markdown("**System Information**")
    st.sidebar.markdown("- Model: XGBoost")
    st.sidebar.markdown("- Accuracy: 87%")
    st.sidebar.markdown("- Dataset: 1,470 records")

    if page == "Dashboard":
        show_dashboard()
    else:
        show_employee_search()

def show_dashboard():
    """Dashboard page with batch predictions"""
    st.markdown('<div class="section-header">Attrition Risk Dashboard</div>', unsafe_allow_html=True)

    # Load employees
    all_employees = get_all_employees()

    if not all_employees:
        st.error("Unable to load employee data from CSV file")
        return

    st.markdown(f"""
    **Analysis Overview:**
    - Available records: {len(all_employees)} employees
    - Model: XGBoost with 87% accuracy
    - Features analyzed: 35+ employee attributes
    """)

    # Let user select how many employees to analyze
    num_to_analyze = st.slider("Number of employees to analyze", min_value=5, max_value=50, value=20, step=5)

    if st.button("Run Attrition Analysis", type="primary"):
        with st.spinner(f"Analyzing {num_to_analyze} employees..."):
            # Take first N employees for batch prediction
            employees_to_predict = all_employees[:num_to_analyze]
            result = predict_batch(employees_to_predict)

            if result and result.get("predictions"):
                predictions = result["predictions"]

                # Store in session state
                st.session_state["predictions"] = predictions
                st.success(f"Analysis complete: {len(predictions)} employees processed")

    # Display results if available
    if "predictions" in st.session_state:
        predictions = st.session_state["predictions"]

        # KPI Metrics
        st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)

        total = len(predictions)
        high_risk = sum(1 for p in predictions if p["risk_level"] == "High")
        medium_risk = sum(1 for p in predictions if p["risk_level"] == "Medium")
        low_risk = total - high_risk - medium_risk
        avg_prob = sum(p["attrition_probability"] for p in predictions) / total * 100
        avg_conf = sum(p["confidence"] for p in predictions) / total * 100

        with col1:
            st.metric("Total Employees", total)
        with col2:
            st.metric("High Risk", high_risk, delta=f"{high_risk/total*100:.1f}%")
        with col3:
            st.metric("Medium Risk", medium_risk, delta=f"{medium_risk/total*100:.1f}%")
        with col4:
            st.metric("Avg. Risk Score", f"{avg_prob:.1f}%")
        with col5:
            st.metric("Model Confidence", f"{avg_conf:.1f}%")

        st.markdown("---")

        # Results Table
        st.markdown('<div class="section-header">Prediction Results</div>', unsafe_allow_html=True)

        # Prepare data for table
        table_data = []
        for pred in predictions:
            risk_label = get_risk_label(pred["risk_level"])
            table_data.append({
                "Employee ID": pred["employee_id"],
                "Risk Level": risk_label,
                "Probability": f"{pred['attrition_probability']*100:.1f}%",
                "Confidence": f"{pred['confidence']*100:.1f}%",
                "Primary Factor": pred["top_factors"][0] if pred["top_factors"] else "N/A",
                "Recommendation": pred["recommendation"]
            })

        df = pd.DataFrame(table_data)

        # Color code by risk
        def highlight_risk(row):
            if "HIGH" in row["Risk Level"]:
                return ['background-color: #fef2f2; color: #991b1b'] * len(row)
            elif "MEDIUM" in row["Risk Level"]:
                return ['background-color: #fffbeb; color: #92400e'] * len(row)
            else:
                return ['background-color: #f0fdf4; color: #166534'] * len(row)

        st.dataframe(df.style.apply(highlight_risk, axis=1), use_container_width=True, height=400)

        # Risk Distribution Chart
        st.markdown('<div class="section-header">Risk Distribution</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            risk_counts = pd.DataFrame([
                {"Risk Level": "High", "Count": high_risk},
                {"Risk Level": "Medium", "Count": medium_risk},
                {"Risk Level": "Low", "Count": low_risk}
            ])

            fig = px.pie(risk_counts, values='Count', names='Risk Level',
                         color='Risk Level',
                         color_discrete_map={'High': '#dc2626', 'Medium': '#f59e0b', 'Low': '#16a34a'})
            fig.update_layout(
                font=dict(family="Inter, Arial, sans-serif", size=12, color="#374151"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig_bar = px.bar(risk_counts, x='Risk Level', y='Count',
                            color='Risk Level',
                            color_discrete_map={'High': '#dc2626', 'Medium': '#f59e0b', 'Low': '#16a34a'})
            fig_bar.update_layout(
                font=dict(family="Inter, Arial, sans-serif", size=12, color="#374151"),
                showlegend=False,
                plot_bgcolor='#ffffff',
                paper_bgcolor='#ffffff'
            )
            fig_bar.update_xaxes(gridcolor='#f1f5f9')
            fig_bar.update_yaxes(gridcolor='#f1f5f9')
            st.plotly_chart(fig_bar, use_container_width=True)

def show_employee_search():
    """Employee search page"""
    st.markdown('<div class="section-header">Employee Search</div>', unsafe_allow_html=True)

    # Load all employees
    all_employees = get_all_employees()

    if not all_employees:
        st.error("Unable to load employee data from CSV file")
        return

    st.markdown(f"Search through **{len(all_employees)} employees** for individual attrition risk analysis.")

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

    if st.button("Search", type="primary"):
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
            st.success(f"Found {len(filtered)} employee(s) - displaying first 20 results")
        else:
            st.warning("No employees found. Please adjust your search criteria.")

    # Display search results
    if "search_results" in st.session_state:
        st.markdown("---")
        st.markdown('<div class="section-header">Search Results</div>', unsafe_allow_html=True)

        for emp in st.session_state["search_results"]:
            with st.expander(f"{emp['employee_id']} | {emp['job_role']} | {emp['department']}", expanded=False):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Personal Information**")
                    st.write(f"Age: {emp['age']}")
                    st.write(f"Gender: {emp['gender']}")
                    st.write(f"Marital Status: {emp['marital_status']}")

                with col2:
                    st.markdown("**Employment Details**")
                    st.write(f"Department: {emp['department']}")
                    st.write(f"Role: {emp['job_role']}")
                    st.write(f"Tenure: {emp['years_at_company']} years")
                    st.write(f"Monthly Income: ${emp['monthly_income']:,}")
                    st.write(f"Overtime: {emp['overtime']}")

                with col3:
                    st.markdown("**Performance Metrics**")
                    st.write(f"Job Satisfaction: {emp['job_satisfaction']}/4")
                    st.write(f"Work-Life Balance: {emp['work_life_balance']}/4")
                    st.write(f"Performance Rating: {emp['performance_rating']}/4")
                    st.write(f"Environment Satisfaction: {emp['environment_satisfaction']}/4")

                st.markdown("---")

                if st.button(f"Analyze Risk - {emp['employee_id']}", key=emp['employee_id']):
                    with st.spinner("Running prediction model..."):
                        prediction = predict_single(emp)

                        if prediction:
                            # Risk metrics
                            risk_col1, risk_col2, risk_col3 = st.columns(3)

                            risk_color = {"High": "red", "Medium": "orange", "Low": "green"}.get(prediction["risk_level"], "gray")

                            with risk_col1:
                                st.metric("Attrition Probability",
                                         f"{prediction['attrition_probability']*100:.1f}%")

                            with risk_col2:
                                st.markdown(f"**Risk Level:** :{risk_color}[{prediction['risk_level'].upper()}]")

                            with risk_col3:
                                st.metric("Model Confidence",
                                         f"{prediction['confidence']*100:.1f}%")

                            # Recommendation
                            st.info(f"**Recommendation:** {prediction['recommendation']}")

                            # Top factors
                            st.markdown("**Key Risk Factors:**")
                            for i, factor in enumerate(prediction['top_factors'][:5], 1):
                                st.write(f"{i}. {factor}")

                            # SHAP chart
                            if prediction.get("shap_values"):
                                st.markdown("---")
                                display_shap_chart(prediction["shap_values"])

if __name__ == "__main__":
    main()
