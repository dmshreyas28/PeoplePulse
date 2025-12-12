# Kaggle Dataset Setup Instructions

## Step 1: Get Your Kaggle API Key

1. Go to https://www.kaggle.com/ and sign in (or create an account)
2. Click on your profile picture (top right) → **Settings**
3. Scroll down to the **API** section
4. Click **"Create New Token"**
5. This will download a file called `kaggle.json`

## Step 2: Place Your Kaggle Credentials

**Option A - Using Environment Variables (Recommended for this session):**
```powershell
# Set these in PowerShell:
$env:KAGGLE_USERNAME = "your_username"
$env:KAGGLE_KEY = "your_api_key"
```

**Option B - Using kaggle.json file:**
Place the `kaggle.json` file in: `C:\Users\YourUsername\.kaggle\kaggle.json`

## Step 3: Download the Dataset

Once credentials are set, run:
```powershell
cd e:\PeoplePulse\ml
.\.venv\Scripts\kaggle datasets download -d pavansubhasht/ibm-hr-analytics-attrition-dataset -p ../data/raw --unzip
```

This will download the IBM HR Analytics dataset (~1,470 employees, 35 features) to your data/raw folder.

## Dataset Details

- **Name:** IBM HR Analytics Employee Attrition & Performance
- **Size:** ~300 KB
- **Records:** 1,470 employees
- **Features:** 35 columns including:
  - Demographics (Age, Gender, Marital Status)
  - Job details (Department, Job Role, Job Level)
  - Compensation (Monthly Income, Salary Hike, Stock Options)
  - Satisfaction metrics (Job, Environment, Relationship, Work-Life Balance)
  - Performance (Performance Rating)
  - **Target:** Attrition (Yes/No)

## Alternative: Manual Download

If you prefer manual download:
1. Go to https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
2. Click "Download"
3. Extract the CSV file to `e:\PeoplePulse\data\raw\`
4. Rename it to `hr_attrition.csv` (or update the config path)
