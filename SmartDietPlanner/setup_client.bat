@echo off
setlocal
cd /d "%~dp0"

set "PG_HOST=localhost"
set "PG_PORT=5000"
set "PG_DATABASE=smart_diet_planner"
set "PG_USER=postgres"
set "PG_PASSWORD=zainab"
if not "%DB_HOST%"=="" set "PG_HOST=%DB_HOST%"
if not "%DB_PORT%"=="" set "PG_PORT=%DB_PORT%"
if not "%DB_DATABASE%"=="" set "PG_DATABASE=%DB_DATABASE%"
if not "%DB_USER%"=="" set "PG_USER=%DB_USER%"
if not "%DB_PASSWORD%"=="" set "PG_PASSWORD=%DB_PASSWORD%"

set "PYTHON_CMD=python"
if exist "%~dp0venv\Scripts\python.exe" set "PYTHON_CMD=%~dp0venv\Scripts\python.exe"

echo ============================================================================
echo Smart Diet Planner - One-Time Setup
echo ============================================================================
echo Using PostgreSQL host: %PG_HOST%:%PG_PORT%
echo Database: %PG_DATABASE%
echo.

where psql >nul 2>nul
if errorlevel 1 (
    echo [ERROR] psql not found in PATH.
    echo Install PostgreSQL or add psql to your system PATH first.
    goto :fail
)

echo [1/6] Installing Flask app dependencies...
"%PYTHON_CMD%" -m pip install -r flask_app\requirements.txt
if errorlevel 1 goto :fail

echo [2/6] Recreating tables...
set "PGPASSWORD=%PG_PASSWORD%"
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -d %PG_DATABASE% -f database\create_tables.sql
if errorlevel 1 goto :fail

echo [3/6] Creating functions...
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -d %PG_DATABASE% -f database\functions.sql
if errorlevel 1 goto :fail

echo [4/6] Creating procedures...
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -d %PG_DATABASE% -f database\procedures.sql
if errorlevel 1 goto :fail

echo [5/6] Creating triggers...
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -d %PG_DATABASE% -f database\triggers.sql
if errorlevel 1 goto :fail

echo [6/6] Seeding realistic demo data...
set "PG_HOST=%PG_HOST%"
set "PG_PORT=%PG_PORT%"
set "PG_DATABASE=%PG_DATABASE%"
set "PG_USER=%PG_USER%"
set "PG_PASSWORD=%PG_PASSWORD%"
set "PGPASSWORD=%PG_PASSWORD%"
"%PYTHON_CMD%" setup_database.py
if errorlevel 1 goto :fail

echo.
echo Setup completed successfully.
echo Next step: run flask_app\start.bat
goto :end

:fail
echo.
echo Setup failed. Check PostgreSQL credentials / connection and rerun.
exit /b 1

:end
endlocal