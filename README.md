# 🎯 PeoplePulse

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**🚀 AI-Powered Employee Attrition Prediction & Retention Platform**

*Predict employee turnover risk, understand the reasons behind it, and take action to retain your best talent.*

[Features](#-features) • [Quick Start](#-quick-start) • [Tech Stack](#️-tech-stack) • [API Reference](#-api-reference)

</div>

---

## 📖 About The Project

**PeoplePulse** is a production-grade, full-stack AI platform designed for HR teams and organizations to proactively manage employee retention. By leveraging machine learning and explainable AI, it predicts which employees are at risk of leaving and provides actionable insights to prevent attrition.

### 🎯 The Problem
Employee turnover is expensive—costing organizations 50-200% of an employee's annual salary. Traditional HR analytics often fail to identify at-risk employees before it's too late.

### 💡 The Solution
PeoplePulse uses advanced ML models trained on real HR data to:
- **Predict** attrition risk with high accuracy
- **Explain** why each employee might leave using SHAP
- **Recommend** targeted retention strategies
- **Simulate** the impact of interventions before implementing them

---

## ✨ Features

### 🤖 Machine Learning Predictions
- **XGBoost/LightGBM Models**: Industry-leading gradient boosting algorithms for accurate predictions
- **35 Employee Features**: Comprehensive analysis including demographics, job satisfaction, compensation, and more
- **Risk Classification**: Automatic categorization into Low/Medium/High risk tiers
- **Batch Processing**: Analyze your entire workforce in seconds

### 📊 Explainable AI (XAI)
- **SHAP Values**: Understand exactly which factors contribute to each prediction
- **Feature Importance**: See what matters most across your organization
- **Individual Explanations**: Drill down into any employee's risk factors
- **Visual Interpretations**: Interactive charts make insights accessible to non-technical users

### 🎯 Actionable Insights
- **Retention Recommendations**: AI-generated strategies tailored to each employee
- **Intervention Simulation**: Model the impact of changes before implementation
- **Priority Ranking**: Focus on the highest-risk employees first
- **Trend Analysis**: Track risk levels over time

### 📈 Interactive Dashboard
- **Real-time Analytics**: Live workforce attrition metrics
- **Risk Distribution**: Visual breakdown of low/medium/high risk employees
- **Department Analysis**: Compare attrition risk across teams
- **Employee Search**: Quickly find and analyze any employee from 1,470 records

### 🔧 Enterprise Ready
- **RESTful API**: Easy integration with existing HR systems
- **Docker Support**: Containerized deployment option
- **SQLite/PostgreSQL**: Flexible database options
- **Scalable Architecture**: Handles thousands of employees

---

## 📸 Application Views

### Dashboard View
```
┌─────────────────────────────────────────────────────────────────────┐
│  📊 PeoplePulse - Attrition Analytics                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │   1,470  │  │   16.1%  │  │    237   │  │    89%   │            │
│  │Employees │  │Avg. Risk │  │High Risk │  │ Accuracy │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│                                                                     │
│  [Run Attrition Predictions]                                        │
│                                                                     │
│  Risk Distribution          │  Department Breakdown                 │
│  ████████████ Low: 892      │  Sales: 24% avg risk                  │
│  ██████ Medium: 341         │  R&D: 14% avg risk                    │
│  ████ High: 237             │  HR: 19% avg risk                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Employee Detail View
```
┌─────────────────────────────────────────────────────────────────────┐
│  👤 Employee: EMP0042 - Sales Executive                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Attrition Risk: 73% [████████████████████░░░░░] HIGH RISK          │
│                                                                     │
│  Top Risk Factors (SHAP Analysis):                                  │
│  ├─ Overtime: Yes                    (+18.5%)                       │
│  ├─ Job Satisfaction: Low (2/4)      (+12.3%)                       │
│  ├─ Years Since Promotion: 4         (+9.7%)                        │
│  ├─ Monthly Income: $3,200           (+7.2%)                        │
│  └─ Work-Life Balance: Poor (1/4)    (+5.8%)                        │
│                                                                     │
│  💡 Recommendations:                                                │
│  • Review workload and overtime requirements                        │
│  • Consider promotion or role enrichment                            │
│  • Discuss compensation adjustment                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          PeoplePulse Architecture                       │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   ┌──────────────────┐         ┌──────────────────┐                   │
│   │                  │  HTTP   │                  │                   │
│   │   Streamlit UI   │◄───────►│  FastAPI Backend │                   │
│   │   (Port 8501)    │  JSON   │   (Port 8000)    │                   │
│   │                  │         │                  │                   │
│   │  • Dashboard     │         │  • REST API      │                   │
│   │  • Employee      │         │  • Predictions   │                   │
│   │    Search        │         │  • SHAP Service  │                   │
│   │  • SHAP Charts   │         │  • Data Mgmt     │                   │
│   │                  │         │                  │                   │
│   └──────────────────┘         └────────┬─────────┘                   │
│                                         │                              │
│                          ┌──────────────┼──────────────┐              │
│                          │              │              │              │
│                          ▼              ▼              ▼              │
│                   ┌──────────┐   ┌──────────┐   ┌──────────┐          │
│                   │          │   │          │   │          │          │
│                   │  SQLite  │   │ XGBoost  │   │   SHAP   │          │
│                   │ Database │   │  Model   │   │ Explainer│          │
│                   │          │   │          │   │          │          │
│                   └──────────┘   └──────────┘   └──────────┘          │
│                                                                        │
│                          ┌──────────────────┐                          │
│                          │   CSV Dataset    │                          │
│                          │  (1,470 Records) │                          │
│                          └──────────────────┘                          │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.109+ | High-performance async REST API framework |
| **Uvicorn** | 0.27+ | ASGI server for FastAPI |
| **SQLAlchemy** | 2.0+ | ORM for database operations |
| **Pydantic** | 2.5+ | Data validation and serialization |
| **SQLite** | - | Lightweight database (local development) |

### Machine Learning
| Technology | Version | Purpose |
|------------|---------|---------|
| **XGBoost** | 2.0+ | Gradient boosting for predictions |
| **LightGBM** | 4.3+ | Alternative gradient boosting model |
| **scikit-learn** | 1.4.0 | ML utilities and preprocessing |
| **SHAP** | 0.44+ | Explainable AI / feature importance |
| **imbalanced-learn** | 0.12+ | Handle class imbalance |
| **Pandas** | 2.1+ | Data manipulation |
| **NumPy** | 1.26+ | Numerical computing |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Streamlit** | 1.52+ | Interactive web dashboard |
| **Plotly** | 5.0+ | Interactive visualizations |

### DevOps (Optional)
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **MLflow** | Experiment tracking |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** installed
- **Git** for cloning the repository

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/peoplepulse.git
cd peoplepulse
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy python-dotenv python-multipart joblib xgboost scikit-learn==1.4.0 shap imbalanced-learn streamlit plotly requests pandas numpy
```

### Step 4: Start the Application

**Option A: One-Click Start (Windows)**
```bash
start.bat
```

**Option B: Manual Start**

Terminal 1 - Backend:
```bash
# Windows
set DATABASE_URL=sqlite:///./test.db
set MODEL_PATH=ml\models\model.pkl
set PYTHONPATH=backend;ml\pipeline
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# Linux/Mac
export DATABASE_URL=sqlite:///./test.db
export MODEL_PATH=ml/models/model.pkl
export PYTHONPATH=backend:ml/pipeline
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
streamlit run streamlit_app.py --server.port 8501
```

### Step 5: Access the Platform
| Service | URL |
|---------|-----|
| **Dashboard** | http://localhost:8501 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

---

## 📁 Project Structure

```
peoplepulse/
│
├── 📂 backend/                    # FastAPI Backend
│   ├── 📂 app/
│   │   ├── main.py               # Application entry point
│   │   ├── config.py             # Configuration settings
│   │   ├── db.py                 # Database connection
│   │   ├── 📂 routers/           # API endpoints
│   │   │   ├── predict.py        # Prediction endpoints
│   │   │   ├── employees.py      # Employee CRUD
│   │   │   └── simulate.py       # Intervention simulation
│   │   ├── 📂 models/            # SQLAlchemy models
│   │   │   ├── employee.py       # Employee model
│   │   │   └── prediction.py     # Prediction model
│   │   ├── 📂 schemas/           # Pydantic schemas
│   │   │   ├── employee_schema.py
│   │   │   └── predict_schema.py
│   │   └── 📂 services/          # Business logic
│   │       ├── model_service.py  # ML model operations
│   │       ├── shap_service.py   # SHAP explanations
│   │       └── feature_service.py # Feature engineering
│   ├── Dockerfile
│   └── requirements.txt
│
├── 📂 ml/                         # Machine Learning Pipeline
│   ├── 📂 pipeline/
│   │   ├── train.py              # Model training script
│   │   ├── preprocess.py         # Data preprocessing
│   │   ├── evaluate.py           # Model evaluation
│   │   ├── explain.py            # SHAP analysis
│   │   └── config.yaml           # ML configuration
│   ├── 📂 models/
│   │   ├── model.pkl             # Trained XGBoost model
│   │   └── metrics.json          # Model performance metrics
│   ├── 📂 notebooks/             # Jupyter notebooks for EDA
│   └── requirements.txt
│
├── 📂 data/
│   ├── 📂 raw/
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv  # IBM HR Dataset (1,470 employees)
│   └── 📂 processed/             # Processed datasets
│
├── 📂 infra/                      # Infrastructure (Optional)
│   ├── docker-compose.yml        # Docker orchestration
│   ├── postgres-init.sql         # PostgreSQL setup
│   ├── start.sh                  # Linux/Mac startup
│   └── start.ps1                 # Windows PowerShell startup
│
├── 📄 streamlit_app.py           # Streamlit Frontend (Dashboard + Search)
├── 📄 start.bat                  # Windows batch startup script
├── 📄 requirements-streamlit.txt # Frontend dependencies
├── 📄 .gitignore
├── 📄 LICENSE                    # MIT License
└── 📄 README.md
```

---

## 📊 API Reference

### Health Check
```http
GET /health
```
Returns backend status and model availability.

**Response:**
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
Predict attrition risk for one employee.

**Request Body:**
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
Predict attrition for multiple employees at once.

**Request Body:**
```json
{
  "employees": [
    { "employee_id": "EMP001", "age": 35, ... },
    { "employee_id": "EMP002", "age": 42, ... }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "employee_id": "EMP001",
      "attrition_probability": 0.23,
      "risk_level": "Low",
      "shap_values": { ... }
    },
    {
      "employee_id": "EMP002",
      "attrition_probability": 0.67,
      "risk_level": "High",
      "shap_values": { ... }
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
Model the impact of a retention intervention.

**Request Body:**
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

## 📋 Dataset

PeoplePulse uses the **IBM HR Analytics Employee Attrition** dataset:

| Feature | Description | Type |
|---------|-------------|------|
| `Age` | Employee age | Integer |
| `Department` | Work department (Sales, R&D, HR) | Category |
| `JobRole` | Job position | Category |
| `MonthlyIncome` | Monthly salary | Integer |
| `OverTime` | Works overtime | Yes/No |
| `YearsAtCompany` | Tenure at company | Integer |
| `JobSatisfaction` | Satisfaction rating (1-4) | Integer |
| `WorkLifeBalance` | Balance rating (1-4) | Integer |
| `EnvironmentSatisfaction` | Environment rating (1-4) | Integer |
| `NumCompaniesWorked` | Previous employers | Integer |
| ... | **35 total features** | ... |

**Dataset Statistics:**
- **Total Employees**: 1,470
- **Attrition Rate**: ~16%
- **Features**: 35 attributes per employee
- **Source**: IBM HR Analytics

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./test.db` |
| `MODEL_PATH` | Path to trained ML model | `ml/models/model.pkl` |
| `PYTHONPATH` | Python module paths | `backend;ml/pipeline` |
| `DEBUG` | Enable debug mode | `False` |

### ML Pipeline Configuration (`ml/pipeline/config.yaml`)

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

## 🧪 Model Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | 89% |
| **Precision** | 85% |
| **Recall** | 78% |
| **F1-Score** | 81% |
| **AUC-ROC** | 0.87 |

---

## 🔒 Security & Privacy

- ⚠️ **Never commit real employee data** to version control
- 🔐 Use environment variables for sensitive configuration
- 🛡️ Implement authentication for production deployments
- 📜 Follow GDPR/CCPA compliance for employee data
- 🔒 Anonymize data before training models

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IBM HR Analytics Dataset** - Sample data source
- **FastAPI** - Modern Python web framework
- **Streamlit** - Rapid dashboard development
- **XGBoost & SHAP** - ML and explainability
- **scikit-learn** - Machine learning utilities

---

## 📧 Support

For questions, issues, or feature requests:
- 📫 Open an issue on GitHub
- 💬 Start a discussion

---

<div align="center">

**Built with ❤️ for better employee retention**

⭐ Star this repo if you find it useful!

</div>
