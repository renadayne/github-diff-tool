@echo off
echo ========================================
echo    Git Diff Tool
echo ========================================
echo.

REM Kiem tra neu co moi truong ao .venv
if exist ".venv\Scripts\python.exe" (
    echo [Info] Su dung moi truong ao .venv...
    ".venv\Scripts\python.exe" run.py
    goto :end
)

REM Kiem tra Python he thong
python --version >nul 2>&1
if errorlevel 1 (
    echo [Loi] Python chua duoc cai dat hoac khong co trong PATH
    echo Vui long cai dat Python tai: https://python.org
    pause
    exit /b 1
)

echo [Info] Khoi dong Git Diff Tool qua Python he thong...
python run.py

if errorlevel 1 (
    echo.
    echo [Loi] Khong the khoi dong ung dung.
    pause
    exit /b 1
)

:end