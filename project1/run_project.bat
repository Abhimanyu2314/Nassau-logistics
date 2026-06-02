@echo off
cd /d "%~dp0"
echo ========================================
echo   Nassau Logistics AI - Starting App
echo ========================================
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Opening Streamlit app...
python -m streamlit run app.py
pause
