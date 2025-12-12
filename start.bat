@echo off
echo ============================================
echo Starting PeoplePulse Application
echo ============================================
echo.

REM Start Backend
echo [1/2] Starting Backend Server...
start "PeoplePulse Backend" cmd /k "cd /d E:\PeoplePulse && set DATABASE_URL=sqlite:///./test.db && set MODEL_PATH=e:\PeoplePulse\ml\models\model.pkl && set PYTHONPATH=e:\PeoplePulse\backend;e:\PeoplePulse\ml\pipeline && e:\PeoplePulse\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul

REM Start Streamlit Frontend
echo [2/2] Starting Streamlit Frontend...
start "PeoplePulse Streamlit" cmd /k "cd /d E:\PeoplePulse && e:\PeoplePulse\.venv\Scripts\streamlit.exe run streamlit_app.py --server.port 8501"
timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo PeoplePulse is starting up!
echo ============================================
echo.
echo Backend:   http://localhost:8000
echo Streamlit: http://localhost:8501
echo.
echo Press any key to open in browser...
pause >nul

start http://localhost:8501

echo.
echo Application is running!
echo Close the Backend and Streamlit windows to stop the servers.
echo.
pause
