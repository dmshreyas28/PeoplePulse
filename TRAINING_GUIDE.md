# Training PeoplePulse with IBM HR Analytics Dataset

## 🎯 Quick Start (3 Steps)

### Step 1: Set Kaggle Credentials
```powershell
# Replace with your actual Kaggle username and API key
$env:KAGGLE_USERNAME = "your_username"
$env:KAGGLE_KEY = "your_api_key_here"
```

**Get your credentials:**
1. Go to https://www.kaggle.com/settings
2. Scroll to API section
3. Click "Create New Token"
4. Open the downloaded `kaggle.json` file to get your username and key

---

### Step 2: Download Dataset
```powershell
cd e:\PeoplePulse
.\download_dataset.ps1
```

This downloads ~1,470 employee records with 35 features.

---

### Step 3: Train the Model
```powershell
cd e:\PeoplePulse\ml
.\.venv\Scripts\python pipeline/train.py --config pipeline/config.yaml
```

Training will:
- ✅ Load 1,470 employee records
- ✅ Perform feature engineering
- ✅ Handle class imbalance with SMOTE
- ✅ Train XGBoost model with 5-fold cross-validation
- ✅ Save trained model to `ml/models/model.pkl`
- ✅ Generate evaluation metrics

---

## 📊 Dataset Details

**IBM HR Analytics Employee Attrition & Performance**
- **Records:** 1,470 employees
- **Features:** 35 columns
- **Target:** Attrition (Yes/No)
- **Class Distribution:** ~16% attrition rate (imbalanced)

**Key Features:**
- Demographics: Age, Gender, MaritalStatus
- Job Info: Department, JobRole, JobLevel, YearsAtCompany
- Compensation: MonthlyIncome, PercentSalaryHike, StockOptionLevel
- Satisfaction: JobSatisfaction, EnvironmentSatisfaction, WorkLifeBalance
- Performance: PerformanceRating
- Engineered Features: TenureRatio, PromotionRate, IncomePerAge, etc.

---

## 🔄 After Training

Once training completes:

1. **Copy model to backend:**
   ```powershell
   Copy-Item -Path "e:\PeoplePulse\ml\models\model.pkl" -Destination "e:\PeoplePulse\backend\models\model.pkl" -Force
   ```

2. **Start backend server:**
   ```powershell
   cd e:\PeoplePulse
   $env:DATABASE_URL='sqlite:///./test.db'
   $env:MODEL_PATH='e:\PeoplePulse\backend\models\model.pkl'
   $env:PYTHONPATH='e:\PeoplePulse\backend;e:\PeoplePulse\ml\pipeline'
   E:\PeoplePulse\ml\.venv\Scripts\python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   ```

3. **Test predictions:**
   - Open http://localhost:8000/docs
   - Try the `/predict` endpoint with employee data

---

## 📈 Expected Training Results

With the full IBM dataset, you should see:
- **Accuracy:** ~85-88%
- **ROC-AUC:** ~0.75-0.82
- **Precision:** ~0.60-0.70 (for attrition class)
- **Recall:** ~0.45-0.60 (for attrition class)
- **Cross-Validation:** Stable performance across 5 folds

---

## 🐛 Troubleshooting

**"Kaggle credentials not found"**
→ Set `$env:KAGGLE_USERNAME` and `$env:KAGGLE_KEY`

**"401 Unauthorized"**
→ Check your API key is correct in kaggle.json or environment variables

**"Dataset not found"**
→ The dataset URL may have changed. Download manually from:
   https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

**Training fails with import errors**
→ Make sure you're using the venv: `.\.venv\Scripts\python`

---

## 🎓 Model Improvements (Optional)

After training with full data, you can:

1. **Tune hyperparameters** in `config.yaml`:
   ```yaml
   model:
     hyperparameters:
       n_estimators: 200
       max_depth: 8
       learning_rate: 0.05
   ```

2. **Enable MLflow tracking**:
   - Start MLflow: `docker-compose up mlflow -d`
   - Set `use_mlflow: true` in config.yaml
   - View experiments at http://localhost:5000

3. **Try different algorithms**:
   - Change `algorithm: "lightgbm"` in config.yaml
   - Or use `algorithm: "random_forest"`
