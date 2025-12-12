# Copilot Prompt & Developer Guide for PeoplePulse
**Employee Attrition Prediction & Retention Platform**

This file (copilot_prompt.md) is a detailed instruction document to guide GitHub Copilot, you, or any developer to build **PeoplePulse** — a full‑stack, production‑grade employee attrition prediction platform using VS Code. It contains: project overview, folder structure, coding conventions, detailed dependencies, setup steps, step‑by‑step build process, and task prompts for Copilot.

---

## Project summary (one line)
PeoplePulse predicts employee attrition, explains reasons using SHAP, prioritizes retention actions, and provides a web dashboard for HR managers.

---

## Tech stack (recommended)
- **Language**: Python 3.10+ (backend, ML)
- **Backend**: FastAPI, Uvicorn/Gunicorn
- **ML / Data**: pandas, numpy, scikit-learn, XGBoost or LightGBM, imbalanced-learn, SHAP, joblib
- **Database**: PostgreSQL (psycopg2 or asyncpg)
- **ORM**: SQLAlchemy (or Tortoise for async)
- **Frontend**: React (Vite or Create React App) or Next.js, Axios, Recharts/D3
- **Orchestration**: Docker, docker-compose
- **Workflow / CI**: GitHub Actions
- **Experiment tracking**: MLflow
- **Optional**: Apache Airflow for ETL / retrain DAGs
- **Monitoring**: Prometheus + Grafana (optional), Sentry (app errors)
- **Dev environment**: VS Code with extensions:
  - Python (ms-python.python)
  - Pylance
  - Docker
  - GitHub Copilot
  - ESLint / Prettier (for frontend)
  - Remote - Containers (optional)

---

## Folder structure (single-source-of-truth)
```
peoplepulse/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── predict.py
│   │   │   ├── simulate.py
│   │   │   ├── employees.py
│   │   ├── models/
│   │   │   ├── employee.py
│   │   │   ├── prediction.py
│   │   ├── services/
│   │   │   ├── model_service.py
│   │   │   ├── shap_service.py
│   │   │   ├── feature_service.py
│   │   ├── schemas/
│   │   │   ├── employee_schema.py
│   │   │   ├── predict_schema.py
│   │   ├── db.py
│   │   ├── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│
├── ml/
│   ├── notebooks/
│   │   ├── EDA.ipynb
│   │   ├── training.ipynb
│   ├── pipeline/
│   │   ├── preprocess.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   ├── explain.py
│   │   ├── config.yaml
│   ├── models/
│   │   ├── model.pkl
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── index.jsx
│   │   │   ├── employee/
│   │   │   │   └── [id].jsx
│   │   ├── components/
│   │   │   ├── RiskTable.jsx
│   │   │   ├── RiskCard.jsx
│   │   │   ├── ShapChart.jsx
│   ├── package.json
│   ├── Dockerfile
│
├── infra/
│   ├── docker-compose.yml
│   ├── postgres-init.sql
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── README.md
└── copilot_prompt.md
```

---

## Key files explained (short)
- `backend/app/main.py` — FastAPI app starter, include routers, startup tasks (load model).
- `backend/app/routers/predict.py` — endpoints for single and batch predictions.
- `backend/app/services/model_service.py` — load model, preprocess, predict, simulate.
- `ml/pipeline/train.py` — training script: preprocessing, training, MLflow logging, save model.
- `frontend/src/pages/index.jsx` — dashboard (risk list, KPIs).
- `infra/docker-compose.yml` — app, postgres, pgadmin, optional mlflow UI.

---

## Dependencies (install lists)

### Backend `backend/requirements.txt` (recommended)
```
fastapi
uvicorn[standard]
pydantic
sqlalchemy
psycopg2-binary
python-dotenv
joblib
pandas
numpy
scikit-learn
xgboost
lightgbm
shap
mlflow
imbalanced-learn
alembic
```

### ML `ml/requirements.txt` (for notebooks)
```
pandas
numpy
scikit-learn
xgboost
lightgbm
shap
matplotlib
seaborn
jupyterlab
mlflow
joblib
imbalanced-learn
sdv  # optional synthetic data
```

### Frontend `package.json` (dependencies snippet)
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "axios": "^1.0.0",
    "recharts": "^2.1.9"
  },
  "devDependencies": {
    "vite": "^4.0.0"
  }
}
```

---

## Environment variables (example `.env`)
```
# Backend
DATABASE_URL=postgresql://postgres:postgres@db:5432/peoplepulse
SECRET_KEY=replace_with_secure_key
MODEL_PATH=/app/models/model.pkl

# MLFLOW
MLFLOW_TRACKING_URI=http://mlflow:5000

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
```

---

## Step-by-step build & run guide (detailed)

> The steps below assume you are working locally with VS Code, Docker & Docker Compose installed.

### 0. Pre-setup (one-time)
1. Install system dependencies:
   - Docker & Docker Compose
   - VS Code
   - Git
   - Python 3.10+
   - Node.js & npm
2. Install VS Code extensions:
   - Python, Pylance, Docker, GitHub Copilot, ESLint, Prettier

### 1. Clone repo & initial scaffold
```bash
git clone <your-repo-url>
cd peoplepulse
# create folders if scaffold not present
mkdir -p backend app ml frontend infra data
```

### 2. Create virtual envs (optional but recommended)
**Backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
**ML (notebook environment)**
```bash
cd ml
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**Frontend**
```bash
cd frontend
npm install
```

### 3. Local Docker run (quickstart)
A `docker-compose.yml` in `infra/` should bring up:
- `db` (Postgres)
- `backend`
- `frontend`
- `mlflow` (optional)
Example:
```bash
cd infra
docker-compose up --build
```
Check:
- Backend at `http://localhost:8000/docs`
- Frontend at `http://localhost:3000` (or configured port)
- Postgres running & initialized by `postgres-init.sql`

### 4. Prepare dataset & run training (ML)
1. Place sample dataset (IBM HR Attrition CSV) into `data/raw/`.
2. Activate ml env: `cd ml && source .venv/bin/activate`.
3. Run training:
```bash
python pipeline/train.py --config pipeline/config.yaml
```
This should:
- Read raw CSV
- Preprocess, engineer features
- Train XGBoost/LightGBM
- Save `model.pkl` in `ml/models/`
- Log metrics/artifacts to MLflow (if configured)

### 5. Load model into backend
- Copy `ml/models/model.pkl` to `backend/app/models/` or update `MODEL_PATH`.
- Start backend (if not running via docker):
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Open `http://localhost:8000/docs` to test endpoints.

### 6. Frontend integration
- Update `REACT_APP_API_URL` env variable in frontend `.env`.
- Run frontend dev server:
```bash
cd frontend
npm run dev
```
- Open the dashboard and ensure API calls hit the backend.

### 7. Retrain & scheduled jobs
- For production use Airflow or a cron job to run `train.py` periodically.
- Use MLflow registry to promote models to Production stage and update backend MODEL_PATH accordingly.

### 8. Monitoring & alerts
- Configure Prometheus & Grafana (if using) via docker-compose
- Add data-drift and performance alerts (compare daily AUC vs baseline)
- Use Sentry for backend error monitoring

---

## Detailed task prompts (copy‑paste prompts for Copilot)
Use these prompts in VS Code with Copilot to generate specific files.

### Prompt: "Generate FastAPI backend skeleton"
```
# Generate a FastAPI backend skeleton.
# Create folders: app/, app/routers, app/services, app/schemas, app/models.
# main.py should instantiate FastAPI, include routers, and load a persisted ML model at startup.
# Use Pydantic schemas for endpoints.
# Add Dockerfile and requirements.txt.
```

### Prompt: "Create training script using XGBoost"
```
# Create ml/pipeline/train.py
# Load CSV from data/raw/hr_attrition.csv
# Implement preprocessing: impute, one-hot or target encode categorical, scale numeric.
# Train an XGBoostClassifier with early stopping and log metrics to MLflow.
# Save trained pipeline (preprocessor + model) as ml/models/model.pkl using joblib.
```

### Prompt: "Create /api/predict/employee endpoint"
```
# Create a FastAPI router endpoint /api/predict/employee
# Accept Pydantic Employee schema, run preprocessing, load model, return probability and top-5 SHAP explanations.
# Use dependency injection to reuse loaded model.
```

### Prompt: "Generate React dashboard with risk table"
```
# Create frontend/src/pages/index.jsx and components/RiskTable.jsx
# Build a page that fetches /api/predict/batch or /api/employee list and displays a table sorted by probability desc.
# Add a RiskCard showing KPI tiles (avg risk, flagged count).
```

---

## Best practices & notes
- **Data privacy**: never commit PII to git. Use synthetic data or anonymize.
- **Explainability**: show SHAP per prediction; make human-in-loop mandatory for actions.
- **Fairness**: evaluate model across protected groups; avoid using protected attributes in decisions.
- **Testing**: unit tests for preprocessors & API endpoints. Integration test for end-to-end prediction.
- **Documentation**: produce a project README, model card, and ethics statement.

---

## Quick checklist before demoing
- ✅ Model training completes and `model.pkl` exists
- ✅ Backend loads model and /api/predict endpoints return probabilities
- ✅ Frontend displays risk table and employee detail with SHAP bars
- ✅ Docker-compose can bring up the stack
- ✅ No PII in repo
- ✅ README explains how to run locally and deploy

---

## Helpful commands summary
```bash
# build backend image
docker build -t peoplepulse-backend ./backend

# start infra stack
docker-compose -f infra/docker-compose.yml up --build

# run training (local)
cd ml
python pipeline/train.py --config pipeline/config.yaml

# run backend locally
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# run frontend locally
cd frontend
npm run dev
```

---

## Licensing & contribution
- Use MIT license for the repo
- Include CONTRIBUTING.md with coding standards and PR process
- Add SECURITY.md with contact for disclosure of vulnerabilities

---

## Next steps I can generate for you (pick one)
1. Full repo skeleton (files + minimal code) scaffolded now.  
2. `train.py` notebook + XGBoost baseline + MLflow logging.  
3. FastAPI starter app with predict endpoint and model service.  
4. React dashboard starter with RiskTable and ShapChart.  
5. Docker-compose and infra scaffolding.

If you want the downloadable `.md` file now, I will save this content to `copilot_prompt.md` and provide a download link.
