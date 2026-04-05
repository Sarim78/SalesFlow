@echo off
echo =====================================================
echo          SalesFlow - Automated Setup
echo =====================================================
echo.

REM -------------------------------------------------------
REM Step 1 - Create Virtual Environment
REM -------------------------------------------------------
echo [1/5] Creating virtual environment...
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
echo [2/5] Activating virtual environment...
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
echo [3/5] Installing dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [OK] Dependencies installed.
echo.

REM -------------------------------------------------------
REM Step 4 - Create PostgreSQL Database and Run Schema
REM -------------------------------------------------------
echo [4/5] Setting up PostgreSQL database...
echo.
echo IMPORTANT: You will need to enter your PostgreSQL password.
echo.
psql -U postgres -c "CREATE DATABASE salesflow;" 2>nul
psql -U postgres -d salesflow -f sql/schema.sql
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run schema.
    echo Make sure PostgreSQL is running and your .env is configured.
    pause
    exit /b 1
)
echo [OK] Database and schema ready.
echo.

REM -------------------------------------------------------
REM Step 5 - Run ETL Pipeline
REM -------------------------------------------------------
echo [5/5] Running ETL pipeline...
python main.py
if %errorlevel% neq 0 (
    echo [ERROR] Pipeline failed.
    echo Make sure your .env file is configured with your database credentials.
    pause
    exit /b 1
)
echo.
echo =====================================================
echo   Done! Data is now loaded into PostgreSQL.
echo   Open Power BI and connect to your database.
echo   Server: localhost  Database: salesflow
echo =====================================================
pause