# PeoplePulse 🎯

**Employee Attrition Prediction & Retention Platform**

PeoplePulse is a production-grade, full-stack AI platform that predicts employee attrition risk, explains predictions using SHAP, and provides actionable retention recommendations for HR teams.

![Tech Stack](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **🤖 ML-Powered Predictions**: XGBoost/LightGBM models for accurate attrition prediction
- **📊 Explainable AI**: SHAP values explain each prediction's contributing factors
- **🎯 Risk Prioritization**: Automatic classification into Low/Medium/High risk tiers
- **💡 Actionable Insights**: AI-generated retention recommendations
- **🔄 Intervention Simulation**: Model the impact of retention strategies before implementation
- **📈 Interactive Dashboard**: Real-time visualization of workforce attrition risk
- **🐳 Docker-Ready**: Complete containerized deployment
- **🔬 MLflow Integration**: Experiment tracking and model versioning

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│                 │      │                  │      │                 │
│  React Frontend │◄────►│  FastAPI Backend │◄────►│   PostgreSQL    │
│   (Dashboard)   │      │   (REST API)     │      │    Database     │
│                 │      │                  │      │                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │                  │
                         │  ML Pipeline     │
                         │  XGBoost + SHAP  │
                         │  MLflow Tracking │
                         │                  │
                         └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/peoplepulse.git
cd peoplepulse
```

### 2. Start the Platform (Docker)

**Windows (PowerShell):**
```powershell
.\infra\start.ps1
```

**Linux/Mac:**
```bash
chmod +x infra/start.sh
./infra/start.sh
```

**Or manually:**
```bash
cd infra
docker-compose up --build
```

### 3. Train the ML Model

```bash
# Create Python virtual environment
cd ml
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python pipeline/train.py --config pipeline/config.yaml
```

The trained model will be saved to `ml/models/model.pkl` (the single source of truth) and automatically loaded by the backend.

### 4. Access the Platform

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000
- **PgAdmin**: http://localhost:5050

## 📁 Project Structure

```
peoplepulse/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── routers/        # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic (ML, SHAP)
│   │   ├── db.py           # Database configuration
│   │   └── config.py       # App settings
│   ├── Dockerfile
│   └── requirements.txt
│
├── ml/                      # Machine Learning pipeline
│   ├── notebooks/          # Jupyter notebooks for EDA
│   ├── pipeline/
│   │   ├── preprocess.py   # Data preprocessing
│   │   ├── train.py        # Model training
│   │   ├── evaluate.py     # Model evaluation
│   │   ├── explain.py      # SHAP explanations
│   │   └── config.yaml     # Pipeline configuration
│   ├── models/             # Trained models
│   └── requirements.txt
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/         # Dashboard & detail pages
│   │   ├── components/    # Reusable UI components
│   │   ├── api.js         # API client
│   │   └── App.jsx        # Main app component
│   ├── Dockerfile
│   └── package.json
│
├── infra/                  # Infrastructure & deployment
│   ├── docker-compose.yml # Multi-container orchestration
│   ├── postgres-init.sql  # Database initialization
│   ├── start.sh           # Quick start script (Linux/Mac)
│   └── start.ps1          # Quick start script (Windows)
│
├── data/
│   ├── raw/               # Raw datasets
│   └── processed/         # Processed datasets
│
└── README.md
```

## 🔧 Configuration

### Backend Configuration (`.env`)

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/peoplepulse
SECRET_KEY=your-secret-key
MODEL_PATH=./models/model.pkl
MLFLOW_TRACKING_URI=http://localhost:5000
DEBUG=True
```

### ML Pipeline Configuration (`ml/pipeline/config.yaml`)

```yaml
data:
  raw_path: "../data/raw/hr_attrition.csv"
  
model:
  algorithm: "xgboost"  # xgboost, lightgbm, random_forest
  hyperparameters:
    n_estimators: 100
    max_depth: 6
    learning_rate: 0.1
```

## 📊 API Endpoints

### Predictions

- `POST /api/predict/employee` - Predict single employee attrition
- `POST /api/predict/batch` - Batch prediction for multiple employees
- `GET /api/predict/history/{employee_id}` - Prediction history

### Simulations

- `POST /api/simulate/intervention` - Simulate retention intervention impact
- `POST /api/simulate/compare` - Compare multiple intervention scenarios

### Employee Management

- `GET /api/employees` - List all employees
- `GET /api/employees/{id}` - Get employee details
- `POST /api/employees` - Create new employee
- `PUT /api/employees/{id}` - Update employee
- `DELETE /api/employees/{id}` - Delete employee

### Health

- `GET /health` - Service health check

## 🧪 Development

### Backend Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Run Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📈 Model Training & MLflow

The ML pipeline supports experiment tracking with MLflow:

1. Start MLflow server (if not using Docker):
   ```bash
   mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
   ```

2. Train model with tracking:
   ```bash
   python ml/pipeline/train.py --config ml/pipeline/config.yaml
   ```

3. View experiments at http://localhost:5000

## 🎨 Frontend Features

- **Dashboard**: Overview of workforce attrition risk with KPIs
- **Risk Table**: Sortable list of employees by risk level
- **Employee Detail**: Deep dive into individual risk factors
- **SHAP Visualizations**: Bar charts showing feature impacts
- **Recommendations**: AI-generated retention strategies

## 🔒 Security & Privacy

- Never commit real employee data
- Use environment variables for sensitive configuration
- Implement proper authentication (not included in demo)
- Follow GDPR/CCPA compliance for employee data
- Anonymize data before training models

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- IBM HR Analytics Dataset (sample data source)
- FastAPI framework
- React & Recharts
- XGBoost, SHAP, and scikit-learn communities
- Docker & MLflow

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for better employee retention**
