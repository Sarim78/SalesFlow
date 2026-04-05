@echo off
echo =====================================================
echo          SalesFlow - Automated Setup
echo =====================================================
echo.

REM -------------------------------------------------------
REM Step 1 - Create Virtual Environment
REM -------------------------------------------------------
echo [1/6] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    echo Make sure Python 3.11+ is installed: https://python.org/downloads
    pause
    exit /b 1
)
echo [OK] Virtual environment created.
echo.

REM -------------------------------------------------------
REM Step 2 - Activate Virtual Environment
REM -------------------------------------------------------
echo [2/6] Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated.
echo.

REM -------------------------------------------------------
REM Step 3 - Install Dependencies
REM -------------------------------------------------------
echo [3/6] Installing dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    echo Make sure requirements.txt exists in this folder.
    pause
    exit /b 1
)
echo [OK] Dependencies installed.
echo.

REM -------------------------------------------------------
REM Step 4 - Create PostgreSQL Database
REM -------------------------------------------------------
echo [4/6] Setting up PostgreSQL database...
echo.
echo IMPORTANT: You will need to enter your PostgreSQL password.
echo If the database already exists, this step will be skipped.
echo.

psql -U postgres -c "CREATE DATABASE salesflow;" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Database may already exist, continuing...
) else (
    echo [OK] Database created.
)
echo.

REM -------------------------------------------------------
REM Step 5 - Run Schema
REM -------------------------------------------------------
echo [5/6] Running database schema...
psql -U postgres -d salesflow -f sql/schema.sql
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run schema.
    echo Make sure PostgreSQL is running and sql/schema.sql exists.
    pause
    exit /b 1
)
echo [OK] Schema applied.
echo.

REM -------------------------------------------------------
REM Step 6 - Run ETL Pipeline
REM -------------------------------------------------------
echo [6/6] Running ETL pipeline...
python main.py
if %errorlevel% neq 0 (
    echo [ERROR] Pipeline failed.
    echo Make sure your .env file is configured with your database credentials.
    pause
    exit /b 1
)
echo [OK] Pipeline complete.
echo.

REM -------------------------------------------------------
REM Launch Dashboard
REM -------------------------------------------------------
echo =====================================================
echo   Setup complete! Launching dashboard...
echo   Open your browser at: http://localhost:8501
echo =====================================================
echo.
streamlit run dashboard/app.py