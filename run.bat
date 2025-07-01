@echo off
chcp 932 > nul
cd /d %~dp0

set PYTHON_VENV=%~dp0.venv
if exist "%PYTHON_VENV%\Scripts\activate.bat" (
    call "%PYTHON_VENV%\Scripts\activate.bat"
) else (
    python -m venv .venv
    call "%PYTHON_VENV%\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

python app.py
pause

