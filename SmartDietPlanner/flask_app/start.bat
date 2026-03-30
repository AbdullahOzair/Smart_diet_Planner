@echo off
setlocal
cd /d "%~dp0"

set "PG_HOST=localhost"
set "PG_PORT=5000"
set "PG_DATABASE=smart_diet_planner"
set "PG_USER=postgres"
set "PG_PASSWORD=zainab"

set "APP_PORT=4001"
if not "%PORT%"=="" set "APP_PORT=%PORT%"

set "PYTHON_CMD=python"
if exist "%~dp0..\venv\Scripts\python.exe" set "PYTHON_CMD=%~dp0..\venv\Scripts\python.exe"

echo ============================================================================
echo Smart Diet ^& Lifestyle Planner - Flask Application
echo ============================================================================
echo.
echo PostgreSQL target: %PG_HOST%:%PG_PORT% (database: %PG_DATABASE%)
echo If this is first run, execute ..\setup_client.bat once before starting app.
echo.

echo [1] Installing dependencies...
"%PYTHON_CMD%" -m pip install -r requirements.txt

echo.
echo [2] Starting Flask application...
echo.
echo Application will be available at: http://localhost:%APP_PORT%
echo.
echo Demo Credentials:
echo   Admin: zainab_moazzam
echo   User:  test_user1
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================================================

set "PORT=%APP_PORT%"
set "PG_HOST=%PG_HOST%"
set "PG_PORT=%PG_PORT%"
set "PG_DATABASE=%PG_DATABASE%"
set "PG_USER=%PG_USER%"
set "PG_PASSWORD=%PG_PASSWORD%"
set "PGPASSWORD=%PG_PASSWORD%"
"%PYTHON_CMD%" app.py

pause
