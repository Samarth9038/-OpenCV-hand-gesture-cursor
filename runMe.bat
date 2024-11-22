@echo off
setlocal enabledelayedexpansion

echo Creating virtual environment...

if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate.bat

python -c "import sys; print('Python executable:', sys.executable)"

python -m pip install --upgrade pip

if exist requirements.txt (
    echo Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install packages. Check your requirements.txt or internet connection.
        pause
        exit /b 1
    )
) else (
    echo No requirements.txt found.
)

cls

echo Running...

python fingerCursor.py
if errorlevel 1 (
    echo Error running main.py. Module not found or other issue.
    pause
    exit /b 1
)

pause
