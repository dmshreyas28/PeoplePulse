@echo off
cd /d E:\PeoplePulse
echo Starting PeoplePulse Streamlit Frontend...
echo ==========================================
.venv\Scripts\streamlit.exe run streamlit_app.py --server.port 8501 --server.headless true
