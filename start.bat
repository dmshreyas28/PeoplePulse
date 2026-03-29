@echo off
echo ============================================
echo Starting PeoplePulse Application
echo ============================================
echo.

REM Get the directory where this script is located
set "PEOPLEPULSE_DIR=%~dp0"
REM Remove trailing backslash
if "%PEOPLEPULSE_DIR:~-1%"=="\" set "PEOPLEPULSE_DIR=%PEOPLEPULSE_DIR:~0,-1%"

REM Start Backend
echo [1/2] Starting Backend Server...
start "PeoplePulse Backend" cmd /k "cd /d "%PEOPLEPULSE_DIR%\backend" && set DATABASE_URL=sqlite:///./peoplepulse.db && set MODEL_PATH=%PEOPLEPULSE_DIR%\ml\models\model.pkl && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul

REM Start Streamlit Frontend
echo [2/2] Starting Streamlit Frontend...
start "PeoplePulse Streamlit" cmd /k "cd /d "%PEOPLEPULSE_DIR%" && streamlit run streamlit_app.py --server.port 8501"
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
