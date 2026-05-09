# PeoplePulse

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

**AI-Powered Employee Attrition Prediction and Retention Platform**

Predict employee turnover risk, understand the contributing factors, and take targeted action to retain talent.

---

## Overview

PeoplePulse is a full-stack AI platform for HR teams to proactively manage employee retention. Using machine learning and explainable AI, it identifies employees at risk of leaving and surfaces actionable insights to prevent attrition before it occurs.

**The problem:** Employee turnover costs organizations 50–200% of an employee's annual salary. Traditional HR analytics rarely identify at-risk employees in time to intervene.

**The solution:** PeoplePulse trains on real HR data to predict attrition risk, explain the drivers behind each prediction, recommend tailored retention strategies, and simulate the impact of interventions before they are implemented.

---

## Features

### Machine Learning Predictions

- XGBoost and LightGBM models for high-accuracy attrition predictions
- Analysis across 35 employee features: demographics, satisfaction scores, compensation, tenure, and more
- Automatic risk classification into Low, Medium, and High tiers
- Batch processing across an entire workforce in seconds

### Explainable AI

- SHAP values to quantify each feature's contribution to a prediction
- Global feature importance across the organization
- Per-employee breakdowns of risk drivers
- Interactive charts accessible to non-technical stakeholders

### Actionable Insights

- AI-generated retention recommendations tailored to individual employees
- Intervention simulation to model changes before implementation
- Priority ranking to focus on the highest-risk employees first
- Trend tracking over time

### Interactive Dashboard

- Live workforce attrition metrics
- Risk distribution across Low, Medium, and High tiers
- Department-level comparison
- Employee search across 1,470 records

### Architecture

- RESTful API for integration with existing HR systems
- Docker support for containerized deployment
- SQLite (development) and PostgreSQL (production) database support
- Scalable design for thousands of employees

---

## Architecture

```
                         PeoplePulse Architecture

   +-----------------------+         +-----------------------+
   |                       |  HTTP   |                       |
   |    Streamlit UI        |<------->|   FastAPI Backend     |
   |    (Port 8501)         |  JSON   |   (Port 8000)        |
   |                       |         |                       |
   |  - Dashboard           |         |  - REST API          |
   |  - Employee Search     |         |  - Predictions       |
   |  - SHAP Charts         |         |  - SHAP Service      |
   |                       |         |  - Data Management   |
   +-----------------------+         +----------+------------+
                                                |
                              +-----------------+-----------------+
                              |                 |                 |
                         +----+-----+    +------+----+    +-------+----+
                         |          |    |           |    |            |
                         |  SQLite  |    |  XGBoost  |    |    SHAP    |
                         | Database |    |   Model   |    |  Explainer |
                         |          |    |           |    |            |
                         +----------+    +-----------+    +------------+

                              +---------------------------+
                              |       CSV Dataset         |
                              |     (1,470 Records)       |
                              +---------------------------+
```

---

## Tech Stack

### Backend

| Technology | Version | Purpose |
|---|---|---|
| FastAPI | 0.109+ | Async REST API framework |
| Uvicorn | 0.27+ | ASGI server |
| SQLAlchemy | 2.0+ | ORM for database operations |
| Pydantic | 2.5+ | Data validation and serialization |
| SQLite / PostgreSQL | — | Local and production databases |

### Machine Learning

| Technology | Version | Purpose |
|---|---|---|
| XGBoost | 2.0+ | Gradient boosting for predictions |
| LightGBM | 4.3+ | Alternative gradient boosting model |
| scikit-learn | 1.4.0 | ML utilities and preprocessing |
| SHAP | 0.44+ | Explainability and feature importance |
| imbalanced-learn | 0.12+ | Class imbalance handling |
| Pandas | 2.1+ | Data manipulation |
| NumPy | 1.26+ | Numerical computing |

### Frontend

| Technology | Version | Purpose |
|---|---|---|
| Streamlit | 1.52+ | Interactive web dashboard |
| Plotly | 5.0+ | Interactive visualizations |

### DevOps (Optional)

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| MLflow | Experiment tracking |

---

## Quick Start

### Prerequisites

- Python 3.10 or later
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/peoplepulse.git
cd peoplepulse
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy python-dotenv \
  python-multipart joblib xgboost scikit-learn==1.4.0 shap imbalanced-learn \
  streamlit plotly requests pandas numpy
```

### Step 4: Start the Application

**Option A — Windows batch script:**

```bash
start.bat
```

**Option B — Manual startup:**

Terminal 1 (Backend):

```bash
# Windows
set DATABASE_URL=sqlite:///./test.db
set MODEL_PATH=ml\models\model.pkl
set PYTHONPATH=backend;ml\pipeline
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# Linux / macOS
export DATABASE_URL=sqlite:///./test.db
export MODEL_PATH=ml/models/model.pkl
export PYTHONPATH=backend:ml/pipeline
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):

```bash
streamlit run streamlit_app.py --server.port 8501
```

### Step 5: Access the Platform

| Service | URL |
|---|---|
| Dashboard | http://localhost:8501 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## Project Structure

```
peoplepulse/
|
+-- backend/                    # FastAPI backend
|   +-- app/
|   |   +-- main.py             # Application entry point
|   |   +-- config.py           # Configuration settings
|   |   +-- db.py               # Database connection
|   |   +-- routers/
|   |   |   +-- predict.py      # Prediction endpoints
|   |   |   +-- employees.py    # Employee CRUD
|   |   |   +-- simulate.py     # Intervention simulation
|   |   +-- models/
|   |   |   +-- employee.py     # Employee ORM model
|   |   |   +-- prediction.py   # Prediction ORM model
|   |   +-- schemas/
|   |   |   +-- employee_schema.py
|   |   |   +-- predict_schema.py
|   |   +-- services/
|   |       +-- model_service.py    # ML model operations
|   |       +-- shap_service.py     # SHAP explanations
|   |       +-- feature_service.py  # Feature engineering
|   +-- Dockerfile
|   +-- requirements.txt
|
+-- ml/                         # Machine learning pipeline
|   +-- pipeline/
|   |   +-- train.py            # Model training
|   |   +-- preprocess.py       # Data preprocessing
|   |   +-- evaluate.py         # Model evaluation
|   |   +-- explain.py          # SHAP analysis
|   |   +-- config.yaml         # ML configuration
|   +-- models/
|   |   +-- model.pkl           # Trained XGBoost model
|   |   +-- metrics.json        # Performance metrics
|   +-- notebooks/              # Jupyter notebooks for EDA
|   +-- requirements.txt
|
+-- data/
|   +-- raw/
|   |   +-- WA_Fn-UseC_-HR-Employee-Attrition.csv
|   +-- processed/
|
+-- infra/                      # Infrastructure (optional)
|   +-- docker-compose.yml
|   +-- postgres-init.sql
|   +-- start.sh
|   +-- start.ps1
|
+-- streamlit_app.py            # Streamlit frontend
+-- start.bat                   # Windows startup script
+-- requirements-streamlit.txt
+-- .gitignore
+-- LICENSE
+-- README.md
```

---

## API Reference

### Health Check

```http
GET /health
```

Returns backend status and model availability.

```json
{
  "status": "healthy",
  "model_loaded": true,
  "database": "connected"
}
```

---

### Predict Single Employee

```http
POST /api/predict/employee
```

Predicts attrition risk for one employee.

**Request body:**

```json
{
  "employee_id": "EMP001",
  "age": 35,
  "gender": "Male",
  "department": "Sales",
  "job_role": "Sales Executive",
  "education": 3,
  "education_field": "Marketing",
  "years_at_company": 5,
  "years_in_current_role": 3,
  "years_since_last_promotion": 1,
  "years_with_curr_manager": 2,
  "num_companies_worked": 3,
  "monthly_income": 6500,
  "percent_salary_hike": 15,
  "stock_option_level": 1,
  "training_times_last_year": 2,
  "job_satisfaction": 3,
  "work_life_balance": 3,
  "environment_satisfaction": 3,
  "relationship_satisfaction": 4,
  "performance_rating": 3,
  "business_travel": "Travel_Rarely",
  "distance_from_home": 10,
  "marital_status": "Married",
  "overtime": "No",
  "daily_rate": 800,
  "hourly_rate": 65,
  "monthly_rate": 15000,
  "job_level": 2,
  "job_involvement": 3,
  "total_working_years": 10
}
```

**Response:**

```json
{
  "employee_id": "EMP001",
  "attrition_probability": 0.23,
  "risk_level": "Low",
  "top_factors": [
    {"feature": "overtime", "value": "No", "impact": -0.15},
    {"feature": "job_satisfaction", "value": 3, "impact": -0.08},
    {"feature": "years_at_company", "value": 5, "impact": -0.05}
  ],
  "recommendation": "This employee has low attrition risk. Continue current engagement strategies."
}
```

---

### Batch Prediction

```http
POST /api/predict/batch
```

Predicts attrition risk for multiple employees.

**Response:**

```json
{
  "predictions": [
    {
      "employee_id": "EMP001",
      "attrition_probability": 0.23,
      "risk_level": "Low"
    },
    {
      "employee_id": "EMP002",
      "attrition_probability": 0.67,
      "risk_level": "High"
    }
  ],
  "summary": {
    "total": 2,
    "high_risk": 1,
    "medium_risk": 0,
    "low_risk": 1,
    "average_probability": 0.45
  }
}
```

---

### Simulate Intervention

```http
POST /api/simulate/intervention
```

Models the impact of a proposed retention intervention.

**Request body:**

```json
{
  "employee_id": "EMP001",
  "interventions": {
    "monthly_income": 7500,
    "job_satisfaction": 4,
    "overtime": "No"
  }
}
```

**Response:**

```json
{
  "original_probability": 0.67,
  "new_probability": 0.31,
  "risk_reduction": 0.36,
  "recommendation": "The proposed interventions would significantly reduce attrition risk."
}
```

---

## Dataset

PeoplePulse uses the IBM HR Analytics Employee Attrition dataset.

| Field | Description | Type |
|---|---|---|
| Age | Employee age | Integer |
| Department | Work department (Sales, R&D, HR) | Categorical |
| JobRole | Job position | Categorical |
| MonthlyIncome | Monthly salary | Integer |
| OverTime | Works overtime | Yes / No |
| YearsAtCompany | Tenure at company | Integer |
| JobSatisfaction | Satisfaction rating (1–4) | Integer |
| WorkLifeBalance | Balance rating (1–4) | Integer |
| EnvironmentSatisfaction | Environment rating (1–4) | Integer |
| NumCompaniesWorked | Previous employers | Integer |

**Dataset statistics:**

- Total employees: 1,470
- Attrition rate: ~16%
- Features per employee: 35
- Source: IBM HR Analytics

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | Database connection string | `sqlite:///./test.db` |
| `MODEL_PATH` | Path to trained ML model | `ml/models/model.pkl` |
| `PYTHONPATH` | Python module paths | `backend;ml/pipeline` |
| `DEBUG` | Enable debug mode | `False` |

### ML Pipeline (`ml/pipeline/config.yaml`)

```yaml
data:
  raw_path: "../data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv"
  target_column: "Attrition"

model:
  algorithm: "xgboost"  # Options: xgboost, lightgbm, random_forest
  hyperparameters:
    n_estimators: 100
    max_depth: 6
    learning_rate: 0.1

preprocessing:
  handle_imbalance: true
  method: "SMOTE"
```

---

## Model Performance

| Metric | Value |
|---|---|
| Accuracy | 89% |
| Precision | 85% |
| Recall | 78% |
| F1-Score | 81% |
| AUC-ROC | 0.87 |

---

## Security and Privacy

- Never commit real employee data to version control
- Use environment variables for sensitive configuration
- Implement authentication before production deployment
- Follow GDPR and CCPA requirements for employee data
- Anonymize data prior to model training

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- IBM HR Analytics Dataset — sample data source
- FastAPI — modern Python web framework
- Streamlit — rapid dashboard development
- XGBoost and SHAP — prediction and explainability
- scikit-learn — machine learning utilities
