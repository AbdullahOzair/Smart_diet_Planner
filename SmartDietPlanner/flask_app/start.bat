@echo off
echo ============================================================================
echo Smart Diet & Lifestyle Planner - Flask Application
echo ============================================================================
echo.

echo [1] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2] Starting Flask application...
echo.
echo Application will be available at: http://localhost:5000
echo.
echo Demo Credentials:
echo   Admin: zainab_moazzam
echo   User:  test_user1
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================================================

python app.py

pause
